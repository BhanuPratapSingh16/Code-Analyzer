package com.codegraph.backend.auth.dto;


import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class RegisterResponse {
    private String id;
    private String username;
    private String email;
}
