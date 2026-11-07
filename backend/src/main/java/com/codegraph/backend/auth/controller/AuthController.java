package com.codegraph.backend.auth.controller;

import com.codegraph.backend.auth.dto.AuthResponse;
import com.codegraph.backend.auth.dto.LoginRequest;
import com.codegraph.backend.auth.dto.RegisterRequest;
import com.codegraph.backend.auth.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    @Autowired
    public AuthController(AuthService authService){
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> registerUser(@Valid @RequestBody RegisterRequest request){
        return ResponseEntity.status(HttpStatus.CREATED).body(authService.registerUser(request));
    }

    @GetMapping("/{id}")
    public ResponseEntity<AuthResponse> getUserById(@PathVariable String id){
        return ResponseEntity.status(HttpStatus.OK).body(authService.getUserById(id));
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request){
        return ResponseEntity.status(HttpStatus.OK).body(authService.loginUser(request));
    }
}
