import streamlit as st
import folium
from streamlit_folium import folium_static
import polyline
from datetime import datetime
from branca.element import Element, MacroElement
from jinja2 import Template

class TitleElement(MacroElement):
    def __init__(self, title_text):
        super().__init__()
        self._name = 'title_element'
        self.title_text = title_text

    def render(self, **kwargs):
        template = Template("""
            <div style="
                position: fixed; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%); 
                z-index: 1000; 
                background-color: white; 
                padding: 5px 15px; 
                border-radius: 5px; 
                box-shadow: 0 0 5px rgba(0,0,0,0.3);
                font-size: 16px;
                font-weight: bold;
            ">
                {{ title }}
            </div>
        """)
        element = Element(template.render(title=self.title_text))
        element._parent = self._parent
        element.render(**kwargs)

def show():
    st.title("Route Map")
    st.write("Generate a map visualization of the route with optional title overlay")
    
    # Check if route data exists and is valid
    if 'route_data' not in st.session_state:
        st.error("🚫 No route data found in session. Please calculate a route first.")
        st.info("Go to the 'Route Planner' tab to create a route")
        return
    
    route_data = st.session_state.route_data
    
    if not route_data or not isinstance(route_data, dict):
        st.error("⚠️ Invalid route data format. Please recalculate your route.")
        return
    
    # Validate required fields
    required_fields = ['geometry', 'distance', 'duration', 'start_address', 'end_address']
    missing_fields = [field for field in required_fields if field not in route_data]
    
    if missing_fields:
        st.error(f"❌ Missing required route data: {', '.join(missing_fields)}")
        st.warning("Please recalculate your route using the Route Planner")
        return
    
    try:
        # Decode the polyline route geometry
        route_points = polyline.decode(route_data['geometry'])
        
        if not route_points or len(route_points) < 2:
            st.error("Invalid route geometry - not enough points to draw")
            return
            
        # Optional title
        map_title = st.text_input("Map Title (optional)", 
                                value=f"{route_data['travel_mode']} Route: {route_data['start_address']} to {route_data['end_address']}")
        
        # Calculate map center and zoom level
        lats = [p[0] for p in route_points]
        lons = [p[1] for p in route_points]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        # Create the map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        
        # Add the route line
        folium.PolyLine(
            route_points,
            color='#1E90FF',  # DodgerBlue
            weight=6,
            opacity=0.8,
            tooltip=f"{route_data['distance']/1000:.1f} km, {format_duration(route_data['duration'])}"
        ).add_to(m)
        
        # Add markers with custom icons
        folium.Marker(
            route_points[0],
            popup=f"<b>Start</b><br>{route_data['start_address']}",
            tooltip="Start",
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m)
        
        folium.Marker(
            route_points[-1],
            popup=f"<b>End</b><br>{route_data['end_address']}",
            tooltip="End",
            icon=folium.Icon(color='red', icon='flag-checkered', prefix='fa')
        ).add_to(m)
        
        # Add title if specified
        if map_title:
            title_element = TitleElement(map_title)
            m.get_root().add_child(title_element)
        
        # Display the map
        folium_static(m, width=800, height=600)
        
        # Add download button
        if st.button("💾 Save Map as HTML"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"route_map_{timestamp}.html"
            m.save(filename)
            st.success(f"Map saved as {filename}")
            st.download_button(
                label="⬇️ Download Map",
                data=open(filename, 'rb').read(),
                file_name=filename,
                mime='text/html'
            )
            
    except polyline.DecodeError:
        st.error("Failed to decode route geometry. Invalid polyline data.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

def format_duration(seconds):
    """Helper function to format duration nicely"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"