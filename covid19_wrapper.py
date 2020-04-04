import COVID19Py
import pandas as pd
from datetime import datetime, date, timedelta
from collections import defaultdict, OrderedDict

class covid19():
    def __init__(self):
        data = self.retrieve_covid19_latest_data()
        self.latest = data['latest']
        self.df = pd.DataFrame(data['locations'])
        self.df = self.format_timeline_matrix()
        
    def retrieve_covid19_latest_data(self):
        covid19 = COVID19Py.COVID19()
        data = covid19.getAll(timelines=True)
        return(data)
    
    def format_timeline_matrix(self):
        toret = defaultdict(list)
        features = ['confirmed', 'deaths']
        for country in range(len(self.df.index)):
            for time in range(len(self.df['timelines'][country]['deaths']['timeline'])):
                toret['country'].append(self.df['country'][country])
                toret['country_code'].append(self.df['country_code'][country])
                toret['province'].append(self.df['province'][country])
                toret['latitude'].append(self.df['coordinates'][country]['latitude'])
                toret['longitude'].append(self.df['coordinates'][country]['longitude'])
                toret['country_population'].append(self.df['country_population'][country])
                for feat in features:
                    array = self.df['timelines'][country][feat]['timeline']
                    toret[feat].append(list(array.values())[time])
                    toret[feat+'time'].append(list(array.keys())[time])
        toret = pd.DataFrame(toret)
        toret = toret.drop(['confirmedtime'], axis=1)  
        toret.rename({'deathstime':'time'}, inplace=True, axis=1) 
        toret['time'] = toret['time'].apply(self.format_date) 
        toret = toret.set_index(pd.DatetimeIndex(toret['time'])).drop('time', axis=1) 
        return(toret)
             
    def format_date(self, row):
        row = datetime.strptime(row,"%Y-%m-%dT%H:%M:%SZ").isoformat()
        return(row)

if __name__ == "__main__":
	cv = covid19()
	df = cv.df
    df_latest = cv.latest