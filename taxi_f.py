import streamlit as st
import pandas as pd
import heapq
from collections import defaultdict
import folium
from folium.features import DivIcon
from streamlit_folium import folium_static
import plotly.express as px

# ---------------------------
# Configuration & Helper Functions
# ---------------------------

# Define the number of available vehicles and drivers
NUM_VEHICLES = 8
NUM_DRIVERS = 8

# City coordinates (for visualization)
city_coords = {
    "Flevolaan[Naarden]": [52.2945, 5.1625],
    "Audrey Hepburnstraat[Almere]": [52.3505, 5.2647],
    "Diemerkade[Diemen]": [52.3493, 4.9684],
    "Flevo Ziekenhuis Hoofdingang": [52.3680, 5.2216],
    "Maandenweg[Almere]": [52.3730, 5.2612],
    "AMC Hoofd [AdamZO]": [52.2949, 4.9577],
    "Operetteweg[Almere]": [52.3596, 5.2593],
    "Hullenbergweg[Amsterdam]": [52.3061, 4.9435],
    "Hettenheuvelweg[Amsterdam Zuidoost]": [52.3078, 4.9442],
}

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

def can_combine(ride1, ride2):
    return (
        ride1["pickup_location"] == ride2["pickup_location"]
        and abs(time_to_minutes(ride1["scheduled_start_time"]) - time_to_minutes(ride2["scheduled_start_time"])) <= 20
    )

def assign_rides(rides, vehicles, drivers):
    rides.sort(key=lambda x: time_to_minutes(x["scheduled_start_time"]))
    vehicle_queue = [(0, vehicle["vehicle_id"]) for vehicle in vehicles]
    heapq.heapify(vehicle_queue)
    ride_assignments = []
    combined_rides = defaultdict(list)
    driver_assignments = defaultdict(list)

    for ride in rides:
        assigned = False
        for combined_ride in combined_rides.values():
            # Combine rides if pickup is the same and scheduled times are within 20 minutes.
            if sum(r["passengers"] for r in combined_ride) + ride["passengers"] <= 4 and can_combine(combined_ride[0], ride):
                combined_ride.append(ride)
                assigned = True
                break
        if not assigned:
            combined_rides[ride["ride_id"]].append(ride)

    for combined_id, combined_ride in combined_rides.items():
        earliest_available_time, vehicle_id = heapq.heappop(vehicle_queue)
        driver_id = vehicle_id  # Each vehicle is assigned a driver with the same ID.
        ride_assignments.append({"vehicle_id": vehicle_id, "driver_id": driver_id, "rides": combined_ride})
        driver_assignments[driver_id].extend(combined_ride)
        # Update vehicle busy time (each ride or combined rides take 30 minutes)
        heapq.heappush(vehicle_queue, (earliest_available_time + 30, vehicle_id))

    return ride_assignments, driver_assignments, combined_rides

# Color interpolation helper functions
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def interpolate_color(color1, color2, t):
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    interpolated = tuple(int(rgb1[i] + (rgb2[i] - rgb1[i]) * t) for i in range(3))
    return rgb_to_hex(interpolated)

# ---------------------------
# Streamlit UI
# ---------------------------

st.image("logo.jpeg", width=200)
st.title("Taxi Ride Scheduler")

rides = [
    
  {
    "ride_id": 1,
    "pickup_location": "Flevolaan[Naarden]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "08:00",
    "scheduled_end_time": "08:30"
  },
  {
    "ride_id": 2,
    "pickup_location": "Flevolaan[Naarden]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "08:10",
    "scheduled_end_time": "08:45"
  },
  {
    "ride_id": 3,
    "pickup_location": "Diemerkade[Diemen]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "09:00",
    "scheduled_end_time": "09:25"
  },
  {
    "ride_id": 4,
    "pickup_location": "Flevo Ziekenhuis Hoofdingang",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "09:00",
    "scheduled_end_time": "09:15"
  },
  {
    "ride_id": 5,
    "pickup_location": "Maandenweg[Almere]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "09:40",
    "scheduled_end_time": "09:50"
  },
  {
    "ride_id": 6,
    "pickup_location": "Maandenweg[Almere]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "09:50",
    "scheduled_end_time": "10:00"
  },
  {
    "ride_id": 7,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "9:30",
    "scheduled_end_time": "10:00"
  },
  {
    "ride_id": 8,
    "pickup_location": "Flevo Ziekenhuis Hoofdingang",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "10:30",
    "scheduled_end_time": "10:45"
  },
  {
    "ride_id": 9,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "Operetteweg[Almere]",
    "passengers": 1,
    "scheduled_start_time": "10:45",
    "scheduled_end_time": "11:00"
  },
  {
    "ride_id": 10,
    "pickup_location": "Hullenbergweg[Amsterdam]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 2,
    "scheduled_start_time": "11:00",
    "scheduled_end_time": "11:40"
  },
  {
    "ride_id": 11,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "Operetteweg[Almere]",
    "passengers": 1,
    "scheduled_start_time": "11:30",
    "scheduled_end_time": "11:40"
  },
  {
    "ride_id": 12,
    "pickup_location": "Operetteweg[Almere]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "11:10",
    "scheduled_end_time": "11:20"
  },
  {
    "ride_id": 13,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "Hettenheuvelweg[Amsterdam Zuidoost]",
    "passengers": 1,
    "scheduled_start_time": "12:00",
    "scheduled_end_time": "12:40"
  },
  {
    "ride_id": 14,
    "pickup_location": "Hettenheuvelweg[Amsterdam Zuidoost]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "12:00",
    "scheduled_end_time": "12:40"
  },
  {
    "ride_id": 15,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "Operetteweg[Almere]",
    "passengers": 1,
    "scheduled_start_time": "13:20",
    "scheduled_end_time": "13:30"
  },
  {
    "ride_id": 16,
    "pickup_location": "Operetteweg[Almere]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "13:30",
    "scheduled_end_time": "13:40"
  },
  {
    "ride_id": 17,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 2,
    "scheduled_start_time": "13:40",
    "scheduled_end_time": "14:10"
  },
  {
    "ride_id": 18,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "14:10",
    "scheduled_end_time": "14:40"
  },
  {
    "ride_id": 19,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "14:40",
    "scheduled_end_time": "15:10"
  },
  {
    "ride_id": 20,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "15:10",
    "scheduled_end_time": "15:40"
  },
  {
    "ride_id": 21,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "15:40",
    "scheduled_end_time": "16:10"
  },
  {
    "ride_id": 22,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "16:10",
    "scheduled_end_time": "16:40"
  },
  {
    "ride_id": 23,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "16:40",
    "scheduled_end_time": "17:10"
  },
  {
    "ride_id": 24,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "17:10",
    "scheduled_end_time": "17:40"
  },
  {
    "ride_id": 25,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "17:40",
    "scheduled_end_time": "18:10"
  },
  {
    "ride_id": 26,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "18:10",
    "scheduled_end_time": "18:40"
  },
  {
    "ride_id": 27,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "18:40",
    "scheduled_end_time": "19:10"
  },
  {
    "ride_id": 28,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "19:10",
    "scheduled_end_time": "19:40"
  },
  {
    "ride_id": 29,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "19:40",
    "scheduled_end_time": "20:10"
  },
  {
    "ride_id": 30,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "20:10",
    "scheduled_end_time": "20:40"
  },
  {
    "ride_id": 31,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "20:40",
    "scheduled_end_time": "21:10"
  },
  {
    "ride_id": 32,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "21:10",
    "scheduled_end_time": "21:40"
  },
  {
    "ride_id": 33,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "21:40",
    "scheduled_end_time": "22:10"
  },
  {
    "ride_id": 34,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "22:10",
    "scheduled_end_time": "22:40"
  },
  {
    "ride_id": 35,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "22:40",
    "scheduled_end_time": "23:10"
  },
  {
    "ride_id": 36,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "23:10",
    "scheduled_end_time": "23:40"
  },
  {
    "ride_id": 37,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "23:40",
    "scheduled_end_time": "00:10"
  },
  {
    "ride_id": 38,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "00:10",
    "scheduled_end_time": "00:40"
  },
  {
    "ride_id": 39,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "00:40",
    "scheduled_end_time": "01:10"
  },
  {
    "ride_id": 40,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "01:10",
    "scheduled_end_time": "01:40"
  },
  {
    "ride_id": 41,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "01:40",
    "scheduled_end_time": "02:10"
  },
  {
    "ride_id": 42,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "02:15",
    "scheduled_end_time": "02:45"
  },
  {
    "ride_id": 43,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "02:50",
    "scheduled_end_time": "03:20"
  },
  {
    "ride_id": 44,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "03:25",
    "scheduled_end_time": "03:55"
  },
  {
    "ride_id": 45,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "04:00",
    "scheduled_end_time": "04:30"
  },
  {
    "ride_id": 46,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "04:35",
    "scheduled_end_time": "05:05"
  },
  {
    "ride_id": 47,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "05:10",
    "scheduled_end_time": "05:40"
  },
  {
    "ride_id": 48,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "05:45",
    "scheduled_end_time": "06:15"
  },
  {
    "ride_id": 49,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "06:20",
    "scheduled_end_time": "06:50"
  },
  {
    "ride_id": 50,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "06:55",
    "scheduled_end_time": "07:25"
  },
  {
    "ride_id": 51,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "07:30",
    "scheduled_end_time": "08:00"
  },
  {
    "ride_id": 52,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "08:05",
    "scheduled_end_time": "08:35"
  },
  {
    "ride_id": 53,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "08:40",
    "scheduled_end_time": "09:10"
  },
  {
    "ride_id": 54,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "09:15",
    "scheduled_end_time": "09:45"
  },
  {
    "ride_id": 55,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 1,
    "scheduled_start_time": "09:50",
    "scheduled_end_time": "10:20"
  },
  {
    "ride_id": 56,
    "pickup_location": "AMC Hoofd [AdamZO]",
    "dropoff_location": "Audrey Hepburnstraat[Almere]",
    "passengers": 1,
    "scheduled_start_time": "10:25",
    "scheduled_end_time": "10:55"
  },
  {
    "ride_id": 57,
    "pickup_location": "Audrey Hepburnstraat[Almere]",
    "dropoff_location": "AMC Hoofd [AdamZO]",
    "passengers": 2,
    "scheduled_start_time": "11:00",
    "scheduled_end_time": "11:30"
  }

]

vehicles = [{"vehicle_id": i + 1, "capacity": 4, "status": "Available", "assigned_rides": []} for i in range(NUM_VEHICLES)]
drivers = [{"driver_id": i + 1, "status": "Available", "assigned_vehicle": i + 1} for i in range(NUM_DRIVERS)]

ride_assignments, driver_assignments, combined_rides = assign_rides(rides, vehicles, drivers)

# ---------------------------
# Top Section: Dashboard Summary & Timeline Chart
# ---------------------------

st.markdown("### Dashboard Summary")

# Compute metrics for dashboard tiles:
num_drivers = NUM_DRIVERS
num_trips = len(rides)
combined_trip_count = sum(1 for rides in combined_rides.values() if len(rides) > 1)
total_passengers = sum(trip["passengers"] for trip in rides)

col1, col2, col3, col4 = st.columns(4)
tile_style = """
            <div style="
                background-color:{bg_color};
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                height: 150px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <h3 style="margin: 0; color:{text_color};">{title}</h3>
                <h2 style="margin: 0; color:{text_color};">{value}</h2>
            </div>
        """

with col1:
    st.markdown(tile_style.format(bg_color="#FFDD57", text_color="#000", title="Drivers", value=num_drivers), unsafe_allow_html=True)
with col2:
    st.markdown(tile_style.format(bg_color="#FF6F61", text_color="#fff", title="Trips", value=num_trips), unsafe_allow_html=True)
with col3:
    st.markdown(tile_style.format(bg_color="#6B5B95", text_color="#fff", title="Combined Trips", value=combined_trip_count), unsafe_allow_html=True)
with col4:
    st.markdown(tile_style.format(bg_color="#88B04B", text_color="#fff", title="Total Passengers", value=total_passengers), unsafe_allow_html=True)

# Timeline chart setup
st.markdown("### Ride Timeline (24-Hour Period)")

def normalize_time(time_str):
    """Convert times >= 24:00 to next day time"""
    hours, minutes = map(int, time_str.split(":"))
    if hours >= 24:
        hours = hours - 24
    return f"{hours:02d}:{minutes:02d}"

timeline_data = []
for assignment in ride_assignments:
    vehicle_id = assignment["vehicle_id"]
    driver_id = assignment["driver_id"]
    
    # Determine if these are combined rides
    is_combined = len(assignment["rides"]) > 1
    
    for ride in assignment["rides"]:
        # Normalize times
        start_time = normalize_time(ride["scheduled_start_time"])
        end_time = normalize_time(ride["scheduled_end_time"])
        
        # Determine if the ride crosses midnight
        crosses_midnight = (
            time_to_minutes(ride["scheduled_end_time"]) < time_to_minutes(ride["scheduled_start_time"])
            or int(ride["scheduled_start_time"].split(":")[0]) >= 24
        )
        
        timeline_data.append({
            "Driver ID": driver_id,
            "Vehicle ID": vehicle_id,
            "Ride ID": ride["ride_id"],
            "Pickup Location": ride["pickup_location"],
            "Dropoff Location": ride["dropoff_location"],
            "Scheduled Time": start_time,
            "Scheduled End Time": end_time,
            "Passengers": ride["passengers"],
            "Ride Type": "Combined Ride" if is_combined else "Single Ride",
            "Crosses Midnight": crosses_midnight
        })

timeline_df = pd.DataFrame(timeline_data)

# Convert times to datetime
base_date = "2025-02-03"
next_date = "2025-02-04"

timeline_df["Start DateTime"] = pd.to_datetime(base_date + " " + timeline_df["Scheduled Time"])
timeline_df["End DateTime"] = pd.to_datetime(base_date + " " + timeline_df["Scheduled End Time"])

# Adjust dates for rides crossing midnight
mask = timeline_df["Crosses Midnight"]
timeline_df.loc[mask, "End DateTime"] = pd.to_datetime(next_date + " " + timeline_df.loc[mask, "Scheduled End Time"])

# For rides starting after midnight (e.g., 24:00+), adjust both start and end times
mask_late_start = timeline_df["Start DateTime"].dt.hour < timeline_df["End DateTime"].dt.hour
timeline_df.loc[mask_late_start & mask, "Start DateTime"] += pd.Timedelta(days=1)

# Define colors for ride types
color_map = {
    "Single Ride": "#1f77b4",    # Blue
    "Combined Ride": "#2ca02c"   # Green
}

# Create statistics for combined rides
total_rides = len(timeline_df)
combined_rides = len(timeline_df[timeline_df["Ride Type"] == "Combined Ride"])
single_rides = total_rides - combined_rides

# Display statistics
st.markdown("### Ride Statistics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rides", total_rides)
with col2:
    st.metric("Combined Rides", combined_rides)
with col3:
    st.metric("Single Rides", single_rides)

# Create the timeline visualization
fig = px.timeline(
    timeline_df,
    x_start="Start DateTime",
    x_end="End DateTime",
    y="Driver ID",
    color="Ride Type",
    color_discrete_map=color_map,
    hover_name="Ride ID",
    title="Ride Assignments Timeline",
    labels={"Driver ID": "Driver", "Ride Type": "Type"},
    hover_data={
        "Pickup Location": True,
        "Dropoff Location": True,
        "Scheduled Time": True,
        "Scheduled End Time": True,
        "Passengers": True,
        "Vehicle ID": True,
        "Ride Type": True,
        "Driver ID": False,
        "Crosses Midnight": False
    }
)

# Update layout
fig.update_layout(
    showlegend=True,
    legend_title="Ride Type",
    xaxis_title="Time",
    yaxis_title="Driver ID",
    height=400,
    xaxis=dict(
        tickformat="%H:%M",
        tickmode="linear",
        dtick="2H",
        range=[
            pd.to_datetime(f"{base_date} 00:00"),
            pd.to_datetime(f"{next_date} 00:00")
        ]
    ),
    yaxis=dict(
        range=[0.5, NUM_DRIVERS + 0.5],
        tickmode="linear",
        tick0=1,
        dtick=1
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12
    ),
    # Adjust legend position
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Update hover template
fig.update_traces(
    hovertemplate="<b>Ride %{hovertext}</b><br>" +
                  "Driver: %{y}<br>" +
                  "Vehicle: %{customdata[5]}<br>" +
                  "Type: %{customdata[6]}<br>" +
                  "From: %{customdata[0]}<br>" +
                  "To: %{customdata[1]}<br>" +
                  "Start: %{customdata[2]}<br>" +
                  "End: %{customdata[3]}<br>" +
                  "Passengers: %{customdata[4]}<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

# Add a detailed breakdown of combined rides
if combined_rides > 0:
    st.markdown("### Combined Rides Details")
    combined_df = timeline_df[timeline_df["Ride Type"] == "Combined Ride"].copy()
    combined_df = combined_df.sort_values(["Driver ID", "Start DateTime"])
    
    # Group combined rides by driver and time
    grouped_rides = combined_df.groupby(["Driver ID", "Vehicle ID", "Scheduled Time"])
    
    for name, group in grouped_rides:
        driver_id, vehicle_id, start_time = name
        st.write(f"Driver {driver_id} (Vehicle {vehicle_id}) - Start Time: {start_time}")
        for _, ride in group.iterrows():
            st.write(f"  - Ride {ride['Ride ID']}: {ride['Pickup Location']} → {ride['Dropoff Location']}, {ride['Passengers']} passenger(s)")

# ---------------------------
# Middle Section: Driver Selection (Centered)
# ---------------------------

# Pagination for timeline
rows_per_page = 5
total_pages = (len(timeline_df) - 1) // rows_per_page + 1
page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

# Slice and display the timeline
start_idx = (page - 1) * rows_per_page
end_idx = start_idx + rows_per_page
st.dataframe(timeline_df.iloc[start_idx:end_idx])

st.markdown("### Select a Driver")
selected_driver = st.selectbox("Select a driver", list(range(1, NUM_DRIVERS + 1)))

# ---------------------------
# Bottom Section: Driver Details (Trips List & Map)
# ---------------------------

st.markdown(f"### Trips assigned to Driver {selected_driver}")

if selected_driver in driver_assignments:
    driver_rides = sorted(driver_assignments[selected_driver], key=lambda r: time_to_minutes(r["scheduled_start_time"]))
    for i, ride in enumerate(driver_rides, start=1):
        st.write(f"- Trip {i}: Ride {ride['ride_id']} from {ride['pickup_location']} to {ride['dropoff_location']} at {ride['scheduled_start_time']}, Passengers: {ride['passengers']}")
else:
    st.write("No rides assigned to this driver.")

st.markdown("### Ride Route Map")
map_center = [52.3676, 4.9041]
m = folium.Map(location=map_center, zoom_start=10)

if selected_driver in driver_assignments:
    driver_rides = sorted(driver_assignments[selected_driver], key=lambda r: time_to_minutes(r["scheduled_start_time"]))
    for i, ride in enumerate(driver_rides, start=1):
        pickup_coords = city_coords.get(ride["pickup_location"], map_center)
        dropoff_coords = city_coords.get(ride["dropoff_location"], map_center)
        details = (
            f"Trip {i}<br>"
            f"Ride ID: {ride['ride_id']}<br>"
            f"Pickup: {ride['pickup_location']}<br>"
            f"Dropoff: {ride['dropoff_location']}<br>"
            f"Time: {ride['scheduled_start_time']}<br>"
            f"Passengers: {ride['passengers']}"
        )
        polyline = folium.PolyLine(
            locations=[pickup_coords, dropoff_coords],
            color="blue",
            weight=6,
            opacity=1,
            tooltip=details
        )
        polyline.add_to(m)
        mid_lat = (pickup_coords[0] + dropoff_coords[0]) / 2
        mid_lon = (pickup_coords[1] + dropoff_coords[1]) / 2
        folium.map.Marker(
            [mid_lat, mid_lon],
            icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(0,0),
                html=f'<div style="font-size: 16pt; color: black; background: #ffffffbb; border-radius: 5px; padding: 2px;">Trip {i}</div>',
            )
        ).add_to(m)
        folium.Marker(
            location=pickup_coords,
            popup=f"Pickup: {ride['pickup_location']}",
            icon=folium.Icon(color="blue")
        ).add_to(m)
        folium.Marker(
            location=dropoff_coords,
            popup=f"Dropoff: {ride['dropoff_location']}",
            icon=folium.Icon(color="red")
        ).add_to(m)

folium_static(m)
