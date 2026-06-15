// PaymentController.java - Spring Boot Fintech Payment Controller (INTENTIONALLY FLAWED)

package com.fintech.payment.controller;

import com.fintech.payment.model.Transaction;
import com.fintech.payment.service.PaymentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;

@RestController
@RequestMapping("/api/v1/payments")
public class PaymentController {

    @Autowired  // FLAW: Field injection instead of constructor injection (Spring best practice violation)
    private PaymentService paymentService;

    // FLAW: No @PreAuthorize or @Secured annotation - anyone authenticated can access
    @PostMapping("/charge")
    public ResponseEntity<Transaction> charge(
            @RequestParam String accountId,  // FLAW: Account ID from request param, not auth principal
            @RequestParam BigDecimal amount,
            @RequestParam String currency) {
        // FLAW: No input validation (amount could be negative, zero, or exceed limits)
        // FLAW: No idempotency key header check
        Transaction txn = paymentService.processCharge(accountId, amount, currency);
        return ResponseEntity.ok(txn);  // FLAW: Returns 200 for charge, should be 201
    }

    // FLAW: No authorization check - IDOR vulnerability
    @GetMapping("/transactions/{accountId}")
    public ResponseEntity<List<Transaction>> getTransactions(@PathVariable String accountId) {
        // FLAW: No check that authenticated user owns this accountId
        List<Transaction> transactions = paymentService.getTransactions(accountId);
        return ResponseEntity.ok(transactions);  // FLAW: No pagination
    }

    @PostMapping("/refund")
    public ResponseEntity<Transaction> refund(
            @RequestParam Long transactionId,
            @RequestParam BigDecimal amount) {
        // FLAW: No authorization - any user can refund any transaction
        // FLAW: No idempotency key
        Transaction refund = paymentService.processRefund(transactionId, amount);
        return ResponseEntity.ok(refund);
    }

    // FLAW: Exposes internal admin endpoint without proper security
    @GetMapping("/admin/all-transactions")
    public ResponseEntity<List<Transaction>> getAllTransactions() {
        // FLAW: No admin role check
        List<Transaction> all = paymentService.getAllTransactions();
        return ResponseEntity.ok(all);  // FLAW: No pagination, could return millions of records
    }
}
