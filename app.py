import streamlit as st
import pandas as pd
import random
import string
import time

# Initialize session state for parameters and validation steps
if 'parameters' not in st.session_state:
    st.session_state['parameters'] = {
        'Smoking': {'num_orders': 100, 'intensity': 0.5}
    }

if 'validation_steps' not in st.session_state:
    st.session_state['validation_steps'] = {
        'Smoking': [
            "Identify Near Side based on the side of the executed order",
            "Only consider Filled or Partially Filled orders",
            "Notional Amount > £5,000,000",
            "Check for Far Side orders for potential abuse",
            "Far Side orders must be: Placed within 45 seconds before Near Side execution, Event type New or Amended, Notional ≤ £5,000,000",
            "Far Side order must be at the top of the book, verified using market depth from the same venue",
            "If all conditions are met, trigger an alert"
        ]
    }

# Function to generate order data
def generate_order_data(num_orders, intensity, scenario):
    orders = []
    for _ in range(num_orders):
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200)))
        venue = random.choice(['ABC', 'XYZ', 'DEF'])
        side = random.choice(['Buy', 'Sell'])
        price = round(random.uniform(90, 110), 2)
        quantity = random.randint(1000, 1000000)
        behavior = random.random() < intensity
        orders.append({
            'order_id': order_id,
            'timestamp': timestamp,
            'venue': venue,
            'side': side,
            'price': price,
            'quantity': quantity,
            'scenario': scenario,
            'behavior': behavior
        })
    return orders

# Streamlit app
st.title("Market Abuse Scenario Simulator")

# Section to view and configure parameters
st.header("Configure Scenario Parameters")

scenario = st.selectbox("Select Scenario", list(st.session_state['parameters'].keys()))

st.subheader(f"Parameters for {scenario}")
num_orders = st.number_input("Number of Orders", min_value=1, value=st.session_state['parameters'][scenario]['num_orders'])
intensity = st.slider("Behavior Intensity", min_value=0.0, max_value=1.0, value=st.session_state['parameters'][scenario]['intensity'])

# Update parameters in session state
st.session_state['parameters'][scenario]['num_orders'] = num_orders
st.session_state['parameters'][scenario]['intensity'] = intensity

# Section to view and configure validation steps
st.header("Configure Validation Steps")

st.subheader(f"Validation Steps for {scenario}")
for i, step in enumerate(st.session_state['validation_steps'][scenario]):
    new_step = st.text_area(f"Step {i+1}", value=step, key=f"step_{i}")
    st.session_state['validation_steps'][scenario][i] = new_step

# Section to add new validation steps
st.subheader("Add New Validation Step")

new_step = st.text_area("New Step Description", key="new_step")

if st.button("Add Validation Step"):
    if new_step:
        st.session_state['validation_steps'][scenario].append(new_step)
        st.success(f"Added new validation step to {scenario} scenario.")
    else:
        st.error("Please enter a step description.")

# Section to generate and download data
st.header("Generate and Download Data")

if st.button("Generate Data"):
    orders = generate_order_data(num_orders, intensity, scenario)
    df = pd.DataFrame(orders)
    
    st.write("Generated Order Data:")
    st.dataframe(df)

    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='order_data.csv',
        mime='text/csv',
    )

    excel = df.to_excel(index=False)
    st.download_button(
        label="Download data as Excel",
        data=excel,
        file_name='order_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )

