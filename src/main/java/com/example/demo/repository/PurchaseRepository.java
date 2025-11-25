// src/main/java/com/example/demo/repository/PurchaseRepository.java
package com.example.demo.repository;

import com.example.demo.model.Purchase;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface    PurchaseRepository extends JpaRepository<Purchase, Integer> {
    boolean existsByCarId(Integer carId);
    List<Purchase> findByCustomerEmail(String email);
}