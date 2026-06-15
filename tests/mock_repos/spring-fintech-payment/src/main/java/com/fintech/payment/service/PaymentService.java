// PaymentService.java - Spring Boot Fintech Payment Service (INTENTIONALLY FLAWED)

package com.fintech.payment.service;

import com.fintech.payment.model.Transaction;
import com.fintech.payment.model.TransactionStatus;
import com.fintech.payment.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

@Service
public class PaymentService {

    @Autowired
    private TransactionRepository transactionRepository;

    private static final String DB_URL = "jdbc:postgresql://localhost:5432/payments";
    private static final String DB_USER = "admin";  // FLAW: Hardcoded DB credentials
    private static final String DB_PASS = "INTENTIONALLY_FAKE_FOR_AUDIT_TEST";  // FLAW: Hardcoded DB password

    @Transactional
    public Transaction processCharge(String accountId, BigDecimal amount, String currency) {
        // FLAW: No validation - amount can be negative, zero, or exceed limits
        // FLAW: No idempotency key check - double-charge risk
        // FLAW: No concurrency control on account balance

        Transaction txn = new Transaction();
        txn.setAccountId(accountId);
        txn.setAmount(amount);
        txn.setCurrency(currency);
        txn.setStatus(TransactionStatus.COMPLETED);  // FLAW: Immediately completed without actual payment processing

        return transactionRepository.save(txn);  // FLAW: No error handling for DB failures
    }

    @Transactional
    public Transaction processRefund(Long transactionId, BigDecimal amount) {
        Transaction original = transactionRepository.findById(transactionId)
            .orElseThrow(() -> new RuntimeException("Transaction not found"));  // FLAW: Generic RuntimeException

        // FLAW: No check that refund amount <= original amount
        // FLAW: No check if already refunded
        // FLAW: No idempotency key

        Transaction refund = new Transaction();
        refund.setAccountId(original.getAccountId());
        refund.setAmount(amount.negate());  // FLAW: Using negate on refund - can create positive refund if amount is negative
        refund.setCurrency(original.getCurrency());
        refund.setStatus(TransactionStatus.REFUNDED);

        return transactionRepository.save(refund);
    }

    // FLAW: Raw JDBC with SQL injection risk
    public List<Transaction> searchTransactions(String query) {
        List<Transaction> results = new ArrayList<>();
        try {
            Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
            // FLAW: SQL injection - query parameter directly in SQL string
            String sql = "SELECT * FROM transactions WHERE account_id LIKE '%" + query + "%'";
            ResultSet rs = conn.createStatement().executeQuery(sql);  // FLAW: Statement instead of PreparedStatement
            while (rs.next()) {
                Transaction txn = new Transaction();
                txn.setId(rs.getLong("id"));
                txn.setAccountId(rs.getString("account_id"));
                results.add(txn);
            }
            conn.close();  // FLAW: Not using try-with-resources - connection leak on exception
        } catch (Exception e) {
            // FLAW: Swallowing exception completely
            e.printStackTrace();  // FLAW: Printing stack trace instead of proper logging
        }
        return results;
    }

    public List<Transaction> getTransactions(String accountId) {
        // FLAW: No pagination
        return transactionRepository.findByAccountId(accountId);
    }

    public List<Transaction> getAllTransactions() {
        // FLAW: No pagination, loads all records
        return transactionRepository.findAll();
    }
}
