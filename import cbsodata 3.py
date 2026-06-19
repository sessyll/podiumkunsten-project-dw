import cbsodata
import pandas as pd
import requests
from pprint import pprint
tables = cbsodata.get_table_list()
list_dict = tables[0]
list_dict.keys()
for table in tables:
    if 'podiumkunsten' in table['Title']:
        print(table['Identifier'], table['Title'])
for table in tables:
    if table['Identifier'] == '70077NED':
        print(table['Title'], table['Identifier'])
info = cbsodata.get_info('70077NED')
# --- Orijinal kodun bura (Değişmesin) ---
data = pd.DataFrame(cbsodata.get_data('70077NED'))
data.rename(columns={"Perioden": "Years", "RegioS": "Regions", "TotaalVoorstellingen_6": "AllPerformances", "Muziekvoorstellingen_8": "MusicPerformances", "TotaalBezoekenAanVoorstellingen_13": "TotalVisitors", "Muziekvoorstellingen_15": "MusicPerformanceVisitors"},  inplace=True)
df = data.set_index('Years')
df2 =  df.drop_duplicates(subset=['ID'])
df2.drop(columns=['ID'], inplace=True)
df_refined = df2.iloc[:,[0,6,8,13,15]]

# .reset_index() oteherwise 'Years' column will be index and csv will not have 'Years' column
df_final = df_refined.reset_index()

# for some reason, csv format is not accepted by datawrapper, so I changed the separator to ';' and it worked.
csv_data = df_final.to_csv(index=False, sep=';')

# id and key
DATAWRAPPER_API_KEY = "TOKEN HERE"
CHART_ID = "zszNI"

import os
from dotenv import load_dotenv
load_dotenv()
DATAWRAPPER_API_KEY = os.getenv("DATAWRAPPER_API_KEY")
print(DATAWRAPPER_API_KEY)

headers = {
    "Authorization": f"Bearer {DATAWRAPPER_API_KEY}",
    "Content-Type": "text/csv"
}

# put request

url = "https://api.datawrapper.de/v3/me"
url_data = f"https://api.datawrapper.de/v3/charts/{CHART_ID}/data"
response_data = requests.put(url_data, headers=headers, data=csv_data)

if response_data.status_code == 204:
    print("✅ Data sent to Datawrapper")
    
    # url_publish = f"https://api.datawrapper.de/v3/charts/{CHART_ID}/publish"
    # response_publish = requests.post(url_publish, headers=headers)
    
    # if response_publish.status_code == 200:
    #     print("🚀 Chart updated and published!")
    #     print("📊 Your live chart's url: https://dwcdn.net")
    # else:
    #    print("❌ Chart publishing failed:", response_publish.text)
else:
    print("❌ Data upload failed:", response_data.text)
    print(f"Hata detayı: {response_data.text}")



response = requests.get(url, headers=headers)
print(response.json())


print("downloaded: 'datawrapper_ready_data.csv'")
