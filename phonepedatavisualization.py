#-----------------------------------------------------------------------------------------#
# PhonePe Data Visualization using Plotly and Streamlit                                   #
#-----------------------------------------------------------------------------------------#
# The data stored in MySQL are fetched and loaded into pandas data frame                  #
# Stremlit is used to build th page to select the criteria used to filter the data        #
# Plotly is used to visualize the data ascharts and it will be shown in streamlit web page#
#-----------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------#
# Import the required components                                                          #
#-----------------------------------------------------------------------------------------#
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json

#-----------------------------------------------------------------------------------------#
# Connect to MySQL DB and select the DB required                                          # 
#-----------------------------------------------------------------------------------------#
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="give your mysql password"
)
cursor = conn.cursor()
cursor.execute("use phonepe")

#-----------------------------------------------------------------------------------------#
# Fetch all the tables from MySQL and losd into data frame for chart analysis             # 
#-----------------------------------------------------------------------------------------#
#-----------------------------------#
#  aggregate insurance dataframe    #
#-----------------------------------#
query = "SELECT * FROM aggregate_insurance"
aggregate_insurance_df = pd.read_sql(query, conn)
print(aggregate_insurance_df)

#-----------------------------------#
# aggregate transaction dataframe   #
#-----------------------------------#
query = "SELECT * FROM aggregate_transaction"
aggregate_transaction_df = pd.read_sql(query, conn)
print(aggregate_transaction_df)

#-----------------------------------#
# aggregate user dataframe          #
#-----------------------------------#
query = "SELECT * FROM aggregate_user"
aggregate_user_df = pd.read_sql(query, conn)
print(aggregate_user_df)

#-----------------------------------#
# map insurance dataframe           #
#-----------------------------------#
query = "SELECT * FROM map_insurance"
map_insurance_df = pd.read_sql(query, conn)
print(map_insurance_df)

#-----------------------------------#
# map transaction dataframe         #
#-----------------------------------#
query = "SELECT * FROM map_transaction"
map_transaction_df = pd.read_sql(query, conn)
print(map_transaction_df)

#-----------------------------------#
# map user dataframe                #
#-----------------------------------#
query = "SELECT * FROM map_user"
map_user_df = pd.read_sql(query, conn)
print(map_user_df)

#-----------------------------------#
# top insurance dataframe           #
#-----------------------------------#
query = "SELECT * FROM top_insurance"
top_insurance_df = pd.read_sql(query, conn)
print(top_insurance_df)

#-----------------------------------#
# top transaction dataframe         #
#-----------------------------------#
query = "SELECT * FROM top_transaction"
top_transaction_df = pd.read_sql(query, conn)
print(top_transaction_df)

#-----------------------------------#
# top user dataframe                #
#-----------------------------------#
query = "SELECT * FROM top_user"
top_user_df = pd.read_sql(query, conn)
print(top_user_df)

#-----------------------------------------------------------------------------------------#
#  These are Function to fectch details from data frame and make plots accordingly        # 
#-----------------------------------------------------------------------------------------#
#--------------------------------------------------------#
# Transaction amount and count abased on year            #
#--------------------------------------------------------#
def transaction_amount_count_year(df, year):

    tacy= df[df["Year"] == year]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    fig_amount= px.bar(tacyg, x="State", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 700,width= 850)
    st.plotly_chart(fig_amount)

    fig_count= px.bar(tacyg, x="State", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 700, width= 850)
    st.plotly_chart(fig_count)

    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    states_name= []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                            color= "Transaction_amount", color_continuous_scale= "Viridis",
                            range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                            hover_name= "State", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                            height= 700,width= 850)
    fig_india_1.update_geos(visible= False)
    st.plotly_chart(fig_india_1)

    fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                            color= "Transaction_count", color_continuous_scale= "Tealrose",
                            range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                            hover_name= "State", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                            height= 700,width= 850)
    fig_india_2.update_geos(visible= False)
    st.plotly_chart(fig_india_2)

    return tacy

#--------------------------------------------------------#
# Transaction amount and count abased on year & quarter  #
#--------------------------------------------------------#
def transaction_amount_count_year_quarter(df, quarter):
    tacy= df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    fig_amount= px.bar(tacyg, x="State", y="Transaction_amount", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 700,width= 850)
    st.plotly_chart(fig_amount)

    fig_count= px.bar(tacyg, x="State", y="Transaction_count", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Bluered_r, height= 700,width= 850)
    st.plotly_chart(fig_count)

    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    states_name= []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                            color= "Transaction_amount", color_continuous_scale= "Rainbow",
                            range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                            hover_name= "State", title= f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                            height= 700,width= 850)
    fig_india_1.update_geos(visible= False)
    st.plotly_chart(fig_india_1)

    fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                            color= "Transaction_count", color_continuous_scale= "Rainbow",
                            range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                            hover_name= "State", title= f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                            height= 700,width= 850)
    fig_india_2.update_geos(visible= False)
    st.plotly_chart(fig_india_2)

    return tacy
            
#--------------------------------------------------------#
# Transaction type                                       #
#--------------------------------------------------------#            
def aggregate_transaction_Transaction_type(df, state):
    tacy= df[df["State"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width= 850, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
    st.plotly_chart(fig_pie_1)


    fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width= 850, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
    st.plotly_chart(fig_pie_2)

#--------------------------------------------------------#
# Agrregare user analysis 1                              #
#--------------------------------------------------------# 
def aggregate_user_plot_1(df, year):
    aguy= df[df["Year"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 850, color_discrete_sequence= px.colors.sequential.Greens_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#--------------------------------------------------------#
# Agrregare user analysis 2                              #
#--------------------------------------------------------# 
def aggregate_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title=  f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 850, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#--------------------------------------------------------#
# Agrregare user analysis 3                              #
#--------------------------------------------------------# 
def aggregate_user_plot_3(df, state):
    auyqs= df[df["State"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 850, markers= True)
    st.plotly_chart(fig_line_1)

#--------------------------------------------------------#
# Map insurance Districts                                #
#--------------------------------------------------------# 
def map_insurance_district(df, state):

    tacy= df[df["State"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    fig_bar_1= px.bar(tacyg, x= "Districts", y= "Transaction_amount", width= 850, 
                    title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r,hover_name="Districts")
    st.plotly_chart(fig_bar_1)

    fig_bar_2= px.bar(tacyg, x= "Districts", y= "Transaction_count", width= 850,
                    title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r,hover_name="Districts")
    st.plotly_chart(fig_bar_2)

#--------------------------------------------------------#
# Map user analysis 1                                    #
#--------------------------------------------------------#
def map_user_plot_1(df, year):
    muy= df[df["Year"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("State")[["Registered_user", "App_opens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "State", y= ["Registered_user", "App_opens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 850, height= 700, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

#--------------------------------------------------------#
# Map user analysis 2                                    #
#--------------------------------------------------------#
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("State")[["Registered_user", "App_opens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "State", y= ["Registered_user", "App_opens"],
                        title= f"{df['Year'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width= 850, height= 700, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#--------------------------------------------------------#
# Map user analysis 3                                    #
#--------------------------------------------------------#
def map_user_plot_3(df, states):
    muyqs= df[df["State"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    fig_map_user_bar_1= px.bar(muyqs, x= "Districts", y= "Registered_user", width=850,
                            title= f"{states.upper()} REGISTERED USER", height= 700, color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2= px.bar(muyqs, x= "Districts", y= "App_opens", width=850,
                            title= f"{states.upper()} APPOPENS", height= 700, color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_map_user_bar_2)

#--------------------------------------------------------#
# Top insurance analysis 1                               #
#--------------------------------------------------------#
def top_insurance_plot_1(df, state):
    tiy= df[df["State"]== state]
    tiy.reset_index(drop= True, inplace= True)

    fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                            title= "TRANSACTION AMOUNT", height= 700,width= 850, color_discrete_sequence= px.colors.sequential.GnBu_r)
    st.plotly_chart(fig_top_insur_bar_1)

    fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                            title= "TRANSACTION COUNT", height= 700,width= 850, color_discrete_sequence= px.colors.sequential.Agsunset_r)
    st.plotly_chart(fig_top_insur_bar_2)

#--------------------------------------------------------#
# Top user analysis 1                                    #
#--------------------------------------------------------#
def top_user_plot_1(df, year):
    tuy= df[df["Year"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["State","Quarter"])["Registered_user"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "State", y= "Registered_user", color= "Quarter", width= 850, height= 700,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "State",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#--------------------------------------------------------#
# Top user analysis  2                                   #
#--------------------------------------------------------#
def top_user_plot_2(df, state):
    tuys= df[df["State"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quarter", y= "Registered_user", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 850, height= 700, color= "Registered_user", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)

#--------------------------------------------------------#
# Top transaction amount question                        #
#--------------------------------------------------------#
def top_chart_transaction_amount(table_name):
    query1= f'''SELECT State, SUM(Transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY State
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    fig_amount= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 700,width= 850)
    st.plotly_chart(fig_amount)

    query2= f'''SELECT State, SUM(Transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY State
                ORDER BY Transaction_amount
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))
    
    fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_2)

    query3= f'''SELECT State, AVG(Transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY State
                ORDER BY Transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_3)


#--------------------------------------------------------#
# Top transaction count question                         #
#--------------------------------------------------------#
def top_chart_transaction_count(table_name):
    query1= f'''SELECT State, SUM(Transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY State
                ORDER BY Transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))


    fig_amount= px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 700,width= 850)
    st.plotly_chart(fig_amount)

    query2= f'''SELECT State, SUM(Transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY State
                ORDER BY Transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))


    fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_2)

    query3= f'''SELECT State, AVG(Transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY State
                ORDER BY Transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_3)

#--------------------------------------------------------#
# Top reistered user question                            #
#--------------------------------------------------------#
def top_chart_registered_user(table_name, state):
    query1= f'''SELECT Districts, SUM(Registered_user) AS registereduser
                FROM {table_name}
                WHERE State= '{state}'
                GROUP BY Districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()

    df_1= pd.DataFrame(table_1, columns=("districts", "registereduser"))

    fig_amount= px.bar(df_1, x="districts", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 700,width= 850)
    st.plotly_chart(fig_amount)

    query2= f'''SELECT Districts, SUM(Registered_user) AS registereduser
                FROM {table_name}
                WHERE State= '{state}'
                GROUP BY Districts
                ORDER BY registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()

    df_2= pd.DataFrame(table_2, columns=("districts", "registereduser"))

    fig_amount_2= px.bar(df_2, x="districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_2)

    query3= f'''SELECT Districts, AVG(Registered_user) AS registereduser
                FROM {table_name}
                WHERE State= '{state}'
                GROUP BY Districts
                ORDER BY registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()

    df_3= pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3= px.bar(df_3, y="districts", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_3)

#--------------------------------------------------------#
# Top appopnes question                                  #
#--------------------------------------------------------#
def top_chart_appopens(table_name, state):
    query1= f'''SELECT Districts, SUM(App_opens) AS appopens
                FROM {table_name}
                WHERE State= '{state}'
                GROUP BY Districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()

    df_1= pd.DataFrame(table_1, columns=("districts", "appopens"))

    fig_amount= px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 700,width= 850)
    st.plotly_chart(fig_amount)

    query2= f'''SELECT Districts, SUM(App_opens) AS appopens
                FROM {table_name}
                WHERE State= '{state}'
                GROUP BY Districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()

    df_2= pd.DataFrame(table_2, columns=("districts", "appopens"))

    fig_amount_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_2)

    query3= f'''SELECT Districts, AVG(App_opens) AS appopens
                FROM {table_name}
                WHERE State= '{state}'
                GROUP BY Districts
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()

    df_3= pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_3)

#--------------------------------------------------------#
# Top registered user question                           #
#--------------------------------------------------------#
def top_chart_registered_users(table_name):
    query1= f'''SELECT State, SUM(Registered_user) AS registeredusers
                FROM {table_name}
                GROUP BY State
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()

    df_1= pd.DataFrame(table_1, columns=("states", "registeredusers"))

    fig_amount= px.bar(df_1, x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 700,width= 850)
    st.plotly_chart(fig_amount)

    query2= f'''SELECT State, SUM(Registered_user) AS registeredusers
                FROM {table_name}
                GROUP BY State
                ORDER BY registeredusers
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()

    df_2= pd.DataFrame(table_2, columns=("states", "registeredusers"))

    fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title="LAST 10 REGISTERED USERS", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_2)

    query3= f'''SELECT State, AVG(Registered_user) AS registeredusers
                FROM {table_name}
                GROUP BY State
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()

    df_3= pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 700,width= 850)
    st.plotly_chart(fig_amount_3)

#-----------------------------------------------------------------------------------------#
# Streamlit and Layout for the Webpage                                                    #
#-----------------------------------------------------------------------------------------#

st.set_page_config(layout= "wide")
st.markdown("<h1 style='text-align: center; color: #6f36ad;'>PhonePe</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #0b5394;'>DATA VISUALIZATION AND EXPLORATION</h2>", unsafe_allow_html=True)
st.divider()

with st.sidebar:
    select= option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"],
                        icons=["house","graph-up-arrow","bar-chart-line"],
                        menu_icon= "menu-button-wide",
                        default_index=0,
                        styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F99AD"},
                                "nav-link-selected": {"background-color": "#6fa8dc"}})

if select == "HOME":    #st.image("img.png")
    st.markdown("## :blue[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([4,1],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :blue[Technologies used :] Github, Python, Pandas, MySQL, Streamlit and Plotly")
        st.divider()
        st.markdown("### :blue[Overview :]  This streamlit app can be used to visualize the PhonePe pulse data and gain lots of insights on Transactions, Number of users, Top 10 state, District, Pincode. Bar charts, Pie charts and Geo map visualization are used to get insights.")
        st.divider()
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")

elif select == "DATA EXPLORATION":
    pass

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select The Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",aggregate_insurance_df["Year"].min(), aggregate_insurance_df["Year"].max(),aggregate_insurance_df["Year"].min())
            aggregate_insurance_tac_year= transaction_amount_count_year(aggregate_insurance_df, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",aggregate_insurance_tac_year["Quarter"].min(), aggregate_insurance_tac_year["Quarter"].max(),aggregate_insurance_tac_year["Quarter"].min())
            transaction_amount_count_year_quarter(aggregate_insurance_tac_year, quarters)

        elif method == "Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:
                years_at= st.slider("**Select the Year**", aggregate_transaction_df["Year"].min(), aggregate_transaction_df["Year"].max(),aggregate_transaction_df["Year"].min())
            aggregate_transaction_tac_year= transaction_amount_count_year(aggregate_transaction_df, years_at)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State:", aggregate_transaction_tac_year["State"].unique())
            aggregate_transaction_Transaction_type(aggregate_transaction_tac_year, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",aggregate_transaction_tac_year["Quarter"].min(), aggregate_transaction_tac_year["Quarter"].max(),aggregate_transaction_tac_year["Quarter"].min())
            aggregate_transaction_tac_year_quater= transaction_amount_count_year_quarter(aggregate_transaction_tac_year, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", aggregate_transaction_tac_year_quater["State"].unique())
            aggregate_transaction_Transaction_type(aggregate_transaction_tac_year_quater, states)

        elif method == "User Analysis":
           
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",aggregate_user_df["Year"].min(), aggregate_user_df["Year"].max(),aggregate_user_df["Year"].min())
            aggregate_user_year= aggregate_user_plot_1(aggregate_user_df, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",aggregate_user_year["Quarter"].min(), aggregate_user_year["Quarter"].max(),aggregate_user_year["Quarter"].min())
            aggregate_user_year_quarter= aggregate_user_plot_2(aggregate_user_year, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", aggregate_user_year_quarter["State"].unique())
            aggregate_user_plot_3(aggregate_user_year_quarter, states)


    with tab2:

        method_2= st.radio("Select The Method",["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi",map_insurance_df["Year"].min(), map_insurance_df["Year"].max(),map_insurance_df["Year"].min())
            map_insurance_tac_year=transaction_amount_count_year(map_insurance_df, years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_mi", map_insurance_tac_year["State"].unique())
            map_insurance_district(map_insurance_tac_year, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mi",map_insurance_tac_year["Quarter"].min(), map_insurance_tac_year["Quarter"].max(),map_insurance_tac_year["Quarter"].min())
            map_insurance_tac_year_quarter= transaction_amount_count_year_quarter(map_insurance_tac_year, quarters)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_Ty", map_insurance_tac_year_quarter["State"].unique())
            map_insurance_district(map_insurance_tac_year_quarter, states)

        elif method_2 == "Map Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",map_transaction_df["Year"].min(), map_transaction_df["Year"].max(),map_transaction_df["Year"].min())
            map_transaction_tac_year= transaction_amount_count_year(map_transaction_df, years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_mi", map_transaction_tac_year["State"].unique())
            map_insurance_district(map_transaction_tac_year, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mt",map_transaction_tac_year["Quarter"].min(), map_transaction_tac_year["Quarter"].max(),map_transaction_tac_year["Quarter"].min())
            map_transaction_tac_year_quarter= transaction_amount_count_year_quarter(map_transaction_tac_year, quarters)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_Ty", map_transaction_tac_year_quarter["State"].unique())
            map_insurance_district(map_transaction_tac_year_quarter, states)


        elif method_2 == "Map User":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mu",map_user_df["Year"].min(), map_user_df["Year"].max(),map_user_df["Year"].min())
            map_user_year= map_user_plot_1(map_user_df, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mu",map_user_year["Quarter"].min(), map_user_year["Quarter"].max(),map_user_year["Quarter"].min())
            map_user_year_quarter= map_user_plot_2(map_user_year, quarters)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_mu", map_user_year_quarter["State"].unique())
            map_user_plot_3(map_user_year_quarter, states)

    with tab3:

        method_3= st.radio("Select The Method",["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_ti",top_insurance_df["Year"].min(), top_insurance_df["Year"].max(),top_insurance_df["Year"].min())
            top_insurance_tac_year= transaction_amount_count_year(top_insurance_df, years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_ti", top_insurance_tac_year["State"].unique())
            top_insurance_plot_1(top_insurance_tac_year, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_ti",top_insurance_tac_year["Quarter"].min(), top_insurance_tac_year["Quarter"].max(),top_insurance_tac_year["Quarter"].min())
            top_insur_tac_year_quarter= transaction_amount_count_year_quarter(top_insurance_tac_year, quarters)
            
        elif method_3 == "Top Transaction":

            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tt",top_transaction_df["Year"].min(), top_transaction_df["Year"].max(),top_transaction_df["Year"].min())
            top_transaction_tac_year= transaction_amount_count_year(top_transaction_df, years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_tt", top_transaction_tac_year["State"].unique())
            top_insurance_plot_1(top_transaction_tac_year, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_tt",top_transaction_tac_year["Quarter"].min(), top_transaction_tac_year["Quarter"].max(),top_transaction_tac_year["Quarter"].min())
            top_transaction_tac_year_quarter= transaction_amount_count_year_quarter(top_transaction_tac_year, quarters)


        elif method_3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tu",top_user_df["Year"].min(), top_user_df["Year"].max(),top_user_df["Year"].min())
            top_user_year= top_user_plot_1(top_user_df, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", top_user_year["State"].unique())
            top_user_plot_2(top_user_year, states)

elif select == "TOP CHARTS":
    
    question= st.selectbox("Select the Question",["01. Transaction Amount and Count of Aggregated Insurance",
                                                  "02. Transaction Amount and Count of Map Insurance",
                                                  "03. Transaction Amount and Count of Top Insurance",
                                                  "04. Transaction Amount and Count of Aggregated Transaction",
                                                  "05. Transaction Amount and Count of Map Transaction",
                                                  "06. Transaction Amount and Count of Top Transaction",
                                                  "07. Transaction Count of Aggregated User",
                                                  "08. Registered users of Map User",
                                                  "09. App opens of Map User",
                                                  "10. Registered users of Top User",
                                                  ])
    
    if question[0:2] == "01":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregate_insurance")

        # st.subheader("TRANSACTION COUNT")
        # top_chart_transaction_count("aggregate_insurance")

    elif question[0:2] == "02":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question[0:2] == "03":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question[0:2] == "04":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregate_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregate_transaction")

    elif question[0:2] == "05":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question[0:2] == "06":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question[0:2] == "07":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregate_user")

    elif question[0:2] == "08":
        
        states= st.selectbox("Select the State", map_user_df["State"].unique())   
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    elif question[0:2] == "09":
        
        states= st.selectbox("Select the State", map_user_df["State"].unique())   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question[0:2] == "10":
          
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user") 