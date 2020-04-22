import requests
from bs4 import BeautifulSoup
import pandas as pd
URL = 'https://www.worldometers.info/coronavirus/#countries'
res = requests.get(URL)
res = res.text
soup = BeautifulSoup(res, features = "html.parser")
_id = "main_table_countries_today"
countries_table = soup.find("table", attrs = {"id":_id})
def format_header(th):
  header = " ".join(th.strings)
  header = header.replace(u"\xa0",u" ").replace("\n","")
  return header.replace(", ", "/")
columns = [format_header(th) for th in countries_table.find("thead").findAll("th")]
country_rows = countries_table.find("tbody").find_all("tr")
parsed_data = []
for country_row in country_rows:
  parsed_data.append([data.get_text().replace("\n","") for data in country_row.findAll("td")])
data_frame = pd.DataFrame(parsed_data, columns = columns)
all_data = data_frame.replace(to_replace=[""], value = 0)
continent_wise_count = all_data[:6]
continent_wise_count = continent_wise_count.drop(continent_wise_count.columns[[8,9,10,11,12]], axis = 1)
continent_wise_count.rename(columns = {'Country/Other':'Continent'}, inplace = True)
country_wise_count = all_data[7:]
continent_wise_count.to_csv(r'./continent_wise_cases.csv',index = False)
country_wise_count.to_csv(r'./country_wise_cases.csv',index = False)
continent_wise_count.set_index("Continent").to_json(r"./continent_wise_cases.json", orient="index")
country_wise_count.set_index("Country/Other").to_json(r"./country_wise_cases.json", orient="index")
print("The operation has been completed successfully")
