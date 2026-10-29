#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Uitvoeren_opdracht import Taken_wortel,opdracht

def starten():
    doel_WAARDE_functie=Taken_wortel/'build/verification/swing';doel_WAARDE_functie.mkdir(parents=True,exist_ok=True)
    les_pad=Taken_wortel/'build/verification/new-java';les_pad.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Taken_wortel/'dist/jkoros-native-korean.jar'),'-d',str(les_pad),str(Taken_wortel/'tests/자바/Swing_test.java'),str(Taken_wortel/'tests/자바/한글창시험.java')])
    validatie_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        gegevens_functie=subprocess.Popen(opdracht()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selector_a916db4e=selectors.DefaultSelector();selector_a916db4e.register(gegevens_functie.stdout,selectors.EVENT_READ)
        def greep_gebeurtenis(초단위=.1):
            for 누름값,_ in selector_a916db4e.select(초단위):
                SECONDE_WAARDE=누름값.fileobj.read(65536)
                if SECONDE_WAARDE:LOG_RECORD.extend(SECONDE_WAARDE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(markering,actueel_functie,초단위=50):
            beëindigen_VERSCHUIVING=time.monotonic()+초단위
            while markering not in LOG_RECORD[actueel_functie:]:
                if time.monotonic()>beëindigen_VERSCHUIVING or gegevens_functie.poll() is not None:raise AssertionError(LOG_RECORD[actueel_functie:].decode('utf-8','replace'))
                greep_gebeurtenis()
            return bytes(LOG_RECORD[actueel_functie:])
        def e_mailen(SECONDE_WAARDE,markering=b'jkoros-native> '):
            actueel_functie=len(LOG_RECORD);gegevens_functie.stdin.write(SECONDE_WAARDE);gegevens_functie.stdin.flush();return 기다리기(markering,actueel_functie)
        def Shell(tekenreeks_gegevens):return e_mailen((tekenreeks_gegevens+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def alias_WAARDE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def click_knop(x_coördinaat,Y_coördinaat):return bytes([30,1,1,x_coördinaat&255,x_coördinaat>>8,Y_coördinaat&255,Y_coördinaat>>8,30,1,0,x_coördinaat&255,x_coördinaat>>8,Y_coördinaat&255,Y_coördinaat>>8])
        def opdracht_MODUS():
            gegevens_functie.stdin.write(b'\x1b');gegevens_functie.stdin.flush();beëindigen_VERSCHUIVING=time.monotonic()+.2
            while time.monotonic()<beëindigen_VERSCHUIVING:greep_gebeurtenis(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Shell('terminal');greep_gebeurtenis(.3)
            gegevens=(Taken_wortel/'build/verification/new-java/Swing_test.class').read_bytes()
            e_mailen('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(gegevens),64):e_mailen(gegevens[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            e_mailen(b'.\n')
            e_mailen('java Swing_test\n'.encode(),b'SWING READY')
            beëindigen_VERSCHUIVING=time.monotonic()+3
            while time.monotonic()<beëindigen_VERSCHUIVING:greep_gebeurtenis(.1)
            # JFrame centered at (120,100), content at y=130.
            e_mailen(click_knop(200,210),b'',)  # focus JTextField
            gegevens_functie.stdin.write('누리'.encode());gegevens_functie.stdin.flush()
            beëindigen_VERSCHUIVING=time.monotonic()+.3
            while time.monotonic()<beëindigen_VERSCHUIVING:greep_gebeurtenis(.05)
            resultaat=e_mailen(click_knop(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_RECORD)-len(resultaat))
            e_mailen(alias_WAARDE(1),b'TERMINAL FOCUS 2')
            resultaat=Shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in resultaat
            e_mailen(click_knop(180,12),b'TERMINAL FOCUS 1')
            beëindigen_VERSCHUIVING=time.monotonic()+.3
            while time.monotonic()<beëindigen_VERSCHUIVING:greep_gebeurtenis(.05)
            with socket.socket(socket.AF_UNIX) as codepoint:
                codepoint.settimeout(10);codepoint.connect(str(모의제어접속))
                with codepoint.makefile('rwb') as Bestand_invoer:
                    json.loads(Bestand_invoer.readline())
                    for aanvraag_WAARDE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(doel_WAARDE_functie/'native-swing.png'),'format':'png'}}):
                        Bestand_invoer.write((json.dumps(aanvraag_WAARDE)+'\n').encode());Bestand_invoer.flush()
                        while True:
                            반환값=json.loads(Bestand_invoer.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            e_mailen(click_knop(505,115))
            Shell('echo SWING_CLOSED_OK')
            gegevens=(les_pad/'한글창시험.class').read_bytes()
            e_mailen('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(gegevens),64):e_mailen(gegevens[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            e_mailen(b'.\n')
            e_mailen('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            e_mailen(click_knop(200,255),'KOREAN SWING CLICK Naam'.encode())
            e_mailen(click_knop(505,115))
            Shell('echo KOREAN_SWING_CLOSED_OK')
            validatie_Rapport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Nederlands Venster/knop/Actie_kennisgeving/gebeurtenis_wachtrij directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if gegevens_functie.poll() is None:gegevens_functie.terminate()
            try:gegevens_functie.wait(timeout=5)
            except subprocess.TimeoutExpired:gegevens_functie.kill();gegevens_functie.wait()
            selector_a916db4e.close();gegevens_functie.stdin.close();gegevens_functie.stdout.close();(doel_WAARDE_functie/'serial.log').write_bytes(LOG_RECORD);(doel_WAARDE_functie/'report.json').write_text(json.dumps(validatie_Rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':starten()
