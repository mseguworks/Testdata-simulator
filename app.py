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
            'SeqNum': random.randint(100000000, 999999999),
            'OrderDetailsId': random.randint(100000000, 999999999),
            'OrderId': random.randint(100000000, 999999999),
            'VersionId': None,
            'EventType': random.choice(['AMEND', 'PARTIALLY_FILLED']),
            'Type': random.choice(['LIMIT', 'MARKET']),
            'OrderFeedId': random.choice(['Stellar', 'Fenics']),
            'TimeInForce': random.choice(['IOC', 'GTC']),
            'InitialTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200))),
            'OrderTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200))),
            'ExecutionTime': None,
            'CurrencyPair': None,
            'InstrumentCode': 'US91282CMS79',
            'SecurityClassId': 'Bond',
            'AssetClassId': 'FI',
            'DealtCurrency': random.choice(['USD', 'GBP']),
            'Price': round(random.uniform(90, 110), 2),
            'Qty': random.uniform(1000000, 20000000),
            'LeavesQty': random.uniform(0, 20000000),
            'CumulativeQty': random.uniform(0, 20000000),
            'FillQty': random.uniform(0, 20000000),
            'FillPrice': round(random.uniform(90, 110), 2),
            'PartyId': None,
            'SalesBookId': None,
            'Side': random.choice(['Buy', 'Sell']),
            'Trader': random.randint(100000, 999999),
            'IsParent': random.choice(['Y', 'N']),
            'ParentId': None,
            'IsAmended': random.choice(['Y', 'N']),
            'AmendedTime': None,
            'IsCancelled': random.choice(['Y', 'N']),
            'CancelledTime': None,
            'IsMonitored': random.choice(['Y', 'N']),
            'IsClientOrder': random.choice(['Y', 'N']),
            'BaseCcyQty': random.uniform(1000000, 20000000),
            'ReceivedTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(random.randint(1609459200, 1640995200))),
            'OrigCurrencyPair': None,
            'OrigPrice': 0.0,
            'OrigSide': None,
            'OrderFeedCounter': None,
            'OrderAltId': None,
            'OrigOrderId': None,
            'ClientOrderId': None,
            'OrigClientOrderId': None,
            'ExpireTime': None,
            'MarketId': None,
            'MaturityDate': None,
            'StrikePrice': None,
            'PutCall': None,
            'PartyType': None,
            'Desk': random.choice(['GETCO', 'LESTREAM']),
            'Value': random.uniform(1000000, 20000000),
            'BaseCcyValue': random.uniform(1000000, 20000000),
            'OrderBookPartyId': None,
            'OrderAttrib1': None,
            'OrderAttrib2': None,
            'OrderAttrib3': None,
            'OrderAttrib4': None,
            'OrderAttrib5': None,
            'OrderAttrib6': None,
            'OrderAttrib7': None,
            'OrderAttrib8': None,
            'Comments': None,
            'DimPartyId': None,
            'DimDeskId': None,
            'DimTraderId': None,
            'DimSecurityClassId': None,
            'DimMarketId': None,
            'DimInstrumentId': None,
            'DimDate': None,
            'DimTimeOfDay': None,
            'DimSalesBookId': None,
            'Venue': random.choice(['ABC', 'XYZ', 'DEF']),
            'IsCreated': random.choice(['Y', 'N']),
            'OrigQty': random.uniform(1000000, 20000000),
            'DeskDescription': None,
            'SettlementRef': None,
            'ExecutionStrategy': None,
            'Owner': None,
            'Modifier': None,
            'DimModifierId': None,
            'DimOwnerId': None,
            'OrigLeavesQty': random.uniform(1000000, 20000000),
            'LastFilledSize': random.uniform(1000000, 20000000),
            'LastFilledPrice': round(random.uniform(90, 110), 2),
            'OrigExecAuthority': None,
            'PortfolioId': None,
            'ExecutionId': None,
            'ParValue': None,
            'TradableItems': None,
            'NumberOfTradableItems': None,
            'QuoteType': None,
            'SalesPerson': None,
            'EventSummary': None,
            'ClientName': None,
            'InternalCtpy': None,
            'InstrumentRef1': None,
            'InstrumentRef2': None,
            'InstrumentQuoteType': None,
            'SettlementDate': None,
            'Position': None,
            'Region': None,
            'FIorIRDFlag': None,
            'ClientNucleusID': None,
            'BankSide': None,
            'ProductDescription': None,
            'StellarOrderStatus': 'CONFIRMED',
            'StellarTransactionStatus': 'CONFIRMED',
            'StellarTransactionType': random.choice(['AMEND_ORDER', 'EXCHANGE_ORDER_FILL']),
            'BaseCcyLeavesQty': random.uniform(1000000, 20000000),
            'IsSpreadOrder': random.choice(['Y', 'N']),
            'LinkedOrder': None,
            'OrdInstrumentType': None,
            'OrdExecType': None,
            'TrOrderStatus': None,
            'UnderlyingInstrumentCode': None,
            'ComponentId': None,
            'DimUnderlyingInstrumentId': None,
            'CancelCategory': None,
            'CFICode': None,
            'Origination': None,
            'QtyNotation': None
        }
        orders.append(order)
    return orders

def apply_rules(df, rules):
    for rule in rules:
        try:
            if rule['type'] == 'simple':
                df[rule['name']] = df.eval(f"{rule['attribute']} {rule['condition']} {repr(rule['value'])}")
            elif rule['type'] == 'compound':
                conditions = [f"{r['attribute']} {r['condition']} {repr(r['value'])}" for r in rule['conditions']]
                df[rule['name']] = df.eval(f" {' ' + rule['logic'] + ' '}.join(conditions) ")
            elif rule['type'] == 'conditional':
                if_conditions = [f"{r['attribute']} {r['condition']} {repr(r['value'])}" for r in rule['if_conditions']]
                then_conditions = [f"{r['attribute']} {r['condition']} {repr(r['value'])}" for r in rule['then_conditions']]
                df[rule['name']] = df.eval(f"({' and '.join(if_conditions)}) and ({' and '.join(then_conditions)})")
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
rule_type = st.selectbox("Rule Type", ["Simple Rule", "Compound Rule (AND/OR)", "Conditional Rule (IF/THEN)"])

if rule_type == "Simple Rule":
    with st.form("add_simple_rule_form"):
        rule_name = st.text_input("Rule Name")
        attribute = st.selectbox("Attribute", ATTRIBUTES)
        condition = st.selectbox("Condition", ["==", "!=", ">", "<", ">=", "<="])
        value = st.text_input("Value")
        if st.form_submit_button("Add Rule"):
            if rule_name and attribute and condition and value:
                st.session_state['rules'].append({
                    'type': 'simple',
                    'name': rule_name,
                    'attribute': attribute,
                    'condition': condition,
                    'value': value
                })
                st.success(f"Added rule: {rule_name}")
            else:
                st.error("Please fill in all fields.")

elif rule_type == "Compound Rule (AND/OR)":
    with st.form("add_compound_rule_form"):
        rule_name = st.text_input("Rule Name")
        logic = st.selectbox("Logic", ["AND", "OR"])
        conditions = []
        for i in range(3):  # Allow up to 3 conditions for simplicity
            attribute = st.selectbox(f"Attribute {i+1}", ATTRIBUTES)
            condition = st.selectbox(f"Condition {i+1}", ["==", "!=", ">", "<", ">=", "<="])
            value = st.text_input(f"Value {i+1}")
            conditions.append({'attribute': attribute, 'condition': condition, 'value': value})
        if st.form_submit_button("Add Rule"):
            if rule_name and all(c['attribute'] and c['condition'] and c['value'] for c in conditions):
                st.session_state['rules'].append({
                    'type': 'compound',
                    'name': rule_name,
                    'logic': logic,
                    'conditions': conditions
                })
                st.success(f"Added rule: {rule_name}")
            else:
                st.error("Please fill in all fields.")

elif rule_type == "Conditional Rule (IF/THEN)":
    with st.form("add_conditional_rule_form"):
        rule_name = st.text_input("Rule Name")
        if_conditions = []
        then_conditions = []
        for i in range(3):  # Allow up to 3 IF conditions for simplicity
            attribute = st.selectbox(f"IF Attribute {i+1}", ATTRIBUTES)
            condition = st.selectbox(f"IF Condition {i+1}", ["==", "!=", ">", "<", ">=", "<="])
            value = st.text_input(f"IF Value {i+1}")
            if_conditions.append({'attribute': attribute, 'condition': condition, 'value': value})
        for i in range(3):  # Allow up to 3 THEN conditions for simplicity
            attribute = st.selectbox(f"THEN Attribute {i+1}", ATTRIBUTES)
            condition = st.selectbox(f"THEN Condition {i+1}", ["==", "!=", ">", "<", ">=", "<="])
            value = st.text_input(f"THEN Value {i+1}")
            then_conditions.append({'attribute': attribute, 'condition': condition, 'value': value})
        time_window = st.number_input("Time Window (seconds)", min_value=0, value=45)
        if st.form_submit_button("Add Rule"):
            if rule_name and all(c['attribute'] and c['condition'] and c['value'] for c in if_conditions) and all(c['attribute'] and c['condition'] and c['value'] for c in then_conditions):
                st.session_state['rules'].append({
                    'type': 'conditional',
                    'name': rule_name,
                    'if_conditions': if_conditions,
                    'then_conditions': then_conditions,
                    'time_window': time_window
                })
                st.success(f"Added rule: {rule_name}")
            else:
                st.error("Please fill in all fields.")

# Display and Edit Rules
for i, rule in enumerate(st.session_state['rules']):
    with st.expander(f"Rule {i+1}: {rule['name']}"):
        st.write(f"**Type**: {rule['type']}")
        if rule['type'] == 'simple':
            st.write(f"**Attribute**: {rule['attribute']}")
            st.write(f"**Condition**: {rule['condition']}")
            st.write(f"**Value**: {rule['value']}")
        elif rule['type'] == 'compound':
            st.write(f"**Logic**: {rule['logic']}")
            for j, cond in enumerate(rule['conditions']):
                st.write(f"**Condition {j+1}**: {cond['attribute']} {cond['condition']} {cond['value']}")
        elif rule['type'] == 'conditional':
            st.write(f"**IF Conditions**:")
            for j, cond in enumerate(rule['if_conditions']):
                st.write(f"**IF Condition {j+1}**: {cond['attribute']} {cond['condition']} {cond['value']}")
            st.write(f"**THEN Conditions**:")
            for j, cond in enumerate(rule['then_conditions']):
                st.write(f"**THEN Condition {j+1}**: {cond['attribute']} {cond['condition']} {cond['value']}")
            st.write(f"**Time Window**: {rule['time_window']} seconds")
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

    # Visual Summary
    st.subheader("Rule Summary")
    rule_summary = df[st.session_state['rules'][0]['name']].value_counts()
    st.bar_chart(rule_summary)


