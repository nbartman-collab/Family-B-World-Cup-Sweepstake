import streamlit as st
import pandas as pd
import json
import os

# 1. Define the Sweepstake Pools exactly as drawn
SWEEPSTAKE_POOLS = {
    "Nick": ["England", "Mexico", "Morocco", "Australia", "Egypt", "Scotland", "South Africa", "Iraq"],
    "Kate": ["France", "Brazil", "Uruguay", "Japan", "Algeria", "Ivory Coast", "Uzbekistan", "Haiti"],
    "Florence": ["Spain", "United States", "Colombia", "Ecuador", "Norway", "Panama", "Jordan", "Cape Verde"],
    "Annabel": ["Argentina", "Germany", "Croatia", "Iran", "Canada", "Paraguay", "Qatar", "New Zealand"],
    "Edward": ["Portugal", "Belgium", "Switzerland", "South Korea", "Austria", "Tunisia", "Saudi Arabia", "Curaçao"]
}

FLAG_MAPPING = {
    "England": "🏴 *England*", "Mexico": "🇲🇽 *Mexico*", "Morocco": "🇲🇦 *Morocco*", "Australia": "🇦🇺 *Australia*", "Egypt": "🇪🇬 *Egypt*", "Scotland": "🏴 *Scotland*", "South Africa": "🇿🇦 *South Africa*", "Iraq": "🇮🇶 *Iraq*",
    "France": "🇫🇷 *France*", "Brazil": "🇧🇷 *Brazil*", "Uruguay": "🇺🇾 *Uruguay*", "Japan": "🇯🇵 *Japan*", "Algeria": "🇩🇿 *Algeria*", "Ivory Coast": "🇨🇮 *Ivory Coast*", "Uzbekistan": "🇺🇿 *Uzbekistan*", "Haiti": "🇭🇹 *Haiti*",
    "Spain": "🇪🇸 *Spain*", "United States": "🇺🇸 *United States*", "Colombia": "🇨🇴 *Colombia*", "Ecuador": "🇪🇨 *Ecuador*", "Norway": "🇳🇴 *Norway*", "Panama": "🇵🇦 *Panama*", "Jordan": "🇯🇴 *Jordan*", "Cape Verde": "🇨🇻 *Cape Verde*",
    "Argentina": "🇦🇷 *Argentina*", "Germany": "🇩🇪 *Germany*", "Croatia": "🇭🇷 *Croatia*", "Iran": "🇮🇷 *Iran*", "Canada": "🇨🇦 *Canada*", "Paraguay": "🇵🇾 *Paraguay*", "Qatar": "🇶🇦 *Qatar*", "New Zealand": "🇳🇿 *New Zealand*",
    "Portugal": "🇵🇹 *Portugal*", "Belgium": "🇧🇪 *Belgium*", "Switzerland": "🇨🇭 *Switzerland*", "South Korea": "🇰🇷 *South Korea*", "Austria": "🇦🇹 *Austria*", "Tunisia": "🇹🇳 *Tunisia*", "Saudi Arabia": "🇸🇦 *Saudi Arabia*", "Curaçao": "🇨🇼 *Curaçao*",
    "Bosnia": "🇧🇦 *Bosnia*", "Türkiye": "🇹🇷 *Türkiye*", "Netherlands": "🇳🇱 *Netherlands*", "Sweden": "🇸🇪 *Sweden*", "Senegal": "🇸🇳 *Senegal*", "Czechia": "🇨🇿 *Czechia*", "Iraq": "🇮🇶 *Iraq*", "DR Congo": "🇨🇩 *DR Congo*", "Ghana": "🇬🇭 *Ghana*"
}

FIXTURES_BY_DAY = {
    "Thursday, June 11": [{"id": "m1", "home": "Mexico", "away": "South Africa", "time": "19:00"}],
    "Friday, June 12": [
        {"id": "m2", "home": "South Korea", "away": "Czechia", "time": "02:00"},
        {"id": "m3", "home": "Canada", "away": "Bosnia", "time": "19:00"}
    ],
    "Saturday, June 13": [
        {"id": "m4", "home": "United States", "away": "Paraguay", "time": "01:00"},
        {"id": "m5", "home": "Qatar", "away": "Switzerland", "time": "19:00"},
        {"id": "m6", "home": "Brazil", "away": "Morocco", "time": "22:00"}
    ],
    "Sunday, June 14": [
        {"id": "m7", "home": "Haiti", "away": "Scotland", "time": "01:00"},
        {"id": "m8", "home": "Australia", "away": "Türkiye", "time": "04:00"},
        {"id": "m9", "home": "Germany", "away": "Curaçao", "time": "17:00"},
        {"id": "m10", "home": "Netherlands", "away": "Japan", "time": "20:00"},
        {"id": "m11", "home": "Ivory Coast", "away": "Ecuador", "time": "23:00"}
    ],
    "Monday, June 15": [
        {"id": "m12", "home": "Sweden", "away": "Tunisia", "time": "02:00"},
        {"id": "m13", "home": "Spain", "away": "Cape Verde", "time": "16:00"},
        {"id": "m14", "home": "Belgium", "away": "Egypt", "time": "19:00"},
        {"id": "m15", "home": "Saudi Arabia", "away": "Uruguay", "time": "22:00"}
    ],
    "Tuesday, June 16": [
        {"id": "m16", "home": "Iran", "away": "New Zealand", "time": "01:00"},
        {"id": "m17", "home": "France", "away": "Senegal", "time": "19:00"},
        {"id": "m18", "home": "Iraq", "away": "Norway", "time": "22:00"}
    ],
    "Wednesday, June 17": [
        {"id": "m19", "home": "Argentina", "away": "Algeria", "time": "01:00"},
        {"id": "m20", "home": "Austria", "away": "Jordan", "time": "04:00"},
        {"id": "m21", "home": "Portugal", "away": "DR Congo", "time": "17:00"},
        {"id": "m22", "home": "England", "away": "Croatia", "time": "20:00"},
        {"id": "m23", "home": "Ghana", "away": "Panama", "time": "23:00"}
    ],
    "Thursday, June 18": [
        {"id": "m24", "home": "Uzbekistan", "away": "Colombia", "time": "03:00"},
        {"id": "m25", "home": "Czechia", "away": "South Africa", "time": "17:00"},
        {"id": "m26", "home": "Switzerland", "away": "Bosnia", "time": "20:00"},
        {"id": "m27", "home": "Canada", "away": "Qatar", "time": "23:00"}
    ],
    "Friday, June 19": [
        {"id": "m28", "home": "Mexico", "away": "South Korea", "time": "02:00"},
        {"id": "m29", "home": "United States", "away": "Australia", "time": "20:00"},
        {"id": "m30", "home": "Scotland", "away": "Morocco", "time": "23:00"}
    ],
    "Saturday, June 20": [
        {"id": "m31", "home": "Brazil", "away": "Haiti", "time": "01:30"},
        {"id": "m32", "home": "Türkiye", "away": "Paraguay", "time": "04:00"},
        {"id": "m33", "home": "Netherlands", "away": "Sweden", "time": "18:00"},
        {"id": "m34", "home": "Germany", "away": "Ivory Coast", "time": "21:00"}
    ],
    "Sunday, June 21": [
        {"id": "m35", "home": "Ecuador", "away": "Curaçao", "time": "01:00"},
        {"id": "m36", "home": "Tunisia", "away": "Japan", "time": "05:00"}
    ]
}

# Standard persistent filesystem path allocation
DB_FILE = "online_sweepstake_memory.json"

def load_global_scores():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_global_scores(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Pull saved database files instantly from central container storage
saved_scores = load_global_scores()

st.set_page_config(page_title="2026 World Cup Sweepstake", page_icon="🏆", layout="wide")
st.title("🏆 Bartman Family World Cup Sweepstake Live Scoreboard")

# 2. Secure Sidebar Control Lock
st.sidebar.header("🔐 Admin Dashboard")
password = st.sidebar.text_input("Enter Admin Password to Log Scores", type="password")
is_admin = (password == "wimbledon2026")

match_scores = {}

if is_admin:
    st.sidebar.success("Access Granted! Update scores below:")
    for match_date, match_list in FIXTURES_BY_DAY.items():
        st.sidebar.markdown(f"### 📅 {match_date}")
        for match in match_list:
            m_id = match["id"]
            h_team = match["home"]
            a_team = match["away"]
            
            default_home = saved_scores.get(m_id, {}).get("home_score", "-")
            default_away = saved_scores.get(m_id, {}).get("away_score", "-")
            
            options = ["-", "0", "1", "2", "3", "4", "5", "6"]
            idx_h = options.index(default_home) if default_home in options else 0
            idx_a = options.index(default_away) if default_away in options else 0
            
            st.sidebar.caption(f"⏰ Kickoff: **{match['time']} BST**")
            col_h_name, col_h_score, col_vs, col_a_score, col_a_name = st.sidebar.columns([3, 2, 1, 2, 3])
            
            with col_h_name:
                st.markdown(f"<p style='text-align: right; margin-top:5px;'>{h_team}</p>", unsafe_allow_html=True)
            with col_h_score:
                h_g = st.selectbox("", options=options, index=idx_h, key=f"h_{m_id}", label_visibility="collapsed")
            with col_vs:
                st.markdown("<p style='text-align: center; margin-top:5px;'>v</p>", unsafe_allow_html=True)
            with col_a_score:
                a_g = st.selectbox("", options=options, index=idx_a, key=f"a_{m_id}", label_visibility="collapsed")
            with col_a_name:
                st.markdown(f"<p style='text-align: left; margin-top:5px;'>{a_team}</p>", unsafe_allow_html=True)
                
            match_scores[m_id] = {"home_team": h_team, "away_team": a_team, "home_score": h_g, "away_score": a_g}
    
    if st.sidebar.button("💾 Save & Publish Scores Online", use_container_width=True):
        save_global_scores(match_scores)
        st.sidebar.success("Global Scoreboard Updated!")
        st.rerun()
else:
    st.sidebar.info("Family View: Keeping track live! Input fields are locked out.")
    match_scores = saved_scores

# Calculate Standings (Updated to include Played and Losses tracking)
stats = {name: {"Played": 0, "Wins": 0, "Draws": 0, "Losses": 0, "Points": 0} for name in SWEEPSTAKE_POOLS}
team_records = {}

for m_id, score_data in match_scores.items():
    h_s = score_data.get("home_score", "-")
    a_s = score_data.get("away_score", "-")
    
    if h_s != "-" and a_s != "-":
        h_goals, a_goals = int(h_s), int(a_s)
        if h_goals > a_goals:
            team_records[score_data["home_team"]] = "W"
            team_records[score_data["away_team"]] = "L"
        elif a_goals > h_goals:
            team_records[score_data["home_team"]] = "L"
            team_records[score_data["away_team"]] = "W"
        else:
            team_records[score_data["home_team"]] = "D"
            team_records[score_data["away_team"]] = "D"

for participant, team_list in SWEEPSTAKE_POOLS.items():
    for team in team_list:
        outcome = team_records.get(team)
        if outcome == "W":
            stats[participant]["Wins"] += 1
            stats[participant]["Points"] += 3
        elif outcome == "D":
            stats[participant]["Draws"] += 1
            stats[participant]["Points"] += 1
        elif outcome == "L":
            stats[participant]["Losses"] += 1
        
    # Total Played is simply the sum of a participant's individual match outcomes
    stats[participant]["Played"] = stats[participant]["Wins"] + stats[participant]["Draws"] + stats[participant]["Losses"]

# Render Table Standings (Ordered: Participant -> Played -> Wins -> Draws -> Losses -> Total Points)
df = pd.DataFrame.from_dict(stats, orient="index").reset_index()
df.columns = ["Participant", "Played", "Wins", "Draws", "Losses", "Total Points"]
df = df.sort_values(by=["Total Points", "Wins"], ascending=False).reset_index(drop=True)
df.index += 1 

st.subheader("📊 Live League Table Standings")
st.table(df)

st.subheader("🏃‍♂️ Team Pools Current Performance Tracking")
cols = st.columns(5)
for idx, (player, teams) in enumerate(SWEEPSTAKE_POOLS.items()):
    with cols[idx]:
        st.markdown(f"### **{player}**")
        for t in teams:
            flag = FLAG_MAPPING.get(t, t)
            outcome = team_records.get(t)
            status_text = f" **({outcome})**" if outcome else ""
            st.markdown(f"• {flag}{status_text}")
