# Leasing-Kilometer-Rechner

Ein moderner, browserbasierter Rechner für Leasing-Fahrzeuge. Gib Übergabe-Datum, anfänglichen Kilometerstand, vertragliche Freikilometer und den aktuellen Kilometerstand an, um sofort zu sehen, ob du im Kontingent liegst.

---

## Funktionen

- Eingabe von **Leasing-Startdatum**, **Anfangs-Kilometerstand**, **vertraglichen Freikilometern pro Jahr** und **aktuellem Kilometerstand**
- Berechnung von
  - **Erlaubten Kilometern pro Tag**
  - **Bis heute maximal zulässigem Kilometerstand**
  - **Rest-Freikilometern** oder **Überschreitung** (Farbcodierung)
- Umschaltbarer **Light/Dark-Mode** mit Speicherung der letzten Auswahl

---

## Voraussetzungen

- [Node.js](https://nodejs.org/) (empfohlen: LTS-Version) und npm
- Ein moderner Browser

---

## Installation & Start (npm)

1. Repository klonen und ins Projektverzeichnis wechseln
   ```bash
   git clone <repo-url>
   cd leasing_km
   ```
2. Abhängigkeiten installieren
   ```bash
   npm install
   ```
3. Entwicklungsserver starten
   ```bash
   npm run dev
   ```
   Der Vite-Server informiert dich über die lokale URL (standardmäßig `http://localhost:5173`).
4. (Optional) Produktionsbuild erzeugen
   ```bash
   npm run build
   ```
   Der fertige Build liegt anschließend im Verzeichnis `dist/` und kann von jedem beliebigen Static-File-Server ausgeliefert werden.

---

## Nutzung

1. Öffne die lokale URL des Entwicklungsservers.
2. Trage im Formular ein:
   - **Leasing-Startdatum**
   - **Anfangs-Kilometerstand**
   - **Vertraglich erlaubte km pro Jahr**
   - **Aktueller Kilometerstand**
3. Klicke auf **„Berechnen“**.
4. Du siehst sofort:
   - **Vertraglich erlaubte km pro Tag**
   - **Bis heute erlaubter Maximal-KM-Stand**
   - **Verbleibende Freikilometer** (grün) oder **Überschreitung** (rot)

---

## Screenshot

![Screenshot](https://github.com/Valgart/leasing_km/blob/main/Screenshot%2003.06.2025%20um%2021.19.57%20PM.png)

---

## Hinweise

- Die früheren Dateien `main.py`, `secrets.py` und `test.html` werden nicht mehr benötigt; das Projekt läuft komplett über npm und eine lokale Vite-Entwicklungsumgebung.
- Falls der Entwicklungsserver nicht erreichbar ist, prüfe, ob der von Vite ausgegebene Port (Standard: `5173`) offen ist und nicht von anderen Anwendungen belegt wird.
