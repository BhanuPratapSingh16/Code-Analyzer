package com.codegraph.backend.fastapi.controller;

import com.codegraph.backend.fastapi.dto.FastApiResponse;
import com.codegraph.backend.fastapi.service.FastApiService;
import com.codegraph.backend.repo.dto.RepoStatus;
import com.codegraph.backend.repo.model.Repo;
import com.codegraph.backend.repo.service.RepoService;
import com.codegraph.backend.security.CustomUserDetails;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.UUID;

@RestController
@RequestMapping("/api/fastapi")
public class FastApiController {

    private static final long MAX_FILE_SIZE = 100L * 1024 * 1024;

    private final FastApiService fastApiService;
    private final RepoService repoService;

    @Autowired
    public FastApiController(FastApiService fastApiService, RepoService repoService){
        this.fastApiService = fastApiService;
        this.repoService = repoService;
    }

    @GetMapping("/connection")
    public String connection(){
        return fastApiService.checkConnection();
    }

    @PostMapping(value = "/{repoId}/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<?> uploadRepository(@PathVariable UUID repoId, @RequestParam("file")MultipartFile file, @AuthenticationPrincipal CustomUserDetails userDetails) throws IOException{
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("Please upload a non-empty ZIP file");
        }

        if (file.getSize() > MAX_FILE_SIZE) {
            return ResponseEntity.status(HttpStatus.CONTENT_TOO_LARGE).body("File size must not exceed 100 MB");
        }

        Repo repo = repoService.getRepoById(repoId, userDetails.getId());
        repo.setStatus(RepoStatus.INDEXING);
        repoService.save(repo);

        try{
            FastApiResponse response = fastApiService.uploadFile(repoId, file);

            repo.setStatus(RepoStatus.READY);
            repoService.save(repo);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            repo.setStatus(RepoStatus.FAILED);
            repoService.save(repo);

            throw e;
        }
    }

}
