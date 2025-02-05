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
    "Lekstraat[Almere]": [52.3752, 5.2140],
    "Wisselweg[Almere]": [52.3702, 5.2148],
    "Flevo Ziekenhuis Hoofdingang": [52.3680, 5.2216],
    "Basilicumweg[Almere]": [52.3697, 5.2238],
    "Flevo Ziekenhuis SPOEDEISENDE HULP": [52.3682, 5.2210],
    "Metropolestraat[Almere]": [52.3755, 5.2197],
    "Markerkant 12[Almere]": [52.3664, 5.2251],
    "Trekweg[Almere]": [52.3823, 5.2219],
    "Station Almere Buiten": [52.3750, 5.2754],
    "Mantegnaplantsoen[Almere]": [52.3698, 5.2183],
    "Cinemadreef[Almere]": [52.3758, 5.2301],
    "Hibiscusstraat[Almere]": [52.3715, 5.2367],
    "Borneostraat[Almere]": [52.3762, 5.2321],
    "Grote Markt (Men at Work)": [52.3740, 5.2188]
}


def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

def can_combine(ride1, ride2):
    return (
        ride1["pickup_location"] == ride2["pickup_location"]
        and abs(time_to_minutes(ride1["scheduled_time"]) - time_to_minutes(ride2["scheduled_time"])) <= 20
    )

def assign_rides(rides, vehicles, drivers):
    rides.sort(key=lambda x: time_to_minutes(x["scheduled_time"]))
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
    {"ride_id": 1, "pickup_location": "Lekstraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:45", "passengers": 2},
    {"ride_id": 2, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Lekstraat[Almere]", "scheduled_time": "20:00", "passengers": 2},
    {"ride_id": 3, "pickup_location": "Lekstraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:45", "passengers": 2},
    {"ride_id": 4, "pickup_location": "Flevo Ziekenhuis Hoofdingang", "dropoff_location": "Basilicumweg[Almere]", "scheduled_time": "17:35", "passengers": 2},
    {"ride_id": 5, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Flevo Ziekenhuis Hoofdingang", "scheduled_time": "15:30", "passengers": 2},
    {"ride_id": 6, "pickup_location": "Metropolestraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "18:40", "passengers": 2},
    {"ride_id": 7, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Markerkant 12[Almere]", "scheduled_time": "20:00", "passengers": 1},
    {"ride_id": 8, "pickup_location": "Markerkant 12[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "23:00", "passengers": 1},
    {"ride_id": 9, "pickup_location": "Markerkant 12[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "23:00", "passengers": 1},
    {"ride_id": 10, "pickup_location": "Lekstraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "23:45", "passengers": 2},
    {"ride_id": 11, "pickup_location": "Lekstraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "00:25", "passengers": 2},
    {"ride_id": 12, "pickup_location": "Markerkant 12[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:30", "passengers": 2},
    {"ride_id": 13, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Markerkant 12[Almere]", "scheduled_time": "19:30", "passengers": 2},
    {"ride_id": 14, "pickup_location": "Markerkant 12[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "16:45", "passengers": 2},
    {"ride_id": 15, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Markerkant 12[Almere]", "scheduled_time": "18:45", "passengers": 2},
    {"ride_id": 16, "pickup_location": "Markerkant 12[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:00", "passengers": 2},
    {"ride_id": 17, "pickup_location": "Lekstraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "23:45", "passengers": 2},
    {"ride_id": 18, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Lekstraat[Almere]", "scheduled_time": "19:30", "passengers": 2},
    {"ride_id": 19, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Markerkant 12[Almere]", "scheduled_time": "18:45", "passengers": 2},
    {"ride_id": 20, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Flevo Ziekenhuis Hoofdingang", "scheduled_time": "13:00", "passengers": 2},
    {"ride_id": 21, "pickup_location": "Lekstraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:45", "passengers": 1},
    {"ride_id": 22, "pickup_location": "Flevo Ziekenhuis SPOEDEISENDE HULP", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:45", "passengers": 2},
    {"ride_id": 23, "pickup_location": "Flevo Ziekenhuis Hoofdingang", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:10", "passengers": 2},
    {"ride_id": 24, "pickup_location": "Trekweg[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:30", "passengers": 2},
    {"ride_id": 25, "pickup_location": "Station Almere Buiten", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "17:45", "passengers": 1},
    {"ride_id": 26, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Mantegnaplantsoen[Almere]", "scheduled_time": "14:30", "passengers": 1},
    {"ride_id": 27, "pickup_location": "Cinemadreef[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "14:00", "passengers": 2},
    {"ride_id": 28, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Hibiscusstraat[Almere]", "scheduled_time": "13:00", "passengers": 1},
    {"ride_id": 29, "pickup_location": "Hibiscusstraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "16:00", "passengers": 1},
    {"ride_id": 30, "pickup_location": "Borneostraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "17:30", "passengers": 1},
    {"ride_id": 31, "pickup_location": "Grote Markt (Men at Work)", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:15", "passengers": 1},
    {"ride_id": 32, "pickup_location": "Wisselweg[Almere]", "dropoff_location": "Lekstraat[Almere]", "scheduled_time": "20:00", "passengers": 1},
    {"ride_id": 33, "pickup_location": "Lekstraat[Almere]", "dropoff_location": "Wisselweg[Almere]", "scheduled_time": "22:15", "passengers": 1},
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
timeline_data = []
for assignment in ride_assignments:
            combined_status = "Yes" if len(assignment["rides"]) > 1 else "No"
            # Sort rides by scheduled time for each assignment
            sorted_rides = sorted(assignment["rides"], key=lambda r: time_to_minutes(r["scheduled_time"]))
            for idx, ride in enumerate(sorted_rides):
                timeline_data.append({
                    "Driver ID": assignment["driver_id"],
                    "Vehicle ID": assignment["vehicle_id"],
                    "Trip Order": idx + 1,
                    "Pickup Location": ride["pickup_location"],
                    "Dropoff Location": ride["dropoff_location"],
                    "Scheduled Time": ride["scheduled_time"],
                    "Passengers": ride["passengers"],
                    "Combined Ride": combined_status

                })

timeline_df = pd.DataFrame(timeline_data)

timeline_df["Scheduled Time"] = pd.to_datetime("2025-02-03 " + timeline_df["Scheduled Time"], format='%Y-%m-%d %H:%M')
timeline_df["End Time"] = timeline_df["Scheduled Time"] + pd.Timedelta(minutes=30)

light_blue = "#a6cee3"  # light
dark_blue = "#1f78b4"   # dark
driver_trip_counts = timeline_df.groupby("Driver ID")["Trip Order"].max().to_dict()

def get_gradient_color(row):
            driver = row["Driver ID"]
            order = row["Trip Order"]
            total = driver_trip_counts.get(driver, 1)
            t = 0 if total == 1 else (order - 1) / (total - 1)
            return interpolate_color(light_blue, dark_blue, t)

timeline_df["CustomColor"] = timeline_df.apply(get_gradient_color, axis=1)

fig = px.timeline(
            timeline_df,
            x_start="Scheduled Time",
            x_end="End Time",
            y="Driver ID",
            color="CustomColor",
            title="Ride Assignments Timeline",
            hover_data={
                "Pickup Location": True,
                "Dropoff Location": True,
                "Scheduled Time": True,
                "Passengers": True,
                "CustomColor": False
            }
        )
fig.update_layout(showlegend=False,
                          xaxis_title="Time",
                          yaxis_title="Driver ID",
                          height=600,
                          xaxis=dict(
                              range=[
                                  pd.to_datetime("2025-02-03 00:00", format='%Y-%m-%d %H:%M'),
                                  pd.to_datetime("2025-02-03 23:00", format='%Y-%m-%d %H:%M')
                              ]
                          ))
fig.update_traces(
            hovertemplate=
            "<b>Driver:</b> %{y}<br>" +
            "<b>Scheduled:</b> %{x}<br>" +
            "<b>Pickup:</b> %{customdata[0]}<br>" +
            "<b>Dropoff:</b> %{customdata[1]}<br>" +
            "<b>Passengers:</b> %{customdata[3]}<extra></extra>"
        )
st.plotly_chart(fig)

        # ---------------------------
        # Middle Section: Driver Selection (Centered)
        # ---------------------------

# Assume timeline_df is already prepared as shown in your code.

# Define the number of rows per page
rows_per_page = 5

# Calculate total number of pages
total_pages = (len(timeline_df) - 1) // rows_per_page + 1

# Create pagination controls
page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

# Compute the start and end indices for the DataFrame slice
start_idx = (page - 1) * rows_per_page
end_idx = start_idx + rows_per_page

# Slice the DataFrame and display it
st.dataframe(timeline_df.iloc[start_idx:end_idx])

st.markdown("### Select a Driver")
selected_driver = st.selectbox("Select a driver", list(range(1, NUM_DRIVERS + 1)))

        # ---------------------------
        # Bottom Section: Driver Details (Trips List & Map)
        # ---------------------------
st.markdown(f"### Trips assigned to Driver {selected_driver}")
        # Sort the rides for the selected driver by scheduled time and add trip number
if selected_driver in driver_assignments:
            driver_rides = sorted(driver_assignments[selected_driver], key=lambda r: time_to_minutes(r["scheduled_time"]))
            for i, ride in enumerate(driver_rides, start=1):
                st.write(f"- Trip {i}: Ride {ride['ride_id']} from {ride['pickup_location']} to {ride['dropoff_location']} at {ride['scheduled_time']}, Passengers: {ride['passengers']}")
else:
            st.write("No rides assigned to this driver.")

st.markdown("### Ride Route Map")
map_center = [52.3676, 4.9041]
m = folium.Map(location=map_center, zoom_start=10)

        # For each ride of the selected driver (sorted by scheduled time)
if selected_driver in driver_assignments:
            driver_rides = sorted(driver_assignments[selected_driver], key=lambda r: time_to_minutes(r["scheduled_time"]))
            for i, ride in enumerate(driver_rides, start=1):
                pickup_coords = city_coords.get(ride["pickup_location"], map_center)
                dropoff_coords = city_coords.get(ride["dropoff_location"], map_center)
                # Define complete details for tooltip/pop-up
                details = (
                    f"Trip {i}<br>"
                    f"Ride ID: {ride['ride_id']}<br>"
                    f"Pickup: {ride['pickup_location']}<br>"
                    f"Dropoff: {ride['dropoff_location']}<br>"
                    f"Time: {ride['scheduled_time']}<br>"
                    f"Passengers: {ride['passengers']}"
                )
                # Draw thicker route line (weight=6) with a tooltip on hover.
                polyline = folium.PolyLine(
                    locations=[pickup_coords, dropoff_coords],
                    color="blue",
                    weight=6,
                    opacity=1,
                    tooltip=details
                )
                polyline.add_to(m)
                # Calculate midpoint to place a label for the trip number.
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
                # Optionally, add markers for pickup and dropoff points with their own popups.
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

