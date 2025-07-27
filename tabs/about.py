
import streamlit as st

def show():
    st.title("🌍 GeoAI Toolkit")
    st.markdown("""
    *Your AI-Powered Geographic Calculation Server*  
    *Version 2.0 | Powered by OpenStreetMap & OSRM*
    """)
    
    st.image("https://i.imgur.com/JbMk7Xr.png", width=300)  # Replace with your logo
    
    st.header("🚀 Overview")
    st.write("""
    The **GeoAI Toolkit** is a specialized geographic computation server designed for:
    - **AI Models** (LLMs, agents, and automation workflows)  
    - **Developers** needing precise spatial calculations  
    - **Researchers** analyzing location-based data  
    """)
    
    with st.expander("✨ Key Features", expanded=True):
        st.markdown("""
        | Feature | Description |
        |---|---|
        | **📍 Smart Geocoding** | Convert addresses ↔ coordinates with AI-assisted validation |
        | **📏 Multi-Mode Distance** | Calculate straight-line or route-based distances (driving/walking/biking) |
        | **🗺️ Route Intelligence** | Get turn-by-turn navigation, travel times, and optimized paths |
        | **🏢 POI Finder** | Discover nearby points of interest with simulated real-world data |
        | **🛠️ API-Ready** | Designed for seamless integration with AI workflows |
        """)
    
    st.header("🧩 How It Works")
    st.markdown("""
    1. **Input** → Addresses, coordinates, or route parameters  
    2. **Process** → Server handles complex geographic computations  
    3. **Output** → Structured data perfect for AI consumption  
    """)
    
    st.warning("""
    ⚠️ **Note for AI Models:**  
    This server provides *raw geographic data* – you may need to post-process results for natural language responses.
    """)
    
    st.header("🔗 Sample Workflow for AI Models")
    st.markdown("""
    ```python
    # Example pseudocode for an AI agent
    1. Geocode("Eiffel Tower, Paris") → (48.8584, 2.2945)
    2. CalculateRoute(start, end, mode="walking") → {distance, duration, steps}
    3. ExtractTime(duration) → "15 minutes"
    4. GenerateMap() → visual_route.png
    ```
    """)
    
    st.header("📜 Data Sources & Attribution")
    st.markdown("""
    - Geocoding: [Nominatim (OpenStreetMap)](https://nominatim.org/)  
    - Routing: [OSRM](http://project-osrm.org/)  
    - Maps: [Leaflet/OpenStreetMap](https://leafletjs.com/)  
    """)
    
    st.caption("""
    *This tool is designed for technical users and AI systems.  
    Accuracy depends on OpenStreetMap's coverage in your region.*
    """)
