package com.example.demo.controller;

import com.example.demo.model.Car;
import com.example.demo.service.CarService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
@RestController
@RequestMapping("/api/cars")
@CrossOrigin(origins = {"http://localhost:8081", "http://localhost:3000", "http://localhost:4173", "http://localhost:5173"})
public class CarController {

    @Autowired
    private CarService carService;

    @GetMapping
    public List<Car> getAllCars() {
        return carService.getAllCars();
    }
    
    @GetMapping("/all-available")
    public List<Car> getAllAvailableCars() {
        return carService.getAllAvailableCars();
    }
    
    @GetMapping("/available")
    public List<Car> getAvailableCars(
            @RequestParam(name = "startDate", required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam(name = "endDate", required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        
        // If dates are not provided, use default values (e.g., today and 7 days from now)
        if (startDate == null) {
            startDate = LocalDate.now();
        }
        if (endDate == null) {
            endDate = startDate.plusDays(7);
        }
        
        return carService.getAvailableCars(startDate, endDate);
    }
    
    @GetMapping("/for-sale")
    public List<Car> getCarsForSale() {
        return carService.getCarsForSale();
    }
    
    @GetMapping("/for-rent")
    public List<Car> getAvailableForRent() {
        return carService.getAvailableForRent();
    }
    
    @PostMapping
    public Car createCar(@RequestBody Car car) {
        return carService.createCar(car);
    }
    
    @GetMapping("/{id}")
    public Car getCarById(@PathVariable int id) {
        return carService.getCarById(id);
    }
    
    @GetMapping("/search")
    public Car getCarByName(@RequestParam String name) {
        return carService.getCarByName(name);
    }
    
    @PutMapping("/{id}")
    public Car updateCar(@PathVariable int id, @RequestBody Car car) {
        car.setId(id);
        return carService.updateCar(car);
    }
    
    @DeleteMapping("/{id}")
    public void deleteCar(@PathVariable int id) {
        carService.deleteCar(id);
    }
}
