package com.codegraph.backend.fastapi.dto;

import lombok.Data;

import java.util.UUID;

@Data
public class FastApiResponse {
    private UUID repository_id;
    private String status;
    private String message;
}
