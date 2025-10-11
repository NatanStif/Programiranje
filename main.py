#Funkcija za učitavanje teksta iz datoteke 
def ucitaj_tekst(filepath):
    try:
        # KOd za otvaranje datoteke ide ovdje
        with open (filepath, 'r', encoding='utf-8') as file:
            sadrzaj = file.read()
        return sadrzaj
    except FileNotFoundError:
        print(f"Greška: Datoteka na putanji '{filepath}' nije pronađena")
        return None # Vratit ćemo 'ništa' ako datoteka ne postoji
      
      # Funkcija za proišćavanje teksta 
def ocisti_tekst(tekst):
#Kod za pročišćavanje teksta ide ovdje
    tekst = tekst.lower()

    interpunkcija = ['.', ',', '!', '?', ':', '"', "'", '(', ')']
    for znak in interpunkcija:
        tekst = tekst.replace(znak, '')

    lista_rijeci = tekst.split()

    return lista_rijeci
       
def broji_rijeci(lista_rijeci):
    rijecnik = {}
    for rijec in lista_rijeci:
        if rijec in rijecnik:
            rijecnik[rijec] += 1
        else:
            rijecnik[rijec] = 1
    return rijecnik

STOP_WORDS = ['i', 'u', 'na', 'je', 'se', 'su', 's', 'za', 'o', 'a', 'pa', 'te', 'li', 'da']

def ukloni_stop_words(rjecnik_frekvencija, stop_words_lista):
    novi_rjecnik = {}
    for rijec, frekvencija in rjecnik_frekvencija.items():
        if rijec not in stop_words_lista:
            novi_rjecnik[rijec] = frekvencija
    return novi_rjecnik

def sortiraj_i_ispisi(rjecnik_frekvencija, broj_rijeci=15):
    sortirana_lista = sorted(rjecnik_frekvencija.items(), key=lambda x: x[1], reverse=True)
    print("")
    print(f"----- Top {broj_rijeci} najčešćih riječi -----")
    print("")
    index = 1
    for rijec_frekvencija in sortirana_lista[:broj_rijeci]:
        rijec = rijec_frekvencija[0]
        frekvencija = rijec_frekvencija[1]
        print(f"{index}. {rijec}: {frekvencija}")
        index += 1
    print("-" * 30)

if __name__=="__main__":
    filepath = "tekst.txt"
    print(f"----- Učitavam tekst iz datoteke: {filepath} -----")
    ucitani_tekst = ucitaj_tekst(filepath)
    if ucitani_tekst:
        print("")
        print("----- Učitani tekst je: -----")
        print("")
        print(ucitani_tekst)
    else:
        print("")
        print("----- Greška pri učitavanju datoteke. -----")

    ucitani_tekst = ocisti_tekst(ucitani_tekst)

    if ucitani_tekst:
        print("")
        print("-----Očišćeni tekst je: -----")
        print("")
        print(ucitani_tekst)
                
        rijeci_brojanje = broji_rijeci(ucitani_tekst)
        
        ocisceni_rijecnik = ukloni_stop_words(rijeci_brojanje, STOP_WORDS)

        # Sortiranje i ispis
        sortiraj_i_ispisi(ocisceni_rijecnik)
    else:
        print("")
        print("Greška pri očišćavanju teksta.")
