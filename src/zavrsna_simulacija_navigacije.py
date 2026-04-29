import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import requests


df_lokacije = pd.read_csv("moji_mars_podaci/mars_lokacije.csv", sep = ";", decimal = ",")
df_uzorci = pd.read_csv("moji_mars_podaci/mars_uzorci.csv", sep = ";", decimal = ",")


df_spojeno = pd.merge(
    df_lokacije,
    df_uzorci,
    on="ID_Uzorka")


df_filtrirano = df_spojeno[df_spojeno["Temp_Tla_C"] < 150]
df_anomalije = df_spojeno[df_spojeno["Temp_Tla_C"] > 149]

#Odnos temperature i vlažnosti tla

# Postavljanje platna (veličina slike)
plt.figure(figsize=(10, 6))

# Crtanje grafa - ti moraš postaviti x i y osi koristeći nazive stupaca iz df_mars
sns.scatterplot(
    data=df_filtrirano,
    x='Temp_Tla_C',
    y='H2O_Postotak',
    hue='Metan_Senzor',
    palette="deep")

# Dodavanje opisa (Neophodno za razumijevanje grafa)
plt.title('Odnos temperature i vlažnosti tla')
plt.xlabel('Temperatura')
plt.ylabel('Vlaga')

# Spremanje datoteke
plt.savefig('graph1_temp_h2o.png')
plt.show()


#Prostorna raspodjela dubine bušenja


# Postavljanje platna (veličina slike)
plt.figure(figsize=(10, 6))

# Crtanje grafa - ti moraš postaviti x i y osi koristeći nazive stupaca iz df_mars
sns.scatterplot(
    data=df_filtrirano,
    x='GPS_LONG',
    y='GPS_LAT',
    hue='Dubina_Busenja_cm',
    palette="crest")

# Dodavanje opisa (Neophodno za razumijevanje grafa)
plt.title('Prostorna raspodjela dubine bušenja')
plt.xlabel('Geografska dužina')
plt.ylabel('Geografska širina')

# Spremanje datoteke
plt.savefig('graph2_heatmap_depth.png')
plt.show()

# 3.
plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df_filtrirano,
    x='GPS_LONG',
    y='GPS_LAT',
    hue='Metan_Senzor')

# Dodavanje opisa (Neophodno za razumijevanje grafa)
plt.title('Lokacije pozitivne detekcije metana')
plt.xlabel('Geografska dužina')
plt.ylabel('Geografska širina')

# Spremanje datoteke
plt.savefig('graph3_methane_scatter.png')
plt.show()

# 4.

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df_filtrirano,
    x='GPS_LONG',
    y='GPS_LAT',
    alpha=0.3,
    hue='H2O_Postotak')

kandidati = df_filtrirano[(df_filtrirano['Metan_Senzor'] == 'Pozitivno') & (df_filtrirano['Organske_Molekule'] == "Da")]

sns.scatterplot(
    data=kandidati,
    x=kandidati['GPS_LONG'],
    y=kandidati['GPS_LAT'],
    marker='*',
    s=250,
    color='red',
    label='Kandidati za život')


plt.title('Geografska analiza uzoraka u krateru Jezero')
plt.xlabel('Geografska dužina')
plt.ylabel('Geografska širina')

# Spremanje datoteke

plt.savefig('graph4_scatter_plot.png')
plt.show()

# Završna mapa misije (Satelitski prikaz Jezero Kratera)

# 1. Priprema praznog platna
plt.figure(figsize=(12, 8))

# 2. Izračunavanje granica (extent) - tražimo minimum i maksimum GPS koordinata
# Format mora biti: [X_min, X_max, Y_min, Y_max]
extent_koordinate = [
    df_filtrirano['GPS_LONG'].min(),
    df_filtrirano['GPS_LONG'].max(),
    df_filtrirano['GPS_LAT'].min(),
    df_filtrirano['GPS_LAT'].max()]

# 3. Učitavanje i prikaz slike
slika_kratera = plt.imread('jezero_crater_satellite_map.jpg')
# Argument aspect='auto' dozvoljava slici da se razvuče preko cijelog grafa
plt.imshow(slika_kratera, extent=extent_koordinate, aspect='auto', alpha=0.7)

# 4. Sada preko slike normalno crtaš svoje točkice (scatter)
sns.scatterplot(
    data=df_filtrirano,
    x='GPS_LONG',
    y='GPS_LAT',
    alpha=0.3,
    hue='H2O_Postotak',
    palette='viridis',
    legend=False)

plt.scatter(
    kandidati['GPS_LONG'],
    kandidati['GPS_LAT'],
    marker='*',
    s=250,
    color='yellow',
    label='Kritične zone bušenja')

plt.title('Završna mapa misije (Satelitski prikaz Jezero Kratera)')
plt.xlabel('Geografska dužina')
plt.ylabel('Geografska širina')

# Spremanje datoteke

plt.savefig('graph5_jezero_mission_map.jpg')
plt.close()


misija = {
    "misija": "Nexus",
    "akcije": []
}

for index, red in kandidati.iterrows():

    akcija = {
        "ID_Uzorka": int(red['ID_Uzorka']),
        "lokacija": {
            "lat": float(red['GPS_LAT']),
            "lon": float(red['GPS_LONG'])
        },

        "naredbe": [
            {
                "tip": "NAVIGACIJA",
                "opis": "Robot se kreće do zadane lokacije"
            },

            {
                "tip": "SONDIRANJE",
                "dubina_cm": float(red['Dubina_Busenja_cm'])
            },

            {
                "tip": "SLANJE_PODATAKA",
                "parametri": {
                    "temperatura": float(red['Temp_Tla_C']),
                    "vlaga": float(red['H2O_Postotak']),
                    "metan": red['Metan_Senzor'],
                    "organske_molekule": bool(red['Organske_Molekule'])
                }
            }
        ]
    }

    misija["akcije"].append(akcija)

json_paket = json.dumps(misija, indent=4)

with open("nexus.json", "w") as f:
    f.write(json_paket)

url = "https://webhook.site/#!/view/03f33f00-c3a0-4a66-8b06-63f1af147efa"

response = requests.post(url, json=misija)

if response.status_code == 200:
    print("Uspješno poslano")
else:
    print(f"Greška pri slanju, error {response.status_code}")
