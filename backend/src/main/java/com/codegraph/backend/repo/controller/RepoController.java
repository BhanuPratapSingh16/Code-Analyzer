package com.codegraph.backend.repo.controller;

import com.codegraph.backend.repo.dto.RepoRequest;
import com.codegraph.backend.repo.dto.RepoResponse;
import com.codegraph.backend.repo.service.RepoService;
import com.codegraph.backend.security.CustomUserDetails;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/repos")
public class RepoController {

    private final RepoService repoService;

    @Autowired
    public RepoController(RepoService repoService){
        this.repoService = repoService;
    }

    @PostMapping("/create")
    public ResponseEntity<RepoResponse> createRepository(@RequestBody RepoRequest request, @AuthenticationPrincipal CustomUserDetails userDetails){
        UUID userId = userDetails.getId();
        return ResponseEntity.status(HttpStatus.CREATED).body(repoService.createRepository(request, userId));
    }

    @GetMapping("/")
    public ResponseEntity<List<RepoResponse>> getAllByUser(@AuthenticationPrincipal CustomUserDetails userDetails){
        UUID userId = userDetails.getId();
        return ResponseEntity.status(HttpStatus.OK).body(repoService.getAllByUser(userId));
    }

    @GetMapping("/{id}")
    public ResponseEntity<RepoResponse> getById(@PathVariable UUID id, @AuthenticationPrincipal CustomUserDetails userDetails){
        UUID userId = userDetails.getId();
        return ResponseEntity.status(HttpStatus.OK).body(repoService.getRepoResponseById(id, userId));
    }
}
