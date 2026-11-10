package com.codegraph.backend.rag;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/rag")
public class RagController {
    private final RagClient ragClient;

    @Autowired
    public RagController(RagClient ragClient){
        this.ragClient = ragClient;
    }

    @GetMapping("/connection")
    public String connection(){
        return ragClient.checkConnection();
    }
}
