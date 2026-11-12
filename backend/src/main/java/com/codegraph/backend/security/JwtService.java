package com.codegraph.backend.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.util.Date;

@Service
public class JwtService {
    private final SecretKey secretKey;
    private final long expiration;

    public JwtService(@Value("${jwt.secret}") String secret, @Value("${jwt.expiration}") long expiration){
        this.secretKey = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
        this.expiration = expiration;
    }

    public String generateAccessToken(CustomUserDetails userDetails){
        long now = System.currentTimeMillis();

        return Jwts.builder()
                .subject(userDetails.getUsername())
                .claim("type", "access")
                .claim("id", userDetails.getId())
                .issuedAt(new Date(now))
                .expiration(new Date(now + expiration))
                .signWith(secretKey)
                .compact();
    }

    public String generateRefreshToken(CustomUserDetails userDetails){
        long now = System.currentTimeMillis();

        return Jwts.builder()
                .subject(userDetails.getUsername())
                .claim("type", "refresh")
                .claim("id", userDetails.getId().toString())
                .issuedAt(new Date(now))
                .expiration(new Date(now + 7 * 24 * 60 * 60 * 1000L))
                .signWith(secretKey)
                .compact();
    }

    public String extractUsername(String token){
        return extractAllClaims(token).getSubject();
    }

    public boolean isAccessTokenValid(String token, String username) {
        Claims claims = extractAllClaims(token);
        String tokenType = claims.get("type", String.class);

        return claims.getSubject().equals(username) && tokenType.equals("access") && claims.getExpiration().after(new Date());
    }

    public boolean isRefreshTokenValid(String token, String username) {
        Claims claims = extractAllClaims(token);
        String tokenType = claims.get("type", String.class);

        return claims.getSubject().equals(username) && tokenType.equals("refresh") && claims.getExpiration().after(new Date());
    }

    private Claims extractAllClaims(String token) {
        return Jwts.parser()
                .verifyWith(secretKey)
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }
}
