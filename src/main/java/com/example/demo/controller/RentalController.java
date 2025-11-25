package com.example.demo.controller;

import com.example.demo.model.Rental;
import com.example.demo.service.RentalService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/rentals")
@CrossOrigin(origins = {"http://localhost:8081", "http://localhost:3000", "http://localhost:4173", "http://localhost:5173"})
public class RentalController {

    private final RentalService rentalService;

    @Autowired
    public RentalController(RentalService rentalService) {
        this.rentalService = rentalService;
    }

    @GetMapping
    public List<Rental> getAllRentals() {
        return rentalService.getAllRentals();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Rental> getRentalById(@PathVariable Integer id) {
        return ResponseEntity.ok(rentalService.getRentalById(id));
    }

    @PostMapping
    public Rental createRental(@RequestBody Rental rental) {
        return rentalService.createRental(rental);
    }

    @PutMapping("/{id}")
    public Rental updateRental(@PathVariable Integer id, @RequestBody Rental rental) {
        return rentalService.updateRental(id, rental);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteRental(@PathVariable Integer id) {
        rentalService.deleteRental(id);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/email/{email}")
    public List<Rental> getRentalsByEmail(@PathVariable String email) {
        return rentalService.getRentalsByEmail(email);
    }

    @GetMapping("/active")
    public List<Rental> getActiveRentals() {
        return rentalService.getActiveRentals();
    }

    @GetMapping("/date-range")
    public List<Rental> getRentalsInDateRange(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate start,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate end) {
        return rentalService.getRentalsInDateRange(start, end);
    }
    
    @GetMapping("/date-range/car/{carId}")
    public List<Rental> getRentalsInDateRangeForCar(
            @PathVariable Integer carId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate start,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate end) {
        return rentalService.getRentalsInDateRangeForCar(carId, start, end);
    }

    @GetMapping("/calculate-price")
    public double calculateRentalPrice(
            @RequestParam Integer carId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        return rentalService.calculateRentalPrice(carId, startDate, endDate);
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<?> updateRentalStatus(@PathVariable Integer id, @RequestBody java.util.Map<String, String> body) {
        String statusStr = body.get("status");
        if (statusStr == null) {
            return ResponseEntity.badRequest().body("Status is required");
        }

        try {
            // Map "APPROVED" to "CONFIRMED" for backward compatibility
            if ("APPROVED".equalsIgnoreCase(statusStr)) {
                statusStr = "CONFIRMED";
            } else if ("REJECTED".equalsIgnoreCase(statusStr)) {
                statusStr = "CANCELLED";
            }
            
            // Get the existing rental first
            Rental existingRental = rentalService.getRentalById(id);
            System.out.println("Existing rental status: " + existingRental.getStatus());
            
            // Create an update object with only the status field set
            Rental rentalUpdate = new Rental();
            rentalUpdate.setStatus(Rental.RentalStatus.valueOf(statusStr));
            
            // Update the rental
            Rental updated = rentalService.updateRental(id, rentalUpdate);
            System.out.println("Updated rental status: " + updated.getStatus());
            
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            System.err.println("Invalid status value: " + statusStr);
            return ResponseEntity.badRequest().body("Invalid status: " + statusStr + ". Valid values are: " + 
                java.util.Arrays.toString(Rental.RentalStatus.values()));
        } catch (Exception e) {
            System.err.println("Error updating rental status: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(500).body("Error updating rental status: " + e.getMessage());
        }
    }
}
