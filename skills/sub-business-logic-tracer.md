---
name: sub-business-logic-tracer
description: Maps user-facing business flows to code paths, identifies business logic correctness and completeness issues, and classifies findings by business impact severity.
parent: code-quality-auditor
---

## Purpose

Technical quality metrics (complexity, coupling, naming) cannot catch broken business logic. A method can have perfect cyclomatic complexity of 1 and still compute a refund incorrectly. This sub-skill audits what the code is *supposed to do* vs. what it *actually does* — tracing the path from user action or API call through to the final system state.

It answers: "Does this code correctly and completely implement the business rules for this domain?"

---

## Inputs

- `source_code`: Entry point files, route/controller files, service/domain layer, data access layer
- `business_purpose`: The stated domain and purpose from Stage 0 (e.g., "healthcare appointment booking API")
- `known_concerns`: Any pain points, production incidents, or known edge cases from the user

---

## Workflow

### Step 1: Entry Point Discovery

Identify all public entry points to the system:
- HTTP endpoints / routes (REST, GraphQL, WebSocket)
- CLI commands
- Scheduled jobs / cron triggers
- Event consumers (Kafka, SQS, pub/sub)
- Public API methods in a library

List each entry point with: method signature / route, HTTP method (if applicable), and what business action it represents.

Example output:
```
Entry Points Discovered:
1. POST /api/v1/appointments — Create appointment booking
2. GET /api/v1/appointments/{id} — Retrieve appointment details
3. DELETE /api/v1/appointments/{id} — Cancel appointment
4. POST /api/v1/appointments/{id}/reschedule — Reschedule appointment
5. PUT /api/v1/patients/{id}/insurance — Update insurance info
```

### Step 2: Business Flow Selection

Select 3–5 of the most critical business flows to trace fully. Prioritize by:
1. Revenue-critical or data-integrity-critical flows (payment, booking, records update)
2. Flows mentioned in the user's known concerns
3. Flows with the most complex code paths (longest call chain)

Document the selected flows and rationale.

### Step 3: Code Path Tracing

For each selected flow, trace the execution path from entry point to final state change (DB write, external API call, response). Document:

```
Flow: Create Appointment Booking
Trigger: POST /api/v1/appointments
→ AppointmentController.create_appointment() [controllers/appointment_controller.py:45]
  → AppointmentValidator.validate_request() [validators/appointment.py:12]
  → DoctorAvailabilityService.check_slot() [services/availability.py:78]
    → DoctorRepository.get_availability() [repositories/doctor.py:34]
  → AppointmentService.create() [services/appointment.py:112]
    → AppointmentRepository.save() [repositories/appointment.py:67]
    → NotificationService.send_confirmation() [services/notification.py:23]
Response: 201 Created with appointment details
```

### Step 4: Business Rule Validation

For each traced flow, systematically check:

**Correctness checks:**
- Does the code implement the stated business rule correctly?
  - Example: Does a discount calculation apply the correct formula?
  - Example: Does an age verification correctly compute age from date of birth (not just compare year)?
- Are boundary conditions handled? (e.g., booking at exactly midnight, zero-quantity order, negative balance)
- Are mathematical operations using correct precision? (e.g., financial amounts should not use floating point)
- Are state transitions valid? (e.g., can a cancelled appointment be rescheduled? should it be allowed?)

**Completeness checks:**
- Are all required validation rules present at the entry point?
- Are authorization checks performed before accessing data (not just authenticating the user)?
- Are all failure paths handled and communicated correctly to the caller?
- Are idempotency concerns addressed for write operations?
- Are concurrent modification scenarios handled (e.g., two users booking the same slot)?

**Edge case checks:**
- What happens when optional fields are absent?
- What happens when external service calls fail (timeout, 500 error)?
- What happens with unicode, special characters, or max-length inputs?
- What happens at the boundary of date/time changes (DST, timezone, end of day)?

### Step 5: Classification and Finding Recording

Record each finding with:

```
[BL-XXX] | Severity | Flow | Description | File:Line | Business Impact | Recommended Fix
```

**Severity classification:**
- **Critical**: Logic error that produces incorrect output, data corruption risk, or unauthorized access. Must be fixed before next release.
- **Major**: Functional gap — the feature is incomplete or fails under predictable real-world conditions (not just edge cases).
- **Minor**: Robustness improvement — the code works in the happy path but could be more complete or defensive.

---

## Output

A structured business logic audit section:

```
## Business Logic Trace

### Entry Points (N found)
[table of entry points]

### Flows Traced

#### Flow 1: [Name]
Trigger: [entry point]
Code Path:
  → [step-by-step with file:line]
Business Rules Checked: [list]

#### Flow 2: [Name]
...

### Business Logic Findings

| ID | Severity | Flow | Description | File:Line | Business Impact | Fix |
|---|---|---|---|---|---|---|
| BL-001 | Critical | Create Appointment | No check for duplicate booking within same time slot — two concurrent requests can create conflicting appointments | services/appointment.py:112 | Double-booking risk; patient receives conflicting confirmations | Add optimistic locking / unique constraint on (doctor_id, slot_time) |
| BL-002 | Major | Cancel Appointment | Cancellation refund not triggered when appointment is cancelled by doctor | services/appointment.py:189 | Patients are not refunded for doctor-cancelled appointments | Add refund trigger in cancellation service for doctor-initiated cancels |
| BL-003 | Minor | Reschedule | Timezone not normalized before saving rescheduled time | services/appointment.py:234 | Could cause display discrepancy for international users | Normalize all datetimes to UTC at entry point |

### Summary
- Critical: N findings
- Major: N findings
- Minor: N findings
- Most critical flow: [name] (N critical findings)
```

---

## Quality Gate

Before returning to the parent skill:
- [ ] At least 3 distinct business flows have been fully traced (entry point → all code layers → final state)
- [ ] Each traced flow has at least one positive observation OR at least one finding
- [ ] All Critical findings have a file:line reference and a concrete recommended fix
- [ ] Concurrency/idempotency was checked for every write operation in traced flows
- [ ] Authorization checks were verified (not just authentication) in all flows involving data access
