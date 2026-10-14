# SeatSmart – Advanced Event Seating Optimizer

SeatSmart is a Python Flask application for automatically assigning event guests to Hall and Balcony seats.

The project uses:

- Python
- Flask
- Object-Oriented Programming
- Backtracking
- Constraint Satisfaction
- HTML
- CSS
- JavaScript
- Excel
- Pytest

---

# Project Objective

The objective of SeatSmart is to automatically assign guests to event seats while respecting:

1. Guest groups
2. Preferred seating sections
3. VIP priority
4. Together constraints
5. Apart constraints
6. Hall capacity
7. Balcony capacity

---

# Venue Capacity

Hall:

300 seats

Balcony:

200 seats

Total:

500 seats

---

# Project Pages

## Home Page

URL:

http://127.0.0.1:5000/

Features:

- Project introduction
- Capacity overview
- Start application
- Guest manager navigation

---

## Venue Setup

URL:

http://127.0.0.1:5000/setup

Features:

- Hall Only
- Balcony Only
- Hall + Balcony
- Capacity configuration
- Venue validation

---

## Guest Manager

URL:

http://127.0.0.1:5000/guests

Features:

- Add guest modal
- Delete guest
- Search guest
- VIP selection
- Group selection
- Preferred section
- Excel upload
- Excel template
- CSV download
- Together constraints
- Apart constraints
- Demo data
- Automatic seating

---

## Result Page

URL:

http://127.0.0.1:5000/result

Features:

- Hall seating plan
- Balcony seating plan
- Seat numbers
- Total guests
- Remaining seats
- Search nodes
- Backtracking count
- Execution time
- Algorithm efficiency
- Excel result download

---

# Demo 1

Hall Demo

300 Guests

Hall Capacity:

300

Balcony Capacity:

0

Result:

300 / 300

HOUSE FULL

---

# Demo 2

Balcony Demo

200 Guests

Hall Capacity:

0

Balcony Capacity:

200

Result:

200 / 200

HOUSE FULL

---

# Demo 3

Hall + Balcony Demo

Hall:

300 Guests

Balcony:

200 Guests

Total:

500 Guests

Result:

500 / 500

HOUSE FULL

---

# Excel Format

Required column:

Name

Optional columns:

Group

Priority

Preferred Section

Example:

| Name | Group | Priority | Preferred Section |
|------|------|------|------|
| Mercypriya | Family | VIP | Hall |
| Priyanjali | Family | Standard | Hall |
| Rahul | Friends | Standard | Balcony |
| Anjali | Friends | VIP | Balcony |

---

# Installation

Open the project folder in VS Code.

Open VS Code terminal.

Run:

```powershell
python -m venv venv