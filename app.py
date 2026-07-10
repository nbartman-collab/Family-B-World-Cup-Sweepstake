import streamlit as st
import pandas as pd
import json
import os

# Set up page styling
st.set_page_config(page_title="Bartman Family Sweepstake", page_icon="🏆", layout="wide")

# --- 1. POOLS & FLAGS CONFIGURATION ---
SWEEPSTAKE_POOLS = {
    "Nick": ["England", "Mexico", "Morocco", "Australia", "Egypt", "Scotland", "South Africa", "Iraq"],
    "Kate": ["France", "Brazil", "Uruguay", "Japan", "Algeria", "Ivory Coast", "Uzbekistan", "Haiti"],
    "Florence": ["Spain", "United States", "Colombia", "Ecuador", "Norway", "Panama", "Jordan", "Cape Verde"],
    "Annabel": ["Argentina", "Germany", "Croatia", "Iran", "Canada", "Paraguay", "Qatar", "New Zealand"],
    "Edward": ["Portugal", "Belgium", "Switzerland", "South Korea", "Austria", "Tunisia", "Saudi Arabia", "Curaçao"]
}

FLAG_MAPPING = {
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Mexico": "🇲🇽", "Morocco": "🇲🇦", "Australia": "🇦🇺", "Egypt": "🇪🇬", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "South Africa": "🇿🇦", "Iraq": "🇮🇶",
    "France": "🇫🇷", "Brazil": "🇧🇷", "Uruguay": "🇺🇾", "Japan": "🇯🇵", "Algeria": "🇩🇿", "Ivory Coast": "🇨🇮", "Uzbekistan": "🇺🇿", "Haiti": "🇭🇹",
    "Spain": "🇪🇸", "United States": "🇺🇸", "Colombia": "🇨🇴", "Ecuador": "🇪🇨", "Norway": "🇳🇴", "Panama": "🇵🇦", "Jordan": "🇯🇴", "Cape Verde": "🇨🇻",
    "Argentina": "🇦🇷", "Germany": "🇩🇪", "Croatia": "🇭🇷", "Iran": "🇮🇷", "Canada": "🇨🇦", "Paraguay": "🇵🇾", "Qatar": "🇶🇦", "New Zealand": "🇳🇿",
    "Portugal": "🇵🇹", "Belgium": "🇧🇪", "Switzerland": "🇨🇭", "South Korea": "🇰🇷", "Austria": "🇦🇹", "Tunisia": "🇹🇳", "Saudi Arabia": "🇸🇦", "Curaçao": "🇨🇼"
}

# --- 2. FIXTURES DICTIONARY (Quarter-Finals & Semi-Finals Schedule) ---
FIXTURES_BY_DAY = {
    "Friday, July 10 (Quarter-Finals)": [
        {"id": "m94", "home": "Morocco", "away": "France", "time": "18:00"},
        # UPDATED: Changed Brazil to Norway
        {"id": "m95", "home": "Norway", "away": "England", "time": "22:00"}
    ],
    "Saturday, July 11 (Quarter-Finals)": [
        {"id": "m96", "home": "Portugal", "away": "Belgium", "time": "19:00"},
        {"id": "m97", "home": "Argentina", "away": "Colombia", "time": "23:00"}
    ],
    "Tuesday, July 14 (Semi-Finals)": [
        {"id": "m98", "home": "Winner M94", "away": "Winner M95", "time": "21:00"}
    ],
    "Wednesday, July 15 (Semi-Finals)": [
        {"id": "m99", "home": "Winner M96", "away": "Winner M97", "time": "21:00"}
    ]
}

# --- 3. HARDCODED BASELINE DATA LAYER (Master Records Unbroken and Accurate) ---
match_scores = {
    "m1": {"home_team": "Mexico", "away_team": "South Africa", "home_score": "2", "away_score": "0"},
    "m2": {"home_team": "South Korea", "away_team": "Czechia", "home_score": "2", "away_score": "1"},
    "m3": {"home_team": "Canada", "away_team": "Bosnia", "home_score": "1", "away_score": "1"},
    "m4": {"home_team": "United States", "away_team": "Paraguay", "home_score": "4", "away_score": "1"},
    "m5": {"home_team": "Qatar", "away_team": "Switzerland", "home_score": "1", "away_score": "1"},
    "m6": {"home_team": "Brazil", "away_team": "Morocco", "home_score": "1", "away_score": "1"},
    "m7": {"home_team": "Haiti", "away_team": "Scotland", "home_score": "0", "away_score": "1"},
    "m8": {"home_team": "Australia", "away_team": "Türkiye", "home_score": "2", "away_score": "0"},
    "m9": {"home_team": "Germany", "away_team": "Curaçao", "home_score": "6", "away_score": "1"},
    "m10": {"home_team": "Netherlands", "away_team": "Japan", "home_score": "2", "away_score": "2"},
    "m11": {"home_team": "Ivory Coast", "away_team": "Ecuador", "home_score": "1", "away_score": "0"},
    "m12": {"home_team": "Sweden", "away_team": "Tunisia", "home_score": "5", "away_score": "1"},
    "m13": {"home_team": "Spain", "away_team": "Cape Verde", "home_score": "0", "away_score": "0"},
    "m14": {"home_team": "Belgium", "away_team": "Egypt", "home_score": "1", "away_score": "1"},
    "m15": {"home_team": "Saudi Arabia", "away_team": "Uruguay", "home_score": "1", "away_score": "1"},
    "m16": {"home_team": "Iran", "away_team": "New Zealand", "home_score": "2", "away_score": "2"},
    "m17": {"home_team": "France", "away_team": "Senegal", "home_score": "3", "away_score": "1"},
    "m18": {"home_team": "Iraq", "away_team": "Norway", "home_score": "1", "away_score": "4"},
    "m19": {"home_team": "Argentina", "away_team": "Algeria", "home_score": "3", "away_score": "0"},
    "m20": {"home_team": "Austria", "away_team": "Jordan", "home_score": "3", "away_score": "1"},
    "m21": {"home_team": "Portugal", "away_team": "DR Congo", "home_score": "1", "away_score": "1"},
    "m22": {"home_team": "England", "away_team": "Croatia", "home_score": "4", "away_score": "2"},
    "m23": {"home_team": "Ghana", "away_team": "Panama", "home_score": "1", "away_score": "0"},
    "m24": {"home_team": "Uzbekistan", "away_team": "Colombia", "home_score": "1", "away_score": "3"},
    "m25": {"home_team": "Czechia", "away_team": "South Africa", "home_score": "1", "away_score": "1"},
    "m26": {"home_team": "Switzerland", "away_team": "Bosnia", "home_score": "4", "away_score": "1"},
    "m27": {"home_team": "Canada", "away_team": "Qatar", "home_score": "6", "away_score": "0"},
    "m28": {"home_team": "Mexico", "away_team": "South Korea", "home_score": "1", "away_score": "0"},
    "m29": {"home_team": "United States", "away_team": "Australia", "home_score": "2", "away_score": "0"},
    "m30": {"home_team": "Scotland", "away_team": "Morocco", "home_score": "0", "away_score": "1"},
    "m31": {"home_team": "Brazil", "away_team": "Haiti", "home_score": "3", "away_score": "0"},
    "m32": {"home_team": "Türkiye", "away_team": "Paraguay", "home_score": "0", "away_score": "1"},
    "m33": {"home_team": "Netherlands", "away_team": "Sweden", "home_score": "5", "away_score": "1"},
    "m34": {"home_team": "Germany", "away_team": "Ivory Coast", "home_score": "2", "away_score": "1"},
    "m35a": {"home_team": "Ecuador", "away_team": "Curaçao", "home_score": "0", "away_score": "0"},
    "m35b": {"home_team": "Tunisia", "away_team": "Japan", "home_score": "0", "away_score": "4"},
    "m35c": {"home_team": "Spain", "away_team": "Saudi Arabia", "home_score": "4", "away_score": "0"},
    "m36a": {"home_team": "Belgium", "away_team": "Iran", "home_score": "0", "away_score": "0"},
    "m36b": {"home_team": "Uruguay", "away_team": "Cape Verde", "home_score": "2", "away_score": "2"},
    "m37": {"home_team": "New Zealand", "away_team": "Egypt", "home_score": "1", "away_score": "3"},
    "m38": {"home_team": "Argentina", "away_team": "Austria", "home_score": "2", "away_score": "0"},
    "m39": {"home_team": "France", "away_team": "Iraq", "home_score": "3", "away_team": "0"},
    "m40": {"home_team": "Norway", "away_team": "Senegal", "home_score": "3", "away_score": "2"},
    "m41": {"home_team": "Jordan", "away_team": "Algeria", "home_score": "1", "away_score": "2"},
    "m42": {"home_team": "Portugal", "away_team": "Uzbekistan", "home_score": "5", "away_score": "0"},
    "m43": {"home_team": "England", "away_team": "Ghana", "home_score": "0", "away_score": "0"},
    "m44": {"home_team": "Panama", "away_team": "Croatia", "home_score": "0", "away_score": "1"},
    "m45": {"home_team": "Colombia", "away_team": "DR Congo", "home_score": "1", "away_score": "0"},
    "m46": {"home_team": "Switzerland", "away_team": "Canada", "home_score": "2", "away_score": "1"},
    "m47": {"home_team": "Bosnia", "away_team": "Qatar", "home_score": "3", "away_score": "1"},
    "m48": {"home_team": "Morocco", "away_team": "Haiti", "home_score": "4", "away_score": "2"},
    "m49": {"home_team": "Scotland", "away_team": "Brazil", "home_score": "0", "away_score": "3"},
    "m50": {"home_team": "South Africa", "away_team": "South Korea", "home_score": "1", "away_score": "0"},
    "m51": {"home_team": "Czechia", "away_team": "Mexico", "home_score": "0", "away_score": "3"},
    "m52": {"home_team": "Curaçao", "away_team": "Ivory Coast", "home_score": "0", "away_score": "2"},
    "m53": {"home_team": "Ecuador", "away_team": "Germany", "home_score": "2", "away_score": "1"},
    "m54": {"home_team": "Tunisia", "away_team": "Netherlands", "home_score": "1", "away_score": "3"},
    "m55": {"home_team": "Japan", "away_team": "Sweden", "home_score": "1", "away_score": "1"},
    "m56": {"home_team": "Türkiye", "away_team": "United States", "home_score": "3", "away_score": "2"},
    "m57": {"home_team": "Paraguay", "away_team": "Australia", "home_score": "0", "away_score": "0"},
    "m58": {"home_team": "Norway", "away_team": "France", "home_score": "1", "away_score": "4"},
    "m59": {"home_team": "Senegal", "away_team": "Iraq", "home_score": "5", "away_score": "0"},
    "m60": {"home_team": "Cape Verde", "away_team": "Saudi Arabia", "home_score": "0", "away_score": "0"},
    "m61": {"home_team": "Uruguay", "away_team": "Spain", "home_score": "0", "away_score": "1"},
    "m62": {"home_team": "New Zealand", "away_team": "Belgium", "home_score": "1", "away_score": "5"},
    "m63": {"home_team": "Egypt", "away_team": "Iran", "home_score": "1", "away_score": "1"},
    "m64": {"home_team": "Panama", "away_team": "England", "home_score": "0", "away_score": "2"},
    "m65": {"home_team": "Croatia", "away_team": "Ghana", "home_score": "2", "away_score": "1"},
    "m66": {"home_team": "Austria", "away_team": "Algeria", "home_score": "3", "away_score": "3"},
    "m67": {"home_team": "Colombia", "away_team": "Portugal", "home_score": "0", "away_score": "0"},
    "m68": {"home_team": "Jordan", "away_team": "Argentina", "home_score": "1", "away_score": "3"},
    "m70": {"home_team": "South Africa", "away_team": "Canada", "home_score": "0", "away_score": "1"},
    "m71": {"home_team": "Brazil", "away_team": "Japan", "home_score": "2", "away_score": "1"},
    "m72": {"home_team": "Germany", "away_team": "Paraguay", "home_score": "1", "away_score": "2"},
    "m73": {"home_team": "Netherlands", "away_team": "Morocco", "home_score": "1", "away_score": "2"},
    "m74": {"home_team": "Ivory Coast", "away_team": "Norway", "home_score": "1", "away_score": "2"},
    "m75": {"home_team": "France", "away_team": "Sweden", "home_score": "3", "away_score": "0"},
    "m76": {"home_team": "Mexico", "away_team": "Ecuador", "home_score": "2", "away_score": "0"},
    "m77": {"home_team": "England", "away_team": "DR Congo", "home_score": "2", "away_score": "1"},
    "m78": {"home_team": "Belgium", "away_team": "Senegal", "home_score": "3", "away_score": "2"},
    "m79": {"home_team": "United States", "away_team": "Bosnia", "home_score": "2", "away_score": "0"},
    "m80": {"home_team": "Spain", "away_team": "Austria", "home_score": "3", "away_score": "0"},
    "m81": {"home_team": "Portugal", "away_team": "Croatia", "home_score": "2", "away_score": "1"},
    "m82": {"home_team": "Switzerland", "away_team": "Algeria", "home_score": "2", "away_score": "0"},
    "m83": {"home_team": "Australia", "away_team": "Egypt", "home_score": "2", "away_score": "4"},
    "m84": {"home_team": "Argentina", "away_team": "Cape Verde", "home_score": "3", "away_score": "2"},
    "m85": {"home_team": "Colombia", "away_team": "Ghana", "home_score": "1", "away_score": "0"}
}

# Bumped cloud cache tracking path index tag to v13 to execute reset smoothly
DB_FILE = "online_sweepstake_v13.json"

def load_global_scores():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                live_data = json.load(f)
                if live_data:
                    return live_data
        except:
            pass
    return match_scores

def save_global_scores(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass

# Initialize session state variables cleanly
if "active_scores" not in st.session_state:
    st.session_state.active_scores = load_global_scores()

# --- 4. ADMIN PANEL SIDEBAR COMPONENT ---
st.sidebar.title("🔐 Admin Dashboard")
password = st.sidebar.text_input("Enter Passcode:", type="password")
is_admin = (password == "wimbledon2026")

if is_admin:
    st.sidebar.success("Access Granted!")
    
    # Collapsible Historical Referencing Header
    with st.sidebar.expander("📚 View Previous Historical Scores Reference"):
        for m_id, data in match_scores.items():
            active_ids = [m["id"] for day_fixtures in FIXTURES_BY_DAY.values() for m in day_fixtures]
            if m_id not in active_ids:
                h_name = data.get("home_team", data.get("home", "Unknown"))
                a_name = data.get("away_team", data.get("away", "Unknown"))
                st.markdown(
                    f"<p style='font-size: 0.9em; margin: 3px 0;'>"
                    f"🏆 {h_name} <b>{data.get('home_score', '-')}</b> v <b>{data.get('away_score', '-')}</b> {a_name}"
                    f"</p>", 
                    unsafe_allow_html=True
                )
    
    st.sidebar.markdown("## ✏️ Enter Active Fixtures")
    for day, matches in FIXTURES_BY_DAY.items():
        st.sidebar.markdown(f"### 📅 {day}")
        for match in matches:
            m_id = match["id"]
            
            if m_id not in st.session_state.active_scores:
                st.session_state.active_scores[m_id] = {"home_team": match["home"], "away_team": match["away"], "home_score": "-", "away_score": "-"}
                
            current_match_data = st.session_state.active_scores[m_id]
            
            col1, col2, col3, col4, col5 = st.sidebar.columns([3, 2, 1, 2, 3])
            options = ["-"] + [str(i) for i in range(15)]
            h_idx = options.index(current_match_data.get("home_score", "-")) if current_match_data.get("home_score", "-") in options else 0
            a_idx = options.index(current_match_data.get("away_score", "-")) if current_match_data.get("away_score", "-") in options else 0
            
            with col1:
                st.markdown(f"<p style='text-align: right; margin: 0; padding-top: 5px;'><b>{match['home']}</b></p>", unsafe_allow_html=True)
            with col2:
                h_score = st.selectbox(f"H#{m_id}", options, index=h_idx, label_visibility="collapsed")
            with col3:
                st.markdown("<p style='text-align: center; margin: 0; padding-top: 5px;'>v</p>", unsafe_allow_html=True)
            with col4:
                a_score = st.selectbox(f"A#{m_id}", options, index=a_idx, label_visibility="collapsed")
            with col5:
                st.markdown(f"<p style='text-align: left; margin: 0; padding-top: 5px;'><b>{match['away']}</b></p>", unsafe_allow_html=True)
                
            st.session_state.active_scores[m_id]["home_score"] = h_score
            st.session_state.active_scores[m_id]["away_score"] = a_score
            st.sidebar.markdown(f"<p style='text-align: center; font-size: 0.85em; color: gray;'>Kickoff: {match['time']}</p>", unsafe_allow_html=True)
            st.sidebar.markdown("---")
            
    if st.sidebar.button("💾 Save & Publish Scores Online", use_container_width=True):
        save_global_scores(st.session_state.active_scores)
        st.sidebar.success("Global Scoreboard Updated!")
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Emergency Cloud Backup Code")
    st.sidebar.code(json.dumps(st.session_state.active_scores))
else:
    st.sidebar.info("Family View: Keeping track live! Input fields are locked out.")

current_scores_dictionary = st.session_state.active_scores

# --- 5. STANDINGS LEAGUE CALCULATOR ---
stats = {name: {"Played": 0, "Wins": 0, "Draws": 0, "Losses": 0, "Points": 0} for name in SWEEPSTAKE_POOLS}
team_records = {}

for m_id, score_data in current_scores_dictionary.items():
    h_s = score_data.get("home_score", "-")
    a_s = score_data.get("away_score", "-")
    
    if h_s != "-" and a_s != "-":
        h_goals, a_goals = int(h_s), int(a_s)
        h_team = score_data.get("home_team", score_data.get("home", "Unknown"))
        a_team = score_data.get("away_team", score_data.get("away", "Unknown"))
        
        if h_team not in team_records: team_records[h_team] = []
        if a_team not in team_records: team_records[a_team] = []
        
        if h_goals > a_goals:
            team_records[h_team].append("W")
            team_records[a_team].append("L")
        elif a_goals > h_goals:
            team_records[h_team].append("L")
            team_records[a_team].append("W")
        else:
            team_records[h_team].append("D")
            team_records[a_team].append("D")

for participant, team_list in SWEEPSTAKE_POOLS.items():
    for team in team_list:
        outcomes = team_records.get(team, [])
        for outcome in outcomes:
            if outcome == "W":
                stats[participant]["Wins"] += 1
                stats[participant]["Points"] += 3
            elif outcome == "D":
                stats[participant]["Draws"] += 1
                stats[participant]["Points"] += 1
            elif outcome == "L":
                stats[participant]["Losses"] += 1
        
    stats[participant]["Played"] = stats[participant]["Wins"] + stats[participant]["Draws"] + stats[participant]["Losses"]

# --- 6. USER INTERFACE LAYOUT DISPLAY ---
st.title("🏆 Bartman Family World Cup Sweepstake Live Scoreboard")

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
            flag = FLAG_MAPPING.get(t, "🏳️")
            outcomes = team_records.get(t, [])
            status_text = f" **({', '.join(outcomes)})**" if outcomes else ""
            st.markdown(f"• {flag} {t}{status_text}")
