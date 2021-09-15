import pandas as pd
import math

"""
Point A to B continuous path finder
-----------------------------------

step 1 : Import csv file
step 2 : get first and last point (latitude,longitude)
step 3 : find the slope ratio by using equation (first latitude-last latitud2)/(first latitude - last latitude)
step 4 : slope ratio is used for straight line
step 5 : appending straight line path by changing latitude of out of line to first latitude
step 6 : find distance of all point (lantitude/Longitude)
step 7 : sort the distance of all points for generate continuous path
step 8 : export the data as new csv file
"""

class GeoLocator():
    def __init__(self):
        pass

    def get_csv(self, filename):
        return pd.read_csv(filename)

    def get_first_last_lat_long_data(self, df_data):
        return df_data.iloc[0], df_data.iloc[-1]

    def get_slope_ratio(self, from_lat, from_long, to_lat, to_long):
        slope_ratio = (from_lat-to_lat)/(from_long-to_long)
        return slope_ratio

    def distance(self, from_lat, from_long, to_lat, to_long):
        if from_lat == to_lat and from_long == to_long:
            return 0
        else:
            radlat1 = math.pi * from_lat/180
            radlat2 = math.pi * to_lat/180
            theta = from_long-to_long
            radtheta = math.pi * theta/180
            dist = math.sin(radlat1) * math.sin(radlat2) + math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta)
            if dist > 1:
                dist = 1
            dist = math.acos(dist)
            dist = dist * 180/math.pi
            dist = dist * 60 * 1.1515
            dist = dist * 1.609344
            return dist;

    def export_csv(self, df_data):
        df_first, df_last = self.get_first_last_lat_long_data(df_data)
        dbl_slope_ratio = self.get_slope_ratio(df_first['latitude'], df_first['longitude'], df_last['latitude'], df_last['longitude'])

        dct_data = {'latitude':[df_first['latitude']], 'longitude':[df_first['longitude']], 'distance': [0]}

        for ind,row in df_data.iterrows():
            if ind !=0:
                current_ratio = self.get_slope_ratio(df_first['latitude'], df_first['longitude'], row['latitude'], row['longitude'])
                distance = self.distance(df_first['latitude'], df_first['longitude'], row['latitude'], row['longitude'])
                if distance not in dct_data['distance']:
                    dct_data['latitude'].append(row['latitude'])
                    dct_data['longitude'].append(row['longitude'])
                    dct_data['distance'].append(distance)

                if round(dbl_slope_ratio,2) != round(current_ratio,2):
                    distance = self.distance(df_first['latitude'], df_first['longitude'],df_first['latitude'],row['longitude'])
                    if distance not in dct_data['distance']:
                        dct_data['latitude'].append(df_first['latitude'])
                        dct_data['longitude'].append(row['longitude'])
                        dct_data['distance'].append(distance)
        df_exp_data = pd.DataFrame(dct_data)
        df_exp_data = df_exp_data.sort_values(by=['distance'])
        df_exp_data.to_csv('exported_details.csv', index=False)


if __name__ == '__main__':
    obj_geo = GeoLocator()
    df_data = obj_geo.get_csv('latitude_longitude_details.csv')
    obj_geo.export_csv(df_data)
