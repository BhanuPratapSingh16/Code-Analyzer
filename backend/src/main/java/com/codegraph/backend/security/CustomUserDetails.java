package com.codegraph.backend.security;

import com.codegraph.backend.user.model.User;
import org.jspecify.annotations.Nullable;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.Collections;
import java.util.UUID;

public class CustomUserDetails implements UserDetails {

    private String username;
    private String email;
    private String password;
    private UUID id;

    public CustomUserDetails(User user){
        this.username = user.getUsername();
        this.email = user.getEmail();
        this.password = user.getPassword();
        this.id = user.getId();
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Collections.emptyList();
    }

    @Override
    public @Nullable String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return username;
    }

    public String getEmail(){
        return email;
    }

    public UUID getId(){
        return id;
    }
}
