import pandas as pd
import neurokit2 as nk
import os

# input & output directories
RAW_DIR = "data/raw/"
PROCESSED_DIR = "data/processed/"
os.makedirs(PROCESSED_DIR, exist_ok=True) 

def run_processing_station():
    metadata = pd.read_csv('metadata.csv')

    extracted_hrv_data = []

    # Go through all 30 participants one by one
    for index, row in metadata.iterrows():
        p_id = row['participant_id']
        file_path = row['raw_file']
        
        print(f"Cleaning and extracting HRV for {p_id}")
        
        try:
            raw_data = pd.read_csv(file_path)
            
            # NeuroKit2 filteer
            # This applies a bandpass filter to remove sensor noise and finds the exact millisecond of every heartbeat.
            signals, info = nk.ecg_process(raw_data['ecg'], sampling_rate=250)
            
            # calculate Heart Rate Variability
            # We pass the detected heartbeats (peaks) to get time-domain HRV metrics.
            hrv_metrics = nk.hrv_time(peaks=info, sampling_rate=250)
    
            hrv_metrics['participant_id'] = p_id
            extracted_hrv_data.append(hrv_metrics)
            
        except Exception as e:
            # catch errors
            print(f"Error processing {p_id}: {e}")
            
    # combine all 30 rows of new heart metrics into one table
    all_hrv_df = pd.concat(extracted_hrv_data, ignore_index=True)
    
    # glue the Behavioral Data and Physiological Data together
    final_processed_data = pd.merge(metadata, all_hrv_df, on='participant_id', how='left')
    
    # save output!
    output_file = os.path.join(PROCESSED_DIR, 'processed_data.csv')
    final_processed_data.to_csv(output_file, index=False)
    
    print(f"\n Processed file saved to: {output_file}")

if __name__ == "__main__":
    run_processing_station()