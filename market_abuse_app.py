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

{
    "chunks": [
        {
            "type": "txt",
            "chunk_number": 1,
            "lines": [
                {
                    "line_number": 1,
                    "text": "import streamlit as st"
                },
                {
                    "line_number": 2,
                    "text": "import pandas as pd"
                },
                {
                    "line_number": 3,
                    "text": ""
                },
                {
                    "line_number": 4,
                    "text": "# Function to check minimum notional"
                },
                {
                    "line_number": 5,
                    "text": "def check_min_notional(cumulative_qty, threshold):"
                },
                {
                    "line_number": 6,
                    "text": "return cumulative_qty > threshold"
                },
                {
                    "line_number": 7,
                    "text": ""
                },
                {
                    "line_number": 8,
                    "text": "# Function to simulate far side open order interest"
                },
                {
                    "line_number": 9,
                    "text": "def simulate_far_side_open_orders(order_time, lookup_window):"
                },
                {
                    "line_number": 10,
                    "text": "# Simulate open orders within the lookup window"
                },
                {
                    "line_number": 11,
                    "text": "# For simplicity, we return a fixed list of open orders"
                },
                {
                    "line_number": 12,
                    "text": "open_orders = ["
                },
                {
                    "line_number": 13,
                    "text": "{\"order_id\": \"O1\", \"venue\": \"ABC\", \"base_ccy_qty\": 4000000, \"side\": \"Buy\", \"price\": 100},"
                },
                {
                    "line_number": 14,
                    "text": "{\"order_id\": \"O2\", \"venue\": \"XYZ\", \"base_ccy_qty\": 3000000, \"side\": \"Sell\", \"price\": 105}"
                },
                {
                    "line_number": 15,
                    "text": "]"
                },
                {
                    "line_number": 16,
                    "text": "return open_orders"
                },
                {
                    "line_number": 17,
                    "text": ""
                },
                {
                    "line_number": 18,
                    "text": "# Function to check market depth availability"
                },
                {
                    "line_number": 19,
                    "text": "def check_market_depth(order_time, lookup_window):"
                },
                {
                    "line_number": 20,
                    "text": "# Simulate market depth availability"
                },
                {
                    "line_number": 21,
                    "text": "# For simplicity, we return True"
                },
                {
                    "line_number": 22,
                    "text": "return True"
                },
                {
                    "line_number": 23,
                    "text": ""
                },
                {
                    "line_number": 24,
                    "text": "# Function to compare order price to market depth"
                },
                {
                    "line_number": 25,
                    "text": "def compare_order_price(open_orders, market_depth, side):"
                },
                {
                    "line_number": 26,
                    "text": "alerts = []"
                },
                {
                    "line_number": 27,
                    "text": "for order in open_orders:"
                },
                {
                    "line_number": 28,
                    "text": "if side == \"Buy\" and order[\"price\"] >= market_depth[\"best_bid\"]:"
                },
                {
                    "line_number": 29,
                    "text": "alerts.append({\"order_id\": order[\"order_id\"], \"severity\": \"MediumE\"})"
                },
                {
                    "line_number": 30,
                    "text": "elif side == \"Sell\" and order[\"price\"] <= market_depth[\"best_ask\"]:"
                },
                {
                    "line_number": 31,
                    "text": "alerts.append({\"order_id\": order[\"order_id\"], \"severity\": \"MediumE\"})"
                },
                {
                    "line_number": 32,
                    "text": "return alerts"
                },
                {
                    "line_number": 33,
                    "text": ""
                },
                {
                    "line_number": 34,
                    "text": "# Streamlit app"
                },
                {
                    "line_number": 35,
                    "text": "st.title(\"Smoking Scenario Order Flow\")"
                },
                {
                    "line_number": 36,
                    "text": ""
                },
                {
                    "line_number": 37,
                    "text": "# Input fields for order data"
                },
                {
                    "line_number": 38,
                    "text": "order_type = st.selectbox(\"Order Type\", [\"Filled\", \"Partially Filled\"])"
                },
                {
                    "line_number": 39,
                    "text": "cumulative_qty = st.number_input(\"Cumulative Quantity (GBP)\", min_value=0)"
                },
                {
                    "line_number": 40,
                    "text": "venue = st.text_input(\"Venue\")"
                },
                {
                    "line_number": 41,
                    "text": "price = st.number_input(\"Price\", min_value=0.0)"
                },
                {
                    "line_number": 42,
                    "text": "side = st.selectbox(\"Side\", [\"Buy\", \"Sell\"])"
                },
                {
                    "line_number": 43,
                    "text": ""
                },
                {
                    "line_number": 44,
                    "text": "# Parameters"
                },
                {
                    "line_number": 45,
                    "text": "threshold = st.number_input(\"Minimum Notional Threshold (GBP)\", min_value=0, value=5000000)"
                },
                {
                    "line_number": 46,
                    "text": "lookup_window = st.number_input(\"Market Depth Lookup Window (seconds)\", min_value=0, value=45)"
                },
                {
                    "line_number": 47,
                    "text": ""
                },
                {
                    "line_number": 48,
                    "text": "# Button to run the scenario"
                },
                {
                    "line_number": 49,
                    "text": "if st.button(\"Run Scenario\"):"
                },
                {
                    "line_number": 50,
                    "text": "# Step 2: Check minimum notional"
                },
                {
                    "line_number": 51,
                    "text": "if check_min_notional(cumulative_qty, threshold):"
                },
                {
                    "line_number": 52,
                    "text": "# Step 3: Simulate far side open order interest"
                },
                {
                    "line_number": 53,
                    "text": "open_orders = simulate_far_side_open_orders(order_type, lookup_window)"
                },
                {
                    "line_number": 54,
                    "text": ""
                },
                {
                    "line_number": 55,
                    "text": "# Step 4: Check market depth availability"
                },
                {
                    "line_number": 56,
                    "text": "if check_market_depth(order_type, lookup_window):"
                },
                {
                    "line_number": 57,
                    "text": "# Simulate market depth data"
                },
                {
                    "line_number": 58,
                    "text": "market_depth = {\"best_bid\": 99, \"best_ask\": 106}"
                },
                {
                    "line_number": 59,
                    "text": ""
                },
                {
                    "line_number": 60,
                    "text": "# Step 5: Compare order price to market depth"
                },
                {
                    "line_number": 61,
                    "text": "alerts = compare_order_price(open_orders, market_depth, side)"
                },
                {
                    "line_number": 62,
                    "text": ""
                },
                {
                    "line_number": 63,
                    "text": "# Display alerts"
                },
                {
                    "line_number": 64,
                    "text": "if alerts:"
                },
                {
                    "line_number": 65,
                    "text": "st.write(\"Alerts:\")"
                },
                {
                    "line_number": 66,
                    "text": "for alert in alerts:"
                },
                {
                    "line_number": 67,
                    "text": "st.write(f\"Order ID: {alert['order_id']}, Severity: {alert['severity']}\")"
                },
                {
                    "line_number": 68,
                    "text": "else:"
                },
                {
                    "line_number": 69,
                    "text": "st.write(\"No alerts triggered.\")"
                },
                {
                    "line_number": 70,
                    "text": "else:"
                },
                {
                    "line_number": 71,
                    "text": "st.write(\"Market depth not available. Alert triggered.\")"
                },
                {
                    "line_number": 72,
                    "text": "else:"
                },
                {
                    "line_number": 73,
                    "text": "st.write(\"Minimum notional not met. No alert triggered.\")"
                },
                {
                    "line_number": 74,
                    "text": ""
                },
                {
                    "line_number": 75,
                    "text": ""
                }
            ],
            "token_count": 475
        }
    ]
}


