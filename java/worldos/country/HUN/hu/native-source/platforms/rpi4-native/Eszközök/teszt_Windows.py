#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from végrehajt_parancs import teendő_gyök,Parancs

def Futtatás():
    cél_ÉRTÉK_pozíció=teendő_gyök/'build/verification/windows';cél_ÉRTÉK_pozíció.mkdir(parents=True,exist_ok=True)
    ellenőrzés_jelent={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest()};LOG_REKORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        adat_pozíció=subprocess.Popen(Parancs()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        szelektor_a916db4e=selectors.DefaultSelector();szelektor_a916db4e.register(adat_pozíció.stdout,selectors.EVENT_READ)
        def leíró_esemény(초단위=.1):
            for 누름값,_ in szelektor_a916db4e.select(초단위):
                MPERC_ÉRTÉK=누름값.fileobj.read(65536)
                if MPERC_ÉRTÉK:LOG_REKORD.extend(MPERC_ÉRTÉK)
            assert b'PANIC:' not in LOG_REKORD and b'HALTED' not in LOG_REKORD,LOG_REKORD[-2048:]
        def 기다리기(jelölő,aktuális_pozíció,초단위=50):
            megszüntet_Ofszet=time.monotonic()+초단위
            while jelölő not in LOG_REKORD[aktuális_pozíció:]:
                if time.monotonic()>megszüntet_Ofszet or adat_pozíció.poll() is not None:raise AssertionError(LOG_REKORD[aktuális_pozíció:].decode('utf-8','replace'))
                leíró_esemény()
            return bytes(LOG_REKORD[aktuális_pozíció:])
        def küld(MPERC_ÉRTÉK,jelölő=b'jkoros-native> '):
            aktuális_pozíció=len(LOG_REKORD);adat_pozíció.stdin.write(MPERC_ÉRTÉK);adat_pozíció.stdin.flush();return 기다리기(jelölő,aktuális_pozíció)
        def felület(sztring_adat):return küld((sztring_adat+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def hivatkozás_ÉRTÉK(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def kattint_gomb(x_koordináta,Y_koordináta):return bytes([30,1,1,x_koordináta&255,x_koordináta>>8,Y_koordináta&255,Y_koordináta>>8,30,1,0,x_koordináta&255,x_koordináta>>8,Y_koordináta&255,Y_koordináta>>8])
        def parancs_mód():
            adat_pozíció.stdin.write(b'\x1b');adat_pozíció.stdin.flush();megszüntet_Ofszet=time.monotonic()+.2
            while time.monotonic()<megszüntet_Ofszet:leíró_esemény(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            felület('terminal');leíró_esemény(.3)
            felület('mkdir first; cd first; export NAME=one')
            küld('vi 첫째.py\n'.encode(),b'NORMAL')
            küld('i값 = 21\nprint(ÉRTÉK * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            megszüntet_Ofszet=time.monotonic()+3
            while time.monotonic()<megszüntet_Ofszet:leíró_esemény(.1)
            küld(hivatkozás_ÉRTÉK(1),b'TERMINAL FOCUS 2');leíró_esemény(.2)
            assert b'/\r\n' in felület('pwd')
            felület('export NAME=two')
            küld('vi 둘째.txt\n'.encode(),b'NORMAL')
            küld('i두 번째 Ablak\n'.encode(),b'INSERT')
            küld(kattint_gomb(180,12),b'TERMINAL FOCUS 1');leíró_esemény(.2)
            parancs_mód();küld(b':wq\r')
            assert b'one:/first' in felület('echo "$NAME:$PWD"')
            assert 'ÉRTÉK = 21\r\nprint(ÉRTÉK * 2)'.encode() in felület('cat 첫째.py')
            KR=felület('python 첫째.py');assert b'42\r\n' in KR,KR
            # Close the first shell with its actual title-bar X; second editor resumes.
            küld(kattint_gomb(560,63),b'TERMINAL FOCUS 2');leíró_esemény(.2)
            parancs_mód();küld(b':wq\r')
            assert b'two:/' in felület('echo "$NAME:$PWD"')
            assert '두 번째 Ablak'.encode() in felület('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            küld('vi 둘째.txt\n'.encode(),b'NORMAL');küld(b'xu',b'NORMAL')
            küld(b'iX',b'INSERT');parancs_mód();küld(b':q\r',b'Unsaved')
            küld(b':q!\r');assert '두 번째 Ablak'.encode() in felület('cat 둘째.txt')
            küld(hivatkozás_ÉRTÉK(1),b'TERMINAL FOCUS 1');leíró_esemény(.2)
            küld(hivatkozás_ÉRTÉK(1),b'TERMINAL FOCUS 3');leíró_esemény(.2)
            küld(hivatkozás_ÉRTÉK(1),b'TERMINAL FOCUS 4');leíró_esemény(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            adat_pozíció.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));adat_pozíció.stdin.flush()
            felület('echo DRAGGED_OK')
            küld('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            küld('i저장하지 않은 adat'.encode(),b'INSERT')
            küld(kattint_gomb(578,97),b'TERMINAL FOCUS 3');leíró_esemény(.2)
            assert '버릴문서.txt'.encode() not in felület('ls')
            küld(hivatkozás_ÉRTÉK(1),b'TERMINAL FOCUS 4');leíró_esemény(.2)
            felület('echo REUSED_WINDOW_OK')
            Kész_összeg=LOG_REKORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Kész_összeg)
            # UART completion precedes the next QEMU display refresh.
            megszüntet_Ofszet=time.monotonic()+.3
            while time.monotonic()<megszüntet_Ofszet:leíró_esemény(.05)
            with socket.socket(socket.AF_UNIX) as kódpont:
                kódpont.settimeout(10);kódpont.connect(str(모의제어접속))
                with kódpont.makefile('rwb') as Fájl_bejegyzés:
                    json.loads(Fájl_bejegyzés.readline())
                    for kérés_ÉRTÉK in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cél_ÉRTÉK_pozíció/'four-terminals.png'),'format':'png'}}):
                        Fájl_bejegyzés.write((json.dumps(kérés_ÉRTÉK)+'\n').encode());Fájl_bejegyzés.flush()
                        while True:
                            반환값=json.loads(Fájl_bejegyzés.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(cél_ÉRTÉK_pozíció/'four-terminals.png')).convert('RGB')
            for koordinátapár,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinátapár)==색상,(koordinátapár,화소들.getpixel(koordinátapár))
            felület('echo FOUR_WINDOWS_OK')
            ellenőrzés_jelent.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if adat_pozíció.poll() is None:adat_pozíció.terminate()
            try:adat_pozíció.wait(timeout=5)
            except subprocess.TimeoutExpired:adat_pozíció.kill();adat_pozíció.wait()
            szelektor_a916db4e.close();adat_pozíció.stdin.close();adat_pozíció.stdout.close();(cél_ÉRTÉK_pozíció/'serial.log').write_bytes(LOG_REKORD);(cél_ÉRTÉK_pozíció/'report.json').write_text(json.dumps(ellenőrzés_jelent,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Futtatás()
