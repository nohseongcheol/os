#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from arbeitsflächeAnsicht import exaktWert
from BeispielEchoServer import WiedergebenDienstanbieterliste
from befehlAusführen import projektWurzel


def sprachePrüfung(Sprache,wiedergebenDienstanbieterEintrag,ergebnisDaten):
    with socket.socket() as vorläufig:
        vorläufig.bind(('127.0.0.1',0));dateiÜbertragungPortNummer=vorläufig.getsockname()[1]
    prozess=subprocess.Popen(['python3',str(projektWurzel/'Werkzeuge/befehlAusführen.py'),'--desktop','--network','--port','0','--ftp-port',str(dateiÜbertragungPortNummer)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    auswähler=selectors.DefaultSelector();auswähler.register(prozess.stdout,selectors.EVENT_READ)
    ablaufprotokoll=bytearray();anfragestelle=None;dateiÜbertragungVerbindung=None
    def nachrichtEmpfangen(markierung,ausführenVorgang=0):
        endeVersatzwert=time.monotonic()+60
        while markierung not in ablaufprotokoll[ausführenVorgang:]:
            if time.monotonic()>endeVersatzwert or prozess.poll() is not None:raise AssertionError(ablaufprotokoll[ausführenVorgang:].decode('utf-8','replace'))
            for gedrücktWert,_ in auswähler.select(.1):
                Daten=gedrücktWert.fileobj.read(65536)
                if Daten:ablaufprotokoll.extend(Daten)
        return ablaufprotokoll[ausführenVorgang:].decode('utf-8','replace').replace('\r\n','\n')
    def gedrücktWert(symbolWert,istDrückend=True):anfragestelle.sendall(struct.pack('>BBHI',4,int(istDrückend),0,symbolWert))
    def versatzwertStarten(zeile):
        ausführenVorgang=len(ablaufprotokoll)
        for zeichenKode in zeile+'\n':
            symbolWert=0xff0d if zeichenKode=='\n' else ord(zeichenKode) if ord(zeichenKode)<256 else 0x1000000|ord(zeichenKode)
            gedrücktWert(symbolWert);gedrücktWert(symbolWert,False)
        return ausführenVorgang
    def befehlshülle(zeile):return nachrichtEmpfangen(b'jkoros-native> ',versatzwertStarten(zeile))
    def befehlAusführen(zeile,erwartet):
        Text=befehlshülle(zeile);assert erwartet in Text and 'exit 0' in Text,(zeile,Text)
        return Text
    def bildpunkteListe():
        anfragestelle.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        rGBFarbe=bytearray(640*480*3)
        while True:
            kategorieWert=exaktWert(anfragestelle,1)[0]
            if kategorieWert==2:continue
            if kategorieWert==3:
                elementeintragAnzahl=struct.unpack('>I',exaktWert(anfragestelle,7)[3:])[0];exaktWert(anfragestelle,elementeintragAnzahl);continue
            assert kategorieWert==0,kategorieWert
            eintragAnzahl=struct.unpack('>H',exaktWert(anfragestelle,3)[1:])[0]
            for _ in range(eintragAnzahl):
                waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert,angefordertHöheWert,Zeichensatz=struct.unpack('>HHHHi',exaktWert(anfragestelle,12));assert Zeichensatz==0,Zeichensatz
                Daten=exaktWert(anfragestelle,angefordertBreiteWert*angefordertHöheWert*4)
                for zeilennummerPosition in range(angefordertHöheWert):
                    for spaltePosition in range(angefordertBreiteWert):
                        ursprünglichDaten=(zeilennummerPosition*angefordertBreiteWert+spaltePosition)*4;zielobjektWert=((senkrechteKoordinateKoordinate+zeilennummerPosition)*640+waagerechteKoordinateKoordinate+spaltePosition)*3
                        rGBFarbe[zielobjektWert:zielobjektWert+3]=bytes((Daten[ursprünglichDaten+2],Daten[ursprünglichDaten+1],Daten[ursprünglichDaten]))
            if eintragAnzahl:return rGBFarbe
    try:
        nachrichtEmpfangen(b'TERMINAL READY');nachrichtEmpfangen(b'jkoros-native> ',ablaufprotokoll.rfind(b'TERMINAL READY'))
        portNummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',ablaufprotokoll).group(1))
        anfragestelle=socket.create_connection(('127.0.0.1',portNummer),timeout=10)
        assert exaktWert(anfragestelle,12)==b'RFB 003.008\n';anfragestelle.sendall(b'RFB 003.008\n')
        assert 1 in exaktWert(anfragestelle,exaktWert(anfragestelle,1)[0]);anfragestelle.sendall(b'\x01');assert exaktWert(anfragestelle,4)==b'\0'*4
        anfragestelle.sendall(b'\x01');anfänglichWert=exaktWert(anfragestelle,24);exaktWert(anfragestelle,struct.unpack('>I',anfänglichWert[20:])[0])
        anfragestelle.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        anfragestelle.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in befehlshülle('ftpd start')
        dateiÜbertragungVerbindung=ftplib.FTP();dateiÜbertragungVerbindung.encoding='utf-8';dateiÜbertragungVerbindung.connect('127.0.0.1',dateiÜbertragungPortNummer,timeout=20);dateiÜbertragungVerbindung.login()
        nutzdatenDaten=('GUI와 FTP 동시 benutzenWert '+Sprache+' 😀\n').encode()
        dateiÜbertragungVerbindung.storbinary('STOR 함께.txt',io.BytesIO(nutzdatenDaten))
        assert nutzdatenDaten.decode().strip() in befehlshülle('cat /함께.txt')
        empfangenWertAnzahl=bytearray();dateiÜbertragungVerbindung.retrbinary('RETR 함께.txt',empfangenWertAnzahl.extend);assert empfangenWertAnzahl==nutzdatenDaten;dateiÜbertragungVerbindung.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        listeSenden=befehlshülle('ls /example')
        assert all(Name in listeSenden for Name in ('java/','c/','python/','README.md')),listeSenden
        if Sprache=='java':
            bündelInhaltsverzeichnis=json.loads((projektWurzel/'build/examples/manifest.json').read_text())
            for pfad,eintragPunkt in bündelInhaltsverzeichnis.items():
                befehlshülle('cp '+pfad+' /example-check.bin')
                inhaltswertWert=bytearray();dateiÜbertragungVerbindung.retrbinary('RETR example-check.bin',inhaltswertWert.extend)
                assert len(inhaltswertWert)==eintragPunkt['bytes'] and hashlib.sha256(inhaltswertWert).hexdigest()==eintragPunkt['sha256'],pfad
            dateiÜbertragungVerbindung.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binär=bytes(range(256))*64
            dateiÜbertragungVerbindung.storbinary('STOR boundary.bin',io.BytesIO(binär))
            inhaltswertWert=bytearray();dateiÜbertragungVerbindung.retrbinary('RETR boundary.bin',inhaltswertWert.extend)
            assert inhaltswertWert==binär and 'boundary.bin' in dateiÜbertragungVerbindung.nlst()
            befehlshülle('cp /boundary.bin /boundary-copy.bin')
            inhaltswertWert=bytearray();dateiÜbertragungVerbindung.retrbinary('RETR boundary-copy.bin',inhaltswertWert.extend)
            assert inhaltswertWert==binär
            dateiÜbertragungVerbindung.delete('boundary.bin');dateiÜbertragungVerbindung.delete('boundary-copy.bin')
        assert 'Ausgabebeispiel' in befehlshülle('ls /example/'+Sprache)
        befehlshülle('cd /example/'+Sprache)
        nameTabelle={'java':'JAVA','c':'C','python':'PYTHON'}[Sprache]
        erwartetDatei=nameTabelle+' Datei: 한글 Daten 😀\n'
        if Sprache=='java':
            befehlAusführen('javac Ausgabebeispiel.java','Compiled:');befehlAusführen('java Ausgabebeispiel','JAVA Ausgabe: 안녕하세요 😀')
            befehlAusführen('javac Dateibeispiel.java','Compiled:');befehlAusführen('java Dateibeispiel',erwartetDatei)
            befehlAusführen('java Netzbeispiel {} {}'.format(wiedergebenDienstanbieterEintrag.tCPPort,wiedergebenDienstanbieterEintrag.uDPPort),'JAVA 네트워크 überprüfen: TCP UDP 한글')
            grafikBefehl='java Grafikbeispiel'
        elif Sprache=='c':
            for Name,weitergeleitetWert,erwartet in [('Ausgabe','', 'C Ausgabe: 안녕하세요 😀'),('Datei','',erwartetDatei),
                    ('네트워크',' '+str(wiedergebenDienstanbieterEintrag.uDPPort),'C 네트워크 überprüfen: UDP 한글')]:
                befehlAusführen('cc '+Name+'Beispiele.c -o befehlAusführen','Compiled native ARM64 ELF:')
                befehlAusführen('./befehlAusführen'+weitergeleitetWert,erwartet)
            befehlAusführen('cc Grafikbeispiel.c -o befehlAusführen','Compiled native ARM64 ELF:');grafikBefehl='./befehlAusführen'
        else:
            for Name,weitergeleitetWert,erwartet in [('Ausgabe','','PYTHON Ausgabe: 안녕하세요 😀'),('Datei','',erwartetDatei),
                    ('네트워크',' '+str(wiedergebenDienstanbieterEintrag.uDPPort),'PYTHON 네트워크 überprüfen: UDP 한글')]:
                befehlAusführen('python '+Name+'Beispiele.py'+weitergeleitetWert,erwartet)
            grafikBefehl='python Grafikbeispiel.py'
        zeichnungStarten=versatzwertStarten(grafikBefehl)
        Text=nachrichtEmpfangen('그림을 확인한 rückseiteWert Enter를 누르세요.\r\n'.encode(),zeichnungStarten)
        assert nameTabelle+' 그래픽: 빨강 초록 파랑' in Text and 'exit 0' not in Text,Text
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        dateiÜbertragungVerbindung.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        empfangenWertAnzahl=bytearray();dateiÜbertragungVerbindung.retrbinary('RETR 도중.txt',empfangenWertAnzahl.extend);assert empfangenWertAnzahl==b'FTP DURING GRAPHICS';dateiÜbertragungVerbindung.delete('도중.txt')
        rGBFarbe=bildpunkteListe()
        for senkrechteKoordinateKoordinate,bildpunktFarbe in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            versatzwertWert=(senkrechteKoordinateKoordinate*640+610)*3;assert tuple(rGBFarbe[versatzwertWert:versatzwertWert+3])==bildpunktFarbe,(Sprache,senkrechteKoordinateKoordinate,tuple(rGBFarbe[versatzwertWert:versatzwertWert+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(rGBFarbe)).save(str(ergebnisDaten/(Sprache+'-graphics.png')))
        gedrücktWert(0xff0d);gedrücktWert(0xff0d,False)
        assert 'exit 0' in nachrichtEmpfangen(b'jkoros-native> ',zeichnungStarten)
        if Sprache=='java':
            fensterStarten=versatzwertStarten('java Fensterbeispiel')
            nachrichtEmpfangen('GUI Beispiele vorbereiten: Fensterbeispiel'.encode(),fensterStarten)
            def klickenWert(waagerechtPosition,senkrechtPosition):
                for schaltfläche in (1,0):anfragestelle.sendall(struct.pack('>BBHH',5,schaltfläche,waagerechtPosition,senkrechtPosition))
            time.sleep(.3)
            vorherigAbbild=Image.frombytes('RGB',(640,480),bytes(bildpunkteListe()))
            klickenWert(160,196)
            for _ in range(2):gedrücktWert(0xff08);gedrücktWert(0xff08,False)
            for zeichenWert in '한글':gedrücktWert(0x1000000|ord(zeichenWert));gedrücktWert(0x1000000|ord(zeichenWert),False)
            for wiederholungAnzahl in (1,2):
                ausführenVorgang=len(ablaufprotokoll);klickenWert(180,242)
                nachrichtEmpfangen(('GUI Gruß: 안녕하세요, 한글님! ('+str(wiederholungAnzahl)+')').encode(),ausführenVorgang)
            time.sleep(.3)
            fensterZeichnung=Image.frombytes('RGB',(640,480),bytes(bildpunkteListe()))
            assert vorherigAbbild.crop((110,272,530,300)).tobytes()!=fensterZeichnung.crop((110,272,530,300)).tobytes()
            fensterZeichnung.save(str(ergebnisDaten/'java-swing.png'))
            ausführenVorgang=len(ablaufprotokoll);klickenWert(535,105)
            assert 'exit 0' in nachrichtEmpfangen(b'jkoros-native> ',ausführenVorgang)
        # Download the guest-created bytes through FTP in the same GUI VM.
        dateiEintragName={'java':'java.txt','c':'c.txt','python':'python.txt'}[Sprache]
        befehlshülle('cp '+dateiEintragName+' /validieren.txt')
        empfangenWertAnzahl=bytearray();dateiÜbertragungVerbindung.retrbinary('RETR validieren.txt',empfangenWertAnzahl.extend);assert empfangenWertAnzahl==erwartetDatei.encode()
        befehlshülle('echo preserved > Ausgabebeispiel.'+('py' if Sprache=='python' else Sprache))
        assert 'EXAMPLES READY' in befehlshülle('example '+Sprache)
        assert '\npreserved\n' in befehlshülle('cat Ausgabebeispiel.'+('py' if Sprache=='python' else Sprache))
        assert '한/nullwertOperand tasteWert, Shift+Space 또는 F9' in befehlshülle('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in befehlshülle('echo GUI NETWORK TOGETHER')
        dateiÜbertragungVerbindung.quit();dateiÜbertragungVerbindung=None;assert 'FTP stopped' in befehlshülle('ftpd stop')
        print('PASS '+Sprache+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if dateiÜbertragungVerbindung:
            try:dateiÜbertragungVerbindung.close()
            except OSError:pass
        if anfragestelle:anfragestelle.close()
        prozess.terminate()
        try:prozess.wait(timeout=8)
        except subprocess.TimeoutExpired:prozess.kill();prozess.wait()
        auswähler.close();prozess.stdout.close();(ergebnisDaten/(Sprache+'-serial.log')).write_bytes(ablaufprotokoll)


def ausführenVorgang():
    ergebnisDaten=projektWurzel/'build/verification/examples';ergebnisDaten.mkdir(parents=True,exist_ok=True)
    validierungBericht={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with WiedergebenDienstanbieterliste() as wiedergebenDienstanbieterEintrag:
            for Sprache in ('java','c','python'):
                sprachePrüfung(Sprache,wiedergebenDienstanbieterEintrag,ergebnisDaten);validierungBericht['languages'].append(Sprache)
            erwartet=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert wiedergebenDienstanbieterEintrag.hatEmpfangenWert==[(kategorieWert,Daten.encode()) for kategorieWert,Daten in erwartet],wiedergebenDienstanbieterEintrag.hatEmpfangenWert
            validierungBericht['host_network_payloads']=[{'protocol':kategorieWert,'text':Daten.decode()} for kategorieWert,Daten in wiedergebenDienstanbieterEintrag.hatEmpfangenWert]
        validierungBericht.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ergebnisDaten/'report.json').write_text(json.dumps(validierungBericht,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ausführenVorgang()
