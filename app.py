import streamlit as st
import requests

st.set_page_config(page_title="TashBot", layout="wide")
st.title("📊 TashBot – Polymarket Live Feed")
st.markdown("Fetching the latest markets from [Polymarket](https://polymarket.com) using GraphQL...")

# GraphQL query
query = """
{
  markets(first: 10, orderBy: volumeUSD, orderDirection: desc) {
    id
    title
    endDate
    volumeUSD
    outcomes {
      name
      price {
        yes
      }
    }
  }
}
"""

try:
    response = requests.post(
        "https://api.polymarket.com/graphql",
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()
    markets = data.get("data", {}).get("markets", [])

    if not markets:
        st.warning("No markets found.")

    for market in markets:
        st.subheader(market["title"])
        st.write(f"📅 Ends: {market['endDate']}")
        st.write(f"💰 Volume: ${market['volumeUSD']:,.2f}")
        st.write("Outcomes:")
        for outcome in market.get("outcomes", []):
            price = float(outcome["price"]["yes"]) * 100
            st.write(f"– {outcome['name']}: {price:.2f}%")

except Exception as e:
    st.error("An error occurred while connecting to the Polymarket GraphQL API.")
    st.code(str(e))
