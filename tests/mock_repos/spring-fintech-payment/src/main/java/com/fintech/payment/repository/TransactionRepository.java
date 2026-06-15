// TransactionRepository.java

package com.fintech.payment.repository;

import com.fintech.payment.model.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    // FLAW: No pagination support in findByAccountId
    List<Transaction> findByAccountId(String accountId);

    // FLAW: No query method for finding by date range, status, etc.
    // FLAW: No custom queries for reporting/analytics
}
