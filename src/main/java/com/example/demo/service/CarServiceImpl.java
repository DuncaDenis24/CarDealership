package com.example.demo.service;

import com.example.demo.exception.ResourceNotFoundException;
import com.example.demo.model.Car;
import com.example.demo.repository.CarRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class CarServiceImpl implements CarService {
    @Autowired
    private CarRepository carRepository;
    @Override
    public List<Car> getAllCars() {
        return carRepository.findAll();
    }
    
    @Override
    public List<Car> getAllAvailableCars() {
        return carRepository.findAllAvailableCars();
    }
    
    @Override
    public List<Car> getAvailableCars(LocalDate startDate, LocalDate endDate) {
        return carRepository.findAvailableCars(startDate, endDate);
    }
    
    @Override
    public List<Car> getCarsForSale() {
        return carRepository.findCarsForSale();
    }
    
    @Override
    public List<Car> getAvailableForRent() {
        return carRepository.findAvailableForRent();
    }
    @Override
    public Car createCar(Car car) {
        return carRepository.save(car);
    }
    @Override
    public Car getCarById(int id) {
        return carRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Car not found with id: " + id));
    }
    @Override
    public Car getCarByName(String name) { return carRepository.findByName(name);}
    @Override
    public Car updateCar(Car car) {
        return carRepository.save(car);
    }
    @Override
    public void deleteCar(int id) {
        carRepository.deleteById(id);
    }
}
