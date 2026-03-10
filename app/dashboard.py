import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page Configuration
st.set_page_config(page_title="Project Sentinel", layout="wide")
st.title("🧠 Project Sentinel: Stress & Cognitive Load Analysis")
st.markdown("**An Open-Science Pipeline for Physiological Data Valorization**")
st.divider()

#Load the Data 
@st.cache_data
def load_data():
    # master data(Python)
    df = pd.read_csv("data/processed/processed_data.csv")
    # statistical results (R)
    stats_rt = pd.read_csv("data/processed/stats_rt_results.csv")
    stats_hrv = pd.read_csv("data/processed/stats_hrv_results.csv")
    return df, stats_rt, stats_hrv

df, stats_rt, stats_hrv = load_data()

# sidebar: Interactive Participant Selector
st.sidebar.header("🔬 Participant Explorer")
st.sidebar.write("Select a subject to view their specific physiological data.")

participant_list = df['participant_id'].unique()
selected_pid = st.sidebar.selectbox("Subject ID:", participant_list)

# Filter data for the selected subject
sub_data = df[df['participant_id'] == selected_pid].iloc[0]

st.sidebar.subheader("Subject Profile")
st.sidebar.write(f"**Condition:** {sub_data['group']}")
st.sidebar.write(f"**Task Difficulty:** {sub_data['difficulty']}")
st.sidebar.write(f"**Reaction Time:** {sub_data['reaction_time_ms']} ms")
st.sidebar.write(f"**HRV (RMSSD):** {round(sub_data['HRV_RMSSD'], 2)}")

# Main View: Global Research Findings
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Behavioral Performance")
    st.write("Reaction Time across conditions.")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x="difficulty", y="reaction_time_ms", hue="group", palette="Set2", ax=ax)
    ax.set_title("Interaction: Stress vs Cognitive Load")
    ax.set_ylabel("Reaction Time (ms)")
    st.pyplot(fig)

with col2:
    st.header("🫀 Physiological Response")
    st.write("Heart Rate Variability (RMSSD). Lower = Stressed.")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x="difficulty", y="HRV_RMSSD", hue="group", palette="magma", ax=ax2)
    ax2.set_title("Autonomic Nervous System Response")
    ax2.set_ylabel("HRV (RMSSD)")
    st.pyplot(fig2)

st.divider()

# Deep Dive: Raw Signal Inspection
st.header(f"📈 Raw Signal Inspection: {selected_pid}")
st.write("Displaying a 5-second window of the 250Hz ECG recording. This demonstrates our capacity to link aggregated metrics back to raw sensor data.")

# Load the specific raw file for the selected user dynamically
raw_file_path = sub_data['raw_file']
if os.path.exists(raw_file_path):
    raw_ecg = pd.read_csv(raw_file_path)
    
    # Plot just the first 5 seconds (1250 samples at 250Hz)
    fig3, ax3 = plt.subplots(figsize=(15, 3))
    ax3.plot(raw_ecg['ecg'][:1250], color='crimson', linewidth=1)
    ax3.set_title(f"Raw ECG Waveform - {selected_pid}")
    ax3.set_xlabel("Samples (250Hz)")
    ax3.set_ylabel("Voltage")
    st.pyplot(fig3)
else:
    st.error(f"Raw file not found at {raw_file_path}")

st.divider()

#R Statistical Output 
st.header("📝 Methodological Analysis (Linear Models)")
st.write("Statistical validation computed via R (`lm`), dynamically imported into the Python environment.")

st_col1, st_col2 = st.columns(2)
with st_col1:
    st.subheader("Behavioral Model (Reaction Time)")
    st.dataframe(stats_rt)
with st_col2:
    st.subheader("Physiological Model (HRV)")
    st.dataframe(stats_hrv)