// src/main/java/com/example/demo/service/PurchaseServiceImpl.java
package com.example.demo.service;

import com.example.demo.exception.ResourceNotFoundException;
import com.example.demo.model.Car;
import com.example.demo.model.Purchase;
import com.example.demo.repository.CarRepository;
import com.example.demo.repository.PurchaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Service
public class PurchaseServiceImpl implements PurchaseService {

    private final PurchaseRepository purchaseRepository;
    private final CarRepository carRepository;
    private final EmailService emailService;

    @Autowired
    public PurchaseServiceImpl(PurchaseRepository purchaseRepository,
                               CarRepository carRepository,
                               EmailService emailService) {
        this.purchaseRepository = purchaseRepository;
        this.carRepository = carRepository;
        this.emailService = emailService;
    }

    @Override
    public List<Purchase> getAllPurchases() {
        return purchaseRepository.findAll();
    }

    @Override
    public Purchase getPurchaseById(Integer id) {
        return purchaseRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Purchase not found with id: " + id));
    }

    @Override
    @Transactional
    public Purchase createPurchase(Purchase purchase) {
        // Validate input
        if (purchase.getCar() == null || purchase.getCar().getId() == null) {
            throw new IllegalArgumentException("Car ID is required");
        }
        
        // Get the car from the database
        Car car = carRepository.findById(purchase.getCar().getId())
                .orElseThrow(() -> new ResourceNotFoundException("Car not found with id: " + purchase.getCar().getId()));

        // Check if car is already purchased
        if (purchaseRepository.existsByCarId(car.getId())) {
            throw new IllegalStateException("Car with ID " + car.getId() + " has already been purchased");
        }

        // Check if car is available for sale
        if (!car.isForSale()) {
            throw new IllegalStateException("Car with ID " + car.getId() + " is not available for purchase");
        }
        
        // Set the purchase date
        purchase.setPurchaseDate(LocalDate.now());
        
        try {
            // Mark car as not available (but preserve forSale/forRent flags)
            car.setAvailable(false);
            carRepository.save(car);
            
            // Set the car in the purchase
            purchase.setCar(car);
            
            // Save and return the purchase
            return purchaseRepository.save(purchase);
        } catch (Exception e) {
            throw new RuntimeException("Failed to process purchase: " + e.getMessage(), e);
        }
    }

    @Override
    @Transactional
    public void deletePurchase(Integer id) {
        Purchase purchase = getPurchaseById(id);
        Car car = purchase.getCar();

        // Mark car as available for sale again
        car.setForSale(true);
        carRepository.save(car);

        purchaseRepository.delete(purchase);
    }

    @Override
    public List<Purchase> getPurchasesByEmail(String email) {
        return purchaseRepository.findByCustomerEmail(email);
    }

    @Override
    @Transactional
    public Purchase updatePurchase(Integer id, Purchase purchaseDetails) {
        Purchase purchase = getPurchaseById(id);

        // Update status if provided
        if (purchaseDetails.getStatus() != null) {
            Purchase.Status newStatus = purchaseDetails.getStatus();
            purchase.setStatus(newStatus);

            // If purchase is cancelled, make the car available for sale again
            if (newStatus == Purchase.Status.CANCELLED) {
                Car car = purchase.getCar();
                car.setAvailable(true);  // Make car available again
                car.setPurchase(null);   // Clear the purchase reference
                carRepository.save(car);
                
                // Send cancellation email before deleting
                try {
                    String to = purchase.getCustomerEmail();
                    String customerName = purchase.getCustomerName();
                    String carDetails = car.toString();
                    String reason = ""; // You can extract this from the request if available
                    emailService.sendPurchaseCancellation(to, customerName, carDetails, reason);
                } catch (Exception e) {
                    System.err.println("Failed to send cancellation email: " + e.getMessage());
                }
                
                // Delete the purchase record
                purchaseRepository.delete(purchase);
                return purchase;  // Return the deleted purchase (will be detached)
            }
            // If purchase is approved/completed, keep car as sold
        }

        // Only save if purchase wasn't cancelled (deleted)
        if (purchase.getStatus() != Purchase.Status.CANCELLED) {
            Purchase saved = purchaseRepository.save(purchase);

            // Send notification emails on purchase status changes
            try {
                Purchase.Status after = saved.getStatus();
                String to = saved.getCustomerEmail();
                String customerName = saved.getCustomerName();
                String carDetails = saved.getCar() != null ? saved.getCar().toString() : "";

                if (after == Purchase.Status.COMPLETED) {
                    // send purchase confirmation
                    emailService.sendPurchaseConfirmation(to, customerName, carDetails, saved.getPurchasePrice());
                }
            } catch (Exception e) {
                System.err.println("Failed to send purchase notification email: " + e.getMessage());
            }

            return saved;
        }
        
        return purchase;  // Return the deleted purchase (in case it was cancelled)
    }
}