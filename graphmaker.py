import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dfMain = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Milling', converters={'Common Name': str})
dfHeritage = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Heritage slabs index', converters={'Common Name': str})


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

try:
  df = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx')
except FileNotFoundError:
  print("Error: Excel file not found.")
except pd.errors.ParserError:
  print("Error: Could not parse Excel file.")