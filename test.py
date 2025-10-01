#Riječnik ili dictionary
kosarica = {}

print(f"Prazna kosarica: {kosarica}")
print(f"Tip: {type(kosarica)}")

kosarica['jabuka'] = 25
kosarica['kreke'] = 23
kosarica['mandarine'] = 3

#Ispis riječnika
print(f"Napunjena košarica: {kosarica}")

kosarica['jabuka'] += 5
print(f"Ažurirana košarica: {kosarica}")

broj_mandarina = kosarica['mandarine']
print(f"Broj mandarina: {broj_mandarina}")

try:
    broj_krusaka = kosarica['kruska']
    print(f"Broj krusaka: {broj_krusaka}")
except Exception as e:
    print(f"Greška : {e}")

trazim_voce = 'kruška'
if trazim_voce in kosarica:
    print(f"Imamo {kosarica[trazim_voce]} komada voća '{trazim_voce}' u kosarici")
else:
    print(f"Nažalost, nemamo '{trazim_voce}' u kosarici")

trazim_voce = 'kreke'
if trazim_voce in kosarica:
    print(f"Imamo {kosarica[trazim_voce]} komada voća '{trazim_voce}' u kosarici")
else:
    print(f"Nažalost, nemamo '{trazim_voce}' u kosarici")
