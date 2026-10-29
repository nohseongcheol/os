"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class WiedergebenPrüfaufbau:
    def __enter__(selbstWert):
        selbstWert.verbindungSteuerung = socket.socket(); selbstWert.verbindungSteuerung.bind(('127.0.0.1', 0)); selbstWert.verbindungSteuerung.listen(1)
        selbstWert.datagrammSteuerung = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); selbstWert.datagrammSteuerung.bind(('127.0.0.1', 0))
        selbstWert.verbindungSteuerung.settimeout(30); selbstWert.datagrammSteuerung.settimeout(30)
        selbstWert.tCPPort = selbstWert.verbindungSteuerung.getsockname()[1]; selbstWert.uDPPort = selbstWert.datagrammSteuerung.getsockname()[1]
        selbstWert.fehlerliste = []; selbstWert.hatEmpfangenWert = {}
        def verbindungSteuerung():
            try:
                verbindung, _ = selbstWert.verbindungSteuerung.accept()
                with verbindung:
                    verbindung.settimeout(5); Daten = bytearray()
                    while b'\n' not in Daten:
                        fragmentWert = verbindung.recv(512)
                        if not fragmentWert: raise RuntimeError('TCP EOF before request')
                        Daten.extend(fragmentWert)
                    selbstWert.hatEmpfangenWert['tcp'] = bytes(Daten); verbindung.sendall(Daten)
            except Exception as hilfsEintrag: selbstWert.fehlerliste.append(str(hilfsEintrag))
        def datagrammSteuerung():
            try:
                Daten, gegenstelleWert = selbstWert.datagrammSteuerung.recvfrom(512); selbstWert.hatEmpfangenWert['udp'] = Daten; selbstWert.datagrammSteuerung.sendto(Daten, gegenstelleWert)
            except Exception as hilfsEintrag: selbstWert.fehlerliste.append(str(hilfsEintrag))
        selbstWert.ausführungsfäden = [threading.Thread(target=dateiEintrag, daemon=True) for dateiEintrag in (verbindungSteuerung, datagrammSteuerung)]
        for terminalEintrag in selbstWert.ausführungsfäden: terminalEintrag.start()
        return selbstWert

    def __exit__(selbstWert, *argumentDatenfeld):
        selbstWert.verbindungSteuerung.close(); selbstWert.datagrammSteuerung.close()
        for terminalEintrag in selbstWert.ausführungsfäden: terminalEintrag.join(timeout=1)
