import pandas as pd
import csv

# id,name,username,password,age,gender,time,calorie_burnt
# 1,Abhishek Raj,a@c.com,12345678,20,male,37.0,33.0
# 2,Abhinav Raj,a@d.com,12345678,22,male,46.4,70.5
# 3,Abhinav Raj,a@e.com,12345678,22,male,14.0,20.0
# 4,Aryan,a@f.com,12345678,21,male,48.0,36.5
# 5,Ankit,a@g.com,12345678,21,male,20.0,67.0
# 6,Sushmit,ps@gmail.com,12345678,21,male,82.0,30.5
header=["id","name","username","password","age","gender","time","calorie_burnt"]
modified_rows = []
f=0

# Open the CSV file in read mode
with open('users.csv', 'r', newline='') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        # if f==0:
        #     f=1
        #     continue
        row[6] = 0
        row[7] = 0

        modified_rows.append(row)

# Open the CSV file in write mode to save the modifications
with open('users.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(header)

    # Write the rest of the rows using writerows
    csv_writer.writerows(modified_rows[1:])

# print(modified_rows)
df = pd.read_csv("users.csv", encoding = "ISO-8859-1")
df1 = pd.read_csv("daily.csv", encoding = "ISO-8859-1")

time_df = df1.groupby(by = ["id"], as_index = False)["time"].sum()
cal_df = df1.groupby(by = ["id"], as_index = False)["calorie"].sum()
# df=pd.read_csv('users.csv')
# print(time_df['id'])
for i,row in time_df.iterrows():
    id=row.id
    id-=1
    time=row.time
    df.loc[id,'time']=df.loc[id,'time']+time
    df.to_csv('users.csv',index=False)

for i,row in cal_df.iterrows():
    id=row.id
    id-=1
    cal=row.calorie
    df.loc[id,'calorie_burnt']=df.loc[id,'calorie_burnt']+cal
    df.to_csv('users.csv',index=False)
    