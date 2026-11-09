package com.codegraph.backend.repo.model;

import com.codegraph.backend.repo.dto.RepoStatus;
import com.codegraph.backend.user.model.User;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.UUID;

@Data
@Builder
@Entity
@Table(name = "repos")
@NoArgsConstructor
@AllArgsConstructor
public class Repo {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private String name;

    @Enumerated(EnumType.STRING)
    private RepoStatus status = RepoStatus.UPLOADED;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(name = "created_at")
    private Instant createdAt;
}
