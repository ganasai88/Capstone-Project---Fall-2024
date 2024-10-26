import streamlit as st
from supabase import create_client
import httpx
import pandas as pd
import base64
import wave


K = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZsdmlqcXplb3RkZGdjcG1zcWVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzNjY4NTksImV4cCI6MjA0Mzk0Mjg1OX0.8u3MtBSBvMEvKaNEB1srPnNlDljZtNtZcZP4AvpICMk'
A = 'https://vlvijqzeotddgcpmsqee.supabase.co/'
db = create_client(A,K)
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), url("https://imgs.search.brave.com/KJm5w-cbELGkNcYvZ6RLPOkg9y9vZK_xGQGWeDH31N8/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly91cGxv/YWQud2lraW1lZGlh/Lm9yZy93aWtpcGVk/aWEvY29tbW9ucy9i/L2I2L1BlbmNpbF9k/cmF3aW5nX29mX2Ff/Z2lybF9pbl9lY3N0/YXN5LmpwZw");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.success('Hi')

# st.write("heyy!!!!")

# df = pd.DataFrame(db.table('Attendence').select('Audio').eq('Student ID','811262686').eq('Course ID','69098').execute().data)
# audio = base64.b64decode(df['Audio'][0])
# with wave.open('audio1.wav', 'wb') as wf:
#     wf.setnchannels(1)
#     wf.setsampwidth(2)
#     wf.setframerate(48000)
#     wf.writeframes(audio)
# st.audio('audio1.wav')
