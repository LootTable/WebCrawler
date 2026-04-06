package com.example.WeirdWebApi;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CrawlerPageRepository extends JpaRepository<CrawlerPage, Integer> {
List<CrawlerPage> findByTitleContaining(String title);
List<CrawlerPage> findByIsDead(int isDead);
List<CrawlerPage> findByTitleContainingAndIsDead(String title, int isDead);
}

