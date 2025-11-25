package com.example.demo.service;

import com.example.demo.model.Rental;
import java.time.LocalDate;
import java.util.List;

public interface RentalService {
    List<Rental> getAllRentals();
    Rental getRentalById(Integer id);
    Rental createRental(Rental rental);
    Rental updateRental(Integer id, Rental rental);
    void deleteRental(Integer id);
    List<Rental> getRentalsByEmail(String email);
    List<Rental> getActiveRentals();
    List<Rental> getRentalsInDateRange(LocalDate startDate, LocalDate endDate);
    List<Rental> getRentalsByCarId(Integer carId);
    List<Rental> getRentalsInDateRangeForCar(Integer carId, LocalDate start, LocalDate end);
    double calculateRentalPrice(Integer carId, LocalDate startDate, LocalDate endDate);
}
