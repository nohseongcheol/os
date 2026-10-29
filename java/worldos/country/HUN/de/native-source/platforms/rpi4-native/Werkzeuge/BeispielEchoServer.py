#!/usr/bin/env python3
"""Deutsch 네트워크 예제용 Wirtssystem TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class WiedergebenDienstanbieterliste:
    def __init__(selbstWert,tCPPort=0,uDPPort=0):
        selbstWert.hatEmpfangenWert=[];selbstWert.ausführungsfäden=[]
        hatEmpfangenWert=selbstWert.hatEmpfangenWert
        class kennwertVerbindungAnfrage(socketserver.BaseRequestHandler):
            def handle(selbstWert):
                selbstWert.request.settimeout(5);Daten=bytearray()
                while b'\n' not in Daten and len(Daten)<=512:
                    fragmentWert=selbstWert.request.recv(512)
                    if not fragmentWert:return
                    Daten.extend(fragmentWert)
                hatEmpfangenWert.append(('tcp',bytes(Daten)));selbstWert.request.sendall(Daten)
        class datagrammKennwertAnfrage(socketserver.BaseRequestHandler):
            def handle(selbstWert):
                Daten,netzbuchseWert=selbstWert.request;hatEmpfangenWert.append(('udp',Daten));netzbuchseWert.sendto(Daten,selbstWert.client_address)
        selbstWert.verbindungSteuerung=socketserver.ThreadingTCPServer(('127.0.0.1',tCPPort),kennwertVerbindungAnfrage)
        try:selbstWert.datagrammSteuerung=socketserver.ThreadingUDPServer(('127.0.0.1',uDPPort),datagrammKennwertAnfrage)
        except Exception:selbstWert.verbindungSteuerung.server_close();raise
        selbstWert.verbindungSteuerung.daemon_threads=selbstWert.datagrammSteuerung.daemon_threads=True
        selbstWert.tCPPort=selbstWert.verbindungSteuerung.server_address[1];selbstWert.uDPPort=selbstWert.datagrammSteuerung.server_address[1]

    def __enter__(selbstWert):
        for dienstanbieterWert in (selbstWert.verbindungSteuerung,selbstWert.datagrammSteuerung):
            hintergrundarbeiter=threading.Thread(target=dienstanbieterWert.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            hintergrundarbeiter.start();selbstWert.ausführungsfäden.append(hintergrundarbeiter)
        return selbstWert

    def __exit__(selbstWert,*argumentDatenfeld):
        for dienstanbieterWert in (selbstWert.verbindungSteuerung,selbstWert.datagrammSteuerung):dienstanbieterWert.shutdown();dienstanbieterWert.server_close()
        for hintergrundarbeiter in selbstWert.ausführungsfäden:hintergrundarbeiter.join(timeout=1)


if __name__=='__main__':
    strukturanalysierer=argparse.ArgumentParser(description=__doc__)
    strukturanalysierer.add_argument('--tcp-port',type=int,default=9000);strukturanalysierer.add_argument('--udp-port',type=int,default=9001)
    argumentDatenfeld=strukturanalysierer.parse_args()
    with WiedergebenDienstanbieterliste(argumentDatenfeld.tcp_port,argumentDatenfeld.udp_port) as wiedergebenDienstanbieterEintrag:
        print('Wirtssystem TCP {}, UDP {} vorbereiten. 게스트 adresse: 10.0.2.2. verlassenProzessProgramm: Ctrl+C'.format(wiedergebenDienstanbieterEintrag.tCPPort,wiedergebenDienstanbieterEintrag.uDPPort),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
