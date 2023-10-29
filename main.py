import streamlit as st
import glob
import json

from api_connect import save_transcript

st.title('Welcome to Podcast Summary')

json_files = glob.glob('*json')

episode_id = st.sidebar.text_input('Please enter an Episode Id:')
button = st.sidebar.button("Download Episode summary", on_click=save_transcript, args=(episode_id,))


def get_clean_summary(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        start_t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_t = f'{minutes:02d}:{seconds:02d}'
    return start_t

if button:
    filename = episode_id + '_chapters.json'

    with open(filename, 'r') as f:
        data = json.load(f)

    chapters = data['chapters']
    podcast_title = data['podcast_title']
    episode_title = data['episode_title']
    thumbnail = data['thumbnail']
    audio = data['audio_url']

    st.header(f"{podcast_title} - {episode_title}")
    st.image(thumbnail, width=200)
    st.markdown(f'#### {episode_title}')

    for chap in chapters:
        with st.expander(chap['gist'] + ' - ' + get_clean_summary(chap['start'])):
            chap['summary']

