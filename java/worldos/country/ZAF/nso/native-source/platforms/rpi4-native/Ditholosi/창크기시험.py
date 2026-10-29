#!/usr/bin/env python3
"""kgonthe_data QEMU/VNC에서 터미널 모서리 goga_boleng·sešupi·동적 tlhaka_boleng sekgobana_go_tsenya_tshedimošo·rulaganya_boleng Diteng_boleng 보존를 검사한다."""
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
from teskethopo_pogelo import 정확한값
from phethagatša_taelo import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    bogolo_SMS = '{}x{}'.format(너비, 높이)
    tiragalo_boleng = subprocess.Popen(['python3', str(기준/'Ditholosi/phethagatša_taelo.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', bogolo_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    sekgethi_a916db4e = selectors.DefaultSelector(); sekgethi_a916db4e.register(tiragalo_boleng.stdout, selectors.EVENT_READ)
    pego_rei = bytearray(); ya_kgole_boleng = None; fetišetša_boleng = None; sešupi_fihlilwego=[False]

    def 기다리기(bontšha_boleng, Diriša=0):
        마감 = time.monotonic() + 60
        while bontšha_boleng not in pego_rei[Diriša:]:
            if time.monotonic() > 마감 or tiragalo_boleng.poll() is not None or b'HALTED' in pego_rei or b'PANIC:' in pego_rei:
                raise AssertionError(pego_rei[Diriša:].decode('utf-8', 'replace'))
            for tiragalo, _ in sekgethi_a916db4e.select(.1):
                data = tiragalo.fileobj.read(65536)
                if data: pego_rei.extend(data)
        return pego_rei[Diriša:].decode('utf-8', 'replace')

    def klika_konope(leswao, 눌림=True): ya_kgole_boleng.sendall(struct.pack('>BBHI', 4, int(눌림), 0, leswao))

    def romela_SMS(Sengwalwa):
        Diriša = len(pego_rei)
        for tlhaka_boleng in Sengwalwa:
            leswao = 0xff0d if tlhaka_boleng == '\n' else ord(tlhaka_boleng) if ord(tlhaka_boleng) < 256 else 0x1000000 | ord(tlhaka_boleng)
            klika_konope(leswao); klika_konope(leswao, False)
        return Diriša

    def šele(Sengwalwa): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', romela_SMS(Sengwalwa+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): ya_kgole_boleng.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def klika_boleng(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def seswantšho_sa_go_bopša_ka_dikhutlwana_seswantšho():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 kgonthe_data 너비를 쓴다.
        ya_kgole_boleng.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        sethalwa_boleng = Image.new('RGB', (너비, 높이)); area_boleng = 0
        while True:
            종류 = 정확한값(ya_kgole_boleng, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                botelele_boleng = struct.unpack('>I', 정확한값(ya_kgole_boleng, 7)[3:])[0]; 정확한값(ya_kgole_boleng, botelele_boleng); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ya_kgole_boleng, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, botelele_boleng, go_enkhouta_boleng = struct.unpack('>HHHHi', 정확한값(ya_kgole_boleng, 12))
                if go_enkhouta_boleng == -239:
                    assert 폭==0 and botelele_boleng==0, 'remote cursor must be hidden'
                    sešupi_fihlilwego[0]=True
                    continue
                assert go_enkhouta_boleng == 0 and 가로+폭 <= 너비 and 세로+botelele_boleng <= 높이
                sethalwa_boleng.paste(Image.frombytes('RGB', (폭, botelele_boleng), 정확한값(ya_kgole_boleng, 폭*botelele_boleng*4), 'raw', 'BGRX'), (가로, 세로))
                area_boleng += 폭*botelele_boleng
            if area_boleng:
                assert area_boleng == 너비*높이, area_boleng
                return sethalwa_boleng

    def lekola_phele(kgokaganyo_boleng, 색):
        마감 = time.monotonic()+10
        while True:
            sethalwa_boleng = seswantšho_sa_go_bopša_ka_dikhutlwana_seswantšho()
            if sethalwa_boleng.getpixel(kgokaganyo_boleng) == 색: return sethalwa_boleng
            if time.monotonic() > 마감: raise AssertionError((kgokaganyo_boleng, sethalwa_boleng.getpixel(kgokaganyo_boleng), 색))

    def apolouto_Difaele(Leina, data): fetišetša_boleng.storbinary('STOR '+Leina, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+bogolo_SMS+' RGB32').encode() in pego_rei
        print('BOOT:', bogolo_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', pego_rei).group(1))
        ya_kgole_boleng = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ya_kgole_boleng, 12) == b'RFB 003.008\n'; ya_kgole_boleng.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ya_kgole_boleng, 정확한값(ya_kgole_boleng, 1)[0]); ya_kgole_boleng.sendall(b'\x01')
        assert 정확한값(ya_kgole_boleng, 4) == b'\0'*4; ya_kgole_boleng.sendall(b'\x01')
        초기 = 정확한값(ya_kgole_boleng, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ya_kgole_boleng, struct.unpack('>I', 초기[20:])[0])
        ya_kgole_boleng.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ya_kgole_boleng.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        lekola_phele((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for tiragalo,_ in sekgethi_a916db4e.select(.02):
                    data=tiragalo.fileobj.read(65536)
                    if data:pego_rei.extend(data)
        lefastere=[12,48,568,360]
        def kgonthiša_bogolo():
            kholomo_boleng,rei_boleng=(lefastere[2]-24)//8,(lefastere[3]-56)//16
            Sengwalwa=šele('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(kholomo_boleng,rei_boleng) in Sengwalwa,Sengwalwa
            # kgonthe_data lefastere 테두리: 단지 Bogolo kwiri_boleng 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            lekola_phele((lefastere[0],lefastere[1]),(32,80,144))
            sethalwa_boleng=lekola_phele((lefastere[0]+lefastere[2]-1,lefastere[1]+lefastere[3]-1),(39,49,64))
            return sethalwa_boleng
        def 모서리(방향):
            return (lefastere[0]+(3 if 방향 in (1,3) else lefastere[2]-4),lefastere[1]+(3 if 방향<=2 else lefastere[3]-4))
        def fetoša_bogolo_goga(방향,차이,konope=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            lekola_phele(흰점,(255,255,255))
            가리키기(가,세,konope)
            끝가=max(0,min(너비-1,가+차이[0]));fetša_Tsepamo=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,fetša_Tsepamo,konope);가리키기(끝가,fetša_Tsepamo,0);숨고르기()
            if konope==1:
                왼,위,폭,botelele_boleng=lefastere;오른,아래=왼+폭,위+botelele_boleng
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+fetša_Tsepamo-세))
                else:아래=max(위+216,min(높이,아래+fetša_Tsepamo-세))
                lefastere[:]=[왼,위,오른-왼,아래-위]
        kgonthiša_bogolo();assert sešupi_fihlilwego[0]
        fetoša_bogolo_goga(4,(-100,-60),4);kgonthiša_bogolo() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            fetoša_bogolo_goga(방향,차이);kgonthiša_bogolo()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        romela_SMS("echo '"+긴글+"'");숨고르기()
        fetoša_bogolo_goga(4,(-1000,-1000));assert lefastere[2:]==[360,216]
        fetoša_bogolo_goga(4,(너비,높이))
        Diriša=romela_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Diriša);kgonthiša_bogolo()
        # vi가 rulaganya_boleng 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        šele('ftpd start')
        fetišetša_boleng=ftplib.FTP();fetišetša_boleng.encoding='utf-8';fetišetša_boleng.connect('127.0.0.1',접속번호,timeout=20);fetišetša_boleng.login()
        기다리기(b'NORMAL',romela_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',romela_SMS('i미저장 한글 data\n'));숨고르기()
        fetoša_bogolo_goga(4,(-너비,-높이))
        # ANSI rei_boleng 이동에 새 rei_boleng 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((lefastere[3]-56)//16)).encode() in pego_rei[-4096:]
        romela_SMS('작은 창에서도 이어 Ngwala\n');숨고르기()
        fetoša_bogolo_goga(4,(너비,높이))
        romela_SMS('큰 창에서도 이어 Ngwala\n');숨고르기()
        klika_konope(0xff1b);klika_konope(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',romela_SMS(':wq\n'))
        Diteng_boleng=bytearray();fetišetša_boleng.retrbinary('RETR 크기자료.txt',Diteng_boleng.extend)
        assert Diteng_boleng=='미저장 한글 data\n작은 창에서도 이어 Ngwala\n큰 창에서도 이어 Ngwala\n'.encode(),Diteng_boleng
        kgonthiša_bogolo().save(str(결과경로/(bogolo_SMS+'-large.png')))
        # 두 번째 창은 setsenywa_sa_tirelwa Bogolo, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Diriša=len(pego_rei);klika_boleng(70,16);기다리기(b'TERMINAL FOCUS 2',Diriša)
        assert 'TERMINAL SIZE 68x19' in šele('terminal size')
        Diriša=len(pego_rei);klika_boleng(180,16);기다리기(b'TERMINAL FOCUS 1',Diriša);kgonthiša_bogolo()
        fetoša_bogolo_goga(4,(-너비,-높이));kgonthiša_bogolo().save(str(결과경로/(bogolo_SMS+'-small.png')))
        # Bogolo fetoša_boleng Morago_boleng X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Diriša=len(pego_rei);klika_boleng(lefastere[0]+lefastere[2]-20,lefastere[1]+15);기다리기(b'TERMINAL FOCUS 2',Diriša)
        assert 'RESIZE CLOSED' in šele('echo RESIZE CLOSED')
        print('PASS:',bogolo_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if fetišetša_boleng:fetišetša_boleng.close()
        if ya_kgole_boleng:ya_kgole_boleng.close()
        if tiragalo_boleng.poll() is None:
            tiragalo_boleng.terminate()
            try:tiragalo_boleng.wait(timeout=8)
            except subprocess.TimeoutExpired:tiragalo_boleng.kill();tiragalo_boleng.wait()
        sekgethi_a916db4e.close();tiragalo_boleng.stdout.close();(결과경로/(bogolo_SMS+'.log')).write_bytes(pego_rei)


def Diriša():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    pego_rei={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);pego_rei['resolutions'].append([너비,높이])
        pego_rei.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(pego_rei,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Diriša()
