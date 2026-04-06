package com.example.WeirdWebApi;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "edges")
public class Edge {
    @Id
    private int id;
    @Column(name = "source_url")
    private String sourceUrl;
    @Column(name = "target_url")
    private String targetUrl;

    public int getId(){
        return id;
    }   
    public String getSourceUrl(){
        return sourceUrl;
    }
    public String getTargetUrl(){
        return targetUrl;
    }
}