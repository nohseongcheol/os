"""Layer-2/SLIP bridge. TCP, UDP and FTP are processed by the guest, not Python.

QEMU's user network supplies NAT/host forwarding. raspi4b has no emulated GENET,
so a second UART carries IPv4 packets to the guest's lwIP stack.
"""
import select
import socket
import struct
import threading
import time
import ipaddress
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, qemu_network

maschineAdresse = bytes.fromhex('525400123456')
netzübergangHardwareAdresse = bytes.fromhex('52550a000202')
internetAdresseWert = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class netzwerkBrücke:
    def __init__(selbstWert, dateiÜbertragungPortNummer=2121, weiterleitendRegeln=(), erfassen=False, gastAdresse=None, wirtssystemAdresse='127.0.0.1'):
        if not 1024 <= dateiÜbertragungPortNummer <= 65535 or 50000 <= dateiÜbertragungPortNummer <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        selbstWert.dateiÜbertragungPortNummer = dateiÜbertragungPortNummer
        selbstWert.ip_config = read_config(Path(__file__).resolve().parents[1])
        gastAdresse = gastAdresse or selbstWert.ip_config['IP']
        qemu_network(selbstWert.ip_config, gastAdresse)
        adresse=ipaddress.IPv4Address(gastAdresse)
        selbstWert.gastAdresse=str(adresse); selbstWert.aktuellAdresse=adresse.packed
        adresse=ipaddress.IPv4Address(wirtssystemAdresse)
        if adresse.is_multicast or str(adresse)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        selbstWert.wirtssystemAdresse=str(adresse)
        selbstWert.erfassen = erfassen; selbstWert.spurProtokolldatei = []
        selbstWert.weiterleitendRegeln = []
        belegt = {('tcp', dateiÜbertragungPortNummer)} | {('tcp', datenPosition) for datenPosition in range(50000,50008)}
        for regelWert in weiterleitendRegeln:
            pfadBaustein = regelWert.split(':')
            if len(pfadBaustein) != 3 or pfadBaustein[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            NetzwerkABI, Wirtssystem, gast = pfadBaustein[0], int(pfadBaustein[1]), int(pfadBaustein[2])
            if not 1024 <= Wirtssystem <= 65535 or not 1 <= gast <= 65535 or (NetzwerkABI, Wirtssystem) in belegt:
                raise ValueError('invalid or duplicate forward: ' + regelWert)
            belegt.add((NetzwerkABI, Wirtssystem)); selbstWert.weiterleitendRegeln.append((NetzwerkABI, Wirtssystem, gast))
        selbstWert.portsEmpfangen = []
        for _ in range(2):
            dienstanbieterWert = socket.socket()
            dienstanbieterWert.bind(('127.0.0.1', 0)); dienstanbieterWert.listen(1); dienstanbieterWert.setblocking(False)
            selbstWert.portsEmpfangen.append(dienstanbieterWert)
        selbstWert.gegenstellen = [None, None]
        selbstWert.istAusstehend = [bytearray(), bytearray()]
        selbstWert.ethernet = bytearray(); selbstWert.seriellDatagramm = bytearray(); selbstWert.maskiert = selbstWert.istUngültig = False
        selbstWert.pausierenEreignis = threading.Event(); selbstWert.fehler = None
        selbstWert.rahmenlisteNachGast = selbstWert.rahmenlisteVonGast = 0
        selbstWert.hintergrundarbeiter = threading.Thread(target=selbstWert.zyklusWert, daemon=True)
        selbstWert.hintergrundarbeiter.start()

    def weitergeleitetArgument(selbstWert):
        seriellPortNummer, ethernetPort = [zeichenketteDaten.getsockname()[1] for zeichenketteDaten in selbstWert.portsEmpfangen]
        weiterleitendRegel = 'user,id=wan,' + qemu_network(selbstWert.ip_config, selbstWert.gastAdresse) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(selbstWert.dateiÜbertragungPortNummer, selbstWert.gastAdresse)
        for portNummer in range(50000, 50008):
            weiterleitendRegel += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(portNummer, selbstWert.gastAdresse)
        for NetzwerkABI, Wirtssystem, gast in selbstWert.weiterleitendRegeln:
            weiterleitendRegel += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(NetzwerkABI, Wirtssystem, selbstWert.gastAdresse, gast)
        weiterleitendRegel=weiterleitendRegel.replace('127.0.0.1:',selbstWert.wirtssystemAdresse+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(seriellPortNummer),
                '-serial', 'chardev:slip', '-netdev', weiterleitendRegel,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ethernetPort),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def ausführungRahmen(selbstWert, paketDaten):
        selbstWert.istAusstehend[1] += struct.pack('!I', len(paketDaten)) + paketDaten

    def spurPaket(selbstWert, richtung, paketDaten):
        if not selbstWert.erfassen or len(paketDaten)<20: return
        versatzwertWert=(paketDaten[0]&15)*4
        eintragWert={'time':time.monotonic(),'direction':richtung,'bytes':len(paketDaten),'protocol':paketDaten[9]}
        if paketDaten[9]==6 and len(paketDaten)>=versatzwertWert+20:
            ursprünglichDaten,zielDatenAdresse,reihenfolgeNummer,bestätigungNummer,konfigurationBitliste,fenster=struct.unpack_from('!HHIIHH',paketDaten,versatzwertWert)
            eintragWert.update(source=ursprünglichDaten,destination=zielDatenAdresse,seq=reihenfolgeNummer,ack=bestätigungNummer,flags=konfigurationBitliste&255,window=fenster,
                        payload=len(paketDaten)-versatzwertWert-((paketDaten[versatzwertWert+12]>>4)*4))
        selbstWert.spurProtokolldatei.append(eintragWert)
        if len(selbstWert.spurProtokolldatei)>2048: del selbstWert.spurProtokolldatei[:1024]

    def sLIPEingabe(selbstWert, Daten):
        for zeichenKode in Daten:
            if zeichenKode == 192:
                if selbstWert.seriellDatagramm and not selbstWert.istUngültig and not selbstWert.maskiert:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(selbstWert.seriellDatagramm)>=20 and selbstWert.seriellDatagramm[0]>>4==4:
                        adresse=bytes(selbstWert.seriellDatagramm[12:16])
                        try:
                            qemu_network(selbstWert.ip_config, str(ipaddress.IPv4Address(adresse)))
                            selbstWert.aktuellAdresse=adresse
                        except ValueError:
                            pass
                    selbstWert.spurPaket('from_guest',selbstWert.seriellDatagramm)
                    selbstWert.ausführungRahmen(netzübergangHardwareAdresse + maschineAdresse + b'\x08\x00' + selbstWert.seriellDatagramm)
                    selbstWert.rahmenlisteVonGast += 1
                selbstWert.seriellDatagramm.clear(); selbstWert.maskiert = selbstWert.istUngültig = False
            elif zeichenKode == 219 and not selbstWert.maskiert:
                selbstWert.maskiert = True
            else:
                if selbstWert.maskiert:
                    if zeichenKode not in (220, 221): selbstWert.istUngültig = True
                    zeichenKode = 192 if zeichenKode == 220 else 219
                    selbstWert.maskiert = False
                if len(selbstWert.seriellDatagramm) < 1600: selbstWert.seriellDatagramm.append(zeichenKode)
                else: selbstWert.istUngültig = True

    def ethernetEingabe(selbstWert, Daten):
        selbstWert.ethernet += Daten
        while len(selbstWert.ethernet) >= 4:
            elementeintragAnzahl = struct.unpack_from('!I', selbstWert.ethernet)[0]
            if elementeintragAnzahl > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(selbstWert.ethernet) < elementeintragAnzahl + 4: return
            ausführungRahmen = bytes(selbstWert.ethernet[4:4+elementeintragAnzahl]); del selbstWert.ethernet[:4+elementeintragAnzahl]
            if len(ausführungRahmen) < 14: continue
            if ausführungRahmen[12:14] == b'\x08\x06' and len(ausführungRahmen) >= 42:
                adresseAuflösungPaket = ausführungRahmen[14:42]
                if adresseAuflösungPaket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and adresseAuflösungPaket[24:28] == selbstWert.aktuellAdresse:
                    rückmeldung = adresseAuflösungPaket[:6] + b'\x00\x02' + maschineAdresse + selbstWert.aktuellAdresse + adresseAuflösungPaket[8:18]
                    selbstWert.ausführungRahmen(ausführungRahmen[6:12] + maschineAdresse + b'\x08\x06' + rückmeldung)
            elif ausführungRahmen[12:14] == b'\x08\x00':
                paketDaten = ausführungRahmen[14:]
                selbstWert.spurPaket('to_guest',paketDaten)
                selbstWert.istAusstehend[0] += b'\xc0' + paketDaten.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                selbstWert.rahmenlisteNachGast += 1

    def zyklusWert(selbstWert):
        try:
            while not selbstWert.pausierenEreignis.is_set():
                leserListe = [zeichenketteDaten for ordnungszahlIndex, zeichenketteDaten in enumerate(selbstWert.portsEmpfangen) if selbstWert.gegenstellen[ordnungszahlIndex] is None]
                leserListe += [zeichenketteDaten for zeichenketteDaten in selbstWert.gegenstellen if zeichenketteDaten is not None]
                schreiberListe = [zeichenketteDaten for ordnungszahlIndex, zeichenketteDaten in enumerate(selbstWert.gegenstellen) if zeichenketteDaten is not None and selbstWert.istAusstehend[ordnungszahlIndex]]
                kannLesen, beschreibbar, _ = select.select(leserListe, schreiberListe, [], .05)
                for zeichenketteDaten in kannLesen:
                    if zeichenketteDaten in selbstWert.portsEmpfangen:
                        ordnungszahlIndex = selbstWert.portsEmpfangen.index(zeichenketteDaten); selbstWert.gegenstellen[ordnungszahlIndex], _ = zeichenketteDaten.accept(); selbstWert.gegenstellen[ordnungszahlIndex].setblocking(False)
                    else:
                        ordnungszahlIndex = selbstWert.gegenstellen.index(zeichenketteDaten); Daten = zeichenketteDaten.recv(16384)
                        if not Daten: return
                        (selbstWert.sLIPEingabe if ordnungszahlIndex == 0 else selbstWert.ethernetEingabe)(Daten)
                for zeichenketteDaten in beschreibbar:
                    ordnungszahlIndex = selbstWert.gegenstellen.index(zeichenketteDaten)
                    try: elementeintragAnzahl = zeichenketteDaten.send(selbstWert.istAusstehend[ordnungszahlIndex])
                    except BlockingIOError: continue
                    del selbstWert.istAusstehend[ordnungszahlIndex][:elementeintragAnzahl]
                if any(len(zweiterWert) > 1024 * 1024 for zweiterWert in selbstWert.istAusstehend):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as hilfsEintrag:
            if not selbstWert.pausierenEreignis.is_set(): selbstWert.fehler = str(hilfsEintrag)

    def schließen(selbstWert):
        selbstWert.pausierenEreignis.set(); selbstWert.hintergrundarbeiter.join(timeout=2)
        for zeichenketteDaten in selbstWert.portsEmpfangen + selbstWert.gegenstellen:
            if zeichenketteDaten is not None: zeichenketteDaten.close()

    def __enter__(selbstWert): return selbstWert
    def __exit__(selbstWert, *argumentDatenfeld): selbstWert.schließen()
