// TransactionStatus.java

package com.fintech.payment.model;

public enum TransactionStatus {
    PENDING,
    COMPLETED,
    FAILED,
    REFUNDED,
    PARTIALLY_REFUNDED
    // FLAW: No state transition validation - can go from any state to any state
}
