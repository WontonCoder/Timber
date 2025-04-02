import pandas as pd
import matplotlib as plt

dfMain = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Milling', converters={'Common Name': str})
dfHeritage = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Heritage slabs index', converters={'Common Name': str})


dfHeritageNames = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx', sheet_name='Sheet3', converters={'Common Name': str})


milledSpecies = dfMain['Common Name']
prices = dfHeritage['Price (15/bf)'] # Access data from a specific column
#print(milledSpecies)

heritageSpecies = dfHeritageNames['Common Name']
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
print(HSpeciesDct)

plt.plot()

try:
  df = pd.read_excel(r'C:\Users\wqj6ya\Downloads\Timber\FYE Sawmilling Data.xlsx')
except FileNotFoundError:
  print("Error: Excel file not found.")
except pd.errors.ParserError:
  print("Error: Could not parse Excel file.")