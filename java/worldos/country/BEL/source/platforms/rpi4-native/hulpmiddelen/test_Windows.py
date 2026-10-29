#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Uitvoeren_opdracht import Taken_wortel,opdracht

def starten():
    doel_WAARDE_functie=Taken_wortel/'build/verification/windows';doel_WAARDE_functie.mkdir(parents=True,exist_ok=True)
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
            Shell('mkdir first; cd first; export NAME=one')
            e_mailen('vi 첫째.py\n'.encode(),b'NORMAL')
            e_mailen('i값 = 21\nprint(WAARDE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            beëindigen_VERSCHUIVING=time.monotonic()+3
            while time.monotonic()<beëindigen_VERSCHUIVING:greep_gebeurtenis(.1)
            e_mailen(alias_WAARDE(1),b'TERMINAL FOCUS 2');greep_gebeurtenis(.2)
            assert b'/\r\n' in Shell('pwd')
            Shell('export NAME=two')
            e_mailen('vi 둘째.txt\n'.encode(),b'NORMAL')
            e_mailen('i두 번째 Venster\n'.encode(),b'INSERT')
            e_mailen(click_knop(180,12),b'TERMINAL FOCUS 1');greep_gebeurtenis(.2)
            opdracht_MODUS();e_mailen(b':wq\r')
            assert b'one:/first' in Shell('echo "$NAME:$PWD"')
            assert 'WAARDE = 21\r\nprint(WAARDE * 2)'.encode() in Shell('cat 첫째.py')
            resultaat=Shell('python 첫째.py');assert b'42\r\n' in resultaat,resultaat
            # Close the first shell with its actual title-bar X; second editor resumes.
            e_mailen(click_knop(560,63),b'TERMINAL FOCUS 2');greep_gebeurtenis(.2)
            opdracht_MODUS();e_mailen(b':wq\r')
            assert b'two:/' in Shell('echo "$NAME:$PWD"')
            assert '두 번째 Venster'.encode() in Shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            e_mailen('vi 둘째.txt\n'.encode(),b'NORMAL');e_mailen(b'xu',b'NORMAL')
            e_mailen(b'iX',b'INSERT');opdracht_MODUS();e_mailen(b':q\r',b'Unsaved')
            e_mailen(b':q!\r');assert '두 번째 Venster'.encode() in Shell('cat 둘째.txt')
            e_mailen(alias_WAARDE(1),b'TERMINAL FOCUS 1');greep_gebeurtenis(.2)
            e_mailen(alias_WAARDE(1),b'TERMINAL FOCUS 3');greep_gebeurtenis(.2)
            e_mailen(alias_WAARDE(1),b'TERMINAL FOCUS 4');greep_gebeurtenis(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            gegevens_functie.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));gegevens_functie.stdin.flush()
            Shell('echo DRAGGED_OK')
            e_mailen('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            e_mailen('i저장하지 않은 gegevens'.encode(),b'INSERT')
            e_mailen(click_knop(578,97),b'TERMINAL FOCUS 3');greep_gebeurtenis(.2)
            assert '버릴문서.txt'.encode() not in Shell('ls')
            e_mailen(alias_WAARDE(1),b'TERMINAL FOCUS 4');greep_gebeurtenis(.2)
            Shell('echo REUSED_WINDOW_OK')
            Voltooid_aantal=LOG_RECORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Voltooid_aantal)
            # UART completion precedes the next QEMU display refresh.
            beëindigen_VERSCHUIVING=time.monotonic()+.3
            while time.monotonic()<beëindigen_VERSCHUIVING:greep_gebeurtenis(.05)
            with socket.socket(socket.AF_UNIX) as codepoint:
                codepoint.settimeout(10);codepoint.connect(str(모의제어접속))
                with codepoint.makefile('rwb') as Bestand_invoer:
                    json.loads(Bestand_invoer.readline())
                    for aanvraag_WAARDE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(doel_WAARDE_functie/'four-terminals.png'),'format':'png'}}):
                        Bestand_invoer.write((json.dumps(aanvraag_WAARDE)+'\n').encode());Bestand_invoer.flush()
                        while True:
                            반환값=json.loads(Bestand_invoer.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(doel_WAARDE_functie/'four-terminals.png')).convert('RGB')
            for coördinatenpaar,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(coördinatenpaar)==색상,(coördinatenpaar,화소들.getpixel(coördinatenpaar))
            Shell('echo FOUR_WINDOWS_OK')
            validatie_Rapport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if gegevens_functie.poll() is None:gegevens_functie.terminate()
            try:gegevens_functie.wait(timeout=5)
            except subprocess.TimeoutExpired:gegevens_functie.kill();gegevens_functie.wait()
            selector_a916db4e.close();gegevens_functie.stdin.close();gegevens_functie.stdout.close();(doel_WAARDE_functie/'serial.log').write_bytes(LOG_RECORD);(doel_WAARDE_functie/'report.json').write_text(json.dumps(validatie_Rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':starten()
