import streamlit as st
import requests

st.set_page_config(page_title="TashBot", layout="wide")
st.title("🤖 TashBot – Polymarket Live Feed")

st.markdown("Obteniendo los mercados más recientes de [Polymarket](https://polymarket.com) en tiempo real...")

# Llamada a la API de Polymarket
url = "https://api.polymarket.com/v3/markets"
try:
    response = requests.get(url)
    data = response.json()
    markets = data.get("markets", [])

    if not markets:
        st.warning("No se encontraron mercados.")

    for market in markets[:10]:  # Mostramos solo los 10 primeros para que cargue rápido
        st.subheader(market["title"])
        st.write(f"📅 Cierra: {market['endDate']}")
        st.write(f"💰 Volumen: ${market['volumeUSD']:,}")
        st.write("Opciones:")
        for outcome in market.get("outcomes", []):
            st.write(f"- {outcome['name']}: {float(outcome['price']['yes'])*100:.2f}%")

except Exception as e:
    st.error("Ocurrió un error al conectar con la API de Polymarket.")
    st.code(str(e))
