## 1. Proposed Model (Conceptual)

### Model Name: Logistic Regression (Conceptual)

Logistic Regression is proposed because:
- It is commonly used for **binary classification problems**
- It outputs results in the form of **probabilities**
- It is easy to interpret and explain

In this case:
- **1** → Booking Confirmed  
- **0** → Booking Cancelled  

> The model is not trained in real-time.  
> The logic is **simulated** using historical ratios.

---

## 2. Mock Training Dataset

The following dataset represents **historical booking data** (simulated):

| Total Bookings | Confirmed Bookings | Cancelled Bookings |
|---------------|-------------------|-------------------|
| 100           | 75                | 25                |
| 80            | 60                | 20                |
| 50            | 38                | 12                |
| 120           | 90                | 30                |

This dataset is used only to understand booking trends.

---

## 3. Training Methodology (Simulated)

1. Historical booking data is analyzed.
2. Confirmation rate is calculated for each record.
3. An average confirmation percentage is derived.
4. This percentage is used as the predicted probability for new bookings.

No real model training or optimization is performed.

---

## 4. Prediction Logic

The confirmation probability is calculated using the formula:


### Example:
- Total Bookings = 100  
- Confirmed = 75  


---

## 5. Final Prediction Output

For a new booking, the system predicts:

**✅ Booking Confirmation Probability: 75%**

This means there is a **75% chance** that the booking will remain confirmed based on past trends.

---

## 6. Conclusion

This mock prediction module demonstrates:
- Understanding of AI/ML fundamentals
- Ability to translate data into insights
- Clear and explainable prediction logic

The focus of this approach is **clarity and reasoning**, which aligns with the expectations for an **AI/ML internship role**.
