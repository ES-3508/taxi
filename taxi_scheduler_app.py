import streamlit as st
import pandas as pd
import heapq
from collections import defaultdict
import folium
from streamlit_folium import folium_static


# Define the number of available vehicles and drivers
NUM_VEHICLES = 8
NUM_DRIVERS = 8

# Updated hospital locations in and around Amsterdam
city_coords = {
    "Amsterdam": [52.3676, 4.9041],  # VU University Medical Center (Amsterdam)
    "Amstelveen": [52.3085, 4.8500],  # Amstelland Hospital (Amstelveen)
    "Haarlem": [52.3874, 4.6462],  # Haarlem Medical Center (Haarlem)
    "Zaandam": [52.4373, 4.8294],  # Zaans Medical Center (Zaandam)
    "Alkmaar": [52.6326, 4.7531],  # Noordwest Ziekenhuisgroep (Alkmaar)
    "Hilversum": [52.2301, 5.1706],  # Tergooi Hospital (Hilversum)
    "Leiden": [52.1601, 4.4970],  # Leiden University Medical Center (Leiden)
    "Utrecht": [52.0907, 5.1214],  # University Medical Center Utrecht (Utrecht)
    "Diemen": [52.3245, 4.9577],  # Diemen Medical Center (Diemen)
}

# Function to convert time to minutes for easy comparison
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

# Function to check if two rides can be combined (within 20 minutes and same pickup location)
def can_combine(ride1, ride2):
    return (
        ride1["pickup_location"] == ride2["pickup_location"] and
        abs(time_to_minutes(ride1["scheduled_time"]) - time_to_minutes(ride2["scheduled_time"])) <= 20
    )

# Assign rides optimally with combination where possible
def assign_rides(rides, vehicles, drivers):
    rides.sort(key=lambda x: time_to_minutes(x["scheduled_time"]))  # Sort by scheduled time
    vehicle_queue = [(0, vehicle["vehicle_id"]) for vehicle in vehicles]  # Min-heap (earliest available vehicle first)
    heapq.heapify(vehicle_queue)
    ride_assignments = []
    combined_rides = defaultdict(list)  # Dictionary to hold combined rides
    driver_assignments = defaultdict(list)

    for ride in rides:
        assigned = False
        # Try to combine the ride with an existing combined ride
        for combined_ride in combined_rides.values():
            if sum(r["passengers"] for r in combined_ride) + ride["passengers"] <= 4 and can_combine(combined_ride[0], ride):
                combined_ride.append(ride)
                assigned = True
                break
        
        if not assigned:
            combined_rides[ride["ride_id"]].append(ride)
    
    # Now, assign rides to vehicles and drivers
    for combined_id, combined_ride in combined_rides.items():
        earliest_available_time, vehicle_id = heapq.heappop(vehicle_queue)
        driver_id = vehicle_id  # Assign a driver corresponding to the vehicle
        ride_assignments.append({"vehicle_id": vehicle_id, "driver_id": driver_id, "rides": combined_ride})
        driver_assignments[driver_id].extend(combined_ride)
        heapq.heappush(vehicle_queue, (earliest_available_time + 30, vehicle_id))  # Assume each ride takes 30 minutes
    
    return ride_assignments, driver_assignments, combined_rides

# Streamlit UI to upload CSV
st.title("Taxi Ride Scheduler")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file with ride data", type="csv")

if uploaded_file is not None:
    # Read CSV file into a pandas dataframe
    rides_df = pd.read_csv(uploaded_file)
    
    # Display the first few rows of the CSV to the user
    st.write("Ride Data from CSV:")
    # st.write(rides_df.head())

    # Ensure the CSV has the required columns (pickup_location, dropoff_location, scheduled_time, passengers)
    if all(col in rides_df.columns for col in ["pickup_location", "dropoff_location", "scheduled_time", "passengers"]):
        # Convert dataframe to a list of rides
        trips = []
        for idx, row in rides_df.iterrows():
            trips.append({
                "ride_id": idx + 1,
                "pickup_location": row["pickup_location"],
                "dropoff_location": row["dropoff_location"],
                "scheduled_time": row["scheduled_time"],
                "passengers": row["passengers"]
            })
        
        # Assign vehicles and drivers to the rides
        vehicles = [{"vehicle_id": i + 1, "capacity": 4, "status": "Available", "assigned_rides": []} for i in range(NUM_VEHICLES)]
        drivers = [{"driver_id": i + 1, "status": "Available", "assigned_vehicle": i + 1} for i in range(NUM_DRIVERS)]
        
        ride_assignments, driver_assignments, combined_rides = assign_rides(trips, vehicles, drivers)
        print("Ride Assignments:", ride_assignments)

        # Sidebar: Filter by Driver
        st.sidebar.header("Filter by Driver")
        selected_driver = st.sidebar.selectbox("Select a driver", range(1, NUM_DRIVERS + 1))

        st.subheader(f"Trips assigned to Driver {selected_driver}")
        if selected_driver in driver_assignments:
            for ride in driver_assignments[selected_driver]:
                st.write(f"- Ride {ride['ride_id']} from {ride['pickup_location']} to {ride['dropoff_location']} at {ride['scheduled_time']}, Passengers: {ride['passengers']}")
        else:
            st.write("No rides assigned to this driver.")

        # Map visualization (show only trips for the selected driver)
        st.subheader("Ride Route Map")
        map_center = [52.3676, 4.9041]  # Default to Amsterdam
        m = folium.Map(location=map_center, zoom_start=10)

        # Loop over only the rides assigned to the selected driver
        for assignment in ride_assignments:
            if assignment["driver_id"] == selected_driver:  # Only show rides for the selected driver
                for ride in assignment["rides"]:
                    pickup_coords = city_coords[ride["pickup_location"]]
                    dropoff_coords = city_coords[ride["dropoff_location"]]
                    
                    # Add markers for pickup and dropoff points for individual rides
                    folium.Marker(
                        location=pickup_coords,
                        popup=f"Pickup: {ride['pickup_location']}",
                        icon=folium.Icon(color="blue")  # Color for individual rides
                    ).add_to(m)
                    folium.Marker(
                        location=dropoff_coords,
                        popup=f"Dropoff: {ride['dropoff_location']}",
                        icon=folium.Icon(color="red")  # Color for dropoff
                    ).add_to(m)

                    # Add a line between pickup and dropoff points for individual rides
                    folium.PolyLine(
                        locations=[pickup_coords, dropoff_coords],
                        color="blue",  # Blue color for individual rides
                        weight=2.5,
                        opacity=1
                    ).add_to(m)

        # Highlight Combined Rides with a different color (green)
        for combined_id, combined_ride in combined_rides.items():
            # For combined rides, we will mark the first ride's pickup and dropoff
            combined_pickup_coords = city_coords[combined_ride[0]["pickup_location"]]
            combined_dropoff_coords = city_coords[combined_ride[0]["dropoff_location"]]
            
            # Add markers for combined pickup and dropoff points
            folium.Marker(
                location=combined_pickup_coords,
                popup=f"Pickup: Combined",
                icon=folium.Icon(color="green")  # Different color for combined rides
            ).add_to(m)
            folium.Marker(
                location=combined_dropoff_coords,
                popup=f"Dropoff: Combined",
                icon=folium.Icon(color="red")
            ).add_to(m)

            # Add a line between pickup and dropoff points for combined rides
            folium.PolyLine(
                locations=[combined_pickup_coords, combined_dropoff_coords],
                color="green",  # Green color for combined rides
                weight=3,
                opacity=1
            ).add_to(m)

        # Display the map in Streamlit
        folium_static(m)

        # Summary statistics (in the main area)
        st.subheader("Summary Statistics")
        total_rides = len(trips)
        assigned_rides = len(ride_assignments)
        unassigned_rides = total_rides - assigned_rides
        avg_passengers = sum(ride["passengers"] for ride in trips) / total_rides

        st.write(f"Total Rides: {total_rides}")
        st.write(f"Assigned Rides: {assigned_rides}")
        st.write(f"Unassigned Rides: {unassigned_rides}")
        st.write(f"Average Passengers per Ride: {avg_passengers:.2f}")

        # CSV download (in the sidebar)
        def rides_to_csv(ride_assignments):
            data = []
            for assignment in ride_assignments:
                for ride in assignment["rides"]:
                    data.append({
                        "ride_id": ride["ride_id"],
                        "pickup_location": ride["pickup_location"],
                        "dropoff_location": ride["dropoff_location"],
                        "scheduled_time": ride["scheduled_time"],
                        "passengers": ride["passengers"],
                        "vehicle_id": assignment["vehicle_id"],
                        "driver_id": assignment["driver_id"]
                    })
            return pd.DataFrame(data)

        df = rides_to_csv(ride_assignments)
        st.sidebar.download_button("Download Ride Assignments CSV", data=df.to_csv(index=False), file_name="ride_assignments.csv", mime="text/csv")
    else:
        st.error("CSV file must contain columns: pickup_location, dropoff_location, scheduled_time, passengers.")
