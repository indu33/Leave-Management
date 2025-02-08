# Employee Leave Management

## Overview  
**Employee Leave Management** is a Frappe-based application designed to streamline employee leave tracking. It efficiently manages leave balances, automates approvals and rejections, and ensures that leave balances are updated automatically upon approval.

## Features  
- Employee leave tracking  
- Leave balance management  
- Automated leave balance updates upon approval  
- Leave application approvals and rejections  
- Role-based access control  

## Technologies Used  
- **Framework:** Frappe  
- **Server-side:** Python  
- **Client-side:** JavaScript  

## About Employee Leave Management
https://github.com/user-attachments/assets/384e3730-ccf3-4e63-a7d1-1296bb260b00
## Modules and Doctypes
Employee Leave Management is a module built on the Frappe framework to manage employee leave records efficiently. It provides features for leave allocation, leave applications, and tracking leave balances.

## Doctypes
**Main Doctypes**
- **Employees** – Stores employee details.
- **Leave Type** – Defines different types of leaves (e.g., Sick Leave, Annual Leave).
- **Leave Allocation** – Allocates leave balances to employees.
- **Leave Application** – Handles employee leave requests.
- **Leave Balance** – Maintains the leave balance for employees.
  ## Child Tables
- **Remaining Leaves** – Tracks the remaining leave balances.
- **Leave Records** – Logs leave transactions for employees.
## Functionality
When an employee is created, we have to create a corresponding user in the system.
Employees can apply for leave, which goes through an approval process.
Leave balances are updated dynamically based on leave applications and allocations
## Leave Type and Leave Allocation
