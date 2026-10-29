#!/usr/bin/env python3
"""skutečný_data QEMU/VNC에서 interpret_příkazů 모서리 přetáhnout_HODNOTA·ukazatel·동적 znak_HODNOTA přihrádka_položka·úprava_HODNOTA Obsah_HODNOTA 보존를 검사한다."""
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
from Plocha_pohled import STEJNÉ_HODNOTA
from Provést_příkaz import akce_kořen


def test_okno_změna_velikosti(너비, výška_HODNOTA, KV_cesta):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); číslo_portu = 임시.getsockname()[1]
    změnit_velikost_SMS = '{}x{}'.format(너비, výška_HODNOTA)
    Proces_HODNOTA = subprocess.Popen(['python3', str(akce_kořen/'nástroje/Provést_příkaz.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(číslo_portu), '--resolution', změnit_velikost_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector(); selektor_a916db4e.register(Proces_HODNOTA.stdout, selectors.EVENT_READ)
    LOGZ_ZÁZNAM = bytearray(); vzdálený_HODNOTA = None; přenos_HODNOTA = None; ukazatel_Skrytý=[False]

    def 기다리기(zobrazit_HODNOTA, Spustit_2=0):
        konečný_termín_HODNOTA = time.monotonic() + 60
        while zobrazit_HODNOTA not in LOGZ_ZÁZNAM[Spustit_2:]:
            if time.monotonic() > konečný_termín_HODNOTA or Proces_HODNOTA.poll() is not None or b'HALTED' in LOGZ_ZÁZNAM or b'PANIC:' in LOGZ_ZÁZNAM:
                raise AssertionError(LOGZ_ZÁZNAM[Spustit_2:].decode('utf-8', 'replace'))
            for Události, _ in selektor_a916db4e.select(.1):
                data = Události.fileobj.read(65536)
                if data: LOGZ_ZÁZNAM.extend(data)
        return LOGZ_ZÁZNAM[Spustit_2:].decode('utf-8', 'replace')

    def klepnout_tlačítko(symbol, 눌림=True): vzdálený_HODNOTA.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def poslat_SMS(text):
        Spustit_2 = len(LOGZ_ZÁZNAM)
        for znak_HODNOTA in text:
            symbol = 0xff0d if znak_HODNOTA == '\n' else ord(znak_HODNOTA) if ord(znak_HODNOTA) < 256 else 0x1000000 | ord(znak_HODNOTA)
            klepnout_tlačítko(symbol); klepnout_tlačítko(symbol, False)
        return Spustit_2

    def prostředí(text): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', poslat_SMS(text+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Svislá_pozice, 눌림): vzdálený_HODNOTA.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Svislá_pozice))

    def klepnout_HODNOTA(가로, Svislá_pozice): 가리키기(가로, Svislá_pozice, 1); 가리키기(가로, Svislá_pozice, 0)

    def rastrový_obrázek_image():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 skutečný_data 너비를 쓴다.
        vzdálený_HODNOTA.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, výška_HODNOTA))
        kreslení_HODNOTA = Image.new('RGB', (너비, výška_HODNOTA)); oblast_HODNOTA_9285603e = 0
        while True:
            Druh_HODNOTA = STEJNÉ_HODNOTA(vzdálený_HODNOTA, 1)[0]
            if Druh_HODNOTA == 2: continue
            if Druh_HODNOTA == 3:
                délka_HODNOTA = struct.unpack('>I', STEJNÉ_HODNOTA(vzdálený_HODNOTA, 7)[3:])[0]; STEJNÉ_HODNOTA(vzdálený_HODNOTA, délka_HODNOTA); continue
            assert Druh_HODNOTA == 0, Druh_HODNOTA
            zboží_POČET = struct.unpack('>H', STEJNÉ_HODNOTA(vzdálený_HODNOTA, 3)[1:])[0]
            for _ in range(zboží_POČET):
                가로, Svislá_pozice, 폭, délka_HODNOTA, Encoding_HODNOTA = struct.unpack('>HHHHi', STEJNÉ_HODNOTA(vzdálený_HODNOTA, 12))
                if Encoding_HODNOTA == -239:
                    assert 폭==0 and délka_HODNOTA==0, 'remote cursor must be hidden'
                    ukazatel_Skrytý[0]=True
                    continue
                assert Encoding_HODNOTA == 0 and 가로+폭 <= 너비 and Svislá_pozice+délka_HODNOTA <= výška_HODNOTA
                kreslení_HODNOTA.paste(Image.frombytes('RGB', (폭, délka_HODNOTA), STEJNÉ_HODNOTA(vzdálený_HODNOTA, 폭*délka_HODNOTA*4), 'raw', 'BGRX'), (가로, Svislá_pozice))
                oblast_HODNOTA_9285603e += 폭*délka_HODNOTA
            if oblast_HODNOTA_9285603e:
                assert oblast_HODNOTA_9285603e == 너비*výška_HODNOTA, oblast_HODNOTA_9285603e
                return kreslení_HODNOTA

    def šek_pixel(souřadnice_HODNOTA, 색):
        konečný_termín_HODNOTA = time.monotonic()+10
        while True:
            kreslení_HODNOTA = rastrový_obrázek_image()
            if kreslení_HODNOTA.getpixel(souřadnice_HODNOTA) == 색: return kreslení_HODNOTA
            if time.monotonic() > konečný_termín_HODNOTA: raise AssertionError((souřadnice_HODNOTA, kreslení_HODNOTA.getpixel(souřadnice_HODNOTA), 색))

    def Upload_Files(Název, data): přenos_HODNOTA.storbinary('STOR '+Název, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+změnit_velikost_SMS+' RGB32').encode() in LOGZ_ZÁZNAM
        print('BOOT:', změnit_velikost_SMS, flush=True)
        vzdálený_číslo = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOGZ_ZÁZNAM).group(1))
        vzdálený_HODNOTA = socket.create_connection(('127.0.0.1', vzdálený_číslo), timeout=20)
        assert STEJNÉ_HODNOTA(vzdálený_HODNOTA, 12) == b'RFB 003.008\n'; vzdálený_HODNOTA.sendall(b'RFB 003.008\n')
        assert 1 in STEJNÉ_HODNOTA(vzdálený_HODNOTA, STEJNÉ_HODNOTA(vzdálený_HODNOTA, 1)[0]); vzdálený_HODNOTA.sendall(b'\x01')
        assert STEJNÉ_HODNOTA(vzdálený_HODNOTA, 4) == b'\0'*4; vzdálený_HODNOTA.sendall(b'\x01')
        počáteční_stav = STEJNÉ_HODNOTA(vzdálený_HODNOTA, 24); assert struct.unpack('>HH', počáteční_stav[:4]) == (너비, výška_HODNOTA)
        STEJNÉ_HODNOTA(vzdálený_HODNOTA, struct.unpack('>I', počáteční_stav[20:])[0])
        vzdálený_HODNOTA.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        vzdálený_HODNOTA.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        šek_pixel((너비-1, výška_HODNOTA-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Události,_ in selektor_a916db4e.select(.02):
                    data=Události.fileobj.read(65536)
                    if data:LOGZ_ZÁZNAM.extend(data)
        Okno=[12,48,568,360]
        def ověřit_změnit_velikost():
            SLOUPEC_HODNOTA,ŘÁDEK_HODNOTA=(Okno[2]-24)//8,(Okno[3]-56)//16
            text=prostředí('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(SLOUPEC_HODNOTA,ŘÁDEK_HODNOTA) in text,text
            # skutečný_data Okno 테두리: 단지 Velikost dotaz_HODNOTA 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            šek_pixel((Okno[0],Okno[1]),(32,80,144))
            kreslení_HODNOTA=šek_pixel((Okno[0]+Okno[2]-1,Okno[1]+Okno[3]-1),(39,49,64))
            return kreslení_HODNOTA
        def 모서리(방향):
            return (Okno[0]+(3 if 방향 in (1,3) else Okno[2]-4),Okno[1]+(3 if 방향<=2 else Okno[3]-4))
        def změnit_velikost_přetáhnout(방향,차이,tlačítko=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            šek_pixel(흰점,(255,255,255))
            가리키기(가,세,tlačítko)
            끝가=max(0,min(너비-1,가+차이[0]));konec_Svislá=max(0,min(výška_HODNOTA-1,세+차이[1]))
            가리키기(끝가,konec_Svislá,tlačítko);가리키기(끝가,konec_Svislá,0);숨고르기()
            if tlačítko==1:
                ZLEVA_HODNOTA,위,폭,délka_HODNOTA=Okno;právo_HODNOTA,아래=ZLEVA_HODNOTA+폭,위+délka_HODNOTA
                if 방향 in (1,3):ZLEVA_HODNOTA=max(0,min(právo_HODNOTA-360,ZLEVA_HODNOTA+끝가-가))
                else:právo_HODNOTA=max(ZLEVA_HODNOTA+360,min(너비,právo_HODNOTA+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+konec_Svislá-세))
                else:아래=max(위+216,min(výška_HODNOTA,아래+konec_Svislá-세))
                Okno[:]=[ZLEVA_HODNOTA,위,právo_HODNOTA-ZLEVA_HODNOTA,아래-위]
        ověřit_změnit_velikost();assert ukazatel_Skrytý[0]
        změnit_velikost_přetáhnout(4,(-100,-60),4);ověřit_změnit_velikost() # právo 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            změnit_velikost_přetáhnout(방향,차이);ověřit_změnit_velikost()
        # vstup_HODNOTA 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        poslat_SMS("echo '"+긴글+"'");숨고르기()
        změnit_velikost_přetáhnout(4,(-1000,-1000));assert Okno[2:]==[360,216]
        změnit_velikost_přetáhnout(4,(너비,výška_HODNOTA))
        Spustit_2=poslat_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Spustit_2);ověřit_změnit_velikost()
        # vi가 úprava_HODNOTA 중에 화면 크기를 zkusit_znovu_HODNOTA 읽고, 저장하지 않은 한글도 유지한다.
        prostředí('ftpd start')
        přenos_HODNOTA=ftplib.FTP();přenos_HODNOTA.encoding='utf-8';přenos_HODNOTA.connect('127.0.0.1',číslo_portu,timeout=20);přenos_HODNOTA.login()
        기다리기(b'NORMAL',poslat_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',poslat_SMS('i미저장 한글 data\n'));숨고르기()
        změnit_velikost_přetáhnout(4,(-너비,-výška_HODNOTA))
        # ANSI ŘÁDEK_HODNOTA 이동에 새 ŘÁDEK_HODNOTA 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Okno[3]-56)//16)).encode() in LOGZ_ZÁZNAM[-4096:]
        poslat_SMS('작은 창에서도 이어 Zápis\n');숨고르기()
        změnit_velikost_přetáhnout(4,(너비,výška_HODNOTA))
        poslat_SMS('큰 창에서도 이어 Zápis\n');숨고르기()
        klepnout_tlačítko(0xff1b);klepnout_tlačítko(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',poslat_SMS(':wq\n'))
        Obsah_HODNOTA=bytearray();přenos_HODNOTA.retrbinary('RETR 크기자료.txt',Obsah_HODNOTA.extend)
        assert Obsah_HODNOTA=='미저장 한글 data\n작은 창에서도 이어 Zápis\n큰 창에서도 이어 Zápis\n'.encode(),Obsah_HODNOTA
        ověřit_změnit_velikost().save(str(KV_cesta/(změnit_velikost_SMS+'-large.png')))
        # 두 번째 창은 výchozí_hodnota Velikost, zkusit_znovu_HODNOTA 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Spustit_2=len(LOGZ_ZÁZNAM);klepnout_HODNOTA(70,16);기다리기(b'TERMINAL FOCUS 2',Spustit_2)
        assert 'TERMINAL SIZE 68x19' in prostředí('terminal size')
        Spustit_2=len(LOGZ_ZÁZNAM);klepnout_HODNOTA(180,16);기다리기(b'TERMINAL FOCUS 1',Spustit_2);ověřit_změnit_velikost()
        změnit_velikost_přetáhnout(4,(-너비,-výška_HODNOTA));ověřit_změnit_velikost().save(str(KV_cesta/(změnit_velikost_SMS+'-small.png')))
        # Velikost změnit_HODNOTA BACK_HODNOTA X 닫기도 새로운 právo 가장자리를 사용한다.
        Spustit_2=len(LOGZ_ZÁZNAM);klepnout_HODNOTA(Okno[0]+Okno[2]-20,Okno[1]+15);기다리기(b'TERMINAL FOCUS 2',Spustit_2)
        assert 'RESIZE CLOSED' in prostředí('echo RESIZE CLOSED')
        print('PASS:',změnit_velikost_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if přenos_HODNOTA:přenos_HODNOTA.close()
        if vzdálený_HODNOTA:vzdálený_HODNOTA.close()
        if Proces_HODNOTA.poll() is None:
            Proces_HODNOTA.terminate()
            try:Proces_HODNOTA.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_HODNOTA.kill();Proces_HODNOTA.wait()
        selektor_a916db4e.close();Proces_HODNOTA.stdout.close();(KV_cesta/(změnit_velikost_SMS+'.log')).write_bytes(LOGZ_ZÁZNAM)


def Spustit_2():
    KV_cesta=akce_kořen/'build/verification/resize';KV_cesta.mkdir(parents=True,exist_ok=True)
    LOGZ_ZÁZNAM={'passed':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,výška_HODNOTA in ((640,480),(1920,1080)):
            test_okno_změna_velikosti(너비,výška_HODNOTA,KV_cesta);LOGZ_ZÁZNAM['resolutions'].append([너비,výška_HODNOTA])
        LOGZ_ZÁZNAM.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KV_cesta/'report.json').write_text(json.dumps(LOGZ_ZÁZNAM,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Spustit_2()
