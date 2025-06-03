import streamlit as st
import pandas as pd
import random
import string
import time

# Initialize session state for parameters and rules
if 'parameters' not in st.session_state:
    st.session_state['parameters'] = {
        'Smoking': {'num_orders': 100, 'intensity': 0.5},
        'Spoofing': {'num_orders': 100, 'intensity': 0.5},
        'Wash Trade': {'num_orders': 100, 'intensity': 0.5}
    }

if 'rules' not in st.session_state:
    st.session_state['rules'] = []

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

# Section to add new validation rules
st.header("Add New Validation Rule")

rule_name = st.text_input("Rule Name")
attribute = st.selectbox("Select Attribute", [
    'SeqNum', 'OrderDetailsId', 'OrderId', 'VersionId', 'EventType', 'Type', 'OrderFeedId', 'TimeInForce', 'InitialTime', 'OrderTime', 'ExecutionTime', 'CurrencyPair', 'InstrumentCode', 'SecurityClassId', 'AssetClassId', 'DealtCurrency', 'Price', 'Qty', 'LeavesQty', 'CumulativeQty', 'FillQty', 'FillPrice', 'PartyId', 'SalesBookId', 'Side', 'Trader', 'IsParent', 'ParentId', 'IsAmended', 'AmendedTime', 'IsCancelled', 'CancelledTime', 'IsMonitored', 'IsClientOrder', 'BaseCcyQty', 'ReceivedTime', 'OrigCurrencyPair', 'OrigPrice', 'OrigSide', 'OrderFeedCounter', 'OrderAltId', 'OrigOrderId', 'ClientOrderId', 'OrigClientOrderId', 'ExpireTime', 'MarketId', 'MaturityDate', 'StrikePrice', 'PutCall', 'PartyType', 'Desk', 'Value', 'BaseCcyValue', 'OrderBookPartyId', 'OrderAttrib1', 'OrderAttrib2', 'OrderAttrib3', 'OrderAttrib4', 'OrderAttrib5', 'OrderAttrib6', 'OrderAttrib7', 'OrderAttrib8', 'Comments', 'DimPartyId', 'DimDeskId', 'DimTraderId', 'DimSecurityClassId', 'DimMarketId', 'DimInstrumentId', 'DimDate', 'DimTimeOfDay', 'DimSalesBookId', 'Venue', 'IsCreated', 'OrigQty', 'DeskDescription', 'SettlementRef', 'ExecutionStrategy', 'Owner', 'Modifier', 'DimModifierId', 'DimOwnerId', 'OrigLeavesQty', 'LastFilledSize', 'LastFilledPrice', 'OrigExecAuthority', 'PortfolioId', 'ExecutionId', 'ParValue', 'TradableItems', 'NumberOfTradableItems', 'QuoteType', 'SalesPerson', 'EventSummary', 'ClientName', 'InternalCtpy', 'InstrumentRef1', 'InstrumentRef2', 'InstrumentQuoteType', 'SettlementDate', 'Position', 'Region', 'FIorIRDFlag', 'ClientNucleusID', 'BankSide', 'ProductDescription', 'StellarOrderStatus', 'StellarTransactionStatus', 'StellarTransactionType', 'BaseCcyLeavesQty', 'IsSpreadOrder', 'LinkedOrder', 'OrdInstrumentType', 'OrdExecType', 'TrOrderStatus', 'UnderlyingInstrumentCode', 'ComponentId', 'DimUnderlyingInstrumentId', 'CancelCategory', 'CFICode', 'Origination', 'QtyNotation'
])
condition = st.selectbox("Select Condition", ["==", "!=", ">", "<", ">=", "<="])
value = st.text_input("Value")

if st.button("Add Rule"):
    if rule_name and attribute and condition and value:
        st.session_state['rules'].append({
            'name': rule_name,
            'attribute': attribute,
            'condition': condition,
            'value': value
        })
        st.success(f"Added rule: {rule_name} - {attribute} {condition} {value}")
    else:
        st.error("Please enter all fields for the rule.")

# Section to view and edit validation rules
st.header("Validation Rules")

for i, rule in enumerate(st.session_state['rules']):
    st.subheader(f"Rule {i+1}: {rule['name']}")
    st.write(f"Attribute: {rule['attribute']}")
    st.write(f"Condition: {rule['condition']}")
    st.write(f"Value: {rule['value']}")
    
    if st.button(f"Delete Rule {i+1}"):
        st.session_state['rules'].pop(i)
        st.experimental_rerun()
    
    new_name = st.text_input(f"Edit Name for Rule {i+1}", value=rule['name'])
    new_attribute = st.selectbox(f"Edit Attribute for Rule {i+1}", [
        'SeqNum', 'OrderDetailsId', 'OrderId', 'VersionId', 'EventType', 'Type', 'OrderFeedId', 'TimeInForce', 'InitialTime', 'OrderTime', 'ExecutionTime', 'CurrencyPair', 'InstrumentCode', 'SecurityClassId', 'AssetClassId', 'DealtCurrency', 'Price', 'Qty', 'LeavesQty', 'CumulativeQty', 'FillQty', 'FillPrice', 'PartyId', 'SalesBookId', 'Side', 'Trader', 'IsParent', 'ParentId', 'IsAmended', 'AmendedTime', 'IsCancelled', 'CancelledTime', 'IsMonitored', 'IsClientOrder', 'BaseCcyQty', 'ReceivedTime', 'OrigCurrencyPair', 'OrigPrice', 'OrigSide', 'OrderFeedCounter', 'OrderAltId', 'OrigOrderId', 'ClientOrderId', 'OrigClientOrderId', 'ExpireTime', 'MarketId', 'MaturityDate', 'StrikePrice', 'PutCall', 'PartyType', 'Desk', 'Value', 'BaseCcyValue', 'OrderBookPartyId', 'OrderAttrib1', 'OrderAttrib2', 'OrderAttrib3', 'OrderAttrib4', 'OrderAttrib5', 'OrderAttrib6', 'OrderAttrib7', 'OrderAttrib8', 'Comments', 'DimPartyId', 'DimDeskId', 'DimTraderId', 'DimSecurityClassId', 'DimMarketId', 'DimInstrumentId', 'DimDate', 'DimTimeOfDay', 'DimSalesBookId', 'Venue', 'IsCreated', 'OrigQty', 'DeskDescription', 'SettlementRef', 'ExecutionStrategy', 'Owner', 'Modifier', 'DimModifierId', 'DimOwnerId', 'OrigLeavesQty', 'LastFilledSize', 'LastFilledPrice', 'OrigExecAuthority', 'PortfolioId', 'ExecutionId', 'ParValue', 'TradableItems', 'NumberOfTradableItems', 'QuoteType', 'SalesPerson', 'EventSummary', 'ClientName', 'InternalCtpy', 'InstrumentRef1', 'InstrumentRef2', 'InstrumentQuoteType', 'SettlementDate', 'Position', 'Region', 'FIorIRDFlag', 'ClientNucleusID', 'BankSide', 'ProductDescription', 'StellarOrderStatus', 'StellarTransactionStatus', 'StellarTransactionType', 'BaseCcyLeavesQty', 'IsSpreadOrder', 'LinkedOrder', 'OrdInstrumentType', 'OrdExecType', 'TrOrderStatus', 'UnderlyingInstrumentCode', 'ComponentId', 'DimUnderlyingInstrumentId', 'CancelCategory', 'CFICode', 'Origination', 'QtyNotation'
    ], index=[
        'SeqNum', 'OrderDetailsId', 'OrderId', 'VersionId', 'EventType', 'Type', 'OrderFeedId', 'TimeInForce', 'InitialTime', 'OrderTime', 'ExecutionTime', 'CurrencyPair', 'InstrumentCode', 'SecurityClassId', 'AssetClassId', 'DealtCurrency', 'Price', 'Qty', 'LeavesQty', 'CumulativeQty', 'FillQty', 'FillPrice', 'PartyId', 'SalesBookId', 'Side', 'Trader', 'IsParent', 'ParentId', 'IsAmended', 'AmendedTime', 'IsCancelled', 'CancelledTime', 'IsMonitored', 'IsClientOrder', 'BaseCcyQty', 'ReceivedTime', 'OrigCurrencyPair', 'OrigPrice', 'OrigSide', 'OrderFeedCounter', 'OrderAltId', 'OrigOrderId', 'ClientOrderId', 'OrigClientOrderId', 'ExpireTime', 'MarketId', 'MaturityDate', 'StrikePrice', 'PutCall', 'PartyType', 'Desk', 'Value', 'BaseCcyValue', 'OrderBookPartyId', 'OrderAttrib1', 'OrderAttrib2', 'OrderAttrib3', 'OrderAttrib4', 'OrderAttrib5', 'OrderAttrib6', 'OrderAttrib7', 'OrderAttrib8', 'Comments', 'DimPartyId', 'DimDeskId', 'DimTraderId', 'DimSecurityClassId', 'DimMarketId', 'DimInstrumentId', 'DimDate', 'DimTimeOfDay', 'DimSalesBookId', 'Venue', 'IsCreated', 'OrigQty', 'DeskDescription', 'SettlementRef', 'ExecutionStrategy', 'Owner', 'Modifier', 'DimModifierId', 'DimOwnerId', 'OrigLeavesQty', 'LastFilledSize', 'LastFilledPrice', 'OrigExecAuthority', 'PortfolioId', 'ExecutionId', 'ParValue', 'TradableItems', 'NumberOfTradableItems', 'QuoteType', 'SalesPerson', 'EventSummary', 'ClientName', 'InternalCtpy', 'InstrumentRef1', 'InstrumentRef2', 'InstrumentQuoteType', 'SettlementDate', 'Position', 'Region', 'FIorIRDFlag', 'ClientNucleusID', 'BankSide', 'ProductDescription', 'StellarOrderStatus', 'StellarTransactionStatus', 'StellarTransactionType', 'BaseCcyLeavesQty', 'IsSpreadOrder', 'LinkedOrder', 'OrdInstrumentType', 'OrdExecType', 'TrOrderStatus', 'UnderlyingInstrumentCode', 'ComponentId', 'DimUnderlyingInstrumentId', 'CancelCategory', 'CFICode', 'Origination', 'QtyNotation'
    ].index(rule['attribute']))
    new_condition = st.selectbox(f"Edit Condition for Rule {i+1}", ["==", "!=", ">", "<", ">=", "<="], index=["==", "!=", ">", "<", ">=", "<="].index(rule['condition']))
    new_value = st.text_input(f"Edit Value for Rule {i+1}", value=rule['value'])
    
    if st.button(f"Update Rule {i+1}"):
        st.session_state['rules'][i] = {
            'name': new_name,
            'attribute': new_attribute,
            'condition': new_condition,
            'value': new_value
        }
        st.success(f"Updated rule: {new_name} - {new_attribute} {new_condition} {new_value}")

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

