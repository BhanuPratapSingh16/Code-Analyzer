package com.codegraph.backend.auth.dto;

import lombok.Data;

@Data
public class RefreshRequest {
    private String refreshToken;
}
