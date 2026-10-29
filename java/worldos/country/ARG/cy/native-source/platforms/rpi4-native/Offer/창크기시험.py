#!/usr/bin/env python3
"""go_iawn_data QEMU/VNC에서 Terfynell 모서리 llusgo_VALUE·pwyntydd·동적 nod_VALUE slot_cofnod·Golygu_VALUE Cynnwys_VALUE 보존를 검사한다."""
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
from bwrdd_gwaith_Gwedd import EXACT_VALUE
from Gweithredu_gorchymyn import prosiect_gwraidd


def 창크기시험(너비, 높이, mesur_llwybr):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); rhif_porth = 임시.getsockname()[1]
    newid_maint_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(prosiect_gwraidd/'Offer/Gweithredu_gorchymyn.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(rhif_porth), '--resolution', newid_maint_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    dewisydd_a916db4e = selectors.DefaultSelector(); dewisydd_a916db4e.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_rhes = bytearray(); pell_VALUE = None; trosglwyddo_VALUE = None; pwyntydd_cudd=[False]

    def 기다리기(sioe_VALUE, Gweithredu_2=0):
        마감 = time.monotonic() + 60
        while sioe_VALUE not in LOG_rhes[Gweithredu_2:]:
            if time.monotonic() > 마감 or Proses_VALUE.poll() is not None or b'HALTED' in LOG_rhes or b'PANIC:' in LOG_rhes:
                raise AssertionError(LOG_rhes[Gweithredu_2:].decode('utf-8', 'replace'))
            for digwyddiad, _ in dewisydd_a916db4e.select(.1):
                data = digwyddiad.fileobj.read(65536)
                if data: LOG_rhes.extend(data)
        return LOG_rhes[Gweithredu_2:].decode('utf-8', 'replace')

    def clicio_botwm(symbol, 눌림=True): pell_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def anfon_SMS(Testun):
        Gweithredu_2 = len(LOG_rhes)
        for nod_VALUE in Testun:
            symbol = 0xff0d if nod_VALUE == '\n' else ord(nod_VALUE) if ord(nod_VALUE) < 256 else 0x1000000 | ord(nod_VALUE)
            clicio_botwm(symbol); clicio_botwm(symbol, False)
        return Gweithredu_2

    def cragen(Testun): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', anfon_SMS(Testun+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Ar_i_fyny_safle, 눌림): pell_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Ar_i_fyny_safle))

    def clicio_VALUE(가로, Ar_i_fyny_safle): 가리키기(가로, Ar_i_fyny_safle, 1); 가리키기(가로, Ar_i_fyny_safle, 0)

    def map_didau_llun():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 go_iawn_data 너비를 쓴다.
        pell_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        lluniad_VALUE = Image.new('RGB', (너비, 높이)); ardal_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(pell_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                hyd_VALUE = struct.unpack('>I', EXACT_VALUE(pell_VALUE, 7)[3:])[0]; EXACT_VALUE(pell_VALUE, hyd_VALUE); continue
            assert 종류 == 0, 종류
            eitem_COUNT = struct.unpack('>H', EXACT_VALUE(pell_VALUE, 3)[1:])[0]
            for _ in range(eitem_COUNT):
                가로, Ar_i_fyny_safle, 폭, hyd_VALUE, amgodio_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(pell_VALUE, 12))
                if amgodio_VALUE == -239:
                    assert 폭==0 and hyd_VALUE==0, 'remote cursor must be hidden'
                    pwyntydd_cudd[0]=True
                    continue
                assert amgodio_VALUE == 0 and 가로+폭 <= 너비 and Ar_i_fyny_safle+hyd_VALUE <= 높이
                lluniad_VALUE.paste(Image.frombytes('RGB', (폭, hyd_VALUE), EXACT_VALUE(pell_VALUE, 폭*hyd_VALUE*4), 'raw', 'BGRX'), (가로, Ar_i_fyny_safle))
                ardal_VALUE_9285603e += 폭*hyd_VALUE
            if ardal_VALUE_9285603e:
                assert ardal_VALUE_9285603e == 너비*높이, ardal_VALUE_9285603e
                return lluniad_VALUE

    def gwirio_pel(cyfesuryn_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            lluniad_VALUE = map_didau_llun()
            if lluniad_VALUE.getpixel(cyfesuryn_VALUE) == 색: return lluniad_VALUE
            if time.monotonic() > 마감: raise AssertionError((cyfesuryn_VALUE, lluniad_VALUE.getpixel(cyfesuryn_VALUE), 색))

    def Upload_Ffeil(Enw, data): trosglwyddo_VALUE.storbinary('STOR '+Enw, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+newid_maint_SMS+' RGB32').encode() in LOG_rhes
        print('BOOT:', newid_maint_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_rhes).group(1))
        pell_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(pell_VALUE, 12) == b'RFB 003.008\n'; pell_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(pell_VALUE, EXACT_VALUE(pell_VALUE, 1)[0]); pell_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(pell_VALUE, 4) == b'\0'*4; pell_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(pell_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(pell_VALUE, struct.unpack('>I', 초기[20:])[0])
        pell_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        pell_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        gwirio_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for digwyddiad,_ in dewisydd_a916db4e.select(.02):
                    data=digwyddiad.fileobj.read(65536)
                    if data:LOG_rhes.extend(data)
        ffenestr=[12,48,568,360]
        def dilysu_newid_maint():
            COLUMN_VALUE,ROW_VALUE=(ffenestr[2]-24)//8,(ffenestr[3]-56)//16
            Testun=cragen('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Testun,Testun
            # go_iawn_data ffenestr 테두리: 단지 Maint ymholiad_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            gwirio_pel((ffenestr[0],ffenestr[1]),(32,80,144))
            lluniad_VALUE=gwirio_pel((ffenestr[0]+ffenestr[2]-1,ffenestr[1]+ffenestr[3]-1),(39,49,64))
            return lluniad_VALUE
        def 모서리(방향):
            return (ffenestr[0]+(3 if 방향 in (1,3) else ffenestr[2]-4),ffenestr[1]+(3 if 방향<=2 else ffenestr[3]-4))
        def ailfeintio_llusgo(방향,차이,botwm=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            gwirio_pel(흰점,(255,255,255))
            가리키기(가,세,botwm)
            끝가=max(0,min(너비-1,가+차이[0]));gorffen_Ar_i_fyny=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,gorffen_Ar_i_fyny,botwm);가리키기(끝가,gorffen_Ar_i_fyny,0);숨고르기()
            if botwm==1:
                LEFT_VALUE,위,폭,hyd_VALUE=ffenestr;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+hyd_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+gorffen_Ar_i_fyny-세))
                else:아래=max(위+216,min(높이,아래+gorffen_Ar_i_fyny-세))
                ffenestr[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        dilysu_newid_maint();assert pwyntydd_cudd[0]
        ailfeintio_llusgo(4,(-100,-60),4);dilysu_newid_maint() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ailfeintio_llusgo(방향,차이);dilysu_newid_maint()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        anfon_SMS("echo '"+긴글+"'");숨고르기()
        ailfeintio_llusgo(4,(-1000,-1000));assert ffenestr[2:]==[360,216]
        ailfeintio_llusgo(4,(너비,높이))
        Gweithredu_2=anfon_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Gweithredu_2);dilysu_newid_maint()
        # vi가 Golygu_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        cragen('ftpd start')
        trosglwyddo_VALUE=ftplib.FTP();trosglwyddo_VALUE.encoding='utf-8';trosglwyddo_VALUE.connect('127.0.0.1',rhif_porth,timeout=20);trosglwyddo_VALUE.login()
        기다리기(b'NORMAL',anfon_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',anfon_SMS('i미저장 한글 data\n'));숨고르기()
        ailfeintio_llusgo(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ffenestr[3]-56)//16)).encode() in LOG_rhes[-4096:]
        anfon_SMS('작은 창에서도 이어 Ysgrifennu\n');숨고르기()
        ailfeintio_llusgo(4,(너비,높이))
        anfon_SMS('큰 창에서도 이어 Ysgrifennu\n');숨고르기()
        clicio_botwm(0xff1b);clicio_botwm(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',anfon_SMS(':wq\n'))
        Cynnwys_VALUE=bytearray();trosglwyddo_VALUE.retrbinary('RETR 크기자료.txt',Cynnwys_VALUE.extend)
        assert Cynnwys_VALUE=='미저장 한글 data\n작은 창에서도 이어 Ysgrifennu\n큰 창에서도 이어 Ysgrifennu\n'.encode(),Cynnwys_VALUE
        dilysu_newid_maint().save(str(mesur_llwybr/(newid_maint_SMS+'-large.png')))
        # 두 번째 창은 gwerth_diofyn Maint, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Gweithredu_2=len(LOG_rhes);clicio_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Gweithredu_2)
        assert 'TERMINAL SIZE 68x19' in cragen('terminal size')
        Gweithredu_2=len(LOG_rhes);clicio_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Gweithredu_2);dilysu_newid_maint()
        ailfeintio_llusgo(4,(-너비,-높이));dilysu_newid_maint().save(str(mesur_llwybr/(newid_maint_SMS+'-small.png')))
        # Maint newid_VALUE BACK_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Gweithredu_2=len(LOG_rhes);clicio_VALUE(ffenestr[0]+ffenestr[2]-20,ffenestr[1]+15);기다리기(b'TERMINAL FOCUS 2',Gweithredu_2)
        assert 'RESIZE CLOSED' in cragen('echo RESIZE CLOSED')
        print('PASS:',newid_maint_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if trosglwyddo_VALUE:trosglwyddo_VALUE.close()
        if pell_VALUE:pell_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
        dewisydd_a916db4e.close();Proses_VALUE.stdout.close();(mesur_llwybr/(newid_maint_SMS+'.log')).write_bytes(LOG_rhes)


def Gweithredu_2():
    mesur_llwybr=prosiect_gwraidd/'build/verification/resize';mesur_llwybr.mkdir(parents=True,exist_ok=True)
    LOG_rhes={'passed':False,'kernel_sha256':hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,mesur_llwybr);LOG_rhes['resolutions'].append([너비,높이])
        LOG_rhes.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(mesur_llwybr/'report.json').write_text(json.dumps(LOG_rhes,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Gweithredu_2()
