#!/usr/bin/env python3
"""stvaran_podaci QEMU/VNC에서 Terminal 모서리 prevući_VALUE·pokazivač·동적 znak_VALUE prostor_za_unos_unos·uređivati_VALUE Sadržaj_VALUE 보존를 검사한다."""
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
from Izvrši_komanda import projicirati_koijen


def 창크기시험(너비, 높이, mjera_put):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); broj_priključka = 임시.getsockname()[1]
    podesiti_veličinu_SMS = '{}x{}'.format(너비, 높이)
    proces_VALUE = subprocess.Popen(['python3', str(projicirati_koijen/'Alati/Izvrši_komanda.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(broj_priključka), '--resolution', podesiti_veličinu_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    birač_a916db4e = selectors.DefaultSelector(); birač_a916db4e.register(proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_red = bytearray(); udaljeno_VALUE = None; prijenos_VALUE = None; pokazivač_Skriveno=[False]

    def 기다리기(program_VALUE, Pokreni=0):
        마감 = time.monotonic() + 60
        while program_VALUE not in LOG_red[Pokreni:]:
            if time.monotonic() > 마감 or proces_VALUE.poll() is not None or b'HALTED' in LOG_red or b'PANIC:' in LOG_red:
                raise AssertionError(LOG_red[Pokreni:].decode('utf-8', 'replace'))
            for događaj, _ in birač_a916db4e.select(.1):
                podaci = događaj.fileobj.read(65536)
                if podaci: LOG_red.extend(podaci)
        return LOG_red[Pokreni:].decode('utf-8', 'replace')

    def klik_dugme(simbol, 눌림=True): udaljeno_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def slati_SMS(Tekst):
        Pokreni = len(LOG_red)
        for znak_VALUE in Tekst:
            simbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            klik_dugme(simbol); klik_dugme(simbol, False)
        return Pokreni

    def ljuska(Tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', slati_SMS(Tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertikalno_položaj, 눌림): udaljeno_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikalno_položaj))

    def klik_VALUE(가로, Vertikalno_položaj): 가리키기(가로, Vertikalno_položaj, 1); 가리키기(가로, Vertikalno_položaj, 0)

    def rasterska_slika_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 stvaran_podaci 너비를 쓴다.
        udaljeno_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ucrtavanje_VALUE = Image.new('RGB', (너비, 높이)); oblast_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(udaljeno_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                dužina_VALUE = struct.unpack('>I', EXACT_VALUE(udaljeno_VALUE, 7)[3:])[0]; EXACT_VALUE(udaljeno_VALUE, dužina_VALUE); continue
            assert 종류 == 0, 종류
            stavka_COUNT = struct.unpack('>H', EXACT_VALUE(udaljeno_VALUE, 3)[1:])[0]
            for _ in range(stavka_COUNT):
                가로, Vertikalno_položaj, 폭, dužina_VALUE, kodiranje_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(udaljeno_VALUE, 12))
                if kodiranje_VALUE == -239:
                    assert 폭==0 and dužina_VALUE==0, 'remote cursor must be hidden'
                    pokazivač_Skriveno[0]=True
                    continue
                assert kodiranje_VALUE == 0 and 가로+폭 <= 너비 and Vertikalno_položaj+dužina_VALUE <= 높이
                ucrtavanje_VALUE.paste(Image.frombytes('RGB', (폭, dužina_VALUE), EXACT_VALUE(udaljeno_VALUE, 폭*dužina_VALUE*4), 'raw', 'BGRX'), (가로, Vertikalno_položaj))
                oblast_VALUE_9285603e += 폭*dužina_VALUE
            if oblast_VALUE_9285603e:
                assert oblast_VALUE_9285603e == 너비*높이, oblast_VALUE_9285603e
                return ucrtavanje_VALUE

    def ček_pel(koordinata_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            ucrtavanje_VALUE = rasterska_slika_IMAGE()
            if ucrtavanje_VALUE.getpixel(koordinata_VALUE) == 색: return ucrtavanje_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinata_VALUE, ucrtavanje_VALUE.getpixel(koordinata_VALUE), 색))

    def Upload_Fajlovi(Naziv, podaci): prijenos_VALUE.storbinary('STOR '+Naziv, io.BytesIO(podaci))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+podesiti_veličinu_SMS+' RGB32').encode() in LOG_red
        print('BOOT:', podesiti_veličinu_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_red).group(1))
        udaljeno_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(udaljeno_VALUE, 12) == b'RFB 003.008\n'; udaljeno_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(udaljeno_VALUE, EXACT_VALUE(udaljeno_VALUE, 1)[0]); udaljeno_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(udaljeno_VALUE, 4) == b'\0'*4; udaljeno_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(udaljeno_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(udaljeno_VALUE, struct.unpack('>I', 초기[20:])[0])
        udaljeno_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        udaljeno_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ček_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for događaj,_ in birač_a916db4e.select(.02):
                    podaci=događaj.fileobj.read(65536)
                    if podaci:LOG_red.extend(podaci)
        prozor=[12,48,568,360]
        def potvrditi_podesiti_veličinu():
            COLUMN_VALUE,ROW_VALUE=(prozor[2]-24)//8,(prozor[3]-56)//16
            Tekst=ljuska('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Tekst,Tekst
            # stvaran_podaci prozor 테두리: 단지 Veličina upit_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ček_pel((prozor[0],prozor[1]),(32,80,144))
            ucrtavanje_VALUE=ček_pel((prozor[0]+prozor[2]-1,prozor[1]+prozor[3]-1),(39,49,64))
            return ucrtavanje_VALUE
        def 모서리(방향):
            return (prozor[0]+(3 if 방향 in (1,3) else prozor[2]-4),prozor[1]+(3 if 방향<=2 else prozor[3]-4))
        def promijeniti_veličinu_prevući(방향,차이,dugme=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ček_pel(흰점,(255,255,255))
            가리키기(가,세,dugme)
            끝가=max(0,min(너비-1,가+차이[0]));završiti_Vertikalno=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,završiti_Vertikalno,dugme);가리키기(끝가,završiti_Vertikalno,0);숨고르기()
            if dugme==1:
                LEFT_VALUE,위,폭,dužina_VALUE=prozor;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+dužina_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+završiti_Vertikalno-세))
                else:아래=max(위+216,min(높이,아래+završiti_Vertikalno-세))
                prozor[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        potvrditi_podesiti_veličinu();assert pokazivač_Skriveno[0]
        promijeniti_veličinu_prevući(4,(-100,-60),4);potvrditi_podesiti_veličinu() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            promijeniti_veličinu_prevući(방향,차이);potvrditi_podesiti_veličinu()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        slati_SMS("echo '"+긴글+"'");숨고르기()
        promijeniti_veličinu_prevući(4,(-1000,-1000));assert prozor[2:]==[360,216]
        promijeniti_veličinu_prevući(4,(너비,높이))
        Pokreni=slati_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Pokreni);potvrditi_podesiti_veličinu()
        # vi가 uređivati_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ljuska('ftpd start')
        prijenos_VALUE=ftplib.FTP();prijenos_VALUE.encoding='utf-8';prijenos_VALUE.connect('127.0.0.1',broj_priključka,timeout=20);prijenos_VALUE.login()
        기다리기(b'NORMAL',slati_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',slati_SMS('i미저장 한글 podaci\n'));숨고르기()
        promijeniti_veličinu_prevući(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((prozor[3]-56)//16)).encode() in LOG_red[-4096:]
        slati_SMS('작은 창에서도 이어 Piši\n');숨고르기()
        promijeniti_veličinu_prevući(4,(너비,높이))
        slati_SMS('큰 창에서도 이어 Piši\n');숨고르기()
        klik_dugme(0xff1b);klik_dugme(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',slati_SMS(':wq\n'))
        Sadržaj_VALUE=bytearray();prijenos_VALUE.retrbinary('RETR 크기자료.txt',Sadržaj_VALUE.extend)
        assert Sadržaj_VALUE=='미저장 한글 podaci\n작은 창에서도 이어 Piši\n큰 창에서도 이어 Piši\n'.encode(),Sadržaj_VALUE
        potvrditi_podesiti_veličinu().save(str(mjera_put/(podesiti_veličinu_SMS+'-large.png')))
        # 두 번째 창은 zadana_vrijednost Veličina, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Pokreni=len(LOG_red);klik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Pokreni)
        assert 'TERMINAL SIZE 68x19' in ljuska('terminal size')
        Pokreni=len(LOG_red);klik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Pokreni);potvrditi_podesiti_veličinu()
        promijeniti_veličinu_prevući(4,(-너비,-높이));potvrditi_podesiti_veličinu().save(str(mjera_put/(podesiti_veličinu_SMS+'-small.png')))
        # Veličina promijeniti_VALUE ZAD_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Pokreni=len(LOG_red);klik_VALUE(prozor[0]+prozor[2]-20,prozor[1]+15);기다리기(b'TERMINAL FOCUS 2',Pokreni)
        assert 'RESIZE CLOSED' in ljuska('echo RESIZE CLOSED')
        print('PASS:',podesiti_veličinu_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if prijenos_VALUE:prijenos_VALUE.close()
        if udaljeno_VALUE:udaljeno_VALUE.close()
        if proces_VALUE.poll() is None:
            proces_VALUE.terminate()
            try:proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:proces_VALUE.kill();proces_VALUE.wait()
        birač_a916db4e.close();proces_VALUE.stdout.close();(mjera_put/(podesiti_veličinu_SMS+'.log')).write_bytes(LOG_red)


def Pokreni():
    mjera_put=projicirati_koijen/'build/verification/resize';mjera_put.mkdir(parents=True,exist_ok=True)
    LOG_red={'passed':False,'kernel_sha256':hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,mjera_put);LOG_red['resolutions'].append([너비,높이])
        LOG_red.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(mjera_put/'report.json').write_text(json.dumps(LOG_red,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Pokreni()
