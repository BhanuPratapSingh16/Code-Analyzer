package com.codegraph.backend.repo.model;

import com.codegraph.backend.repo.dto.RepositoryStatus;
import com.codegraph.backend.user.model.User;
import jakarta.persistence.*;
import lombok.Builder;
import lombok.Data;

import java.util.UUID;

@Data
@Entity
@Table(name = "repos")
public class Repo {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private String name;

    @Enumerated(EnumType.STRING)
    private RepositoryStatus repositoryStatus;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}
