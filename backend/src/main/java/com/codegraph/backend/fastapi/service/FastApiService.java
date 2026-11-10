package com.codegraph.backend.fastapi.service;

import com.codegraph.backend.fastapi.dto.FastApiResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.*;
import java.io.IOException;
import java.util.UUID;

@Service
public class FastApiService {
    private final RestClient fastApiRestClient;

    @Autowired
    public FastApiService(RestClient fastApiRestClient){
        this.fastApiRestClient = fastApiRestClient;
    }

    public String checkConnection(){
        return fastApiRestClient.get()
                .uri("/api/fastapi/connection")
                .retrieve()
                .body(String.class);
    }

    public FastApiResponse uploadFile(UUID repositoryId, MultipartFile file) throws IOException {
        ByteArrayResource fileResource = new NamedByteArrayResource(file.getBytes(), file.getOriginalFilename());

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", fileResource);
        return fastApiRestClient.post()
                .uri("/repositories/{id}/upload", repositoryId)
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .body(body)
                .retrieve()
                .body(FastApiResponse.class);
    }

    private static class NamedByteArrayResource extends ByteArrayResource{
        private final String filename;

        public NamedByteArrayResource(byte[] byteArray, String filename){
            super(byteArray);
            this.filename = filename;
        }

        @Override
        public String getFilename(){
            return this.filename;
        }

    }
}
