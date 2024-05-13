#-----------------------------------------------------------------------------------------#
# This module fetches the data from Json file and put the corresponding details of json   # 
# file to phonepe MySQL DB, corresponding tables are created                              #
# Created by Dinesh P K                                                                   #
#-----------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------#
# Import the required components                                                          #
#-----------------------------------------------------------------------------------------#
import pprint
import mysql.connector
import os
import json

#-----------------------------------------------------------------------------------------#
# Connect to MySQL DB and select the DB required                                          # 
#-----------------------------------------------------------------------------------------#
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="give your my sql password"
)
cursor = conn.cursor()
cursor.execute("use phonepe")

#-----------------------------------------------------------------------------------------#
# The following code fetched the data from Json file and insert the corrsponding data in  # 
# to corresponding mySQL table                                                            #
#-----------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------#
# 01 Aggregated Insurance                                                                 #
#-----------------------------------------------------------------------------------------#
agg_ins_path="D:/Study/Guvi/VS/phonepe/pulse/data/aggregated/insurance/country/india/state/"
agg_ins_list=os.listdir(agg_ins_path)
agg_ins_insert_values=[]

create_query='''create table if not exists phonepe.aggregate_insurance(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Transaction_type varchar(50),
                                            Transaction_count bigint,
                                            Transaction_amount bigint)'''
cursor.execute(create_query)
conn.commit()

agg_ins_insert_values = [
    (state.replace("andaman-&-nicobar-islands","Andaman & Nicobar").
     replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu").
     replace("-", " ").
     title(),
     year, int(file.strip(".json")), i["name"], i["paymentInstruments"][0]["count"], i["paymentInstruments"][0]["amount"])
    for state in agg_ins_list
    for year in os.listdir(agg_ins_path + state)
    for file in os.listdir(agg_ins_path + state + "/" + year)
    for i in json.load(open(agg_ins_path + state + "/" + year + "/" + file, "r"))["data"]["transactionData"]
]

# pprint.pprint(agg_ins_insert_values)
print(len(agg_ins_insert_values))

for insert_rows in agg_ins_insert_values:
    insert_query = '''INSERT INTO phonepe.aggregate_insurance 
                        (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount) values'''
    insert_agg_ins=insert_query+str(insert_rows)
    # print(insert_agg_ins)
    try:
        cursor.execute(insert_agg_ins)
    except mysql.connector.Error as err:
        pass
    conn.commit()

#-----------------------------------------------------------------------------------------#
# 02 Aggregated Transaction                                                               #
#-----------------------------------------------------------------------------------------#
agg_tran_path="D:/Study/Guvi/VS/phonepe/pulse/data/aggregated/transaction/country/india/state/"
agg_tran_list=os.listdir(agg_tran_path)
agg_tran_insert_values=[]

create_query='''create table if not exists phonepe.aggregate_Transaction(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Transaction_type varchar(50),
                                            Transaction_count bigint,
                                            Transaction_amount bigint)'''
cursor.execute(create_query)
conn.commit()

agg_tran_insert_values = [
    (state.replace("andaman-&-nicobar-islands","Andaman & Nicobar").
     replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu").
     replace("-", " ").
     title(),
     year, int(file.strip(".json")), i["name"], i["paymentInstruments"][0]["count"], i["paymentInstruments"][0]["amount"])
    for state in agg_tran_list
    for year in os.listdir(agg_tran_path + state)
    for file in os.listdir(agg_tran_path + state + "/" + year)
    for i in json.load(open(agg_tran_path + state + "/" + year + "/" + file, "r"))["data"]["transactionData"]
]

# pprint.pprint(agg_tran_insert_values)
print(len(agg_tran_insert_values))

for insert_rows in agg_tran_insert_values:
    insert_query = '''INSERT INTO phonepe.aggregate_transaction 
                        (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount) values'''
    insert_agg_tran=insert_query+str(insert_rows)
    # print(insert_agg_tran)
    try:
        cursor.execute(insert_agg_tran)
    except mysql.connector.Error as err:
        pass
    conn.commit()

#-----------------------------------------------------------------------------------------#
# 03 Aggregated User                                                                      #
#-----------------------------------------------------------------------------------------#
agg_user_path="D:/Study/Guvi/VS/PhonePe/pulse/data/aggregated/user/country/india/state/"
agg_tran_list=os.listdir(agg_user_path)
agg_user_insert_values=[]

create_query='''create table if not exists phonepe.aggregate_user(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Brands varchar(50),
                                            Transaction_count bigint,
                                            Percentage float)'''
cursor.execute(create_query)
conn.commit()

for state in agg_tran_list:
    selected_state=agg_user_path+state+"/"
    # print(selected_state)
    state_year_list=os.listdir(selected_state)
    # print(state_year_list)
    for year in state_year_list:
        selected_state_year=selected_state+year+"/"
        # print(selected_state_year)
        file_list=os.listdir(selected_state_year)
        for file in file_list:
            selected_file=selected_state_year+file
            # print(selected_file)
            phonepe_data=open(selected_file,"r")
            loaded_data=json.load(phonepe_data)
            # pprint.pprint(loaded_data)
            try:   
                for i in loaded_data["data"]["usersByDevice"]:
                    list_in_for=[]
                    tuple_in_for=()
                    state=state.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
                    state=state.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
                    state=state.replace("-", " ")
                    state=state.title()
                    list_in_for.append(state)
                    list_in_for.append(year)
                    list_in_for.append(int(file.strip(".json")))
                    list_in_for.append(i["brand"])
                    list_in_for.append(i["count"])
                    list_in_for.append(i["percentage"])
                    tuple_in_for=tuple(list_in_for)
                    if len(tuple_in_for)>0:
                        agg_user_insert_values.append(tuple_in_for)
                    else:
                        pass
            except:
                pass
# pprint.pprint(agg_user_insert_values)
print(len(agg_user_insert_values))

for insert_rows in agg_user_insert_values:
    insert_query = '''INSERT INTO phonepe.aggregate_user
                    (State, Year, Quarter, Brands, Transaction_count, Percentage) values'''
    insert_agg_user=insert_query+str(insert_rows)
    # print(insert_agg_user)
    try:
        cursor.execute(insert_agg_user)
    except mysql.connector.Error as err:
        pass
    conn.commit()

#-----------------------------------------------------------------------------------------#
# 04 Map Insurance                                                                        #
#-----------------------------------------------------------------------------------------#
map_ins_path="D:/Study/Guvi/VS/phonepe/pulse/data/map/insurance/hover/country/india/state/"
map_ins_list=os.listdir(map_ins_path)
map_ins_insert_values=[]

create_query='''create table if not exists phonepe.map_insurance(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Districts varchar(50),
                                            Transaction_count bigint,
                                            Transaction_amount bigint)'''
cursor.execute(create_query)
conn.commit()

map_ins_insert_values = [
    (state.replace("andaman-&-nicobar-islands","Andaman & Nicobar").
     replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu").
     replace("-", " ").
     title(),
     year, int(file.strip(".json")), i["name"], i["metric"][0]["count"], i["metric"][0]["amount"])
    for state in map_ins_list
    for year in os.listdir(map_ins_path + state)
    for file in os.listdir(map_ins_path + state + "/" + year)
    for i in json.load(open(map_ins_path + state + "/" + year + "/" + file, "r"))["data"]["hoverDataList"]
]

# pprint.pprint(map_ins_insert_values)
print(len(map_ins_insert_values))

for insert_rows in map_ins_insert_values:
    insert_query = '''INSERT INTO phonepe.map_insurance 
                        (State, Year, Quarter, Districts, Transaction_count, Transaction_amount) values'''
    insert_map_ins=insert_query+str(insert_rows)
    # print(insert_map_ins)
    try:
        cursor.execute(insert_map_ins)
    except mysql.connector.Error as err:
        pass
    conn.commit()

#-----------------------------------------------------------------------------------------#
# 05 Map Transaction                                                                      #
#-----------------------------------------------------------------------------------------#
map_tran_path="D:/Study/Guvi/VS/phonepe/pulse/data/map/transaction/hover/country/india/state/"
map_tran_list=os.listdir(map_tran_path)
map_tran_insert_values=[]

create_query='''create table if not exists phonepe.map_transaction(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Districts varchar(50),
                                            Transaction_count bigint,
                                            Transaction_amount bigint)'''
cursor.execute(create_query)
conn.commit()

map_tran_insert_values = [
    (state.replace("andaman-&-nicobar-islands","Andaman & Nicobar").
     replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu").
     replace("-", " ").
     title(),
     year, int(file.strip(".json")), i["name"], i["metric"][0]["count"], i["metric"][0]["amount"])
    for state in map_tran_list
    for year in os.listdir(map_tran_path + state)
    for file in os.listdir(map_tran_path + state + "/" + year)
    for i in json.load(open(map_tran_path + state + "/" + year + "/" + file, "r"))["data"]["hoverDataList"]
]

# pprint.pprint(map_tran_insert_values)
print(len(map_tran_insert_values))

for insert_rows in map_tran_insert_values:
    insert_query = '''INSERT INTO phonepe.map_transaction 
                        (State, Year, Quarter, Districts, Transaction_count, Transaction_amount) values'''
    insert_map_tran=insert_query+str(insert_rows)
    # print(insert_map_tran)
    try:
        cursor.execute(insert_map_tran)
    except mysql.connector.Error as err:
        pass
    conn.commit()

#-----------------------------------------------------------------------------------------#
# 06 Map User                                                                             #
#-----------------------------------------------------------------------------------------#
map_user_path="D:/Study/Guvi/VS/phonepe/pulse/data/map/user/hover/country/india/state/"
map_user_list=os.listdir(map_user_path)
map_user_insert_values=[]

create_query='''create table if not exists phonepe.map_user(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Districts varchar(50),
                                            Registered_user bigint,
                                            App_opens bigint)'''
cursor.execute(create_query)
conn.commit()

map_user_insert_values = [
    (state.replace("andaman-&-nicobar-islands","Andaman & Nicobar").
     replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu").
     replace("-", " ").
     title(),
     year, int(file.strip(".json")), i[0], i[1]["registeredUsers"], i[1]["appOpens"])
    for state in map_user_list
    for year in os.listdir(map_user_path + state)
    for file in os.listdir(map_user_path + state + "/" + year)
    for i in json.load(open(map_user_path + state + "/" + year + "/" + file, "r"))["data"]["hoverData"].items()
]

# pprint.pprint(map_user_insert_values)
print(len(map_user_insert_values))

for insert_rows in map_user_insert_values:
    insert_query = '''INSERT INTO phonepe.map_user (State, Year, Quarter, Districts, Registered_user, App_opens) values'''
    insert_map_user=insert_query+str(insert_rows)
    # print(insert_map_user)
    try:
        cursor.execute(insert_map_user)
    except mysql.connector.Error as err:
        pass
    conn.commit()

#-----------------------------------------------------------------------------------------#
# 07 Top Insurance                                                                        #
#-----------------------------------------------------------------------------------------#
top_ins_path="D:/Study/Guvi/VS/phonepe/pulse/data/top/insurance/country/india/state/"
top_ins_list=os.listdir(top_ins_path)
top_ins_insert_values=[]

create_query='''create table if not exists phonepe.top_insurance(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Pincodes int,
                                            Transaction_count bigint,
                                            Transaction_amount bigint)'''
cursor.execute(create_query)
conn.commit()

top_ins_insert_values = [
    (state.replace("andaman-&-nicobar-islands","Andaman & Nicobar").
     replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu").
     replace("-", " ").
     title(),
     year, int(file.strip(".json")), i["entityName"], i["metric"]["count"], i["metric"]["amount"])
    for state in top_ins_list
    for year in os.listdir(top_ins_path + state)
    for file in os.listdir(top_ins_path + state + "/" + year)
    for i in json.load(open(top_ins_path + state + "/" + year + "/" + file, "r"))["data"]["pincodes"]
]

# pprint.pprint(top_ins_insert_values)
print(len(top_ins_insert_values))

for insert_rows in top_ins_insert_values:
    insert_query = '''INSERT INTO phonepe.top_insurance 
                        (State, Year, Quarter, Pincodes, Transaction_count, Transaction_amount) values'''
    insert_top_ins=insert_query+str(insert_rows)
    # print(insert_top_ins)
    try:
        cursor.execute(insert_top_ins)
    except mysql.connector.Error as err:
        pass
    conn.commit()

#-----------------------------------------------------------------------------------------#
# 08 Top Transaction                                                                      #
#-----------------------------------------------------------------------------------------#
top_tran_path="D:/Study/Guvi/VS/phonepe/pulse/data/top/transaction/country/india/state/"
top_tran_list=os.listdir(top_tran_path)
top_tran_insert_values=[]

create_query='''create table if not exists phonepe.top_transaction(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Pincodes int,
                                            Transaction_count bigint,
                                            Transaction_amount bigint)'''
cursor.execute(create_query)
conn.commit()

top_tran_insert_values = [
    (state.replace("andaman-&-nicobar-islands","Andaman & Nicobar").
     replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu").
     replace("-", " ").
     title(),
     year, int(file.strip(".json")), i["entityName"], i["metric"]["count"], i["metric"]["amount"])
    for state in top_tran_list
    for year in os.listdir(top_tran_path + state)
    for file in os.listdir(top_tran_path + state + "/" + year)
    for i in json.load(open(top_tran_path + state + "/" + year + "/" + file, "r"))["data"]["pincodes"]
]

# pprint.pprint(top_tran_insert_values)
print(len(top_tran_insert_values))

for insert_rows in top_tran_insert_values:
    insert_query = '''INSERT INTO phonepe.top_transaction 
                        (State, Year, Quarter, Pincodes, Transaction_count, Transaction_amount) values'''
    insert_top_ins=insert_query+str(insert_rows)
    # print(insert_top_ins)
    try:
        cursor.execute(insert_top_ins)
    except mysql.connector.Error as err:
        pass
    conn.commit()

#-----------------------------------------------------------------------------------------#
# 09 Top User                                                                             #
#-----------------------------------------------------------------------------------------#
top_user_path="D:/Study/Guvi/VS/phonepe/pulse/data/top/user/country/india/state/"
top_user_list=os.listdir(top_user_path)
top_user_insert_values=[]

create_query='''create table if not exists phonepe.top_user(State varchar(50) not null,
                                            Year int,
                                            Quarter int,
                                            Pincodes int,
                                            Registered_user bigint)'''
cursor.execute(create_query)
conn.commit()

top_user_insert_values = [
    (state.replace("andaman-&-nicobar-islands","Andaman & Nicobar").
     replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu").
     replace("-", " ").
     title(),
     year, int(file.strip(".json")), i["name"], i["registeredUsers"])
    for state in top_user_list
    for year in os.listdir(top_user_path + state)
    for file in os.listdir(top_user_path + state + "/" + year)
    for i in json.load(open(top_user_path + state + "/" + year + "/" + file, "r"))["data"]["pincodes"]
]

# pprint.pprint(top_user_insert_values)
print(len(top_user_insert_values))

for insert_rows in top_user_insert_values:
    insert_query = '''INSERT INTO phonepe.top_user 
                        (State, Year, Quarter, Pincodes, Registered_user) values'''
    insert_top_user=insert_query+str(insert_rows)
    # print(insert_top_user)
    try:
        cursor.execute(insert_top_user)
    except mysql.connector.Error as err:
        pass
    conn.commit()