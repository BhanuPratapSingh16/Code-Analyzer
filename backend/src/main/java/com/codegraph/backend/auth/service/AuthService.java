package com.codegraph.backend.auth.service;

import com.codegraph.backend.auth.dto.*;
import com.codegraph.backend.security.CustomUserDetails;
import com.codegraph.backend.security.CustomUserDetailsService;
import com.codegraph.backend.security.JwtService;
import com.codegraph.backend.user.model.User;
import com.codegraph.backend.user.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final CustomUserDetailsService customUserDetailsService;

    @Autowired
    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder, AuthenticationManager authenticationManager, JwtService jwtService, CustomUserDetailsService customUserDetailsService){
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.jwtService = jwtService;
        this.customUserDetailsService = customUserDetailsService;
    }

    public RegisterResponse registerUser(RegisterRequest request){
        if(userRepository.existsByUsername(request.getUsername())){
            throw new IllegalArgumentException("Username already exists");
        }
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .build();
        User savedUser = userRepository.save(user);

        return new RegisterResponse(savedUser.getId(), savedUser.getUsername(), savedUser.getEmail());
    }

    public AuthResponse loginUser(LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
        );
        CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();

        String accessToken = jwtService.generateAccessToken(userDetails);
        String refreshToken = jwtService.generateRefreshToken(userDetails);

        return AuthResponse
                .builder()
                .id(userDetails.getId())
                .username(userDetails.getUsername())
                .email(userDetails.getEmail())
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .build();
    }

    public RefreshResponse refreshResponse(String refreshToken){
        String username = jwtService.extractUsername(refreshToken);

        CustomUserDetails userDetails = customUserDetailsService.loadUserByUsername(username);

        if(!jwtService.isRefreshTokenValid(refreshToken, username)){
            throw new RuntimeException("Refresh Token Invalid!");
        }

        return new RefreshResponse(jwtService.generateAccessToken(userDetails));
    }
}
