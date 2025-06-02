import streamlit as st
import pandas as pd

# Function to check minimum notional
def check_min_notional(cumulative_qty, threshold):
    return cumulative_qty > threshold

# Function to simulate far side open order interest
def simulate_far_side_open_orders(order_time, lookup_window):
    # Simulate open orders within the lookup window
    # For simplicity, we return a fixed list of open orders
    open_orders = [
        {"order_id": "O1", "venue": "ABC", "base_ccy_qty": 4000000, "side": "Buy", "price": 100},
        {"order_id": "O2", "venue": "XYZ", "base_ccy_qty": 3000000, "side": "Sell", "price": 105}
    ]
    return open_orders

# Function to check market depth availability
def check_market_depth(order_time, lookup_window):
    # Simulate market depth availability
    # For simplicity, we return True
    return True

# Function to compare order price to market depth
def compare_order_price(open_orders, market_depth, side):
    alerts = []
    for order in open_orders:
        if side == "Buy" and order["price"] >= market_depth["best_bid"]:
            alerts.append({"order_id": order["order_id"], "severity": "MediumE"})
        elif side == "Sell" and order["price"] <= market_depth["best_ask"]:
            alerts.append({"order_id": order["order_id"], "severity": "MediumE"})
    return alerts

# Streamlit app
st.title("Smoking Scenario Order Flow")

# Input fields for order data
order_type = st.selectbox("Order Type", ["Filled", "Partially Filled"])
cumulative_qty = st.number_input("Cumulative Quantity (GBP)", min_value=0)
venue = st.text_input("Venue")
price = st.number_input("Price", min_value=0.0)
side = st.selectbox("Side", ["Buy", "Sell"])

# Parameters
threshold = st.number_input("Minimum Notional Threshold (GBP)", min_value=0, value=5000000)
lookup_window = st.number_input("Market Depth Lookup Window (seconds)", min_value=0, value=45)

# Button to run the scenario
if st.button("Run Scenario"):
    # Step 2: Check minimum notional
    if check_min_notional(cumulative_qty, threshold):
        # Step 3: Simulate far side open order interest
        open_orders = simulate_far_side_open_orders(order_type, lookup_window)
        
        # Step 4: Check market depth availability
        if check_market_depth(order_type, lookup_window):
            # Simulate market depth data
            market_depth = {"best_bid": 99, "best_ask": 106}
            
            # Step 5: Compare order price to market depth
            alerts = compare_order_price(open_orders, market_depth, side)
            
            # Display alerts
            if alerts:
                st.write("Alerts:")
                for alert in alerts:
                    st.write(f"Order ID: {alert['order_id']}, Severity: {alert['severity']}")
            else:
                st.write("No alerts triggered.")
        else:
            st.write("Market depth not available. Alert triggered.")
    else:
        st.write("Minimum notional not met. No alert triggered.")


