# ALX_prodev Database Seeder

## 🎯 Objective

This project sets up a **MySQL database** named `ALX_prodev`, creates a `user_data` table, populates it with sample data from a CSV file, and provides a **Python generator** to stream rows one by one.

---

## 🗂️ Table Structure

The table `user_data` has the following fields:

- `user_id` → Primary Key (UUID), Indexed
- `name` → VARCHAR, required
- `email` → VARCHAR, required, unique
- `age` → DECIMAL, required

---
