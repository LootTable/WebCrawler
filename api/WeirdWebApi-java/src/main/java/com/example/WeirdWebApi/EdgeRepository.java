package com.example.WeirdWebApi;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface EdgeRepository extends JpaRepository<Edge, Integer> {
    // Used by the dashboard to show outbound links for a selected page.
    List<Edge> findBySourceUrl(String sourceUrl);

}
