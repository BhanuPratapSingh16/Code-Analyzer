package com.codegraph.backend.repo.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.Instant;

@Data
@AllArgsConstructor
public class RepoRequest {
    private String name;
}
