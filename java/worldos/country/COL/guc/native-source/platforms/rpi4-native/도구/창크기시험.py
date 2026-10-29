#!/usr/bin/env python3
"""실제 QEMU/VNC에서 터미널 모서리 ajarattaa_ajutuu·포인터·동적 jeerü_ajutuu 칸·anaataa_ajutuu alu_ujatüü_ajutuu 보존를 검사한다."""
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
from a_yataainpalaa_e_rajaa import 정확한값
from 실행 import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    크기글 = '{}x{}'.format(너비, 높이)
    과정 = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', 크기글], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(과정.stdout, selectors.EVENT_READ)
    aa_innachikimaajatü_aparatsee = bytearray(); 원격 = None; alate_eraa_ajutuu = None; 포인터숨김=[False]

    def 기다리기(표시, 시작=0):
        마감 = time.monotonic() + 60
        while 표시 not in aa_innachikimaajatü_aparatsee[시작:]:
            if time.monotonic() > 마감 or 과정.poll() is not None or b'HALTED' in aa_innachikimaajatü_aparatsee or b'PANIC:' in aa_innachikimaajatü_aparatsee:
                raise AssertionError(aa_innachikimaajatü_aparatsee[시작:].decode('utf-8', 'replace'))
            for kasachiki, _ in 선택기.select(.1):
                atijaaya = kasachiki.fileobj.read(65536)
                if atijaaya: aa_innachikimaajatü_aparatsee.extend(atijaaya)
        return aa_innachikimaajatü_aparatsee[시작:].decode('utf-8', 'replace')

    def aküliküjaa_ajüttülee(기호, 눌림=True): 원격.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def 글보내기(글):
        시작 = len(aa_innachikimaajatü_aparatsee)
        for jeerü_ajutuu in 글:
            기호 = 0xff0d if jeerü_ajutuu == '\n' else ord(jeerü_ajutuu) if ord(jeerü_ajutuu) < 256 else 0x1000000 | ord(jeerü_ajutuu)
            aküliküjaa_ajüttülee(기호); aküliküjaa_ajüttülee(기호, False)
        return 시작

    def aluwataalapu_u(글): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', 글보내기(글+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): 원격.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def aküliküjaa_ajutuu(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def maapa_wiitümaajatü_ayaakuaa():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 실제 너비를 쓴다.
        원격.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        그림 = Image.new('RGB', (너비, 높이)); 면적 = 0
        while True:
            종류 = 정확한값(원격, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                akaliaa_ajutuu = struct.unpack('>I', 정확한값(원격, 7)[3:])[0]; 정확한값(원격, akaliaa_ajutuu); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(원격, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, akaliaa_ajutuu, atijitaalüjiaa_ajutuu = struct.unpack('>HHHHi', 정확한값(원격, 12))
                if atijitaalüjiaa_ajutuu == -239:
                    assert 폭==0 and akaliaa_ajutuu==0, 'remote cursor must be hidden'
                    포인터숨김[0]=True
                    continue
                assert atijitaalüjiaa_ajutuu == 0 and 가로+폭 <= 너비 and 세로+akaliaa_ajutuu <= 높이
                그림.paste(Image.frombytes('RGB', (폭, akaliaa_ajutuu), 정확한값(원격, 폭*akaliaa_ajutuu*4), 'raw', 'BGRX'), (가로, 세로))
                면적 += 폭*akaliaa_ajutuu
            if 면적:
                assert 면적 == 너비*높이, 면적
                return 그림

    def cheeke_pikserü(ayaawatülee_ajutuu, 색):
        마감 = time.monotonic()+10
        while True:
            그림 = maapa_wiitümaajatü_ayaakuaa()
            if 그림.getpixel(ayaawatülee_ajutuu) == 색: return 그림
            if time.monotonic() > 마감: raise AssertionError((ayaawatülee_ajutuu, 그림.getpixel(ayaawatülee_ajutuu), 색))

    def 올리기(이름, atijaaya): alate_eraa_ajutuu.storbinary('STOR '+이름, io.BytesIO(atijaaya))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+크기글+' RGB32').encode() in aa_innachikimaajatü_aparatsee
        print('BOOT:', 크기글, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', aa_innachikimaajatü_aparatsee).group(1))
        원격 = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(원격, 12) == b'RFB 003.008\n'; 원격.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(원격, 정확한값(원격, 1)[0]); 원격.sendall(b'\x01')
        assert 정확한값(원격, 4) == b'\0'*4; 원격.sendall(b'\x01')
        초기 = 정확한값(원격, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(원격, struct.unpack('>I', 초기[20:])[0])
        원격.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        원격.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        cheeke_pikserü((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for kasachiki,_ in 선택기.select(.02):
                    atijaaya=kasachiki.fileobj.read(65536)
                    if atijaaya:aa_innachikimaajatü_aparatsee.extend(atijaaya)
        analaaya=[12,48,568,360]
        def 크기확인():
            sha_washa_watüsü_ajutuu,aparatsee_ajutuu=(analaaya[2]-24)//8,(analaaya[3]-56)//16
            글=aluwataalapu_u('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(sha_washa_watüsü_ajutuu,aparatsee_ajutuu) in 글,글
            # 실제 analaaya 테두리: 단지 크기 asakiriaa_ajutuu 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            cheeke_pikserü((analaaya[0],analaaya[1]),(32,80,144))
            그림=cheeke_pikserü((analaaya[0]+analaaya[2]-1,analaaya[1]+analaaya[3]-1),(39,49,64))
            return 그림
        def 모서리(방향):
            return (analaaya[0]+(3 if 방향 in (1,3) else analaaya[2]-4),analaaya[1]+(3 if 방향<=2 else analaaya[3]-4))
        def 크기끌기(방향,차이,ajüttülee=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            cheeke_pikserü(흰점,(255,255,255))
            가리키기(가,세,ajüttülee)
            끝가=max(0,min(너비-1,가+차이[0]));끝세=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,끝세,ajüttülee);가리키기(끝가,끝세,0);숨고르기()
            if ajüttülee==1:
                왼,위,폭,akaliaa_ajutuu=analaaya;오른,아래=왼+폭,위+akaliaa_ajutuu
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+끝세-세))
                else:아래=max(위+216,min(높이,아래+끝세-세))
                analaaya[:]=[왼,위,오른-왼,아래-위]
        크기확인();assert 포인터숨김[0]
        크기끌기(4,(-100,-60),4);크기확인() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            크기끌기(방향,차이);크기확인()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        글보내기("echo '"+긴글+"'");숨고르기()
        크기끌기(4,(-1000,-1000));assert analaaya[2:]==[360,216]
        크기끌기(4,(너비,높이))
        시작=글보내기('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),시작);크기확인()
        # vi가 anaataa_ajutuu 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        aluwataalapu_u('ftpd start')
        alate_eraa_ajutuu=ftplib.FTP();alate_eraa_ajutuu.encoding='utf-8';alate_eraa_ajutuu.connect('127.0.0.1',접속번호,timeout=20);alate_eraa_ajutuu.login()
        기다리기(b'NORMAL',글보내기('vi /크기자료.txt\n'))
        기다리기(b'INSERT',글보내기('i미저장 한글 atijaaya\n'));숨고르기()
        크기끌기(4,(-너비,-높이))
        # ANSI aparatsee_ajutuu 이동에 새 aparatsee_ajutuu 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((analaaya[3]-56)//16)).encode() in aa_innachikimaajatü_aparatsee[-4096:]
        글보내기('작은 창에서도 이어 ashajaa\n');숨고르기()
        크기끌기(4,(너비,높이))
        글보내기('큰 창에서도 이어 ashajaa\n');숨고르기()
        aküliküjaa_ajüttülee(0xff1b);aküliküjaa_ajüttülee(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',글보내기(':wq\n'))
        alu_ujatüü_ajutuu=bytearray();alate_eraa_ajutuu.retrbinary('RETR 크기자료.txt',alu_ujatüü_ajutuu.extend)
        assert alu_ujatüü_ajutuu=='미저장 한글 atijaaya\n작은 창에서도 이어 ashajaa\n큰 창에서도 이어 ashajaa\n'.encode(),alu_ujatüü_ajutuu
        크기확인().save(str(결과경로/(크기글+'-large.png')))
        # 두 번째 창은 ajutuu_aneekuushitüjülia 크기, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        시작=len(aa_innachikimaajatü_aparatsee);aküliküjaa_ajutuu(70,16);기다리기(b'TERMINAL FOCUS 2',시작)
        assert 'TERMINAL SIZE 68x19' in aluwataalapu_u('terminal size')
        시작=len(aa_innachikimaajatü_aparatsee);aküliküjaa_ajutuu(180,16);기다리기(b'TERMINAL FOCUS 1',시작);크기확인()
        크기끌기(4,(-너비,-높이));크기확인().save(str(결과경로/(크기글+'-small.png')))
        # 크기 변경 뒤 X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        시작=len(aa_innachikimaajatü_aparatsee);aküliküjaa_ajutuu(analaaya[0]+analaaya[2]-20,analaaya[1]+15);기다리기(b'TERMINAL FOCUS 2',시작)
        assert 'RESIZE CLOSED' in aluwataalapu_u('echo RESIZE CLOSED')
        print('PASS:',크기글,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if alate_eraa_ajutuu:alate_eraa_ajutuu.close()
        if 원격:원격.close()
        if 과정.poll() is None:
            과정.terminate()
            try:과정.wait(timeout=8)
            except subprocess.TimeoutExpired:과정.kill();과정.wait()
        선택기.close();과정.stdout.close();(결과경로/(크기글+'.log')).write_bytes(aa_innachikimaajatü_aparatsee)


def 시작():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    aa_innachikimaajatü_aparatsee={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);aa_innachikimaajatü_aparatsee['resolutions'].append([너비,높이])
        aa_innachikimaajatü_aparatsee.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(aa_innachikimaajatü_aparatsee,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':시작()
