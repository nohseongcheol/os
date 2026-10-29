#!/usr/bin/env python3
"""rzeczywisty_dane QEMU/VNC에서 interpretator_poleceń 모서리 przeciągnąć_WARTOŚĆ·wskaźnik·동적 znak_WARTOŚĆ gniazdo_wpis·Edytuj_WARTOŚĆ treść_WARTOŚĆ_cb0f2404 보존를 검사한다."""
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
from PIL import Image
from Pulpit_Widok import PORÓWNAJ_WARTOŚĆ
from Wykonaj_polecenie import Project_korzeń


def test_okno_zmiana_rozmiaru(너비, wysokość_WARTOŚĆ, KR_ścieżka):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); numer_portu = 임시.getsockname()[1]
    zmienić_rozmiar_SMS = '{}x{}'.format(너비, wysokość_WARTOŚĆ)
    Proces_WARTOŚĆ = subprocess.Popen(['python3', str(Project_korzeń/'narzędzia/Wykonaj_polecenie.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numer_portu), '--resolution', zmienić_rozmiar_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector(); selektor_a916db4e.register(Proces_WARTOŚĆ.stdout, selectors.EVENT_READ)
    LOG_zapis = bytearray(); zdalny_WARTOŚĆ = None; transfer_WARTOŚĆ = None; wskaźnik_Ukryty=[False]

    def 기다리기(program_WARTOŚĆ, Uruchom_2=0):
        termin_ostateczny_WARTOŚĆ = time.monotonic() + 60
        while program_WARTOŚĆ not in LOG_zapis[Uruchom_2:]:
            if time.monotonic() > termin_ostateczny_WARTOŚĆ or Proces_WARTOŚĆ.poll() is not None or b'HALTED' in LOG_zapis or b'PANIC:' in LOG_zapis:
                raise AssertionError(LOG_zapis[Uruchom_2:].decode('utf-8', 'replace'))
            for Wydarzenie, _ in selektor_a916db4e.select(.1):
                dane = Wydarzenie.fileobj.read(65536)
                if dane: LOG_zapis.extend(dane)
        return LOG_zapis[Uruchom_2:].decode('utf-8', 'replace')

    def klikać_przycisk(symbol, 눌림=True): zdalny_WARTOŚĆ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def wysłać_SMS_a(tekst):
        Uruchom_2 = len(LOG_zapis)
        for znak_WARTOŚĆ in tekst:
            symbol = 0xff0d if znak_WARTOŚĆ == '\n' else ord(znak_WARTOŚĆ) if ord(znak_WARTOŚĆ) < 256 else 0x1000000 | ord(znak_WARTOŚĆ)
            klikać_przycisk(symbol); klikać_przycisk(symbol, False)
        return Uruchom_2

    def powłoka(tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', wysłać_SMS_a(tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, gałąź_stanowisko, 눌림): zdalny_WARTOŚĆ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, gałąź_stanowisko))

    def klikać_WARTOŚĆ(가로, gałąź_stanowisko): 가리키기(가로, gałąź_stanowisko, 1); 가리키기(가로, gałąź_stanowisko, 0)

    def mapa_bitowa_OBRAZ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 rzeczywisty_dane 너비를 쓴다.
        zdalny_WARTOŚĆ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, wysokość_WARTOŚĆ))
        rysunek_WARTOŚĆ = Image.new('RGB', (너비, wysokość_WARTOŚĆ)); obszar_WARTOŚĆ_9285603e = 0
        while True:
            Rodzaj_WARTOŚĆ = PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 1)[0]
            if Rodzaj_WARTOŚĆ == 2: continue
            if Rodzaj_WARTOŚĆ == 3:
                długość_WARTOŚĆ = struct.unpack('>I', PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 7)[3:])[0]; PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, długość_WARTOŚĆ); continue
            assert Rodzaj_WARTOŚĆ == 0, Rodzaj_WARTOŚĆ
            towar_ILE_LICZB = struct.unpack('>H', PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 3)[1:])[0]
            for _ in range(towar_ILE_LICZB):
                가로, gałąź_stanowisko, 폭, długość_WARTOŚĆ, Encoding_WARTOŚĆ = struct.unpack('>HHHHi', PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 12))
                if Encoding_WARTOŚĆ == -239:
                    assert 폭==0 and długość_WARTOŚĆ==0, 'remote cursor must be hidden'
                    wskaźnik_Ukryty[0]=True
                    continue
                assert Encoding_WARTOŚĆ == 0 and 가로+폭 <= 너비 and gałąź_stanowisko+długość_WARTOŚĆ <= wysokość_WARTOŚĆ
                rysunek_WARTOŚĆ.paste(Image.frombytes('RGB', (폭, długość_WARTOŚĆ), PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 폭*długość_WARTOŚĆ*4), 'raw', 'BGRX'), (가로, gałąź_stanowisko))
                obszar_WARTOŚĆ_9285603e += 폭*długość_WARTOŚĆ
            if obszar_WARTOŚĆ_9285603e:
                assert obszar_WARTOŚĆ_9285603e == 너비*wysokość_WARTOŚĆ, obszar_WARTOŚĆ_9285603e
                return rysunek_WARTOŚĆ

    def czek_piksel(współrzędna_WARTOŚĆ, 색):
        termin_ostateczny_WARTOŚĆ = time.monotonic()+10
        while True:
            rysunek_WARTOŚĆ = mapa_bitowa_OBRAZ()
            if rysunek_WARTOŚĆ.getpixel(współrzędna_WARTOŚĆ) == 색: return rysunek_WARTOŚĆ
            if time.monotonic() > termin_ostateczny_WARTOŚĆ: raise AssertionError((współrzędna_WARTOŚĆ, rysunek_WARTOŚĆ.getpixel(współrzędna_WARTOŚĆ), 색))

    def Upload_Files(Nazwa, dane): transfer_WARTOŚĆ.storbinary('STOR '+Nazwa, io.BytesIO(dane))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+zmienić_rozmiar_SMS+' RGB32').encode() in LOG_zapis
        print('BOOT:', zmienić_rozmiar_SMS, flush=True)
        zdalny_identyfikator = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_zapis).group(1))
        zdalny_WARTOŚĆ = socket.create_connection(('127.0.0.1', zdalny_identyfikator), timeout=20)
        assert PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 12) == b'RFB 003.008\n'; zdalny_WARTOŚĆ.sendall(b'RFB 003.008\n')
        assert 1 in PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 1)[0]); zdalny_WARTOŚĆ.sendall(b'\x01')
        assert PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 4) == b'\0'*4; zdalny_WARTOŚĆ.sendall(b'\x01')
        stan_początkowy = PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, 24); assert struct.unpack('>HH', stan_początkowy[:4]) == (너비, wysokość_WARTOŚĆ)
        PORÓWNAJ_WARTOŚĆ(zdalny_WARTOŚĆ, struct.unpack('>I', stan_początkowy[20:])[0])
        zdalny_WARTOŚĆ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        zdalny_WARTOŚĆ.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        czek_piksel((너비-1, wysokość_WARTOŚĆ-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Wydarzenie,_ in selektor_a916db4e.select(.02):
                    dane=Wydarzenie.fileobj.read(65536)
                    if dane:LOG_zapis.extend(dane)
        Okno=[12,48,568,360]
        def 크기확인():
            kolumna_WARTOŚĆ,WIERSZ_WARTOŚĆ=(Okno[2]-24)//8,(Okno[3]-56)//16
            tekst=powłoka('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(kolumna_WARTOŚĆ,WIERSZ_WARTOŚĆ) in tekst,tekst
            # rzeczywisty_dane Okno 테두리: 단지 Rozmiar zapytanie_WARTOŚĆ 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            czek_piksel((Okno[0],Okno[1]),(32,80,144))
            rysunek_WARTOŚĆ=czek_piksel((Okno[0]+Okno[2]-1,Okno[1]+Okno[3]-1),(39,49,64))
            return rysunek_WARTOŚĆ
        def 모서리(방향):
            return (Okno[0]+(3 if 방향 in (1,3) else Okno[2]-4),Okno[1]+(3 if 방향<=2 else Okno[3]-4))
        def zmienić_rozmiar_przeciągnąć(방향,차이,przycisk=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            czek_piksel(흰점,(255,255,255))
            가리키기(가,세,przycisk)
            끝가=max(0,min(너비-1,가+차이[0]));Koniec_gałąź=max(0,min(wysokość_WARTOŚĆ-1,세+차이[1]))
            가리키기(끝가,Koniec_gałąź,przycisk);가리키기(끝가,Koniec_gałąź,0);숨고르기()
            if przycisk==1:
                LEWY_WARTOŚĆ,위,폭,długość_WARTOŚĆ=Okno;PRAWY_WARTOŚĆ,아래=LEWY_WARTOŚĆ+폭,위+długość_WARTOŚĆ
                if 방향 in (1,3):LEWY_WARTOŚĆ=max(0,min(PRAWY_WARTOŚĆ-360,LEWY_WARTOŚĆ+끝가-가))
                else:PRAWY_WARTOŚĆ=max(LEWY_WARTOŚĆ+360,min(너비,PRAWY_WARTOŚĆ+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+Koniec_gałąź-세))
                else:아래=max(위+216,min(wysokość_WARTOŚĆ,아래+Koniec_gałąź-세))
                Okno[:]=[LEWY_WARTOŚĆ,위,PRAWY_WARTOŚĆ-LEWY_WARTOŚĆ,아래-위]
        크기확인();assert wskaźnik_Ukryty[0]
        zmienić_rozmiar_przeciągnąć(4,(-100,-60),4);크기확인() # PRAWY 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            zmienić_rozmiar_przeciągnąć(방향,차이);크기확인()
        # wejście_WARTOŚĆ 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        wysłać_SMS_a("echo '"+긴글+"'");숨고르기()
        zmienić_rozmiar_przeciągnąć(4,(-1000,-1000));assert Okno[2:]==[360,216]
        zmienić_rozmiar_przeciągnąć(4,(너비,wysokość_WARTOŚĆ))
        Uruchom_2=wysłać_SMS_a('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Uruchom_2);크기확인()
        # vi가 Edytuj_WARTOŚĆ 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        powłoka('ftpd start')
        transfer_WARTOŚĆ=ftplib.FTP();transfer_WARTOŚĆ.encoding='utf-8';transfer_WARTOŚĆ.connect('127.0.0.1',numer_portu,timeout=20);transfer_WARTOŚĆ.login()
        기다리기(b'NORMAL',wysłać_SMS_a('vi /크기자료.txt\n'))
        기다리기(b'INSERT',wysłać_SMS_a('i미저장 한글 dane\n'));숨고르기()
        zmienić_rozmiar_przeciągnąć(4,(-너비,-wysokość_WARTOŚĆ))
        # ANSI WIERSZ_WARTOŚĆ 이동에 새 WIERSZ_WARTOŚĆ 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Okno[3]-56)//16)).encode() in LOG_zapis[-4096:]
        wysłać_SMS_a('작은 창에서도 이어 Zapis\n');숨고르기()
        zmienić_rozmiar_przeciągnąć(4,(너비,wysokość_WARTOŚĆ))
        wysłać_SMS_a('큰 창에서도 이어 Zapis\n');숨고르기()
        klikać_przycisk(0xff1b);klikać_przycisk(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',wysłać_SMS_a(':wq\n'))
        treść_WARTOŚĆ_cb0f2404=bytearray();transfer_WARTOŚĆ.retrbinary('RETR 크기자료.txt',treść_WARTOŚĆ_cb0f2404.extend)
        assert treść_WARTOŚĆ_cb0f2404=='미저장 한글 dane\n작은 창에서도 이어 Zapis\n큰 창에서도 이어 Zapis\n'.encode(),treść_WARTOŚĆ_cb0f2404
        크기확인().save(str(KR_ścieżka/(zmienić_rozmiar_SMS+'-large.png')))
        # 두 번째 창은 wartość_domyślna Rozmiar, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Uruchom_2=len(LOG_zapis);klikać_WARTOŚĆ(70,16);기다리기(b'TERMINAL FOCUS 2',Uruchom_2)
        assert 'TERMINAL SIZE 68x19' in powłoka('terminal size')
        Uruchom_2=len(LOG_zapis);klikać_WARTOŚĆ(180,16);기다리기(b'TERMINAL FOCUS 1',Uruchom_2);크기확인()
        zmienić_rozmiar_przeciągnąć(4,(-너비,-wysokość_WARTOŚĆ));크기확인().save(str(KR_ścieżka/(zmienić_rozmiar_SMS+'-small.png')))
        # Rozmiar zmienić_WARTOŚĆ BACK_WARTOŚĆ X 닫기도 새로운 PRAWY 가장자리를 사용한다.
        Uruchom_2=len(LOG_zapis);klikać_WARTOŚĆ(Okno[0]+Okno[2]-20,Okno[1]+15);기다리기(b'TERMINAL FOCUS 2',Uruchom_2)
        assert 'RESIZE CLOSED' in powłoka('echo RESIZE CLOSED')
        print('PASS:',zmienić_rozmiar_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if transfer_WARTOŚĆ:transfer_WARTOŚĆ.close()
        if zdalny_WARTOŚĆ:zdalny_WARTOŚĆ.close()
        if Proces_WARTOŚĆ.poll() is None:
            Proces_WARTOŚĆ.terminate()
            try:Proces_WARTOŚĆ.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_WARTOŚĆ.kill();Proces_WARTOŚĆ.wait()
        selektor_a916db4e.close();Proces_WARTOŚĆ.stdout.close();(KR_ścieżka/(zmienić_rozmiar_SMS+'.log')).write_bytes(LOG_zapis)


def Uruchom_2():
    KR_ścieżka=Project_korzeń/'build/verification/resize';KR_ścieżka.mkdir(parents=True,exist_ok=True)
    LOG_zapis={'passed':False,'kernel_sha256':hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,wysokość_WARTOŚĆ in ((640,480),(1920,1080)):
            test_okno_zmiana_rozmiaru(너비,wysokość_WARTOŚĆ,KR_ścieżka);LOG_zapis['resolutions'].append([너비,wysokość_WARTOŚĆ])
        LOG_zapis.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_ścieżka/'report.json').write_text(json.dumps(LOG_zapis,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Uruchom_2()
