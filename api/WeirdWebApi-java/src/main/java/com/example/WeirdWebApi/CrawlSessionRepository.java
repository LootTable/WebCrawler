package com.example.WeirdWebApi;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CrawlSessionRepository extends JpaRepository<CrawlSession, Integer> {
    // Return the newest crawl runs first for the dashboard.
    List<CrawlSession> findTop10ByOrderByIdDesc();
}
