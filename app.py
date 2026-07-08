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

# --- 2. FIXTURES DICTIONARY (Current Active & Upcoming Knockout Phase Schedule) ---
FIXTURES_BY_DAY = {
    "Saturday, July 4": [
        {"id": "m86", "home": "Canada", "away": "Morocco", "time": "22:30"},
        {"id": "m87", "home": "Paraguay", "away": "France", "time": "02:30 (Sun)"}
    ],
    "Sunday, July 5": [
        {"id": "m88", "home": "Brazil", "away": "Norway", "time": "21:00"},
        {"id": "m89", "home": "Mexico", "away": "England", "time": "01:00 (Mon)"}
    ],
    "Monday, July 6": [
        {"id": "m90", "home": "Portugal", "away": "Spain", "time": "23:30"}
    ],
    "Tuesday, July 7": [
        {"id": "m91", "home": "United States", "away": "Belgium", "time": "04:30 (Wed)"},
        {"id": "m92", "home": "Argentina", "away": "Egypt", "time": "21:30"},
        {"id": "m93", "home": "Switzerland", "away": "Colombia", "time": "01:30 (Wed)"}
    ]
}

# --- 3. HARDCODED BASELINE DATA LAYER (Fully Unbroken Historical Match List) ---
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
    "m39": {"home_team": "France", "away_team": "Iraq", "home_score": "3", "away_score": "0"},
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
    "m51": {"home_team": "Czechia", "away_team": "Mexico", "home_score": "0",
