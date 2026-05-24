import streamlit as st
from mood_detector import detect_mood
from music_recommender import search_tracks_by_mood
from utils import display_track_card

st.set_page_config(
    page_title="Mood Music Recommender",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Mood-Based Music Recommender")
st.markdown("Tell me how you're feeling, and I'll find the perfect songs for you.")

mood_input = st.text_area(
    "How are you feeling right now?",
    placeholder="e.g., I'm feeling energetic and ready to take on the world!",
    height=100
)

col1, col2 = st.columns([1, 2])
with col1:
    num_tracks = st.slider("Number of songs", min_value=5, max_value=20, value=10)
with col2:
    genre = st.selectbox(
        "Preferred genre (optional)",
        ["Any", "pop", "rock", "hip-hop", "jazz", "classical", "electronic", "r&b", "country"]
    )

if st.button("🎶 Find My Music", use_container_width=True):
    if not mood_input.strip():
        st.warning("Please describe your mood first!")
    else:
        with st.spinner("Analyzing your mood..."):
            mood_data = detect_mood(mood_input)

        st.subheader(f"Detected Mood: {mood_data['label'].capitalize()}")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Valence (Happiness)", f"{mood_data['valence']:.0%}")
        col_b.metric("Energy", f"{mood_data['energy']:.0%}")
        col_c.metric("Danceability", f"{mood_data['danceability']:.0%}")

        with st.spinner("Fetching music recommendations..."):
            query = f"{mood_data['label']} {genre if genre != 'Any' else ''}"
            from music_recommender import get_mixed_recommendations
            tracks = get_mixed_recommendations(mood_data["label"], limit=num_tracks)

        if tracks:
            st.subheader(f"🎧 {len(tracks)} Songs for Your Mood")
            for track in tracks:
                display_track_card(track)
        else:
            st.error("Could not fetch recommendations. Please check your Spotify API credentials.")

st.markdown("---")
st.caption("Powered by Spotify API & TextBlob NLP | Built with Streamlit")