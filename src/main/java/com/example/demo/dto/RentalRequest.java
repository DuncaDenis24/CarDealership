package com.example.demo.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDate;

@Data
public class RentalRequest {
    @NotNull(message = "User ID is required")
    private Long userId;
    
    @NotNull(message = "Car ID is required")
    private Long carId;
    
    @NotNull(message = "Start date is required")
    @FutureOrPresent(message = "Start date must be in the present or future")
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate startDate;
    
    @NotNull(message = "End date is required")
    @FutureOrPresent(message = "End date must be in the present or future")
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate endDate;
    
    public boolean isValidDateRange() {
        return !endDate.isBefore(startDate);
    }
}
