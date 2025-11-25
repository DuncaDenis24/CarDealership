// src/main/java/com/example/demo/model/Purchase.java
package com.example.demo.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;
import lombok.ToString;
import java.time.LocalDate;

@Entity
@Data
@ToString(exclude = {"car"})
@Table(name = "purchases")
public class Purchase {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private String customerName;

    @Column(nullable = false)
    private String customerEmail;

    @Column(nullable = false)
    private String customerPhone;

    @Column(nullable = false)
    private String customerAddress;

    @OneToOne
    @JoinColumn(name = "car_id", nullable = false)
    private Car car;

    @Column(nullable = false)
    private double purchasePrice;

    @Column(nullable = false)
    private LocalDate purchaseDate = LocalDate.now();

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private PaymentMethod paymentMethod;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status = Status.PENDING;

    public enum PaymentMethod {
        CASH, CREDIT_CARD, BANK_TRANSFER, LEASING
    }

    public enum Status {
        PENDING, COMPLETED, CANCELLED
    }
}