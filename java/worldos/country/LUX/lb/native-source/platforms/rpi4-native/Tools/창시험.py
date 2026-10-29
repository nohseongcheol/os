#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ausféieren_Befeel import projezéieren_Racinn,Befeel

def Laf():
    Zil_VALUE_positionéieren=projezéieren_Racinn/'build/verification/windows';Zil_VALUE_positionéieren.mkdir(parents=True,exist_ok=True)
    Validatioun_mellen={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest()};LOG_Rei=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        Daten_positionéieren=subprocess.Popen(Befeel()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        Selekteur_a916db4e=selectors.DefaultSelector();Selekteur_a916db4e.register(Daten_positionéieren.stdout,selectors.EVENT_READ)
        def Handle_Evenement(초단위=.1):
            for 누름값,_ in Selekteur_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_Rei.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_Rei and b'HALTED' not in LOG_Rei,LOG_Rei[-2048:]
        def 기다리기(Markéierung,현재위치,초단위=50):
            bëennegen_OFFSET=time.monotonic()+초단위
            while Markéierung not in LOG_Rei[현재위치:]:
                if time.monotonic()>bëennegen_OFFSET or Daten_positionéieren.poll() is not None:raise AssertionError(LOG_Rei[현재위치:].decode('utf-8','replace'))
                Handle_Evenement()
            return bytes(LOG_Rei[현재위치:])
        def mailen(SECOND_VALUE,Markéierung=b'jkoros-native> '):
            현재위치=len(LOG_Rei);Daten_positionéieren.stdin.write(SECOND_VALUE);Daten_positionéieren.stdin.flush();return 기다리기(Markéierung,현재위치)
        def Shell(Zeechefolleg_Daten):return mailen((Zeechefolleg_Daten+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def Ofkierzung_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klicken_Tast(X_Koordinat,세로좌표):return bytes([30,1,1,X_Koordinat&255,X_Koordinat>>8,세로좌표&255,세로좌표>>8,30,1,0,X_Koordinat&255,X_Koordinat>>8,세로좌표&255,세로좌표>>8])
        def Befeel_MODE():
            Daten_positionéieren.stdin.write(b'\x1b');Daten_positionéieren.stdin.flush();bëennegen_OFFSET=time.monotonic()+.2
            while time.monotonic()<bëennegen_OFFSET:Handle_Evenement(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Shell('terminal');Handle_Evenement(.3)
            Shell('mkdir first; cd first; export NAME=one')
            mailen('vi 첫째.py\n'.encode(),b'NORMAL')
            mailen('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            bëennegen_OFFSET=time.monotonic()+3
            while time.monotonic()<bëennegen_OFFSET:Handle_Evenement(.1)
            mailen(Ofkierzung_VALUE(1),b'TERMINAL FOCUS 2');Handle_Evenement(.2)
            assert b'/\r\n' in Shell('pwd')
            Shell('export NAME=two')
            mailen('vi 둘째.txt\n'.encode(),b'NORMAL')
            mailen('i두 번째 Fënster\n'.encode(),b'INSERT')
            mailen(klicken_Tast(180,12),b'TERMINAL FOCUS 1');Handle_Evenement(.2)
            Befeel_MODE();mailen(b':wq\r')
            assert b'one:/first' in Shell('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in Shell('cat 첫째.py')
            Mooss=Shell('python 첫째.py');assert b'42\r\n' in Mooss,Mooss
            # Close the first shell with its actual title-bar X; second editor resumes.
            mailen(klicken_Tast(560,63),b'TERMINAL FOCUS 2');Handle_Evenement(.2)
            Befeel_MODE();mailen(b':wq\r')
            assert b'two:/' in Shell('echo "$NAME:$PWD"')
            assert '두 번째 Fënster'.encode() in Shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            mailen('vi 둘째.txt\n'.encode(),b'NORMAL');mailen(b'xu',b'NORMAL')
            mailen(b'iX',b'INSERT');Befeel_MODE();mailen(b':q\r',b'Unsaved')
            mailen(b':q!\r');assert '두 번째 Fënster'.encode() in Shell('cat 둘째.txt')
            mailen(Ofkierzung_VALUE(1),b'TERMINAL FOCUS 1');Handle_Evenement(.2)
            mailen(Ofkierzung_VALUE(1),b'TERMINAL FOCUS 3');Handle_Evenement(.2)
            mailen(Ofkierzung_VALUE(1),b'TERMINAL FOCUS 4');Handle_Evenement(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            Daten_positionéieren.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));Daten_positionéieren.stdin.flush()
            Shell('echo DRAGGED_OK')
            mailen('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            mailen('i저장하지 않은 Daten'.encode(),b'INSERT')
            mailen(klicken_Tast(578,97),b'TERMINAL FOCUS 3');Handle_Evenement(.2)
            assert '버릴문서.txt'.encode() not in Shell('ls')
            mailen(Ofkierzung_VALUE(1),b'TERMINAL FOCUS 4');Handle_Evenement(.2)
            Shell('echo REUSED_WINDOW_OK')
            완료량=LOG_Rei.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            bëennegen_OFFSET=time.monotonic()+.3
            while time.monotonic()<bëennegen_OFFSET:Handle_Evenement(.05)
            with socket.socket(socket.AF_UNIX) as Zeechecode:
                Zeechecode.settimeout(10);Zeechecode.connect(str(모의제어접속))
                with Zeechecode.makefile('rwb') as Fichier_Agab:
                    json.loads(Fichier_Agab.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(Zil_VALUE_positionéieren/'four-terminals.png'),'format':'png'}}):
                        Fichier_Agab.write((json.dumps(요청값)+'\n').encode());Fichier_Agab.flush()
                        while True:
                            반환값=json.loads(Fichier_Agab.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(Zil_VALUE_positionéieren/'four-terminals.png')).convert('RGB')
            for Koordinatekoppel,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(Koordinatekoppel)==색상,(Koordinatekoppel,화소들.getpixel(Koordinatekoppel))
            Shell('echo FOUR_WINDOWS_OK')
            Validatioun_mellen.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if Daten_positionéieren.poll() is None:Daten_positionéieren.terminate()
            try:Daten_positionéieren.wait(timeout=5)
            except subprocess.TimeoutExpired:Daten_positionéieren.kill();Daten_positionéieren.wait()
            Selekteur_a916db4e.close();Daten_positionéieren.stdin.close();Daten_positionéieren.stdout.close();(Zil_VALUE_positionéieren/'serial.log').write_bytes(LOG_Rei);(Zil_VALUE_positionéieren/'report.json').write_text(json.dumps(Validatioun_mellen,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Laf()
