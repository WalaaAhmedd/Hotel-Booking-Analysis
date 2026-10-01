# 🏨 Hotel Booking Analysis & Dashboard

## 📌 Project Overview

This project analyzes hotel booking data to understand booking patterns, cancellations, market segments, hotel performance, lead time, pricing, and length of stay.

The project includes:

- Data understanding
- Data cleaning
- Exploratory Data Analysis (EDA)
- Data visualization
- Interactive Streamlit dashboard

---

## 📊 Dataset

The dataset contains hotel booking records with information about:

- Hotel type
- Booking status
- Lead time
- Arrival date
- Length of stay
- Number of guests
- Market segment
- Customer type
- Room type
- ADR
- Cancellation status
- Special requests

The dataset contains 119,390 booking records and 33 columns before cleaning.

---

## 🧹 Data Cleaning

The cleaning process included checking:

- Missing values
- Duplicate records
- Data types
- Categorical values
- Numerical values
- Invalid values

Additional features were created for analysis, including:

- `total_nights`
- `cancellation_status`

---

## 📈 Visualizations

The project includes the following visualizations:

1. Hotel Distribution
2. Cancellation Rate
3. Cancellation by Hotel
4. Bookings by Month
5. ADR by Hotel
6. Lead Time vs Cancellation
7. Market Segment
8. Cancellation Rate by Market Segment
9. Length of Stay

---

## 🖥️ Interactive Dashboard

The project includes a Streamlit dashboard with four sections:

### 📊 Overview
- Cancellation Rate
- Hotel Distribution

### 📈 Bookings
- Bookings by Month
- Market Segment

### ❌ Cancellations
- Cancellation by Hotel
- Cancellation Rate by Market Segment
- Lead Time vs Cancellation

### 🏨 Stay
- ADR by Hotel
- Length of Stay

The dashboard also includes filters for:

- Hotel
- Arrival Year
- Market Segment

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook

---

## ▶️ How to Run the Dashboard

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
