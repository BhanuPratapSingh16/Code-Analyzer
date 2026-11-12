package com.codegraph.backend.repo.repository;

import com.codegraph.backend.repo.model.Repo;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface RepoRepository extends JpaRepository<Repo, UUID> {
    List<Repo> findAllByUserIdOrderByCreatedAtDesc(UUID userId);

    Optional<Repo> findByIdAndUserId(UUID id, UUID userId);
}
