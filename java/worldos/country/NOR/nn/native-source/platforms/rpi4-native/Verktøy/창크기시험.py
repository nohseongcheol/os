#!/usr/bin/env python3
"""faktisk_data QEMU/VNC에서 Terminal 모서리 dra_VALUE·peikar·동적 teikn_VALUE felt_oppføring·redigere_VALUE Innhald_VALUE 보존를 검사한다."""
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
from stasjonær_vise import EXACT_VALUE
from Utfør_kommando import spegle_rot


def 창크기시험(너비, 높이, forretningsmål_bane):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portnummer = 임시.getsockname()[1]
    endre_storleik_SMS = '{}x{}'.format(너비, 높이)
    Prosess_VALUE = subprocess.Popen(['python3', str(spegle_rot/'Verktøy/Utfør_kommando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portnummer), '--resolution', endre_storleik_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    veljar_a916db4e = selectors.DefaultSelector(); veljar_a916db4e.register(Prosess_VALUE.stdout, selectors.EVENT_READ)
    LOG_rad = bytearray(); fjern_VALUE = None; Overfør_VALUE = None; peikar_Skjult=[False]

    def 기다리기(vise_VALUE_487749b8, Køyr_2=0):
        마감 = time.monotonic() + 60
        while vise_VALUE_487749b8 not in LOG_rad[Køyr_2:]:
            if time.monotonic() > 마감 or Prosess_VALUE.poll() is not None or b'HALTED' in LOG_rad or b'PANIC:' in LOG_rad:
                raise AssertionError(LOG_rad[Køyr_2:].decode('utf-8', 'replace'))
            for Hending, _ in veljar_a916db4e.select(.1):
                data = Hending.fileobj.read(65536)
                if data: LOG_rad.extend(data)
        return LOG_rad[Køyr_2:].decode('utf-8', 'replace')

    def klikk_knapp(symbol, 눌림=True): fjern_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def sende_SMS(Tekst):
        Køyr_2 = len(LOG_rad)
        for teikn_VALUE in Tekst:
            symbol = 0xff0d if teikn_VALUE == '\n' else ord(teikn_VALUE) if ord(teikn_VALUE) < 256 else 0x1000000 | ord(teikn_VALUE)
            klikk_knapp(symbol); klikk_knapp(symbol, False)
        return Køyr_2

    def grensesnitt(Tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', sende_SMS(Tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, vertikalvising_plassere, 눌림): fjern_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikalvising_plassere))

    def klikk_VALUE(가로, vertikalvising_plassere): 가리키기(가로, vertikalvising_plassere, 1); 가리키기(가로, vertikalvising_plassere, 0)

    def punktgrafikk_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktisk_data 너비를 쓴다.
        fjern_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        teikning_VALUE = Image.new('RGB', (너비, 높이)); felt_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(fjern_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lengd_VALUE = struct.unpack('>I', EXACT_VALUE(fjern_VALUE, 7)[3:])[0]; EXACT_VALUE(fjern_VALUE, lengd_VALUE); continue
            assert 종류 == 0, 종류
            vare_COUNT = struct.unpack('>H', EXACT_VALUE(fjern_VALUE, 3)[1:])[0]
            for _ in range(vare_COUNT):
                가로, vertikalvising_plassere, 폭, lengd_VALUE, koding_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(fjern_VALUE, 12))
                if koding_VALUE == -239:
                    assert 폭==0 and lengd_VALUE==0, 'remote cursor must be hidden'
                    peikar_Skjult[0]=True
                    continue
                assert koding_VALUE == 0 and 가로+폭 <= 너비 and vertikalvising_plassere+lengd_VALUE <= 높이
                teikning_VALUE.paste(Image.frombytes('RGB', (폭, lengd_VALUE), EXACT_VALUE(fjern_VALUE, 폭*lengd_VALUE*4), 'raw', 'BGRX'), (가로, vertikalvising_plassere))
                felt_VALUE_9285603e += 폭*lengd_VALUE
            if felt_VALUE_9285603e:
                assert felt_VALUE_9285603e == 너비*높이, felt_VALUE_9285603e
                return teikning_VALUE

    def sjekk_piksel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            teikning_VALUE = punktgrafikk_IMAGE()
            if teikning_VALUE.getpixel(koordinat_VALUE) == 색: return teikning_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, teikning_VALUE.getpixel(koordinat_VALUE), 색))

    def Upload_Filer(Namn, data): Overfør_VALUE.storbinary('STOR '+Namn, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+endre_storleik_SMS+' RGB32').encode() in LOG_rad
        print('BOOT:', endre_storleik_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_rad).group(1))
        fjern_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(fjern_VALUE, 12) == b'RFB 003.008\n'; fjern_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(fjern_VALUE, EXACT_VALUE(fjern_VALUE, 1)[0]); fjern_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(fjern_VALUE, 4) == b'\0'*4; fjern_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(fjern_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(fjern_VALUE, struct.unpack('>I', 초기[20:])[0])
        fjern_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        fjern_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        sjekk_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Hending,_ in veljar_a916db4e.select(.02):
                    data=Hending.fileobj.read(65536)
                    if data:LOG_rad.extend(data)
        vindauge=[12,48,568,360]
        def stadfeste_endre_storleik():
            COLUMN_VALUE,ROW_VALUE=(vindauge[2]-24)//8,(vindauge[3]-56)//16
            Tekst=grensesnitt('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Tekst,Tekst
            # faktisk_data vindauge 테두리: 단지 Storleik spørjing_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            sjekk_piksel((vindauge[0],vindauge[1]),(32,80,144))
            teikning_VALUE=sjekk_piksel((vindauge[0]+vindauge[2]-1,vindauge[1]+vindauge[3]-1),(39,49,64))
            return teikning_VALUE
        def 모서리(방향):
            return (vindauge[0]+(3 if 방향 in (1,3) else vindauge[2]-4),vindauge[1]+(3 if 방향<=2 else vindauge[3]-4))
        def endre_storleik_dra(방향,차이,knapp=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            sjekk_piksel(흰점,(255,255,255))
            가리키기(가,세,knapp)
            끝가=max(0,min(너비-1,가+차이[0]));avslutte_vertikalvising=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,avslutte_vertikalvising,knapp);가리키기(끝가,avslutte_vertikalvising,0);숨고르기()
            if knapp==1:
                LEFT_VALUE,위,폭,lengd_VALUE=vindauge;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+lengd_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+avslutte_vertikalvising-세))
                else:아래=max(위+216,min(높이,아래+avslutte_vertikalvising-세))
                vindauge[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        stadfeste_endre_storleik();assert peikar_Skjult[0]
        endre_storleik_dra(4,(-100,-60),4);stadfeste_endre_storleik() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            endre_storleik_dra(방향,차이);stadfeste_endre_storleik()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        sende_SMS("echo '"+긴글+"'");숨고르기()
        endre_storleik_dra(4,(-1000,-1000));assert vindauge[2:]==[360,216]
        endre_storleik_dra(4,(너비,높이))
        Køyr_2=sende_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Køyr_2);stadfeste_endre_storleik()
        # vi가 redigere_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        grensesnitt('ftpd start')
        Overfør_VALUE=ftplib.FTP();Overfør_VALUE.encoding='utf-8';Overfør_VALUE.connect('127.0.0.1',portnummer,timeout=20);Overfør_VALUE.login()
        기다리기(b'NORMAL',sende_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',sende_SMS('i미저장 한글 data\n'));숨고르기()
        endre_storleik_dra(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((vindauge[3]-56)//16)).encode() in LOG_rad[-4096:]
        sende_SMS('작은 창에서도 이어 Skriv\n');숨고르기()
        endre_storleik_dra(4,(너비,높이))
        sende_SMS('큰 창에서도 이어 Skriv\n');숨고르기()
        klikk_knapp(0xff1b);klikk_knapp(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',sende_SMS(':wq\n'))
        Innhald_VALUE=bytearray();Overfør_VALUE.retrbinary('RETR 크기자료.txt',Innhald_VALUE.extend)
        assert Innhald_VALUE=='미저장 한글 data\n작은 창에서도 이어 Skriv\n큰 창에서도 이어 Skriv\n'.encode(),Innhald_VALUE
        stadfeste_endre_storleik().save(str(forretningsmål_bane/(endre_storleik_SMS+'-large.png')))
        # 두 번째 창은 standardverdi Storleik, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Køyr_2=len(LOG_rad);klikk_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Køyr_2)
        assert 'TERMINAL SIZE 68x19' in grensesnitt('terminal size')
        Køyr_2=len(LOG_rad);klikk_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Køyr_2);stadfeste_endre_storleik()
        endre_storleik_dra(4,(-너비,-높이));stadfeste_endre_storleik().save(str(forretningsmål_bane/(endre_storleik_SMS+'-small.png')))
        # Storleik endre_VALUE TILBAKE_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Køyr_2=len(LOG_rad);klikk_VALUE(vindauge[0]+vindauge[2]-20,vindauge[1]+15);기다리기(b'TERMINAL FOCUS 2',Køyr_2)
        assert 'RESIZE CLOSED' in grensesnitt('echo RESIZE CLOSED')
        print('PASS:',endre_storleik_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Overfør_VALUE:Overfør_VALUE.close()
        if fjern_VALUE:fjern_VALUE.close()
        if Prosess_VALUE.poll() is None:
            Prosess_VALUE.terminate()
            try:Prosess_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Prosess_VALUE.kill();Prosess_VALUE.wait()
        veljar_a916db4e.close();Prosess_VALUE.stdout.close();(forretningsmål_bane/(endre_storleik_SMS+'.log')).write_bytes(LOG_rad)


def Køyr_2():
    forretningsmål_bane=spegle_rot/'build/verification/resize';forretningsmål_bane.mkdir(parents=True,exist_ok=True)
    LOG_rad={'passed':False,'kernel_sha256':hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,forretningsmål_bane);LOG_rad['resolutions'].append([너비,높이])
        LOG_rad.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(forretningsmål_bane/'report.json').write_text(json.dumps(LOG_rad,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Køyr_2()
