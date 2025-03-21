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

normal_assigned_trips = [{'ride_id': "4855782", 'driver_name': 'B. de Wit'},
 {'ride_id': "4855966", 'driver_name': 'B. de Wit'},
 {'ride_id': "4856020", 'driver_name': 'B. de Wit'},
 {'ride_id': "4852241", 'driver_name': 'M. El Haddad'},
 {'ride_id': "4855985", 'driver_name': 'M. El Haddad'},
 {'ride_id': "4855949", 'driver_name': 'M. El Haddad'},
 {'ride_id': "4855937", 'driver_name': 'M. El Haddad'},
 {'ride_id': "4855991", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860768", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861034", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855964", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855986", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855957", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855974", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855963", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855972", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855995", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860444", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856010", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855960", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855980", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855989", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856040", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855979", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859130", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861027", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4858858", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855946", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855988", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855961", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4858724", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860002", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859911", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855999", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4852194", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856009", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856024", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860798", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860534", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855971", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856012", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855969", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859068", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856005", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855983", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855984", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859507", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859547", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859063", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856001", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861056", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860782", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855143", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860443", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856234", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4853947", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860650", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4858659", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856038", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860966", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860087", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861094", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859976", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861283", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859639", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860531", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861100", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861297", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861328", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860020", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861327", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861039", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861064", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861037", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861084", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861280", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861289", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861338", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861082", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861070", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861102", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855981", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860811", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861063", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861346", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861057", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861340", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856178", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860957", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861030", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861061", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860976", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861353", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859546", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4853939", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4856011", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859913", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4855943", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4859627", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861332", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4852637", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861058", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861278", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861312", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861092", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861266", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860783", 'driver_name': 'N. Nico'},
 {'ride_id': "4861292", 'driver_name': 'N. Margania'},
 {'ride_id': "4861300", 'driver_name': 'N. El Khannoussi'},
 {'ride_id': "4860822", 'driver_name': 'F. Abdoelhak'},
 {'ride_id': "4861060", 'driver_name': 'M. Assen'},
 {'ride_id': "4861277", 'driver_name': 'T. Ekkelboom'},
 {'ride_id': "4861041", 'driver_name': 'O. Idrissi'},
 {'ride_id': "4861324", 'driver_name': 'G. de Wit'},
 {'ride_id': "4861029", 'driver_name': 'R. taxi Service'},
 {'ride_id': "4861382", 'driver_name': 'M. Bourret'},
 {'ride_id': "4847214", 'driver_name': 'R. Bona'},
 {'ride_id': "4853945", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4856036", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4848016", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4861294", 'driver_name': 'C. Versnick'},
 {'ride_id': "4861071", 'driver_name': 'H. Kemner'},
 {'ride_id': "4860403", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861295", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4860450", 'driver_name': 'E. Maas'},
 {'ride_id': "4861321", 'driver_name': 'F. Jansen'},
 {'ride_id': "4856023", 'driver_name': 'G. van der Woude'},
 {'ride_id': "4850591", 'driver_name': 'J. van der Hoorn'},
 {'ride_id': "4861285", 'driver_name': 'Z. Al Habib'},
 {'ride_id': "4861366", 'driver_name': 'R. Paulussen'},
 {'ride_id': "4861330", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861303", 'driver_name': 'R. Teo'},
 {'ride_id': "4861298", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4861293", 'driver_name': 'A. Scholte'},
 {'ride_id': "4860978", 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': "4861097", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4861279", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4855962", 'driver_name': 'C. Versnick'},
 {'ride_id': "4861311", 'driver_name': 'R. Bona'},
 {'ride_id': "4861317", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4856021", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4861296", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4861322", 'driver_name': 'F. Jansen'},
 {'ride_id': "4861274", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4860405", 'driver_name': 'H. Kemner'},
 {'ride_id': "4861055", 'driver_name': 'M. Assen'},
 {'ride_id': "4861275", 'driver_name': 'T. Ekkelboom'},
 {'ride_id': "4855998", 'driver_name': 'G. de Wit'},
 {'ride_id': "4861342", 'driver_name': 'R. taxi Service'},
 {'ride_id': "4861301", 'driver_name': 'M. Bourret'},
 {'ride_id': "4860278", 'driver_name': 'R. Bona'},
 {'ride_id': "4861302", 'driver_name': 'N. El Khannoussi'},
 {'ride_id': "4861339", 'driver_name': 'O. Idrissi'},
 {'ride_id': "4861286", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4861273", 'driver_name': 'B. Acolatse'},
 {'ride_id': "4861318", 'driver_name': 'R. Bona'},
 {'ride_id': "4861355", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4856248", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4861356", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4860810", 'driver_name': 'E. Maas'},
 {'ride_id': "4861065", 'driver_name': 'F. Jansen'},
 {'ride_id': "4861062", 'driver_name': 'G. van der Woude'},
 {'ride_id': "4860818", 'driver_name': 'J. van der Hoorn'},
 {'ride_id': "4861336", 'driver_name': 'Z. Al Habib'},
 {'ride_id': "4861307", 'driver_name': 'R. Paulussen'},
 {'ride_id': "4844900", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861364", 'driver_name': 'R. Teo'},
 {'ride_id': "4855970", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4861343", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861358", 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': "4851493", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4855996", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4859102", 'driver_name': 'C. Versnick'},
 {'ride_id': "4856025", 'driver_name': 'H. Kemner'},
 {'ride_id': "4851484", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4861362", 'driver_name': 'R. Bona'},
 {'ride_id': "4861337", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4856261", 'driver_name': 'E. Maas'},
 {'ride_id': "4861320", 'driver_name': 'F. Jansen'},
 {'ride_id': "4855944", 'driver_name': 'G. van der Woude'},
 {'ride_id': "4855954", 'driver_name': 'J. van der Hoorn'},
 {'ride_id': "4855940", 'driver_name': 'Z. Al Habib'},
 {'ride_id': "4855994", 'driver_name': 'R. Paulussen'},
 {'ride_id': "4856039", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4856027", 'driver_name': 'R. Teo'},
 {'ride_id': "4861270", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4860488", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861046", 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': "4860981", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4861333", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4861354", 'driver_name': 'C. Versnick'},
 {'ride_id': "4855987", 'driver_name': 'H. Kemner'},
 {'ride_id': "4856002", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4861367", 'driver_name': 'R. Bona'},
 {'ride_id': "4861365", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4855366", 'driver_name': 'E. Maas'},
 {'ride_id': "4861344", 'driver_name': 'F. Jansen'},
 {'ride_id': "4861345", 'driver_name': 'G. van der Woude'},
 {'ride_id': "4858765", 'driver_name': 'J. van der Hoorn'},
 {'ride_id': "4856007", 'driver_name': 'Z. Al Habib'},
 {'ride_id': "4861363", 'driver_name': 'R. Paulussen'},
 {'ride_id': "4858799", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4855936", 'driver_name': 'R. Teo'},
 {'ride_id': "4856017", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4861314", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861325", 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': "4854596", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4855976", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4856042", 'driver_name': 'C. Versnick'},
 {'ride_id': "4857047", 'driver_name': 'H. Kemner'},
 {'ride_id': "4858718", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4860088", 'driver_name': 'R. Bona'},
 {'ride_id': "4859885", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4860623", 'driver_name': 'E. Maas'},
 {'ride_id': "4856003", 'driver_name': 'F. Jansen'},
 {'ride_id': "4856014", 'driver_name': 'G. van der Woude'},
 {'ride_id': "4861348", 'driver_name': 'J. van der Hoorn'},
 {'ride_id': "4861093", 'driver_name': 'Z. Al Habib'},
 {'ride_id': "4855950", 'driver_name': 'R. Paulussen'},
 {'ride_id': "4856018", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4859043", 'driver_name': 'R. Teo'},
 {'ride_id': "4861407", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4848017", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861349", 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': "4856035", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4861319", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4860451", 'driver_name': 'C. Versnick'},
 {'ride_id': "4861326", 'driver_name': 'H. Kemner'},
 {'ride_id': "4855951", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4855977", 'driver_name': 'R. Bona'},
 {'ride_id': "4855953", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4856006", 'driver_name': 'E. Maas'},
 {'ride_id': "4855941", 'driver_name': 'F. Jansen'},
 {'ride_id': "4860983", 'driver_name': 'G. van der Woude'},
 {'ride_id': "4855992", 'driver_name': 'J. van der Hoorn'},
 {'ride_id': "4855982", 'driver_name': 'Z. Al Habib'},
 {'ride_id': "4860406", 'driver_name': 'R. Paulussen'},
 {'ride_id': "4861370", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861410", 'driver_name': 'R. Teo'},
 {'ride_id': "4855973", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4860835", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861053", 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': "4855959", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4856026", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4861099", 'driver_name': 'C. Versnick'},
 {'ride_id': "4861098", 'driver_name': 'H. Kemner'},
 {'ride_id': "4861400", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4858320", 'driver_name': 'R. Bona'},
 {'ride_id': "4856037", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4860007", 'driver_name': 'E. Maas'},
 {'ride_id': "4856000", 'driver_name': 'F. Jansen'},
 {'ride_id': "4860821", 'driver_name': 'G. van der Woude'},
 {'ride_id': "4847213", 'driver_name': 'J. van der Hoorn'},
 {'ride_id': "4861059", 'driver_name': 'Z. Al Habib'},
 {'ride_id': "4856016", 'driver_name': 'R. Paulussen'},
 {'ride_id': "4861412", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861117", 'driver_name': 'R. Teo'},
 {'ride_id': "4850592", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4855990", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861091", 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': "4855958", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4858798", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4861051", 'driver_name': 'C. Versnick'},
 {'ride_id': "4860956", 'driver_name': 'H. Kemner'},
 {'ride_id': "4860819", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4853940", 'driver_name': 'R. Bona'},
 {'ride_id': "4860771", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4855942", 'driver_name': 'E. Maas'},
 {'ride_id': "4861453", 'driver_name': 'F. Jansen'},
 {'ride_id': "4860834", 'driver_name': 'G. van der Woude'},
 {'ride_id': "4861054", 'driver_name': 'J. van der Hoorn'},
 {'ride_id': "4859104", 'driver_name': 'Z. Al Habib'},
 {'ride_id': "4860980", 'driver_name': 'R. Paulussen'},
 {'ride_id': "4860006", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4860472", 'driver_name': 'R. Teo'},
 {'ride_id': "4859628", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4860456", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861368", 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': "4861374", 'driver_name': 'T. Staphorst'},
 {'ride_id': "4861116", 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': "4861415", 'driver_name': 'C. Versnick'},
 {'ride_id': "4861313", 'driver_name': 'H. Kemner'},
 {'ride_id': "4861422", 'driver_name': 'E. van der Steeg'},
 {'ride_id': "4861416", 'driver_name': 'R. Bona'},
 {'ride_id': "4861417", 'driver_name': 'D. Teo Kalf'},
 {'ride_id': "4861506", 'driver_name': 'E. Maas'},
 {'ride_id': "4855965", 'driver_name': 'F. Jansen'},
{'ride_id': "4861369", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861471", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4861038", 'driver_name': 'O. Idrissi'},
 {'ride_id': "4861457", 'driver_name': 'M. Bourret'},
 {'ride_id': "4861042", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861492", 'driver_name': 'M. Bourret'},
 {'ride_id': "4861435", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861495", 'driver_name': 'R. Teo'},
 {'ride_id': "4853943", 'driver_name': 'R. Teo'},
 {'ride_id': "4861475", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4861470", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4855993", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4859632", 'driver_name': 'M. Bourret'},
 {'ride_id': "4861437", 'driver_name': 'A. Scholte'},
 {'ride_id': "4861088", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861040", 'driver_name': 'O. Idrissi'},
 {'ride_id': "4861036", 'driver_name': 'O. Idrissi'},
 {'ride_id': "4861494", 'driver_name': 'R. Teo'},
 {'ride_id': "4861423", 'driver_name': 'A. Scholte'},
 {'ride_id': "4853941", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4853948", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861491", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4861434", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861439", 'driver_name': 'A. Scholte'},
 {'ride_id': "4860689", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861477", 'driver_name': 'R. Teo'},
 {'ride_id': "4861473", 'driver_name': 'R. El Khattabi'},
 {'ride_id': "4861474", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861458", 'driver_name': 'M. Bourret'},
 {'ride_id': "4858321", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861482", 'driver_name': 'R. Teo'},
 {'ride_id': "4861469", 'driver_name': 'R. Teo'},
 {'ride_id': "4861503", 'driver_name': 'C. Messoudi'},
 {'ride_id': "4861535", 'driver_name': 'M. Bourret'},
 {'ride_id': "4853944", 'driver_name': 'R. Teo'}]


combined_trips = [
    {'ride_id': ["4850912", "4855948"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4855975", "4858332"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4856022", "4856008"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4855955", "4855947"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4855945", "4855968"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4856019", "4854458"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4855939", "4855978"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4855967", "4855952"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4856004", "4855938"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4860275", "4855956"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4856262", "4860489"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4844901", "4855997"], 'driver_name': 'M. El Haddad'},
 {'ride_id': ["4858760", "4860982"], 'driver_name': 'M. El Haddad'},
{'ride_id': ["4847214", "4861311"], 'driver_name': 'R. Bona'},
 {'ride_id': ["4856036", "4856248"], 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': ["4860403", "4860450"], 'driver_name': 'B. Acolatse'},
 {'ride_id': ["4860978", "4860818"], 'driver_name': 'M. Sprinkhuize'},
 {'ride_id': ["4861317", "4861318"], 'driver_name': 'E. van der Steeg'},
 {'ride_id': ["4856021", "4855970"], 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': ["4861274", "4861273"], 'driver_name': 'B. Acolatse'},
 {'ride_id': ["4861301", "4860278"], 'driver_name': 'M. Bourret'},
 {'ride_id': ["4861286", "4861364"], 'driver_name': 'E. van der Steeg'},
 {'ride_id': ["4861355", "4861354"], 'driver_name': 'E. van der Steeg'},
 {'ride_id': ["4861356", "4860810"], 'driver_name': 'D. Teo Kalf'},
 {'ride_id': ["4861336", "4861333"], 'driver_name': 'Z. Al Habib'},
 {'ride_id': ["4861307", "4861343"], 'driver_name': 'R. Paulussen'},
 {'ride_id': ["4844900", "4855996"], 'driver_name': 'C. Messoudi'},
 {'ride_id': ["4851493", "4851484"], 'driver_name': 'E. van der Steeg'},
 {'ride_id': ["4856025", "4855954"], 'driver_name': 'H. Kemner'},
 {'ride_id': ["4861337", "4860981"], 'driver_name': 'D. Teo Kalf'},
 {'ride_id': ["4856261", "4860488"], 'driver_name': 'E. Maas'},
 {'ride_id': ["4861320", "4861270"], 'driver_name': 'F. Jansen'},
 {'ride_id': ["4855944", "4855950"], 'driver_name': 'G. van der Woude'},
 {'ride_id': ["4855940", "4855987"], 'driver_name': 'R. Paulussen'},
 {'ride_id': ["4861367", "4861345"], 'driver_name': 'D. Teo Kalf'},
 {'ride_id': ["4861363", "4858718"], 'driver_name': 'R. Paulussen'},
 {'ride_id': ["4854596", "4857047"], 'driver_name': 'T. Staphorst'},
 {'ride_id': ["4855976", "4856042"], 'driver_name': 'X. Lion-Sjin-Tjoe'},
 {'ride_id': ["4856003", "4856014"], 'driver_name': 'F. Jansen'},
 {'ride_id': ["4861407", "4860406"], 'driver_name': 'R. El Khattabi'},
 {'ride_id': ["4855951", "4855982"], 'driver_name': 'E. van der Steeg'},
 {'ride_id': ["4855977", "4856006"], 'driver_name': 'R. Bona'},
{'ride_id': ["4861478", "4856041"], 'driver_name': 'A. Scholte'},
 {'ride_id': ["4861456", "4861472"], 'driver_name': 'A. Scholte'},
 {'ride_id': ["4861462", "4861476"], 'driver_name': 'A. Scholte'},
 {'ride_id': ["4861454", "4861483"], 'driver_name': 'A. Scholte'},
 {'ride_id': ["4856013", "4856015"], 'driver_name': 'C. Messoudi'}
 ]

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
        # Collect ride details for all rides in the combined trip
        combined_ride_details = []
        ride_id = []
        pickup_locations = []
        dropoff_locations = []
        total_passengers = 0
        
        for ride_id in trip['ride_id']:
            for ride in rides:
                if str(ride["ID"]) == ride_id:
                    ride_id.append(ride["ID"])
                    pickup_locations.append(ride["Pickup_Location"])
                    dropoff_locations.append(ride["Dropoff_Location"])
                    total_passengers += ride["No of Passengers"]
                    break
        
        # Create a single row for the combined trip
        combined_trips_data.append({
            "Driver": trip['driver_name'],
            "Ride IDs": ", ".join(map(str, ride_id)),
            "Pickup Locations": ", ".join(pickup_locations),
            "Dropoff Locations": ", ".join(dropoff_locations),
            "Total Passengers": total_passengers
        })
   
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
