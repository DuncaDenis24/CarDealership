package com.example.demo.repository;

import com.example.demo.model.Rental;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface RentalRepository extends JpaRepository<Rental, Integer> {
    
    // Find all rentals for a specific customer email
    List<Rental> findByCustomerEmail(String customerEmail);
    
    // Find all active rentals (not completed or cancelled)
    @Query("SELECT r FROM Rental r WHERE r.status NOT IN (com.example.demo.model.Rental.RentalStatus.COMPLETED, com.example.demo.model.Rental.RentalStatus.CANCELLED)")
    List<Rental> findActiveRentals();
    
    // Find rentals for a specific car within a date range
    @Query("SELECT DISTINCT r FROM Rental r JOIN FETCH r.car c WHERE c.id = :carId AND " +
           "((r.startDate BETWEEN :startDate AND :endDate) " +
           "OR (r.endDate BETWEEN :startDate AND :endDate) " +
           "OR (r.startDate <= :startDate AND r.endDate >= :endDate))")
    List<Rental> findRentalsInDateRangeForCar(
        @Param("carId") Integer carId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );
    
    // Find all rentals within a date range (for backward compatibility)
    @Query("SELECT r FROM Rental r WHERE (r.startDate BETWEEN :startDate AND :endDate) OR (r.endDate BETWEEN :startDate AND :endDate) OR (r.startDate <= :startDate AND r.endDate >= :endDate)")
    List<Rental> findRentalsInDateRange(
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );
    
    // Find all rentals for a specific car
    List<Rental> findByCarId(Integer carId);
}
