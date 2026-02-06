# 🚀 Performance Optimization Report

This document records the performance evolution of the ETL pipeline.
**Test Environment:** [Ryzen 5 5600G] / [16GB DDR4]
**Dataset:** 10 Million records (Synthetically generated)

## Execution History

| Version | Key Change | Total Time | Throughput (rows/s) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **v1** | Initial implementation with `uuid.UUID` and `Decimal` objects | ~546s (9m06s) | ~18,315/s | ✅ Success |
| **v2** | Removal of `uuid.UUID` (primitive str) + Fraud discarding | ~325s (5m25s) | ~24,615/s | ✅ Success |
| **v3** | Full Persistence (10M inserts - including Frauds) | ~376s (6m16s) | ~26,595/s | ✅ Success |
| **v4** | **Architecture Refactor (CLI), Python 3.12 & Flush Fix** | **~248s (4m08s)** | **~40,274/s** | 🚀 **Record** |

## Technical Analysis

### v1 -> v2: The Strong Typing Bottleneck
Profiling `v1` revealed that Python's `uuid.UUID` class consumed about **33% of total time** just validating strings in the constructor. Migrating to primitive `str` in the Domain layer reduced total time by ~40%.

### v2 -> v3: Scale Efficiency (Batch Processing)
Even with a 25% increase in write load (persisting frauds instead of discarding), throughput improved, proving that I/O bottlenecks were successfully mitigated by efficient *Batch Inserts*.

### v3 -> v4: Stability & Runtime Optimization (The Leap)
Version v4 consolidated the move to a modular CLI architecture and fixed buffer flush edge cases.
* **Key Factor:** The combination of cleaner code (less object overhead) and native **Python 3.12** optimizations resulted in a massive **51% throughput jump**.
* **Result:** Processing 10 million complex records in just 4 minutes, running locally on SQLite.