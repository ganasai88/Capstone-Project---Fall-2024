import streamlit as st
from supabase import create_client
import httpx
import pandas as pd
import base64
import wave


K = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZsdmlqcXplb3RkZGdjcG1zcWVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzNjY4NTksImV4cCI6MjA0Mzk0Mjg1OX0.8u3MtBSBvMEvKaNEB1srPnNlDljZtNtZcZP4AvpICMk'
A = 'https://vlvijqzeotddgcpmsqee.supabase.co/'
db = create_client(A,K)

st.write("heyy!!!!")

df = pd.DataFrame(db.table('Attendence').select('Audio').eq('Student ID','811262686').eq('Course ID','69098').execute().data)
audio = base64.b64decode(df['Audio'][0])
with wave.open('audio1.wav', 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(48000)
    wf.writeframes(audio)
st.audio('audio1.wav')
