#!/usr/bin/env python3
"""skutočný_údaje QEMU/VNC에서 Terminál 모서리 presunúť_VALUE·ukazovateľ·동적 znak_VALUE 칸·úprava_VALUE obsah_VALUE 보존를 검사한다."""
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
from počítač_zobraziť import EXACT_VALUE
from Vykonať_príkaz import akcia_koreň


def 창크기시험(너비, výška_VALUE, KR_cesta):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); číslo_portu = 임시.getsockname()[1]
    zmeniť_veľkosť_SMS = '{}x{}'.format(너비, výška_VALUE)
    Proces_VALUE = subprocess.Popen(['python3', str(akcia_koreň/'Nástroje/Vykonať_príkaz.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(číslo_portu), '--resolution', zmeniť_veľkosť_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector(); selektor_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); vzdialený_VALUE = None; prenos_VALUE = None; ukazovateľ_Skryté=[False]

    def 기다리기(zobraziť_VALUE_487749b8, Spustiť_2=0):
        termín_VALUE = time.monotonic() + 60
        while zobraziť_VALUE_487749b8 not in LOG_RECORD[Spustiť_2:]:
            if time.monotonic() > termín_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Spustiť_2:].decode('utf-8', 'replace'))
            for Udalosť, _ in selektor_a916db4e.select(.1):
                údaje = Udalosť.fileobj.read(65536)
                if údaje: LOG_RECORD.extend(údaje)
        return LOG_RECORD[Spustiť_2:].decode('utf-8', 'replace')

    def kliknúť_tlačidlo(symbol, 눌림=True): vzdialený_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def odoslať_SMS_správu(Spracovanie_textu):
        Spustiť_2 = len(LOG_RECORD)
        for znak_VALUE in Spracovanie_textu:
            symbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            kliknúť_tlačidlo(symbol); kliknúť_tlačidlo(symbol, False)
        return Spustiť_2

    def 셸(Spracovanie_textu): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', odoslať_SMS_správu(Spracovanie_textu+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, vertikála_pozícia, 눌림): vzdialený_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikála_pozícia))

    def kliknúť_VALUE(가로, vertikála_pozícia): 가리키기(가로, vertikála_pozícia, 1); 가리키기(가로, vertikála_pozícia, 0)

    def bitová_mapa_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 skutočný_údaje 너비를 쓴다.
        vzdialený_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, výška_VALUE))
        kresba_VALUE = Image.new('RGB', (너비, výška_VALUE)); oblasť_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(vzdialený_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                dĺžka_VALUE = struct.unpack('>I', EXACT_VALUE(vzdialený_VALUE, 7)[3:])[0]; EXACT_VALUE(vzdialený_VALUE, dĺžka_VALUE); continue
            assert 종류 == 0, 종류
            položka_COUNT = struct.unpack('>H', EXACT_VALUE(vzdialený_VALUE, 3)[1:])[0]
            for _ in range(položka_COUNT):
                가로, vertikála_pozícia, 폭, dĺžka_VALUE, kódovanie_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(vzdialený_VALUE, 12))
                if kódovanie_VALUE == -239:
                    assert 폭==0 and dĺžka_VALUE==0, 'remote cursor must be hidden'
                    ukazovateľ_Skryté[0]=True
                    continue
                assert kódovanie_VALUE == 0 and 가로+폭 <= 너비 and vertikála_pozícia+dĺžka_VALUE <= výška_VALUE
                kresba_VALUE.paste(Image.frombytes('RGB', (폭, dĺžka_VALUE), EXACT_VALUE(vzdialený_VALUE, 폭*dĺžka_VALUE*4), 'raw', 'BGRX'), (가로, vertikála_pozícia))
                oblasť_VALUE_9285603e += 폭*dĺžka_VALUE
            if oblasť_VALUE_9285603e:
                assert oblasť_VALUE_9285603e == 너비*výška_VALUE, oblasť_VALUE_9285603e
                return kresba_VALUE

    def skontrolovať_pixel(súradnica_VALUE, 색):
        termín_VALUE = time.monotonic()+10
        while True:
            kresba_VALUE = bitová_mapa_IMAGE()
            if kresba_VALUE.getpixel(súradnica_VALUE) == 색: return kresba_VALUE
            if time.monotonic() > termín_VALUE: raise AssertionError((súradnica_VALUE, kresba_VALUE.getpixel(súradnica_VALUE), 색))

    def nahrať_Súbory(Názov, údaje): prenos_VALUE.storbinary('STOR '+Názov, io.BytesIO(údaje))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+zmeniť_veľkosť_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', zmeniť_veľkosť_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        vzdialený_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(vzdialený_VALUE, 12) == b'RFB 003.008\n'; vzdialený_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(vzdialený_VALUE, EXACT_VALUE(vzdialený_VALUE, 1)[0]); vzdialený_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(vzdialený_VALUE, 4) == b'\0'*4; vzdialený_VALUE.sendall(b'\x01')
        počiatočný_stav = EXACT_VALUE(vzdialený_VALUE, 24); assert struct.unpack('>HH', počiatočný_stav[:4]) == (너비, výška_VALUE)
        EXACT_VALUE(vzdialený_VALUE, struct.unpack('>I', počiatočný_stav[20:])[0])
        vzdialený_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        vzdialený_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        skontrolovať_pixel((너비-1, výška_VALUE-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Udalosť,_ in selektor_a916db4e.select(.02):
                    údaje=Udalosť.fileobj.read(65536)
                    if údaje:LOG_RECORD.extend(údaje)
        Okno=[12,48,568,360]
        def overiť_zmeniť_veľkosť():
            COLUMN_VALUE,ROW_VALUE=(Okno[2]-24)//8,(Okno[3]-56)//16
            Spracovanie_textu=셸('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Spracovanie_textu,Spracovanie_textu
            # skutočný_údaje Okno 테두리: 단지 Veľkosť dotaz_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            skontrolovať_pixel((Okno[0],Okno[1]),(32,80,144))
            kresba_VALUE=skontrolovať_pixel((Okno[0]+Okno[2]-1,Okno[1]+Okno[3]-1),(39,49,64))
            return kresba_VALUE
        def 모서리(방향):
            return (Okno[0]+(3 if 방향 in (1,3) else Okno[2]-4),Okno[1]+(3 if 방향<=2 else Okno[3]-4))
        def zmeniť_veľkosť_presunúť(방향,차이,Tlačidlo=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            skontrolovať_pixel(흰점,(255,255,255))
            가리키기(가,세,Tlačidlo)
            끝가=max(0,min(너비-1,가+차이[0]));ukončiť_hovor_vertikála=max(0,min(výška_VALUE-1,세+차이[1]))
            가리키기(끝가,ukončiť_hovor_vertikála,Tlačidlo);가리키기(끝가,ukončiť_hovor_vertikála,0);숨고르기()
            if Tlačidlo==1:
                LEFT_VALUE,위,폭,dĺžka_VALUE=Okno;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+dĺžka_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ukončiť_hovor_vertikála-세))
                else:아래=max(위+216,min(výška_VALUE,아래+ukončiť_hovor_vertikála-세))
                Okno[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        overiť_zmeniť_veľkosť();assert ukazovateľ_Skryté[0]
        zmeniť_veľkosť_presunúť(4,(-100,-60),4);overiť_zmeniť_veľkosť() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            zmeniť_veľkosť_presunúť(방향,차이);overiť_zmeniť_veľkosť()
        # vstup_VALUE 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        odoslať_SMS_správu("echo '"+긴글+"'");숨고르기()
        zmeniť_veľkosť_presunúť(4,(-1000,-1000));assert Okno[2:]==[360,216]
        zmeniť_veľkosť_presunúť(4,(너비,výška_VALUE))
        Spustiť_2=odoslať_SMS_správu('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Spustiť_2);overiť_zmeniť_veľkosť()
        # vi가 úprava_VALUE 중에 화면 크기를 skúsiť_znova_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        셸('ftpd start')
        prenos_VALUE=ftplib.FTP();prenos_VALUE.encoding='utf-8';prenos_VALUE.connect('127.0.0.1',číslo_portu,timeout=20);prenos_VALUE.login()
        기다리기(b'NORMAL',odoslať_SMS_správu('vi /크기자료.txt\n'))
        기다리기(b'INSERT',odoslať_SMS_správu('i미저장 한글 údaje\n'));숨고르기()
        zmeniť_veľkosť_presunúť(4,(-너비,-výška_VALUE))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Okno[3]-56)//16)).encode() in LOG_RECORD[-4096:]
        odoslať_SMS_správu('작은 창에서도 이어 Zápis\n');숨고르기()
        zmeniť_veľkosť_presunúť(4,(너비,výška_VALUE))
        odoslať_SMS_správu('큰 창에서도 이어 Zápis\n');숨고르기()
        kliknúť_tlačidlo(0xff1b);kliknúť_tlačidlo(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',odoslať_SMS_správu(':wq\n'))
        obsah_VALUE=bytearray();prenos_VALUE.retrbinary('RETR 크기자료.txt',obsah_VALUE.extend)
        assert obsah_VALUE=='미저장 한글 údaje\n작은 창에서도 이어 Zápis\n큰 창에서도 이어 Zápis\n'.encode(),obsah_VALUE
        overiť_zmeniť_veľkosť().save(str(KR_cesta/(zmeniť_veľkosť_SMS+'-large.png')))
        # 두 번째 창은 predvolená_hodnota Veľkosť, skúsiť_znova_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Spustiť_2=len(LOG_RECORD);kliknúť_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Spustiť_2)
        assert 'TERMINAL SIZE 68x19' in 셸('terminal size')
        Spustiť_2=len(LOG_RECORD);kliknúť_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Spustiť_2);overiť_zmeniť_veľkosť()
        zmeniť_veľkosť_presunúť(4,(-너비,-výška_VALUE));overiť_zmeniť_veľkosť().save(str(KR_cesta/(zmeniť_veľkosť_SMS+'-small.png')))
        # Veľkosť zmeniť_VALUE BACK_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Spustiť_2=len(LOG_RECORD);kliknúť_VALUE(Okno[0]+Okno[2]-20,Okno[1]+15);기다리기(b'TERMINAL FOCUS 2',Spustiť_2)
        assert 'RESIZE CLOSED' in 셸('echo RESIZE CLOSED')
        print('PASS:',zmeniť_veľkosť_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if prenos_VALUE:prenos_VALUE.close()
        if vzdialený_VALUE:vzdialený_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
        selektor_a916db4e.close();Proces_VALUE.stdout.close();(KR_cesta/(zmeniť_veľkosť_SMS+'.log')).write_bytes(LOG_RECORD)


def Spustiť_2():
    KR_cesta=akcia_koreň/'build/verification/resize';KR_cesta.mkdir(parents=True,exist_ok=True)
    LOG_RECORD={'passed':False,'kernel_sha256':hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,výška_VALUE in ((640,480),(1920,1080)):
            창크기시험(너비,výška_VALUE,KR_cesta);LOG_RECORD['resolutions'].append([너비,výška_VALUE])
        LOG_RECORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_cesta/'report.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Spustiť_2()
