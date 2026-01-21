# Sleeper Bus Ticket Booking System

## 📌 Project Overview
The **Sleeper Bus Ticket Booking System** is a full-stack web application designed to demonstrate a bus seat booking platform. It features an interactive user interface for selecting seats, a backend API for managing bookings, and a mock AI/ML module to predict booking confirmation probabilities.

This project uses **FastAPI** for the backend and **Streamlit** for the frontend, showcasing a clean separation of concerns and a modern Python-based tech stack.

---

## 🚀 How It Works

The system is divided into three main components:

### 1. Backend (`backend/main.py`)
The backend is built with **FastAPI** and serves as the core logic engine.
-   **In-Memory Database**: It uses a Python dictionary (`SEATS_DB`) to temporarily store the state of 20 sleeper seats (Lower and Upper berths) during the session.
-   **REST API Endpoints**:
    -   `GET /seats`: Fetches the current status of all seats.
    -   `GET /stations`: Returns the route stations and arrival times.
    -   `POST /book-seat`: Handles seat booking logic, preventing double bookings.
    -   `POST /cancel-booking`: Allows users to cancel their reservations.
    -   `POST /predict-probability`: Uses the ML logic to estimate booking success chances.

### 2. Machine Learning Logic (`backend/ml_logic.py`)
This module simulates an AI model. In a real-world scenario, this would likely be a Logistic Regression model trained on historical data (as described in `Prediction_Approach.md`).
-   For this demo, it uses **heuristic rules** to calculate a "Confirmation Probability":
    -   **Days Prior**: Booking earlier increases the probability.
    -   **Seat Type**: Sleeper seats have higher biological demand.
    -   **Weekend**: Travel on weekends affects the score.
    -   **Random Noise**: A small random factor is added to simulate real-world variance.

### 3. Frontend (`frontend/app.py`)
The frontend is built with **Streamlit**, providing a user-friendly web interface.
-   **Seat Map**: Visualizes seats in a grid. Red (🔴) indicates booked, and Green (🟢) indicates available.
-   **API Integration**: It makes HTTP requests to the FastAPI backend to fetch data and submit bookings.
-   **Sidebar**: Displays route information and the Booking Probability estimator tool.

---

## 🛠️ Technology Stack
-   **Information Backend**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **HTTP Client**: `requests`
-   **Data Processing**: `pandas`
-   **Model Validation**: `pydantic`

---

## ⚙️ Installation & Setup

Follow these steps to run the application locally.

### Prerequisites
-   Python 3.8 or higher installed.

### 1. Install Dependencies
Open your terminal/command prompt and navigate to the project folder. Run:
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
In a **new terminal window**, run the FastAPI backend:
```bash
uvicorn backend.main:app --reload
```
*You should see output indicating the server is running at `http://127.0.0.1:8000`.*

### 3. Start the Frontend Application
In a **separate terminal window**, run the Streamlit frontend:
```bash
streamlit run frontend/app.py
```
*Depending on your system, this will usually auto-open `http://localhost:8501` in your web browser.*

---

## 📖 Usage Guide

1.  **View Route**: Check the sidebar to see the stations from Ahmedabad to Mumbai.
2.  **Check Probability**: use the "Booking Probability" tool in the sidebar. Adjust "Days before travel" and click **Predict** to see the AI estimation.
3.  **Book a Seat**:
    -   Look at the "Select a Seat" section.
    -   Find a Green (🟢) seat ID.
    -   Scroll down to "Booking Details", select "Book a Seat", choose the ID, enter your name, and click "Confirm Booking".
    -   The seat will turn Red (🔴).
4.  **Cancel a Booking**:
    -   Select "Cancel Booking" in the "Booking Details" section.
    -   Choose your booked seat and confirm to release it.

---

## 📂 Project Structure
```
ScaleTech Task/
├── backend/
│   ├── main.py        # FastAPI application & endpoints
│   └── ml_logic.py    # Mock prediction logic
├── frontend/
│   └── app.py         # Streamlit dashboard
├── Prediction_Approach.md # Explains the ML concept vs implementation
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```
