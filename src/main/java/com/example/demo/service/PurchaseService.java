// src/main/java/com/example/demo/service/PurchaseService.java
package com.example.demo.service;

import com.example.demo.model.Purchase;
import java.util.List;

public interface PurchaseService {
    List<Purchase> getAllPurchases();
    Purchase getPurchaseById(Integer id);
    Purchase createPurchase(Purchase purchase);
    void deletePurchase(Integer id);
    List<Purchase> getPurchasesByEmail(String email);
    Purchase updatePurchase(Integer id, Purchase purchaseDetails);
}