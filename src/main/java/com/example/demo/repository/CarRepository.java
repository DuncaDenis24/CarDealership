package com.example.demo.repository;

import com.example.demo.model.Car;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface CarRepository extends JpaRepository<Car, Integer> {
    @Query("SELECT c FROM Car c WHERE c.name = :name")
    Car findByName(@Param("name") String name);
    
    @Query("SELECT DISTINCT c FROM Car c " +
           "LEFT JOIN c.rentals r " +
           "WHERE c.isAvailable = true " +
           "AND c.forRent = true " +
           "AND c.purchase IS NULL " +
           "AND (r IS NULL OR r.status IN ('COMPLETED', 'CANCELLED') OR " +
           "    NOT EXISTS (SELECT 1 FROM Rental r2 WHERE r2.car = c AND r2.status = 'ACTIVE' " +
           "    AND ((:startDate BETWEEN r2.startDate AND r2.endDate) " +
           "    OR (:endDate BETWEEN r2.startDate AND r2.endDate) " +
           "    OR (r2.startDate <= :endDate AND r2.endDate >= :startDate))))")
    List<Car> findAvailableCars(
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );
    
    @Query("SELECT c FROM Car c WHERE c.forSale = true")
    List<Car> findCarsForSale();
    
    @Query("SELECT c FROM Car c WHERE c.isAvailable = true AND c.forRent = true")
    List<Car> findAvailableForRent();
    
    // Find all available cars (for rent or for sale)
    @Query("SELECT c FROM Car c WHERE c.isAvailable = true AND (c.forSale = true OR c.forRent = true)")
    List<Car> findAllAvailableCars();
}

