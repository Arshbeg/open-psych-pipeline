import pandas as pd
import numpy as np
import os

np.random.seed(42)
os.makedirs('data/raw', exist_ok=True)

def simulate_ecg(duration=120, heart_rate=70, variability=5):
    #we simulate a raw ECG-like signal with R-peaks and noise.
    sampling_rate = 250
    total_samples = duration * sampling_rate
    # basic heartbeat pattern
    period = sampling_rate / (heart_rate / 60.0)
    ecg = np.zeros(total_samples)
    for i in range(0, total_samples, int(period)):
        jitter = np.random.randint(-variability, variability)
        if i + jitter < total_samples:
            ecg[i + jitter] = 1.0 
    
    # Smooth the peaks and add noise
    ecg = np.convolve(ecg, [0.1, 0.5, 1.0, 0.5, 0.1], mode='same')
    return ecg + np.random.normal(0, 0.05, total_samples)

# Generate 30 Participants
participants = []
for i in range(1, 31):
    p_id = f"SUB_{i:03d}"
    group = "Stress" if i % 2 == 0 else "Control"
    difficulty = "High" if np.random.rand() > 0.5 else "Low"
    
    # Logic: Stress + High Difficulty = Very Slow Reaction Times
    base_rt = 400
    rt_penalty = (100 if group == "Stress" else 0) + (150 if difficulty == "High" else 0)
    interaction = 80 if (group == "Stress" and difficulty == "High") else 0
    rt = np.random.normal(base_rt + rt_penalty + interaction, 30)
    
    # Accuracy logic: 0.0 to 1.0
    acc = np.clip(np.random.normal(0.95 - (0.15 if group == "Stress" else 0) - (0.20 if difficulty == "High" else 0), 0.05), 0, 1)

    # Save Signal
    hr = 95 if group == "Stress" else 72
    signal = simulate_ecg(heart_rate=hr, variability=(3 if group == "Stress" else 10))
    file_path = f"data/raw/{p_id}_ecg.csv"
    pd.DataFrame({'ecg': signal}).to_csv(file_path, index=False)

    participants.append({
        "participant_id": p_id, "group": group, "difficulty": difficulty,
        "reaction_time_ms": round(rt, 2), "accuracy": round(acc, 2),
        "raw_file": file_path
    })

# Save Metadata
pd.DataFrame(participants).to_csv('metadata.csv', index=False)
print(" 30 subjects generated.")