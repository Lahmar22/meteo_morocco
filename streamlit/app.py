import streamlit as st
import psycopg2

st.title("Weather Dashboard")

try:
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="weather",
        user="admin",
        password="admin"
    )

    st.success("Connexion PostgreSQL réussie !")

    cursor = conn.cursor()
    cursor.execute("SELECT version();")

    version = cursor.fetchone()[0]

    st.write("PostgreSQL version :")
    st.code(version)

    cursor.close()
    conn.close()

except Exception as e:
    st.error(f"Erreur PostgreSQL : {e}")