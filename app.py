import streamlit as st
import pandas as pd
import random
import string
import time
from io import BytesIO

# Function to generate order data based on scenario logic
def generate_order_data(num_orders, scenario_logic, **kwargs):
    orders = []
    for _ in range(num_orders):
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200)))  # Random timestamp
        venue = random.choice(['ABC', 'XYZ', 'DEF'])
        side = random.choice(['Buy', 'Sell'])
        price = round(random.uniform(90, 110), 2)
        quantity = random.randint(1000, 1000000)
        scenario_behavior = scenario_logic(**kwargs)
        orders.append({
            'order_id': order_id,
            'timestamp': timestamp,
            'venue': venue,
            'side': side,
            'price': price,
            'quantity': quantity,
            'scenario_behavior': scenario_behavior
        })
    return orders

# Example scenario logic functions
def smoking_scenario_logic(smoking_intensity):
    return random.random() < smoking_intensity

def spoofing_scenario_logic(spoofing_intensity):
    return random.random() < spoofing_intensity

def wash_trade_scenario_logic(wash_trade_intensity):
    return random.random() < wash_trade_intensity

# Streamlit app
st.title("Market Abuse Scenario Simulator")

# Section for Generating Order Data
st.header("Generate Order Data")

# Select scenario
scenario = st.selectbox("Select Scenario", ["Smoking", "Spoofing", "Wash Trade"])

# Input fields for order data
num_orders = st.number_input("Number of Orders", min_value=1, value=100)

# Scenario-specific parameters
if scenario == "Smoking":
    smoking_intensity = st.slider("Smoking Behavior Intensity", min_value=0.0, max_value=1.0, value=0.5)
    scenario_logic = smoking_scenario_logic
    scenario_params = {'smoking_intensity': smoking_intensity}
elif scenario == "Spoofing":
    spoofing_intensity = st.slider("Spoofing Behavior Intensity", min_value=0.0, max_value=1.0, value=0.5)
    scenario_logic = spoofing_scenario_logic
    scenario_params = {'spoofing_intensity': spoofing_intensity}
elif scenario == "Wash Trade":
    wash_trade_intensity = st.slider("Wash Trade Behavior Intensity", min_value=0.0, max_value=1.0, value=0.5)
    scenario_logic = wash_trade_scenario_logic
    scenario_params = {'wash_trade_intensity': wash_trade_intensity}

# Button to generate data
if st.button("Generate Data"):
    orders = generate_order_data(num_orders, scenario_logic, **scenario_params)
    df = pd.DataFrame(orders)
    
    st.write("Generated Order Data:")
    st.dataframe(df)

    # Download as CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='order_data.csv',
        mime='text/csv',
    )

    # Download as Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    st.download_button(
        label="Download data as Excel",
        data=processed_data,
        file_name='order_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )

# Section for Adding New Scenarios
st.header("Add New Scenario")

new_scenario_name = st.text_input("Scenario Name")
new_scenario_intensity = st.slider("Scenario Intensity", min_value=0.0, max_value=1.0, value=0.5)

if st.button("Add Scenario"):
    st.write(f"New scenario '{new_scenario_name}' with intensity {new_scenario_intensity} added.")

