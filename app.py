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
        {"id": "m35a", "home": "Ecuador", "away": "Curaçao", "time": "01:00"},
        {"id": "m35b", "home": "Tunisia", "away": "Japan", "time": "05:00"},
        {"id": "m35c", "home": "Spain", "away": "Saudi Arabia", "time": "17:00"},
        {"id": "m36a", "home": "Belgium", "away": "Iran", "time": "20:00"},
        {"id": "m36b", "home": "Uruguay", "away": "Cape Verde", "time": "23:00"}
    ],
    "Monday, June 22": [
        {"id": "m37", "home": "New Zealand", "away": "Egypt", "time": "02:00"},
        {"id": "m38", "home": "Argentina", "away": "Austria", "time": "18:00"},
        {"id": "m39", "home": "France", "away": "Iraq", "time": "22:00"}
    ],
    "Tuesday, June 23": [
        {"id": "m40", "home": "Norway", "away": "Senegal", "time": "01:00"},
        {"id": "m41", "home": "Jordan", "away": "Algeria", "time": "04:00"},
        {"id": "m42", "home": "Portugal", "away": "Uzbekistan", "time": "18:00"},
        {"id": "m43", "home": "England", "away": "Ghana", "time": "21:00"}
    ],
    "Wednesday, June 24": [
        {"id": "m44", "home": "Panama", "away": "Croatia", "time": "00:00"},
        {"id": "m45", "home": "Colombia", "away": "DR Congo", "time": "03:00"},
        {"id": "m46", "home": "Switzerland", "away": "Canada", "time": "20:00"},
        {"id": "m47", "home": "Bosnia", "away": "Qatar", "time": "20:00"},
        {"id": "m48", "home": "Morocco", "away": "Haiti", "time": "23:00"},
        {"id": "m49", "home": "Scotland", "away": "Brazil", "time": "23:00"}
    ],
    "Thursday, June 25": [
        {"id": "m50", "home": "South Africa", "away": "South Korea", "time": "02:00"},
        {"id": "m51", "home": "Czechia", "away": "Mexico", "time": "02:00"},
        {"id": "m52", "home": "Curaçao", "away": "Ivory Coast", "time": "21:00"},
        {"id": "m53", "home": "Ecuador", "away": "Germany", "time": "21:00"}
    ],
    "Friday, June 26": [
        {"id": "m54", "home": "Tunisia", "away": "Netherlands", "time": "00:00"},
        {"id": "m55", "home": "Japan", "away": "Sweden", "time": "00:00"},
        {"id": "m56", "home": "Türkiye", "away": "United States", "time": "03:00"},
        {"id": "m57", "home": "Paraguay", "away": "Australia", "time": "03:00"},
        {"id": "m58", "home": "Norway", "away": "France", "time": "20:00"},
        {"id": "m59", "home": "Senegal", "away": "Iraq", "time": "20:00"}
    ],
    "Saturday, June 27": [
        {"id": "m60", "home": "Cape Verde", "away": "Saudi Arabia", "time": "01:00"},
        {"id": "m61", "home": "Uruguay", "away": "Spain", "time": "01:00"},
        {"id": "m62", "home": "New Zealand", "away": "Belgium", "time": "04:00"},
        {"id": "m63", "home": "Egypt", "away": "Iran", "time": "04:00"},
        {"id": "m64", "home": "Panama", "away": "England", "time": "22:00"},
        {"id": "m65", "home": "Croatia", "away": "Ghana", "time": "22:00"}
    ],
    "Sunday, June 28": [
        {"id": "m66", "home": "DR Congo", "away": "Uzbekistan", "time": "00:00"},
        {"id": "m67", "home": "Colombia", "away": "Portugal", "time": "00:00"},
        {"id": "m68", "home": "Jordan", "away": "Argentina", "time": "03:00"},
        {"id": "m69", "home": "Algeria", "away": "Austria", "time": "03:00"}
    ]
}

# --- MASTER SCORE BACKUP (Native Python Dictionary Override) ---
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
    "m66": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m67": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m68": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m69": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}
}

# Emulated persistence functions to prevent structural layout errors down the line
saved_scores = match_scores

def load_global_scores():
    return match_scores

def save_global_scores(data):
    pass# --- MASTER SCORE BACKUP (Native Python Dictionary Override) ---
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
    "m66": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m67": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m68": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m69": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}
}

# Emulated persistence functions to prevent structural layout errors down the line
saved_scores = match_scores

def load_global_scores():
    return match_scores

def save_global_scores(data):
    pass# --- MASTER SCORE BACKUP (Native Python Dictionary Override) ---
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
    "m66": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m67": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m68": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}, 
    "m69": {"home_team": "-", "away_team": "-", "home_score": "-", "away_score": "-"}
}

# Emulated persistence functions to prevent structural layout errors down the line
saved_scores = match_scores

def load_global_scores():
    return match_scores

def save_global_scores(data):
    pass    # Save to temporary active memory
    with open(DB_FILE, "w") as f:
        json.dump(data, f)
saved_scores = load_global_scores()

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

# Calculate Standings (Fixed to accumulate multiple matches per team)
stats = {name: {"Played": 0, "Wins": 0, "Draws": 0, "Losses": 0, "Points": 0} for name in SWEEPSTAKE_POOLS}

# Change team_records to hold a list of results for each country
team_records = {}

for m_id, score_data in match_scores.items():
    h_s = score_data.get("home_score", "-")
    a_s = score_data.get("away_score", "-")
    
    if h_s != "-" and a_s != "-":
        h_goals, a_goals = int(h_s), int(a_s)
        
        h_team = score_data["home_team"]
        a_team = score_data["away_team"]
        
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
        # Loop through ALL recorded match outcomes for this country
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
        
    # Calculate total played cleanly from accumulated results
    stats[participant]["Played"] = stats[participant]["Wins"] + stats[participant]["Draws"] + stats[participant]["Losses"]

# Render Table Standings
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
            outcomes = team_records.get(t, [])
            status_text = f" **({" ,".join(outcomes)})**" if outcomes else ""
            st.markdown(f"• {flag}{status_text}")

# Emergency Cloud Backup section for the Admin
if is_admin:
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Emergency Cloud Backup")
    st.sidebar.write("If the server resets, copy this text block and paste it into MASTER_BACKUP_STRING on GitHub:")
    st.sidebar.code(json.dumps(match_scores))
