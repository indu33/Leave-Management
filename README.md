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
https://github.com/user-attachments/assets/18685db4-4bea-4a77-a337-040e8fa6e09f
## Leave Type and Leave Allocation Doctypes
**Leave Type Doctype**
- The Leave Type doctype defines different types of leaves available for employees. It includes a Carry Forward option:

- If the Carry Forward checkbox is enabled, an additional field appears to specify the number of carry-forward leaves allowed.
## Leave Allocation Doctype
- The Leave Allocation doctype manages leave assignments for employees. 
- It includes a child table named Leave Records, which dynamically updates based on specific conditions:

**Gender-Based Leave Allocation:**
- If the employee is female, maternity leave will be enabled in the Leave Records child table.
- If the employee is male, maternity leave will not be included.
**Automatic Leave Allocation:**
Based on the selected Leave Type, the system automatically fetches the allocated leaves and carry-forward leaves into the Leave Records child table.
## Leave Application and Leave Balances
https://github.com/user-attachments/assets/441cbed2-d79a-49bb-9d28-3eadf6c37215

- If the employee is male, the "Maternity" option should not appear in the leave type field if it is only applicable to female employees.
- If the employee selects the same start and end date for leave, it should be calculated as 8 hours. However, if the employee selects the "Half-Day" checkbox, the leave 
  should be calculated as 4 hours.

**Leave Application Workflow**
- **Employee Submission:** Employees must apply for leave from their desk using the Leave Application Doctype.
- **Team Lead Review:** The application is forwarded to the Team Lead for initial approval.
- **Manager Approval:** Upon Team Lead approval, the request is forwarded to the Manager for final approval or rejection.
- **Employee Notification:** Once the Manager approves or rejects the leave, the employee receives an email notification.
- **Leave Balance Update:** If approved, the leave balance is automatically updated in the Leave Balance Doctype.
## Leave Balance Doctype
**The Leave Balance Doctype includes two child tables:**

- **Leave Records:** Stores the originally allocated leaves for the employee.
- **Remaining Leaves:** Displays the number of leaves left for the employee.
## Reports
- **Leave Balance Report:** Displays the current leave balances of employees.
- **Leave Application Summary:** Shows approved, pending, and rejected leave applications.
## Dashboard Cards
**The dashboard includes the following key metrics:**
- Total Leaves Applied
- Pending Approvals
- Employees on Leave Today
## Notifications
**Weekly Pending Leave Application Notification**

https://github.com/user-attachments/assets/4154066d-6917-4f5e-8381-f30de9ad3909
- If any leave application remains pending for approval, a weekly email notification will be sent to the Manager as a reminder.

