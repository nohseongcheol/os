#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from befehlAusführen import projektWurzel,befehl

def ausführenVorgang():
    zielWertPosition=projektWurzel/'build/verification/swing';zielWertPosition.mkdir(parents=True,exist_ok=True)
    klassePfad=projektWurzel/'build/verification/new-java';klassePfad.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projektWurzel/'dist/jkoros-native-korean.jar'),'-d',str(klassePfad),str(projektWurzel/'Prüfungen/Java/SwingPrüfung.java'),str(projektWurzel/'Prüfungen/Java/hangulFensterPrüfung.java')])
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
            Daten=(projektWurzel/'build/verification/new-java/SwingPrüfung.class').read_bytes()
            senden('load SwingPrüfung.class\n'.encode(),b'hex> ')
            for ordnungszahlIndex in range(0,len(Daten),64):senden(Daten[ordnungszahlIndex:ordnungszahlIndex+64].hex().encode()+b'\n',b'hex> ')
            senden(b'.\n')
            senden('java SwingPrüfung\n'.encode(),b'SWING READY')
            endeVersatzwert=time.monotonic()+3
            while time.monotonic()<endeVersatzwert:kennwertEreignis(.1)
            # JFrame centered at (120,100), content at y=130.
            senden(klickenSchaltfläche(200,210),b'',)  # focus JTextField
            datenPosition.stdin.write('누리'.encode());datenPosition.stdin.flush()
            endeVersatzwert=time.monotonic()+.3
            while time.monotonic()<endeVersatzwert:kennwertEreignis(.05)
            ergebnis=senden(klickenSchaltfläche(200,255),'SWING CLICK 이름누리'.encode())
            abwarten(b'true',len(protokolldateiAufzeichnung)-len(ergebnis))
            senden(kurzwegWert(1),b'TERMINAL FOCUS 2')
            ergebnis=befehlshülle('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ergebnis
            senden(klickenSchaltfläche(180,12),b'TERMINAL FOCUS 1')
            endeVersatzwert=time.monotonic()+.3
            while time.monotonic()<endeVersatzwert:kennwertEreignis(.05)
            with socket.socket(socket.AF_UNIX) as zeichenKode:
                zeichenKode.settimeout(10);zeichenKode.connect(str(attrappeSteuerungVerbindung))
                with zeichenKode.makefile('rwb') as dateiEintrag:
                    json.loads(dateiEintrag.readline())
                    for anfrageWert in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(zielWertPosition/'native-swing.png'),'format':'png'}}):
                        dateiEintrag.write((json.dumps(anfrageWert)+'\n').encode());dateiEintrag.flush()
                        while True:
                            zurückgegebenWert=json.loads(dateiEintrag.readline())
                            if 'error' in zurückgegebenWert:raise AssertionError(zurückgegebenWert)
                            if 'return' in zurückgegebenWert:break
            senden(klickenSchaltfläche(505,115))
            befehlshülle('echo SWING_CLOSED_OK')
            Daten=(klassePfad/'hangulFensterPrüfung.class').read_bytes()
            senden('load hangulFensterPrüfung.class\n'.encode(),b'hex> ')
            for ordnungszahlIndex in range(0,len(Daten),64):senden(Daten[ordnungszahlIndex:ordnungszahlIndex+64].hex().encode()+b'\n',b'hex> ')
            senden(b'.\n')
            senden('java hangulFensterPrüfung\n'.encode(),b'KOREAN SWING READY')
            senden(klickenSchaltfläche(200,255),'KOREAN SWING CLICK Name'.encode())
            senden(klickenSchaltfläche(505,115))
            befehlshülle('echo KOREAN_SWING_CLOSED_OK')
            validierungBericht.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Deutsch fenster/schaltfläche/AktionMitteilung/EreignisWarteschlange directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if datenPosition.poll() is None:datenPosition.terminate()
            try:datenPosition.wait(timeout=5)
            except subprocess.TimeoutExpired:datenPosition.kill();datenPosition.wait()
            Auswähler.close();datenPosition.stdin.close();datenPosition.stdout.close();(zielWertPosition/'serial.log').write_bytes(protokolldateiAufzeichnung);(zielWertPosition/'report.json').write_text(json.dumps(validierungBericht,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ausführenVorgang()
