package com.codegraph.backend.exception;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class ErrorResponse {
    private int status;
    private String error;
    private String message;
    private LocalDateTime timeStamp;

    public ErrorResponse(int status, String error, String message){
        this.status = status;
        this.error = error;
        this.message = message;
        this.timeStamp = LocalDateTime.now();
    }
}
