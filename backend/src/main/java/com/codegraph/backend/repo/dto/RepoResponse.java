package com.codegraph.backend.repo.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

import java.time.Instant;
import java.util.UUID;

@Data
@Builder
@AllArgsConstructor
public class RepoResponse {
    private UUID id;
    private String name;
    private UUID userId;
    private RepoStatus status;
    private Instant createdAt;
}
