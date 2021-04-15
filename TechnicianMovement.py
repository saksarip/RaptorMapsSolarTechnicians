import pandas as pd
from haversine import haversine
from haversine import Unit
import json


#Loads the technician data into dictionary format
with open('api_techician_response_data.json') as f:
  data = json.load(f)


'''
The distances between the techs are loaded into a dataframe. 
I included separate columns for each pair of solar technicians. 
As a result this method of processing the data would have to change if there are more than 3 technicians. 
If the number of technicians is dynamic, a non-tabular format would work better.
'''


tech_distance_data = pd.DataFrame(columns=['tsecs', 'tminutes',
                                           'DistanceBetweenTech1_2(Ft)', 'DistanceBetweenTech1_3(Ft)',
                                           'DistanceBetweenTech2_3(Ft)', 'IsTech1_2Close',
                                           'IsTech1_3Close', 'IsTech2_3Close'])


#The data is parsed and processed. Using the haversine function the distances are calculated and converted to Feet,
# and formatted in a dictionary that can be added to the DataFrame.

def construct_row(minute_data):
  tech_data = minute_data['features']
  tsecs = tech_data[0]['properties']['tsecs']

  tech_three_loc = tech_data[0]['geometry']['coordinates']

  tech_one_loc = tech_data[1]['geometry']['coordinates']

  tech_two_loc = tech_data[2]['geometry']['coordinates']

  # Haversine distance used radius of the earth to calculate distance betweeen points on a sphere
  # Assumes earth is perfectly spherical, and that the radius is constant throughout the earth
  # This assumption isn't perfectly true, ellipsoidal calculation would improve accuracy, but for
  # these small distances the difference is negligible.

  one_two_distance = haversine(tech_two_loc, tech_one_loc, unit=Unit.FEET)
  one_three_distance = haversine(tech_three_loc, tech_one_loc, unit=Unit.FEET)
  two_three_distance = haversine(tech_three_loc, tech_two_loc, unit=Unit.FEET)

  is_one_two_close = int(one_two_distance <= 1000)
  is_one_three_close = int(one_three_distance <= 1000)
  is_two_three_close = int(two_three_distance <= 1000)

  row = {
    'tsecs': tsecs,
    'tminutes': tsecs / 60,
    'DistanceBetweenTech1_2(Ft)': one_two_distance,
    'DistanceBetweenTech1_3(Ft)': one_three_distance,
    'DistanceBetweenTech2_3(Ft)': two_three_distance,
    'IsTech1_2Close': is_one_two_close,
    'IsTech1_3Close': is_one_three_close,
    'IsTech2_3Close': is_two_three_close
  }

  return row

#Appending each row to the overall dataframes
for minute_data in data:
    tech_distance_data = tech_distance_data.append(construct_row(minute_data), ignore_index=True)

print(tech_distance_data)

#Saving data to file
tech_distance_data.to_csv('tech_distance_data.csv')
