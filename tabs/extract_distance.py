import streamlit as st

def show():
    st.title("Extract Route Distance")
    st.write("Extract the actual travel distance from route data")
    
    if 'route_data' not in st.session_state or st.session_state.route_data is None:
        st.warning("No route data available. Please plan a route first using the Route Planner tab.")
        return
    
    route_data = st.session_state.route_data
    
    # Validate route data structure
    if 'distance' not in route_data:
        st.error("Invalid route data: Missing distance information")
        return
        
    try:
        distance_meters = route_data['distance']
        
        if isinstance(distance_meters, (int, float)):
            st.success(f"📏 Travel distance: {distance_meters/1000:.2f} km")
            
            # Display route details if available
            if all(key in route_data for key in ['start_address', 'end_address', 'travel_mode']):
                st.write("**Route Details:**")
                st.write(f"📍 From: {route_data['start_address']}")
                st.write(f"🏁 To: {route_data['end_address']}")
                st.write(f"🚗 Mode: {route_data['travel_mode']}")
        else:
            st.error("Invalid distance format in route data")
            
    except Exception as e:
        st.error(f"Error processing route data: {str(e)}")