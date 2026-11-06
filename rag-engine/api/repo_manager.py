import uuid
import shutil
import zipfile
from pathlib import Path, PurePosixPath
from config import REPOSITORY_ROOT, MAX_UPLOAD_SIZE, MAX_EXTRACTED_SIZE, MAX_FILES

class RepositoryManager:
    def __init__(self):
        REPOSITORY_ROOT.mkdir(parents=True, exist_ok=True)

    def save(self, zip_file:Path):
        repository_id = str(uuid.uuid4())
        
        storage_path = (REPOSITORY_ROOT / repository_id).resolve()
        if not storage_path.is_relative_to(REPOSITORY_ROOT):
            raise ValueError("Invalid repository storage path")
        
        if storage_path.exists():
            raise FileExistsError(f"Repository already exists: {repository_id}")
        
        storage_path.mkdir(parents=True, exist_ok=False)
        
        try:
            self._check_upload_size(zip_file)
            
            with zipfile.ZipFile(zip_file, "r") as archive:
                members = self._validate_archive(archive)
                
                if not members:
                    raise ValueError("ZIP archive is empty")
                
                for member in members:
                    self._extract_member(archive, member, storage_path)

            return repository_id, storage_path
        
        except Exception:
            shutil.rmtree(storage_path, ignore_errors=True)
            
    def _check_upload_size(self, zip_file:Path):
        size = zip_file.stat().st_size
        
        if size > MAX_UPLOAD_SIZE:
            raise ValueError(f"ZIP file exceeds maximum upload size of {MAX_UPLOAD_SIZE} MB")
        
    def _validate_archive(self, archive:zipfile.ZipFile):
        members = archive.infolist()
        
        if len(members) > MAX_FILES:
            raise ValueError(f"ZIP contains too many files. Maximum: {MAX_FILES} allowed")

        total_size = 0
        
        for member in members:
            filename = member.filename
            
            if not filename:
                raise ValueError("ZIP contains invalid filename")
            
            if "\\" in filename or "\x00" in filename:
                raise ValueError(f"Invalid ZIP path: {filename}")
            
            total_size += member.file_size
            
            if total_size > MAX_EXTRACTED_SIZE:
                raise ValueError("Extracted ZIP size exceeds the allowed limit")
            
        return members
        
    
    def _extract_member(self, archive:zipfile.ZipFile, member:zipfile.ZipInfo, storage_path:Path):
        relative_path = PurePosixPath(member.filename)
        
        destination = storage_path.joinpath(*relative_path.parts).resolve()
        
        if not destination.is_relative_to(storage_path):
            raise ValueError(f"ZIP entry escapes repository directory: {member.filename}")
        
        if member.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            return

        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Stream file contents
        with archive.open(member, "r") as source:
            with destination.open("wb") as target:
                shutil.copyfileobj(source, target, length=1024 * 1024)
