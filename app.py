import streamlit as st
import pandas as pd
import random
import string
import time
import io

# Constants
ATTRIBUTES = [
    'SeqNum', 'OrderDetailsId', 'OrderId', 'VersionId', 'EventType', 'Type', 'OrderFeedId', 'TimeInForce',
    'InitialTime', 'OrderTime', 'ExecutionTime', 'CurrencyPair', 'InstrumentCode', 'SecurityClassId',
    'AssetClassId', 'DealtCurrency', 'Price', 'Qty', 'LeavesQty', 'CumulativeQty', 'FillQty', 'FillPrice',
    'PartyId', 'SalesBookId', 'Side', 'Trader', 'IsParent', 'ParentId', 'IsAmended', 'AmendedTime',
    'IsCancelled', 'CancelledTime', 'IsMonitored', 'IsClientOrder', 'BaseCcyQty', 'ReceivedTime',
    'OrigCurrencyPair', 'OrigPrice', 'OrigSide', 'OrderFeedCounter', 'OrderAltId', 'OrigOrderId',
    'ClientOrderId', 'OrigClientOrderId', 'ExpireTime', 'MarketId', 'MaturityDate', 'StrikePrice', 'PutCall',
    'PartyType', 'Desk', 'Value', 'BaseCcyValue', 'OrderBookPartyId', 'OrderAttrib1', 'OrderAttrib2',
    'OrderAttrib3', 'OrderAttrib4', 'OrderAttrib5', 'OrderAttrib6', 'OrderAttrib7', 'OrderAttrib8',
    'Comments', 'DimPartyId', 'DimDeskId', 'DimTraderId', 'DimSecurityClassId', 'DimMarketId',
    'DimInstrumentId', 'DimDate', 'DimTimeOfDay', 'DimSalesBookId', 'Venue', 'IsCreated', 'OrigQty',
    'DeskDescription', 'SettlementRef', 'ExecutionStrategy', 'Owner', 'Modifier', 'DimModifierId',
    'DimOwnerId', 'OrigLeavesQty', 'LastFilledSize', 'LastFilledPrice', 'OrigExecAuthority', 'PortfolioId',
    'ExecutionId', 'ParValue', 'TradableItems', 'NumberOfTradableItems', 'QuoteType', 'SalesPerson',
    'EventSummary', 'ClientName', 'InternalCtpy', 'InstrumentRef1', 'InstrumentRef2', 'InstrumentQuoteType',
    'SettlementDate', 'Position', 'Region', 'FIorIRDFlag', 'ClientNucleusID', 'BankSide',
    'ProductDescription', 'StellarOrderStatus', 'StellarTransactionStatus', 'StellarTransactionType',
    'BaseCcyLeavesQty', 'IsSpreadOrder', 'LinkedOrder', 'OrdInstrumentType', 'OrdExecType', 'TrOrderStatus',
    'UnderlyingInstrumentCode', 'ComponentId', 'DimUnderlyingInstrumentId', 'CancelCategory', 'CFICode',
    'Origination', 'QtyNotation'
]

# Initialize session state
if 'parameters' not in st.session_state:
    st.session_state['parameters'] = {
        'Smoking': {'num_orders': 100, 'intensity': 0.5},
        'Spoofing': {'num_orders': 100, 'intensity': 0.5},
        'Wash Trade': {'num_orders': 100, 'intensity': 0.5}
    }

if 'rules' not in st.session_state:
    st.session_state['rules'] = []

# Helper functions
def generate_order_data(num_orders, intensity, scenario):
    orders = []
    for _ in range(num_orders):
        order = {
            'order_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200))),
            'venue': random.choice(['ABC', 'XYZ', 'DEF']),
            'side': random.choice(['Buy', 'Sell']),
            'price': round(random.uniform(90, 110), 2),
            'quantity': random.randint(1000, 1000000),
            'scenario': scenario,
            'behavior': random.random() < intensity
        }
        orders.append(order)
    return orders

def apply_rules(df, rules):
    for rule in rules:
        try:
            df[rule['name']] = df.eval(f"{rule['attribute']} {rule['condition']} {repr(rule['value'])}")
        except Exception as e:
            df[rule['name']] = f"Error: {e}"
    return df

# UI
st.title("📊 Market Abuse Scenario Simulator")

# Scenario Configuration
st.header("1. Configure Scenario Parameters")
scenario = st.selectbox("Select Scenario", list(st.session_state['parameters'].keys()))
params = st.session_state['parameters'][scenario]
params['num_orders'] = st.number_input("Number of Orders", min_value=1, value=params['num_orders'])
params['intensity'] = st.slider("Behavior Intensity", 0.0, 1.0, value=params['intensity'])

# Rule Management
st.header("2. Manage Validation Rules")
with st.form("add_rule_form"):
    rule_name = st.text_input("Rule Name")
    attribute = st.selectbox("Attribute", ATTRIBUTES)
    condition = st.selectbox("Condition", ["==", "!=", ">", "<", ">=", "<="])
    value = st.text_input("Value")
    if st.form_submit_button("Add Rule"):
        if rule_name and attribute and condition and value:
            st.session_state['rules'].append({
                'name': rule_name,
                'attribute': attribute,
                'condition': condition,
                'value': value
            })
            st.success(f"Added rule: {rule_name}")
        else:
            st.error("Please fill in all fields.")

# Display and Edit Rules
for i, rule in enumerate(st.session_state['rules']):
    with st.expander(f"Rule {i+1}: {rule['name']}"):
        st.write(f"**Attribute**: {rule['attribute']}")
        st.write(f"**Condition**: {rule['condition']}")
        st.write(f"**Value**: {rule['value']}")
        if st.button(f"Delete Rule {i+1}"):
            st.session_state['rules'].pop(i)
            st.experimental_rerun()

# Data Generation
st.header("3. Generate and Download Data")
if st.button("Generate Data"):
    orders = generate_order_data(params['num_orders'], params['intensity'], scenario)
    df = pd.DataFrame(orders)
    df = apply_rules(df, st.session_state['rules'])

    st.subheader("Generated Order Data")
    st.dataframe(df)

    csv = df.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name="order_data.csv", mime="text/csv")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    st.download_button("Download Excel", data=output.getvalue(), file_name="order_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
