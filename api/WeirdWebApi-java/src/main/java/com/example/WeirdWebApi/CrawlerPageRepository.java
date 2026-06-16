package com.example.WeirdWebApi;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CrawlerPageRepository extends JpaRepository<CrawlerPage, Integer> {
    // Spring Data builds the SQL queries from these method names.
    List<CrawlerPage> findByTitleContaining(String title);

    List<CrawlerPage> findByIsDead(int isDead);

    List<CrawlerPage> findByTitleContainingAndIsDead(String title, int isDead);
}
