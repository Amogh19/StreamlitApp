import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="NFHS Dashboard", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Load the specific CSV you uploaded
    df = pd.read_csv("All India National Family Health Survey.xlsx")
    
    # Cleaning: The sample shows 'NA' values and some empty columns
    df = df.replace('NA', pd.NA)
    # Convert numeric columns to float where possible, skipping the 'STATE' column
    for col in df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Options")

# State Selection
all_states = df['STATE'].unique().tolist()
selected_states = st.sidebar.multiselect("Select States", options=all_states, default=all_states[:5])

# Indicator Selection (excluding metadata columns)
indicators = df.columns[2:].tolist()
selected_indicator = st.sidebar.selectbox("Select Health Indicator", options=indicators)

# Filter Data
filtered_df = df[df['STATE'].isin(selected_states)]

# --- MAIN PANEL ---
st.title("🇮🇳 National Family Health Survey (NFHS) Explorer")
st.markdown(f"Visualizing: **{selected_indicator}** across selected states.")

# --- METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    avg_val = filtered_df[selected_indicator].mean()
    st.metric("Average Value", f"{avg_val:.2f}")
with col2:
    max_state = filtered_df.loc[filtered_df[selected_indicator].idxmax(), 'STATE']
    st.metric("Highest State", max_state)
with col3:
    total_states = len(selected_states)
    st.metric("States Compared", total_states)

st.divider()

# --- VISUALIZATIONS ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("State-wise Comparison")
    fig_bar = px.bar(
        filtered_df, 
        x='STATE', 
        y=selected_indicator, 
        color='STATE',
        text_auto='.2s',
        title=f"{selected_indicator} by State"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("Data Distribution")
    fig_box = px.box(
        df, 
        y=selected_indicator, 
        points="all",
        title="National Distribution Range"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --- RAW DATA ---
with st.expander("View Filtered Dataset"):

    st.write(filtered_df[['STATE', 'nfhs', selected_indicator]])


