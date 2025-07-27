import streamlit as st
import folium
from streamlit_folium import folium_static
from math import radians, sin, cos, sqrt, atan2

def show():
    st.title("Distance Calculator")
    st.write("Calculate the straight-line distance between two coordinates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Point A")
        lat_a = st.number_input("Latitude A", value=37.7749, format="%.6f")
        lon_a = st.number_input("Longitude A", value=-122.4194, format="%.6f")
    
    with col2:
        st.subheader("Point B")
        lat_b = st.number_input("Latitude B", value=34.0522, format="%.6f")
        lon_b = st.number_input("Longitude B", value=-118.2437, format="%.6f")
    
    if st.button("Calculate Distance"):
        # Haversine formula for distance calculation
        R = 6371.0  # Earth radius in km
        
        lat1, lon1 = radians(lat_a), radians(lon_a)
        lat2, lon2 = radians(lat_b), radians(lon_b)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        
        st.success(f"Distance between points: {distance:.2f} km")
        
        # Display both points on map
        m = folium.Map(location=[(lat_a + lat_b)/2, (lon_a + lon_b)/2], zoom_start=6)
        folium.Marker([lat_a, lon_a], popup="Point A", tooltip="Point A").add_to(m)
        folium.Marker([lat_b, lon_b], popup="Point B", tooltip="Point B").add_to(m)
        
        # Add line between points
        folium.PolyLine([(lat_a, lon_a), (lat_b, lon_b)], color="red", weight=2.5, opacity=1).add_to(m)
        
        folium_static(m, width=700, height=400)