"""eigen 커널의 Datei·Kommunikation·Bildschirm 호출과 Deutsch ausnahme. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as Betriebssystem
import sys as Laufzeit

def Ausgabe(*Wert, trenner=" ", endung="\n", **altsystemArgumente):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in altsystemArgumente: altsystemArgumente["sep"] = trenner
    if "end" not in altsystemArgumente: altsystemArgumente["end"] = endung
    print(*Wert, **altsystemArgumente)

Ganzzahl = int
befehlArgumente = Laufzeit.argv
VersuchenErneutFehler = 11

class SystemFehler(OSError):
    def __init__(selbstWert, Nummer, beschreibung="Betriebssystem 작업에 실패했습니다."):
        super().__init__(Nummer, beschreibung)
        selbstWert.Nummer = Nummer
        selbstWert.beschreibung = beschreibung

def systemAufrufen(Funktion, *argumente):
    try:
        return Funktion(*argumente)
    except OSError as fehler:
        Nummer = fehler.args[0] if fehler.args else 0
        raise SystemFehler(Nummer)

def textKodieren(Text):
    return Text.encode("utf-8")

def textDekodieren(Daten):
    return Daten.decode("utf-8")

def dateiLesen(Name):
    return systemAufrufen(Betriebssystem.read, Name)

def dateiSchreiben(Name, Daten):
    return systemAufrufen(Betriebssystem.write, Name, Daten)

def dateiEntfernen(Name):
    return systemAufrufen(Betriebssystem.remove, Name)

def datagrammÖffnen(portNummer):
    return systemAufrufen(Betriebssystem.udp_open, portNummer)

def datagrammSenden(endpunkt, portNummer, Daten):
    return systemAufrufen(Betriebssystem.udp_send, endpunkt, portNummer, Daten)

def externDatagrammSenden(endpunkt, adresse, portNummer, Daten):
    return systemAufrufen(Betriebssystem.udp_sendto, endpunkt, adresse, portNummer, Daten)

def datagrammEmpfangen(endpunkt):
    return systemAufrufen(Betriebssystem.udp_recv, endpunkt)

def netzwerkSchließen(endpunkt):
    return systemAufrufen(Betriebssystem.udp_close, endpunkt)

def rechteckZeichnen(*argumente):
    return systemAufrufen(Betriebssystem.rect, *argumente)

def bildschirmGröße():
    return systemAufrufen(Betriebssystem.screen_size)

def fürZeichnungWarten():
    return systemAufrufen(Betriebssystem.wait_key)

millisekunden = Betriebssystem.ticks_ms
