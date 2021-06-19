#/usr/bin/python3.9

"""
visualizer.py
The script for visualizing the Canadian birth data from Ancestry's Civil War Records

Developed by Adam Payzant
"""
import csv
import matplotlib.pyplot as plt
import numpy as np

fields = []
rows = []

# Opens the csv file
with open("data/birth_refined.csv") as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Extracts the fields
    fields = next(csvreader)

    # Extracts the cells
    for row in csvreader:
        rows.append(row)

# Lets make the pie charts
hal = 0
ns = 0
mon = 0
qc = 0
ott = 0
tor = 0
on = 0

for r in rows:
    if "Halifax" in r[1]:
        hal += 1
    elif "Nova Scotia" in r[1]:
        ns += 1
    
    if "Montreal" in r[1]:
        mon += 1
    elif "Quebec" in r[1]:
        qc += 1

    if "Toronto" in r[1]:
        tor += 1
    elif "Ottawa" in r[1]:
        ott += 1
    elif "Ontario" in r[1]:
        on += 1

plt.pie(np.array([hal, ns]), labels=["Halifax", "Nova Scotia"])
plt.show()

plt.pie(np.array([mon, qc]), labels=["Montreal", "Quebec"])
plt.show()

plt.pie(np.array([ott, tor, on]), labels=["Ottawa", "Toronto", "Ontario"])
plt.show()


# Now lets do the province distribution
prov = {
    "Nova Scotia": 0,
    "New Brunswick": 0,
    "Quebec": 0,
    "Ontario": 0,
    "Manitoba": 0,
    "Saskatchewan": 0,
    "Alberta": 0,
    "British Columbia": 0,
    "Newfoundland": 0,
}

# Counts the number of occurances for each provinces
for r in rows:
    for k in prov.keys():
        if k in r[1]:
            prov[k] += 1
plt.bar(list(prov.keys()), list(prov.values()))
plt.xlabel("Provinces")
plt.ylabel("People enlisted")
plt.xticks(rotation=25)
plt.show()