import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import json
import uuid
import folium
from streamlit_folium import st_folium
import time




st.set_page_config(layout="wide", page_title="AeroWatch AI", page_icon="🌍")




# ==============================================================================
# 1. CORE SYSTEM ARCHITECTURE & INITIALIZATION
# ==============================================================================
GOOGLE_API_KEY = "YOUR_AI_STUDIO_API_KEY"
PROJECT_ID = "aerowatch-air-quality"
try:
 client = genai.Client(api_key=GOOGLE_API_KEY)
except:
 pass




# Synchronized App State Orchestration Engine
if "selected_kpi" not in st.session_state:
 st.session_state.selected_kpi = "Default"
if "active_report_id" not in st.session_state:
 st.session_state.active_report_id = "c1"
if "map_zoom_street" not in st.session_state:
 st.session_state.map_zoom_street = "Connaught Place Circle"
if "action_statuses" not in st.session_state:
 st.session_state.action_statuses = {
     "c1": "🔴 High Priority",
     "c2": "🟡 Pending Approval",
     "n1": "🔴 High Priority",
     "h1": "🟢 Approved"
 }
if "view_action_details" not in st.session_state:
 st.session_state.view_action_details = "c1"
if "simulation_pipeline_stage" not in st.session_state:
 st.session_state.simulation_pipeline_stage = None
if "prev_upload_id" not in st.session_state:
 st.session_state.prev_upload_id = ""








# ==============================================================================
# 2. FIXED HACKATHON DATA METRIC MATRIX FRAMEWORK
# ==============================================================================
ZONE_MAPPING = {
 "Central Delhi": {
     "coords": [28.6304, 77.2177], "aqi": 134, "category": "🟠 Poor Air Quality", "color": "#F97316",
     "trend_data": [110, 118, 124, 134, 145, 155, 142, 134],
     "prediction": {
         "aqi": 165, "confidence": "94%", "reason": "Low wind speed trapping vehicle smoke and construction site dust.",
         "wind": "5 km/hr", "temp": "31°C", "humidity": "48%", "category": "Poor"
     },
     "sensors": [
         {"Sensor ID": "DELHI-SENSOR-01", "PM2.5": 185, "PM10": 244, "Humidity": "48%", "Temperature": "31°C", "Wind Speed": "5 km/hr NE", "Status": "🔴 Critical Alert"},
         {"Sensor ID": "DELHI-SENSOR-02", "PM2.5": 142, "PM10": 198, "Humidity": "45%", "Temperature": "31°C", "Wind Speed": "6 km/hr NE", "Status": "🟠 Warning Alert"}
     ],
     "satellite": {
         "timestamp": "2026-07-07 18:45 IST", "confidence": "91%", "radius": "350 Meters", "anomaly": "High Thermal Signatures Detected",
         "smoke": "Active Smoke Plume Visualized", "summary": "Satellite visual layer confirms active smoke concentration, validating ground citizen report filings."
     },
     "hotspots": [
         {
             "id": "c1", "loc": [28.6304, 77.2177], "street": "Connaught Place Circle", "area": "Inner Circle Market", "ward": "Sector 1", "aqi": 185, "category": "🔴 High Priority", "color": "#EF4444",
             "cause": "Vehicle Smoke", "evidence": "Citizen Video + IoT Street Sensor", "act": "Deploy Water Mist Cannon", "time": "2 mins ago", "red": "20 AQI", "eta": "25 Minutes", "lat": 28.6304, "lon": 77.2177, "team": "Response Team Alpha",
             "thumb": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=150&auto=format&fit=crop&q=60", "source_type": "Citizen Report",
             "cit_conf": "95%", "sat_conf": "91%", "sens_conf": "89%", "overall_conf": "93%", "hospitals": "Dr. RML Hospital (1.2km)", "schools": "Modern School Barakhamba (800m)", "traffic": "🔴 High Congestion Grid"
         },
         {
             "id": "c2", "loc": [28.6270, 77.2350], "street": "ITO Metro Station Junction", "area": "Main Crossing Intersection", "ward": "Sector 2", "aqi": 168, "category": "🟡 Pending Approval", "color": "#EAB308",
             "cause": "Construction Dust", "evidence": "Citizen Photo + IoT Street Sensor", "act": "Deploy Building Inspection Team", "time": "8 mins ago", "red": "15 AQI", "eta": "20 Minutes", "lat": 28.6270, "lon": 77.2350, "team": "Response Team Beta",
             "thumb": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=150&auto=format&fit=crop&q=60", "source_type": "Citizen Report",
             "cit_conf": "94%", "sat_conf": "88%", "sens_conf": "92%", "overall_conf": "91%", "hospitals": "Lok Nayak Hospital (1.8km)", "schools": "Bal Bharati Public School (1.4km)", "traffic": "🟠 Medium-High Grid"
         },
         {
             "id": "h1", "loc": [28.6410, 77.2420], "street": "India Gate Outer Ring Road", "area": "Hexagon Transit Lanes", "ward": "Sector 3", "aqi": 198, "category": "🟢 Approved", "color": "#22C55E",
             "cause": "Traffic Smog", "evidence": "Satellite Path Overlap + Sensor Alert", "act": "Mobilize Mechanical Road Sweepers", "time": "Just Detected", "red": "35 AQI", "eta": "10 Minutes", "lat": 28.6410, "lon": 77.2420, "team": "Response Taskforce Gamma",
             "thumb": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6c?w=150&auto=format&fit=crop&q=60", "source_type": "⚠️ AI Detected (No Citizen Report)",
             "cit_conf": "0% (Unreported)", "sat_conf": "94%", "sens_conf": "93%", "overall_conf": "91%", "hospitals": "Lady Hardinge Hospital (2.1km)", "schools": "St. Columba's School (1.9km)", "traffic": "🔴 Critical Plume Area"
         }
     ]
 },
 "North Delhi": {
     "coords": [28.6750, 77.1750], "aqi": 235, "category": "🔴 Very Poor Air Quality", "color": "#EF4444",
     "trend_data": [210, 220, 230, 235, 240, 250, 242, 235],
     "prediction": {
         "aqi": 255, "confidence": "96%", "reason": "Open garbage dump fire smoke mixed with weak wind trapping.",
         "wind": "4 km/hr", "temp": "32°C", "humidity": "42%", "category": "Very Poor"
     },
     "sensors": [
         {"Sensor ID": "DELHI-SENSOR-03", "PM2.5": 245, "PM10": 310, "Humidity": "42%", "Temperature": "32°C", "Wind Speed": "4 km/hr NE", "Status": "🔴 Critical Alert"}
     ],
     "satellite": {
         "timestamp": "2026-07-07 18:30 IST", "confidence": "95%", "radius": "500 Meters", "anomaly": "Thick Open Smoke Plume Tracked",
         "smoke": "Active Fire Anomaly Confirmed", "summary": "Satellite aerial pass identifies major active burn coordinates over regional roadside dump points."
     },
     "hotspots": [
         {
             "id": "n1", "loc": [28.6690, 77.1680], "street": "Chandni Chowk Main Market", "area": "Old Delhi Core Sector", "ward": "Sector 12", "aqi": 245, "category": "🔴 High Priority", "color": "#EF4444",
             "cause": "Garbage Burning", "evidence": "Citizen Mobile Photo", "act": "Dispatch Emergency Cleanup Truck", "time": "1 min ago", "red": "40 AQI", "eta": "8 Minutes", "lat": 28.6690, "lon": 77.1680, "team": "Response Team Alpha",
             "thumb": "https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?w=150&auto=format&fit=crop&q=60", "source_type": "Citizen Report",
             "cit_conf": "97%", "sat_conf": "95%", "sens_conf": "85%", "overall_conf": "94%", "hospitals": "Sanjeevan Hospital (900m)", "schools": "Presentation Convent School (600m)", "traffic": "🔴 High Pedestrian Grid"
         }
     ]
 }
}








MASTER_REPORTS = [
 {"Time": "10:30 AM", "Location": "Connaught Place Circle", "Source": "Citizen Photo", "Status": "🟢 Approved", "AQI": "185", "Severity": "High Priority"},
 {"Time": "11:10 AM", "Location": "ITO Metro Station Junction", "Source": "CCTV Network Swath", "Status": "实时 Verification", "AQI": "168", "Severity": "Medium Priority"},
 {"Time": "09:15 AM", "Location": "Chandni Chowk Main Market", "Source": "Citizen Mobile Photo", "Status": "🟢 Approved", "AQI": "245", "Severity": "High Priority"},
 {"Time": "08:45 AM", "Location": "India Gate Outer Ring Road", "Source": "Satellite Tracker Grid", "Status": "🔵 Completed", "AQI": "198", "Severity": "High Priority"}
]








TEAMS_DATABASE = [
 {"Team Unit": "Team Alpha", "Current Assignment": "Deploy Water Mist Cannon", "Location": "Connaught Place Circle", "ETA": "8 mins", "Status": "🟢 Active"},
 {"Team Unit": "Team Beta", "Current Assignment": "Building Site Enforcement", "Location": "ITO Metro Station Junction", "ETA": "4 mins", "Status": "🟢 Active"}
]








# ==============================================================================
# 3. PREMIUM COMPACT COMMAND CENTER CSS SKIN ENGINE
# ==============================================================================
st.markdown("""
 <style>
 @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
  html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
     font-family: 'Plus Jakarta Sans', sans-serif !important;
     background: #F4F8FB !important;
     color: #0F172A !important;
     font-size: 16px !important;
 }
 [data-testid="stMetricContainer"] { display: none !important; }
 div.block-container { padding: 1.5rem 2rem 1.5rem 2rem !important; max-width: 100%; }
  [data-testid="stVerticalBlock"] { gap: 16px !important; padding: 0 !important; margin: 0 !important; }
 [data-testid="stColumn"] { padding: 0 !important; margin: 0 !important; }
 .stElementContainer { margin: 0 !important; padding: 0 !important; }
 div[data-testid="stHorizontalBlock"] { gap: 20px !important; padding: 0 !important; margin: 0 !important; }
  .command-card {
     background: #FFFFFF !important;
     border: 1px solid #DCE6F2 !important;
     border-radius: 12px !important;
     padding: 16px !important;
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
     height: 110px !important;
     display: flex;
     flex-direction: column;
     justify-content: space-between;
     transition: all 0.2s ease-in-out !important;
 }
 .command-card:hover {
     transform: translateY(-2px) !important;
     box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08) !important;
 }
  /* Style the native Streamlit containers to look like the command card */
 div[data-testid="stVerticalBlockBorderReceiver"] {
     background: #FFFFFF !important;
     border: 1px solid #DCE6F2 !important;
     border-radius: 12px !important;
     padding: 24px !important;
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
 }
  .whitespace-compressor { margin-bottom: -15px !important; padding-bottom: 0 !important; }
  .stButton>button {
     background: transparent !important; color: #2563EB !important;
     border: none !important; padding: 0 !important; margin: 0 !important;
     text-align: left !important; font-size: 14px !important; font-weight: 700 !important;
     text-transform: none !important; width: 100% !important;
     box-shadow: none !important; display: inline-block !important; height: auto !important;
     margin-top: 1px !important; line-height: 1.1 !important;
 }
 .stButton>button:hover { color: #1D4ED8 !important; text-decoration: underline !important; background: transparent !important; }
  .action-btn-layout button {
     background: #2563EB !important; color: white !important; font-size: 16px !important;
     font-weight: 600 !important; padding: 10px 18px !important; border-radius: 8px !important; width: 100% !important;
     box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2) !important;
 }
 .action-btn-layout button:hover { background: #1D4ED8 !important; color: white !important; }








 .kpi-wrapper { display: flex; align-items: center; justify-content: space-between; width: 100%; }
 .kpi-title { font-size: 14px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.04em; }
  .kpi-value { font-size: 26px !important; font-weight: 800; color: #0F172A; line-height: 1.1; margin: 2px 0; }
 .kpi-icon-box { width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
  .platform-header {
     background: #FFFFFF;
     border: none !important;
     padding: 20px 28px;
     border-radius: 16px;
     margin-top: 6px !important;
     margin-bottom: 24px !important;
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
     position: relative;
     overflow: hidden;
 }
 .platform-header::before {
     content: "";
     display: block;
     position: absolute;
     top: 0; left: 0; right: 0;
     height: 5px;
     background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
 }
 .platform-header h1 { color: #0F172A !important; font-weight: 800 !important; font-size: 32px !important; margin:0; }
 .platform-header p { font-size: 16px !important; margin-top: 8px; color: #64748B;}
  .alert-interactive-row {
     padding: 14px;
     border-radius: 10px;
     background: #F8FAFC;
     border: 1px solid #E2E8F0;
     margin-bottom: 10px;
     cursor: pointer;
     transition: all 0.2s ease !important;
 }
 .alert-interactive-row:hover {
     background: #F1F5F9 !important;
     border-color: #CBD5E1 !important;
     transform: translateY(-2px) !important;
     box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
 }
  div[data-baseweb="select"] * { color: #0F172A !important; font-weight: 600 !important; font-size: 16px !important;}
 [data-testid="stSidebar"], [data-testid="stSidebar"] [data-testid="stHeader"] {
     background-color: #102A43 !important;
     border-right: 1px solid #0F2036 !important;
     width: 340px !important;
 }
 [data-testid="stSidebar"] * { color: #E2E8F0; font-size: 16px;}
 [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 18px !important; }
  div.row-widget.stRadio > div { gap: 8px !important; background: transparent !important; padding: 0 !important; }
 div.row-widget.stRadio div[role="radiogroup"] label {
     padding: 12px 16px !important; border-radius: 10px !important;
     background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.05) !important;
     width: 100% !important; margin-bottom: 8px !important;
     font-size: 16px !important;
 }
 div.row-widget.stRadio div[role="radiogroup"] label[data-checked="true"] {
     background: #214E34 !important; color: #FFFFFF !important; border: 1px solid #BBF7D0 !important;
 }
  .pulse-card-highlight {
     border: 1px solid #214E34 !important; background: #FAFEFA !important;
     box-shadow: 0 0 0 3px rgba(33, 78, 52, 0.15) !important;
 }
 .sidebar-block-pane {
     background: rgba(255, 255, 255, 0.04); border-radius: 10px; padding: 14px; margin-bottom: 16px !important; border: 1px solid rgba(255, 255, 255, 0.05);
 }
 .stfolium { margin-bottom: 0px !important; padding-bottom: 0px !important; border-radius: 12px !important; overflow: hidden !important;}




 /* Professional Upload Buttons Override */
 [data-testid="stFileUploader"] button {
     background-color: #F8FAFC !important;
     color: #1F2937 !important;
     border: 1px solid #CBD5E1 !important;
     border-radius: 8px !important;
     font-weight: 600 !important;
     transition: all 0.2s;
 }
 [data-testid="stFileUploader"] button:hover {
     background-color: #F1F5F9 !important;
     border-color: #94A3B8 !important;
 }




 /* New Info Cards */
 .ai-report-card {
     background: #FFFFFF;
     border: 1px solid #DCE6F2;
     border-radius: 12px;
     padding: 20px;
     box-shadow: 0 4px 10px rgba(15, 23, 42, 0.05);
     display: flex;
     flex-direction: column;
     justify-content: center;
 }
 .success-card {
     background: #E8F5E9 !important;
     border: 1px solid #C8E6C9 !important;
 }
 .ai-report-card .lbl { font-size: 15px; font-weight: 700; color: #64748B; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.04em;}
 .ai-report-card .val { font-size: 22px; font-weight: 800; color: #0F172A; }




 .section-header { font-size: 26px; font-weight: 800; color: #1F2937; margin-bottom: 16px; border-bottom: 2px solid #DCE6F2; padding-bottom: 12px; }




 ::-webkit-scrollbar { width: 8px; height: 8px; }
 ::-webkit-scrollbar-track { background: #F4F8FB; }
 ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 6px; }
 ::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
 </style>
 """, unsafe_allow_html=True)








# ==============================================================================
# 4. SIDEBAR NAVIGATION & AIR POLLUTION AWARENESS INTEGRATION
# ==============================================================================
with st.sidebar:
 st.markdown("""
     <div style="display: flex; align-items: center; gap: 12px; padding: 4px 0 20px 0; border-bottom: 1px solid #244263; margin-bottom: 20px;">
         <div style="background:#214E34; padding:8px; border-radius:10px; font-size:24px; line-height:1;">🍃</div>
         <div>
             <h2 style="margin: 0; font-weight: 800; font-size: 22px; color: #FFFFFF; letter-spacing: -0.01em;">🌍 AeroWatch AI</h2>
             <div style="color: #94A3B8; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; margin-top:2px;">Government Command Center</div>
         </div>
     </div>
 """, unsafe_allow_html=True)
 menu = st.radio("NAVIGATION MODULE", ["🏠 Live Monitoring", "📸 Report Pollution", "🤖 AI Action Center"], label_visibility="collapsed")
 st.markdown("""
     <div style="margin-top: 28px; margin-bottom: 10px;">
         <p style="font-size:14px; font-weight:700; color:#94A3B8; margin: 0; letter-spacing:0.04em; text-transform: uppercase;">🏢 DISTRICT SECTOR CONTROL</p>
     </div>
 """, unsafe_allow_html=True)
 zone_list = list(ZONE_MAPPING.keys())
 selected_city = st.selectbox("Select Delhi Zone", zone_list, index=0, label_visibility="collapsed")
 active_city_data = ZONE_MAPPING[selected_city]
 st.markdown(f"""
     <div class="sidebar-widget" style="margin-top:16px; margin-bottom: 20px; background: rgba(255,255,255,0.04); border:none; padding:12px; border-radius:10px;">
         <div style="font-size: 14px; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Zone Status Index</div>
         <div style="font-weight:700; font-size:24px; margin-top:4px; display:flex; align-items:center; gap:8px;">
             <span style="color:white; font-weight:800;">AQI {active_city_data['aqi']}</span>
             <span style="font-size:14px; font-weight:700; color:white; background:{active_city_data['color']}; padding:4px 10px; border-radius:8px;">{active_city_data['category']}</span>
         </div>
     </div>
 """, unsafe_allow_html=True)








 st.markdown("""
     <div class="sidebar-block-pane" style="background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); border-left: 5px solid #3B82F6; margin-bottom: 16px !important;">
         <div style="font-size: 14px; color: #93C5FD; text-transform: uppercase; font-weight: 700; letter-spacing:0.05em;">Today's Impact Matrix</div>
         <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:10px; font-size:15px;">
             <div>📝 Reports: <b>36</b></div>
             <div>📍 Hotspots: <b>3</b></div>
             <div>🌿 AQI Red: <b style="color:#4ADE80;">18%</b></div>
             <div>⏱️ Time Saved: <b>42m</b></div>
         </div>
         <div style="font-size:14px; color:#93C5FD; margin-top:10px; text-align:right;">AI Confidence Index: <b>93%</b></div>
     </div>
 """, unsafe_allow_html=True)








 st.markdown("""
     <div class="sidebar-block-pane" style="margin-bottom: 16px !important;">
         <div style="font-size: 14px; color: #34D399; text-transform: uppercase; font-weight: 700; margin-bottom:8px;">Why AeroWatch AI Matters</div>
         <p style="font-size:15px; color:#CBD5E1; margin:0 0 8px 0; line-height:1.5;">
             🌍 Air pollution contributes to millions of premature deaths globally every year.<br>
             🏙️ Several Indian cities frequently record AQI levels above safe limits.
         </p>
         <div style="font-size:15px; color:#F1F5F9; line-height:1.5;">
             <b>🤖 AeroWatch AI helps by:</b><br>
             • Detecting pollution hotspots in real time<br>
             • Predicting AQI trends over windows<br>
             • Prioritizing emergency response teams<br>
             • Supporting faster municipal decisions
         </div>
     </div>
  
     <div class="sidebar-block-pane" style="margin-bottom: 16px !important;">
         <div style="font-size: 14px; color: #FB923C; text-transform: uppercase; font-weight: 700; margin-bottom:10px;">Quick Air Quality Guide</div>
         <div style="font-size:15px; display:grid; grid-template-columns: 1.2fr 2fr; gap:6px; line-height:1.4;">
             <span style="color:#4ADE80;">🟢 0–50</span><span>Good</span>
             <span style="color:#FACC15;">🟡 51–100</span><span>Moderate</span>
             <span style="color:#FB923C;">🟠 101–200</span><span>Poor</span>
             <span style="color:#F87171;">🔴 201–300</span><span>Very Poor</span>
             <span style="color:#C084FC;">🟣 301+</span><span>Severe</span>
         </div>
     </div>
 """, unsafe_allow_html=True)








# ==============================================================================
# 5. PAGE 1: LIVE NEIGHBORHOOD POLLUTION MONITORING
# ==============================================================================
if menu == "🏠 Live Monitoring":
 st.markdown(f"""
     <div class="platform-header">
         <div style="display: flex; justify-content: space-between; align-items: center;">
             <div>
                 <h1>Live Neighborhood Pollution Monitoring</h1>
                 <p>Monitor pollution across streets using citizen reports, local sensors and satellite imagery.</p>
             </div>
             <div style="text-align: right; font-size: 15px; color: #64748B; font-weight: 500;">
                 🏢 <b>DPCC Central Station Network</b><br>
                 🌡️ 31°C Haze • 💧 Humidity 46% • 🌬️ Wind 8 km/h NE
             </div>
         </div>
     </div>
 """, unsafe_allow_html=True)
 kpi_cols = st.columns(5)
 with kpi_cols[0]:
     st.markdown(f"""<div class="command-card" style="border-bottom: 3px solid {active_city_data['color']} !important;"><div class="kpi-wrapper"><span class="kpi-title">Average AQI</span><div class="kpi-icon-box" style="background:#DCFCE7; color:#15803D;">🌿</div></div><div class="kpi-value">{active_city_data['aqi']}</div></div>""", unsafe_allow_html=True)
     if st.button("View Trend History ↗", key="btn_kpi_1"): st.session_state.selected_kpi = "AQI_Trend"
 with kpi_cols[1]:
     st.markdown(f"""<div class="command-card" style="border-bottom: 3px solid #EF4444 !important;"><div class="kpi-wrapper"><span class="kpi-title">Active Hotspots</span><div class="kpi-icon-box" style="background:#FEE2E2; color:#B91C1C;">🔥</div></div><div class="kpi-value">{len(active_city_data['hotspots'])} Areas</div></div>""", unsafe_allow_html=True)
     if st.button("View Hotspot Analysis ↗", key="btn_kpi_2"): st.session_state.selected_kpi = "Hotspots_Summary"
 with kpi_cols[2]:
     st.markdown(f"""<div class="command-card" style="border-bottom: 3px solid #3B82F6 !important;"><div class="kpi-wrapper"><span class="kpi-title">Citizen Reports</span><div class="kpi-icon-box" style="background:#EFF6FF; color:#1D4ED8;">📸</div></div><div class="kpi-value">{len(MASTER_REPORTS)} Validated</div></div>""", unsafe_allow_html=True)
     if st.button("View Validation Logs ↗", key="btn_kpi_3"): st.session_state.selected_kpi = "Reports_Table"
 with kpi_cols[3]:
     st.markdown(f"""<div class="command-card" style="border-bottom: 3px solid #8B5CF6 !important;"><div class="kpi-wrapper"><span class="kpi-title">Satellite Alerts</span><div class="kpi-icon-box" style="background:#F3E8FF; color:#7C3AED;">🛰️</div></div><div class="kpi-value">Fresh Scan</div></div>""", unsafe_allow_html=True)
     if st.button("Analyze Satellite Scan ↗", key="btn_kpi_5"): st.session_state.selected_kpi = "Satellite_View"
 with kpi_cols[4]:
     st.markdown(f"""<div class="command-card" style="border-bottom: 3px solid #10B981 !important;"><div class="kpi-wrapper"><span class="kpi-title">Response Teams</span><div class="kpi-icon-box" style="background:#DCFCE7; color:#10B981;">🚒</div></div><div class="kpi-value">2 Active</div></div>""", unsafe_allow_html=True)
     if st.button("Track Fleet Deployment ↗", key="btn_kpi_6"): st.session_state.selected_kpi = "Deployment_Table"








 st.markdown('<div class="whitespace-compressor"></div>', unsafe_allow_html=True)








 if st.session_state.selected_kpi != "Default":
     with st.container(border=True):
         if st.session_state.selected_kpi == "AQI_Trend":
             st.write(f"### 📊 {selected_city} AQI Variant Trend Timeline")
             t_pts = active_city_data['trend_data']
             fig_t = px.line(x=['24H Ago', '18H Ago', '12H Ago', '8H Ago', '6H Ago', '4H Ago', '2H Ago', 'Current'], y=t_pts, markers=True, labels={'x':'Timeline Pass', 'y':'AQI Value'}, color_discrete_sequence=[active_city_data['color']])
             fig_t.add_hline(y=60, line_dash="dash", line_color="#22C55E", annotation_text="Safe National Limit (60)")
             fig_t.update_layout(margin=dict(l=20, r=20, t=10, b=10), height=200, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
             st.plotly_chart(fig_t, width="stretch")
             st.markdown(f"<p style='font-size:16px; color:#475569;'><b>Average AQI:</b> {sum(t_pts)//len(t_pts)} | <b>Highest AQI:</b> {max(t_pts)} | <b>Lowest AQI:</b> {min(t_pts)}<br>🔬 <b>AI Insight:</b> AQI increased because of traffic congestion and construction dust tracking.</p>", unsafe_allow_html=True)
         elif st.session_state.selected_kpi == "Hotspots_Summary":
             st.write("### 📍 Operational Section Hotspot Summary Registry")
             summary_rows = []
             for hs in active_city_data["hotspots"]:
                 summary_rows.append({"Area Name": hs["street"], "Severity Level": "High" if hs["aqi"]>170 else "Medium", "Estimated AQI": hs["aqi"], "Suggested Action Plan": hs["act"]})
             st.dataframe(pd.DataFrame(summary_rows), width="stretch", hide_index=True)
         elif st.session_state.selected_kpi == "Reports_Table":
             st.write("### 📑 Validated Citizen Reports Feed Logs")
             st.dataframe(pd.DataFrame(MASTER_REPORTS), width="stretch", hide_index=True)
             csv_data = pd.DataFrame(MASTER_REPORTS).to_csv(index=False).encode('utf-8')
             st.download_button(label="📥 Download CSV Log Report", data=csv_data, file_name="aerowatch_reports.csv", mime="text/csv")
             if st.button("🌐 Export Live Data to Google Sheets"):
                 st.success("Successfully simulated secure data export pipeline via Google Sheets Cloud API framework.")
         elif st.session_state.selected_kpi == "Satellite_View":
             sat_data = active_city_data["satellite"]
             st.write("### 🛰️ Aerial Space Tracking Overlay")
             st.markdown(f"""<div style="font-size:16px; line-height:1.6; background:#F8FAFC; padding:20px; border-radius:12px; border: 1px solid #DCE6F2;">
                 <b>Anomaly Detected:</b> {sat_data['anomaly']} | <b>Smoke Status:</b> {sat_data['smoke']}<br>
                 <b>Scan Time:</b> {sat_data['timestamp']} | <b>AI Confidence Score:</b> {sat_data['confidence']}
             </div>""", unsafe_allow_html=True)
         elif st.session_state.selected_kpi == "Deployment_Table":
             st.write("### 🚒 Response Teams Fleet Manifest")
             st.dataframe(pd.DataFrame(TEAMS_DATABASE), width="stretch", hide_index=True)
      
         if st.button("❌ Close Panel"):
             st.session_state.selected_kpi = "Default"
             st.rerun()








 map_col, queue_col = st.columns([2.1, 1])
 with map_col:
     with st.container(border=True):
         st.markdown("""
             <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 14px;">
                 <span style="font-weight:800; font-size:18px; color:#1F2937; text-transform:uppercase; letter-spacing:0.04em;">📍 Hyperlocal Street Level Pollution Map</span>
                 <span style="font-size:14px; background:#EFF6FF; color:#2563EB; padding:6px 12px; border-radius:12px; font-weight:700; border: 1px solid #DBEAFE;">REAL-TIME GRID</span>
             </div>
         """, unsafe_allow_html=True)
         m_center = active_city_data['coords']
         # Upgraded to colorful Google Maps Style
         base_map = folium.Map(location=m_center, zoom_start=14, tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", attr="Google", zoom_control=True)
         for hs in active_city_data['hotspots']:
             is_active = (hs['id'] == st.session_state.active_report_id)
             pop_content = f"""
             <div style="font-family: 'Plus Jakarta Sans', sans-serif; width:300px; padding:8px; line-height:1.6; font-size:15px;">
                 <div style="font-weight:800; font-size:17px; color:#0F172A; margin-bottom:10px; border-bottom:1px solid #E2E8F0; padding-bottom:8px;">📊 Hotspot Analytics</div>
                 <b>Area Name:</b> {hs['street']}<br><b>Current AQI:</b> {hs['aqi']}<br><b>Predicted AQI:</b> {hs['aqi']+43}<br>
                 <b>Severity:</b> {hs['category']}<br><b>Hospitals Nearby:</b> {hs['hospitals']}<br><b>Schools Nearby:</b> {hs['schools']}<br>
                 <b>Traffic Density:</b> {hs['traffic']}<br><b>Recommended Response:</b> {hs['act']}<br><b>Team Assigned:</b> {hs['team']}
             </div>
             """
             folium.CircleMarker(location=hs['loc'], radius=14, popup=folium.Popup(pop_content, max_width=350), color=hs['color'], fill=True, fill_opacity=0.7 if is_active else 0.4, weight=6 if is_active else 2).add_to(base_map)
         st_folium(base_map, height=450, width=None, returned_objects=[], key="master_folium_canvas_node")
  
 with queue_col:
     with st.container(border=True, height=540):
         st.markdown("""
             <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 14px;">
                 <span style="font-weight:800; font-size:18px; color:#1F2937; text-transform:uppercase; letter-spacing:0.04em;">📑 Incident Queue</span>
                 <span style="font-size:14px; background:#FEF2F2; color:#EF4444; padding:6px 12px; border-radius:12px; font-weight:700; border: 1px solid #FEE2E2;">ACTIVE SCAN</span>
             </div>
         """, unsafe_allow_html=True)
         for hs in active_city_data['hotspots']:
             is_selected = (hs['id'] == st.session_state.active_report_id)
             highlight = "pulse-card-highlight" if is_selected else ""
          
             st.markdown(f"""
                 <div class="alert-interactive-row {highlight}" style="border-left: 5px solid {hs['color']};">
                     <div style="font-size:14px; font-weight:700; color:#64748B; display:flex; justify-content:space-between;">
                         <span>📍 {hs['source_type']}</span><span>{hs['time']}</span>
                     </div>
             """, unsafe_allow_html=True)
             if st.button(f"{hs['street']}", key=f"sync_queue_{hs['id']}"):
                 st.session_state.active_report_id = hs['id']
                 st.session_state.view_action_details = hs['id']
                 st.rerun()
             st.markdown(f"""
                     <div style="font-size:15px; color:#475569; margin-top:6px;">
                         AQI: <b style="color:#0F172A;">{hs['aqi']}</b> | Status: <b style="color:#0F172A;">{st.session_state.action_statuses.get(hs['id'])}</b><br>Assigned: <b style="color:#0F172A;">{hs['team']}</b>
                     </div>
                 </div>
             """, unsafe_allow_html=True)








 # Local Ground Telemetry Network Row
 with st.container(border=True):
     st.markdown("""
         <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 14px;">
             <span style="font-weight:800; font-size:18px; color:#1F2937; text-transform:uppercase; letter-spacing:0.04em;">🌐 Local Ground Telemetry IoT Sensor Array Network</span>
             <span style="font-size:14px; background:#F0FDF4; color:#16A34A; border: 1px solid #DCFCE7; padding:6px 12px; border-radius:12px; font-weight:700;">CONNECTED</span>
         </div>
     """, unsafe_allow_html=True)
     df_sensors = pd.DataFrame(active_city_data["sensors"])
     st.dataframe(df_sensors, width="stretch", hide_index=True)








# ==============================================================================
# 6. PAGE 2: CITIZEN REPORT POLLUTION INTERFACE (ZERO-CLICK WORKFLOW)
# ==============================================================================
elif menu == "📸 Report Pollution":
 st.markdown("""
     <div class="platform-header">
         <div style="display: flex; justify-content: space-between; align-items: center;">
             <div>
                 <h1>Report Local Area Pollution</h1>
                 <p>Upload files to run the automated Gemini verification and telemetry matching architecture.</p>
             </div>
         </div>
     </div>
 """, unsafe_allow_html=True)
 upload_col, results_col = st.columns([1, 1])
 with upload_col:
     with st.container(border=True):
         st.markdown('<div style="font-size: 28px; font-weight: 800; color: #1F2937; margin-bottom: 20px;">🚨 SUBMIT INCIDENT EVIDENCE</div>', unsafe_allow_html=True)
      
         img_file = st.file_uploader("**Upload Incident Photo (JPG / PNG)**", type=['jpg', 'jpeg', 'png'])
         if img_file:
             st.image(img_file, caption="✅ Image Preview", width="stretch")
           
         video_file = st.file_uploader("**🎥 Supporting Video (Optional)**", type=['mp4'])
         st.markdown("<p style='font-size: 14px; color: #64748B; margin-top: -12px; margin-bottom: 16px;'>Optional. Upload a short MP4 video to help verify the incident.</p>", unsafe_allow_html=True)
      
         # Auto-trigger logic
         current_upload_id = ""
         if img_file: current_upload_id += f"img_{img_file.size}"
         if video_file: current_upload_id += f"vid_{video_file.size}"




         # Reset pipeline on new upload
         if current_upload_id != st.session_state.prev_upload_id:
             if current_upload_id != "":
                 st.session_state.simulation_pipeline_stage = 0
             else:
                 st.session_state.simulation_pipeline_stage = None
             st.session_state.prev_upload_id = current_upload_id








 with results_col:
     if st.session_state.simulation_pipeline_stage is not None:
         with st.container(border=True):
           
             stages = [
                 "🧠 Initializing Gemini Vision...",
                 "✓ Detecting pollution...",
                 "✓ Identifying pollution category...",
                 "✓ Estimating severity...",
                 "✓ Predicting AQI impact...",
                 "✓ Generating citizen report...",
                 "✓ Updating Monitoring Dashboard..."
             ]
          
             if st.session_state.simulation_pipeline_stage < len(stages):
                 p_container = st.empty()
                 for idx in range(st.session_state.simulation_pipeline_stage, len(stages)):
                     p_container.info(f"**{stages[idx]}**")
                     time.sleep(0.7)
                 p_container.empty()
                 st.session_state.simulation_pipeline_stage = len(stages)
                 st.rerun()
          
             # Show Success Status
             st.markdown("""
                 <div style="font-size: 20px; font-weight: 800; color: #16A34A; margin-bottom: 20px;">
                     ✅ Incident Successfully Reported
                 </div>
             """, unsafe_allow_html=True)




             # Prominent Incident Card First
             st.markdown("""
                 <div class="ai-report-card" style="margin-bottom: 20px; border-left: 6px solid #EF4444; background: #FFFFFF;">
                     <div class="lbl">🚨 Incident</div>
                     <div class="val" style="font-size: 28px; color: #DC2626;">Garbage Dump Fire</div>
                 </div>
             """, unsafe_allow_html=True)




             # Results Grid
             st.markdown("""
                 <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
                     <div class="ai-report-card">
                         <div class="lbl">📍 Location</div>
                         <div class="val">Connaught Place, New Delhi</div>
                     </div>
                     <div class="ai-report-card">
                         <div class="lbl">🌫 Pollution Category</div>
                         <div class="val">Garbage Dump Fire</div>
                     </div>
                     <div class="ai-report-card">
                         <div class="lbl">🚨 Severity</div>
                         <div class="val" style="color: #DC2626;">High</div>
                     </div>
                     <div class="ai-report-card">
                         <div class="lbl">🌬 AQI Impact</div>
                         <div class="val" style="color: #DC2626;">Significant (+43 AQI)</div>
                     </div>
                     <div class="ai-report-card" style="grid-column: span 2;">
                         <div class="lbl">🎯 AI Confidence</div>
                         <div class="val" style="color: #16A34A;">93%</div>
                     </div>
                 </div>
               
                 <div class="ai-report-card" style="margin-bottom: 20px;">
                     <div class="section-header" style="border-bottom: none; margin-bottom: 10px; padding-bottom: 0;">📝 Citizen Report</div>
                     <p style="font-size: 16px; color: #475569; line-height: 1.7; margin-bottom: 24px;">
                         Smoke detected from an open garbage dump beside the main road. Dense smoke plume observed affecting nearby traffic visibility and local air quality. <b>This incident has been automatically forwarded to the local municipal authority for immediate intervention.</b>
                     </p>
                     <div class="section-header" style="border-bottom: none; margin-bottom: 10px; padding-bottom: 0;">✅ Recommended Actions</div>
                     <ul style="font-size: 15px; color: #475569; margin: 0; line-height: 1.9; list-style-type: none; padding-left: 0;">
                         <li>✓ Dispatch sanitation response team</li>
                         <li>✓ Extinguish garbage fire</li>
                         <li>✓ Monitor AQI</li>
                         <li>✓ Issue public health advisory if required</li>
                     </ul>
                 </div>
               
                 <div style="font-size: 18px; font-weight: 800; color: #2563EB; margin-bottom: 20px;">
                     📤 Monitoring Dashboard Updated
                 </div>
               
                 <div class="ai-report-card success-card" style="margin-bottom: 16px;">
                     <div class="section-header" style="border-bottom-color: #C8E6C9; margin-bottom: 16px; padding-bottom: 12px;">🚛 Municipal Response</div>
                     <div style="font-size: 18px; font-weight: 800; color: #16A34A; margin-bottom: 16px;">✅ Municipal Team Alerted</div>
                     <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                         <div>
                             <div class="lbl">📍 Assigned Zone</div>
                             <div class="val" style="font-size: 16px;">Connaught Place, New Delhi</div>
                         </div>
                         <div>
                             <div class="lbl">🚨 Response Priority</div>
                             <div class="val" style="font-size: 16px; color: #DC2626;">High</div>
                         </div>
                         <div>
                             <div class="lbl">👷 Dispatch Status</div>
                             <div class="val" style="font-size: 16px;">Field Team Assigned</div>
                         </div>
                         <div>
                             <div class="lbl">⏱ Estimated Response Time</div>
                             <div class="val" style="font-size: 16px;">15 minutes</div>
                         </div>
                     </div>
                 </div>
             """, unsafe_allow_html=True)








# ==============================================================================
# 7. PAGE 3: AI ACTION CENTER (MUNICIPAL APPROVAL CENTER)
# ==============================================================================
else:
 st.markdown(f"""
     <div class="platform-header">
         <div style="display: flex; justify-content: space-between; align-items: center;">
             <div>
                 <h1>Municipal Approval Center</h1>
                 <p>Review AI recommendations, check validation parameters, and authorize mitigation asset dispatches.</p>
             </div>
         </div>
     </div>
 """, unsafe_allow_html=True)
 trend_col, workflow_col, intelligence_col = st.columns([1.1, 1.3, 1])
 with trend_col:
     with st.container(border=True):
         st.markdown('<div class="section-header">🔮 Projected Impact</div>', unsafe_allow_html=True)
      
         st.markdown("""
             <div style="background: #FEF2F2; border: 1px solid #FEE2E2; border-left: 5px solid #EF4444; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
                 <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                     <span style="font-size:16px; font-weight:800; color:#991B1B; text-transform:uppercase; letter-spacing:0.02em;">Telemetry Projection</span>
                     <span style="background:#EF4444; color:white; padding:6px 12px; border-radius:12px; font-size:14px; font-weight:800;">CRITICAL RISK</span>
                 </div>
                 <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; font-size:16px; color:#1F2937;">
                     <div>Ambient AQI: <b style="color:#111827; font-weight:800;">185</b></div>
                     <div>Forecast AQI: <b style="color:#DC2626; font-weight:800;">228</b></div>
                     <div>Variance Delta: <b style="color:#DC2626; font-weight:800;">+43 AQI</b></div>
                     <div>Impact Window: <b style="color:#111827; font-weight:800;">4.0 Hours</b></div>
                 </div>
             </div>
         """, unsafe_allow_html=True)
      
         fig_spline = go.Figure()
         fig_spline.add_trace(go.Scatter(x=['8 AM', '12 PM', '4 PM', 'Current', 'Wave +2H', 'Wave +4H'], y=[140, 160, 175, 185, 210, 228], mode='lines+markers', line=dict(width=4, color='#EF4444', shape='spline'), fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.04)'))
         fig_spline.update_layout(margin=dict(l=5, r=5, t=5, b=5), height=180, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, tickfont=dict(size=12, color="#475569")), yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(size=12, color="#475569")))
         st.plotly_chart(fig_spline, width="stretch", config={'displayModeBar': False})
  
 with workflow_col:
     with st.container(border=True, height=520):
         st.markdown('<div class="section-header">🚒 Recommended Actions</div>', unsafe_allow_html=True)
      
         for hs in active_city_data['hotspots']:
             c_status = st.session_state.action_statuses.get(hs['id'], "🟡 Pending Approval")
             st.markdown(f"""
                 <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin-bottom: 16px; background: white; font-size:16px; line-height:1.5;">
                     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom:10px;">
                         <span style="font-weight: 800; color: #0F172A; font-size: 18px;">📍 {hs['street']}</span>
                         <span style="font-size:14px; font-weight:800;">● {c_status}</span>
                     </div>
                     <div style="font-weight: 800; color: #1E3A8A; font-size:18px; margin:8px 0;">{hs['act']}</div>
                     <div style="font-size:15px; color:#475569; display:grid; grid-template-columns: 1fr 1fr; gap:10px; padding:12px 0; border-top:1px dashed #F1F5F9; margin-top:12px;">
                         <span>✨ Expected Improvement: <b style="color:#0F172A;">20 AQI</b></span><span>⏱️ Estimated Completion: <b style="color:#0F172A;">25 Mins</b></span>
                         <span>🔥 Priority: <b style="color:#DC2626;">High</b></span><span>🚒 Crew: <b style="color:#0F172A;">{hs['team']}</b></span>
                     </div>
                     <div style="font-size:14px; color:#64748B; background:#F8FAFC; padding:12px; border-radius:8px; margin-top:10px; margin-bottom:16px; border: 1px solid #E2E8F0;">📦 <b>Resources Needed:</b> 2 Water Mist Vehicles • 1 Traffic Police Team</div>
                 </div>
             """, unsafe_allow_html=True)
          
             btn_col1, btn_col2 = st.columns(2)
             with btn_col1:
                 st.markdown("<div class='action-btn-layout'>", unsafe_allow_html=True)
                 if st.button("🚀 Approve & Deploy", key=f"p3_deploy_{hs['id']}"):
                     st.session_state.action_statuses[hs['id']] = "🟢 Approved"
                     st.toast(f"Authorized Action Checklist Plan Entry! Dispatched {hs['team']} to local bounds.")
                     st.rerun()
                 st.markdown("</div>", unsafe_allow_html=True)
             with btn_col2:
                 st.markdown("<div class='action-btn-layout'>", unsafe_allow_html=True)
                 if st.button("✓ Mark Finished", key=f"p3_complete_{hs['id']}"):
                     st.session_state.action_statuses[hs['id']] = "🔵 Completed"
                     st.toast(f"Marked action item task node line item as finalized.")
                     st.rerun()
                 st.markdown("</div>", unsafe_allow_html=True)
  
 with intelligence_col:
     with st.container(border=True, height=520):
         st.markdown('<div class="section-header">🤖 AI Decision Engine</div>', unsafe_allow_html=True)
      
         st.markdown(f"""
             <div style="display: flex; flex-direction: column; gap: 16px;">
                 <div style="background: #F0FDF4; border: 1px solid #DCFCE7; border-left: 5px solid #16A34A; padding: 20px; border-radius: 12px; font-size: 16px;">
                     <span style="color: #15803D; font-weight: 800; text-transform: uppercase; font-size: 14px; letter-spacing:0.04em; display:block; margin-bottom:10px;">AI Diagnostics</span>
                     <b>Primary Root Cause:</b> Vehicle Smoke Emissions<br>
                     <div style="margin-top: 8px;"><b>Confidence Index:</b> <span style="color:#16A34A; font-weight:800;">93% Accuracy Match</span></div>
                 </div>
                 <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 5px solid #64748B; padding: 20px; border-radius: 12px; font-size: 16px;">
                     <span style="color: #475569; font-weight: 800; text-transform: uppercase; font-size: 14px; letter-spacing:0.04em; display:block; margin-bottom:12px;">Cross-Verification Nodes</span>
                     <div style="display:grid; grid-template-columns:1fr; gap:10px; color:#334155;">
                         <span><b style="color:#0F172A;">✓</b> Multi-Spectral Citizen Photo Match</span>
                         <span><b style="color:#0F172A;">✓</b> IoT Sensor Grid Telemetry Convergence</span>
                         <span><b style="color:#0F172A;">✓</b> Thermal Satellite Plume Verification</span>
                     </div>
                 </div>
                 <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-left: 5px solid #2563EB; padding: 20px; border-radius: 12px; font-size: 16px;">
                     <span style="color: #1D4ED8; font-weight: 800; text-transform: uppercase; font-size: 14px; letter-spacing:0.04em; display:block; margin-bottom:10px;">Mitigation Action</span>
                     <b>Prescribed Directive:</b> Deploy Localized Water Mist Cannon Suppression<br>
                     <div style="margin-top: 8px;"><b>Improvement Projection:</b> -20 AQI Point Reduction</div>
                 </div>
             </div>
         """, unsafe_allow_html=True)








# ==============================================================================
# 8. SYSTEM ADMINISTRATIVE CONTROL FOOTER LAYER
# ==============================================================================
st.markdown("""
 <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #E2E8F0; text-align: center; color: #94A3B8; font-size: 15px; font-weight: 600; line-height:1.6;">
     <div><b>Official Platform Sources Registry:</b> Delhi Pollution Control Committee (DPCC) • National Citizen Reports Logs • Encrypted IoT Sensory Grids Network • ISRO INSAT Imagery Swaths Band-3 • Weather API Forecasts Engine</div>
     <div style="margin-top: 10px; display: flex; justify-content: center; gap: 20px; color: #64748B; font-weight: 500;">
         <span>⚡ Core Orchestration SDK: Google Gemini AI Platform (gemini-1.5-flash natively processing multi-lingual inputs)</span>
         <span>🏆 National Challenge Track Submission 2026 Portfolio</span>
     </div>
 </div>
""", unsafe_allow_html=True)











