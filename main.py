import rp2
import network
import ubinascii
import machine
import time
import socket
import gc

from machine import Pin
from secrets import secrets

# === 1. WLAN-Einrichtung ===
rp2.country('DE')  # Ländercode für den LAN-Chip

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# MAC zum Debug
mac = ubinascii.hexlify(wlan.config('mac'), ':').decode()
print("MAC-Adresse:", mac)

ssid = secrets['ssid']
pw   = secrets['pw']

print("Verbinde mit WLAN:", ssid)
wlan.connect(ssid, pw)

# Bis zu 10 Sekunden auf Verbindung warten
timeout = 10
while timeout > 0:
    status = wlan.status()
    # status < 0   -> falsche Zugangsdaten
    # status == 3  -> erfolgreich verbunden
    if status < 0 or status >= 3:
        break
    timeout -= 1
    print("Warte auf WLAN…", timeout)
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError("WLAN-Verbindung fehlgeschlagen (Status {})".format(wlan.status()))
else:
    print("Verbunden. IP =", wlan.ifconfig()[0])

# === 2. HTTP-Server initialisieren ===
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
# Erlaubt Direkt-Bind an Port 80 nach Neustart
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print("HTTP-Server hört auf", wlan.ifconfig()[0], "Port 80")

gc.enable()

def serve_static(path, client):
    """
    Liefert statische Ressourcen in 512-Byte-Blöcken aus.
    - path   = der angefragte Pfad, z.B. '/index.html'
    - client = der Socket, über den wir antworten
    """
    if path == '/':
        path = '/index.html'
    filename = path.lstrip('/')

    # Grobes MIME-Type-Raten anhand der Dateiendung
    if filename.endswith('.html'):
        content_type = "text/html; charset=utf-8"
    elif filename.endswith('.css'):
        content_type = "text/css"
    elif filename.endswith('.js'):
        content_type = "application/javascript"
    elif filename.endswith('.png'):
        content_type = "image/png"
    else:
        content_type = "application/octet-stream"

    try:
        # Dateiimaginär öffnen und gesamten Inhalt lesen
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        total_length = len(data)
        print("  >> Datei gefunden, Länge:", total_length, "Bytes")

        # HTTP-Header aufbauen
        header  = "HTTP/1.0 200 OK\r\n"
        header += "Content-Type: " + content_type + "\r\n"
        header += "Content-Length: " + str(total_length) + "\r\n"
        header += "\r\n"

        # Header senden
        client.send(header.encode('utf-8'))

        # Datei-Inhalt in Blöcken à 512 Bytes senden
        chunk_size = 512
        sent = 0
        while sent < total_length:
            block = data[sent:sent + chunk_size]
            client.send(block)
            sent += len(block)
            # Kurz schlafen, damit Puffer geleert werden
            time.sleep(0.01)

        print("  >> Datei komplett gesendet.")
    except OSError as e:
        # 404 Not Found
        print("  !! Datei-Fehler:", e)
        err_body = "<h1>404 Not Found</h1>"
        err_hdr  = "HTTP/1.0 404 NOT FOUND\r\n"
        err_hdr += "Content-Type: text/html; charset=utf-8\r\n"
        err_hdr += "Content-Length: " + str(len(err_body)) + "\r\n"
        err_hdr += "\r\n"
        client.send(err_hdr.encode('utf-8'))
        client.send(err_body.encode('utf-8'))


# === 3. Haupt-Schleife – hier warten wir auf jeden neuen Client ===
while True:
    try:
        cl, addr = s.accept()
        print("==> Anfrage von", addr)

        # DREI SCHRITTE: 1) request-line lesen, 2) alle Header-Zeilen konsumieren, 3) serve_static()
        cl_file = cl.makefile('rwb', 0)

        # 1) Erste Zeile: "GET /pfad HTTP/1.1\r\n"
        request_line = cl_file.readline().decode('utf-8')
        if not request_line:
            cl.close()
            continue

        parts = request_line.split()
        if len(parts) < 2:
            cl.close()
            continue
        method = parts[0]
        path   = parts[1]
        print("Angeforderter Pfad:", path)

        # 2) Alle weiteren Header-Zeilen überspringen, bis Leerzeile
        while True:
            header_line = cl_file.readline()
            if not header_line or header_line == b'\r\n':
                break

        # 3) Statische Datei ausliefern
        serve_static(path, cl)

        cl.close()
        gc.collect()
    except Exception as e:
        print("Fehler in Verbindung:", e)
        try:
            cl.close()
        except:
            pass
        gc.collect()

