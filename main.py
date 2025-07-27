import streamlit as st
from tabs import about, extract_distance, extract_time, geocoding, distance, route, route_map, poi

# Set page config
st.set_page_config(page_title="🌍 GeoAI Toolkit", layout="wide")

# Sidebar with app info
with st.sidebar:
    st.title("🌍 GeoAI Toolkit")
    st.write("Geographic calculation tools for AI models")
    st.write("---")
    st.write("**Navigation**")
    st.write("Select a tool from the tabs above")
    st.write("---")
    st.write("**About**")
    st.write("This server provides geographic calculation tools including geocoding, distance calculation, route planning, and points of interest search.")

# Create tabs
tabs = {
    "About": about,
    "Address Geocoding": geocoding,
    "Distance Calculator": distance,
    "Route Planner": route,
    "Extract Time": extract_time,
    "Extract Distance": extract_distance,
    "Route Map": route_map,
    "Points of Interest": poi
}


# Display radio buttons for navigation
current_tab = st.radio("Select Tool", list(tabs.keys()), horizontal=True)

# Display the selected tab
tabs[current_tab].show()