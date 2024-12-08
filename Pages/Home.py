import streamlit as st
import pandas as pd
from supabase import create_client
import uuid
import base64
import time
from extra_streamlit_components import CookieManager
from datetime import datetime
# Set page configuration

K = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZsdmlqcXplb3RkZGdjcG1zcWVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzNjY4NTksImV4cCI6MjA0Mzk0Mjg1OX0.8u3MtBSBvMEvKaNEB1srPnNlDljZtNtZcZP4AvpICMk'
A = 'https://vlvijqzeotddgcpmsqee.supabase.co/'


db = create_client(A,K)

st.set_page_config(
    page_title="Kent State University",
    page_icon="C:/Users/KOTA SRI SURYA TEJA/Desktop/K+Emblem/K Emblem/K Emblem PNGs/K_Emblem_RGB.png",
    initial_sidebar_state="auto",
    layout = 'centered'
)
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, .3), rgba(255, 255, 255, .4)), url("https://www-s3-live.kent.edu/s3fs-root/s3fs-public/athletic-wordmark.jpg");
        background-size: 40%;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: 55%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

cookie_manager = CookieManager()
cookies = cookie_manager.get_all()

#74c8d689-a70c-11ef-b645-0897987298c2

st.title("Kent State's Student Attendence")

# Initialize session state variables if they do not exist
st.session_state['goto'] = ''


# Create two columns for buttons and forms
bcol1, bcol2 = st.columns(2)

def find_address():
    mac = uuid.getnode()
    device_id = ':'.join(f"{(mac >> 8 * i) & 0xff:02x}" for i in reversed(range(6)))
    return device_id


def check_passwd(a):
    s=0
    if len(a)>=8 and len(a)<13:
        s+=1
    f=[]
    sym=['!','@','#','$','%','^','&','*','(',')']
    for i in a:
        if i.islower() and '1' not in f:
            f.append('1')
        elif i.isupper() and '2' not in f:
            f.append('2')
        elif i.isnumeric() and '3' not in f:
            f.append('3')
        elif i not in sym and '4' not in f:
            f.append('4')
    if len(f)!=4 or s!=1: 
        return 0
    return 1

# Admin section
with bcol1:
    bcol1.caption("Admin Access")
    # Display admin form if admin_b is True
    ad_name = bcol1.text_input("Admin Username",value="Mani369")
    ad_passwd = bcol1.text_input("Account Password", type='password',value="Mani")
    st.session_state['admin_submit'] = bcol1.button("Submit Admin")
    if 'admin_submit' in st.session_state and st.session_state.get('admin_submit'):
        db_res=pd.DataFrame(db.table('Admin').select('Name').eq('Username',ad_name).eq('Passwd',ad_passwd).execute().data)
        if len(db_res)>0:
            st.session_state['ad_usnm'] = ad_name
            st.session_state['Admin_login'] = True
            st.switch_page('pages/Dashboard.py')
        else:
            st.error("check the creds!!")
        
# Student section
with bcol2:
    # Student section
    option = bcol2.radio("Student", ('Login','Signup'), captions=["Already a Member?","Create your student account"],index=None)
    if option=='Login':
        st_ID = bcol2.text_input("ID",value="811262686")
        st_passwd = bcol2.text_input("Password", type='password',value='Mani')
        sub_b, for_b = bcol2.columns([.5,.5])
        if sub_b.button("Submit Student"):
            
            st.session_state["goto"] = None  # Hide the form after submission
            Dev_ID = cookies.get('Device_ID')
            db_res=pd.DataFrame(db.table('Students').select('*').eq('ID',st_ID).eq('Passwd',st_passwd).execute().data)
            c = db.table('Students').select('*').eq('Address',Dev_ID).execute().data
            if len(db_res)>0 and db_res['Address'][0]==Dev_ID and len(c)==1:
                find_address()
                st.session_state['st_ID']=st_ID
                st.session_state['Student_login']=True
                st.session_state['goto']='admin'
                st.switch_page("pages/Dashboard.py")
            else:
                st.error("Please check the Creds/Key")
        if for_b.button("Forgot/Generate?"):
            st.session_state['Key']=True
            db_res=pd.DataFrame(db.table('Students').select('*').eq('ID',st_ID).eq('Passwd',st_passwd).execute().data)
            if db_res['Status'][0]=='NOT REQUIRED':
                db.table("Students").update({'Status':'REQUIRED'}).eq('ID',st_ID).eq('Passwd',st_passwd).execute()
                cookie_manager.delete("Device_ID")
                bcol2.success("Request Submmitted!!")
                time.sleep(1)
                st.rerun()
            elif db_res['Status'][0]=='REQUIRED':
                bcol2.warning("Pending to approve!!")
                time.sleep(1)
                st.rerun()
            elif db_res['Status'][0]=='APPROVED':
                cookie_manager.set('Device_ID', str(uuid.uuid1()), expires_at=datetime.fromisoformat("2026-12-31T23:59:59"))
                r= db.table("Students").update({'Address':cookies.get('Device_ID'),'Status':'NOT REQUIRED'}).eq('ID',st_ID).eq('Passwd',st_passwd).execute()
                time.sleep(1)
                st.rerun()


    if option=='Signup':
        bcol2.warning("Please sign up from your permanent device")
        st_ID = bcol2.text_input("ID",value='811262689')
        st_passwd = bcol2.text_input("Password", type='password',value='Asdfgh1!')
        st_name = bcol2.text_input("Name",value='Steve')
        st_button = bcol2.button("Submit")
        if st_button:
            f=0
            if len(st_ID)!=9 or st_ID[:2]!='81':
                bcol2.warning("Please enter proper  student ID")
                f=1
            elif check_passwd(st_passwd)==0:
                bcol2.warning("! Password must contain atleast a uppercase, lowercase, numeric and special character")
                f=1
            else:
                add = base64.b64encode(find_address().encode()).decode('utf-8')
                db_res=pd.DataFrame(db.table('Students').select('*').eq('ID',st_ID).execute().data)
                db_res1=db.table('Students').select('*').eq('Address',add).execute().data
                if len(db_res)==0 and f==0 and db_res1:
                    db.table('Students').insert([{'ID':st_ID,'Passwd':st_passwd,'Name':st_name,'Address':add}]).execute()
                    bcol2.success(st_name+', your profile has been created')
                else:
                    bcol2.error("Student/Device is already registered")
            st.session_state["goto"] = 'admin'
