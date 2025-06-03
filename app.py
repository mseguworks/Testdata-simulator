import streamlit as st
import pandas as pd
import random
import string
import time

# Function to generate test order data for Smoking scenario
def generate_smoking_data(num_orders, smoking_intensity):
    orders = []
    for _ in range(num_orders):
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200)))  # Random timestamp
        venue = random.choice(['ABC', 'XYZ', 'DEF'])
        side = random.choice(['Buy', 'Sell'])
        price = round(random.uniform(90, 110), 2)
        quantity = random.randint(1000, 1000000)
        smoking_behavior = random.random() < smoking_intensity
        orders.append({
            'order_id': order_id,
            'timestamp': timestamp,
            'venue': venue,
            'side': side,
            'price': price,
            'quantity': quantity,
            'smoking_behavior': smoking_behavior
        })
    return orders

# Function to generate test order data for Spoofing scenario
def generate_spoofing_data(num_orders, spoofing_intensity):
    orders = []
    for _ in range(num_orders):
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200)))  # Random timestamp
        venue = random.choice(['ABC', 'XYZ', 'DEF'])
        side = random.choice(['Buy', 'Sell'])
        price = round(random.uniform(90, 110), 2)
        quantity = random.randint(1000, 1000000)
        spoofing_behavior = random.random() < spoofing_intensity
        orders.append({
            'order_id': order_id,
            'timestamp': timestamp,
            'venue': venue,
            'side': side,
            'price': price,
            'quantity': quantity,
            'spoofing_behavior': spoofing_behavior
        })
    return orders

# Function to generate test order data for Wash Trade scenario
def generate_wash_trade_data(num_orders, wash_trade_intensity):
    orders = []
    for _ in range(num_orders):
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200)))  # Random timestamp
        venue = random.choice(['ABC', 'XYZ', 'DEF'])
        side = random.choice(['Buy', 'Sell'])
        price = round(random.uniform(90, 110), 2)
        quantity = random.randint(1000, 1000000)
        wash_trade_behavior = random.random() < wash_trade_intensity
        orders.append({
            'order_id': order_id,
            'timestamp': timestamp,
            'venue': venue,
            'side': side,
            'price': price,
            'quantity': quantity,
            'wash_trade_behavior': wash_trade_behavior
        })
    return orders

# Streamlit app
st.title("Market Abuse Scenario Simulator")

# Smoking Scenario
st.header("Smoking Scenario")
num_orders_smoking = st.number_input("Number of Orders (Smoking)", min_value=1, value=100)
smoking_intensity = st.slider("Smoking Behavior Intensity", min_value=0.0, max_value=1.0, value=0.5)

if st.button("Generate Smoking Data"):
    smoking_orders = generate_smoking_data(num_orders_smoking, smoking_intensity)
    df_smoking = pd.DataFrame(smoking_orders)
    
    st.write("Generated Smoking Order Data:")
    st.dataframe(df_smoking)

    csv_smoking = df_smoking.to_csv(index=False)
    st.download_button(
        label="Download Smoking Data as CSV",
        data=csv_smoking,
        file_name='smoking_order_data.csv',
        mime='text/csv',
    )

# Spoofing Scenario
st.header("Spoofing Scenario")
num_orders_spoofing = st.number_input("Number of Orders (Spoofing)", min_value=1, value=100)
spoofing_intensity = st.slider("Spoofing Behavior Intensity", min_value=0.0, max_value=1.0, value=0.5)

if st.button("Generate Spoofing Data"):
    spoofing_orders = generate_spoofing_data(num_orders_spoofing, spoofing_intensity)
    df_spoofing = pd.DataFrame(spoofing_orders)
    
    st.write("Generated Spoofing Order Data:")
    st.dataframe(df_spoofing)

    csv_spoofing = df_spoofing.to_csv(index=False)
    st.download_button(
        label="Download Spoofing Data as CSV",
        data=csv_spoofing,
        file_name='spoofing_order_data.csv',
        mime='text/csv',
    )

# Wash Trade Scenario
st.header("Wash Trade Scenario")
num_orders_wash_trade = st.number_input("Number of Orders (Wash Trade)", min_value=1, value=100)
wash_trade_intensity = st.slider("Wash Trade Behavior Intensity", min_value=0.0, max_value=1.0, value=0.5)

if st.button("Generate Wash Trade Data"):
    wash_trade_orders = generate_wash_trade_data(num_orders_wash_trade, wash_trade_intensity)
    df_wash_trade = pd.DataFrame(wash_trade_orders)
    
    st.write("Generated Wash Trade Order Data:")
    st.dataframe(df_wash_trade)

    csv_wash_trade = df_wash_trade.to_csv(index=False)
    st.download_button(
        label="Download Wash Trade Data as CSV",
        data=csv_wash_trade,
        file_name='wash_trade_order_data.csv',
        mime='text/csv',
    )


