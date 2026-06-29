package com.example.WeirdWebApi;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "crawl_sessions")
public class CrawlSession {
    // Maps one crawler run so the API can show crawl history.
    @Id
    private int id;

    @Column(name = "start_url")
    private String startUrl;

    @Column(name = "max_pages")
    private int maxPages;

    @Column(name = "max_depth")
    private int maxDepth;

    @Column(name = "pages_attempted")
    private int pagesAttempted;

    @Column(name = "request_failures")
    private int requestFailures;

    @Column(name = "started_at")
    private String startedAt;

    @Column(name = "completed_at")
    private String completedAt;

    public int getId() {
        return id;
    }

    public String getStartUrl() {
        return startUrl;
    }

    public int getMaxPages() {
        return maxPages;
    }

    public int getMaxDepth() {
        return maxDepth;
    }

    public int getPagesAttempted() {
        return pagesAttempted;
    }

    public int getRequestFailures() {
        return requestFailures;
    }

    public String getStartedAt() {
        return startedAt;
    }

    public String getCompletedAt() {
        return completedAt;
    }
}
