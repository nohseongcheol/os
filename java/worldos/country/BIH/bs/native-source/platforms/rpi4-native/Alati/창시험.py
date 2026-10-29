#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izvrši_komanda import projicirati_koijen,Naredba

def Pokreni():
    odredište_VALUE_položaj=projicirati_koijen/'build/verification/windows';odredište_VALUE_položaj.mkdir(parents=True,exist_ok=True)
    provjera_izvještaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest()};LOG_red=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        podaci_položaj=subprocess.Popen(Naredba()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        birač_a916db4e=selectors.DefaultSelector();birač_a916db4e.register(podaci_položaj.stdout,selectors.EVENT_READ)
        def hvatište_događaj(초단위=.1):
            for 누름값,_ in birač_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_red.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_red and b'HALTED' not in LOG_red,LOG_red[-2048:]
        def 기다리기(확인표시,trenutno_položaj,초단위=50):
            završiti_Pomak=time.monotonic()+초단위
            while 확인표시 not in LOG_red[trenutno_položaj:]:
                if time.monotonic()>završiti_Pomak or podaci_položaj.poll() is not None:raise AssertionError(LOG_red[trenutno_položaj:].decode('utf-8','replace'))
                hvatište_događaj()
            return bytes(LOG_red[trenutno_položaj:])
        def poslati(SECOND_VALUE,확인표시=b'jkoros-native> '):
            trenutno_položaj=len(LOG_red);podaci_položaj.stdin.write(SECOND_VALUE);podaci_položaj.stdin.flush();return 기다리기(확인표시,trenutno_položaj)
        def ljuska(string_podaci):return poslati((string_podaci+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def prečica_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_dugme(koordinata_x,Y_koordinata):return bytes([30,1,1,koordinata_x&255,koordinata_x>>8,Y_koordinata&255,Y_koordinata>>8,30,1,0,koordinata_x&255,koordinata_x>>8,Y_koordinata&255,Y_koordinata>>8])
        def komanda_mod():
            podaci_položaj.stdin.write(b'\x1b');podaci_položaj.stdin.flush();završiti_Pomak=time.monotonic()+.2
            while time.monotonic()<završiti_Pomak:hvatište_događaj(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ljuska('terminal');hvatište_događaj(.3)
            ljuska('mkdir first; cd first; export NAME=one')
            poslati('vi 첫째.py\n'.encode(),b'NORMAL')
            poslati('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            završiti_Pomak=time.monotonic()+3
            while time.monotonic()<završiti_Pomak:hvatište_događaj(.1)
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 2');hvatište_događaj(.2)
            assert b'/\r\n' in ljuska('pwd')
            ljuska('export NAME=two')
            poslati('vi 둘째.txt\n'.encode(),b'NORMAL')
            poslati('i두 번째 prozor\n'.encode(),b'INSERT')
            poslati(klik_dugme(180,12),b'TERMINAL FOCUS 1');hvatište_događaj(.2)
            komanda_mod();poslati(b':wq\r')
            assert b'one:/first' in ljuska('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in ljuska('cat 첫째.py')
            mjera=ljuska('python 첫째.py');assert b'42\r\n' in mjera,mjera
            # Close the first shell with its actual title-bar X; second editor resumes.
            poslati(klik_dugme(560,63),b'TERMINAL FOCUS 2');hvatište_događaj(.2)
            komanda_mod();poslati(b':wq\r')
            assert b'two:/' in ljuska('echo "$NAME:$PWD"')
            assert '두 번째 prozor'.encode() in ljuska('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            poslati('vi 둘째.txt\n'.encode(),b'NORMAL');poslati(b'xu',b'NORMAL')
            poslati(b'iX',b'INSERT');komanda_mod();poslati(b':q\r',b'Unsaved')
            poslati(b':q!\r');assert '두 번째 prozor'.encode() in ljuska('cat 둘째.txt')
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 1');hvatište_događaj(.2)
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 3');hvatište_događaj(.2)
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 4');hvatište_događaj(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            podaci_položaj.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));podaci_položaj.stdin.flush()
            ljuska('echo DRAGGED_OK')
            poslati('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            poslati('i저장하지 않은 podaci'.encode(),b'INSERT')
            poslati(klik_dugme(578,97),b'TERMINAL FOCUS 3');hvatište_događaj(.2)
            assert '버릴문서.txt'.encode() not in ljuska('ls')
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 4');hvatište_događaj(.2)
            ljuska('echo REUSED_WINDOW_OK')
            완료량=LOG_red.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            završiti_Pomak=time.monotonic()+.3
            while time.monotonic()<završiti_Pomak:hvatište_događaj(.05)
            with socket.socket(socket.AF_UNIX) as kôd_znaka:
                kôd_znaka.settimeout(10);kôd_znaka.connect(str(모의제어접속))
                with kôd_znaka.makefile('rwb') as fajl_unos:
                    json.loads(fajl_unos.readline())
                    for HTTP_zahtjev_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(odredište_VALUE_položaj/'four-terminals.png'),'format':'png'}}):
                        fajl_unos.write((json.dumps(HTTP_zahtjev_VALUE)+'\n').encode());fajl_unos.flush()
                        while True:
                            반환값=json.loads(fajl_unos.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(odredište_VALUE_položaj/'four-terminals.png')).convert('RGB')
            for par_koordinata,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(par_koordinata)==색상,(par_koordinata,화소들.getpixel(par_koordinata))
            ljuska('echo FOUR_WINDOWS_OK')
            provjera_izvještaj.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if podaci_položaj.poll() is None:podaci_položaj.terminate()
            try:podaci_položaj.wait(timeout=5)
            except subprocess.TimeoutExpired:podaci_položaj.kill();podaci_položaj.wait()
            birač_a916db4e.close();podaci_položaj.stdin.close();podaci_položaj.stdout.close();(odredište_VALUE_položaj/'serial.log').write_bytes(LOG_red);(odredište_VALUE_položaj/'report.json').write_text(json.dumps(provjera_izvještaj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pokreni()
