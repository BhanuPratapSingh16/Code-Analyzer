package com.codegraph.backend.rag;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class RagClient {
    private final WebClient webClient;

    @Autowired
    public RagClient(WebClient webClient){
        this.webClient = webClient;
    }

    public String checkConnection(){
        return webClient.get()
                .uri("/api/rag/connection")
                .retrieve()
                .bodyToMono(String.class)
                .block();
    }
}
