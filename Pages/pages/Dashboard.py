import streamlit as st
from PIL import Image
import pandas as pd
from supabase import create_client
from io import BytesIO
import time
import base64
import plotly.express as px
import plotly.graph_objects as go
from datetime import date,datetime,timedelta
from st_audiorec import st_audiorec
import wave
import numpy as np
import scipy.io.wavfile as wavf
from python_speech_features import mfcc
from sklearn.metrics.pairwise import cosine_similarity

K = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZsdmlqcXplb3RkZGdjcG1zcWVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzNjY4NTksImV4cCI6MjA0Mzk0Mjg1OX0.8u3MtBSBvMEvKaNEB1srPnNlDljZtNtZcZP4AvpICMk'
A = 'https://vlvijqzeotddgcpmsqee.supabase.co/'
db = create_client(A,K)

st.set_page_config(
    layout='wide',
    initial_sidebar_state = 'expanded'
)



def rem(c):
    tb = 'Students'
    col = 'ID'
    if c==2:
        tb = 'Admin'
        col = 'Username'
    db.table(tb).update({'Photo': None}).eq(col,ID).execute()
    st.rerun()

def pic_up(image,ID,c):
    tb = 'Students'
    col = 'ID'
    if c==2:
        tb = 'Admin'
        col = 'Username'
    image = base64.b64encode(image).decode('utf-8')
    db.table(tb).update({'Photo':image}).eq(col,ID).execute()

def pic_ret(ID,c):
    tb = 'Students'
    col = 'ID'
    if c==2:
        tb = 'Admin'
        col = 'Username'
    photo = pd.DataFrame(db.table(tb).select('Photo').eq(col,ID).execute().data)
    photo = base64.b64decode(photo['Photo'][0])
    return photo

LO = st.button("Log out")
profile,data = st.columns([0.2,0.8])

# Additional CSS styling
st.markdown(
    """
    <style>
    /* App Background */
    .stApp {
        background: linear-gradient(rgba(240, 248, 255, 0.9), rgba(230, 230, 250, 0.7)),
                    url("https://imgs.search.brave.com/vW6JK7sBhpNgmDbgRyWmLzGONQI6M3sUm6fUWiKUd6A/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTMw/ODk2MTM2Ny9waG90/by9rZW50LXN0YXRl/LXVuaXZlcnNpdHkt/Y2FtcHVzLW9oaW8t/dXNhLmpwZz9zPTYx/Mng2MTImdz0wJms9/MjAmYz1ZSDZBUF9W/YWVpVmJlVzZNWEo3/NF9IRkI0dTY2a0F2/cEQzYWNocjFBRTFz/PQ");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    
    /* Button Styling */
    .stButton button {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        border: 2px solid #0056b3;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #0056b3;
        border-color: #003c82;
    }
    
    /* Selectbox Styling */
    .stSelectbox div[data-baseweb="select"] {
        font-size: 16px;
        color: #333;
        background-color: rgba(255, 255, 255, 0.8);
        border: 2px solid #0056b3;
        border-radius: 8px;
        padding: 5px;
    }
    label[data-testid="stSelectboxLabel"] {
        font-size: 20px;
        color: #0056b3;
        font-weight: bold;
    }
    /* Markdown Text Styling */
    h1, h4 {
        text-align: center;
        font-family: Arial, sans-serif;
        color: #333;
    }
    hr {
        border: none;
        height: 2px;
        background-color: #007bff;
        width: 80%;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Now, you can keep the rest of your code as is.
# Your custom CSS styles will be applied to the app, giving it a more appealing look and feel.



def Feature(a):
    sr, val = wavf.read(a)
    val = mfcc(val,sr)
    return np.mean(val,axis=0)
    



if LO:
    st.session_state['st_ID'] = None
    st.session_state['Student_login'] =False
    st.session_state['ad_usnm'] = ""
    st.session_state['Admin_login'] =False
    if 'CW_sem' in st.session_state:
        del st.session_state['CW_sem']
    st.switch_page("Home.py")
    st.empty()
if "Student_login" and "st_ID" in st.session_state and st.session_state["Student_login"]==True:
    ID = st.session_state['st_ID']
    row = pd.DataFrame(db.table('Students').select('*').eq('ID',ID).execute().data)
    data.success("Welcome "+row['Name'][0]+'😄')

    ## upload option if it detects no photo in DB
    if row['Photo'][0]==None:
        ph = profile.empty()
        photo = ph.file_uploader('***upload photo***',)
        if photo:
            image = photo.read()
            pic_up(image,ID,1)
            ph.success("Photo Uploaded Successfully!!")
            time.sleep(1)
            ph.empty()
            profile.image(photo)
            pic_up = profile.button('Remove')
            if pic_up:
                rem(c=1)
    ### retrieves photo from DB
    else:
        ph = profile.empty()
        photo = Image.open(BytesIO(pic_ret(ID,1)))
        profile.image(photo)
        pic_del = profile.button('Remove')
        if pic_del:
            rem(c=1)
  
    ### Attendence section
    data.markdown("""
<h1 style="text-align: Center; font-family: Raleway;">Attendence</h1>
<hr style="width: 1400px; height: 3px; background-color: #007bff; border: none; margin: auto;">
""",unsafe_allow_html=True)
    
    _,at1,_,at2,_ =data.columns([.2,.2,.1,.2,.3])
    at1.markdown("""<h4>Select the course</h4>""",unsafe_allow_html=True)
    dt = date.today()
    a_ls = pd.DataFrame(db.table("Course Work").select('Course ID').eq('Status','TBA').eq('Student ID',ID).execute().data)
    a_cid = at1.selectbox("Select the course",a_ls['Course ID'])
    a_sb = at1.button('Verify')
    if a_sb:
        st.session_state['a_sb']=True
    if 'a_sb' in st.session_state and st.session_state['a_sb']==True:
        at2.markdown("""<h4>Record class audio to verify</h4>""",unsafe_allow_html=True)
        at_val = at2.experimental_audio_input("Record")
        if at_val:
            at_end = datetime.now()
            f,f1 = wavf.read(at_val)
            s = len(f1)/f
            at_start = at_end - timedelta(seconds=(len(f1)/f))
        at_sb = at2.button("Submit")
        if at_sb:
            st.session_state['at_sb']=True
        if 'at_sb' in st.session_state and st.session_state['at_sb']:
            dt = dt.strftime("%Y/%m/%d")
            a_p_id = db.table('Professors').select('Professor ID').eq('Course ID',a_cid).execute().data
            at_p_val = db.table('PF_Attendence').select('*').eq('Professor ID',int(a_p_id[0]['Professor ID'])).eq('Date',dt).execute().data
            
            if len(at_p_val):
                
                audio = base64.b64decode(at_p_val[0]['Audio'])
                with wave.open('Professor.wav', 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(48000)
                    wf.writeframes(audio)
                    wf.close()
                with wave.open('Student.wav', 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(48000)
                    wf.writeframes(f1)
                    wf.close()
                
                chc = db.table('Attendence').select('*').eq('Student ID',ID).eq('Date',dt).eq('Course ID',int(a_cid)).execute().data
                if len(chc)==0:
                    at_end = datetime.strftime(at_end,'%H:%M:%S.%f')
                    at_start = datetime.strftime(at_start,'%H:%M:%S.%f')
                    at_start = datetime.strptime(at_start,'%H:%M:%S.%f')
                    at_end=datetime.strptime(at_end,'%H:%M:%S.%f')
                    at_end_p=datetime.strptime(at_p_val[0]['Time_End'],'%H:%M:%S.%f')
                    at_start_p=datetime.strptime(at_p_val[0]['Time_Start'],'%H:%M:%S.%f')
                    tol_s= at_end-at_end_p
                    if tol_s<timedelta(seconds=10):
                        at2.success('In time')
                        time.sleep(1)
                    else:
                        db.table('Attendence').insert([{'Date':dt,'Student ID':ID,'Course ID':int(a_cid),'Attendence': 'NO',"Time_Start":at_start.strftime('%H:%M:%S.%f'),"Time_End":at_end.strftime('%H:%M:%S.%f')}]).execute()
                        at2.error('Sorry not in time')
                        time.sleep(1)
                        del st.session_state['at_sb']
                        del st.session_state['a_sb']
                        st.rerun()
                    if (at_end_p-at_start_p)/(at_end-at_start)>1:
                        db.table('Attendence').insert([{'Date':dt,'Student ID':ID,'Course ID':int(a_cid),'Attendence': 'NO',"Time_Start":at_start.strftime('%H:%M:%S.%f'),"Time_End":at_end.strftime('%H:%M:%S.%f')}]).execute()
                        at2.error('Sorry Insufficient audio to analyse')
                        time.sleep(1)
                        del st.session_state['at_sb']
                        del st.session_state['a_sb']
                        st.rerun()
                    pro = Feature('Professor.wav')
                    stu = Feature('Student.wav')
                    AT = "NO"
                    confidence = cosine_similarity(np.reshape(pro,(1,-1)),np.reshape(stu,(1,-1)))[0][0]
                    print(confidence)
                    if confidence>.70:
                        AT = "YES"
                        r = db.table('Attendence').insert([{'Date':dt,'Student ID':ID,'Course ID':int(a_cid),'Attendence': AT,"Time_Start":at_start.strftime('%H:%M:%S.%f'),"Time_End":at_end.strftime('%H:%M:%S.%f')}]).execute()                    
                    if AT=='YES':
                        at2.success("Recorded successfully")
                    else:
                        at2.warning('Marked as Absent')
                    r = db.table('Attendence').insert([{'Date':dt,'Student ID':ID,'Course ID':int(a_cid),'Attendence': AT,"Time_Start":at_start.strftime('%H:%M:%S.%f'),"Time_End":at_end.strftime('%H:%M:%S.%f')}]).execute()
                    time.sleep(1)
                else:
                    at2.warning('Attendence taken already')
                    time.sleep(1)
            else:
                at2.warning("Try Again")
            del st.session_state['a_sb']
            del st.session_state['at_sb']
            st.rerun()
    
    data.markdown("""
<h1 style="text-align: Center; font-family: Raleway;">Send Message</h1>
<hr style="width: 1400px; height: 3px; background-color: #007bff; border: none; margin: auto;">
""",unsafe_allow_html=True)
    
    _,at11,_,at22,_ = data.columns([.2,.2,.1,.2,.3])
    at11.markdown("""<h4>Select the course</h4>""",unsafe_allow_html=True)
    r=pd.DataFrame(db.table('Course Work').select('Course ID').eq('Student ID',ID).eq('Status','TBA').execute().data)
    if len(r)>0:
        mcc = at11.selectbox('Course',r['Course ID'])
        if at11.button('Fetch'):
            st.session_state['mcc']=True
    if 'mcc' in st.session_state and st.session_state['mcc']:
        at22.markdown("""<h4>Write the message</h4>""",unsafe_allow_html=True)
        msg = at22.text_area("Message")
        if at22.button('send'):
            db.table('Message').insert([{'Course ID': int(mcc),'Student ID':int(ID),'Message':msg,'Status':'Unread'}]).execute()
            at22.success('Sent the Message!!')
            time.sleep(1)
            del st.session_state['mcc']
            st.rerun()

elif "Admin_login" and "ad_usnm" in st.session_state and st.session_state["Admin_login"]==True:
    ID = st.session_state['ad_usnm']
    row = pd.DataFrame(db.table('Admin').select('*').eq('Username',ID).execute().data)
    data.success("Welcome "+row['Name'][0]+'😄')
    ## Profile Picture
    if row['Photo'][0]==None:
        ph = profile.empty()
        photo = ph.file_uploader('***upload photo***',)
        if photo:
            image = photo.read()
            pic_up(image,ID,2)
            ph.success("Photo Uploaded Successfully!!")
            time.sleep(1)
            ph.empty()
            profile.image(photo)
            pic_del = profile.button('Remove')
            if pic_del:
                rem(c=2)
    else:
        ph = profile.empty()
        photo = Image.open(BytesIO(pic_ret(ID,2)))
        profile.image(photo)
        pic_del = profile.button('Remove')
        if pic_del:
            rem(c=2)

    ## Attendence
    data.markdown("""
<h1 style="text-align: Center; font-family: Raleway;">Attendence</h1>
<hr style="width: 1400px; height: 3px; background-color: #007bff; border: none; margin: auto;">
""",unsafe_allow_html=True)

    _,at1,_,at2,_ =data.columns([.1,.2,.1,.3,.3])
    at1.markdown("""<h4>Select Course ID to take Attendence</h4>""",unsafe_allow_html=True)
    ls = pd.DataFrame(db.table('Professors').select('Course ID').eq('Professor ID',row['Professor ID'][0]).execute().data)
    at_ch=at1.selectbox("Enter",(ls['Course ID']))
    dt = date.today()
    if at1.button("Proceed"):
        st.session_state['ad_at'] = True
    if 'ad_at' in st.session_state and st.session_state['ad_at']==True:
        at2.markdown("""<h4>Record class audio to verify</h4>""",unsafe_allow_html=True)
        ad_val = at2.experimental_audio_input("Record")
        if ad_val:
            at_end=datetime.now()
            f,f1 = wavf.read(ad_val)
            at_start = at_end - timedelta(seconds=(len(f1)/f))
        ad_sb = at2.button("Upload")
        if ad_sb:
            st.session_state['ad_sb']=True
        if 'ad_sb' in st.session_state and st.session_state['ad_sb']==True:
            dt = dt.strftime("%Y/%m/%d")
            chc = db.table('Professors').select('Course ID').eq('Professor ID',row['Professor ID'][0]).execute().data
            chc2 = db.table('PF_Attendence').select('*').eq('Professor ID',row['Professor ID'][0]).eq('Date',dt).eq('Course ID',at_ch).execute().data
            if len(chc2)>0:
                st.session_state['at_ch']=True
            if 'at_ch' in st.session_state and st.session_state['at_ch']:
                at1.write("Want to Overwrite?")
                ch = at1.radio(label="Want to Overwrite?",options=['Overwrite','Deny it'])
                at_ch_sb1 = at1.button('Proceed!!')
                if at_ch_sb1 and ch=='Overwrite':
                    res=db.table('PF_Attendence').delete().eq('Professor ID',row['Professor ID'][0]).eq('Date',dt).eq('Course ID',at_ch).execute().data
                    del st.session_state['at_ch']
                    st.rerun()
                if at_ch_sb1 and ch=='Deny it':
                    del st.session_state['at_ch']
                    del st.session_state['ad_sb']
                    del st.session_state['ad_at']
                    st.rerun()

            else:
                ad_val = wave.open(ad_val,'rb')
                ad_f = ad_val.getnframes()
                ad_fr = ad_val.getframerate()
                ad_d = ad_f/float(ad_fr)
                ad_val = ad_val.readframes(ad_f)
                ad_val = base64.b64encode(ad_val).decode('utf-8')
                at_end=at_end.strftime('%H:%M:%S.%f')
                at_start=at_start.strftime('%H:%M:%S.%f')
                r = db.table('PF_Attendence').insert([{'Date':dt,'Professor ID':int(row['Professor ID'][0]),'Course ID':int(at_ch),'Audio':ad_val,"Time_Start":at_start,"Time_End":at_end}]).execute()
                at2.success("Recorded successfully")
                time.sleep(1)
                del st.session_state['ad_at']
                del st.session_state['ad_sb']
                st.rerun()
    _,at11,_,at22,_ =data.columns([.1,.2,.1,.3,.3])
    at11.markdown("""<h4>Change in Attendence?</h4>""",unsafe_allow_html=True)
    at_sb_ch = at11.selectbox("Select",ls['Course ID'])
    at_ID = at11.text_input("Enter Student ID")
    at_op = at11.selectbox('select the option',['Change in Attendence','Approval Key','List out - Attended','List out - Absent','Delete a record'])
    at_ch_sb = at11.button("Fetch")
    if at_ch_sb:
        st.session_state['at_ch_ab']=True
    if 'at_ch_ab' in st.session_state and st.session_state['at_ch_ab']==True:
        if at_op=='Change in Attendence':
            if at_ID:
                r = pd.DataFrame(db.table('Attendence').select('*').eq('Student ID',int(at_ID)).eq('Course ID',int(at_sb_ch)).eq('Student ID',int(at_ID)).execute().data)
                at22.write(r)
                at_sno = at22.text_input("Enter S.No ID")
                at_c = at22.selectbox("select",['YES','NO'])
                if at22.button('Change'):
                    r=db.table('Attendence').update({'Attendence':at_c}).eq('ID',int(at_sno)).execute()
                    if len(r):
                        at22.success('Updated!!')
                    else:
                        at22.warning('Record not found')
            else:
                at22.warning('Fill the Student ID!!')
            time.sleep(1)
            del st.session_state['at_ch_ab']
        elif at_op=='Approval Key':
            r = db.table('Students').select('Status').eq('ID',int(at_ID)).execute().data
            print(r)
            if r[0]['Status']=='REQUIRED':
                r = db.table('Students').update({'Status':'APPROVED'}).eq('ID',int(at_ID)).execute()
                if r:
                    at11.success('Approved!!')
                    time.sleep(1)
            else:
                at11.warning('No need to Approve!!')
                time.sleep(1)
                del st.session_state['at_ch_ab']
        elif at_op=='Approval Key':
            r = db.table('Students').select('Status').eq('ID',int(at_ID)).execute().data
            if r[0]['Status']=='REQUIRED':
                r = db.table('Students').update({'Status':'APPROVED'}).eq('ID',int(at_ID)).execute()
                if r:
                    at11.success('Approved!!')
                    time.sleep(1)
            else:
                at11.warning('No need to Approve!!')
                time.sleep(1)
            del st.session_state['at_ch_ab']
            st.rerun()
        elif at_op=='List out - Attended':
            if at_ID:
                r = pd.DataFrame(db.table('Attendence').select('*').eq('Student ID',int(at_ID)).eq('Course ID',int(at_sb_ch)).eq('Attendence','YES').execute().data)
                if len(r):
                    at22.success(at_ID+' Attendence history')
                else:
                    at22.error('No records found!!')
            else:
                r = pd.DataFrame(db.table('Attendence').select('*').eq('Course ID',int(at_sb_ch)).eq('Attendence','YES').execute().data)
            if len(r)>0:
                at22.write(r)
                if at22.button('Done?'):
                    del st.session_state['at_ch_ab']
                    st.rerun()
        elif at_op=='List out - Absent':
            if at_ID:
                r = pd.DataFrame(db.table('Attendence').select('*').eq('Student ID',int(at_ID)).eq('Course ID',int(at_sb_ch)).eq('Attendence','NO').execute().data)
                if len(r):
                    at22.error(at_ID+' Attendence history')
                else:
                    at22.error('No records found!!')
            else:
                r = pd.DataFrame(db.table('Attendence').select('*').eq('Course ID',int(at_sb_ch)).eq('Attendence','NO').execute().data)
            if len(r)>0:
                at22.write(r)
                if at22.button('Done?'):
                    del st.session_state['at_ch_ab']
                    st.rerun()
        elif at_op=='Delete a record':
            r = pd.DataFrame(db.table('Attendence').select('*').eq('Course ID',int(at_sb_ch)).eq('Student ID',int(at_ID)).execute().data)
            at22.write(r)
            at_sno = at22.text_input("Enter ID.no")
            at_c = at22.selectbox("select",['Delete Record','Cancel Operation'])
            if at22.button('Apply'):
                if at_c=='Delete Record':
                    r=db.table('Attendence').delete().eq('ID',int(at_sno)).execute().data
                    if len(r)>0:
                        at22.success('Deleted!!')
                    else:
                        at22.warning("Record not found")
                    time.sleep(1)
                del st.session_state['at_ch_ab']
        
    data.markdown("""
<h1 style="text-align: Center; font-family: Raleway;">Notification Inbox</h1>
<hr style="width: 1400px; height: 3px; background-color: #007bff; border: none; margin: auto;">
""",unsafe_allow_html=True)
    
    _,ad11,_,ad22,_ =data.columns([.1,.2,.1,.3,.3])
    ad11.markdown("""<h4>Select the Student ID</h4>""",unsafe_allow_html=True)
    res = pd.DataFrame(db.table('Message').select('Student ID').execute().data)
    IDs = res['Student ID'].unique()
    res = pd.DataFrame(db.table('Students').select('Name').in_('ID',IDs).execute().data)
    ops=res['Name']+'-'+str(IDs)
    
    mc = ad11.selectbox('Select the ID',ops)
    mc1 = ad11.selectbox('choose',['Read','Unread'])
    if ad11.button('Fetch!'):
        for i,j in zip(list(res['Name']),list(IDs)):
           print(i,j)
        mc = int(mc)
        st.session_state['fetch']=True
    if 'fetch' in st.session_state and st.session_state['fetch']:
        res = pd.DataFrame(db.table('Message').select('*').eq('Student ID',mc).eq('Status',mc1).execute().data)
        ad22.markdown("""<h4>Select the ID to view the Message</h4>""",unsafe_allow_html=True)
        if len(res)>0:
            msg_ch = ad22.selectbox("select",res['ID'])
            if ad22.button('view'):
                st.session_state['view']=True
        else:
            ad22.warning("Sorry no messages found!!")
            time.sleep(1)
            del st.session_state['fetch']
            st.rerun()
    if 'view' in st.session_state and st.session_state['view']:
        l = res[res['ID']==msg_ch]['Message'].tolist()
        ad22.write(l[0])
        adch = ad22.selectbox('choose',['-','Mark as Read','Leave unread'])
        if ad22.button('Submit!'):
            st.session_state['RU']=True
    if 'RU' in st.session_state and st.session_state['RU']:
        if adch=='Mark as Read':
            #db.table(tb).update({'Photo':image}).eq(col,ID).execute()
            db.table('Message').update({'Status':'Read'}).eq('ID',msg_ch).execute()
        elif adch=='Leave unread':
            db.table('Message').update({'Status':'Unread'}).eq('ID',msg_ch).execute()
        else:
            pass
        del st.session_state['RU']
        del st.session_state['fetch']
        del st.session_state['view']
        st.rerun()
    
    
else:
    profile.warning("Show yourself!!")
