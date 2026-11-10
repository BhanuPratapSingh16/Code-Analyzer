package com.codegraph.backend.repo.service;

import com.codegraph.backend.repo.dto.RepoRequest;
import com.codegraph.backend.repo.dto.RepoResponse;
import com.codegraph.backend.repo.dto.RepoStatus;
import com.codegraph.backend.repo.model.Repo;
import com.codegraph.backend.repo.repository.RepoRepository;
import com.codegraph.backend.user.model.User;
import com.codegraph.backend.user.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class RepoService {

    private final RepoRepository repoRepository;
    private final UserRepository userRepository;

    @Autowired
    public RepoService(RepoRepository repoRepository, UserRepository userRepository){
        this.repoRepository = repoRepository;
        this.userRepository = userRepository;
    }

    public RepoResponse createRepository(RepoRequest request, UUID userId){
        Repo repo = Repo
                .builder()
                .name(request.getName())
                .status(RepoStatus.UPLOADED)
                .createdAt(Instant.now())
                .build();

        User user = userRepository.findById(userId).orElseThrow(() -> new RuntimeException("User not found!"));
        repo.setUser(user);

        Repo savedRepo = repoRepository.save(repo);

        return RepoResponse
                .builder()
                .id(savedRepo.getId())
                .name(savedRepo.getName())
                .status(savedRepo.getStatus())
                .createdAt(savedRepo.getCreatedAt())
                .userId(savedRepo.getUser().getId())
                .build();
    }

    public List<RepoResponse> getAllByUser(UUID userId) {
        List<Repo> repos = repoRepository.findAllByUserIdOrderByCreatedAtDesc(userId);

        List<RepoResponse> reposResponse = new ArrayList<>();
        for(Repo repo:repos){
            RepoResponse repoResponse = RepoResponse
                    .builder()
                    .id(repo.getId())
                    .name(repo.getName())
                    .status(repo.getStatus())
                    .createdAt(repo.getCreatedAt())
                    .userId(repo.getUser().getId())
                    .build();
            reposResponse.add(repoResponse);
        }

        return reposResponse;
    }

    public RepoResponse getById(UUID id, UUID userId){
        Repo repo = repoRepository.findByIdAndUserId(id, userId).orElseThrow(() -> new IllegalArgumentException("Invalid repository or unauthorized user"));
        return RepoResponse
            .builder()
            .id(repo.getId())
            .name(repo.getName())
            .status(repo.getStatus())
            .createdAt(repo.getCreatedAt())
            .userId(repo.getUser().getId())
            .build();
    }
}
