"""eigen 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 Wirtssystem 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as Betriebssystem

listePfad = "/lib/.pip.json"


def fingerabdruckWert(Daten):
    return "".join("%02x" % Wert for Wert in hashlib.sha256(Daten).digest())


def listeLesen():
    if Betriebssystem.path_kind(listePfad) == 0:
        return {}
    return json.loads(Betriebssystem.read(listePfad).decode("utf-8"))


def protokolldateiSchreiben(pfad, Daten):
    if Betriebssystem.write(pfad, Daten) != len(Daten):
        raise OSError(28)


def pfadPrüfen(pfad):
    if not isinstance(pfad, str) or not pfad.endswith(".py"):
        raise ValueError("Python 소스만 설치할 Zahl 있습니다.")
    if any(unterteilWert in ("", ".", "..") or unterteilWert.startswith(".") for unterteilWert in pfad.split("/")):
        raise ValueError("허용하지 않는 Paket pfad")
    if "\\" in pfad or any(ord(zeichenWert) < 32 or ord(zeichenWert) == 127 for zeichenWert in pfad):
        raise ValueError("잘못된 pfad Zeichen")
    ergebnis = "/lib/" + pfad
    if len(ergebnis.encode("utf-8")) > 63 or pfad in ("Deutsch.py", "Paket.py"):
        raise ValueError("Paket 경로가 너무 길거나 standardwertWert 라이브러리와 겹칩니다.")
    return ergebnis


class datenstromEmpfangen:
    def __init__(selbstWert, endpunkt):
        selbstWert.endpunkt = endpunkt
        selbstWert.verbleibendDaten = b""
        selbstWert.ausführenVorgang = Betriebssystem.ticks_ms()

    def genauLesen(selbstWert, Länge):
        Daten = bytearray()
        while len(Daten) < Länge:
            if Betriebssystem.ticks_ms() - selbstWert.ausführenVorgang > 90000:
                raise ValueError("Paket wertWeitergeben antwort zeitWert 초과")
            if not selbstWert.verbleibendDaten:
                try:
                    selbstWert.verbleibendDaten = Betriebssystem.tcp_read(selbstWert.endpunkt, 512)
                except OSError as fehler:
                    if fehler.args[0] != 11:
                        raise
                    Betriebssystem.sleep_ms(10)
                    continue
                if not selbstWert.verbleibendDaten:
                    raise ValueError("Paket 전송이 중간에 끝났습니다.")
            elementeintragAnzahl = min(Länge - len(Daten), len(selbstWert.verbleibendDaten))
            Daten.extend(selbstWert.verbleibendDaten[:elementeintragAnzahl])
            selbstWert.verbleibendDaten = selbstWert.verbleibendDaten[elementeintragAnzahl:]
            Betriebssystem.sleep_ms(0)
        return bytes(Daten)


def herunterladen(anfrage, portNummer):
    if len(anfrage) > 96 or any(zeichenWert not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for zeichenWert in anfrage):
        raise ValueError("사용법: pip install Name 또는 Name==버전")
    endpunkt = Betriebssystem.tcp_open()
    try:
        ausführenVorgang = Betriebssystem.ticks_ms()
        while True:
            try:
                Betriebssystem.tcp_connect(endpunkt, "10.0.2.2", portNummer)
                break
            except OSError as fehler:
                if fehler.args[0] not in (11, 115) or Betriebssystem.ticks_ms() - ausführenVorgang > 5000:
                    raise ValueError("Paket wertWeitergeben verbinden fehlschlagWert: 호스트에서 --network --pip로 실행하십시오.")
                Betriebssystem.sleep_ms(10)
        Daten = (anfrage + "\n").encode()
        while Daten:
            try:
                elementeintragAnzahl = Betriebssystem.tcp_write(endpunkt, Daten)
                if not elementeintragAnzahl:
                    raise ValueError("Paket anfrage übertragungWert fehlschlagWert")
                Daten = Daten[elementeintragAnzahl:]
            except OSError as fehler:
                if fehler.args[0] != 11:
                    raise
                Betriebssystem.sleep_ms(10)
                if Betriebssystem.ticks_ms() - ausführenVorgang > 10000:
                    raise ValueError("Paket anfrage übertragungWert zeitWert 초과")
        datenstromWert = datenstromEmpfangen(endpunkt)
        kopfWert = datenstromWert.genauLesen(8)
        if kopfWert[:4] != b"JKP1":
            raise ValueError("Paket übertragungWert vertragWert 불일치")
        Länge = (kopfWert[4] << 24) | (kopfWert[5] << 16) | (kopfWert[6] << 8) | kopfWert[7]
        if Länge > 8192:
            raise ValueError("Paket 명세가 너무 큽니다.")
        vorgabe = json.loads(datenstromWert.genauLesen(Länge).decode())
        if "error" in vorgabe:
            raise ValueError(vorgabe["error"])
        if not 1 <= len(vorgabe["files"]) <= 16:
            raise ValueError("꾸러미당 quelltextBaum 파일은 1~16개여야 합니다.")
        if sum(eintragWert["size"] for eintragWert in vorgabe["files"]) > 65536:
            raise ValueError("Paket quelltextBaum 합계는 64 KiB 이하여야 합니다.")
        dateiEinträge = {}
        for eintragWert in vorgabe["files"]:
            pfad = pfadPrüfen(eintragWert["path"])
            if pfad in dateiEinträge or not 0 <= eintragWert["size"] <= 16384:
                raise ValueError("중복 pfad 또는 Datei größe 초과")
            Daten = datenstromWert.genauLesen(eintragWert["size"])
            if fingerabdruckWert(Daten) != eintragWert["sha256"]:
                raise ValueError("Paket Datei SHA-256 불일치")
            # 실행하지 않고 aktuellElementeintrag MicroPython의 문법으로 먼저 검사한다.
            compile(Daten.decode("utf-8"), pfad, "exec")
            dateiEinträge[pfad] = Daten
            gc.collect()
        return vorgabe, dateiEinträge
    finally:
        Betriebssystem.udp_close(endpunkt)


def wertEinrichten(anfrage, portNummer):
    print("Paket herunterladen:", anfrage)
    vorgabe, dateiEinträge = herunterladen(anfrage, portNummer)
    eintragListe = listeLesen()
    Name = vorgabe["name"]
    if Name in eintragListe:
        if eintragListe[Name]["version"] == vorgabe["version"]:
            for pfad, fingerabdruckDaten in eintragListe[Name]["files"].items():
                if Betriebssystem.path_kind(pfad) != 1 or fingerabdruckWert(Betriebssystem.read(pfad)) != fingerabdruckDaten:
                    raise ValueError("설치된 Paket 파일이 달라졌습니다: " + pfad)
            print("이미 설치됨:", Name, vorgabe["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 rückseiteWert 설치하십시오.")
    for pfad in dateiEinträge:
        if Betriebssystem.path_kind(pfad):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + pfad)
    eintragListe[Name] = {"version": vorgabe["version"], "files": {pfad: fingerabdruckWert(Daten) for pfad, Daten in dateiEinträge.items()}}
    neuListe = json.dumps(eintragListe).encode()
    if len(neuListe) > 16384:
        raise ValueError("Paket eintragListe größe 초과")
    vorherigListe = Betriebssystem.read(listePfad) if Betriebssystem.path_kind(listePfad) else None
    erstelltDatei = []
    erstelltVerzeichnis = []
    try:
        for pfad, Daten in dateiEinträge.items():
            teile = pfad.split("/")
            for Zahl in range(2, len(teile)):
                verzeichnisWert = "/".join(teile[:Zahl])
                artWert = Betriebssystem.path_kind(verzeichnisWert)
                if artWert == 0:
                    Betriebssystem.mkdir(verzeichnisWert)
                    erstelltVerzeichnis.append(verzeichnisWert)
                elif artWert != 2:
                    raise ValueError("verzeichnisWert 경로에 파일이 있습니다: " + verzeichnisWert)
            erstelltDatei.append(pfad)
            protokolldateiSchreiben(pfad, Daten)
        protokolldateiSchreiben(listePfad, neuListe)
    except Exception:
        for pfad in erstelltDatei:
            if Betriebssystem.path_kind(pfad):
                Betriebssystem.remove(pfad)
        for verzeichnisWert in reversed(erstelltVerzeichnis):
            Betriebssystem.rmdir(verzeichnisWert)
        if vorherigListe is not None:
            protokolldateiSchreiben(listePfad, vorherigListe)
        elif Betriebssystem.path_kind(listePfad):
            Betriebssystem.remove(listePfad)
        raise
    print("wertEinrichten istFertig:", Name, vorgabe["version"], "→ /lib (RAM)")


def eintragEntfernen(Name):
    eintragListe = listeLesen()
    if Name not in eintragListe:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Name)
    for pfad, fingerabdruckDaten in eintragListe[Name]["files"].items():
        if Betriebssystem.path_kind(pfad) != 1 or fingerabdruckWert(Betriebssystem.read(pfad)) != fingerabdruckDaten:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + pfad)
    for pfad in eintragListe[Name]["files"]:
        Betriebssystem.remove(pfad)
    del eintragListe[Name]
    protokolldateiSchreiben(listePfad, json.dumps(eintragListe).encode())
    print("eintragEntfernen istFertig:", Name)


def ausführenVorgang(argumente):
    portNummer = 8027
    if len(argumente) >= 2 and argumente[-2] == "--port":
        portNummer = int(argumente[-1])
        argumente = argumente[:-2]
    if argumente == ["list"]:
        for Name, systemInformation in listeLesen().items():
            print(Name, systemInformation["version"])
    elif len(argumente) == 2 and argumente[0] == "install":
        wertEinrichten(argumente[1], portNummer)
    elif len(argumente) == 2 and argumente[0] == "uninstall":
        eintragEntfernen(argumente[1])
    elif not argumente or argumente in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython quelltextBaum 설치기 (PyPA pip 전체가 아님)")
        print("pip install Name[==버전] [--port 8027] | pip list | pip uninstall Name")
        print("Wirtssystem: Werkzeuge/befehlAusführen.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ausführenVorgang(sys.argv[1:])
    except Exception as fehler:
        print("Paket fehler:", fehler)
        sys.exit(1)
