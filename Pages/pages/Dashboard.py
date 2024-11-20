import streamlit as st
from extra_streamlit_components import CookieManager
from datetime import datetime
import uuid

c = st.button("wanna fuck??")
print(uuid.uuid1())

# Initialize CookieManager
cookie_manager = CookieManager()

st.title("Cookie Management Example")

# Display all cookies
st.subheader("Current Cookies")
cookies = cookie_manager.get_all()
st.write(cookies)

# Set a cookie
if st.button("Set a Cookie"):
    cookie_manager.set("Device_ID", "74c8d689-a70c-11ef-b645-0897987298c2", expires_at=datetime.fromisoformat("2024-12-31T23:59:59"))
    st.success("Cookie has been set!")

# Get a specific cookie
st.subheader("Retrieve a Cookie")
cookie_name = st.text_input("Enter Cookie Name", "my_cookie")
if st.button("Get Cookie"):
    cookie_value = cookies.get(cookie_name)
    if cookie_value:
        st.success(f"Cookie Value: {cookie_value}")
    else:
        st.error("Cookie not found.")

# Delete a cookie
if st.button("Delete Cookie"):
    cookie_manager.delete("my_cookie")
    st.success("Cookie has been deleted.")
