import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

#^ PAGE CONFIGURATION---------------------------- 
st.set_page_config(
    page_title="Start Your Travel Journey", 
    page_icon="🌍", 
    layout="wide"
)

#^ BACKGROUND STYLE---------------------------- 
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1517760444937-f6397edcbbcd');
    background-size: cover;
    background-attachment: fixed;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
</style>
'''

#^ GLOBAL VARS & FUNCS------------------------- 
st.markdown(page_bg_img, unsafe_allow_html=True)

pois = pd.DataFrame(columns=['Loc_Name','City','Country','Lat','Long'])
m = folium.Map(zoom_start=14)

# ---- SESSION STATE INIT ----
for k in ["sel_ctry", "sel_city", "sel_loc"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ---- CALLBACKS ----
def reset_city_and_loc():
    st.session_state.sel_city = None
    st.session_state.sel_loc = None

def reset_loc():
    st.session_state.sel_loc = None

def Update_poi(info):
    for r in info:
        pois.loc[len(pois)] = r
def Initializer(): # <-- used for getting db info, call Update_poi  
    Update_poi([
        ["Sky Tower", "Auckland", "New Zealand", -36.8485,174.7633],
        ["Auckland War Memorial Museum", "Auckland", "New Zealand", -36.8605,174.7773],
        ["Mount Eden (Maungawhau)", "Auckland", "New Zealand", -36.8793,174.7656],
        ["Waiheke Island", "Auckland", "New Zealand", -36.807,175.075],
        ["Viaduct Harbour", "Auckland", "New Zealand", -36.8422,174.7588]
    ])
Initializer()

#^ LAYOUT STRUCTURE---------------------------- 
uppR = st.columns([1,5,1]) 
midR = st.columns([1,2,4,2,1],gap='medium')
lowR = st.columns([1,1,1])

#* ---------------------------- ROW 1: TITLE
with uppR[1]:
    st.markdown("<h1 style='text-align:center; font-size:60px;'>Start Your Travel Journey</h1>", unsafe_allow_html=True)

#* ---------------------------- ROW 2: OPTIONS & TRANSLATOR
with midR[1]:
    opsTrans = st.columns([2]) + st.columns([2,1.5]) + st.columns([2]) # Top = Map, Bottom = Flight Recommendations 
    with opsTrans[0]:
        st.subheader("Search Filters")
    with opsTrans[1]:
        sel_org = st.selectbox("Choose a Orgin:",
                               ['Toronto','New York','Tokoyo','London','Paris'],
                               index=None,
                               placeholder="Select...")
        sel_ctry = st.selectbox("Choose a Country:", 
                                pois['Country'].unique().tolist(), 
                                index=None, 
                                key="sel_ctry",
                                placeholder="Select...",
                                on_change=reset_city_and_loc)
        city_list = pois[pois['Country'] == sel_ctry]['City'].unique().tolist() if sel_ctry else []
        sel_city = st.selectbox("Choose a City:", 
                                city_list, 
                                index=None, 
                                key = "sel_city",
                                placeholder="Select...",
                                disabled=(sel_ctry == None),
                                on_change=reset_loc)
        loc_list = pois[pois['City'] == sel_city]['Loc_Name'].unique().tolist() if sel_city else []
        sel_loc = st.selectbox("Choose a Location:", 
                                loc_list, 
                                index=None, 
                                placeholder="Select...",
                                disabled=(sel_city == None))
    with opsTrans[2]:
        sel_crowd = st.selectbox("Choose Crowd level:",
                                ['LOW','MEDIUM','HIGH'],
                                index=None,
                                placeholder="Select...")
        sel_attract = st.selectbox("Choose Attraction level:",
                                    ['LOW','MEDIUM','HIGH'],
                                    index=None,
                                    placeholder="Select...")
        sel_hoilday = st.selectbox("Choose Hoilday option:",
                                   ['YES','NO','BOTH'],
                                   index=None,
                                   placeholder="Select...")
        sel_season = st.selectbox("Choose Travel Season:",
                                  ['WINTER','SPRING','SUMMER','FALL'],
                                  index=None,
                                  placeholder="Select...")
    with opsTrans[3]:
        st.subheader("Your Suggestions")
        mode = st.radio("Input:", ["Text", "Voice"], horizontal=True)
        user_input = ""

        if mode == "Text":
            user_input = st.text_area("Enter text in any language:", placeholder="Type Here")
        else:
            pass
    
#* ---------------------------- ROW 2: MAP & RECOMMEND 
with midR[2]:
    mapRec = st.columns([2]) + st.columns([2]) # Top = Map, Bottom = Flight Recommendations 
    with mapRec[0]:
        if sel_loc:
            latlong = pois.loc[pois.index[pois['Loc_Name'] == sel_loc].tolist()[0],['Lat','Long']].tolist()
            folium.Marker(
                location=latlong,
                popup=sel_loc,
                tooltip=sel_loc,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
            lat, lon = latlong
            m.fit_bounds([[lat - 0.01, lon - 0.01], [lat + 0.01, lon + 0.01]])
        folium_static(m, width=None)

    with mapRec[1]:
        st.markdown("""
            <style>
                .poi-recbox {
                    background-color: rgba(131, 131, 131, 0.50);
                    padding: 15px;
                    border-radius: 15px;
                    height: 300px;
                }
            </style>
            """, unsafe_allow_html=True)

        st.markdown(f"""

            <div class='poi-recbox'>
                <h3>Recommendations</h3>   
            </div>
            """, unsafe_allow_html=True)

#* ---------------------------- ROW 2: LOC EDA
with midR[3]:
    # Create dynamic HTML items
    # LocNs = [] 
    # if sel_loc != None:
    #     LocNs = pois[pois['Loc_Name'] == sel_loc,['Loc_Name']].tolist()

    items_html = "".join([
        f"<div class='poi-item'>{name}</div>"
        for name in [[] if sel_loc == None else [sel_loc]][0]
    ])

    st.markdown(f"""
        <div class='poi-desbox'>
            <h3>Destination Forecast</h3>
            {items_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .poi-desbox {
                background-color: rgba(131, 131, 131, 0.50);
                padding: 15px;
                border-radius: 15px;
                height: 842px;
                overflow-y: auto;
            }

            .poi-item {
                background: #eee;
                padding: 10px 15px;
                border-radius: 10px;
                margin-bottom: 8px;
                font-size: 20px;
                font-weight: bold;
                color: rgb(0, 0, 255);
                height: 300px;
            }
            .poi-item:hover {
                background:#dcdcdc;
                cursor:pointer;
            }
        </style>
        """, unsafe_allow_html=True)



# # ----------------------------
# # ROW 1: TITLE
# # ----------------------------
# with rC[1]:
#     st.markdown("<h1 style='text-align:center; font-size:60px;'>Start Your Travel Journey</h1>", unsafe_allow_html=True)

# # ----------------------------
# # ROW 2: SEARCH & TRANSLATOR + MAP & RECOMMENDATION 
# # ----------------------------
# with rC[4]:
#     rC2 = st.columns([2]) # Top = Controls, Bottom = LLM
#     with rC2[0]:

#         poi_list = [
#             "CN Tower, Toronto",
#             "Harbourfront Centre, Toronto",
#             "Royal Ontario Museum, Toronto",
#             "Ripley's Aquarium, Toronto",
#             "Distillery District, Toronto",
#             "Casa Loma, Toronto"
#         ]

#         st.markdown(
#             """<div style="background-color:rgba(255,255,255,0.8);padding: 20px; border-radius: 10px;">
#                     <h3>Search a Point of Interest</h3>
#             """,unsafe_allow_html=True)
        
#         selected_location = st.selectbox("Choose a Location:", poi_list, index=None, placeholder="Select...")

#         st.markdown("""</div>""",unsafe_allow_html=True)

#         # st.markdown(
#         #     """
#         #     <div style="background-color:rgba(255,255,255,0.8);padding: 20px; border-radius: 10px;">
#         #         <h3>Search a Point of Interest</h3>
#         #         <p>This is content within a custom HTML div.</p>
#         #     </div>
#         #     """,
#         #     unsafe_allow_html=True
#         # )

        

#         # AI Translator Feature
#         st.subheader("Your Suggestions")
#         mode = st.radio("Input:", ["Text", "Voice"], horizontal=True)
#         user_input = ""

#         if mode == "Text":
#             user_input = st.text_area("Enter text in any language:", placeholder="Type Here")
#         else:
#             pass

# with rC[5]: # MAP * RECOMMONDATIONS LIVE 
#     rC3 = st.columns([2]) + st.columns([2]) # Top = Map, Bottom = Flight Recommendations 
#     with rC3[0]:
#         m = folium.Map(location=[43.65107, -79.347015], zoom_start=14)
#         poi_coords = {
#             "CN Tower, Toronto": [43.6426, -79.3871],
#             "Harbourfront Centre, Toronto": [43.6387, -79.3823],
#             "Royal Ontario Museum, Toronto": [43.6677, -79.3948],
#             "Ripley's Aquarium, Toronto": [43.6424, -79.3860],
#             "Distillery District, Toronto": [43.6500, -79.3590],
#             "Casa Loma, Toronto": [43.6780, -79.4094]
#         }
#         if selected_location:
#             folium.Marker(
#                 location=poi_coords[selected_location],
#                 popup=selected_location,
#                 tooltip=selected_location,
#                 icon=folium.Icon(color="blue", icon="info-sign")
#             ).add_to(m)
#             lat, lon = poi_coords[selected_location]
#             m.fit_bounds([[lat - 0.01, lon - 0.01], [lat + 0.01, lon + 0.01]])
#         folium_static(m, width=None)
#         st.markdown("</div>", unsafe_allow_html=True)
        
#     # ----------------------------
#     # ROW 3: SCROLLABLE TILES
#     # ----------------------------
#     with rC3[1]:
#         st.markdown(
#             """
#             <h3>Featured Attractions</h3>
#             <div style='background-color:rgba(255,255,255,0.8);padding:15px;border-radius:15px;height:180px;overflow-x:auto;white-space:nowrap;'>
#             <div style='display:flex;gap:20px;'>
#             <div style='background:#eee;padding:10px 20px;border-radius:10px;'>CN Tower</div>
#             <div style='background:#eee;padding:10px 20px;border-radius:10px;'>Royal Ontario Museum</div>
#             <div style='background:#eee;padding:10px 20px;border-radius:10px;'>Casa Loma</div>
#             <div style='background:#eee;padding:10px 20px;border-radius:10px;'>Harbourfront Centre</div>
#             <div style='background:#eee;padding:10px 20px;border-radius:10px;'>Distillery District</div>
#             <div style='background:#eee;padding:10px 20px;border-radius:10px;'>Ripley's Aquarium</div>
#             <div style='background:#eee;padding:10px 20px;border-radius:10px;'>Nathan Phillips Square</div>
#             <div style='background:#eee;padding:10px 20px;border-radius:10px;'>Toronto Islands</div>
#             </div></div>
#             """, unsafe_allow_html=True
#         )

# with rC[6]:
#     rC4 = st.columns([1]) # Loc EDA
#     with rC4[0]:
#         st.markdown(
#             """
#             <div style='background-color:rgba(255,255,255,0.8);padding:15px;border-radius:15px;height:180px;overflow-x:auto;white-space:nowrap;'>
#             <h3>Where Location EDA goes</h3>
#             <div style='display:flex;gap:20px;'>
#             </div></div>
#             """, unsafe_allow_html=True
#         )