package com.codegraph.backend.auth.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class LoginRequest {
    @NotBlank(message = "Username cannot be empty!")
    private String username;

    @NotBlank(message = "Password is mandatory")
    private String password;
}
