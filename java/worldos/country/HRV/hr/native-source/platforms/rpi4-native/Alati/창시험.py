#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izvrši_naredba import akcija_korijen,Naredba

def Pokreni():
    odredište_VALUE_položaj=akcija_korijen/'build/verification/windows';odredište_VALUE_položaj.mkdir(parents=True,exist_ok=True)
    provjera_izvješće={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest()};LOG_zapis=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        podaci_položaj=subprocess.Popen(Naredba()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        odabirač_a916db4e=selectors.DefaultSelector();odabirač_a916db4e.register(podaci_položaj.stdout,selectors.EVENT_READ)
        def ustroj_događaj(초단위=.1):
            for 누름값,_ in odabirač_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_zapis.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_zapis and b'HALTED' not in LOG_zapis,LOG_zapis[-2048:]
        def 기다리기(marker,redovno_položaj,초단위=50):
            završiti_razgovor_pomak=time.monotonic()+초단위
            while marker not in LOG_zapis[redovno_položaj:]:
                if time.monotonic()>završiti_razgovor_pomak or podaci_položaj.poll() is not None:raise AssertionError(LOG_zapis[redovno_položaj:].decode('utf-8','replace'))
                ustroj_događaj()
            return bytes(LOG_zapis[redovno_položaj:])
        def slati(SECOND_VALUE,marker=b'jkoros-native> '):
            redovno_položaj=len(LOG_zapis);podaci_položaj.stdin.write(SECOND_VALUE);podaci_položaj.stdin.flush();return 기다리기(marker,redovno_položaj)
        def ljuska(niz_podaci):return slati((niz_podaci+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def prečac_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_tipka(koordinata_x,세로좌표):return bytes([30,1,1,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8,30,1,0,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8])
        def naredba_MODE():
            podaci_položaj.stdin.write(b'\x1b');podaci_položaj.stdin.flush();završiti_razgovor_pomak=time.monotonic()+.2
            while time.monotonic()<završiti_razgovor_pomak:ustroj_događaj(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ljuska('terminal');ustroj_događaj(.3)
            ljuska('mkdir first; cd first; export NAME=one')
            slati('vi 첫째.py\n'.encode(),b'NORMAL')
            slati('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            završiti_razgovor_pomak=time.monotonic()+3
            while time.monotonic()<završiti_razgovor_pomak:ustroj_događaj(.1)
            slati(prečac_VALUE(1),b'TERMINAL FOCUS 2');ustroj_događaj(.2)
            assert b'/\r\n' in ljuska('pwd')
            ljuska('export NAME=two')
            slati('vi 둘째.txt\n'.encode(),b'NORMAL')
            slati('i두 번째 Prozor\n'.encode(),b'INSERT')
            slati(klik_tipka(180,12),b'TERMINAL FOCUS 1');ustroj_događaj(.2)
            naredba_MODE();slati(b':wq\r')
            assert b'one:/first' in ljuska('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in ljuska('cat 첫째.py')
            REZULTAT=ljuska('python 첫째.py');assert b'42\r\n' in REZULTAT,REZULTAT
            # Close the first shell with its actual title-bar X; second editor resumes.
            slati(klik_tipka(560,63),b'TERMINAL FOCUS 2');ustroj_događaj(.2)
            naredba_MODE();slati(b':wq\r')
            assert b'two:/' in ljuska('echo "$NAME:$PWD"')
            assert '두 번째 Prozor'.encode() in ljuska('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            slati('vi 둘째.txt\n'.encode(),b'NORMAL');slati(b'xu',b'NORMAL')
            slati(b'iX',b'INSERT');naredba_MODE();slati(b':q\r',b'Unsaved')
            slati(b':q!\r');assert '두 번째 Prozor'.encode() in ljuska('cat 둘째.txt')
            slati(prečac_VALUE(1),b'TERMINAL FOCUS 1');ustroj_događaj(.2)
            slati(prečac_VALUE(1),b'TERMINAL FOCUS 3');ustroj_događaj(.2)
            slati(prečac_VALUE(1),b'TERMINAL FOCUS 4');ustroj_događaj(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            podaci_položaj.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));podaci_položaj.stdin.flush()
            ljuska('echo DRAGGED_OK')
            slati('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            slati('i저장하지 않은 podaci'.encode(),b'INSERT')
            slati(klik_tipka(578,97),b'TERMINAL FOCUS 3');ustroj_događaj(.2)
            assert '버릴문서.txt'.encode() not in ljuska('ls')
            slati(prečac_VALUE(1),b'TERMINAL FOCUS 4');ustroj_događaj(.2)
            ljuska('echo REUSED_WINDOW_OK')
            Dovršeno_iznos=LOG_zapis.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Dovršeno_iznos)
            # UART completion precedes the next QEMU display refresh.
            završiti_razgovor_pomak=time.monotonic()+.3
            while time.monotonic()<završiti_razgovor_pomak:ustroj_događaj(.05)
            with socket.socket(socket.AF_UNIX) as kodna_točka:
                kodna_točka.settimeout(10);kodna_točka.connect(str(모의제어접속))
                with kodna_točka.makefile('rwb') as Datoteka_unos:
                    json.loads(Datoteka_unos.readline())
                    for zahtjev_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(odredište_VALUE_položaj/'four-terminals.png'),'format':'png'}}):
                        Datoteka_unos.write((json.dumps(zahtjev_VALUE)+'\n').encode());Datoteka_unos.flush()
                        while True:
                            반환값=json.loads(Datoteka_unos.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(odredište_VALUE_položaj/'four-terminals.png')).convert('RGB')
            for koordinirani_par,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinirani_par)==색상,(koordinirani_par,화소들.getpixel(koordinirani_par))
            ljuska('echo FOUR_WINDOWS_OK')
            provjera_izvješće.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if podaci_položaj.poll() is None:podaci_položaj.terminate()
            try:podaci_položaj.wait(timeout=5)
            except subprocess.TimeoutExpired:podaci_položaj.kill();podaci_položaj.wait()
            odabirač_a916db4e.close();podaci_položaj.stdin.close();podaci_položaj.stdout.close();(odredište_VALUE_položaj/'serial.log').write_bytes(LOG_zapis);(odredište_VALUE_položaj/'report.json').write_text(json.dumps(provjera_izvješće,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pokreni()
