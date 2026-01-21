
import random

def predict_booking_probability(days_prior: int, seat_type: str, is_weekend: bool) -> float:
    """
    Predicts the probability of booking confirmation based on mock historical data factors.
    
    Args:
        days_prior (int): Number of days before travel.
        seat_type (str): 'Sleeper' or 'Seater' (in this system generally Sleeper).
        is_weekend (bool): Whether the travel date is a weekend.
        
    Returns:
        float: Probability percentage (0.0 to 100.0).
    """
    
    # Base probability
    prob = 50.0
    
    # Factor 1: Days Prior (Earlier booking = Higher chance)
    if days_prior > 10:
        prob += 30
    elif days_prior > 3:
        prob += 15
    else:
        prob -= 10
        
    # Factor 2: Seat Type (Sleeper usually high demand)
    if seat_type.lower() == 'sleeper':
        prob += 10
        
    # Factor 3: Weekend (Higher demand, but also higher cancellation if plans change?)
    # Let's assume Weekend travel is more confirmed.
    if is_weekend:
        prob += 5
    
    # Add some randomness to simulate real-world variance
    noise = random.uniform(-5, 5)
    prob += noise
    
    # Clamp value between 0 and 100
    return max(0.0, min(100.0, round(prob, 2)))
