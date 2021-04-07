import pandas as pd
locationDetails = pd.read_csv('LocationDetails.csv')
nameView = locationDetails[locationDetails['Location'] == 'Royal Opera House Muscat']
print(nameView['Description'].values.tolist())
