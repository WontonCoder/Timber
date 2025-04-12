import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

dfMain = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Milling', converters={'Common Name': str})
dfHeritage = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Heritage slabs index', converters={'Common Name': str})
dfWeights = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Log weight calculation', 
                          converters={'Common Name': str, 'Mill date':str, 'weight': float})
dfsheet3 = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Sheet3', converters={'Common Name': str})

bdft = dfsheet3['BdFt']
milledSpecies = dfMain['Common Name']
prices = dfsheet3['Price (15/bf)'] # Access data from a specific column
#print(type(prices[0]))

heritageSpecies = dfsheet3['Common Name']
#print(heritageSpecies)

uniqueHSpecies = set()
uniqueMSpecies = set()
HSpeciesDct = {}

Hcount = 0
newTree = 0
for i in range(heritageSpecies.size):
  currentLen = len(uniqueHSpecies)
  uniqueHSpecies.add(heritageSpecies[i])
  if len(uniqueHSpecies) == currentLen or Hcount == 0:
    Hcount+=1
  else:
    HSpeciesDct[heritageSpecies[i-1]] = [i - newTree, newTree, i] #gives the number of trees of this species and where in the dataframe it starts and ends. 
    newTree = i



for species in milledSpecies:
  uniqueMSpecies.add(species)
uniqueMSpecies.remove("-----")
#print(uniqueSpecies)
#print(len(uniqueHSpecies))
#print(HSpeciesDct)

sns.scatterplot(x="BdFt", y= "Price (15/bf)", hue=heritageSpecies, data=dfsheet3)
plt.xlabel("BdFt")
plt.ylabel("Price")
plt.title("Visual Depiction of Price per board foot per type of wood that is being saved by UVA Sawmilling")
plt.show()

dates = dfWeights['Mill date']
#print(dates)
dates = dates.fillna('2024-02-24 00:00:00')
#print(dates)
weights = dfWeights['Weight']
#print(weights)
dateDict= {}

def addDict(start, weight):
  if sinceStart not in dateDict:
    dateDict[start] = [weight]
  else:
    dateDict[start].append(weight)

startDate = 9 *30 + 4
for index, date in enumerate(dates):
  year = int(date[0:4])
  month = int(date[5:7])
  day = int(date[8:10])
  sumDate = (year-2020)*365 + month * 30 + day
  sinceStart = sumDate - startDate

  addDict(sinceStart, float(weights[index]))
for key in dateDict:
  dateDict[key] = sum(dateDict[key])/2
#print(dateDict)

for i in range(len(dateDict.keys())):
  upToSum = 0
  keysList = list(dateDict.keys())
  upToSum = dateDict[keysList[i]] + dateDict[keysList[i-1]]
  dateDict[keysList[i]] = upToSum

#print(dateDict)

slope = 4.6 * 2204.623/365
x_values = np.array([0, 1300])
y_values = slope * x_values


plt.plot(dateDict.keys(), dateDict.values(), label='Trees')
plt.xlabel("Days since Start of Data Collection")
plt.ylabel("Amount of Carbon")
plt.title("Amount of Carbon contained in Trees cut down on UVA campus vs Cars Yearly output.")


plt.plot(x_values, y_values, label='Cars')

plt.show()

try:
  df = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx')
except FileNotFoundError:
  print("Error: Excel file not found.")
except pd.errors.ParserError:
  print("Error: Could not parse Excel file.")