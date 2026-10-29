#!/usr/bin/env python3
"""stvarni_podaci QEMU/VNC에서 Terminal 모서리 prevući_VALUE·pokazivač·동적 znak_VALUE 칸·Uredi_VALUE Sadržaj_VALUE 보존를 검사한다."""
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
from desktop_Prikaz import EXACT_VALUE
from Izvrši_komanda import radnja_koren


def 창크기시험(너비, 높이, KR_putanja):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); broj_porta = 임시.getsockname()[1]
    promeniti_veličinu_SMS = '{}x{}'.format(너비, 높이)
    Proces_VALUE = subprocess.Popen(['python3', str(radnja_koren/'Alatke/Izvrši_komanda.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(broj_porta), '--resolution', promeniti_veličinu_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    birač_a916db4e = selectors.DefaultSelector(); birač_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_snimi = bytearray(); udaljen_VALUE = None; prenos_VALUE = None; pokazivač_Skriveno=[False]

    def 기다리기(emisija_VALUE, koristiti=0):
        krajnji_rok_VALUE = time.monotonic() + 60
        while emisija_VALUE not in LOG_snimi[koristiti:]:
            if time.monotonic() > krajnji_rok_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_snimi or b'PANIC:' in LOG_snimi:
                raise AssertionError(LOG_snimi[koristiti:].decode('utf-8', 'replace'))
            for događaj, _ in birač_a916db4e.select(.1):
                podaci = događaj.fileobj.read(65536)
                if podaci: LOG_snimi.extend(podaci)
        return LOG_snimi[koristiti:].decode('utf-8', 'replace')

    def klik_taster(simbol, 눌림=True): udaljen_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def poslati_SMS_poruku(SMS):
        koristiti = len(LOG_snimi)
        for znak_VALUE in SMS:
            simbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            klik_taster(simbol); klik_taster(simbol, False)
        return koristiti

    def ljuska(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', poslati_SMS_poruku(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, vertikala_pozicija, 눌림): udaljen_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikala_pozicija))

    def klik_VALUE(가로, vertikala_pozicija): 가리키기(가로, vertikala_pozicija, 1); 가리키기(가로, vertikala_pozicija, 0)

    def raster_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 stvarni_podaci 너비를 쓴다.
        udaljen_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        crtež_VALUE = Image.new('RGB', (너비, 높이)); oblast_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(udaljen_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(udaljen_VALUE, 7)[3:])[0]; EXACT_VALUE(udaljen_VALUE, 길이); continue
            assert 종류 == 0, 종류
            stavka_COUNT = struct.unpack('>H', EXACT_VALUE(udaljen_VALUE, 3)[1:])[0]
            for _ in range(stavka_COUNT):
                가로, vertikala_pozicija, 폭, 길이, kodiranje_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(udaljen_VALUE, 12))
                if kodiranje_VALUE == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    pokazivač_Skriveno[0]=True
                    continue
                assert kodiranje_VALUE == 0 and 가로+폭 <= 너비 and vertikala_pozicija+길이 <= 높이
                crtež_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(udaljen_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, vertikala_pozicija))
                oblast_VALUE_9285603e += 폭*길이
            if oblast_VALUE_9285603e:
                assert oblast_VALUE_9285603e == 너비*높이, oblast_VALUE_9285603e
                return crtež_VALUE

    def proveriti_piksel(좌표, 색):
        krajnji_rok_VALUE = time.monotonic()+10
        while True:
            crtež_VALUE = raster_IMAGE()
            if crtež_VALUE.getpixel(좌표) == 색: return crtež_VALUE
            if time.monotonic() > krajnji_rok_VALUE: raise AssertionError((좌표, crtež_VALUE.getpixel(좌표), 색))

    def Otprema_Datoteke(ime, podaci): prenos_VALUE.storbinary('STOR '+ime, io.BytesIO(podaci))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+promeniti_veličinu_SMS+' RGB32').encode() in LOG_snimi
        print('BOOT:', promeniti_veličinu_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_snimi).group(1))
        udaljen_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(udaljen_VALUE, 12) == b'RFB 003.008\n'; udaljen_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(udaljen_VALUE, EXACT_VALUE(udaljen_VALUE, 1)[0]); udaljen_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(udaljen_VALUE, 4) == b'\0'*4; udaljen_VALUE.sendall(b'\x01')
        početno_stanje = EXACT_VALUE(udaljen_VALUE, 24); assert struct.unpack('>HH', početno_stanje[:4]) == (너비, 높이)
        EXACT_VALUE(udaljen_VALUE, struct.unpack('>I', početno_stanje[20:])[0])
        udaljen_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        udaljen_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        proveriti_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for događaj,_ in birač_a916db4e.select(.02):
                    podaci=događaj.fileobj.read(65536)
                    if podaci:LOG_snimi.extend(podaci)
        prozor=[12,48,568,360]
        def verifikovati_promeniti_veličinu():
            COLUMN_VALUE,ROW_VALUE=(prozor[2]-24)//8,(prozor[3]-56)//16
            SMS=ljuska('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in SMS,SMS
            # stvarni_podaci prozor 테두리: 단지 promeniti_veličinu upit_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            proveriti_piksel((prozor[0],prozor[1]),(32,80,144))
            crtež_VALUE=proveriti_piksel((prozor[0]+prozor[2]-1,prozor[1]+prozor[3]-1),(39,49,64))
            return crtež_VALUE
        def 모서리(방향):
            return (prozor[0]+(3 if 방향 in (1,3) else prozor[2]-4),prozor[1]+(3 if 방향<=2 else prozor[3]-4))
        def promeniti_veličinu_prevući(방향,차이,taster=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            proveriti_piksel(흰점,(255,255,255))
            가리키기(가,세,taster)
            끝가=max(0,min(너비-1,가+차이[0]));završiti_razgovor_vertikala=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,završiti_razgovor_vertikala,taster);가리키기(끝가,završiti_razgovor_vertikala,0);숨고르기()
            if taster==1:
                LEFT_VALUE,위,폭,길이=prozor;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+길이
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+završiti_razgovor_vertikala-세))
                else:아래=max(위+216,min(높이,아래+završiti_razgovor_vertikala-세))
                prozor[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        verifikovati_promeniti_veličinu();assert pokazivač_Skriveno[0]
        promeniti_veličinu_prevući(4,(-100,-60),4);verifikovati_promeniti_veličinu() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            promeniti_veličinu_prevući(방향,차이);verifikovati_promeniti_veličinu()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        poslati_SMS_poruku("echo '"+긴글+"'");숨고르기()
        promeniti_veličinu_prevući(4,(-1000,-1000));assert prozor[2:]==[360,216]
        promeniti_veličinu_prevući(4,(너비,높이))
        koristiti=poslati_SMS_poruku('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),koristiti);verifikovati_promeniti_veličinu()
        # vi가 Uredi_VALUE 중에 화면 크기를 pokušati_ponovo_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        ljuska('ftpd start')
        prenos_VALUE=ftplib.FTP();prenos_VALUE.encoding='utf-8';prenos_VALUE.connect('127.0.0.1',broj_porta,timeout=20);prenos_VALUE.login()
        기다리기(b'NORMAL',poslati_SMS_poruku('vi /크기자료.txt\n'))
        기다리기(b'INSERT',poslati_SMS_poruku('i미저장 한글 podaci\n'));숨고르기()
        promeniti_veličinu_prevući(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((prozor[3]-56)//16)).encode() in LOG_snimi[-4096:]
        poslati_SMS_poruku('작은 창에서도 이어 쓰기\n');숨고르기()
        promeniti_veličinu_prevući(4,(너비,높이))
        poslati_SMS_poruku('큰 창에서도 이어 쓰기\n');숨고르기()
        klik_taster(0xff1b);klik_taster(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',poslati_SMS_poruku(':wq\n'))
        Sadržaj_VALUE=bytearray();prenos_VALUE.retrbinary('RETR 크기자료.txt',Sadržaj_VALUE.extend)
        assert Sadržaj_VALUE=='미저장 한글 podaci\n작은 창에서도 이어 쓰기\n큰 창에서도 이어 쓰기\n'.encode(),Sadržaj_VALUE
        verifikovati_promeniti_veličinu().save(str(KR_putanja/(promeniti_veličinu_SMS+'-large.png')))
        # 두 번째 창은 podrazumevana_vrednost promeniti_veličinu, pokušati_ponovo_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        koristiti=len(LOG_snimi);klik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',koristiti)
        assert 'TERMINAL SIZE 68x19' in ljuska('terminal size')
        koristiti=len(LOG_snimi);klik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',koristiti);verifikovati_promeniti_veličinu()
        promeniti_veličinu_prevući(4,(-너비,-높이));verifikovati_promeniti_veličinu().save(str(KR_putanja/(promeniti_veličinu_SMS+'-small.png')))
        # promeniti_veličinu promeniti_VALUE NAZAD_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        koristiti=len(LOG_snimi);klik_VALUE(prozor[0]+prozor[2]-20,prozor[1]+15);기다리기(b'TERMINAL FOCUS 2',koristiti)
        assert 'RESIZE CLOSED' in ljuska('echo RESIZE CLOSED')
        print('PASS:',promeniti_veličinu_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if prenos_VALUE:prenos_VALUE.close()
        if udaljen_VALUE:udaljen_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
        birač_a916db4e.close();Proces_VALUE.stdout.close();(KR_putanja/(promeniti_veličinu_SMS+'.log')).write_bytes(LOG_snimi)


def koristiti():
    KR_putanja=radnja_koren/'build/verification/resize';KR_putanja.mkdir(parents=True,exist_ok=True)
    LOG_snimi={'passed':False,'kernel_sha256':hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_putanja);LOG_snimi['resolutions'].append([너비,높이])
        LOG_snimi.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_putanja/'report.json').write_text(json.dumps(LOG_snimi,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':koristiti()
