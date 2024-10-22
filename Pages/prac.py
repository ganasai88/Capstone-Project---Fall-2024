import streamlit as st
from supabase import create_client
import httpx
import pandas as pd

K ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRneXphcXJyeHNqcXdsa2FucnFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY3MDI1NzIsImV4cCI6MjA0MjI3ODU3Mn0.gkOxXIxUR0axX5syhUhQlOBCTqodeMVkSu5YP_sUjJw"
A ="https://tgyzaqrrxsjqwlkanrqh.supabase.co/"

sp= create_client(A, K)

st.write("heyy!!!!")

df = pd.DataFrame(sp.table('status').select('*').execute().data)
st.write(df)
