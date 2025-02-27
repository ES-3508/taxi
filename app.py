import openai
import json
import streamlit as st
import plotly.express as px
import pandas as pd
from geopy.distance import geodesic
import math
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
import folium
from streamlit_folium import folium_static
import random

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]

normal_assigned_trips = [{'ride_id': '4832056', 'driver_name': 'Norman'},
{'ride_id': '4832095', 'driver_name': 'Norman'},
{'ride_id': '4832047', 'driver_name': 'emma'},
{'ride_id': '4832097', 'driver_name': 'kriten'},
{'ride_id': '4828807', 'driver_name': 'kriten'},
{'ride_id': '4836309', 'driver_name': 'John Doe'},
{'ride_id': '4832098', 'driver_name': 'emma'},
{'ride_id': '4832079', 'driver_name': 'natalie'},
{'ride_id': '4836567', 'driver_name': 'John Doe'},
{'ride_id': '4836262', 'driver_name': 'John Doe'},
{'ride_id': '4835930', 'driver_name': 'John Doe'},
{'ride_id': '4832074', 'driver_name': 'kriten'},
{'ride_id': '4832104', 'driver_name': 'kriten'},
{'ride_id': '4836416', 'driver_name': 'John Doe'},
{'ride_id': '4836107', 'driver_name': 'emma'},
{'ride_id': '4836677', 'driver_name': 'emma'},
{'ride_id': '4836567', 'driver_name': 'kriten'},
 {'ride_id': '4836262', 'driver_name': 'emma'},
 {'ride_id': '4835930', 'driver_name': 'natalie'},
 {'ride_id': '4832074', 'driver_name': 'fred'},
 {'ride_id': '4832056', 'driver_name': 'croose'},
 {'ride_id': '4832095', 'driver_name': 'John Doe'},
 {'ride_id': '4832047', 'driver_name': 'Norman'},
 {'ride_id': '4832097', 'driver_name': 'fenna'},
 {'ride_id': '4828807', 'driver_name': 'kriten'},
 {'ride_id': '4836309', 'driver_name': 'emma'},
 {'ride_id': '4832098', 'driver_name': 'natalie'},
 {'ride_id': '4832079', 'driver_name': 'fred'},
 {'ride_id': '4832104', 'driver_name': 'croose'},
 {'ride_id': '4836416', 'driver_name': 'John Doe'},
 {'ride_id': '4836107', 'driver_name': 'Norman'},
 {'ride_id': '4836677', 'driver_name': 'fenna'},
 {'ride_id': '4832140', 'driver_name': 'kriten'},
 {'ride_id': '4832068', 'driver_name': 'emma'},
 {'ride_id': '4832105', 'driver_name': 'natalie'},
 {'ride_id': '4832110', 'driver_name': 'fred'},
{'ride_id': '4832078', 'driver_name': 'emma'},
{'ride_id': '4835963', 'driver_name': 'emma'},
{'ride_id': '4832138', 'driver_name': 'croose'},
 {'ride_id': '4832055', 'driver_name': 'John Doe'},
 {'ride_id': '4836523', 'driver_name': 'Norman'},
 {'ride_id': '4835961', 'driver_name': 'fenna'},
 {'ride_id': '4832067', 'driver_name': 'kriten'},
 {'ride_id': '4832130', 'driver_name': 'emma'},
 {'ride_id': '4832054', 'driver_name': 'natalie'},
 {'ride_id': '4832090', 'driver_name': 'fred'},
 {'ride_id': '4836227', 'driver_name': 'croose'},
 {'ride_id': '4831147', 'driver_name': 'John Doe'},
 {'ride_id': '4832117', 'driver_name': 'Norman'},
 {'ride_id': '4835593', 'driver_name': 'fenna'},
 {'ride_id': '4825796', 'driver_name': 'kriten'},
 {'ride_id': '4832069', 'driver_name': 'emma'},
 {'ride_id': '4836504', 'driver_name': 'natalie'},
 {'ride_id': '4834622', 'driver_name': 'fred'},
 {'ride_id': '4835606', 'driver_name': 'croose'},
 {'ride_id': '4832078', 'driver_name': 'John Doe'},
 {'ride_id': '4835963', 'driver_name': 'Norman'},
 {'ride_id': '4832086', 'driver_name': 'fenna'},
{'ride_id': '4836434', 'driver_name': 'emma'},
{'ride_id': '4836699', 'driver_name': 'emma'},
{'ride_id': '4836689', 'driver_name': 'emma'},
{'ride_id': '4836403', 'driver_name': 'emma'},
{'ride_id': '4836445', 'driver_name': 'emma'},
{'ride_id': '4834751', 'driver_name': 'emma'},
{'ride_id': '4835333', 'driver_name': 'emma'},
{'ride_id': '4836380', 'driver_name': 'emma'},
{'ride_id': '4832087', 'driver_name': 'kriten'},
 {'ride_id': '4834747', 'driver_name': 'emma'},
 {'ride_id': '4829381', 'driver_name': 'natalie'},
 {'ride_id': '4834467', 'driver_name': 'fred'},
 {'ride_id': '4832082', 'driver_name': 'croose'},
 {'ride_id': '4832129', 'driver_name': 'John Doe'},
 {'ride_id': '4836108', 'driver_name': 'Norman'},
 {'ride_id': '4835243', 'driver_name': 'fenna'},
 {'ride_id': '4832093', 'driver_name': 'kriten'},
 {'ride_id': '4832099', 'driver_name': 'emma'},
 {'ride_id': '4835308', 'driver_name': 'natalie'},
 {'ride_id': '4833187', 'driver_name': 'fred'},
 {'ride_id': '4832116', 'driver_name': 'croose'},
 {'ride_id': '4832096', 'driver_name': 'John Doe'},
 {'ride_id': '4832139', 'driver_name': 'Norman'},
 {'ride_id': '4832065', 'driver_name': 'fenna'},
 {'ride_id': '4832103', 'driver_name': 'kriten'},
 {'ride_id': '4835914', 'driver_name': 'emma'},
 {'ride_id': '4832113', 'driver_name': 'natalie'},
 {'ride_id': '4834468', 'driver_name': 'fred'},
 {'ride_id': '4836434', 'driver_name': 'croose'},
 {'ride_id': '4836699', 'driver_name': 'John Doe'},
 {'ride_id': '4836689', 'driver_name': 'Norman'},
 {'ride_id': '4836403', 'driver_name': 'fenna'},
 {'ride_id': '4836445', 'driver_name': 'kriten'},
 {'ride_id': '4834751', 'driver_name': 'emma'},
 {'ride_id': '4835333', 'driver_name': 'natalie'},
 {'ride_id': '4836380', 'driver_name': 'fred'},
 {'ride_id': '4836253', 'driver_name': 'croose'},
 {'ride_id': '4836365', 'driver_name': 'John Doe'},
 {'ride_id': '4836355', 'driver_name': 'Norman'},
 {'ride_id': '4836731', 'driver_name': 'fenna'},
 {'ride_id': '4835915', 'driver_name': 'kriten'},
 {'ride_id': '4829380', 'driver_name': 'emma'},
 {'ride_id': '4836549', 'driver_name': 'natalie'},
 {'ride_id': '4835617', 'driver_name': 'fred'},
 {'ride_id': '4830784', 'driver_name': 'croose'},
 {'ride_id': '4836762', 'driver_name': 'John Doe'},
 {'ride_id': '4836366', 'driver_name': 'kriten'},
 {'ride_id': '4835933', 'driver_name': 'emma'},
 {'ride_id': '4836356', 'driver_name': 'natalie'},
 {'ride_id': '4835616', 'driver_name': 'fred'},
 {'ride_id': '4836442', 'driver_name': 'croose'},
 {'ride_id': '4836393', 'driver_name': 'John Doe'},
 {'ride_id': '4836696', 'driver_name': 'kriten'},
 {'ride_id': '4835601', 'driver_name': 'emma'},
 {'ride_id': '4835440', 'driver_name': 'natalie'},
 {'ride_id': '4836361', 'driver_name': 'fred'},
 {'ride_id': '4836386', 'driver_name': 'croose'},
 {'ride_id': '4835964', 'driver_name': 'John Doe'},
 {'ride_id': '4836690', 'driver_name': 'kriten'},
 {'ride_id': '4835022', 'driver_name': 'emma'},
 {'ride_id': '4836848', 'driver_name': 'natalie'},
 {'ride_id': '4836370', 'driver_name': 'fred'},
 {'ride_id': '4836795', 'driver_name': 'croose'},
 {'ride_id': '4836693', 'driver_name': 'John Doe'},
 {'ride_id': '4836707', 'driver_name': 'kriten'},
 {'ride_id': '4836716', 'driver_name': 'emma'},
 {'ride_id': '4836765', 'driver_name': 'natalie'},
 {'ride_id': '4835019', 'driver_name': 'fred'},
 {'ride_id': '4832066', 'driver_name': 'croose'},
 {'ride_id': '4836692', 'driver_name': 'John Doe'},
 {'ride_id': '4836742', 'driver_name': 'kriten'},
 {'ride_id': '4836687', 'driver_name': 'emma'},
 {'ride_id': '4836702', 'driver_name': 'natalie'},
 {'ride_id': '4836688', 'driver_name': 'fred'},
 {'ride_id': '4832112', 'driver_name': 'croose'},
 {'ride_id': '4834469', 'driver_name': 'John Doe'},
 {'ride_id': '4836357', 'driver_name': 'kriten'},
 {'ride_id': '4834975', 'driver_name': 'emma'},
 {'ride_id': '4836743', 'driver_name': 'natalie'},
 {'ride_id': '4836714', 'driver_name': 'fred'},
 {'ride_id': '4836400', 'driver_name': 'croose'},
 {'ride_id': '4836114', 'driver_name': 'John Doe'},
 {'ride_id': '4836374', 'driver_name': 'kriten'},
 {'ride_id': '4832094', 'driver_name': 'emma'},
 {'ride_id': '4836741', 'driver_name': 'natalie'},
 {'ride_id': '4832109', 'driver_name': 'fred'},
 {'ride_id': '4832122', 'driver_name': 'croose'},
 {'ride_id': '4836686', 'driver_name': 'John Doe'},
 {'ride_id': '4836818', 'driver_name': 'kriten'},
 {'ride_id': '4836771', 'driver_name': 'emma'},
 {'ride_id': '4836706', 'driver_name': 'natalie'},
 {'ride_id': '4836395', 'driver_name': 'fred'},
 {'ride_id': '4832083', 'driver_name': 'croose'},
 {'ride_id': '4835292', 'driver_name': 'John Doe'},
 {'ride_id': '4836759', 'driver_name': 'emma'},
 {'ride_id': '4836359', 'driver_name': 'kriten'},
 {'ride_id': '4836869', 'driver_name': 'natalie'},
 {'ride_id': '4836534', 'driver_name': 'fred'},
 {'ride_id': '4836761', 'driver_name': 'croose'},
 {'ride_id': '4836703', 'driver_name': 'fenna'},
 {'ride_id': '4835020', 'driver_name': 'John Doe'},
 {'ride_id': '4832115', 'driver_name': 'emma'},
 {'ride_id': '4836325', 'driver_name': 'kriten'},
 {'ride_id': '4832050', 'driver_name': 'natalie'},
 {'ride_id': '4836556', 'driver_name': 'fred'},
 {'ride_id': '4836704', 'driver_name': 'croose'},
 {'ride_id': '4836758', 'driver_name': 'fenna'},
 {'ride_id': '4836720', 'driver_name': 'John Doe'},
 {'ride_id': '4836450', 'driver_name': 'emma'},
 {'ride_id': '4832108', 'driver_name': 'kriten'},
 {'ride_id': '4836854', 'driver_name': 'natalie'},
 {'ride_id': '4836104', 'driver_name': 'fred'},
 {'ride_id': '4836729', 'driver_name': 'croose'},
 {'ride_id': '4836736', 'driver_name': 'fenna'},
 {'ride_id': '4835996', 'driver_name': 'John Doe'},
 {'ride_id': '4836539', 'driver_name': 'emma'},
 {'ride_id': '4836715', 'driver_name': 'kriten'},
 {'ride_id': '4832141', 'driver_name': 'natalie'},
 {'ride_id': '4835792', 'driver_name': 'fred'},
 {'ride_id': '4836032', 'driver_name': 'croose'},
 {'ride_id': '4836728', 'driver_name': 'fenna'},
 {'ride_id': '4836410', 'driver_name': 'John Doe'},
 {'ride_id': '4836712', 'driver_name': 'emma'},
 {'ride_id': '4832131', 'driver_name': 'kriten'},
 {'ride_id': '4832064', 'driver_name': 'natalie'},
 {'ride_id': '4832106', 'driver_name': 'fred'},
 {'ride_id': '4835024', 'driver_name': 'croose'},
 {'ride_id': '4833262', 'driver_name': 'fenna'},
 {'ride_id': '4836701', 'driver_name': 'John Doe'},
 {'ride_id': '4835207', 'driver_name': 'emma'},
 {'ride_id': '4836680', 'driver_name': 'kriten'},
 {'ride_id': '4836371', 'driver_name': 'natalie'},
 {'ride_id': '4832070', 'driver_name': 'fred'},
 {'ride_id': '4836682', 'driver_name': 'croose'},
 {'ride_id': '4832080', 'driver_name': 'fenna'},
 {'ride_id': '4836733', 'driver_name': 'John Doe'},
 {'ride_id': '4836862', 'driver_name': 'emma'},
 {'ride_id': '4832071', 'driver_name': 'kriten'},
 {'ride_id': '4832118', 'driver_name': 'natalie'},
 {'ride_id': '4825520', 'driver_name': 'fred'},
 {'ride_id': '4833188', 'driver_name': 'croose'},
 {'ride_id': '4834471', 'driver_name': 'fenna'},
 {'ride_id': '4834621', 'driver_name': 'John Doe'},
 {'ride_id': '4836685', 'driver_name': 'emma'},
 {'ride_id': '4836367', 'driver_name': 'kriten'},
 {'ride_id': '4832137', 'driver_name': 'natalie'},
 {'ride_id': '4834876', 'driver_name': 'fred'},
 {'ride_id': '4835736', 'driver_name': 'croose'},
 {'ride_id': '4836489', 'driver_name': 'fenna'},
 {'ride_id': '4836341', 'driver_name': 'John Doe'},
 {'ride_id': '4835300', 'driver_name': 'emma'},
 {'ride_id': '4829379', 'driver_name': 'kriten'},
 {'ride_id': '4832120', 'driver_name': 'natalie'},
 {'ride_id': '4836550', 'driver_name': 'fred'},
 {'ride_id': '4836358', 'driver_name': 'croose'},
 {'ride_id': '4836735', 'driver_name': 'fenna'},
 {'ride_id': '4836384', 'driver_name': 'John Doe'},
 {'ride_id': '4836973', 'driver_name': 'emma'},
 {'ride_id': '4836115', 'driver_name': 'kriten'},
 {'ride_id': '4829374', 'driver_name': 'natalie'},
 {'ride_id': '4835148', 'driver_name': 'fred'},
 {'ride_id': '4836409', 'driver_name': 'croose'},
 {'ride_id': '4835021', 'driver_name': 'fenna'},
 {'ride_id': '4834874', 'driver_name': 'John Doe'},
 {'ride_id': '4836963', 'driver_name': 'emma'},
 {'ride_id': '4836850', 'driver_name': 'kriten'},
 {'ride_id': '4836953', 'driver_name': 'natalie'},
 {'ride_id': '4836961', 'driver_name': 'fred'},
 {'ride_id': '4836958', 'driver_name': 'croose'},
 {'ride_id': '4836957', 'driver_name': 'fenna'},
 {'ride_id': '4836906', 'driver_name': 'John Doe'},
 {'ride_id': '4832041', 'driver_name': 'emma'},
 {'ride_id': '4836401', 'driver_name': 'kriten'},
 {'ride_id': '4829371', 'driver_name': 'natalie'},
 {'ride_id': '4836929', 'driver_name': 'fred'},
 {'ride_id': '4836889', 'driver_name': 'croose'},
 {'ride_id': '4836443', 'driver_name': 'fenna'},
 {'ride_id': '4826071', 'driver_name': 'John Doe'},
 {'ride_id': '4835452', 'driver_name': 'emma'},
 {'ride_id': '4836360', 'driver_name': 'kriten'},
 {'ride_id': '4836514', 'driver_name': 'natalie'},
 {'ride_id': '4836405', 'driver_name': 'fred'},
 {'ride_id': '4836345', 'driver_name': 'croose'},
 {'ride_id': '4835985', 'driver_name': 'fenna'},
 {'ride_id': '4836970', 'driver_name': 'John Doe'},
 {'ride_id': '4836877', 'driver_name': 'emma'},
 {'ride_id': '4836954', 'driver_name': 'kriten'},
 {'ride_id': '4836538', 'driver_name': 'natalie'},
 {'ride_id': '4836364', 'driver_name': 'fred'},
 {'ride_id': '4836988', 'driver_name': 'croose'},
 {'ride_id': '4836959', 'driver_name': 'fenna'},
 {'ride_id': '4832107', 'driver_name': 'John Doe'},
 {'ride_id': '4837003', 'driver_name': 'emma'},
 {'ride_id': '4836962', 'driver_name': 'kriten'},
 {'ride_id': '4836968', 'driver_name': 'natalie'},
 {'ride_id': '4836951', 'driver_name': 'fred'},
 {'ride_id': '4836385', 'driver_name': 'croose'},
 {'ride_id': '4836796', 'driver_name': 'fenna'},
 {'ride_id': '4836540', 'driver_name': 'John Doe'},
 {'ride_id': '4836956', 'driver_name': 'emma'},
 {'ride_id': '4836981', 'driver_name': 'kriten'},
 {'ride_id': '4836982', 'driver_name': 'natalie'},
 {'ride_id': '4836490', 'driver_name': 'fred'},
 {'ride_id': '4836967', 'driver_name': 'croose'},
 {'ride_id': '4835905', 'driver_name': 'fenna'},
 {'ride_id': '4829376', 'driver_name': 'John Doe'},
 {'ride_id': '4837004', 'driver_name': 'emma'},
 {'ride_id': '4836990', 'driver_name': 'kriten'},
 {'ride_id': '4825519', 'driver_name': 'natalie'},
 {'ride_id': '4836969', 'driver_name': 'fred'},
 {'ride_id': '4836342', 'driver_name': 'croose'},
 {'ride_id': '4836491', 'driver_name': 'fenna'},
 {'ride_id': '4836426', 'driver_name': 'John Doe'},
 {'ride_id': '4837017', 'driver_name': 'emma'},
 {'ride_id': '4832119', 'driver_name': 'kriten'},
 {'ride_id': '4836344', 'driver_name': 'natalie'},
 {'ride_id': '4836994', 'driver_name': 'fred'},
 {'ride_id': '4836976', 'driver_name': 'croose'},
 {'ride_id': '4837008', 'driver_name': 'fenna'},
 {'ride_id': '4836536', 'driver_name': 'John Doe'},
 {'ride_id': '4832081', 'driver_name': 'emma'},
 {'ride_id': '4837034', 'driver_name': 'kriten'},
 {'ride_id': '4836402', 'driver_name': 'natalie'},
 {'ride_id': '4836779', 'driver_name': 'fred'},
 {'ride_id': '4836955', 'driver_name': 'croose'},
 {'ride_id': '4836876', 'driver_name': 'fenna'},
 {'ride_id': '4836435', 'driver_name': 'John Doe'},
 {'ride_id': '4836343', 'driver_name': 'emma'},
 {'ride_id': '4832901', 'driver_name': 'kriten'},
 {'ride_id': '4834474', 'driver_name': 'natalie'}]

combined_trips = [{'ride_id': ['4832077', '4832084'], 'driver_name': 'fenna'},
{'ride_id': ['4832085', '4832091'], 'driver_name': 'fenna'},
{'ride_id': ['4836234', '4834709'], 'driver_name': 'fenna'},
{'ride_id': ['4832072', '4832053'], 'driver_name': 'fenna'},
{'ride_id': ['4832052', '4832062'], 'driver_name': 'fenna'},
{'ride_id': ['4832089', '4832075'], 'driver_name': 'fenna'},
{'ride_id': ['4828927', '4832136'], 'driver_name': 'fenna'},
{'ride_id': ['4832133', '4833213'], 'driver_name': 'fenna'},
{'ride_id': ['4832076', '4832063'], 'driver_name': 'fenna'},
{'ride_id': ['4828958', '4832073'], 'driver_name': 'fenna'},
{'ride_id': ['4832123', '4832049'], 'driver_name': 'fenna'},
{'ride_id': ['4808802', '4834875'], 'driver_name': 'fenna'},
{'ride_id': ['4832077', '4832084'], 'driver_name': 'fenna'},
 {'ride_id': ['4832085', '4832091'], 'driver_name': 'fenna'},
 {'ride_id': ['4836234', '4834709'], 'driver_name': 'fenna'},
 {'ride_id': ['4832072', '4832053'], 'driver_name': 'fenna'},
 {'ride_id': ['4832052', '4832062'], 'driver_name': 'fenna'},
 {'ride_id': ['4832089', '4832075'], 'driver_name': 'fenna'},
 {'ride_id': ['4828927', '4832136'], 'driver_name': 'fenna'},
 {'ride_id': ['4832133', '4833213'], 'driver_name': 'fenna'},
 {'ride_id': ['4832076', '4832063'], 'driver_name': 'fenna'},
 {'ride_id': ['4828958', '4832073'], 'driver_name': 'fenna'},
 {'ride_id': ['4832123', '4832049'], 'driver_name': 'fenna'},
 {'ride_id': ['4808802', '4834875'], 'driver_name': 'fenna'},
 {'ride_id': ['4832061', '4832046'], 'driver_name': 'John Doe'},
 {'ride_id': ['4832051', '4832128'], 'driver_name': 'emma'},
 {'ride_id': ['4835997', '4832101'], 'driver_name': 'kriten'},
 {'ride_id': ['4835984', '4836019'], 'driver_name': 'natalie'},
 {'ride_id': ['4832124', '4832135'], 'driver_name': 'fred'},
 {'ride_id': ['4832121', '4833494'], 'driver_name': 'croose'},
 {'ride_id': ['4832057', '4832045'], 'driver_name': 'fenna'},
 {'ride_id': ['4832088', '4832058'], 'driver_name': 'John Doe'},
 {'ride_id': ['4834470', '4836018'], 'driver_name': 'emma'},
 {'ride_id': ['4836897', '4836535'], 'driver_name': 'kriten'},
 {'ride_id': ['4832114', '4836388'], 'driver_name': 'natalie'},
 {'ride_id': ['4831975', '4829378'], 'driver_name': 'fred'},
 {'ride_id': ['4836991', '4832134'], 'driver_name': 'croose'},
 {'ride_id': ['4833431', '4832900'], 'driver_name': 'fenna'},
 {'ride_id': ['4830361', '4833438'], 'driver_name': 'John Doe'},
 {'ride_id': ['4835770', '4835774'], 'driver_name': 'emma'},
 {'ride_id': ['4836977', '4836971'], 'driver_name': 'kriten'},
 {'ride_id': ['4832127', '4836975'], 'driver_name': 'natalie'},
 {'ride_id': ['4836983', '4836989'], 'driver_name': 'fred'},
 {'ride_id': ['4836974', '4836987'], 'driver_name': 'croose'},
 {'ride_id': ['4832060', '4832888'], 'driver_name': 'fenna'},
 {'ride_id': ['4836979', '4836986'], 'driver_name': 'John Doe'},
 {'ride_id': ['4834472', '4834473'], 'driver_name': 'emma'}]

def convert_objectid(item):
    if isinstance(item, dict):
        return {k: convert_objectid(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [convert_objectid(i) for i in item]
    elif isinstance(item, ObjectId):
        return str(item)
    else:
        return item

def fetch_ride_details():
    with open("merged_rides.json", "r") as file:
        rides = json.load(file)
    
    extracted_rides = []
    for ride in rides:
        extracted_rides.append({
            "ID": ride.get("ID"),
            "Pickup_Location": ride.get("Pickup_Location"),
            "Pickup_Coordinates": ride.get("Pickup_Coordinates"),
            "Dropoff_Location": ride.get("Dropoff_Location"),
            "Dropoff_Coordinates": ride.get("Dropoff_Coordinates"),
            "No of Passengers": ride.get("Passengers"),
            "Start Time": ride.get("Scheduled_Start_Time"),
        })
    return extracted_rides

def get_coordinates_for_assigned_trips():
    # Fetch all ride details without limit
    with open("merged_rides.json", "r") as file:
        rides = json.load(file)
    
    # Create a dictionary for quick lookup by ID
    rides_dict = {str(ride.get("ID")): ride for ride in rides}
    
    # Process normal assigned trips
    normal_trips_with_coords = []
    for trip in normal_assigned_trips:
        ride_id = trip['ride_id']
        if ride_id in rides_dict:
            ride_info = rides_dict[ride_id]
            normal_trips_with_coords.append({
                'driver_name': trip['driver_name'],
                'ride_id': ride_id,
                'Pickup_Coordinates': ride_info.get('Pickup_Coordinates'),
                'Dropoff_Coordinates': ride_info.get('Dropoff_Coordinates'),
                'Pickup_Location': ride_info.get('Pickup_Location'),
                'Dropoff_Location': ride_info.get('Dropoff_Location'),
                'Passengers': ride_info.get('Passengers'),
                'Start Time': ride_info.get('Scheduled_Start_Time'),
                'Type': 'Single Ride'
            })
    
    # Process combined trips
    combined_trips_with_coords = []
    for trip in combined_trips:
        for ride_id in trip['ride_id']:
            if ride_id in rides_dict:
                ride_info = rides_dict[ride_id]
                combined_trips_with_coords.append({
                    'driver_name': trip['driver_name'],
                    'ride_id': ride_id,
                    'Pickup_Coordinates': ride_info.get('Pickup_Coordinates'),
                    'Dropoff_Coordinates': ride_info.get('Dropoff_Coordinates'),
                    'Pickup_Location': ride_info.get('Pickup_Location'),
                    'Dropoff_Location': ride_info.get('Dropoff_Location'),
                    'Passengers': ride_info.get('Passengers'),
                    'Start Time': ride_info.get('Scheduled_Start_Time'),
                    'Type': 'Combined Ride'
                })
    
    return normal_trips_with_coords, combined_trips_with_coords

def get_start_time(ride_id, rides):
    ride_id = int(ride_id)  # Ensure type consistency
    for ride in rides:
        if int(ride["ID"]) == ride_id:
            return ride["Start Time"]
    return None

def display_ride_timeline():
    rides = fetch_ride_details()
    data = []
    
    for trip in normal_assigned_trips:
        start_time = get_start_time(trip['ride_id'], rides)
        if start_time:
            data.append({"Driver": trip['driver_name'], "Time": start_time, "Type": "Single Ride"})
    
    for trip in combined_trips:
        for ride_id in trip['ride_id']:
            start_time = get_start_time(ride_id, rides)
            if start_time:
                data.append({"Driver": trip['driver_name'], "Time": start_time, "Type": "Combined Ride"})
    
    if not data:
        st.warning("No valid ride assignments found.")
        return
    
    df = pd.DataFrame(data)

    if df.empty or "Time" not in df.columns:
        st.warning("Time column is missing or empty in DataFrame.")
        return

    fig = px.scatter(df, x='Time', y='Driver', color='Type',
                     title='Ride Assignments Timeline',
                     labels={'Time': 'Time', 'Driver': 'Driver ID'},
                     color_discrete_map={"Single Ride": "blue", "Combined Ride": "green"})
    st.plotly_chart(fig)
    
def get_all_drivers():
    driver_names = set()
    for trip in normal_assigned_trips:
        driver_names.add(trip['driver_name'])
    for trip in combined_trips:
        driver_names.add(trip['driver_name'])
    return sorted(list(driver_names))

def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

def display_driver_map(driver_name, trips_data):
    if not trips_data:
        st.info("No trip data available to display on map")
        return
    
    # Initialize the map with the first trip's pickup location
    first_trip = trips_data[0]
    pickup_coords = first_trip.get("Pickup_Coordinates")
    if not pickup_coords:
        st.warning("Coordinates not available for mapping")
        return
    
    m = folium.Map(location=pickup_coords, zoom_start=12)
    
    # Add each trip to the map
    for trip in trips_data:
        pickup_coords = trip.get("Pickup_Coordinates")
        dropoff_coords = trip.get("Dropoff_Coordinates")
        ride_id = trip.get("ride_id")
        
        if not pickup_coords or not dropoff_coords:
            continue
        
        # Generate a unique color for this trip
        color = generate_random_color()
        
        # Add pickup marker
        folium.Marker(
            location=pickup_coords,
            popup=f"Pickup: {trip.get('Pickup_Location')}<br>Ride ID: {ride_id}",
            icon=folium.Icon(color='green')
        ).add_to(m)
        
        # Add dropoff marker
        folium.Marker(
            location=dropoff_coords,
            popup=f"Dropoff: {trip.get('Dropoff_Location')}<br>Ride ID: {ride_id}",
            icon=folium.Icon(color='red')
        ).add_to(m)
        
        # Add a line connecting pickup to dropoff
        folium.PolyLine(
            locations=[pickup_coords, dropoff_coords],
            color=color,
            weight=3,
            opacity=0.7,
            popup=f"Ride ID: {ride_id}<br>Passengers: {trip.get('Passengers')}<br>Type: {trip.get('Type')}"
        ).add_to(m)
    
    # Display the map
    st.subheader(f"Trip Map for {driver_name}")
    folium_static(m)

def display_trip_tables():
    rides = fetch_ride_details()
    
    # For normal assigned trips
    normal_trips_data = []
    for trip in normal_assigned_trips:
        for ride in rides:
            if str(ride["ID"]) == trip['ride_id']:
                normal_trips_data.append({
                    "Driver": trip['driver_name'],
                    "Ride ID": ride["ID"],
                    "Pickup Location": ride["Pickup_Location"],
                    "Dropoff Location": ride["Dropoff_Location"],
                    "Passengers": ride["No of Passengers"]
                })
                break
    
    # For combined trips
    combined_trips_data = []
    for trip in combined_trips:
        for ride_id in trip['ride_id']:
            for ride in rides:
                if str(ride["ID"]) == ride_id:
                    combined_trips_data.append({
                        "Driver": trip['driver_name'],
                        "Ride ID": ride["ID"],
                        "Pickup Location": ride["Pickup_Location"],
                        "Dropoff Location": ride["Dropoff_Location"],
                        "Passengers": ride["No of Passengers"]
                    })
                    break
    
    st.subheader("Normal Assigned Trips")
    if normal_trips_data:
        normal_df = pd.DataFrame(normal_trips_data)
        st.dataframe(normal_df)
    else:
        st.info("No normal assigned trips found.")
    
    st.subheader("Combined Assigned Trips")
    if combined_trips_data:
        combined_df = pd.DataFrame(combined_trips_data)
        st.dataframe(combined_df)
    else:
        st.info("No combined trips found.")

def display_trips_by_driver():
    # Get list of all drivers
    drivers = get_all_drivers()
    
    # Create dropdown for driver selection
    selected_driver = st.selectbox("Select a driver", drivers)
    
    # Get all trips with coordinates
    normal_trips_with_coords, combined_trips_with_coords = get_coordinates_for_assigned_trips()
    
    # Filter for the selected driver
    normal_driver_trips = [trip for trip in normal_trips_with_coords if trip['driver_name'] == selected_driver]
    combined_driver_trips = [trip for trip in combined_trips_with_coords if trip['driver_name'] == selected_driver]
    
    # Combine both types of trips
    all_driver_trips = normal_driver_trips + combined_driver_trips
    
    if all_driver_trips:
        # Display map first
        display_driver_map(selected_driver, all_driver_trips)
        
        # Then display table of trips
        st.subheader(f"All trips for {selected_driver}")
        # Remove coordinate columns for display
        display_trips = [{k: v for k, v in trip.items() if k not in ['Pickup_Coordinates', 'Dropoff_Coordinates']} 
                         for trip in all_driver_trips]
        trips_df = pd.DataFrame(display_trips)
        st.dataframe(trips_df)
        
        # Summary metrics
        total_trips = len(all_driver_trips)
        total_passengers = sum(int(trip.get("Passengers", 0)) for trip in all_driver_trips)
        normal_count = len(normal_driver_trips)
        combined_count = len(combined_driver_trips)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trips", total_trips)
        with col2:
            st.metric("Total Passengers", total_passengers)
        with col3:
            st.metric("Normal Trips", normal_count)
        with col4:
            st.metric("Combined Trips", combined_count)
    else:
        st.info(f"No trips found for {selected_driver}")

def calculate_travel_time(origin: tuple, destination: tuple) -> int:
    try:
        distance = geodesic(origin, destination).kilometers
        time_hours = (distance / 30) * 1.2
        return math.ceil(time_hours * 60)
    except Exception as e:
        print(f"Error calculating travel time for {origin} -> {destination}: {str(e)}")
        return None

def get_eta_for_rides(rides):
    eta_results = []
    for ride in rides:
        ride_id = ride.get("ID")
        pickup_coords = ride.get("Pickup_Coordinates")
        dropoff_coords = ride.get("Dropoff_Coordinates")
        
        if isinstance(pickup_coords, list) and len(pickup_coords) == 2 and \
           isinstance(dropoff_coords, list) and len(dropoff_coords) == 2:
            origin = tuple(pickup_coords)
            destination = tuple(dropoff_coords)
            eta = calculate_travel_time(origin, destination)
            ride["ETA (mins)"] = eta
            eta_results.append(ride)
        else:
            print(f"Skipping ride ID {ride_id} due to missing coordinates.")
    return eta_results

# def mongo_to_pandas(mongo_docs):
#     for doc in mongo_docs:
#         if '_id' in doc:
#             doc['_id'] = str(doc['_id'])
#     return mongo_docs 

def get_all_drivers_with_vehicles():
    collection = db['drivers']
    drivers = list(collection.find({}))
    
    for driver in drivers:
        vehicle = db['vehicles'].find_one({"vehicle_number": driver['vehicle_number']}, {"_id": 0, "vehicle_number": 0})
        driver['vehicle'] = vehicle
    
    return drivers

def display_paginated_table(data, key, title):
    st.write(title)
    converted_data = convert_objectid(data)
    
    page_size = 10
    total_pages = (len(converted_data) + page_size - 1) // page_size
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, key=key)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    df = pd.DataFrame(converted_data[start_idx:end_idx])
    st.table(df)

def display_dashboard_summary():
    driver_count = len(get_all_drivers_with_vehicles())
    total_trips = len(normal_assigned_trips) + sum(len(trip['ride_id']) for trip in combined_trips)
    combined_trip_count = len(combined_trips)
    total_passengers = sum(trip.get("No of Passengers", 0) for trip in fetch_ride_details())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Drivers", value=driver_count)
    with col2:
        st.metric(label="Trips", value=total_trips)
    with col3:
        st.metric(label="Combined Trips", value=combined_trip_count)
    with col4:
        st.metric(label="Total Passengers", value=total_passengers)

def display_all_trips_map():
    normal_trips_with_coords, combined_trips_with_coords = get_coordinates_for_assigned_trips()
    all_trips = normal_trips_with_coords + combined_trips_with_coords
    
    if not all_trips:
        st.info("No trip data available to display on map")
        return
    
    # Get the center coordinates (average of all coordinates)
    all_pickup_coords = [trip.get("Pickup_Coordinates") for trip in all_trips if trip.get("Pickup_Coordinates")]
    if not all_pickup_coords:
        st.warning("No valid pickup coordinates found")
        return
    
    center_lat = sum(coords[0] for coords in all_pickup_coords) / len(all_pickup_coords)
    center_lng = sum(coords[1] for coords in all_pickup_coords) / len(all_pickup_coords)
    
    m = folium.Map(location=[center_lat, center_lng], zoom_start=10)
    
    # Create a dictionary to group trips by driver
    driver_trips = {}
    for trip in all_trips:
        driver_name = trip.get("driver_name")
        if driver_name not in driver_trips:
            driver_trips[driver_name] = []
        driver_trips[driver_name].append(trip)
    
    # Assign a consistent color for each driver
    driver_colors = {driver: generate_random_color() for driver in driver_trips.keys()}
    
    # Add trips to the map, grouped by driver
    for driver_name, trips in driver_trips.items():
        color = driver_colors[driver_name]
        for trip in trips:
            pickup_coords = trip.get("Pickup_Coordinates")
            dropoff_coords = trip.get("Dropoff_Coordinates")
            ride_id = trip.get("ride_id")
            
            if not pickup_coords or not dropoff_coords:
                continue
            
            # Add pickup marker
            folium.Marker(
                location=pickup_coords,
                popup=f"Driver: {driver_name}<br>Pickup: {trip.get('Pickup_Location')}<br>Ride ID: {ride_id}",
                icon=folium.Icon(color='green')
            ).add_to(m)
            
            # Add dropoff marker
            folium.Marker(
                location=dropoff_coords,
                popup=f"Driver: {driver_name}<br>Dropoff: {trip.get('Dropoff_Location')}<br>Ride ID: {ride_id}",
                icon=folium.Icon(color='red')
            ).add_to(m)
            
            # Add a line connecting pickup to dropoff
            folium.PolyLine(
                locations=[pickup_coords, dropoff_coords],
                color=color,
                weight=3,
                opacity=0.7,
                popup=f"Driver: {driver_name}<br>Ride ID: {ride_id}<br>Type: {trip.get('Type')}"
            ).add_to(m)
    
    # Add a legend for driver colors
    legend_html = '''
         <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    border:2px solid grey; z-index:9999; 
                    font-size:14px; background-color:white;
                    padding: 10px;
                    opacity: 0.8;">
         <p><strong>Drivers</strong></p>
    '''
    for driver, color in driver_colors.items():
        legend_html += f'<p><i style="background:{color};width:15px;height:15px;display:inline-block;"></i> {driver}</p>'
    legend_html += '</div>'
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Display the map
    st.subheader("All Trips Map")
    folium_static(m)

def main():
    st.title("AI Taxi Ride Planning")
    
    if st.button("Process"):
        st.session_state["rides"] = fetch_ride_details()
    
    if "rides" in st.session_state:
        display_paginated_table(st.session_state["rides"], "rides_page", "Processed Rides")
        
    if st.button("Calculate ETA"):
        st.session_state["rides_with_eta"] = get_eta_for_rides(st.session_state["rides"])
    
    if "rides_with_eta" in st.session_state:
        display_paginated_table(st.session_state["rides_with_eta"], "eta_page", "Rides with ETA")
    
    if st.button("Load Drivers"):
        st.session_state["drivers"] = get_all_drivers_with_vehicles()
    
    if "drivers" in st.session_state:
        display_paginated_table(st.session_state["drivers"], "drivers_page", "Available Drivers")
    
    if st.button("Schedule"):
        st.session_state["show_dashboard"] = True
    
    if st.session_state.get("show_dashboard", False):
        tabs = st.tabs(["Dashboard Summary", "Ride Timeline", "All Trips", "Driver Trips"])
        
        with tabs[0]:
            display_dashboard_summary()
        
        with tabs[1]:
            display_ride_timeline()
        
        with tabs[2]:
            display_trip_tables()
        
        with tabs[3]:
            display_trips_by_driver()

if __name__ == "__main__":
    main()
