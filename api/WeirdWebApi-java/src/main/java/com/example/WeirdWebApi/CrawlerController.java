package com.example.WeirdWebApi;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CrawlerController {
    private final CrawlerPageRepository crawlerPageRepository;
    private final EdgeRepository edgeRepository;
    public CrawlerController(CrawlerPageRepository crawlerPageRepository, EdgeRepository edgeRepository){
        this.crawlerPageRepository = crawlerPageRepository;
        this.edgeRepository = edgeRepository;
    }

    @GetMapping("/pages")
    public List<CrawlerPage> findPages(
        @RequestParam(required = false) String title,
        @RequestParam(required = false) Integer isDead) {

    if (title == null && isDead == null) {
        return crawlerPageRepository.findAll();
    } else if (title != null && isDead == null) {
        return crawlerPageRepository.findByTitleContaining(title);
    } else if (title == null && isDead != null) {
        return crawlerPageRepository.findByIsDead(isDead);
    } else {
        return crawlerPageRepository.findByTitleContainingAndIsDead(title, isDead);
    }
}

    @GetMapping("/edges")
    public List<Edge> findEdgesBySourceUrl(@RequestParam String sourceUrl){
        return edgeRepository.findBySourceUrl(sourceUrl);
    }

}    