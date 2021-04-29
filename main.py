from enum import auto
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import locale
locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
from bs4 import BeautifulSoup as soup
from datetime import date, datetime
from urllib.request import Request, urlopen
import warnings
warnings.filterwarnings("ignore")
# import matplotlib.pyplot as plt
# from pandas_profiling import ProfileReport
# import seaborn as sns
# import gc
# import plotly.graph_objs as gob
# import geopandas as gpd
# import plotly.offline as py
# import os

####################################################################

vaccine = pd.read_csv('country_vaccinations.csv')
vaccine['date_new'] = pd.to_datetime(vaccine['date'])
covid=pd.read_csv('worldometer_coronavirus_daily_data.csv')
covid_cum=pd.read_csv('worldometer_coronavirus_summary_data.csv')
covid['date_new'] = pd.to_datetime(covid['date'])

# url = "https://www.worldometers.info/coronavirus/#countries"
url = 'https://www.worldometers.info/coronavirus/'

req = Request(url , headers={'User-agent' : "Mozilla/5.0"})

webpage = urlopen(req)
page_soup = soup(webpage, "html.parser")

today = datetime.now()
yesterday_str = "%s %d,%d" %(date.today().strftime("%b"), today.day-1, today.year)


###################################################################
table = page_soup.findAll("table", {"id": "main_table_countries_yesterday"})

containers = table[0].findAll("tr", {"style":""})
title = containers[0]

del containers[0]

all_data = []
clean = True

for country in containers:
    country_data = []
    country_container = country.findAll("td")
    
    if country_container[1].text == "China":
        continue

    
    for i in range(1, len(country_container)):
        final_feature = country_container[i].text
        if clean :
            if i != 1 and i != len(country_container)-1:
                final_feature = final_feature.replace(",","")
                
                if final_feature.find('+') != -1:
                    final_feature = final_feature.replace("+","")
                    final_feature = float(final_feature)
                elif final_feature.find("-") != -1:
                    final_feature = final_feature.replace("-","")
                    final_feature = float(final_feature)*-1
                    
        if final_feature == 'N/A':
            final_feature = 0
        elif final_feature == "" or final_feature == " ":
            final_feature = 0
            
        country_data.append(final_feature)
    all_data.append(country_data)

df = pd.DataFrame(all_data)
df.drop([14,15,16,17,18,19,20], inplace=True, axis = 1)

column_labels = ["Country", "Total Cases","New Cases","Total Deaths","New Deaths",
               "Total Rocovered", "New Recovered","Active Cases","Serious, Critical","Total Cases/1M",
               "Deaths/1M","Total Tests","Tests/1M","Population"]
df.columns = column_labels

for label in df.columns:
    if label != 'Country' and label != "Continent":
        df[label] = pd.to_numeric(df[label])

df["%Inc Cases"] = df["New Cases"]/df["Total Cases"]*100
df["%Inc Deaths"] = df["New Deaths"]/df["Total Deaths"]*100
df["%Inc Recovered"] = df["New Recovered"]/df["Total Rocovered"]*100

####################################################################

# india = covid[covid['country']=='India']
# fig = px.bar(india, x='date', y='daily_new_cases',title='Daily new cases from Apr 2020 to Apr 2021',width=700, height=400)
# fig.show()




window = tk.Tk()
window.title("COVID-19 ANALYIS")
window.configure(background="#161625")
window.grid_columnconfigure(0, weight=1)

#####################   TITLE   #####################

frame1 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame1.grid(row = 0, columnspan=4, padx=5, pady=5)
title = tk.Label(master=frame1,width=40, 
                    text=" Covid-19 Analysis", 
                    background="#1e1e30",
                    foreground="#bdbdbd", 
                    font=("archia 18 bold"))
title.pack(expand=YES, fill=BOTH, padx=5, pady=5)

#####################################################

##############   Covid-19 India Live  ###############

for i in range(4):
	window.columnconfigure(i, weight= 1, minsize=75)

	for j in range(4):
		frame2 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
		if j==0:
			frame2.grid(row=1, column=0,padx=5, pady=5)
			label_confirmed = tk.Label(master=frame2, width=10,
										height=5,
										text=f"Confirmed \n Cases \n",
										font=("archia 12 bold"),
										background="#331327",
            							foreground="#ff073a")
			label_confirmed.pack(padx=5, pady=5)
		if j==1:
			frame2.grid(row=1, column=1,padx=5, pady=5)
			label_active = tk.Label(master=frame2, width=10,
									height=5,
									text=f"Active \n Cases \n",
									font=("archia 12 bold"),
									background="#132240",
            						foreground="#007bff")
			label_active.pack(padx=5, pady=5)
		if j==2:
			frame2.grid(row=1, column=2,padx=5, pady=5)
			label_recovered = tk.Label(master=frame2, width=10,
										height=5,
										text=f"Recovered \n Cases \n",
										font=("archia 12 bold"),
										background="#182828",
            							foreground="#28a745")
			label_recovered.pack(padx=5, pady=5)
		if j==3:
			frame2.grid(row=1, column=3,padx=5, pady=5)
			label_deceased = tk.Label(master=frame2, width=10,
										height=5,
										text=f"Deceased \n \n",
										font=("archia 12 bold"),
										background="#202230",
            							foreground="#6c757d")
			label_deceased.pack(padx=5, pady=5)

def clicked():
	url = "https://api.covid19india.org/data.json"
	page = requests.get(url)
	data = json.loads(page.text)

	confirm = int(data["statewise"][0]["confirmed"])
	active = int(data["statewise"][0]["active"])
	recovered = int(data["statewise"][0]["recovered"])
	deceased = int(data["statewise"][0]["deaths"])
	deltaconfirmed = int(data["statewise"][0]["deltaconfirmed"])
	deltarecovered = int(data["statewise"][0]["deltarecovered"])
	deltadeaths = int(data["statewise"][0]["deltadeaths"])

	confirm = str(locale.format_string("%d", confirm, grouping=True))
	active = str(locale.format_string("%d", active, grouping=True))
	recovered = str(locale.format_string("%d", recovered, grouping=True))
	deceased = str(locale.format_string("%d", deceased, grouping=True))
	deltaconfirmed = str(locale.format_string("%d", deltaconfirmed, grouping=True))
	deltarecovered = str(locale.format_string("%d", deltarecovered, grouping=True))
	deltadeaths = str(locale.format_string("%d", deltadeaths, grouping=True))

	label_confirmed.configure(text="Confirmed \n\n+" +deltaconfirmed + "\n" + confirm)	
	label_active.configure(text="Active \n\n" + "\n" + active)
	label_recovered.configure(text="Recovered \n\n+"+ deltarecovered + "\n" + recovered)
	label_deceased.configure(text="Deceased \n\n+"+ deltadeaths + "\n" + deceased)


frame3 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame3.grid(row = 2, columnspan=4, padx=5, pady=5)
refresh_btn = tk.Button(master=frame3, text="Refresh",
						width=10,
						font=("archia 12 bold"),
						foreground="#9673b9",
						background="#230f41",
						command=clicked
						)
refresh_btn.pack(padx=5, pady=5)

#####################################################



############   Covid around the world   #############

def world_clicked():
    fig = go.Figure(data=go.Choropleth(locations = covid_cum['country'],
                                locationmode='country names',
                                z = covid_cum['total_confirmed'],
                                text = covid_cum['country'],
    #                             color_continuous_scale='reds',
                                colorscale = 'reds',
                                autocolorscale=False,
    #                             reversescale=True,
                                marker_line_color='darkgray',
                                marker_line_width=0.5,
                            
                            ))

    fig.update_layout(
        title_text='Total confirmed cases around the world',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ))
    fig.show()

frame4 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame4.grid(row=3, column=0, padx=5, pady=5)
world_map_btn = tk.Button(master=frame4, text="World Map",
                            width=10,
                            font=("archia 12 bold"),
						    foreground="#9673b9",
						    background="#230f41",
						    command=world_clicked
                        )

world_map_btn.pack(padx=1, pady=1)

#####################################################

####################   World Total   ############################

cases = df[["Total Rocovered", "Active Cases", "Total Deaths"]].loc[0]
cases_df = pd.DataFrame(cases).reset_index()
cases_df.columns = ["Type", "Total"]

cases_df["Percentage"] = np.round(100*cases_df['Total']/np.sum(cases_df["Total"]),2)
cases_df["Virus"] = ["Covid-19" for i in range(len(cases_df))]

def total_graph():

	fig = px.bar(cases_df, x = "Virus", y = "Percentage", 
					color = "Type",
					hover_data = ["Total"], width=600
				)
	fig.show()

frame5 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame5.grid(row=3, column=1, padx=5, pady=5)

world_total_btn = tk.Button(master=frame5, text="World data",
							width=10,
							font=("archia 12 bold"),
							foreground="#9673b9",
							background="#230f41",
							command=total_graph
							)
world_total_btn.pack(padx=1, pady=1)

#####################################################

new_df = df[1:]
def worst_hit():

	fig = px.scatter(new_df.head(20), x="Country", y="Total Cases", size="Total Cases", color="Country",
				hover_name="Country", size_max=60)
	fig.update_layout(
		title=str(20) +" Worst hit countries",
		xaxis_title="Countries",
		yaxis_title="Confirmed Cases",
		width = 1000
	)
	fig.show()

frame6 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame6.grid(row=3, column=2, padx=5, pady=5)

worst_hit_btn = tk.Button(master=frame6, text="Worst Hit",
							width=10,
							font=("archia 12 bold"),
							foreground="#9673b9",
							background="#230f41",
							command=worst_hit
							)
worst_hit_btn.pack(padx=1, pady=1)


#####################################################
#####################################################

frame_l = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame_l.grid(row = 4, columnspan=4, padx=5, pady=5)
label_l = tk.Label(master=frame_l,
                    text="Worst Hit Countries Analysis", 
                    background="#1e1e30",
                    foreground="#bdbdbd", 
                    font=("archia 15 bold"))
label_l.pack(fill=BOTH,padx=5, pady=5,expand=1)


#####################################################

####### 10 worst hit countries - Confirmed cases  #######
def worst_hit_confirm():
	fig = px.bar(
		new_df.head(10),
		x = "Country",
		y = "Total Cases",
		title= "Top 10 worst affected countries", # the axis names
		color_discrete_sequence=["purple"], 
		height=500,
		width=800
	)
	fig.show()

frame7 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame7.grid(row=5, column=0, padx=5, pady=5)
a = tk.Button(master=frame7, text="By Cases",
							width=10,
							font=("archia 12 bold"),
							foreground="#9673b9",
							background="#230f41",
							command=worst_hit_confirm
							)
a.pack(padx=1, pady=1)


###############################################################

####### 10 worst hit countries - Total Deaths  #######

def worst_hit_by_deaths():
	fig = px.bar(
		new_df.head(10),
		x = "Country",
		y = "Total Deaths",
		title= "Top 10 worst affected countries", # the axis names
		color_discrete_sequence=["red"], 
		height=500,
		width=800
	)
	fig.show()

frame8 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame8.grid(row=5, column=1, padx=5, pady=5)
b = tk.Button(master=frame8, text="By Deaths",
							width=10,
							font=("archia 12 bold"),
							foreground="#9673b9",
							background="#230f41",
							command=worst_hit_by_deaths
							)
b.pack(padx=1, pady=1)

###############################################################

####### 10 worst hit countries - Recovering cases  #######

def worst_hit_by_recovery():
	fig = px.bar(
		new_df.head(10),
		x = "Country",
		y = "Total Rocovered",
		title= "Top 10 worst affected countries", # the axis names
		color_discrete_sequence=["green"], 
		height=500,
		width=800
	)
	fig.show()

frame9 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame9.grid(row=5, column=2, padx=5, pady=5)
c = tk.Button(master=frame9, text="By Recovery",
							width=10,
							font=("archia 12 bold"),
							foreground="#9673b9",
							background="#230f41",
							command=worst_hit_by_recovery
							)
c.pack(padx=1, pady=1)

###############################################################

####### 10 Worst hit countries - Active cases  #######

def worst_hit_by_active():
	fig = px.bar(
		new_df.head(10),
		x = "Country",
		y = "Active Cases",
		title= "Top 10 worst affected countries", # the axis names
		color_discrete_sequence=["pink"], 
		height=500,
		width=800
	)
	fig.show()

frame10 = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame10.grid(row=5, column=3, padx=5, pady=5)
d = tk.Button(master=frame10, text="By Active",
							width=10,
							font=("archia 12 bold"),
							foreground="#9673b9",
							background="#230f41",
							command=worst_hit_by_active
							)
d.pack(padx=1, pady=1)

###############################################################


india = df[df['Country']=='India']

india = india.transpose()

col_label = ['Data']
india.columns = col_label
# print(india['Data'])

new_india = india.drop(['Country','Population','Total Tests'])
print(new_india)
fig = px.bar(india, x=new_india.index, y=new_india['Data'] ,title='Daily new cases from Apr 2020 to Apr 2021',width=700, height=400)
fig.show()

# fig = px.scatter(new_india, x=new_india.index, y="Data", color=new_india.index,
# 				hover_name=new_india.index, size_max=60)
# fig.update_layout(
# 		title=str(20) +" Worst hit countries",
# 		xaxis_title="Countries",
# 		yaxis_title="Confirmed Cases",
# 		width = 1000
# )
# fig.show()
print(new_india['Data'][0])
# # india = india.drop('Country')
# india = pd.DataFrame(india ,columns=['Numbers'])

# # india.index = column_labels
# print(india)


window.mainloop()