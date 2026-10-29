#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Wykonaj_polecenie import Project_korzeń,polecenie

def Uruchom_2():
    cel_WARTOŚĆ_stanowisko=Project_korzeń/'build/verification/swing';cel_WARTOŚĆ_stanowisko.mkdir(parents=True,exist_ok=True)
    Klasa_ścieżka=Project_korzeń/'build/verification/new-java';Klasa_ścieżka.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_korzeń/'dist/jkoros-native-korean.jar'),'-d',str(Klasa_ścieżka),str(Project_korzeń/'testy/자바/Swing_test.java'),str(Project_korzeń/'testy/자바/한글창시험.java')])
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
            dane=(Project_korzeń/'build/verification/new-java/Swing_test.class').read_bytes()
            wysłać('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dane),64):wysłać(dane[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            wysłać(b'.\n')
            wysłać('java Swing_test\n'.encode(),b'SWING READY')
            Koniec_przesunąć=time.monotonic()+3
            while time.monotonic()<Koniec_przesunąć:uchwyt_konkurs(.1)
            # JFrame centered at (120,100), content at y=130.
            wysłać(klikać_przycisk(200,210),b'',)  # focus JTextField
            dane_stanowisko.stdin.write('누리'.encode());dane_stanowisko.stdin.flush()
            Koniec_przesunąć=time.monotonic()+.3
            while time.monotonic()<Koniec_przesunąć:uchwyt_konkurs(.05)
            WYNIK=wysłać(klikać_przycisk(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_zapis)-len(WYNIK))
            wysłać(skrót_WARTOŚĆ(1),b'TERMINAL FOCUS 2')
            WYNIK=powłoka('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in WYNIK
            wysłać(klikać_przycisk(180,12),b'TERMINAL FOCUS 1')
            Koniec_przesunąć=time.monotonic()+.3
            while time.monotonic()<Koniec_przesunąć:uchwyt_konkurs(.05)
            with socket.socket(socket.AF_UNIX) as kod_znaku:
                kod_znaku.settimeout(10);kod_znaku.connect(str(모의제어접속))
                with kod_znaku.makefile('rwb') as Plik_wpis:
                    json.loads(Plik_wpis.readline())
                    for żądanie_WARTOŚĆ in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cel_WARTOŚĆ_stanowisko/'native-swing.png'),'format':'png'}}):
                        Plik_wpis.write((json.dumps(żądanie_WARTOŚĆ)+'\n').encode());Plik_wpis.flush()
                        while True:
                            반환값=json.loads(Plik_wpis.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            wysłać(klikać_przycisk(505,115))
            powłoka('echo SWING_CLOSED_OK')
            dane=(Klasa_ścieżka/'한글창시험.class').read_bytes()
            wysłać('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dane),64):wysłać(dane[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            wysłać(b'.\n')
            wysłać('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            wysłać(klikać_przycisk(200,255),'KOREAN SWING CLICK Nazwa'.encode())
            wysłać(klikać_przycisk(505,115))
            powłoka('echo KOREAN_SWING_CLOSED_OK')
            walidacja_Raport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','polski Okno/przycisk/akcja_powiadomienie/konkurs_kolejka directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if dane_stanowisko.poll() is None:dane_stanowisko.terminate()
            try:dane_stanowisko.wait(timeout=5)
            except subprocess.TimeoutExpired:dane_stanowisko.kill();dane_stanowisko.wait()
            selektor_a916db4e.close();dane_stanowisko.stdin.close();dane_stanowisko.stdout.close();(cel_WARTOŚĆ_stanowisko/'serial.log').write_bytes(LOG_zapis);(cel_WARTOŚĆ_stanowisko/'report.json').write_text(json.dumps(walidacja_Raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Uruchom_2()
