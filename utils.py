import streamlit as st


def ms_to_duration(ms: int) -> str:
    """Convert milliseconds to m:ss format."""
    seconds = ms // 1000
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def display_track_card(track: dict):
    """Render a styled track card in Streamlit."""
    with st.container():
        col1, col2 = st.columns([1, 4])

        with col1:
            if track.get("image"):
                st.image(track["image"], width=80)
            else:
                st.markdown("🎵")

        with col2:
            st.markdown(f"**[{track['name']}]({track['url']})**")
            st.markdown(f"🎤 {track['artist']} · 💿 {track['album']}")

            meta_cols = st.columns(3)
            meta_cols[0].caption(f"⏱ {ms_to_duration(track['duration_ms'])}")
            meta_cols[1].caption(f"🔥 Popularity: {track['popularity']}/100")

            if track.get("preview_url"):
                meta_cols[2].caption("▶ Preview available")
                st.audio(track["preview_url"], format="audio/mp3")

        st.divider()