#!/usr/bin/env python3
"""stvaran_podaci QEMU/VNC에서 Terminal 모서리 vući_VALUE·pokazivač·동적 znak_VALUE 칸·Uredi_VALUE Sadržaj_VALUE 보존를 검사한다."""
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
from stolni_Prikaz import EXACT_VALUE
from Izvrši_naredba import akcija_korijen


def 창크기시험(너비, 높이, KR_put):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); broj_priključka = 임시.getsockname()[1]
    promijeniti_veličinu_SMS = '{}x{}'.format(너비, 높이)
    Proces_VALUE = subprocess.Popen(['python3', str(akcija_korijen/'Alati/Izvrši_naredba.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(broj_priključka), '--resolution', promijeniti_veličinu_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    odabirač_a916db4e = selectors.DefaultSelector(); odabirač_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_zapis = bytearray(); udaljeno_VALUE = None; Prijenos_VALUE = None; pokazivač_sakriven=[False]

    def 기다리기(emisija_VALUE, Pokreni=0):
        rok_za_dovršetak_VALUE = time.monotonic() + 60
        while emisija_VALUE not in LOG_zapis[Pokreni:]:
            if time.monotonic() > rok_za_dovršetak_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_zapis or b'PANIC:' in LOG_zapis:
                raise AssertionError(LOG_zapis[Pokreni:].decode('utf-8', 'replace'))
            for Događaj, _ in odabirač_a916db4e.select(.1):
                podaci = Događaj.fileobj.read(65536)
                if podaci: LOG_zapis.extend(podaci)
        return LOG_zapis[Pokreni:].decode('utf-8', 'replace')

    def klik_tipka(simbol, 눌림=True): udaljeno_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def slanje_SMS_a(Tekst):
        Pokreni = len(LOG_zapis)
        for znak_VALUE in Tekst:
            simbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            klik_tipka(simbol); klik_tipka(simbol, False)
        return Pokreni

    def ljuska(Tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', slanje_SMS_a(Tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Okomito_položaj, 눌림): udaljeno_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Okomito_položaj))

    def klik_VALUE(가로, Okomito_položaj): 가리키기(가로, Okomito_položaj, 1); 가리키기(가로, Okomito_položaj, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 stvaran_podaci 너비를 쓴다.
        udaljeno_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        crtež_VALUE = Image.new('RGB', (너비, 높이)); područje_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(udaljeno_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(udaljeno_VALUE, 7)[3:])[0]; EXACT_VALUE(udaljeno_VALUE, 길이); continue
            assert 종류 == 0, 종류
            artikl_COUNT = struct.unpack('>H', EXACT_VALUE(udaljeno_VALUE, 3)[1:])[0]
            for _ in range(artikl_COUNT):
                가로, Okomito_položaj, 폭, 길이, šifriranje_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(udaljeno_VALUE, 12))
                if šifriranje_VALUE == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    pokazivač_sakriven[0]=True
                    continue
                assert šifriranje_VALUE == 0 and 가로+폭 <= 너비 and Okomito_položaj+길이 <= 높이
                crtež_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(udaljeno_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, Okomito_položaj))
                područje_VALUE_9285603e += 폭*길이
            if područje_VALUE_9285603e:
                assert područje_VALUE_9285603e == 너비*높이, područje_VALUE_9285603e
                return crtež_VALUE

    def 화소확인(좌표, 색):
        rok_za_dovršetak_VALUE = time.monotonic()+10
        while True:
            crtež_VALUE = bitmap_IMAGE()
            if crtež_VALUE.getpixel(좌표) == 색: return crtež_VALUE
            if time.monotonic() > rok_za_dovršetak_VALUE: raise AssertionError((좌표, crtež_VALUE.getpixel(좌표), 색))

    def Prijenos_Datoteke(Ime, podaci): Prijenos_VALUE.storbinary('STOR '+Ime, io.BytesIO(podaci))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+promijeniti_veličinu_SMS+' RGB32').encode() in LOG_zapis
        print('BOOT:', promijeniti_veličinu_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_zapis).group(1))
        udaljeno_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(udaljeno_VALUE, 12) == b'RFB 003.008\n'; udaljeno_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(udaljeno_VALUE, EXACT_VALUE(udaljeno_VALUE, 1)[0]); udaljeno_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(udaljeno_VALUE, 4) == b'\0'*4; udaljeno_VALUE.sendall(b'\x01')
        početno_stanje = EXACT_VALUE(udaljeno_VALUE, 24); assert struct.unpack('>HH', početno_stanje[:4]) == (너비, 높이)
        EXACT_VALUE(udaljeno_VALUE, struct.unpack('>I', početno_stanje[20:])[0])
        udaljeno_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        udaljeno_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        화소확인((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Događaj,_ in odabirač_a916db4e.select(.02):
                    podaci=Događaj.fileobj.read(65536)
                    if podaci:LOG_zapis.extend(podaci)
        Prozor=[12,48,568,360]
        def provjeriti_promijeniti_veličinu():
            COLUMN_VALUE,ROW_VALUE=(Prozor[2]-24)//8,(Prozor[3]-56)//16
            Tekst=ljuska('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Tekst,Tekst
            # stvaran_podaci Prozor 테두리: 단지 Veličina upit_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            화소확인((Prozor[0],Prozor[1]),(32,80,144))
            crtež_VALUE=화소확인((Prozor[0]+Prozor[2]-1,Prozor[1]+Prozor[3]-1),(39,49,64))
            return crtež_VALUE
        def 모서리(방향):
            return (Prozor[0]+(3 if 방향 in (1,3) else Prozor[2]-4),Prozor[1]+(3 if 방향<=2 else Prozor[3]-4))
        def promijeniti_veličinu_vući(방향,차이,gumb=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            화소확인(흰점,(255,255,255))
            가리키기(가,세,gumb)
            끝가=max(0,min(너비-1,가+차이[0]));završiti_razgovor_Okomito=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,završiti_razgovor_Okomito,gumb);가리키기(끝가,završiti_razgovor_Okomito,0);숨고르기()
            if gumb==1:
                LEFT_VALUE,위,폭,길이=Prozor;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+길이
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+završiti_razgovor_Okomito-세))
                else:아래=max(위+216,min(높이,아래+završiti_razgovor_Okomito-세))
                Prozor[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        provjeriti_promijeniti_veličinu();assert pokazivač_sakriven[0]
        promijeniti_veličinu_vući(4,(-100,-60),4);provjeriti_promijeniti_veličinu() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            promijeniti_veličinu_vući(방향,차이);provjeriti_promijeniti_veličinu()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        slanje_SMS_a("echo '"+긴글+"'");숨고르기()
        promijeniti_veličinu_vući(4,(-1000,-1000));assert Prozor[2:]==[360,216]
        promijeniti_veličinu_vući(4,(너비,높이))
        Pokreni=slanje_SMS_a('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Pokreni);provjeriti_promijeniti_veličinu()
        # vi가 Uredi_VALUE 중에 화면 크기를 pokušati_ponovno_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        ljuska('ftpd start')
        Prijenos_VALUE=ftplib.FTP();Prijenos_VALUE.encoding='utf-8';Prijenos_VALUE.connect('127.0.0.1',broj_priključka,timeout=20);Prijenos_VALUE.login()
        기다리기(b'NORMAL',slanje_SMS_a('vi /크기자료.txt\n'))
        기다리기(b'INSERT',slanje_SMS_a('i미저장 한글 podaci\n'));숨고르기()
        promijeniti_veličinu_vući(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Prozor[3]-56)//16)).encode() in LOG_zapis[-4096:]
        slanje_SMS_a('작은 창에서도 이어 Zapisuj\n');숨고르기()
        promijeniti_veličinu_vući(4,(너비,높이))
        slanje_SMS_a('큰 창에서도 이어 Zapisuj\n');숨고르기()
        klik_tipka(0xff1b);klik_tipka(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',slanje_SMS_a(':wq\n'))
        Sadržaj_VALUE=bytearray();Prijenos_VALUE.retrbinary('RETR 크기자료.txt',Sadržaj_VALUE.extend)
        assert Sadržaj_VALUE=='미저장 한글 podaci\n작은 창에서도 이어 Zapisuj\n큰 창에서도 이어 Zapisuj\n'.encode(),Sadržaj_VALUE
        provjeriti_promijeniti_veličinu().save(str(KR_put/(promijeniti_veličinu_SMS+'-large.png')))
        # 두 번째 창은 zadana_vrijednost Veličina, pokušati_ponovno_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Pokreni=len(LOG_zapis);klik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Pokreni)
        assert 'TERMINAL SIZE 68x19' in ljuska('terminal size')
        Pokreni=len(LOG_zapis);klik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Pokreni);provjeriti_promijeniti_veličinu()
        promijeniti_veličinu_vući(4,(-너비,-높이));provjeriti_promijeniti_veličinu().save(str(KR_put/(promijeniti_veličinu_SMS+'-small.png')))
        # Veličina promijeniti_VALUE TRAG_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Pokreni=len(LOG_zapis);klik_VALUE(Prozor[0]+Prozor[2]-20,Prozor[1]+15);기다리기(b'TERMINAL FOCUS 2',Pokreni)
        assert 'RESIZE CLOSED' in ljuska('echo RESIZE CLOSED')
        print('PASS:',promijeniti_veličinu_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Prijenos_VALUE:Prijenos_VALUE.close()
        if udaljeno_VALUE:udaljeno_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
        odabirač_a916db4e.close();Proces_VALUE.stdout.close();(KR_put/(promijeniti_veličinu_SMS+'.log')).write_bytes(LOG_zapis)


def Pokreni():
    KR_put=akcija_korijen/'build/verification/resize';KR_put.mkdir(parents=True,exist_ok=True)
    LOG_zapis={'passed':False,'kernel_sha256':hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_put);LOG_zapis['resolutions'].append([너비,높이])
        LOG_zapis.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_put/'report.json').write_text(json.dumps(LOG_zapis,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Pokreni()
