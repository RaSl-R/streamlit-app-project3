import streamlit as st
import psycopg2
import pandas as pd
import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
import os

# Připojovací údaje (lze později nahradit načítáním z .env)
DB_USER = "neondb_owner"
DB_PASSWORD = "npg_bqIR6D2UkALc"
DB_HOST = "ep-icy-moon-a2bfjmyb-pooler.eu-central-1.aws.neon.tech"
DB_NAME = "neondb"

@st.cache_resource
def get_connection():
    conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(conn_str, connect_args={"sslmode": "require"})
    return engine.connect()

@st.cache_data
def list_schemas(_conn):
    result = _conn.execute(text("SELECT schema_name FROM information_schema.schemata"))
    return [row[0] for row in result]

def load_data():
    return pd.read_sql("SELECT * FROM watchlist ORDER BY id", conn)

st.title("📈 Můj Watchlist")

df = load_data()
st.dataframe(df)

with st.form("add_stock"):
    name = st.text_input("Název")
    symbol = st.text_input("Ticker")
    url = st.text_input("Odkaz TradingView")
    limit_buy = st.number_input("Limit Buy", step=0.01)
    limit_sell = st.number_input("Limit Sell", step=0.01)
    note = st.text_area("Poznámka")
    submitted = st.form_submit_button("Přidat")
    if submitted:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO watchlist (name, symbol, source_url, limit_buy, limit_sell, note) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, symbol, url, limit_buy, limit_sell, note)
            )
            conn.commit()
        st.success("Akcie přidána ✅")
