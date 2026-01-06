import random
from datetime import datetime, timedelta
import numpy as np

def random_date(start_date, end_date):
    """Generate a random datetime between two dates."""
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start_date + timedelta(seconds=random_second)

def business_day_date(start_date, end_date):
    """Generate a date weighted towards Mon-Wed (Productivity spike)."""
    # Simple rejection sampling for realistic distribution
    while True:
        dt = random_date(start_date, end_date)
        # 0=Mon, 6=Sun. 
        # Weights: Mon-Wed (high), Thu-Fri (med), Sat-Sun (low)
        day = dt.weekday()
        r = random.random()
        
        if day <= 2 and r < 0.9: return dt      # Mon-Wed: 90% accept
        elif day <= 4 and r < 0.6: return dt    # Thu-Fri: 60% accept
        elif day > 4 and r < 0.05: return dt    # Weekend: 5% accept (rare crunch time)

def get_completion_date(created_at, due_date):
    """
    Generate a completion date using log-normal distribution logic.
    Most tasks completed shortly after creation or near due date.
    """
    if not due_date:
        days_to_add = int(np.random.lognormal(mean=2, sigma=1)) # Skewed left
        return created_at + timedelta(days=max(1, days_to_add))
    
    # 70% completed on time, 30% late
    if random.random() < 0.7:
        return random_date(created_at, datetime.combine(due_date, datetime.min.time()))
    else:
        # Overdue by 1-10 days
        return datetime.combine(due_date, datetime.min.time()) + timedelta(days=random.randint(1, 10))