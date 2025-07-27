import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import math
import random

def show():
    st.title("Points of Interest")
    st.write("Find nearby restaurants, hotels, attractions, and other POIs within a specified radius")
    
    col1, col2 = st.columns(2)
    
    with col1:
        address = st.text_input("Center Location Address", "Times Square, New York")
        radius = st.number_input("Search Radius (km)", min_value=0.1, max_value=50.0, value=1.0, step=0.1)
    
    with col2:
        poi_type = st.selectbox("POI Type", [
            "restaurant", "hotel", "attraction", 
            "museum", "park", "shopping_mall",
            "cafe", "bar", "landmark"
        ])
        max_results = st.number_input("Maximum Results", min_value=1, max_value=50, value=10)
    
    if st.button("Search POIs"):
        if address:
            try:
                # Geocode address
                geolocator = Nominatim(user_agent="poi_finder")
                location = geolocator.geocode(address)
                
                if location:
                    # Generate simulated POIs around the location
                    num_pois = min(max_results, 10)  # Limit to 10 for demo
                    pois = []
                    
                    for i in range(num_pois):
                        angle = random.uniform(0, 2 * 3.14159)
                        distance = random.uniform(0, radius/111.32)  # approx km to degrees
                        
                        lat = location.latitude + distance * math.cos(angle)
                        lon = location.longitude + distance * math.sin(angle)
                        
                        pois.append({
                            "name": f"{poi_type.capitalize()} {i+1}",
                            "latitude": lat,
                            "longitude": lon,
                            "type": poi_type,
                            "address": f"Simulated address for {poi_type} {i+1}",
                            "distance": math.sqrt((lat-location.latitude)**2 + (lon-location.longitude)**2) * 111.32
                        })
                    
                    # Sort by distance
                    pois.sort(key=lambda x: x['distance'])
                    
                    st.success(f"Found {len(pois)} {poi_type}s within {radius} km")
                    
                    # Display POIs on map
                    m = folium.Map(location=[location.latitude, location.longitude], zoom_start=14)
                    
                    # Add center marker
                    folium.Marker([location.latitude, location.longitude],
                                popup="Search Center",
                                tooltip="Center",
                                icon=folium.Icon(color="blue")).add_to(m)
                    
                    # Add POI markers
                    for poi in pois:
                        folium.Marker([poi['latitude'], poi['longitude']],
                                    popup=f"<b>{poi['name']}</b><br>{poi['address']}<br>Distance: {poi['distance']:.2f} km",
                                    tooltip=poi['name'],
                                    icon=folium.Icon(color="red")).add_to(m)
                    
                    # Add radius circle
                    folium.Circle([location.latitude, location.longitude],
                                radius=radius*1000,  # in meters
                                color="blue",
                                fill=True,
                                fill_opacity=0.2).add_to(m)
                    
                    folium_static(m, width=700, height=500)
                    
                    # Display POI list
                    st.subheader(f"Nearby {poi_type.capitalize()}s")
                    for poi in pois:
                        with st.expander(f"{poi['name']} - {poi['distance']:.2f} km away"):
                            st.write(f"**Address:** {poi['address']}")
                            st.write(f"**Coordinates:** {poi['latitude']:.6f}, {poi['longitude']:.6f}")
                else:
                    st.error("Could not geocode the provided address. Please try a more specific address.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter an address to search around")