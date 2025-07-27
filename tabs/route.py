import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import polyline
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic
import time
from datetime import timedelta

# Configuration
OSRM_URL = "http://router.project-osrm.org/route/v1"
GEOCODING_TIMEOUT = 10

def get_coordinates(address):
    """Enhanced global geocoding with retries"""
    geolocator = Nominatim(user_agent="global_route_planner")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    try:
        location = geocode(address, timeout=GEOCODING_TIMEOUT)
        if location:
            return {
                "lat": location.latitude,
                "lon": location.longitude,
                "address": location.address
            }
        return None
    except Exception as e:
        st.error(f"Geocoding error: {str(e)}")
        return None

def get_route(start_lat, start_lon, end_lat, end_lon, mode):
    """Get route with proper error handling and consistent data structure"""
    profiles = {
        "driving": "car",
        "walking": "foot",
        "bicycling": "bike"
    }
    
    try:
        response = requests.get(
            f"{OSRM_URL}/{profiles[mode]}/{start_lon},{start_lat};{end_lon},{end_lat}",
            params={'overview': 'full', 'steps': 'true'},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 'Ok' and data.get('routes'):
                route = data['routes'][0]
                return {
                    "geometry": route['geometry'],  # Polyline encoded string
                    "coordinates": polyline.decode(route['geometry']),  # Decoded coordinates
                    "distance": route['distance'],  # in meters
                    "duration": route['duration'],  # in seconds
                    "start_address": st.session_state.start_point.get("address", "Start Location"),
                    "end_address": st.session_state.end_point.get("address", "End Location"),
                    "travel_mode": mode.capitalize(),
                    "steps": data.get('waypoints', [{}])[0].get('steps', [])
                }
        st.error("Failed to get route from OSRM service")
        return None
    except Exception as e:
        st.error(f"Routing error: {str(e)}")
        return None

def format_duration(seconds):
    """Human-readable duration"""
    td = timedelta(seconds=seconds)
    if td.days > 0:
        return f"{td.days}d {td.seconds//3600}h"
    hours, remainder = divmod(td.seconds, 3600)
    minutes = remainder // 60
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def show():
    st.title("🌍 Persistent Route Planner")
    
    # Initialize session state
    if "start_point" not in st.session_state:
        st.session_state.start_point = None
    if "end_point" not in st.session_state:
        st.session_state.end_point = None
    if "route_data" not in st.session_state:
        st.session_state.route_data = None
    
    # Location selection
    st.subheader("1. Select Locations")
    col1, col2 = st.columns(2)
    with col1:
        start_address = st.text_input("Start Address", key="start_addr", value="mughalpura, Lahore, Pakistan")
        if st.button("Set Start Location"):
            if start_address:
                with st.spinner("Locating start point..."):
                    coords = get_coordinates(start_address)
                    if coords:
                        st.session_state.start_point = coords
                        st.session_state.route_data = None  # Clear previous route
                        st.success(f"Start location set to: {coords['address']}")
                    else:
                        st.error("Could not find start location")
    
    with col2:
        end_address = st.text_input("End Address", key="end_addr", value="Garden Town, Lahore, Pakistan")
        if st.button("Set End Location"):
            if end_address:
                with st.spinner("Locating end point..."):
                    coords = get_coordinates(end_address)
                    if coords:
                        st.session_state.end_point = coords
                        st.session_state.route_data = None  # Clear previous route
                        st.success(f"End location set to: {coords['address']}")
                    else:
                        st.error("Could not find end location")
    
    # Map display
    if st.session_state.start_point or st.session_state.end_point:
        map_center = [20, 0]
        zoom = 2
        
        if st.session_state.start_point and st.session_state.end_point:
            map_center = [
                (st.session_state.start_point["lat"] + st.session_state.end_point["lat"])/2,
                (st.session_state.start_point["lon"] + st.session_state.end_point["lon"])/2
            ]
            distance_km = geodesic(
                (st.session_state.start_point["lat"], st.session_state.start_point["lon"]),
                (st.session_state.end_point["lat"], st.session_state.end_point["lon"])
            ).km
            zoom = 12 if distance_km < 500 else 6
        
        m = folium.Map(location=map_center, zoom_start=zoom)
        
        if st.session_state.start_point:
            folium.Marker(
                [st.session_state.start_point["lat"], st.session_state.start_point["lon"]],
                popup="Start: " + st.session_state.start_point.get("address", ""),
                icon=folium.Icon(color="green")
            ).add_to(m)
        
        if st.session_state.end_point:
            folium.Marker(
                [st.session_state.end_point["lat"], st.session_state.end_point["lon"]],
                popup="End: " + st.session_state.end_point.get("address", ""),
                icon=folium.Icon(color="red")
            ).add_to(m)
        
        # Draw route if available
        if st.session_state.route_data and 'coordinates' in st.session_state.route_data:
            folium.PolyLine(
                st.session_state.route_data["coordinates"],
                color="blue",
                weight=5,
                opacity=0.7,
                tooltip=f"{st.session_state.route_data['distance']/1000:.1f} km"
            ).add_to(m)
        
        st_folium(m, width=800, height=500)
    
    # Route calculation
    if st.session_state.start_point and st.session_state.end_point:
        st.subheader("2. Calculate Route")
        travel_mode = st.selectbox(
            "Travel Mode",
            ["driving", "walking", "bicycling"],
            key="travel_mode"
        )
        
        if st.button("Calculate Route"):
            with st.spinner("Calculating best route..."):
                route = get_route(
                    st.session_state.start_point["lat"], st.session_state.start_point["lon"],
                    st.session_state.end_point["lat"], st.session_state.end_point["lon"],
                    travel_mode
                )
                if route:
                    st.session_state.route_data = route
                    st.success("Route calculated successfully!")
                else:
                    st.error("Failed to calculate route. Please try again.")
        
        # Persistent route display
        if st.session_state.route_data:
            st.subheader("Route Details")
            cols = st.columns(3)
            cols[0].metric("Start", st.session_state.route_data.get("start_address", "Start"))
            cols[1].metric("Distance", f"{st.session_state.route_data['distance']/1000:.1f} km")
            cols[2].metric("Duration", format_duration(st.session_state.route_data['duration']))
            
            if st.session_state.route_data.get('steps'):
                st.subheader("Turn-by-Turn Directions")
                for i, step in enumerate(st.session_state.route_data['steps'], 1):
                    st.markdown(f"{i}. {step['instruction']}")

if __name__ == "__main__":
    show()