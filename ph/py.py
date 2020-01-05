# -*- coding: utf-8 -*-
# Versio 4.12.2018
'''.
Tietokannan syntaksi

DummyDataBase.txt

Card UID: XX XX XX XX
Name: x
Worker ID: XX XX XX X
Empty Line: x

Lokitiedoston syntaksi

Log.txt

Thursday PP.KK.VVVV HH:MM
Card UID: 
Name: 
Worker ID: 
LOGGED IN
'''

from datetime import datetime
import sys
import serial

Arduino_Serial = serial.Serial('COM8',9600)

# Tiedostot
tietokantatiedosto = "DummyDataBase.txt"
lokitiedosto = "Log.txt"

# Muuttujat
riveja_tietokannassa = 0
tyontekijoita_tietokannassa = 0
riveja_lokissa = 0
tapahtumia_lokissa = 0
tyontekijoita_listassa = 0

# Listat
card_id_lista = []
nimi_lista = []
worker_id_lista = []
loki_paivamaara_lista = []
loki_kellonaika_lista = []
loki_card_id_lista = []
loki_nimi_lista = []
loki_worker_id_lista = []
loki_tila_lista = []

def paavalikko():
	print("")
	print("(1) Lisää työntekijä")
	print("(2) Poista työntekijöitä")
	print("(3) Tulosta työntekijät")
	print("(4) Loki")
	print("(5) Poistu")

def lisaa_tyontekija():
	print("Lue kortti lukijalla")
	while True:
		rivi_arduinolta = lue_rivi_arduinolta()
		rivi_arduinolta = siisti_merkkijono_arduinolta(rivi_arduinolta)
		if "Card UID: " in rivi_arduinolta:
			card_id = str(rivi_arduinolta.replace("Card UID: ",""))
			nimi = input("Anna työntekijän nimi: ")
			worker_id = input("Anna työntekijän ID: ")
			card_id_lista.append(card_id)
			nimi_lista.append(nimi)
			worker_id_lista.append(worker_id)
			paivita_tietokanta()
			break

def poista_tyontekijoita():
	print("")
	print("(1) Poista yksittäinen tyontekijä")
	print("(2) Poista kaikki työntekijät")
	print("(3) Poistu")
	
	valinta = kysy_int()

	while valinta == 1:	# Poista yksittäinen työntekijä
		poista_yksittainen()
		break

	while valinta == 2:	# Poista kaikki työntekijät
		poista_kaikki()
		break
		
	while valinta == 3:	# Poistu
		break
		
def poista_yksittainen():
	print("")
	print("Valitse poistettava työntekijä")
	indeksi = 0
	jarjestysluku = 1
	tyontekijoita_listassa = len(nimi_lista)
	while indeksi < tyontekijoita_listassa:
		print(jarjestysluku, nimi_lista[indeksi])
		indeksi += 1
		jarjestysluku += 1
	valinta = kysy_int()
	indeksi = valinta - 1
	del card_id_lista[indeksi]
	del nimi_lista[indeksi]
	del worker_id_lista[indeksi]
	paivita_tietokanta()
	
def poista_kaikki():
	print("")
	print("Haluatko poistaa kaikki työntekijät? (y/n)")
	valinta = kysy_str()
	if valinta == "y":
		del card_id_lista[:]
		del nimi_lista[:]
		del worker_id_lista[:]
	paivita_tietokanta()

def tulosta_tyontekijat():
	print("")
	indeksi = 0
	tyontekijoita_listassa = len(nimi_lista)
	if tyontekijoita_listassa == 0:
		print("Tietokannassa ei ole työntekijöitä")
	else:
		print("Tietokannassa ovat seuraavat työntekijät:")
	while indeksi < tyontekijoita_listassa:
		print(nimi_lista[indeksi])
		indeksi += 1
		
def loki():
	print("")
	print("Näytä paikalla olleet työntekijät")
	print("(1) Tänään")
	print("(2) Tällä viikolla")
	print("(3) Tässä kuussa")
	print("(4) Näytä yksittäisen työntekijän työaika")
	print("(5) Poistu")
	# Palkka???
	
	valinta = kysy_int()
	
	while valinta == 1:
		paikalla_tanaan()
		break
	
	while valinta == 2:
		print("")
		break
	
	while valinta == 3:
		print("")
		break
	
	while valinta == 4:
		laske_tyoaika()
		break
		
	while valinta == 5:
		break
	
def paikalla_tanaan():
	print("")
	tama_paiva = datetime.now().strftime("%d.%m.%Y")
	indeksi = 0
	tapahtumia_lokissa = len(loki_paivamaara_lista)
	if tapahtumia_lokissa == 0:
		print("Loki on tyhjä")
	else:
		print("Tänään paikalla ovat olleet seuraavat työntekijät:")
	while indeksi < tapahtumia_lokissa:
		if tama_paiva == loki_paivamaara_lista[indeksi]:
			if loki_tila_lista[indeksi] == "LOGGED IN":
				print(loki_nimi_lista[indeksi])
		indeksi += 1
	
def laske_tyoaika():
	print("")
	print("Valitse työntekijä")
	indeksi = 0
	jarjestysluku = 1
	tyontekijoita_listassa = len(nimi_lista)
	while indeksi < tyontekijoita_listassa:
		print(jarjestysluku, nimi_lista[indeksi])
		indeksi += 1
		jarjestysluku += 1
	valinta = kysy_int()
	indeksi = valinta - 1
	
def paivita_tietokanta():
	tiedosto = open(tietokantatiedosto, "w")
	indeksi = 0
	tyontekijoita_listassa = len(nimi_lista)
	while indeksi < tyontekijoita_listassa:
		tiedosto.write("Card UID: ")
		tiedosto.write(card_id_lista[indeksi])
		tiedosto.write("\n")
		tiedosto.write("Name: ")
		tiedosto.write(nimi_lista[indeksi])
		tiedosto.write("\n")
		tiedosto.write("Worker ID: ")
		tiedosto.write(worker_id_lista[indeksi])
		tiedosto.write("\n")
		tiedosto.write("Empty Line")
		tiedosto.write("\n")
		indeksi += 1

def rivien_lkm_tiedostossa(a):
	tiedosto = open(a, "r")
	rivi = 0
	for line in tiedosto:
		rivin_sisalto = str(line)
		if rivin_sisalto == "":
			break
		else:
			rivi += 1
	return rivi

def nouda_card_id_tietokannasta():
	tiedosto = open(tietokantatiedosto, "r")
	indeksi = 0
	while indeksi < tyontekijoita_tietokannassa:
		rivi = 3
		for line in tiedosto:
			rivi += 1
			if rivi % 4 == 0:
				card_id = str(line)
				card_id = siisti_merkkijono_tiedostosta(card_id)
				card_id_lista.append(card_id)
				indeksi += 1

def nouda_nimet_tietokannasta():
	tiedosto = open(tietokantatiedosto, "r")
	indeksi = 0
	while indeksi < tyontekijoita_tietokannassa:
		rivi = 2
		for line in tiedosto:
			rivi += 1
			if rivi % 4 == 0:
				nimi = str(line)
				nimi = siisti_merkkijono_tiedostosta(nimi)
				nimi_lista.append(nimi)
				indeksi += 1

def nouda_worker_id_tietokannasta():
	tiedosto = open(tietokantatiedosto, "r")
	indeksi = 0
	while indeksi < tyontekijoita_tietokannassa:
		rivi = 1
		for line in tiedosto:
			rivi += 1
			if rivi % 4 == 0:
				worker_id = str(line)
				worker_id = siisti_merkkijono_tiedostosta(worker_id)
				worker_id_lista.append(worker_id)
				indeksi += 1
				
def nouda_aika_lokista():
	tiedosto = open(lokitiedosto, "r")
	indeksi = 0
	while indeksi < tapahtumia_lokissa:
		rivi = 4
		for line in tiedosto:
			rivi += 1
			if rivi % 5 == 0:
				rivin_sisalto = str(line)
				rivin_sisalto = siisti_merkkijono_tiedostosta(rivin_sisalto)
				kellonaika = rivin_sisalto[-5:]
				loki_kellonaika_lista.append(kellonaika)
				paivamaara = rivin_sisalto[:-6]
				paivamaara = paivamaara[-10:]
				loki_paivamaara_lista.append(paivamaara)
				indeksi += 1
				
def nouda_card_id_lokista():
	tiedosto = open(lokitiedosto, "r")
	indeksi = 0
	while indeksi < tapahtumia_lokissa:
		rivi = 3
		for line in tiedosto:
			rivi += 1
			if rivi % 5 == 0:
				aika = str(line)
				aika = siisti_merkkijono_tiedostosta(aika)
				loki_card_id_lista.append(aika)
				indeksi += 1
				
def nouda_nimet_lokista():
	tiedosto = open(lokitiedosto, "r")
	indeksi = 0
	while indeksi < tapahtumia_lokissa:
		rivi = 2
		for line in tiedosto:
			rivi += 1
			if rivi % 5 == 0:
				aika = str(line)
				aika = siisti_merkkijono_tiedostosta(aika)
				loki_nimi_lista.append(aika)
				indeksi += 1
				
def nouda_worker_id_lokista():
	tiedosto = open(lokitiedosto, "r")
	indeksi = 0
	while indeksi < tapahtumia_lokissa:
		rivi = 1
		for line in tiedosto:
			rivi += 1
			if rivi % 5 == 0:
				aika = str(line)
				aika = siisti_merkkijono_tiedostosta(aika)
				loki_worker_id_lista.append(aika)
				indeksi += 1
				
def nouda_tila_lokista():
	tiedosto = open(lokitiedosto, "r")
	indeksi = 0
	while indeksi < tapahtumia_lokissa:
		rivi = 0
		for line in tiedosto:
			rivi += 1
			if rivi % 5 == 0:
				aika = str(line)
				aika = siisti_merkkijono_tiedostosta(aika)
				loki_tila_lista.append(aika)
				indeksi += 1

def lue_rivi_arduinolta():
	rivi = Arduino_Serial.readline()
	return rivi

def siisti_merkkijono_arduinolta(sisaan):
	ulos = str(sisaan.decode('utf-8'))
	ulos = str(ulos.replace("\n",""))
	ulos = str(ulos.replace("\r",""))
	ulos = str(ulos.replace("b",""))
	ulos = str(ulos.replace("'",""))
	return ulos
	
def siisti_merkkijono_tiedostosta(sisaan):
	ulos = str(sisaan.replace("\n",""))
	ulos = str(ulos.replace("\r",""))
	ulos = str(ulos.replace("b",""))
	ulos = str(ulos.replace("'",""))
	ulos = str(ulos.replace("Card UID: ",""))
	ulos = str(ulos.replace("Name: ",""))
	ulos = str(ulos.replace("Worker ID: ",""))
	return ulos

def kysy_int():
	valinta = int(input(">>> "))
	return valinta

def kysy_str():
	valinta = str(input(">>> "))
	return valinta


riveja_tietokannassa = int(rivien_lkm_tiedostossa(tietokantatiedosto))
tyontekijoita_tietokannassa = int(riveja_tietokannassa / 4)
riveja_lokissa = int(rivien_lkm_tiedostossa(lokitiedosto))
tapahtumia_lokissa = int(riveja_tietokannassa / 5)

nouda_card_id_tietokannasta()
nouda_nimet_tietokannasta()
nouda_worker_id_tietokannasta()
nouda_aika_lokista()
nouda_card_id_lokista()
nouda_nimet_lokista()
nouda_worker_id_lokista()
nouda_tila_lokista()

tyontekijoita_listassa = int(len(nimi_lista))

print("Työntekijöiden hallinta")

while True:
	'''
	print("")
	print("Tietokannasta")
	print(card_id_lista)
	print(nimi_lista)
	print(worker_id_lista)
	print("")
	print("Lokista")
	print(loki_paivamaara_lista)
	print(loki_kellonaika_lista)
	print(loki_card_id_lista)
	print(loki_nimi_lista)
	print(loki_worker_id_lista)
	print(loki_tila_lista)
	'''
	
	paavalikko()
	valinta = kysy_int()

	while valinta == 1:	# Lisää työntekijä
		lisaa_tyontekija()
		break

	while valinta == 2:	# Poista työntekijöitä
		poista_tyontekijoita()
		break

	while valinta == 3:	# Tulosta työntekijät
		tulosta_tyontekijat()
		break

	while valinta == 4: # Loki
		loki()
		break

	while valinta == 5:	# Poistu
		paivita_tietokanta()
		sys.exit()
