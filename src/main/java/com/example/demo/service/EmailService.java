package com.example.demo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
public class EmailService {

    @Autowired
    private JavaMailSender mailSender;

    @Value("${app.email.sender}")
    private String fromEmail;

    @Value("${app.email.subject.rental-confirmation}")
    private String rentalSubject;

    @Value("${app.email.subject.purchase-confirmation}")
    private String purchaseSubject;

    @Async
    public void sendRentalConfirmation(String toEmail, String customerName, String carDetails, String rentalPeriod, double totalPrice) {
        String subject = String.format(rentalSubject, "Rental #" + System.currentTimeMillis());
        String message = String.format(
            "Dear %s,\n\n" +
            "Thank you for your rental! Here are your rental details:\n\n" +
            "=== RENTAL DETAILS ===\n" +
            "• Customer: %s\n" +
            "• Car: %s\n" +
            "• Rental Period: %s\n" +
            "• Total Price: $%.2f\n\n" +
            "We hope you enjoy your rental! If you have any questions, please don't hesitate to contact us.\n\n" +
            "Best regards,\nThe Car Rental Team",
            customerName, customerName, formatCarDetails(carDetails), rentalPeriod, totalPrice
        );

        sendEmail(toEmail, subject, message);
    }

    @Async
    public void sendPurchaseConfirmation(String toEmail, String customerName, String carDetails, double totalPrice) {
        String subject = String.format(purchaseSubject, "Purchase #" + System.currentTimeMillis());
        String message = String.format(
            "Dear %s,\n\n" +
            "Thank you for your purchase! Here are your order details:\n\n" +
            "=== ORDER DETAILS ===\n" +
            "• Customer: %s\n" +
            "• Car: %s\n" +
            "• Total Amount: $%.2f\n\n" +
            "Your vehicle will be prepared for delivery. Our team will contact you within 24 hours " +
            "to confirm the delivery details and schedule a convenient time for you.\n\n" +
            "If you have any questions, feel free to reply to this email or call us at (555) 123-4567.\n\n" +
            "Best regards,\nThe Car Sales Team\n" +
            "Phone: (555) 123-4567\n" +
            "Email: sales@cardealership.com",
            customerName, customerName, formatCarDetails(carDetails), totalPrice
        );

        sendEmail(toEmail, subject, message);
    }
    
    @Async
    public void sendPurchaseCancellation(String toEmail, String customerName, String carDetails, String reason) {
        String subject = "Your Purchase Has Been Cancelled";
        String message = String.format(
            "Dear %s,\n\n" +
            "We regret to inform you that your purchase has been cancelled.\n\n" +
            "=== CANCELLATION DETAILS ===\n" +
            "• Customer: %s\n" +
            "• Car: %s\n" +
            "• Reason: %s\n\n" +
            "If you did not request this cancellation or believe this is a mistake, please contact our support team immediately.\n\n" +
            "Best regards,\nThe Car Sales Team\n" +
            "Phone: (555) 123-4567\n" +
            "Email: support@cardealership.com",
            customerName, customerName, formatCarDetails(carDetails), 
            (reason != null && !reason.isEmpty()) ? reason : "Not specified"
        );

        sendEmail(toEmail, subject, message);
    }
    
    @Async
    public void sendRentalCancellation(String toEmail, String customerName, String carDetails, String rentalPeriod, String reason) {
        String subject = "Your Rental Has Been Cancelled";
        String message = String.format(
            "Dear %s,\n\n" +
            "We regret to inform you that your rental has been cancelled.\n\n" +
            "=== CANCELLATION DETAILS ===\n" +
            "• Customer: %s\n" +
            "• Car: %s\n" +
            "• Rental Period: %s\n" +
            "• Reason: %s\n\n" +
            "If you did not request this cancellation or believe this is a mistake, please contact our support team immediately.\n\n" +
            "Best regards,\nThe Car Rental Team\n" +
            "Phone: (555) 123-4567\n" +
            "Email: support@cardealership.com",
            customerName, customerName, formatCarDetails(carDetails), rentalPeriod,
            (reason != null && !reason.isEmpty()) ? reason : "Not specified"
        );

        sendEmail(toEmail, subject, message);
    }
    
    // Helper method to format car details from the raw toString() output
    private String formatCarDetails(String rawCarDetails) {
        try {
            // Extract relevant information using regex
            String pattern = "Car\\(id=(?<id>\\d+), name=(?<name>[^,]+), model=(?<model>[^,]+), " +
                           "color=(?<color>[^,]+), year=(?<year>\\d{4})";
            java.util.regex.Pattern r = java.util.regex.Pattern.compile(pattern);
            java.util.regex.Matcher m = r.matcher(rawCarDetails);
            
            if (m.find()) {
                return String.format("%s %s (%s) - %s (ID: %s)",
                    m.group("name"),
                    m.group("model"),
                    m.group("year"),
                    m.group("color"),
                    m.group("id")
                );
            }
        } catch (Exception e) {
            // If parsing fails, return the original string
            System.err.println("Error formatting car details: " + e.getMessage());
        }
        return rawCarDetails; // Fallback to original if parsing fails
    }

    @Async
    public void sendEmail(String to, String subject, String text) {
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setFrom(fromEmail);
            message.setTo(to);
            message.setSubject(subject);
            message.setText(text);
            mailSender.send(message);
        } catch (Exception e) {
            // Log the error but don't fail the main operation
            System.err.println("Failed to send email: " + e.getMessage());
        }
    }
}
