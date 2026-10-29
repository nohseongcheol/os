#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izvedi_ukaz import pobuda_koren,Ukaz

def Zaženi():
    cilj_VALUE_položaj=pobuda_koren/'build/verification/windows';cilj_VALUE_položaj.mkdir(parents=True,exist_ok=True)
    preverjanje_veljavnosti_prijavi={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest()};LOG_zapis=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        podatki_položaj=subprocess.Popen(Ukaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        izbirnik_a916db4e=selectors.DefaultSelector();izbirnik_a916db4e.register(podatki_položaj.stdout,selectors.EVENT_READ)
        def ročica_dogodek(초단위=.1):
            for 누름값,_ in izbirnik_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_zapis.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_zapis and b'HALTED' not in LOG_zapis,LOG_zapis[-2048:]
        def 기다리기(oznaka,sprotno_položaj,초단위=50):
            končati_klic_odmik=time.monotonic()+초단위
            while oznaka not in LOG_zapis[sprotno_položaj:]:
                if time.monotonic()>končati_klic_odmik or podatki_položaj.poll() is not None:raise AssertionError(LOG_zapis[sprotno_položaj:].decode('utf-8','replace'))
                ročica_dogodek()
            return bytes(LOG_zapis[sprotno_položaj:])
        def poslati(SECOND_VALUE,oznaka=b'jkoros-native> '):
            sprotno_položaj=len(LOG_zapis);podatki_položaj.stdin.write(SECOND_VALUE);podatki_položaj.stdin.flush();return 기다리기(oznaka,sprotno_položaj)
        def lupina(niz_podatki):return poslati((niz_podatki+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def bližnjica_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_gumb(koordinata_x,세로좌표):return bytes([30,1,1,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8,30,1,0,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8])
        def ukaz_MODE():
            podatki_položaj.stdin.write(b'\x1b');podatki_položaj.stdin.flush();končati_klic_odmik=time.monotonic()+.2
            while time.monotonic()<končati_klic_odmik:ročica_dogodek(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            lupina('terminal');ročica_dogodek(.3)
            lupina('mkdir first; cd first; export NAME=one')
            poslati('vi 첫째.py\n'.encode(),b'NORMAL')
            poslati('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            končati_klic_odmik=time.monotonic()+3
            while time.monotonic()<končati_klic_odmik:ročica_dogodek(.1)
            poslati(bližnjica_VALUE(1),b'TERMINAL FOCUS 2');ročica_dogodek(.2)
            assert b'/\r\n' in lupina('pwd')
            lupina('export NAME=two')
            poslati('vi 둘째.txt\n'.encode(),b'NORMAL')
            poslati('i두 번째 okno\n'.encode(),b'INSERT')
            poslati(klik_gumb(180,12),b'TERMINAL FOCUS 1');ročica_dogodek(.2)
            ukaz_MODE();poslati(b':wq\r')
            assert b'one:/first' in lupina('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in lupina('cat 첫째.py')
            REZULTAT=lupina('python 첫째.py');assert b'42\r\n' in REZULTAT,REZULTAT
            # Close the first shell with its actual title-bar X; second editor resumes.
            poslati(klik_gumb(560,63),b'TERMINAL FOCUS 2');ročica_dogodek(.2)
            ukaz_MODE();poslati(b':wq\r')
            assert b'two:/' in lupina('echo "$NAME:$PWD"')
            assert '두 번째 okno'.encode() in lupina('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            poslati('vi 둘째.txt\n'.encode(),b'NORMAL');poslati(b'xu',b'NORMAL')
            poslati(b'iX',b'INSERT');ukaz_MODE();poslati(b':q\r',b'Unsaved')
            poslati(b':q!\r');assert '두 번째 okno'.encode() in lupina('cat 둘째.txt')
            poslati(bližnjica_VALUE(1),b'TERMINAL FOCUS 1');ročica_dogodek(.2)
            poslati(bližnjica_VALUE(1),b'TERMINAL FOCUS 3');ročica_dogodek(.2)
            poslati(bližnjica_VALUE(1),b'TERMINAL FOCUS 4');ročica_dogodek(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            podatki_položaj.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));podatki_položaj.stdin.flush()
            lupina('echo DRAGGED_OK')
            poslati('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            poslati('i저장하지 않은 podatki'.encode(),b'INSERT')
            poslati(klik_gumb(578,97),b'TERMINAL FOCUS 3');ročica_dogodek(.2)
            assert '버릴문서.txt'.encode() not in lupina('ls')
            poslati(bližnjica_VALUE(1),b'TERMINAL FOCUS 4');ročica_dogodek(.2)
            lupina('echo REUSED_WINDOW_OK')
            Dokončano_znesek=LOG_zapis.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Dokončano_znesek)
            # UART completion precedes the next QEMU display refresh.
            končati_klic_odmik=time.monotonic()+.3
            while time.monotonic()<končati_klic_odmik:ročica_dogodek(.05)
            with socket.socket(socket.AF_UNIX) as koda_znaka:
                koda_znaka.settimeout(10);koda_znaka.connect(str(모의제어접속))
                with koda_znaka.makefile('rwb') as Datoteka_vnos:
                    json.loads(Datoteka_vnos.readline())
                    for zahteva_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cilj_VALUE_položaj/'four-terminals.png'),'format':'png'}}):
                        Datoteka_vnos.write((json.dumps(zahteva_VALUE_625fa62c)+'\n').encode());Datoteka_vnos.flush()
                        while True:
                            반환값=json.loads(Datoteka_vnos.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(cilj_VALUE_položaj/'four-terminals.png')).convert('RGB')
            for par_koordinat,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(par_koordinat)==색상,(par_koordinat,화소들.getpixel(par_koordinat))
            lupina('echo FOUR_WINDOWS_OK')
            preverjanje_veljavnosti_prijavi.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if podatki_položaj.poll() is None:podatki_položaj.terminate()
            try:podatki_položaj.wait(timeout=5)
            except subprocess.TimeoutExpired:podatki_položaj.kill();podatki_položaj.wait()
            izbirnik_a916db4e.close();podatki_položaj.stdin.close();podatki_položaj.stdout.close();(cilj_VALUE_položaj/'serial.log').write_bytes(LOG_zapis);(cilj_VALUE_položaj/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Zaženi()
