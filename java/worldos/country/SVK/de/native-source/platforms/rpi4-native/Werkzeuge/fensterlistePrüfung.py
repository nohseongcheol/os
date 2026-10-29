#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from befehlAusführen import projektWurzel,befehl

def ausführenVorgang():
    zielWertPosition=projektWurzel/'build/verification/windows';zielWertPosition.mkdir(parents=True,exist_ok=True)
    validierungBericht={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest()};protokolldateiAufzeichnung=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as arbeitendPfad:
        attrappeSteuerungVerbindung=Path(arbeitendPfad)/'qmp.sock'
        datenPosition=subprocess.Popen(befehl()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(attrappeSteuerungVerbindung)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        Auswähler=selectors.DefaultSelector();Auswähler.register(datenPosition.stdout,selectors.EVENT_READ)
        def kennwertEreignis(sekundenEinheit=.1):
            for gedrücktWert,_ in Auswähler.select(sekundenEinheit):
                zweiterWert=gedrücktWert.fileobj.read(65536)
                if zweiterWert:protokolldateiAufzeichnung.extend(zweiterWert)
            assert b'PANIC:' not in protokolldateiAufzeichnung and b'HALTED' not in protokolldateiAufzeichnung,protokolldateiAufzeichnung[-2048:]
        def abwarten(markierung,aktuellPosition,sekundenEinheit=50):
            endeVersatzwert=time.monotonic()+sekundenEinheit
            while markierung not in protokolldateiAufzeichnung[aktuellPosition:]:
                if time.monotonic()>endeVersatzwert or datenPosition.poll() is not None:raise AssertionError(protokolldateiAufzeichnung[aktuellPosition:].decode('utf-8','replace'))
                kennwertEreignis()
            return bytes(protokolldateiAufzeichnung[aktuellPosition:])
        def senden(zweiterWert,markierung=b'jkoros-native> '):
            aktuellPosition=len(protokolldateiAufzeichnung);datenPosition.stdin.write(zweiterWert);datenPosition.stdin.flush();return abwarten(markierung,aktuellPosition)
        def befehlshülle(zeichenketteDaten):return senden((zeichenketteDaten+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def kurzwegWert(dritterIndex):return bytes([30,2,dritterIndex,0,0,0,0])
        def klickenSchaltfläche(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate):return bytes([30,1,1,waagerechteKoordinateKoordinate&255,waagerechteKoordinateKoordinate>>8,senkrechteKoordinateKoordinate&255,senkrechteKoordinateKoordinate>>8,30,1,0,waagerechteKoordinateKoordinate&255,waagerechteKoordinateKoordinate>>8,senkrechteKoordinateKoordinate&255,senkrechteKoordinateKoordinate>>8])
        def befehlBetriebsart():
            datenPosition.stdin.write(b'\x1b');datenPosition.stdin.flush();endeVersatzwert=time.monotonic()+.2
            while time.monotonic()<endeVersatzwert:kennwertEreignis(.03)
        try:
            abwarten(b'jkoros-native> ',0)
            befehlshülle('terminal');kennwertEreignis(.3)
            befehlshülle('mkdir first; cd first; export NAME=one')
            senden('vi ersterOrdnungszahl.py\n'.encode(),b'NORMAL')
            senden('i값 = 21\nprint(Wert * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            endeVersatzwert=time.monotonic()+3
            while time.monotonic()<endeVersatzwert:kennwertEreignis(.1)
            senden(kurzwegWert(1),b'TERMINAL FOCUS 2');kennwertEreignis(.2)
            assert b'/\r\n' in befehlshülle('pwd')
            befehlshülle('export NAME=two')
            senden('vi zweiterOrdnungszahl.txt\n'.encode(),b'NORMAL')
            senden('i두 번째 fenster\n'.encode(),b'INSERT')
            senden(klickenSchaltfläche(180,12),b'TERMINAL FOCUS 1');kennwertEreignis(.2)
            befehlBetriebsart();senden(b':wq\r')
            assert b'one:/first' in befehlshülle('echo "$NAME:$PWD"')
            assert 'Wert = 21\r\nprint(Wert * 2)'.encode() in befehlshülle('cat ersterOrdnungszahl.py')
            ergebnis=befehlshülle('python ersterOrdnungszahl.py');assert b'42\r\n' in ergebnis,ergebnis
            # Close the first shell with its actual title-bar X; second editor resumes.
            senden(klickenSchaltfläche(560,63),b'TERMINAL FOCUS 2');kennwertEreignis(.2)
            befehlBetriebsart();senden(b':wq\r')
            assert b'two:/' in befehlshülle('echo "$NAME:$PWD"')
            assert '두 번째 fenster'.encode() in befehlshülle('cat zweiterOrdnungszahl.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            senden('vi zweiterOrdnungszahl.txt\n'.encode(),b'NORMAL');senden(b'xu',b'NORMAL')
            senden(b'iX',b'INSERT');befehlBetriebsart();senden(b':q\r',b'Unsaved')
            senden(b':q!\r');assert '두 번째 fenster'.encode() in befehlshülle('cat zweiterOrdnungszahl.txt')
            senden(kurzwegWert(1),b'TERMINAL FOCUS 1');kennwertEreignis(.2)
            senden(kurzwegWert(1),b'TERMINAL FOCUS 3');kennwertEreignis(.2)
            senden(kurzwegWert(1),b'TERMINAL FOCUS 4');kennwertEreignis(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            datenPosition.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));datenPosition.stdin.flush()
            befehlshülle('echo DRAGGED_OK')
            senden('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            senden('i저장하지 않은 Daten'.encode(),b'INSERT')
            senden(klickenSchaltfläche(578,97),b'TERMINAL FOCUS 3');kennwertEreignis(.2)
            assert '버릴문서.txt'.encode() not in befehlshülle('ls')
            senden(kurzwegWert(1),b'TERMINAL FOCUS 4');kennwertEreignis(.2)
            befehlshülle('echo REUSED_WINDOW_OK')
            abgeschlossenGesamtmenge=protokolldateiAufzeichnung.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            abwarten(b'jkoros-native> ',abgeschlossenGesamtmenge)
            # UART completion precedes the next QEMU display refresh.
            endeVersatzwert=time.monotonic()+.3
            while time.monotonic()<endeVersatzwert:kennwertEreignis(.05)
            with socket.socket(socket.AF_UNIX) as zeichenKode:
                zeichenKode.settimeout(10);zeichenKode.connect(str(attrappeSteuerungVerbindung))
                with zeichenKode.makefile('rwb') as dateiEintrag:
                    json.loads(dateiEintrag.readline())
                    for anfrageWert in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(zielWertPosition/'four-terminals.png'),'format':'png'}}):
                        dateiEintrag.write((json.dumps(anfrageWert)+'\n').encode());dateiEintrag.flush()
                        while True:
                            zurückgegebenWert=json.loads(dateiEintrag.readline())
                            if 'error' in zurückgegebenWert:raise AssertionError(zurückgegebenWert)
                            if 'return' in zurückgegebenWert:break
            from PIL import Image
            bildpunkteListe=Image.open(str(zielWertPosition/'four-terminals.png')).convert('RGB')
            for koordinatePaar,bildpunktFarbe in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert bildpunkteListe.getpixel(koordinatePaar)==bildpunktFarbe,(koordinatePaar,bildpunkteListe.getpixel(koordinatePaar))
            befehlshülle('echo FOUR_WINDOWS_OK')
            validierungBericht.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if datenPosition.poll() is None:datenPosition.terminate()
            try:datenPosition.wait(timeout=5)
            except subprocess.TimeoutExpired:datenPosition.kill();datenPosition.wait()
            Auswähler.close();datenPosition.stdin.close();datenPosition.stdout.close();(zielWertPosition/'serial.log').write_bytes(protokolldateiAufzeichnung);(zielWertPosition/'report.json').write_text(json.dumps(validierungBericht,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ausführenVorgang()
