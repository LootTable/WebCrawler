package com.example.WeirdWebApi;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface EdgeRepository extends JpaRepository<Edge, Integer> {
List<Edge> findBySourceUrl(String sourceUrl);

}