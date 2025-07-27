import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import re

def validate_city_in_address(address, expected_city):
    """Check if the expected city appears in the geocoded address"""
    if not expected_city:
        return True
    return expected_city.lower() in address.lower()

def extract_city_from_input(address):
    """Try to extract the city from user input"""
    # Simple pattern to find city names after commas
    parts = [part.strip() for part in address.split(',')]
    if len(parts) > 1:
        return parts[-1].strip()
    return None

def show():
    st.title("🌍 Accurate Address Geocoding")
    st.write("Convert any worldwide address to precise coordinates with validation")
    
    # Address input with format guidance
    with st.expander("ℹ️ How to enter addresses (click to expand)"):
        st.markdown("""
        **For best results, please use this format:**  
        `[Street/Building], [Area], [City], [Country]`  

        **Examples:**
        - `Taj Mahal Road, Agra, Uttar Pradesh, India`  
        - `1600 Amphitheatre Parkway, Mountain View, CA, USA`  
        - `Mughal Pura Bus Stop, Lahore, Punjab, Pakistan`  
        - `Rue de Rivoli, 4th arrondissement, Paris, France`  
        """)

    address = st.text_input(
        "Enter complete address (include city and country)", 
        placeholder="E.g., 'Mughal Pura Bus Stop, Lahore, Pakistan'"
    )
    
    zoom_level = st.slider("Map zoom level", 1, 18, 15)
    enable_validation = st.checkbox("Enable city validation", value=True, 
                                  help="Warn if geocoded location doesn't match expected city")

    if st.button("📍 Geocode Address"):
        if address:
            with st.spinner("Locating address..."):
                try:
                    # Initialize geocoder
                    geolocator = Nominatim(
                        user_agent="accurate_geo_app",
                        timeout=15
                    )
                    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
                    
                    # Geocode with detailed parameters
                    location = geocode(
                        address,
                        exactly_one=True,
                        addressdetails=True,
                        language='en'
                    )
                    
                    if location:
                        # Extract expected city from input
                        expected_city = extract_city_from_input(address)
                        
                        # Validate location
                        if enable_validation and expected_city:
                            if not validate_city_in_address(location.address, expected_city):
                                st.warning(f"⚠️ The found location appears to be in a different city than expected ({expected_city}).")
                                st.warning("Found location: " + location.address)
                        
                        st.success("✅ Location Found")
                        
                        # Display core information
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Latitude", f"{location.latitude:.6f}°")
                            st.write(f"**Full Address:** {location.address}")
                        with col2:
                            st.metric("Longitude", f"{location.longitude:.6f}°")
                            if hasattr(location, 'raw'):
                                loc_type = location.raw.get('type', 'point')
                                st.write(f"**Location Type:** {loc_type}")
                        
                        # Create map
                        st.subheader("🗺️ Location Map")
                        m = folium.Map(
                            location=[location.latitude, location.longitude],
                            zoom_start=zoom_level,
                            tiles="OpenStreetMap"
                        )
                        
                        # Add detailed marker
                        folium.Marker(
                            [location.latitude, location.longitude],
                            popup=f"""
                            <b>Address:</b> {location.address}<br>
                            <b>Coordinates:</b> {location.latitude:.6f}, {location.longitude:.6f}<br>
                            <b>OSM Type:</b> {location.raw.get('type', 'N/A') if hasattr(location, 'raw') else 'N/A'}
                            """,
                            tooltip="Click for details",
                            icon=folium.Icon(color="blue", icon="map-marker")
                        ).add_to(m)
                        
                        # Add accuracy circle (100m radius)
                        folium.Circle(
                            location=[location.latitude, location.longitude],
                            radius=100,
                            color='#3186cc',
                            fill=True,
                            fill_color='#3186cc',
                            fill_opacity=0.2
                        ).add_to(m)
                        
                        folium_static(m, width=700, height=500)
                        
                        # Additional tools
                        st.subheader("📍 Location Tools")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.code(f"Decimal Degrees:\n{location.latitude:.6f}, {location.longitude:.6f}", language="text")
                        with col2:
                            st.code(f"Google Maps:\nhttps://maps.google.com/?q={location.latitude},{location.longitude}", language="text")
                            st.code(f"OpenStreetMap:\nhttps://www.openstreetmap.org/#map=18/{location.latitude}/{location.longitude}", language="text")
                        
                        # Raw data
                        with st.expander("📊 Technical Details"):
                            if hasattr(location, 'raw'):
                                st.json(location.raw)
                            else:
                                st.write("No raw data available")
                    
                    else:
                        st.error("❌ Address not found. Please:")
                        st.markdown("""
                        - Check for typos
                        - Add more specific details
                        - Include city and country
                        - Try alternative address formats
                        """)
                
                except GeocoderTimedOut:
                    st.error("⌛ Service timeout. Please try again in a moment.")
                except GeocoderServiceError:
                    st.error("🌐 Geocoding service unavailable. Please try later.")
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

        else:
            st.warning("Please enter an address to geocode")

    # Quality tips
    st.markdown("---")
    st.subheader("🔍 Tips for Better Results")
    st.markdown("""
    1. **Always include the city and country** in your address
    2. **Add specific landmarks** near your location
    3. **Use local address formats** when possible
    4. **Verify the map location** matches your expectations
    5. For businesses, **include the street address**
    """)

    # Attribution
    st.markdown("---")
    st.caption("""
    *Geocoding powered by [Nominatim](https://nominatim.openstreetmap.org/) (OpenStreetMap)*  
    *Accuracy depends on OpenStreetMap data coverage in your area*
    """)

if __name__ == "__main__":
    show()