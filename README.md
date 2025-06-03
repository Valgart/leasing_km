# Leasing-Kilometer-Rechner für Raspberry Pico W

Dieses Projekt wurde getestet und ist gedacht für den Einsatz auf einem **Raspberry Pico W**. Mit dem bereitgestellten Script kannst du schnell überprüfen, ob du innerhalb der Freikilometer deines Leasingvertrags bleibst.

---

## Funktionen

- Eingabe des **Übergabe-Datums** und des **KM-Standes** bei Fahrzeugübernahme  
- Eingabe der **Freikilometer pro Jahr** (laut Leasingvertrag)  
- Eingabe des **aktuellen KM-Standes**  

Anhand dieser Daten wird automatisch berechnet:

1. **Erlaubte Kilometer pro Tag** (basierend auf den Freikilometern pro Jahr)  
2. **Bisher gefahrene Kilometer** seit Fahrzeugübergabe  
3. **Differenz** zwischen bisher gefahrenen Kilometern und erlaubten Kilometern  
   - Befinden sich noch Freikilometer im Plus, wird der verbleibende Wert **grün** dargestellt  
   - Wurde das Freikilometer-Kontingent überschritten, erscheint der Fehlbetrag **rot**  

---

## Voraussetzungen

- Raspberry Pico W mit MicroPython-Firmware  
- WLAN-Zugangsdaten (`ssid` und `pw`) in einer Datei `secrets.py` (Schlüsselwort-Paar `{ 'ssid': 'DEIN_NETZWERK', 'pw': 'DEIN_PASSWORT' }`)  
- Die Dateien `main.py` und `index.html` müssen im Root-Verzeichnis des Pico abgelegt sein  
- Browser (auf einem Gerät im selben WLAN), um die Weboberfläche aufzurufen  

---

## Installation

1. **MicroPython auf den Pico laden**  
   - Lade die neueste MicroPython-HEX-Datei für Raspberry Pico W herunter.  
   - Verbinde den Pico im Boot-Modus mit dem PC und spiele die Firmware über das Raspberry Pi Imager Tool oder Thonny auf.

2. **Projektdateien hochladen**  
   - Erstelle lokal eine Datei `secrets.py` mit folgendem Inhalt (ersetze SSID und Passwort durch deine Daten):
     ```python
     secrets = {
       'ssid': 'DEIN_NETZWERK',
       'pw':   'DEIN_PASSWORT'
     }
     ```
   - Kopiere die Dateien `main.py`, `index.html` und `secrets.py` ins Wurzelverzeichnis des Pico (z. B. per Thonny → Rechtsklick auf den Pico → „Datei hochladen“).

3. **Pico neu starten**  
   - Starte den Pico neu (z. B. über Thonny: Run ▶).  
   - Die serielle Konsole sollte Folgendes anzeigen:
     ```
     MAC-Adresse: xx:xx:xx:xx:xx:xx
     Verbinde mit WLAN: DEIN_NETZWERK
     Verbunden. IP = 192.168.x.y
     HTTP-Server hört auf 192.168.x.y Port 80
     ```

---

## Nutzung

1. Öffne im Browser (Laptop oder Smartphone im selben WLAN) die Adresse des Pico, z. B.:  http://192.168.x.y/

2. Trage im Formular ein:
- **Leasing-Startdatum** (Datum, an dem du das Fahrzeug übernommen hast)  
- **Anfangs-Kilometerstand** (z. B. 0 oder den beim Leasingstart gelesenen Wert)  
- **Vertraglich erlaubte km pro Jahr** (z. B. 15 000)  
- **Aktueller Kilometerstand** (z. B. 6 500)  

3. Klicke auf **„Berechnen“**.  
4. Daraufhin werden automatisch angezeigt:
- **Vertraglich erlaubte km pro Tag**  
- **Bis heute erlaubter Maximal-KM-Stand**  
- **Verbleibende Freikilometer** (grün), oder  
- **Überschrittenes Kontingent** (rot)  

---

## Beispiel-Screenshot

![Screenshot](https://github.com/Valgart/leasing_km/blob/main/Screenshot%2003.06.2025%20um%2021.19.57%20PM.png)

---


## Hinweise / Troubleshooting

- **Kein WLAN**: Prüfe in der seriellen Konsole, ob die Anmeldung am WLAN erfolgreich war.  
- **Seite lädt nicht**: Stelle sicher, dass `index.html` korrekt im Root-Verzeichnis liegt und du die richtige IP-Adresse aufrufst (z. B. `/index.html`).  
- **JavaScript deaktiviert**: Stelle sicher, dass JavaScript im Browser aktiviert ist, da die Berechnung clientseitig erfolgt.  
- **Dark/Light-Mode**: Oben rechts kannst du zwischen hellem und dunklem Design wechseln.  

---


