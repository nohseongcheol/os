#!/usr/bin/env python3
"""dearbh_dàta QEMU/VNC에서 tèirmineal 모서리 slaod_VALUE·tomhaire·동적 caractar_VALUE slot_cur_a_steach·deasaich_VALUE susbaint_VALUE 보존를 검사한다."""
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
from deasg_seall import EXACT_VALUE
from gnìomhaich_àithne import tilg_freumh


def 창크기시험(너비, 높이, tomhas_slighe):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    atharraich_am_meud_SMS = '{}x{}'.format(너비, 높이)
    Pròiseas_VALUE = subprocess.Popen(['python3', str(tilg_freumh/'innealan/gnìomhaich_àithne.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', atharraich_am_meud_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    roghnaichear_a916db4e = selectors.DefaultSelector(); roghnaichear_a916db4e.register(Pròiseas_VALUE.stdout, selectors.EVENT_READ)
    LOG_ràgh = bytearray(); cian_VALUE = None; tar_chur_VALUE = None; tomhaire_falaichte=[False]

    def 기다리기(show_VALUE, ruith=0):
        마감 = time.monotonic() + 60
        while show_VALUE not in LOG_ràgh[ruith:]:
            if time.monotonic() > 마감 or Pròiseas_VALUE.poll() is not None or b'HALTED' in LOG_ràgh or b'PANIC:' in LOG_ràgh:
                raise AssertionError(LOG_ràgh[ruith:].decode('utf-8', 'replace'))
            for tachartas, _ in roghnaichear_a916db4e.select(.1):
                dàta = tachartas.fileobj.read(65536)
                if dàta: LOG_ràgh.extend(dàta)
        return LOG_ràgh[ruith:].decode('utf-8', 'replace')

    def briog_putan(samhla, 눌림=True): cian_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, samhla))

    def cuir_SMS(SMS):
        ruith = len(LOG_ràgh)
        for caractar_VALUE in SMS:
            samhla = 0xff0d if caractar_VALUE == '\n' else ord(caractar_VALUE) if ord(caractar_VALUE) < 256 else 0x1000000 | ord(caractar_VALUE)
            briog_putan(samhla); briog_putan(samhla, False)
        return ruith

    def slige(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', cuir_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, inghearach_suidhich, 눌림): cian_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, inghearach_suidhich))

    def briog_VALUE(가로, inghearach_suidhich): 가리키기(가로, inghearach_suidhich, 1); 가리키기(가로, inghearach_suidhich, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 dearbh_dàta 너비를 쓴다.
        cian_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tarraing_VALUE = Image.new('RGB', (너비, 높이)); raon_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(cian_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                faid_VALUE = struct.unpack('>I', EXACT_VALUE(cian_VALUE, 7)[3:])[0]; EXACT_VALUE(cian_VALUE, faid_VALUE); continue
            assert 종류 == 0, 종류
            nì_COUNT = struct.unpack('>H', EXACT_VALUE(cian_VALUE, 3)[1:])[0]
            for _ in range(nì_COUNT):
                가로, inghearach_suidhich, 폭, faid_VALUE, còdachadh_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(cian_VALUE, 12))
                if còdachadh_VALUE == -239:
                    assert 폭==0 and faid_VALUE==0, 'remote cursor must be hidden'
                    tomhaire_falaichte[0]=True
                    continue
                assert còdachadh_VALUE == 0 and 가로+폭 <= 너비 and inghearach_suidhich+faid_VALUE <= 높이
                tarraing_VALUE.paste(Image.frombytes('RGB', (폭, faid_VALUE), EXACT_VALUE(cian_VALUE, 폭*faid_VALUE*4), 'raw', 'BGRX'), (가로, inghearach_suidhich))
                raon_VALUE_9285603e += 폭*faid_VALUE
            if raon_VALUE_9285603e:
                assert raon_VALUE_9285603e == 너비*높이, raon_VALUE_9285603e
                return tarraing_VALUE

    def seic_pel(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            tarraing_VALUE = bitmap_IMAGE()
            if tarraing_VALUE.getpixel(좌표) == 색: return tarraing_VALUE
            if time.monotonic() > 마감: raise AssertionError((좌표, tarraing_VALUE.getpixel(좌표), 색))

    def luchdaich_suas_faidhlichean(Ainm, dàta): tar_chur_VALUE.storbinary('STOR '+Ainm, io.BytesIO(dàta))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+atharraich_am_meud_SMS+' RGB32').encode() in LOG_ràgh
        print('BOOT:', atharraich_am_meud_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ràgh).group(1))
        cian_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(cian_VALUE, 12) == b'RFB 003.008\n'; cian_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(cian_VALUE, EXACT_VALUE(cian_VALUE, 1)[0]); cian_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(cian_VALUE, 4) == b'\0'*4; cian_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(cian_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(cian_VALUE, struct.unpack('>I', 초기[20:])[0])
        cian_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        cian_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        seic_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for tachartas,_ in roghnaichear_a916db4e.select(.02):
                    dàta=tachartas.fileobj.read(65536)
                    if dàta:LOG_ràgh.extend(dàta)
        uinneag=[12,48,568,360]
        def dearbh_atharraich_am_meud():
            colbh_VALUE,ROW_VALUE=(uinneag[2]-24)//8,(uinneag[3]-56)//16
            SMS=slige('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(colbh_VALUE,ROW_VALUE) in SMS,SMS
            # dearbh_dàta uinneag 테두리: 단지 atharraich_am_meud ceist_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            seic_pel((uinneag[0],uinneag[1]),(32,80,144))
            tarraing_VALUE=seic_pel((uinneag[0]+uinneag[2]-1,uinneag[1]+uinneag[3]-1),(39,49,64))
            return tarraing_VALUE
        def 모서리(방향):
            return (uinneag[0]+(3 if 방향 in (1,3) else uinneag[2]-4),uinneag[1]+(3 if 방향<=2 else uinneag[3]-4))
        def atharraich_am_meud_slaod(방향,차이,putan=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            seic_pel(흰점,(255,255,255))
            가리키기(가,세,putan)
            끝가=max(0,min(너비-1,가+차이[0]));crìochnaich_inghearach=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,crìochnaich_inghearach,putan);가리키기(끝가,crìochnaich_inghearach,0);숨고르기()
            if putan==1:
                LEFT_VALUE,위,폭,faid_VALUE=uinneag;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+faid_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+crìochnaich_inghearach-세))
                else:아래=max(위+216,min(높이,아래+crìochnaich_inghearach-세))
                uinneag[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        dearbh_atharraich_am_meud();assert tomhaire_falaichte[0]
        atharraich_am_meud_slaod(4,(-100,-60),4);dearbh_atharraich_am_meud() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            atharraich_am_meud_slaod(방향,차이);dearbh_atharraich_am_meud()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        cuir_SMS("echo '"+긴글+"'");숨고르기()
        atharraich_am_meud_slaod(4,(-1000,-1000));assert uinneag[2:]==[360,216]
        atharraich_am_meud_slaod(4,(너비,높이))
        ruith=cuir_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ruith);dearbh_atharraich_am_meud()
        # vi가 deasaich_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        slige('ftpd start')
        tar_chur_VALUE=ftplib.FTP();tar_chur_VALUE.encoding='utf-8';tar_chur_VALUE.connect('127.0.0.1',접속번호,timeout=20);tar_chur_VALUE.login()
        기다리기(b'NORMAL',cuir_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',cuir_SMS('i미저장 한글 dàta\n'));숨고르기()
        atharraich_am_meud_slaod(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((uinneag[3]-56)//16)).encode() in LOG_ràgh[-4096:]
        cuir_SMS('작은 창에서도 이어 sgrìobh\n');숨고르기()
        atharraich_am_meud_slaod(4,(너비,높이))
        cuir_SMS('큰 창에서도 이어 sgrìobh\n');숨고르기()
        briog_putan(0xff1b);briog_putan(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',cuir_SMS(':wq\n'))
        susbaint_VALUE=bytearray();tar_chur_VALUE.retrbinary('RETR 크기자료.txt',susbaint_VALUE.extend)
        assert susbaint_VALUE=='미저장 한글 dàta\n작은 창에서도 이어 sgrìobh\n큰 창에서도 이어 sgrìobh\n'.encode(),susbaint_VALUE
        dearbh_atharraich_am_meud().save(str(tomhas_slighe/(atharraich_am_meud_SMS+'-large.png')))
        # 두 번째 창은 luach_bunaiteach atharraich_am_meud, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ruith=len(LOG_ràgh);briog_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',ruith)
        assert 'TERMINAL SIZE 68x19' in slige('terminal size')
        ruith=len(LOG_ràgh);briog_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',ruith);dearbh_atharraich_am_meud()
        atharraich_am_meud_slaod(4,(-너비,-높이));dearbh_atharraich_am_meud().save(str(tomhas_slighe/(atharraich_am_meud_SMS+'-small.png')))
        # atharraich_am_meud atharraich_VALUE Air_ais_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        ruith=len(LOG_ràgh);briog_VALUE(uinneag[0]+uinneag[2]-20,uinneag[1]+15);기다리기(b'TERMINAL FOCUS 2',ruith)
        assert 'RESIZE CLOSED' in slige('echo RESIZE CLOSED')
        print('PASS:',atharraich_am_meud_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if tar_chur_VALUE:tar_chur_VALUE.close()
        if cian_VALUE:cian_VALUE.close()
        if Pròiseas_VALUE.poll() is None:
            Pròiseas_VALUE.terminate()
            try:Pròiseas_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Pròiseas_VALUE.kill();Pròiseas_VALUE.wait()
        roghnaichear_a916db4e.close();Pròiseas_VALUE.stdout.close();(tomhas_slighe/(atharraich_am_meud_SMS+'.log')).write_bytes(LOG_ràgh)


def ruith():
    tomhas_slighe=tilg_freumh/'build/verification/resize';tomhas_slighe.mkdir(parents=True,exist_ok=True)
    LOG_ràgh={'passed':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,tomhas_slighe);LOG_ràgh['resolutions'].append([너비,높이])
        LOG_ràgh.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(tomhas_slighe/'report.json').write_text(json.dumps(LOG_ràgh,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ruith()
