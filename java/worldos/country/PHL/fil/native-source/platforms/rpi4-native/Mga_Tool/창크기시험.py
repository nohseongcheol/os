#!/usr/bin/env python3
"""totoo_data QEMU/VNC에서 Terminal 모서리 mag_drag_VALUE·pointer·동적 karakter_VALUE espasyo_pagpasok·edit_VALUE Nilalaman_VALUE 보존를 검사한다."""
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
from desktop_View import EXACT_VALUE
from Mag_execute_utos import Project_root


def 창크기시험(너비, 높이, sukat_path):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); numero_ng_port = 임시.getsockname()[1]
    sukat_SMS = '{}x{}'.format(너비, 높이)
    Proseso_VALUE = subprocess.Popen(['python3', str(Project_root/'Mga_Tool/Mag_execute_utos.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numero_ng_port), '--resolution', sukat_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tagapili_a916db4e = selectors.DefaultSelector(); tagapili_a916db4e.register(Proseso_VALUE.stdout, selectors.EVENT_READ)
    LOG_hanay = bytearray(); malayuan_VALUE = None; lipat_VALUE = None; pointer_nakatago=[False]

    def 기다리기(ipakita_VALUE, run=0):
        마감 = time.monotonic() + 60
        while ipakita_VALUE not in LOG_hanay[run:]:
            if time.monotonic() > 마감 or Proseso_VALUE.poll() is not None or b'HALTED' in LOG_hanay or b'PANIC:' in LOG_hanay:
                raise AssertionError(LOG_hanay[run:].decode('utf-8', 'replace'))
            for kaganapan, _ in tagapili_a916db4e.select(.1):
                data = kaganapan.fileobj.read(65536)
                if data: LOG_hanay.extend(data)
        return LOG_hanay[run:].decode('utf-8', 'replace')

    def magklik_button(simbolo, 눌림=True): malayuan_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbolo))

    def magpadala_ng_SMS(SMS):
        run = len(LOG_hanay)
        for karakter_VALUE in SMS:
            simbolo = 0xff0d if karakter_VALUE == '\n' else ord(karakter_VALUE) if ord(karakter_VALUE) < 256 else 0x1000000 | ord(karakter_VALUE)
            magklik_button(simbolo); magklik_button(simbolo, False)
        return run

    def shell(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', magpadala_ng_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, archive_posisyon, 눌림): malayuan_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, archive_posisyon))

    def magklik_VALUE(가로, archive_posisyon): 가리키기(가로, archive_posisyon, 1); 가리키기(가로, archive_posisyon, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 totoo_data 너비를 쓴다.
        malayuan_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        iginuhit_VALUE = Image.new('RGB', (너비, 높이)); lugar_VALUE = 0
        while True:
            종류 = EXACT_VALUE(malayuan_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                haba_VALUE = struct.unpack('>I', EXACT_VALUE(malayuan_VALUE, 7)[3:])[0]; EXACT_VALUE(malayuan_VALUE, haba_VALUE); continue
            assert 종류 == 0, 종류
            item_COUNT = struct.unpack('>H', EXACT_VALUE(malayuan_VALUE, 3)[1:])[0]
            for _ in range(item_COUNT):
                가로, archive_posisyon, 폭, haba_VALUE, pag_encode_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(malayuan_VALUE, 12))
                if pag_encode_VALUE == -239:
                    assert 폭==0 and haba_VALUE==0, 'remote cursor must be hidden'
                    pointer_nakatago[0]=True
                    continue
                assert pag_encode_VALUE == 0 and 가로+폭 <= 너비 and archive_posisyon+haba_VALUE <= 높이
                iginuhit_VALUE.paste(Image.frombytes('RGB', (폭, haba_VALUE), EXACT_VALUE(malayuan_VALUE, 폭*haba_VALUE*4), 'raw', 'BGRX'), (가로, archive_posisyon))
                lugar_VALUE += 폭*haba_VALUE
            if lugar_VALUE:
                assert lugar_VALUE == 너비*높이, lugar_VALUE
                return iginuhit_VALUE

    def tseke_pel(coordinate_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            iginuhit_VALUE = bitmap_IMAGE()
            if iginuhit_VALUE.getpixel(coordinate_VALUE) == 색: return iginuhit_VALUE
            if time.monotonic() > 마감: raise AssertionError((coordinate_VALUE, iginuhit_VALUE.getpixel(coordinate_VALUE), 색))

    def upload_Mga_File(pangalan, data): lipat_VALUE.storbinary('STOR '+pangalan, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+sukat_SMS+' RGB32').encode() in LOG_hanay
        print('BOOT:', sukat_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_hanay).group(1))
        malayuan_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(malayuan_VALUE, 12) == b'RFB 003.008\n'; malayuan_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(malayuan_VALUE, EXACT_VALUE(malayuan_VALUE, 1)[0]); malayuan_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(malayuan_VALUE, 4) == b'\0'*4; malayuan_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(malayuan_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(malayuan_VALUE, struct.unpack('>I', 초기[20:])[0])
        malayuan_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        malayuan_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        tseke_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for kaganapan,_ in tagapili_a916db4e.select(.02):
                    data=kaganapan.fileobj.read(65536)
                    if data:LOG_hanay.extend(data)
        window=[12,48,568,360]
        def tiyakin_kumpirmahin_sukat():
            kolum_VALUE,ROW_VALUE=(window[2]-24)//8,(window[3]-56)//16
            SMS=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(kolum_VALUE,ROW_VALUE) in SMS,SMS
            # totoo_data window 테두리: 단지 sukat_82232621 query_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            tseke_pel((window[0],window[1]),(32,80,144))
            iginuhit_VALUE=tseke_pel((window[0]+window[2]-1,window[1]+window[3]-1),(39,49,64))
            return iginuhit_VALUE
        def 모서리(방향):
            return (window[0]+(3 if 방향 in (1,3) else window[2]-4),window[1]+(3 if 방향<=2 else window[3]-4))
        def palitan_ang_laki_mag_drag(방향,차이,button=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            tseke_pel(흰점,(255,255,255))
            가리키기(가,세,button)
            끝가=max(0,min(너비-1,가+차이[0]));tapusin_archive=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,tapusin_archive,button);가리키기(끝가,tapusin_archive,0);숨고르기()
            if button==1:
                LEFT_VALUE,위,폭,haba_VALUE=window;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+haba_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+tapusin_archive-세))
                else:아래=max(위+216,min(높이,아래+tapusin_archive-세))
                window[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        tiyakin_kumpirmahin_sukat();assert pointer_nakatago[0]
        palitan_ang_laki_mag_drag(4,(-100,-60),4);tiyakin_kumpirmahin_sukat() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            palitan_ang_laki_mag_drag(방향,차이);tiyakin_kumpirmahin_sukat()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        magpadala_ng_SMS("echo '"+긴글+"'");숨고르기()
        palitan_ang_laki_mag_drag(4,(-1000,-1000));assert window[2:]==[360,216]
        palitan_ang_laki_mag_drag(4,(너비,높이))
        run=magpadala_ng_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),run);tiyakin_kumpirmahin_sukat()
        # vi가 edit_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        lipat_VALUE=ftplib.FTP();lipat_VALUE.encoding='utf-8';lipat_VALUE.connect('127.0.0.1',numero_ng_port,timeout=20);lipat_VALUE.login()
        기다리기(b'NORMAL',magpadala_ng_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',magpadala_ng_SMS('i미저장 한글 data\n'));숨고르기()
        palitan_ang_laki_mag_drag(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((window[3]-56)//16)).encode() in LOG_hanay[-4096:]
        magpadala_ng_SMS('작은 창에서도 이어 sumulat\n');숨고르기()
        palitan_ang_laki_mag_drag(4,(너비,높이))
        magpadala_ng_SMS('큰 창에서도 이어 sumulat\n');숨고르기()
        magklik_button(0xff1b);magklik_button(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',magpadala_ng_SMS(':wq\n'))
        Nilalaman_VALUE=bytearray();lipat_VALUE.retrbinary('RETR 크기자료.txt',Nilalaman_VALUE.extend)
        assert Nilalaman_VALUE=='미저장 한글 data\n작은 창에서도 이어 sumulat\n큰 창에서도 이어 sumulat\n'.encode(),Nilalaman_VALUE
        tiyakin_kumpirmahin_sukat().save(str(sukat_path/(sukat_SMS+'-large.png')))
        # 두 번째 창은 value_ng_default sukat_82232621, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        run=len(LOG_hanay);magklik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',run)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        run=len(LOG_hanay);magklik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',run);tiyakin_kumpirmahin_sukat()
        palitan_ang_laki_mag_drag(4,(-너비,-높이));tiyakin_kumpirmahin_sukat().save(str(sukat_path/(sukat_SMS+'-small.png')))
        # sukat_82232621 baguhin_VALUE Bumalik_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        run=len(LOG_hanay);magklik_VALUE(window[0]+window[2]-20,window[1]+15);기다리기(b'TERMINAL FOCUS 2',run)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',sukat_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if lipat_VALUE:lipat_VALUE.close()
        if malayuan_VALUE:malayuan_VALUE.close()
        if Proseso_VALUE.poll() is None:
            Proseso_VALUE.terminate()
            try:Proseso_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proseso_VALUE.kill();Proseso_VALUE.wait()
        tagapili_a916db4e.close();Proseso_VALUE.stdout.close();(sukat_path/(sukat_SMS+'.log')).write_bytes(LOG_hanay)


def run():
    sukat_path=Project_root/'build/verification/resize';sukat_path.mkdir(parents=True,exist_ok=True)
    LOG_hanay={'passed':False,'kernel_sha256':hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,sukat_path);LOG_hanay['resolutions'].append([너비,높이])
        LOG_hanay.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(sukat_path/'report.json').write_text(json.dumps(LOG_hanay,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':run()
