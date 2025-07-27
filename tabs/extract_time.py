import streamlit as st
from datetime import timedelta

def show():
    st.title("Extract Route Time")
    st.write("Extract human-readable travel time from route data")
    
    if 'route_data' not in st.session_state or st.session_state.route_data is None:
        st.warning("No route data available. Please plan a route first using the Route Planner tab.")
        return
    
    route_data = st.session_state.route_data
    
    # Validate route data structure
    if 'duration' not in route_data:
        st.error("Invalid route data: Missing duration information")
        return
        
    try:
        duration_seconds = route_data['duration']
        
        # Convert to human-readable format
        if isinstance(duration_seconds, (int, float)):
            if duration_seconds < 60:
                time_str = f"{int(duration_seconds)} sec"
            elif duration_seconds < 3600:
                minutes = int(duration_seconds / 60)
                seconds = int(duration_seconds % 60)
                time_str = f"{minutes} min {seconds} sec"
            else:
                hours = int(duration_seconds / 3600)
                remaining_seconds = duration_seconds % 3600
                minutes = int(remaining_seconds / 60)
                time_str = f"{hours} h {minutes} min"
            
            st.success(f"⏱️ Travel time: {time_str}")
        else:
            st.error("Invalid duration format in route data")
            
        # Display route details if available
        if all(key in route_data for key in ['start_address', 'end_address', 'travel_mode']):
            st.write("**Route Details:**")
            st.write(f"📍 From: {route_data['start_address']}")
            st.write(f"🏁 To: {route_data['end_address']}")
            st.write(f"🚗 Mode: {route_data['travel_mode']}")
            
    except Exception as e:
        st.error(f"Error processing route data: {str(e)}")