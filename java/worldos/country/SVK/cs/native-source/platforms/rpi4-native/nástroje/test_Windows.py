#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Provést_příkaz import akce_kořen,příkaz

def Spustit_2():
    cíl_HODNOTA_pozice=akce_kořen/'build/verification/windows';cíl_HODNOTA_pozice.mkdir(parents=True,exist_ok=True)
    ověření_Zpráva={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest()};LOGZ_ZÁZNAM=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_pozice=subprocess.Popen(příkaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selektor_a916db4e=selectors.DefaultSelector();selektor_a916db4e.register(data_pozice.stdout,selectors.EVENT_READ)
        def úchyt_událost(초단위=.1):
            for 누름값,_ in selektor_a916db4e.select(초단위):
                SEKUNDA_HODNOTA=누름값.fileobj.read(65536)
                if SEKUNDA_HODNOTA:LOGZ_ZÁZNAM.extend(SEKUNDA_HODNOTA)
            assert b'PANIC:' not in LOGZ_ZÁZNAM and b'HALTED' not in LOGZ_ZÁZNAM,LOGZ_ZÁZNAM[-2048:]
        def 기다리기(značka,dobrá_pozice,초단위=50):
            konec_POSUN=time.monotonic()+초단위
            while značka not in LOGZ_ZÁZNAM[dobrá_pozice:]:
                if time.monotonic()>konec_POSUN or data_pozice.poll() is not None:raise AssertionError(LOGZ_ZÁZNAM[dobrá_pozice:].decode('utf-8','replace'))
                úchyt_událost()
            return bytes(LOGZ_ZÁZNAM[dobrá_pozice:])
        def poslat(SEKUNDA_HODNOTA,značka=b'jkoros-native> '):
            dobrá_pozice=len(LOGZ_ZÁZNAM);data_pozice.stdin.write(SEKUNDA_HODNOTA);data_pozice.stdin.flush();return 기다리기(značka,dobrá_pozice)
        def prostředí(řetězec_data):return poslat((řetězec_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def zkratka_HODNOTA(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klepnout_tlačítko(souřadnice_x,Y_souřadnice):return bytes([30,1,1,souřadnice_x&255,souřadnice_x>>8,Y_souřadnice&255,Y_souřadnice>>8,30,1,0,souřadnice_x&255,souřadnice_x>>8,Y_souřadnice&255,Y_souřadnice>>8])
        def příkaz_MODE():
            data_pozice.stdin.write(b'\x1b');data_pozice.stdin.flush();konec_POSUN=time.monotonic()+.2
            while time.monotonic()<konec_POSUN:úchyt_událost(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            prostředí('terminal');úchyt_událost(.3)
            prostředí('mkdir first; cd first; export NAME=one')
            poslat('vi 첫째.py\n'.encode(),b'NORMAL')
            poslat('i값 = 21\nprint(HODNOTA * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            konec_POSUN=time.monotonic()+3
            while time.monotonic()<konec_POSUN:úchyt_událost(.1)
            poslat(zkratka_HODNOTA(1),b'TERMINAL FOCUS 2');úchyt_událost(.2)
            assert b'/\r\n' in prostředí('pwd')
            prostředí('export NAME=two')
            poslat('vi 둘째.txt\n'.encode(),b'NORMAL')
            poslat('i두 번째 Okno\n'.encode(),b'INSERT')
            poslat(klepnout_tlačítko(180,12),b'TERMINAL FOCUS 1');úchyt_událost(.2)
            příkaz_MODE();poslat(b':wq\r')
            assert b'one:/first' in prostředí('echo "$NAME:$PWD"')
            assert 'HODNOTA = 21\r\nprint(HODNOTA * 2)'.encode() in prostředí('cat 첫째.py')
            VÝSLEDEK=prostředí('python 첫째.py');assert b'42\r\n' in VÝSLEDEK,VÝSLEDEK
            # Close the first shell with its actual title-bar X; second editor resumes.
            poslat(klepnout_tlačítko(560,63),b'TERMINAL FOCUS 2');úchyt_událost(.2)
            příkaz_MODE();poslat(b':wq\r')
            assert b'two:/' in prostředí('echo "$NAME:$PWD"')
            assert '두 번째 Okno'.encode() in prostředí('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            poslat('vi 둘째.txt\n'.encode(),b'NORMAL');poslat(b'xu',b'NORMAL')
            poslat(b'iX',b'INSERT');příkaz_MODE();poslat(b':q\r',b'Unsaved')
            poslat(b':q!\r');assert '두 번째 Okno'.encode() in prostředí('cat 둘째.txt')
            poslat(zkratka_HODNOTA(1),b'TERMINAL FOCUS 1');úchyt_událost(.2)
            poslat(zkratka_HODNOTA(1),b'TERMINAL FOCUS 3');úchyt_událost(.2)
            poslat(zkratka_HODNOTA(1),b'TERMINAL FOCUS 4');úchyt_událost(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_pozice.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_pozice.stdin.flush()
            prostředí('echo DRAGGED_OK')
            poslat('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            poslat('i저장하지 않은 data'.encode(),b'INSERT')
            poslat(klepnout_tlačítko(578,97),b'TERMINAL FOCUS 3');úchyt_událost(.2)
            assert '버릴문서.txt'.encode() not in prostředí('ls')
            poslat(zkratka_HODNOTA(1),b'TERMINAL FOCUS 4');úchyt_událost(.2)
            prostředí('echo REUSED_WINDOW_OK')
            dokončeno_částka=LOGZ_ZÁZNAM.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',dokončeno_částka)
            # UART completion precedes the next QEMU display refresh.
            konec_POSUN=time.monotonic()+.3
            while time.monotonic()<konec_POSUN:úchyt_událost(.05)
            with socket.socket(socket.AF_UNIX) as bod_kódu:
                bod_kódu.settimeout(10);bod_kódu.connect(str(모의제어접속))
                with bod_kódu.makefile('rwb') as Soubor_položka:
                    json.loads(Soubor_položka.readline())
                    for žádost_HODNOTA in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cíl_HODNOTA_pozice/'four-terminals.png'),'format':'png'}}):
                        Soubor_položka.write((json.dumps(žádost_HODNOTA)+'\n').encode());Soubor_položka.flush()
                        while True:
                            반환값=json.loads(Soubor_položka.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(cíl_HODNOTA_pozice/'four-terminals.png')).convert('RGB')
            for souřadnice,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(souřadnice)==색상,(souřadnice,화소들.getpixel(souřadnice))
            prostředí('echo FOUR_WINDOWS_OK')
            ověření_Zpráva.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_pozice.poll() is None:data_pozice.terminate()
            try:data_pozice.wait(timeout=5)
            except subprocess.TimeoutExpired:data_pozice.kill();data_pozice.wait()
            selektor_a916db4e.close();data_pozice.stdin.close();data_pozice.stdout.close();(cíl_HODNOTA_pozice/'serial.log').write_bytes(LOGZ_ZÁZNAM);(cíl_HODNOTA_pozice/'report.json').write_text(json.dumps(ověření_Zpráva,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Spustit_2()
