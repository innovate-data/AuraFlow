import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def generate_industrial_data(days=30, frequency='5T'):
    """
    Generates synthetic SCADA data for a pipeline pump station.
    frequency='5T' means 5-minute intervals.
    """
    # 1. Create Time Index
    start_date = datetime(2026, 1, 1)
    periods = days * 24 * 12  # 12 intervals per hour
    time_index = [start_date + timedelta(minutes=5*i) for i in range(periods)]
    
    n = len(time_index)
    
    # 2. Base Signals (Normal Operation)
    # Pressure: Sinusoidal daily fluctuation + noise
    pressure = 800 + 20 * np.sin(np.linspace(0, days * 2 * np.pi, n)) + np.random.normal(0, 2, n)
    
    # Temperature: Slowly rising during the day
    temp = 65 + 10 * np.sin(np.linspace(0, days * 2 * np.pi, n)) + np.random.normal(0, 0.5, n)
    
    # Vibration: Steady state with minor variance
    vibration = 0.05 + np.random.normal(0, 0.005, n)

    # 3. Inject Anomalies (The "Interesting" Part)
    # Leak (Pressure Drop) - Day 10
    pressure[2880:3000] -= 150 
    
    # Bearing Failure (Vibration Spike) - Day 20
    vibration[5760:5800] *= 5 
    
    # Sensor Drift (Temperature climbing) - Day 25 onwards
    temp[7200:] += np.linspace(0, 15, n - 7200)

    # 4. Create DataFrame
    df = pd.DataFrame({
        'timestamp': time_index,
        'pressure_psi': pressure,
        'temp_f': temp,
        'vibration_mm_s': vibration,
        'label': 0  # 0 for normal
    })

    # Mark anomalies in the label column for validation
    df.iloc[2880:3000, df.columns.get_loc('label')] = 1
    df.iloc[5760:5800, df.columns.get_loc('label')] = 1
    df.iloc[7200:, df.columns.get_loc('label')] = 1
    
    return df

# Generate and Save
df_industrial = generate_industrial_data()
df_industrial.to_csv('synthetic_pump_data.csv', index=False)

print("✅ Dataset generated with 3 specific anomaly types: Leak, Bearing Failure, and Sensor Drift.")