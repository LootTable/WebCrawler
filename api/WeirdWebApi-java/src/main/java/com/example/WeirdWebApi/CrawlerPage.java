package com.example.WeirdWebApi;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "crawler")
public class CrawlerPage {
    // Maps the SQLite crawler table so Spring can return crawled pages as JSON.
    @Id
    private int id;
    private String url;
    private String title;

    @Column(name = "status_code")
    private int statusCode;

    @Column(name = "is_dead")
    private int isDead;

    public int getId() {
        return id;
    }

    public String getUrl() {
        return url;
    }

    public String getTitle() {
        return title;
    }

    public int getStatusCode() {
        return statusCode;
    }

    public int getIsDead() {
        return isDead;
    }
}
