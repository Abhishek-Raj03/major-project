import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import altair as alt
import streamlit.components.v1 as com
import json
from streamlit_lottie import st_lottie
import requests
# <iframe src="https://lottie.host/embed/a2273076-8992-4c74-a349-4d0d40b1624a/xhKS86kIkH.json"></iframe>
# <iframe src="https://lottie.host/embed/c1e4ea76-7beb-428d-ae94-c8ab019b24b4/Kug8BwWij8.json"></iframe>
st.set_page_config(page_title="FitnessTracker!!!", page_icon=":bar_chart:",layout="wide")
# com.iframe("https://lottie.host/embed/c1e4ea76-7beb-428d-ae94-c8ab019b24b4/Kug8BwWij8.json")
image_path = "feelings.png"

# Streamlit app
# st.title("Streamlit with PNG Image")

# Display the image
col1, col2 = st.columns((2))
with col1:
    st.title(" :bar_chart: Fitness Tracker")
    st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)
    # category = 'fitness'
    # api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    # response = requests.get(api_url, headers={'X-Api-Key': 'eQTly/BTtC/bl6t3APTDSg==zGUXnjnEXYfOkAnI'})
    # s = response.text
    # data = json.loads(s)
    # quote = data[0]['quote']
    # author = data[0]['author']
    quote="I think exercise tests us in so many ways, our skills, our hearts, our ability to bounce back after setbacks. This is the inner beauty of sports and competition, and it can serve us all well as adult athletes."
    author="Peggy Fleming"
    st.markdown(f'<span>{quote}</span><br><span><strong>- {author}</strong></span>',unsafe_allow_html=True)

with col2:
    # st.image(image_path, caption='Your Image Caption',width=200)
    with open("a1.json") as source:
        animation=json.load(source)
        st_lottie(animation,width=250,height=250)


# fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))

# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = pd.read_csv(filename, encoding = "ISO-8859-1")
# else:
    # os.chdir(r"C:\Users\AEPAC\Desktop\Streamlit")
df = pd.read_csv("users.csv", encoding = "ISO-8859-1")


df1 = pd.read_csv("daily.csv", encoding = "ISO-8859-1")


# with open('users.csv', 'r', newline='') as file:
# print(df[df["name"].unique()==name])
# print("----------------",name)



# Getting the min and max date 
startDate = pd.to_datetime(df1["date"]).min()
endDate = pd.to_datetime(df1["date"]).max()

col1, col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))


time_sum=df['time'].sum()
cal_sum=df['calorie_burnt'].sum()
col1, col2 = st.columns((2))
with col1:
    # st.header("Total Time Spend")
    st.markdown('<span style="color:Cyan; font-size: 35px">Total Time Spend</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="font-size:40px;">`{time_sum} mins`</span>', unsafe_allow_html=True)

with col2:
    # st.header("Total calorie burnt")
    st.markdown('<span style="color:orange; font-size: 35px">Total calorie burnt</span>', unsafe_allow_html=True)
    # st.subheader(f"`{cal_sum}`")
    st.markdown(f'<span style="font-size:40px;">`{cal_sum} cal`</span>', unsafe_allow_html=True)

    # st.subheader(str(cal_sum)+" cal")
time_df = df.groupby(by = ["name"], as_index = False)["time"].sum()
cal_df = df.groupby(by = ["name"], as_index = False)["calorie_burnt"].sum()
col1, col2 = st.columns((2))
with col1:
    st.subheader("User Vs Time")
    fig = px.bar(time_df, x = "name", y = "time", text = ['{:,} min'.format(x) for x in time_df["time"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)


with col2:
    st.subheader("User calorie burnt")
    fig = px.pie(cal_df, values = "calorie_burnt", names = "name", hole = 0.5)
    fig.update_traces(text = cal_df["name"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Download Time_ViewData"):
        st.write(time_df.style.background_gradient(cmap="Blues"))
        csv = time_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "time.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
        
with cl2:
    with st.expander("Download Calorie_ViewData"):
        st.write(cal_df.style.background_gradient(cmap="Blues"))
        csv = cal_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "calorie.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
st.sidebar.image("g3.gif", use_column_width=True)
name = st.sidebar.selectbox("Pick the User", df["name"].unique())
names = st.sidebar.multiselect("Compare Users", df["name"].unique())
# name=st.selectbox("Pick the User", df["name"].unique())
cal_df1=df1[df1['name']==name]
time_df1=df1[df1['name']==name]

col1, col2 = st.columns((2))
with col1:
    st.subheader(f"Past 7 days calorie burnt Report of Sushmit")
    # print("-----------")
    # print(cal_df1['id'].get(3))
    fig = px.bar(cal_df1, x = "date", y = "calorie", text = ['{:,} cal'.format(x) for x in cal_df1["calorie"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Past 7 days time spend Report of Sushmit")
    # st.write("##")
    # st.write("##")
    fig = px.bar(time_df1, x = "date", y = "time", text = ['{:,} min'.format(x) for x in time_df1["time"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)
    # chart=(alt.Chart(time_df1).mark_bar().encode(alt.X("date"),alt.Y("time"),alt.Color("date"),
    #                                              alt.Tooltip(["date","time"]),).interactive())
    # st.altair_chart(chart,use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander(f"Download {name} Data"):
        st.write(cal_df1.style.background_gradient(cmap="Blues"))
        csv = cal_df1.to_csv(index = False).encode('utf-8')
        st.download_button(f"Download now", data = csv, file_name = "time.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
        

st.subheader('Time Series Analysis of total calorie burnt by all users')
cal_df2=df1.groupby(by=["date"],as_index=False)["calorie"].sum()
fig3=px.line(cal_df2,x="date",y="calorie",height=500, width = 1000,template="gridon")
st.plotly_chart(fig3,use_container_width=True)


st.subheader('Time Series Analysis of total time spend by all users')
time_df2=df1.groupby(by=["date"],as_index=False)["time"].sum()
fig3=px.line(time_df2,x="date",y="time",height=500, width = 1000,template="gridon")
fig3.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play',
                                            method='animate', args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])])])

st.plotly_chart(fig3,use_container_width=True)



# sus=df1[df1['name']=='Sushmit']
# abhi=df1[df1['name']=='Abhishek Raj']
# cal_sus=sus.groupby(by=["date"],as_index=False)["calorie"].sum()
# cal_abhi=abhi.groupby(by=["date"],as_index=False)["calorie"].sum()
# st.subheader('Time Series Analysis of total calorie burnt by sushmit vs abhishek')
# fig3=px.line(cal_sus,cal_abhi,x="date",y="calorie",height=500, width = 1000,template="gridon")
# st.plotly_chart(fig3,use_container_width=True)

# fig = px.line(df1, x="date", y="calorie", height=500, width=1000, template="gridon", title="Calorie Comparison")
# df4=sus.groupby(by=["date"],as_index=False)["calorie"].sum()
# df5=abhi.groupby(by=["date"],as_index=False)["calorie"].sum()
# # df6=pd.DataFrame(df4,df5)
# df6 = pd.concat([df4, df5], axis=0)
# # st.line_chart(df6,x="date",y="calorie")
# st.line_chart(df6)
# Streamlit app
st.title('Calorie Burnt Line Race Graph')

# Select unique users
users = df1['name'].unique()

# Create a sidebar for user selection
selected_user = st.sidebar.selectbox('Select User', users)

# Filter data for the selected user
user_data = df1[df1['name'] == selected_user]

# Create line race graph
fig = px.line(user_data, x='date', y='calorie', title=f'Calorie Burnt Line Race - {selected_user}',
              labels={'calorie': 'Calorie Burnt', 'date': 'Date'})

# Add animation for line race effect
fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play',
                                            method='animate', args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])])])

frames = [dict(data=[dict(type='scatter', mode='lines', x=user_data['date'][:i+1], y=user_data['calorie'][:i+1])],
               traces=[0], name=f'Frame {i+1}') for i in range(len(user_data))]

fig.frames = frames

# Show the line race graph
st.plotly_chart(fig)