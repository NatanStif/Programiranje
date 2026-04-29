**Simulacija stvarnih podataka: Vizualizacija i uplink**

---

## A. Izvršni sažetak (Executive Summary)

* **Analitički pipeline za obradu geoprostornih i kemijskih podataka prikupljenih unutar kratera Jezero na Marsu. Program identificira znanstveno relevantne lokacije s potencijalnim indikatorima biološke aktivnosti te generira navigacijske naloge za autonomni istraživački sustav. Program učitava dvije relacijske CSV tablice s podacima o lokacijama uzorkovanja i senzorskim očitanjima, spaja ih, filtrira anomalije te generira strukturirani JSON navigacijski nalog za robota-istraživača.**

* **Ključne funkcionalnosti:**

* * Učitavanje i spajanje relacijskih CSV podataka
* * Validacija i filtriranje senzorskih anomalija
* * Geoprostorna vizualizacija (5 grafova)
* * Generiranje JSON navigacijskog naloga (_nexus.json_)

---

## B. Metodologija obrade podataka (Data Wrangling)

* **Iz mape _moji_mars_podaci_ učitavamo CSV datoteke _mars_lokacije.csv_ i _mars_uzorci.csv_. Obje datoteke koriste ";" kao separator i "," kao decimalni znak.**

_df_lokacije = pd.read_csv("moji_mars_podaci/mars_lokacije.csv", sep=";", decimal=",")_

_df_uzorci   = pd.read_csv("moji_mars_podaci/mars_uzorci.csv",   sep=";", decimal=",")_

* **Datoteke se zatim spajaju po ključu _ID_Uzorka_.**

_df_spojeno = pd.merge(df_lokacije, df_uzorci, on="ID_Uzorka")_

* **Podaci se zatim filtriraju pomoću varijable _df_filtrirano_ i anomalije se zapisuju u varijablu _df_anomalije_.**

_df_filtrirano = df_spojeno[df_spojeno["Temp_Tla_C"] < 150]_

_df_anomalije  = df_spojeno[df_spojeno["Temp_Tla_C"] > 149]_

* **Podaci se filtriraju kako bi se izbjegli podaci sa greškama koji bi mogli kvariti podatke u daljnjem dijelu programa.**
---

## C. Geoprostorna analiza i vizualizacija

**1. Odnos temperature i vlažnosti tla**
   
   <img src="assets/graph1_temp_h2o.png" width="500">

* **Graf prikazuje odnos između temperature i vlažnosti tla, uz dodatnu dimenziju prisutnosti metana (hue).**

* **Može se uočiti da je metan prisutan na lokacijama sa niskom temperaturom i visokom količinom vlage**

**2. Prostorna raspodjela dubine bušenja**
   
   <img src="assets/graph2_heatmap_depth.png" width="500">

* **Graf prikazuje koordinate svih lokacija bušenja te koliko se duboko bušilo.**

* **Može se uočiti da se većinom buši dublje u određenim zonama**

**3. Lokacije pozitivne detekcije metana**
   
   <img src="assets/graph3_methane_scatter.png" width="500">
   
* **Graf prikazuje pozitivne i negativne metanske signale**

* **Može se uočiti da su metanski signali raspoređeni po zonama**

**4. Geografska analiza uzoraka u krateru Jezero**
   
   <img src="assets/graph4_scatter_plot.png" width="500">
   
   Na temelju filtriranih podataka izdvojene su lokacije koje zadovoljavaju uvjete:

* pozitivan metanski signal
* prisutnost organskih molekula

Takve lokacije označene su markerom visoke vidljivosti.

Interpretacija:

**5. Završna mapa misije (Satelitski prikaz Jezero Kratera)**
   
   <img src="assets/graph5_jezero_mission_map.jpg" width="500">
   
   Podaci su projicirani na satelitsku sliku korištenjem parametra "extent", koji definira granice prikaza slike u koordinatnom sustavu podataka:

[min_long, max_long, min_lat, max_lat]

Tehnički značaj:
Extent mapiranje omogućuje transformaciju piksel koordinata slike u realne GPS koordinate. Time se postiže precizno preklapanje analitičkih rezultata s vizualnim kontekstom terena, što je ključno za navigaciju autonomnih sustava.

---

## D. Komunikacijski protokol (JSON Uplink)

Izlazni sustav generira strukturirani JSON objekt koji sadržava listu kandidata za istraživanje. Svaki zapis uključuje identifikator uzorka, geopoziciju i skup akcija koje robot treba izvršiti.

Primjer strukture:
{
"kandidati": [
{
"ID_Uzorka": 101,
"GPS_LAT": 18.45,
"GPS_LONG": 77.52,
"akcije": [
{"tip": "NAVIGACIJA"},
{"tip": "SONDIRANJE"},
{"tip": "SLANJE_PODATAKA"}
]
}
]
}

Generiranje ovog izlaza implementirano je korištenjem iterativne petlje kroz filtrirani DataFrame. Time se omogućuje dinamičko skaliranje sustava – broj kandidata nije unaprijed definiran (izbjegnut je hardcoding), već ovisi isključivo o rezultatima analize.

---

## E. Inženjerski dnevnik (Troubleshooting Log)

1. Problem: Neispravno učitavanje CSV datoteka
   Simptom:
   Podaci su bili nepravilno parsirani zbog korištenja krivog separatora i decimalnog znaka.

Uzrok:
Datoteke su koristile ";" kao separator i "," kao decimalni znak.

Rješenje:
Eksplicitno definiranje parametara prilikom učitavanja:
sep=";" i decimal=","

---

2. Problem: Gubitak zapisa prilikom spajanja tablica
   Simptom:
   Nakon merge operacije broj redaka bio je manji od očekivanog.

Uzrok:
Nepodudaranje ID vrijednosti između tablica.

Rješenje:
Analiza presjeka ID-eva i potvrda da inner join uklanja nepodudarne zapise. Po potrebi bi se mogao koristiti left join, ali je u ovom slučaju konzistentnost podataka imala prioritet.

---

3. Problem: Neispravno prikazivanje satelitske slike
   Simptom:
   Podaci nisu bili poravnati sa slikom.

Uzrok:
Nedostatak pravilno definiranih granica (extent).

Rješenje:
Izračun minimalnih i maksimalnih GPS koordinata iz skupa podataka i njihova primjena na parametar extent.

---
