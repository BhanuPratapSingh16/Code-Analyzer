package com.codegraph.backend.auth.service;

import com.codegraph.backend.auth.dto.AuthResponse;
import com.codegraph.backend.auth.dto.LoginRequest;
import com.codegraph.backend.auth.dto.RegisterRequest;
import com.codegraph.backend.user.model.User;
import com.codegraph.backend.user.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Autowired
    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder){
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public AuthResponse registerUser(RegisterRequest request){
        if(userRepository.existsByUsername(request.getUsername())){
            throw new IllegalArgumentException("Username already exists");
        }
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .build();
        User savedUser = userRepository.save(user);

        return new AuthResponse(savedUser.getId(), savedUser.getUsername(), savedUser.getEmail());
    }

    public AuthResponse getUserById(String id){
        User user = userRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("User not found"));
        return new AuthResponse(user.getId(), user.getUsername(), user.getEmail());
    }

    public AuthResponse loginUser(LoginRequest request){
        User user = userRepository.findByUsername(request.getUsername()).orElseThrow(() -> new IllegalArgumentException("User not found"));
        return new AuthResponse(user.getId(), user.getUsername(), user.getEmail());
    }
}
