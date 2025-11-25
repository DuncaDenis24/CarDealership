package com.example.demo.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;
import lombok.ToString;
import java.util.List;

@Entity
@Data
@Table(name = "cars")
@ToString(exclude = {"rentals", "purchases"})
public class Car {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String model;

    @Column(nullable = false)
    private String color;

    @Column(name = "manufacture_year", nullable = false)
    private int year;

    @Column(nullable = false)
    private String licensePlate;

    @Column(nullable = false)
    private double dailyRate;

    @Column(nullable = false)
    private double price;  // Added price for purchase

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private CarType type;

    @Column(name = "is_available", nullable = false)
    private boolean isAvailable = true;

    @Column(name = "is_for_sale", nullable = false)
    private boolean forSale = true;  // New field to track if car is for sale

    @Column(name = "is_for_rent", nullable = false)
    private boolean forRent = true;  // New field to track if car is for rent

    @OneToMany(mappedBy = "car", cascade = CascadeType.ALL)
    @JsonIgnore
    private List<Rental> rentals;

    @OneToOne(mappedBy = "car", cascade = CascadeType.ALL)
    @JsonIgnore
    private Purchase purchase;  // New relationship with Purchase

    @Column(name = "image_url", length = 1000)
    private String imageUrl;  // URL of the car image

    public enum CarType {
        SEDAN, SUV, HATCHBACK, CONVERTIBLE, SPORTS, MINIVAN, PICKUP
    }
}