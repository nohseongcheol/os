#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izvrši_komanda import radnja_koren,komanda

def koristiti():
    odredište_VALUE_pozicija=radnja_koren/'build/verification/windows';odredište_VALUE_pozicija.mkdir(parents=True,exist_ok=True)
    provera_valjanosti_izveštaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest()};LOG_snimi=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        podaci_pozicija=subprocess.Popen(komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        birač_a916db4e=selectors.DefaultSelector();birač_a916db4e.register(podaci_pozicija.stdout,selectors.EVENT_READ)
        def pokazivač_događaj(초단위=.1):
            for 누름값,_ in birač_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_snimi.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_snimi and b'HALTED' not in LOG_snimi,LOG_snimi[-2048:]
        def 기다리기(označivač,aktuelno_pozicija,초단위=50):
            završiti_razgovor_Pomak=time.monotonic()+초단위
            while označivač not in LOG_snimi[aktuelno_pozicija:]:
                if time.monotonic()>završiti_razgovor_Pomak or podaci_pozicija.poll() is not None:raise AssertionError(LOG_snimi[aktuelno_pozicija:].decode('utf-8','replace'))
                pokazivač_događaj()
            return bytes(LOG_snimi[aktuelno_pozicija:])
        def poslati(SECOND_VALUE,označivač=b'jkoros-native> '):
            aktuelno_pozicija=len(LOG_snimi);podaci_pozicija.stdin.write(SECOND_VALUE);podaci_pozicija.stdin.flush();return 기다리기(označivač,aktuelno_pozicija)
        def ljuska(niska_podaci):return poslati((niska_podaci+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def prečica_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_taster(x_koordinata,세로좌표):return bytes([30,1,1,x_koordinata&255,x_koordinata>>8,세로좌표&255,세로좌표>>8,30,1,0,x_koordinata&255,x_koordinata>>8,세로좌표&255,세로좌표>>8])
        def komanda_MODE():
            podaci_pozicija.stdin.write(b'\x1b');podaci_pozicija.stdin.flush();završiti_razgovor_Pomak=time.monotonic()+.2
            while time.monotonic()<završiti_razgovor_Pomak:pokazivač_događaj(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ljuska('terminal');pokazivač_događaj(.3)
            ljuska('mkdir first; cd first; export NAME=one')
            poslati('vi 첫째.py\n'.encode(),b'NORMAL')
            poslati('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            završiti_razgovor_Pomak=time.monotonic()+3
            while time.monotonic()<završiti_razgovor_Pomak:pokazivač_događaj(.1)
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 2');pokazivač_događaj(.2)
            assert b'/\r\n' in ljuska('pwd')
            ljuska('export NAME=two')
            poslati('vi 둘째.txt\n'.encode(),b'NORMAL')
            poslati('i두 번째 prozor\n'.encode(),b'INSERT')
            poslati(klik_taster(180,12),b'TERMINAL FOCUS 1');pokazivač_događaj(.2)
            komanda_MODE();poslati(b':wq\r')
            assert b'one:/first' in ljuska('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in ljuska('cat 첫째.py')
            KR=ljuska('python 첫째.py');assert b'42\r\n' in KR,KR
            # Close the first shell with its actual title-bar X; second editor resumes.
            poslati(klik_taster(560,63),b'TERMINAL FOCUS 2');pokazivač_događaj(.2)
            komanda_MODE();poslati(b':wq\r')
            assert b'two:/' in ljuska('echo "$NAME:$PWD"')
            assert '두 번째 prozor'.encode() in ljuska('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            poslati('vi 둘째.txt\n'.encode(),b'NORMAL');poslati(b'xu',b'NORMAL')
            poslati(b'iX',b'INSERT');komanda_MODE();poslati(b':q\r',b'Unsaved')
            poslati(b':q!\r');assert '두 번째 prozor'.encode() in ljuska('cat 둘째.txt')
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 1');pokazivač_događaj(.2)
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 3');pokazivač_događaj(.2)
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 4');pokazivač_događaj(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            podaci_pozicija.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));podaci_pozicija.stdin.flush()
            ljuska('echo DRAGGED_OK')
            poslati('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            poslati('i저장하지 않은 podaci'.encode(),b'INSERT')
            poslati(klik_taster(578,97),b'TERMINAL FOCUS 3');pokazivač_događaj(.2)
            assert '버릴문서.txt'.encode() not in ljuska('ls')
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 4');pokazivač_događaj(.2)
            ljuska('echo REUSED_WINDOW_OK')
            Dovršeno_iznos=LOG_snimi.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Dovršeno_iznos)
            # UART completion precedes the next QEMU display refresh.
            završiti_razgovor_Pomak=time.monotonic()+.3
            while time.monotonic()<završiti_razgovor_Pomak:pokazivač_događaj(.05)
            with socket.socket(socket.AF_UNIX) as kôd_znaka:
                kôd_znaka.settimeout(10);kôd_znaka.connect(str(모의제어접속))
                with kôd_znaka.makefile('rwb') as Datoteka_stavka:
                    json.loads(Datoteka_stavka.readline())
                    for zahtev_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(odredište_VALUE_pozicija/'four-terminals.png'),'format':'png'}}):
                        Datoteka_stavka.write((json.dumps(zahtev_VALUE_625fa62c)+'\n').encode());Datoteka_stavka.flush()
                        while True:
                            반환값=json.loads(Datoteka_stavka.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(odredište_VALUE_pozicija/'four-terminals.png')).convert('RGB')
            for koordinatni_par,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinatni_par)==색상,(koordinatni_par,화소들.getpixel(koordinatni_par))
            ljuska('echo FOUR_WINDOWS_OK')
            provera_valjanosti_izveštaj.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if podaci_pozicija.poll() is None:podaci_pozicija.terminate()
            try:podaci_pozicija.wait(timeout=5)
            except subprocess.TimeoutExpired:podaci_pozicija.kill();podaci_pozicija.wait()
            birač_a916db4e.close();podaci_pozicija.stdin.close();podaci_pozicija.stdout.close();(odredište_VALUE_pozicija/'serial.log').write_bytes(LOG_snimi);(odredište_VALUE_pozicija/'report.json').write_text(json.dumps(provera_valjanosti_izveštaj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':koristiti()
