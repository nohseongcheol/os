#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Wykonaj_polecenie import Project_korzeń,polecenie

def Uruchom_2():
    cel_WARTOŚĆ_stanowisko=Project_korzeń/'build/verification/windows';cel_WARTOŚĆ_stanowisko.mkdir(parents=True,exist_ok=True)
    walidacja_Raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest()};LOG_zapis=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        dane_stanowisko=subprocess.Popen(polecenie()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selektor_a916db4e=selectors.DefaultSelector();selektor_a916db4e.register(dane_stanowisko.stdout,selectors.EVENT_READ)
        def uchwyt_konkurs(초단위=.1):
            for 누름값,_ in selektor_a916db4e.select(초단위):
                SEKUNDA_WARTOŚĆ=누름값.fileobj.read(65536)
                if SEKUNDA_WARTOŚĆ:LOG_zapis.extend(SEKUNDA_WARTOŚĆ)
            assert b'PANIC:' not in LOG_zapis and b'HALTED' not in LOG_zapis,LOG_zapis[-2048:]
        def 기다리기(pisak,bieżący_stanowisko,초단위=50):
            Koniec_przesunąć=time.monotonic()+초단위
            while pisak not in LOG_zapis[bieżący_stanowisko:]:
                if time.monotonic()>Koniec_przesunąć or dane_stanowisko.poll() is not None:raise AssertionError(LOG_zapis[bieżący_stanowisko:].decode('utf-8','replace'))
                uchwyt_konkurs()
            return bytes(LOG_zapis[bieżący_stanowisko:])
        def wysłać(SEKUNDA_WARTOŚĆ,pisak=b'jkoros-native> '):
            bieżący_stanowisko=len(LOG_zapis);dane_stanowisko.stdin.write(SEKUNDA_WARTOŚĆ);dane_stanowisko.stdin.flush();return 기다리기(pisak,bieżący_stanowisko)
        def powłoka(ciąg_dane):return wysłać((ciąg_dane+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def skrót_WARTOŚĆ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikać_przycisk(współrzędna_X,Y_współrzędna):return bytes([30,1,1,współrzędna_X&255,współrzędna_X>>8,Y_współrzędna&255,Y_współrzędna>>8,30,1,0,współrzędna_X&255,współrzędna_X>>8,Y_współrzędna&255,Y_współrzędna>>8])
        def polecenie_tryb():
            dane_stanowisko.stdin.write(b'\x1b');dane_stanowisko.stdin.flush();Koniec_przesunąć=time.monotonic()+.2
            while time.monotonic()<Koniec_przesunąć:uchwyt_konkurs(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            powłoka('terminal');uchwyt_konkurs(.3)
            powłoka('mkdir first; cd first; export NAME=one')
            wysłać('vi 첫째.py\n'.encode(),b'NORMAL')
            wysłać('i값 = 21\nprint(WARTOŚĆ * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            Koniec_przesunąć=time.monotonic()+3
            while time.monotonic()<Koniec_przesunąć:uchwyt_konkurs(.1)
            wysłać(skrót_WARTOŚĆ(1),b'TERMINAL FOCUS 2');uchwyt_konkurs(.2)
            assert b'/\r\n' in powłoka('pwd')
            powłoka('export NAME=two')
            wysłać('vi 둘째.txt\n'.encode(),b'NORMAL')
            wysłać('i두 번째 Okno\n'.encode(),b'INSERT')
            wysłać(klikać_przycisk(180,12),b'TERMINAL FOCUS 1');uchwyt_konkurs(.2)
            polecenie_tryb();wysłać(b':wq\r')
            assert b'one:/first' in powłoka('echo "$NAME:$PWD"')
            assert 'WARTOŚĆ = 21\r\nprint(WARTOŚĆ * 2)'.encode() in powłoka('cat 첫째.py')
            WYNIK=powłoka('python 첫째.py');assert b'42\r\n' in WYNIK,WYNIK
            # Close the first shell with its actual title-bar X; second editor resumes.
            wysłać(klikać_przycisk(560,63),b'TERMINAL FOCUS 2');uchwyt_konkurs(.2)
            polecenie_tryb();wysłać(b':wq\r')
            assert b'two:/' in powłoka('echo "$NAME:$PWD"')
            assert '두 번째 Okno'.encode() in powłoka('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            wysłać('vi 둘째.txt\n'.encode(),b'NORMAL');wysłać(b'xu',b'NORMAL')
            wysłać(b'iX',b'INSERT');polecenie_tryb();wysłać(b':q\r',b'Unsaved')
            wysłać(b':q!\r');assert '두 번째 Okno'.encode() in powłoka('cat 둘째.txt')
            wysłać(skrót_WARTOŚĆ(1),b'TERMINAL FOCUS 1');uchwyt_konkurs(.2)
            wysłać(skrót_WARTOŚĆ(1),b'TERMINAL FOCUS 3');uchwyt_konkurs(.2)
            wysłać(skrót_WARTOŚĆ(1),b'TERMINAL FOCUS 4');uchwyt_konkurs(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            dane_stanowisko.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));dane_stanowisko.stdin.flush()
            powłoka('echo DRAGGED_OK')
            wysłać('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            wysłać('i저장하지 않은 dane'.encode(),b'INSERT')
            wysłać(klikać_przycisk(578,97),b'TERMINAL FOCUS 3');uchwyt_konkurs(.2)
            assert '버릴문서.txt'.encode() not in powłoka('ls')
            wysłać(skrót_WARTOŚĆ(1),b'TERMINAL FOCUS 4');uchwyt_konkurs(.2)
            powłoka('echo REUSED_WINDOW_OK')
            Wykonane_ilość=LOG_zapis.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Wykonane_ilość)
            # UART completion precedes the next QEMU display refresh.
            Koniec_przesunąć=time.monotonic()+.3
            while time.monotonic()<Koniec_przesunąć:uchwyt_konkurs(.05)
            with socket.socket(socket.AF_UNIX) as kod_znaku:
                kod_znaku.settimeout(10);kod_znaku.connect(str(모의제어접속))
                with kod_znaku.makefile('rwb') as Plik_wpis:
                    json.loads(Plik_wpis.readline())
                    for żądanie_WARTOŚĆ in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cel_WARTOŚĆ_stanowisko/'four-terminals.png'),'format':'png'}}):
                        Plik_wpis.write((json.dumps(żądanie_WARTOŚĆ)+'\n').encode());Plik_wpis.flush()
                        while True:
                            반환값=json.loads(Plik_wpis.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(cel_WARTOŚĆ_stanowisko/'four-terminals.png')).convert('RGB')
            for para_koordynatów,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(para_koordynatów)==색상,(para_koordynatów,화소들.getpixel(para_koordynatów))
            powłoka('echo FOUR_WINDOWS_OK')
            walidacja_Raport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if dane_stanowisko.poll() is None:dane_stanowisko.terminate()
            try:dane_stanowisko.wait(timeout=5)
            except subprocess.TimeoutExpired:dane_stanowisko.kill();dane_stanowisko.wait()
            selektor_a916db4e.close();dane_stanowisko.stdin.close();dane_stanowisko.stdout.close();(cel_WARTOŚĆ_stanowisko/'serial.log').write_bytes(LOG_zapis);(cel_WARTOŚĆ_stanowisko/'report.json').write_text(json.dumps(walidacja_Raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Uruchom_2()
