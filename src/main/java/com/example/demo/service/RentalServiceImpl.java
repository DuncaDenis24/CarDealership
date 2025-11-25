package com.example.demo.service;

import com.example.demo.exception.ResourceNotFoundException;
import com.example.demo.model.Car;
import com.example.demo.model.Rental;
import com.example.demo.repository.CarRepository;
import com.example.demo.repository.RentalRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.List;

@Service
public class RentalServiceImpl implements RentalService {
    private final RentalRepository rentalRepository;
    private final CarRepository carRepository;
    private final EmailService emailService;

    @Autowired
    public RentalServiceImpl(RentalRepository rentalRepository, 
                           CarRepository carRepository,
                           EmailService emailService) {
        this.rentalRepository = rentalRepository;
        this.carRepository = carRepository;
        this.emailService = emailService;
    }

    @Override
    public List<Rental> getAllRentals() {
        return rentalRepository.findAll();
    }
    @Override
    public Rental getRentalById(Integer id) {
        return rentalRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Rental not found with id: " + id));
    }

    @Override
    @Transactional
    public Rental createRental(Rental rental) {
        // Verify car exists and is available
        Car car = carRepository.findById(rental.getCar().getId())
                .orElseThrow(() -> new ResourceNotFoundException("Car not found with id: " + rental.getCar().getId()));

        if (!car.isAvailable()) {
            throw new IllegalStateException("Car is not available for rent");
        }
        
        // Check if car is already rented for the requested dates
        List<Rental> overlappingRentals = rentalRepository.findRentalsInDateRange(
                rental.getStartDate(),
                rental.getEndDate()
        ).stream()
         .filter(r -> r.getCar().getId().equals(car.getId())
                 && !r.getStatus().equals(Rental.RentalStatus.CANCELLED))
         .toList();
         
        if (!overlappingRentals.isEmpty()) {
            throw new IllegalStateException("Car is already rented for the selected dates");
        }
        
        // Calculate total price and set it before saving
        long days = ChronoUnit.DAYS.between(rental.getStartDate(), rental.getEndDate()) + 1;
        double totalPrice = days * car.getDailyRate();
        rental.setTotalPrice(totalPrice);
        
        // Save the rental
        Rental savedRental = rentalRepository.save(rental);

        return savedRental;
    }

    @Override
    @Transactional
    public Rental updateRental(Integer id, Rental rentalDetails) {
        Rental rental = getRentalById(id);
        System.out.println("Updating rental " + id + " with status: " + 
            (rentalDetails.getStatus() != null ? rentalDetails.getStatus() : "no status change"));

        // Update fields if they are not null
        if (rentalDetails.getStartDate() != null) {
            rental.setStartDate(rentalDetails.getStartDate());
        }

        if (rentalDetails.getEndDate() != null) {
            rental.setEndDate(rentalDetails.getEndDate());
        }

        if (rentalDetails.getStatus() != null) {
            Rental.RentalStatus newStatus = rentalDetails.getStatus();
            System.out.println("Setting rental status to: " + newStatus);
            rental.setStatus(newStatus);

            // If rental is completed, make the car available again
            if (newStatus == Rental.RentalStatus.COMPLETED) {
                Car car = rental.getCar();
                if (car != null) {
                    System.out.println("Setting car " + car.getId() + " to available");
                    car.setAvailable(true);
                    car = carRepository.save(car);
                } else {
                    System.err.println("Warning: Car is null for rental " + rental.getId());
                }
            }
            // If rental is cancelled, delete it after making the car available
            else if (newStatus == Rental.RentalStatus.CANCELLED) {
                Car car = rental.getCar();
                if (car != null) {
                    System.out.println("Setting car " + car.getId() + " to available and deleting cancelled rental");
                    car.setAvailable(true);
                    car = carRepository.save(car);
                }
                // Delete the rental after sending the email (handled below)
                rentalRepository.delete(rental);
                return rental; // Return the deleted rental
            }
        }

        Rental saved = rentalRepository.save(rental);

        // Send notification emails when admin accepts/confirms or cancels the rental
        try {
            Rental.RentalStatus statusAfter = saved.getStatus();
            String to = saved.getCustomerEmail();
            String customerName = saved.getCustomerName();
            String carDetails = saved.getCar() != null ? saved.getCar().toString() : "";
            String rentalPeriod = saved.getStartDate() + " to " + saved.getEndDate();

            if (statusAfter == Rental.RentalStatus.CONFIRMED || statusAfter == Rental.RentalStatus.COMPLETED) {
                // send confirmation
                emailService.sendRentalConfirmation(to, customerName, carDetails, rentalPeriod, saved.getTotalPrice());
            } else if (statusAfter == Rental.RentalStatus.CANCELLED) {
                String reason = ""; // You can extract this from the request if available
                emailService.sendRentalCancellation(to, customerName, carDetails, rentalPeriod, reason);
            }
        } catch (Exception e) {
            // Log but don't break the update flow
            System.err.println("Failed to send rental notification email: " + e.getMessage());
        }

        return saved;
    }

    @Override
    @Transactional
    public void deleteRental(Integer id) {
        Rental rental = getRentalById(id);

        // Make the car available again if the rental is active
        if (rental.getStatus() == Rental.RentalStatus.PENDING ||
            rental.getStatus() == Rental.RentalStatus.CONFIRMED) {
            Car car = rental.getCar();
            car.setAvailable(true);
            carRepository.save(car);
        }

        rentalRepository.delete(rental);
    }

    @Override
    public List<Rental> getRentalsByEmail(String email) {
        return rentalRepository.findByCustomerEmail(email);
    }

    @Override
    public List<Rental> getActiveRentals() {
        return rentalRepository.findActiveRentals();
    }

    @Override
    public List<Rental> getRentalsInDateRange(LocalDate start, LocalDate end) {
        return rentalRepository.findRentalsInDateRange(start, end);
    }
    
    @Override
    public List<Rental> getRentalsInDateRangeForCar(Integer carId, LocalDate start, LocalDate end) {
        return rentalRepository.findRentalsInDateRangeForCar(carId, start, end);
    }
    @Override
    public List<Rental> getRentalsByCarId(Integer carId) {
        return rentalRepository.findByCarId(carId);
    }
    
    @Override
    public double calculateRentalPrice(Integer carId, LocalDate startDate, LocalDate endDate) {
        // Get the car
        Car car = carRepository.findById(carId)
                .orElseThrow(() -> new ResourceNotFoundException("Car not found with id: " + carId));
                
        if (!car.isAvailable()) {
            throw new IllegalStateException("This car is not available for rent");
        }
        
        // Calculate number of days
        long days = ChronoUnit.DAYS.between(startDate, endDate) + 1;
        if (days <= 0) {
            throw new IllegalArgumentException("End date must be after start date");
        }
        
        // Calculate total price
        return days * car.getDailyRate();
    }
}
