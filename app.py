import streamlit as st
import pandas as pd
import random
import string
import time

# Initialize session state for parameters
if 'parameters' not in st.session_state:
    st.session_state['parameters'] = {
        'Smoking': {'num_orders': 100, 'intensity': 0.5},
        'Spoofing': {'num_orders': 100, 'intensity': 0.5},
        'Wash Trade': {'num_orders': 100, 'intensity': 0.5}
    }

# Function to generate order data
def generate_order_data(num_orders, intensity, scenario, additional_params):
    orders = []
    for _ in range(num_orders):
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200)))
        venue = random.choice(['ABC', 'XYZ', 'DEF'])
        side = random.choice(['Buy', 'Sell'])
        price = round(random.uniform(90, 110), 2)
        quantity = random.randint(1000, 1000000)
        behavior = random.random() < intensity
        order = {
            'order_id': order_id,
            'timestamp': timestamp,
            'venue': venue,
            'side': side,
            'price': price,
            'quantity': quantity,
            'scenario': scenario,
            'behavior': behavior
        }
        order.update(additional_params)
        orders.append(order)
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

# Display existing parameters
st.write("Existing Parameters:")
for param, value in st.session_state['parameters'][scenario].items():
    st.write(f"{param}: {value}")

# Section to add new parameters
st.header("Add New Parameters")

new_param_name = st.text_input("Parameter Name")
new_param_value = st.text_input("Parameter Value")

if st.button("Add Parameter"):
    if new_param_name and new_param_value:
        st.session_state['parameters'][scenario][new_param_name] = new_param_value
        st.success(f"Added parameter {new_param_name} with value {new_param_value} to {scenario} scenario.")
    else:
        st.error("Please enter both parameter name and value.")

# Section to generate and download data
st.header("Generate and Download Data")

if st.button("Generate Data"):
    additional_params = {k: v for k, v in st.session_state['parameters'][scenario].items() if k not in ['num_orders', 'intensity']}
    orders = generate_order_data(num_orders, intensity, scenario, additional_params)
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

