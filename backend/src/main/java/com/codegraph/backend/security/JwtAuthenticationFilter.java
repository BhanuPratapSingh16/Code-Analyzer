package com.codegraph.backend.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    private final JwtService jwtService;
    private final CustomUserDetailsService customUserDetailsService;

    public JwtAuthenticationFilter(JwtService jwtService, CustomUserDetailsService customUserDetailsService){
        this.jwtService = jwtService;
        this.customUserDetailsService = customUserDetailsService;
    }


    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        if(request.getServletPath().startsWith("/api/auth/login")
            || request.getServletPath().startsWith("/api/auth/register")
            || request.getServletPath().startsWith("/api/auth/logout")){
            filterChain.doFilter(request, response);
            return;
        }

        String token = getTokenFromRequest(request);
        if(token == null){
            filterChain.doFilter(request, response);
            return;
        }

        try{
            String username = jwtService.extractUsername(token);
            if(SecurityContextHolder.getContext().getAuthentication() == null){
                CustomUserDetails userDetails = customUserDetailsService.loadUserByUsername(username);

                if(jwtService.isAccessTokenValid(token, username)){
                    UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                    authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                    SecurityContextHolder.getContext().setAuthentication(authentication);
                }
            }
        } catch (Exception e) {
            SecurityContextHolder.clearContext();
        }

        filterChain.doFilter(request, response);
    }

    private String getTokenFromRequest(HttpServletRequest request){
        if(request.getCookies() == null){
            return null;
        }
        for(Cookie cookie: request.getCookies()){
            if("accessToken".equals(cookie.getName())){
                return cookie.getValue();
            }
        }
        return null;
    }
}
