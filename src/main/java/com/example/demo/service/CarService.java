package com.example.demo.service;

import com.example.demo.model.Car;

import java.time.LocalDate;
import java.util.List;

public interface CarService {
    // Get all cars regardless of availability
    List<Car> getAllCars();
    
    // Get available cars for rent within a date range
    List<Car> getAvailableCars(LocalDate startDate, LocalDate endDate);
    
    // Get all available cars (for rent or for sale)
    List<Car> getAllAvailableCars();
    
    // Get cars marked for sale
    List<Car> getCarsForSale();
    
    // Get available cars for rent
    List<Car> getAvailableForRent();
    
    // CRUD operations
    Car createCar(Car car);
    Car getCarById(int id);
    Car getCarByName(String name);
    Car updateCar(Car car);
    void deleteCar(int id);
}
