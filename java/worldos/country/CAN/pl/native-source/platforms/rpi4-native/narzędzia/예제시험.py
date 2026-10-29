#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from Pulpit_Widok import PORÓWNAJ_WARTOŚĆ
from 예제되돌림서버 import echo_Serwery
from Wykonaj_polecenie import Project_korzeń


def test_Język(Język,echo_serwer_wpis,KR_dane):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));transfer_plików_numer_portu=임시자원.getsockname()[1]
    Proces=subprocess.Popen(['python3',str(Project_korzeń/'narzędzia/Wykonaj_polecenie.py'),'--desktop','--network','--port','0','--ftp-port',str(transfer_plików_numer_portu)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selektor=selectors.DefaultSelector();selektor.register(Proces.stdout,selectors.EVENT_READ)
    transkrypcja=bytearray();klient=None;transfer_plików_połączenie=None
    def odbierać_e_mail(pisak,Uruchom_2=0):
        Koniec_przesunąć=time.monotonic()+60
        while pisak not in transkrypcja[Uruchom_2:]:
            if time.monotonic()>Koniec_przesunąć or Proces.poll() is not None:raise AssertionError(transkrypcja[Uruchom_2:].decode('utf-8','replace'))
            for 누름값,_ in selektor.select(.1):
                dane=누름값.fileobj.read(65536)
                if dane:transkrypcja.extend(dane)
        return transkrypcja[Uruchom_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbol_WARTOŚĆ,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_WARTOŚĆ))
    def START_przesunąć(wiersz_wejścia):
        Uruchom_2=len(transkrypcja)
        for kod_znaku in wiersz_wejścia+'\n':
            symbol_WARTOŚĆ=0xff0d if kod_znaku=='\n' else ord(kod_znaku) if ord(kod_znaku)<256 else 0x1000000|ord(kod_znaku)
            누름값(symbol_WARTOŚĆ);누름값(symbol_WARTOŚĆ,False)
        return Uruchom_2
    def powłoka(wiersz_wejścia):return odbierać_e_mail(b'jkoros-native> ',START_przesunąć(wiersz_wejścia))
    def Wykonaj_polecenie(wiersz_wejścia,예상결과):
        tekst=powłoka(wiersz_wejścia);assert 예상결과 in tekst and 'exit 0' in tekst,(wiersz_wejścia,tekst)
        return tekst
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            obszar_WARTOŚĆ=PORÓWNAJ_WARTOŚĆ(klient,1)[0]
            if obszar_WARTOŚĆ==2:continue
            if obszar_WARTOŚĆ==3:
                towar_ILE_LICZB=struct.unpack('>I',PORÓWNAJ_WARTOŚĆ(klient,7)[3:])[0];PORÓWNAJ_WARTOŚĆ(klient,towar_ILE_LICZB);continue
            assert obszar_WARTOŚĆ==0,obszar_WARTOŚĆ
            wpis_ILE_LICZB=struct.unpack('>H',PORÓWNAJ_WARTOŚĆ(klient,3)[1:])[0]
            for _ in range(wpis_ILE_LICZB):
                współrzędna_X,Y_współrzędna,너비값,wymagane_wysokość_WARTOŚĆ,zestaw_znaków=struct.unpack('>HHHHi',PORÓWNAJ_WARTOŚĆ(klient,12));assert zestaw_znaków==0,zestaw_znaków
                dane=PORÓWNAJ_WARTOŚĆ(klient,너비값*wymagane_wysokość_WARTOŚĆ*4)
                for WIERSZ_stanowisko in range(wymagane_wysokość_WARTOŚĆ):
                    for kolumna_stanowisko in range(너비값):
                        원본자료=(WIERSZ_stanowisko*너비값+kolumna_stanowisko)*4;wartość_docelowa=((Y_współrzędna+WIERSZ_stanowisko)*640+współrzędna_X+kolumna_stanowisko)*3
                        빛삼원색[wartość_docelowa:wartość_docelowa+3]=bytes((dane[원본자료+2],dane[원본자료+1],dane[원본자료]))
            if wpis_ILE_LICZB:return 빛삼원색
    try:
        odbierać_e_mail(b'TERMINAL READY');odbierać_e_mail(b'jkoros-native> ',transkrypcja.rfind(b'TERMINAL READY'))
        numer_portu=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkrypcja).group(1))
        klient=socket.create_connection(('127.0.0.1',numer_portu),timeout=10)
        assert PORÓWNAJ_WARTOŚĆ(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in PORÓWNAJ_WARTOŚĆ(klient,PORÓWNAJ_WARTOŚĆ(klient,1)[0]);klient.sendall(b'\x01');assert PORÓWNAJ_WARTOŚĆ(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=PORÓWNAJ_WARTOŚĆ(klient,24);PORÓWNAJ_WARTOŚĆ(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in powłoka('ftpd start')
        transfer_plików_połączenie=ftplib.FTP();transfer_plików_połączenie.encoding='utf-8';transfer_plików_połączenie.connect('127.0.0.1',transfer_plików_numer_portu,timeout=20);transfer_plików_połączenie.login()
        ładunek_dane=('GUI와 FTP 동시 używać_WARTOŚĆ '+Język+' 😀\n').encode()
        transfer_plików_połączenie.storbinary('STOR 함께.txt',io.BytesIO(ładunek_dane))
        assert ładunek_dane.decode().strip() in powłoka('cat /함께.txt')
        KWOTA_WYKUP_ILE_LICZB=bytearray();transfer_plików_połączenie.retrbinary('RETR 함께.txt',KWOTA_WYKUP_ILE_LICZB.extend);assert KWOTA_WYKUP_ILE_LICZB==ładunek_dane;transfer_plików_połączenie.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        wysłać_Lista=powłoka('ls /example')
        assert all(Nazwa in wysłać_Lista for Nazwa in ('java/','c/','python/','README.md')),wysłać_Lista
        if Język=='java':
            pakiet_manifest=json.loads((Project_korzeń/'build/examples/manifest.json').read_text())
            for ścieżka_2,punkt_wejścia in pakiet_manifest.items():
                powłoka('cp '+ścieżka_2+' /example-check.bin')
                treść_WARTOŚĆ_cb0f2404=bytearray();transfer_plików_połączenie.retrbinary('RETR example-check.bin',treść_WARTOŚĆ_cb0f2404.extend)
                assert len(treść_WARTOŚĆ_cb0f2404)==punkt_wejścia['bytes'] and hashlib.sha256(treść_WARTOŚĆ_cb0f2404).hexdigest()==punkt_wejścia['sha256'],ścieżka_2
            transfer_plików_połączenie.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binarny=bytes(range(256))*64
            transfer_plików_połączenie.storbinary('STOR boundary.bin',io.BytesIO(binarny))
            treść_WARTOŚĆ_cb0f2404=bytearray();transfer_plików_połączenie.retrbinary('RETR boundary.bin',treść_WARTOŚĆ_cb0f2404.extend)
            assert treść_WARTOŚĆ_cb0f2404==binarny and 'boundary.bin' in transfer_plików_połączenie.nlst()
            powłoka('cp /boundary.bin /boundary-copy.bin')
            treść_WARTOŚĆ_cb0f2404=bytearray();transfer_plików_połączenie.retrbinary('RETR boundary-copy.bin',treść_WARTOŚĆ_cb0f2404.extend)
            assert treść_WARTOŚĆ_cb0f2404==binarny
            transfer_plików_połączenie.delete('boundary.bin');transfer_plików_połączenie.delete('boundary-copy.bin')
        assert 'PrzykładWyjścia' in powłoka('ls /example/'+Język)
        powłoka('cd /example/'+Język)
        nazwa_tabela={'java':'JAVA','c':'C','python':'PYTHON'}[Język]
        예상파일=nazwa_tabela+' nazwa_pliku: 한글 dane 😀\n'
        if Język=='java':
            Wykonaj_polecenie('javac PrzykładWyjścia.java','Compiled:');Wykonaj_polecenie('java PrzykładWyjścia','JAVA pozycja_wyjścia: 안녕하세요 😀')
            Wykonaj_polecenie('javac PrzykładPliku.java','Compiled:');Wykonaj_polecenie('java PrzykładPliku',예상파일)
            Wykonaj_polecenie('java PrzykładSieci {} {}'.format(echo_serwer_wpis.port_TCP,echo_serwer_wpis.UDP_port),'JAVA 네트워크 확인: TCP UDP 한글')
            grafika_polecenie='java PrzykładRysunku'
        elif Język=='c':
            for Nazwa,전달값,예상결과 in [('pozycja_wyjścia','', 'C pozycja_wyjścia: 안녕하세요 😀'),('nazwa_pliku','',예상파일),
                    ('네트워크',' '+str(echo_serwer_wpis.UDP_port),'C 네트워크 확인: UDP 한글')]:
                Wykonaj_polecenie('cc '+Nazwa+'예제.c -o Wykonaj_polecenie','Compiled native ARM64 ELF:')
                Wykonaj_polecenie('./Wykonaj_polecenie'+전달값,예상결과)
            Wykonaj_polecenie('cc PrzykładRysunku.c -o Wykonaj_polecenie','Compiled native ARM64 ELF:');grafika_polecenie='./Wykonaj_polecenie'
        else:
            for Nazwa,전달값,예상결과 in [('pozycja_wyjścia','','PYTHON pozycja_wyjścia: 안녕하세요 😀'),('nazwa_pliku','',예상파일),
                    ('네트워크',' '+str(echo_serwer_wpis.UDP_port),'PYTHON 네트워크 확인: UDP 한글')]:
                Wykonaj_polecenie('python '+Nazwa+'예제.py'+전달값,예상결과)
            grafika_polecenie='python PrzykładRysunku.py'
        START_rysunek=START_przesunąć(grafika_polecenie)
        tekst=odbierać_e_mail('그림을 확인한 BACK_WARTOŚĆ Enter를 누르세요.\r\n'.encode(),START_rysunek)
        assert nazwa_tabela+' 그래픽: 빨강 초록 파랑' in tekst and 'exit 0' not in tekst,tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        transfer_plików_połączenie.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        KWOTA_WYKUP_ILE_LICZB=bytearray();transfer_plików_połączenie.retrbinary('RETR 도중.txt',KWOTA_WYKUP_ILE_LICZB.extend);assert KWOTA_WYKUP_ILE_LICZB==b'FTP DURING GRAPHICS';transfer_plików_połączenie.delete('도중.txt')
        빛삼원색=화소들()
        for Y_współrzędna,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            przesunąć_WARTOŚĆ_450fc799=(Y_współrzędna*640+610)*3;assert tuple(빛삼원색[przesunąć_WARTOŚĆ_450fc799:przesunąć_WARTOŚĆ_450fc799+3])==색상,(Język,Y_współrzędna,tuple(빛삼원색[przesunąć_WARTOŚĆ_450fc799:przesunąć_WARTOŚĆ_450fc799+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_dane/(Język+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in odbierać_e_mail(b'jkoros-native> ',START_rysunek)
        if Język=='java':
            START_okno=START_przesunąć('java PrzykładOkna')
            odbierać_e_mail('GUI 예제 Przygotuj: PrzykładOkna'.encode(),START_okno)
            def klikać_WARTOŚĆ(가로,gałąź_stanowisko):
                for przycisk in (1,0):klient.sendall(struct.pack('>BBHH',5,przycisk,가로,gałąź_stanowisko))
            time.sleep(.3)
            Wstecz_OBRAZ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klikać_WARTOŚĆ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for znak_WARTOŚĆ in '한글':누름값(0x1000000|ord(znak_WARTOŚĆ));누름값(0x1000000|ord(znak_WARTOŚĆ),False)
            for powtórzenie_ILE_LICZB in (1,2):
                Uruchom_2=len(transkrypcja);klikać_WARTOŚĆ(180,242)
                odbierać_e_mail(('GUI 인사: 안녕하세요, 한글님! ('+str(powtórzenie_ILE_LICZB)+')').encode(),Uruchom_2)
            time.sleep(.3)
            okno_rysunek=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Wstecz_OBRAZ.crop((110,272,530,300)).tobytes()!=okno_rysunek.crop((110,272,530,300)).tobytes()
            okno_rysunek.save(str(KR_dane/'java-swing.png'))
            Uruchom_2=len(transkrypcja);klikać_WARTOŚĆ(535,105)
            assert 'exit 0' in odbierać_e_mail(b'jkoros-native> ',Uruchom_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Plik_wpis_nazwa={'java':'java.txt','c':'c.txt','python':'python.txt'}[Język]
        powłoka('cp '+Plik_wpis_nazwa+' /walidować.txt')
        KWOTA_WYKUP_ILE_LICZB=bytearray();transfer_plików_połączenie.retrbinary('RETR walidować.txt',KWOTA_WYKUP_ILE_LICZB.extend);assert KWOTA_WYKUP_ILE_LICZB==예상파일.encode()
        powłoka('echo preserved > PrzykładWyjścia.'+('py' if Język=='python' else Język))
        assert 'EXAMPLES READY' in powłoka('example '+Język)
        assert '\npreserved\n' in powłoka('cat PrzykładWyjścia.'+('py' if Język=='python' else Język))
        assert '한/zero_operand Klucz_WARTOŚĆ, Shift+Space 또는 F9' in powłoka('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in powłoka('echo GUI NETWORK TOGETHER')
        transfer_plików_połączenie.quit();transfer_plików_połączenie=None;assert 'FTP stopped' in powłoka('ftpd stop')
        print('PASS '+Język+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if transfer_plików_połączenie:
            try:transfer_plików_połączenie.close()
            except OSError:pass
        if klient:klient.close()
        Proces.terminate()
        try:Proces.wait(timeout=8)
        except subprocess.TimeoutExpired:Proces.kill();Proces.wait()
        selektor.close();Proces.stdout.close();(KR_dane/(Język+'-serial.log')).write_bytes(transkrypcja)


def Uruchom_2():
    KR_dane=Project_korzeń/'build/verification/examples';KR_dane.mkdir(parents=True,exist_ok=True)
    walidacja_Raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with echo_Serwery() as echo_serwer_wpis:
            for Język in ('java','c','python'):
                test_Język(Język,echo_serwer_wpis,KR_dane);walidacja_Raport['languages'].append(Język)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert echo_serwer_wpis.수신됨==[(obszar_WARTOŚĆ,dane.encode()) for obszar_WARTOŚĆ,dane in 예상결과],echo_serwer_wpis.수신됨
            walidacja_Raport['host_network_payloads']=[{'protocol':obszar_WARTOŚĆ,'text':dane.decode()} for obszar_WARTOŚĆ,dane in echo_serwer_wpis.수신됨]
        walidacja_Raport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_dane/'report.json').write_text(json.dumps(walidacja_Raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Uruchom_2()
