package com.example.WeirdWebApi;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;


@RestController
public class HealthController {
    @GetMapping("/health")
    public String health(){
        return "ok";
    }
}
