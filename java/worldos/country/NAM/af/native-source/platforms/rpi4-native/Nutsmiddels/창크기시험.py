#!/usr/bin/env python3
"""werklik_data QEMU/VNC에서 Terminaal 모서리 sleep_VALUE·wyser·동적 karakter_VALUE gleuf_inskrywing·redigeer_VALUE Inhoud_VALUE 보존를 검사한다."""
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
from werkskerm_bekyk import EXACT_VALUE
from uitvoer_bevel import Project_wortel


def 창크기시험(너비, 높이, maatreël_pad):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    verstel_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(Project_wortel/'Nutsmiddels/uitvoer_bevel.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', verstel_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selekteerder_a916db4e = selectors.DefaultSelector(); selekteerder_a916db4e.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_ry = bytearray(); afstands_VALUE = None; oordra_VALUE = None; wyser_verskuilde=[False]

    def 기다리기(wys_VALUE, Loop=0):
        마감 = time.monotonic() + 60
        while wys_VALUE not in LOG_ry[Loop:]:
            if time.monotonic() > 마감 or Proses_VALUE.poll() is not None or b'HALTED' in LOG_ry or b'PANIC:' in LOG_ry:
                raise AssertionError(LOG_ry[Loop:].decode('utf-8', 'replace'))
            for gebeurtenis, _ in selekteerder_a916db4e.select(.1):
                data = gebeurtenis.fileobj.read(65536)
                if data: LOG_ry.extend(data)
        return LOG_ry[Loop:].decode('utf-8', 'replace')

    def klik_knoppie(simbool, 눌림=True): afstands_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbool))

    def stuur_SMS(Teks):
        Loop = len(LOG_ry)
        for karakter_VALUE in Teks:
            simbool = 0xff0d if karakter_VALUE == '\n' else ord(karakter_VALUE) if ord(karakter_VALUE) < 256 else 0x1000000 | ord(karakter_VALUE)
            klik_knoppie(simbool); klik_knoppie(simbool, False)
        return Loop

    def dop(Teks): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', stuur_SMS(Teks+'; echo __RESIZE_DONE__\n'))

    def p_at(가로, Vertikaal_plaas, 눌림): afstands_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikaal_plaas))

    def klik_VALUE(가로, Vertikaal_plaas): p_at(가로, Vertikaal_plaas, 1); p_at(가로, Vertikaal_plaas, 0)

    def bispatroon_foto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 werklik_data 너비를 쓴다.
        afstands_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tekening_VALUE = Image.new('RGB', (너비, 높이)); area_VALUE = 0
        while True:
            종류 = EXACT_VALUE(afstands_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lengte_VALUE = struct.unpack('>I', EXACT_VALUE(afstands_VALUE, 7)[3:])[0]; EXACT_VALUE(afstands_VALUE, lengte_VALUE); continue
            assert 종류 == 0, 종류
            item_COUNT = struct.unpack('>H', EXACT_VALUE(afstands_VALUE, 3)[1:])[0]
            for _ in range(item_COUNT):
                가로, Vertikaal_plaas, 폭, lengte_VALUE, enkodering_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(afstands_VALUE, 12))
                if enkodering_VALUE == -239:
                    assert 폭==0 and lengte_VALUE==0, 'remote cursor must be hidden'
                    wyser_verskuilde[0]=True
                    continue
                assert enkodering_VALUE == 0 and 가로+폭 <= 너비 and Vertikaal_plaas+lengte_VALUE <= 높이
                tekening_VALUE.paste(Image.frombytes('RGB', (폭, lengte_VALUE), EXACT_VALUE(afstands_VALUE, 폭*lengte_VALUE*4), 'raw', 'BGRX'), (가로, Vertikaal_plaas))
                area_VALUE += 폭*lengte_VALUE
            if area_VALUE:
                assert area_VALUE == 너비*높이, area_VALUE
                return tekening_VALUE

    def tjek_pieksel(koördinaat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            tekening_VALUE = bispatroon_foto()
            if tekening_VALUE.getpixel(koördinaat_VALUE) == 색: return tekening_VALUE
            if time.monotonic() > 마감: raise AssertionError((koördinaat_VALUE, tekening_VALUE.getpixel(koördinaat_VALUE), 색))

    def oplaai_Lêers(Naam, data): oordra_VALUE.storbinary('STOR '+Naam, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+verstel_SMS+' RGB32').encode() in LOG_ry
        print('BOOT:', verstel_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ry).group(1))
        afstands_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(afstands_VALUE, 12) == b'RFB 003.008\n'; afstands_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(afstands_VALUE, EXACT_VALUE(afstands_VALUE, 1)[0]); afstands_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(afstands_VALUE, 4) == b'\0'*4; afstands_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(afstands_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(afstands_VALUE, struct.unpack('>I', 초기[20:])[0])
        afstands_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        afstands_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        tjek_pieksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for gebeurtenis,_ in selekteerder_a916db4e.select(.02):
                    data=gebeurtenis.fileobj.read(65536)
                    if data:LOG_ry.extend(data)
        venster=[12,48,568,360]
        def verifieer_verstel():
            kolom_VALUE,ry_VALUE=(venster[2]-24)//8,(venster[3]-56)//16
            Teks=dop('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(kolom_VALUE,ry_VALUE) in Teks,Teks
            # werklik_data venster 테두리: 단지 Grootte navraag_VALUE 값만 바뀐 것이 아닌지 확인한다.
            p_at(너비-1,10,0);숨고르기()
            tjek_pieksel((venster[0],venster[1]),(32,80,144))
            tekening_VALUE=tjek_pieksel((venster[0]+venster[2]-1,venster[1]+venster[3]-1),(39,49,64))
            return tekening_VALUE
        def 모서리(방향):
            return (venster[0]+(3 if 방향 in (1,3) else venster[2]-4),venster[1]+(3 if 방향<=2 else venster[3]-4))
        def herskaleer_sleep(방향,차이,knoppie=1):
            가,세=모서리(방향);p_at(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            tjek_pieksel(흰점,(255,255,255))
            p_at(가,세,knoppie)
            끝가=max(0,min(너비-1,가+차이[0]));beëindig_Vertikaal=max(0,min(높이-1,세+차이[1]))
            p_at(끝가,beëindig_Vertikaal,knoppie);p_at(끝가,beëindig_Vertikaal,0);숨고르기()
            if knoppie==1:
                LEFT_VALUE,위,폭,lengte_VALUE=venster;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+lengte_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+beëindig_Vertikaal-세))
                else:아래=max(위+216,min(높이,아래+beëindig_Vertikaal-세))
                venster[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        verifieer_verstel();assert wyser_verskuilde[0]
        herskaleer_sleep(4,(-100,-60),4);verifieer_verstel() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            herskaleer_sleep(방향,차이);verifieer_verstel()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        stuur_SMS("echo '"+긴글+"'");숨고르기()
        herskaleer_sleep(4,(-1000,-1000));assert venster[2:]==[360,216]
        herskaleer_sleep(4,(너비,높이))
        Loop=stuur_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Loop);verifieer_verstel()
        # vi가 redigeer_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        dop('ftpd start')
        oordra_VALUE=ftplib.FTP();oordra_VALUE.encoding='utf-8';oordra_VALUE.connect('127.0.0.1',접속번호,timeout=20);oordra_VALUE.login()
        기다리기(b'NORMAL',stuur_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',stuur_SMS('i미저장 한글 data\n'));숨고르기()
        herskaleer_sleep(4,(-너비,-높이))
        # ANSI ry_VALUE 이동에 새 ry_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((venster[3]-56)//16)).encode() in LOG_ry[-4096:]
        stuur_SMS('작은 창에서도 이어 Skryf\n');숨고르기()
        herskaleer_sleep(4,(너비,높이))
        stuur_SMS('큰 창에서도 이어 Skryf\n');숨고르기()
        klik_knoppie(0xff1b);klik_knoppie(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',stuur_SMS(':wq\n'))
        Inhoud_VALUE=bytearray();oordra_VALUE.retrbinary('RETR 크기자료.txt',Inhoud_VALUE.extend)
        assert Inhoud_VALUE=='미저장 한글 data\n작은 창에서도 이어 Skryf\n큰 창에서도 이어 Skryf\n'.encode(),Inhoud_VALUE
        verifieer_verstel().save(str(maatreël_pad/(verstel_SMS+'-large.png')))
        # 두 번째 창은 verstekwaarde Grootte, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Loop=len(LOG_ry);klik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Loop)
        assert 'TERMINAL SIZE 68x19' in dop('terminal size')
        Loop=len(LOG_ry);klik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Loop);verifieer_verstel()
        herskaleer_sleep(4,(-너비,-높이));verifieer_verstel().save(str(maatreël_pad/(verstel_SMS+'-small.png')))
        # Grootte verander_VALUE TERUG_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Loop=len(LOG_ry);klik_VALUE(venster[0]+venster[2]-20,venster[1]+15);기다리기(b'TERMINAL FOCUS 2',Loop)
        assert 'RESIZE CLOSED' in dop('echo RESIZE CLOSED')
        print('PASS:',verstel_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if oordra_VALUE:oordra_VALUE.close()
        if afstands_VALUE:afstands_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
        selekteerder_a916db4e.close();Proses_VALUE.stdout.close();(maatreël_pad/(verstel_SMS+'.log')).write_bytes(LOG_ry)


def Loop():
    maatreël_pad=Project_wortel/'build/verification/resize';maatreël_pad.mkdir(parents=True,exist_ok=True)
    LOG_ry={'passed':False,'kernel_sha256':hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,maatreël_pad);LOG_ry['resolutions'].append([너비,높이])
        LOG_ry.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(maatreël_pad/'report.json').write_text(json.dumps(LOG_ry,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Loop()
