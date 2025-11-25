// src/main/java/com/example/demo/controller/PurchaseController.java
package com.example.demo.controller;

import com.example.demo.model.Car;
import com.example.demo.model.Purchase;
import com.example.demo.service.PurchaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/purchases")
@CrossOrigin(origins = "*")
public class PurchaseController {

    private final PurchaseService purchaseService;

    @Autowired
    public PurchaseController(PurchaseService purchaseService) {
        this.purchaseService = purchaseService;
    }

    @GetMapping
    public List<Purchase> getAllPurchases() {
        return purchaseService.getAllPurchases();
    }

    @GetMapping("/{id}")
    public Purchase getPurchaseById(@PathVariable Integer id) {
        return purchaseService.getPurchaseById(id);
    }

    @PostMapping
    public ResponseEntity<Purchase> createPurchase(@RequestBody Map<String, Object> request) {
        try {
            Purchase purchase = new Purchase();

            // Support two payload formats: either flat carId or nested car object
            Object carObj = request.get("car");
            Integer carId = null;
            if (carObj instanceof Map) {
                Object idVal = ((Map<?, ?>) carObj).get("id");
                if (idVal != null) {
                    carId = Integer.parseInt(idVal.toString());
                }
            }
            if (carId == null && request.get("carId") != null) {
                carId = Integer.parseInt(request.get("carId").toString());
            }

            if (carId == null) {
                return ResponseEntity.badRequest().build();
            }

            purchase.setCustomerName((String) request.get("customerName"));
            purchase.setCustomerEmail((String) request.get("customerEmail"));
            purchase.setCustomerPhone((String) request.get("customerPhone"));
            purchase.setCustomerAddress((String) request.get("customerAddress"));
            if (request.get("purchasePrice") != null) {
                purchase.setPurchasePrice(Double.parseDouble(request.get("purchasePrice").toString()));
            }
            if (request.get("paymentMethod") != null) {
                try {
                    purchase.setPaymentMethod(Purchase.PaymentMethod.valueOf(((String) request.get("paymentMethod"))));
                } catch (IllegalArgumentException ignored) {
                }
            }

            // Create a car reference with just the ID
            Car car = new Car();
            car.setId(carId);
            purchase.setCar(car);

            Purchase createdPurchase = purchaseService.createPurchase(purchase);
            return ResponseEntity.ok(createdPurchase);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deletePurchase(@PathVariable Integer id) {
        purchaseService.deletePurchase(id);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/email/{email}")
    public List<Purchase> getPurchasesByEmail(@PathVariable String email) {
        return purchaseService.getPurchasesByEmail(email);
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<Purchase> updatePurchaseStatus(
            @PathVariable Integer id,
            @RequestBody Map<String, String> request) {
        String status = request.get("status");

        Purchase purchaseDetails = new Purchase();
        try {
            purchaseDetails.setStatus(Purchase.Status.valueOf(status.toUpperCase()));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }

        Purchase updatedPurchase = purchaseService.updatePurchase(id, purchaseDetails);
        return ResponseEntity.ok(updatedPurchase);
    }

}