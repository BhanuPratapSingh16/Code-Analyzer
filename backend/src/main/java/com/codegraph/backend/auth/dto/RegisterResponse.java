package com.codegraph.backend.auth.dto;


import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.UUID;

@Data
@AllArgsConstructor
public class RegisterResponse {
    private UUID id;
    private String username;
    private String email;
}
