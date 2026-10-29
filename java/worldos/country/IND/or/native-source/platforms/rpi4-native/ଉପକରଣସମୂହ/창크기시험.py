#!/usr/bin/env python3
"""ପ୍ରକୃତ_ଡାଟା QEMU/VNC에서 ଟର୍ମିନାଲ 모서리 ଡ୍ରାଗ୍_ମୂଲ୍ୟ·ପଏଣ୍ଟର୍·동적 ବର୍ଣ୍ଣ_ମୂଲ୍ୟ ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି·ସଂପାଦନା_ମୂଲ୍ୟ ବିଷୟ_ମୂଲ୍ୟ 보존를 검사한다."""
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
from ଡେସ୍କଟପ୍_ଭିୟୁ import 정확한값
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍


def 창크기시험(너비, 높이, ମାପ_ପଥ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); ପୋର୍ଟ୍_ନମ୍ଵର୍ = 임시.getsockname()[1]
    ଅକାର_ପାଠ = '{}x{}'.format(너비, 높이)
    ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = subprocess.Popen(['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ପୋର୍ଟ୍_ନମ୍ଵର୍), '--resolution', ଅକାର_ପାଠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ଚୟନକାରୀ_a916db4e = selectors.DefaultSelector(); ଚୟନକାରୀ_a916db4e.register(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdout, selectors.EVENT_READ)
    ଲଗ୍_ଧାଡ଼ି = bytearray(); ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ = None; ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ = None; ପଏଣ୍ଟର୍_ଲୁକ୍କାୟିତ=[False]

    def 기다리기(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ, ଚଳାନ୍ତୁ=0):
        마감 = time.monotonic() + 60
        while ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ not in ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:]:
            if time.monotonic() > 마감 or ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None or b'HALTED' in ଲଗ୍_ଧାଡ଼ି or b'PANIC:' in ଲଗ୍_ଧାଡ଼ି:
                raise AssertionError(ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:].decode('utf-8', 'replace'))
            for ଘଟଣା, _ in ଚୟନକାରୀ_a916db4e.select(.1):
                ଡାଟା = ଘଟଣା.fileobj.read(65536)
                if ଡାଟା: ଲଗ୍_ଧାଡ଼ି.extend(ଡାଟା)
        return ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:].decode('utf-8', 'replace')

    def କ୍ଲିକ୍_କରିବା_ବଟନ୍(ସଙ୍କେତ, 눌림=True): ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ସଙ୍କେତ))

    def SMS_ପ୍ରେରଣ_କରନ୍ତୁ(ପାଠ୍ଯ):
        ଚଳାନ୍ତୁ = len(ଲଗ୍_ଧାଡ଼ି)
        for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ପାଠ୍ଯ:
            ସଙ୍କେତ = 0xff0d if ବର୍ଣ୍ଣ_ମୂଲ୍ୟ == '\n' else ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) if ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) < 256 else 0x1000000 | ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)
            କ୍ଲିକ୍_କରିବା_ବଟନ୍(ସଙ୍କେତ); କ୍ଲିକ୍_କରିବା_ବଟନ୍(ସଙ୍କେତ, False)
        return ଚଳାନ୍ତୁ

    def ଖୋଳ(ପାଠ୍ଯ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_ପ୍ରେରଣ_କରନ୍ତୁ(ପାଠ୍ଯ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 눌림): ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି))

    def କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି): 가리키기(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 1); 가리키기(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 0)

    def ବିଟ୍_ମ୍ୟାପ୍_ଚିତ୍ର():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ପ୍ରକୃତ_ଡାଟା 너비를 쓴다.
        ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ଅଙ୍କନ_ମୂଲ୍ୟ = Image.new('RGB', (너비, 높이)); ବର୍ଗ_ମୂଲ୍ୟ_9285603e = 0
        while True:
            종류 = 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = struct.unpack('>I', 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 7)[3:])[0]; 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 3)[1:])[0]
            for _ in range(개수):
                가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 폭, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ, ଏନକୋଡିଂ_ମୂଲ୍ୟ = struct.unpack('>HHHHi', 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 12))
                if ଏନକୋଡିଂ_ମୂଲ୍ୟ == -239:
                    assert 폭==0 and ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ==0, 'remote cursor must be hidden'
                    ପଏଣ୍ଟର୍_ଲୁକ୍କାୟିତ[0]=True
                    continue
                assert ଏନକୋଡିଂ_ମୂଲ୍ୟ == 0 and 가로+폭 <= 너비 and ଅନୁଲମ୍ବ_ସ୍ଥିତି+ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ <= 높이
                ଅଙ୍କନ_ମୂଲ୍ୟ.paste(Image.frombytes('RGB', (폭, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ), 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 폭*ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ*4), 'raw', 'BGRX'), (가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି))
                ବର୍ଗ_ମୂଲ୍ୟ_9285603e += 폭*ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ
            if ବର୍ଗ_ମୂଲ୍ୟ_9285603e:
                assert ବର୍ଗ_ମୂଲ୍ୟ_9285603e == 너비*높이, ବର୍ଗ_ମୂଲ୍ୟ_9285603e
                return ଅଙ୍କନ_ମୂଲ୍ୟ

    def ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍(ସଂଯୋଜନ_ମୂଲ୍ୟ, 색):
        마감 = time.monotonic()+10
        while True:
            ଅଙ୍କନ_ମୂଲ୍ୟ = ବିଟ୍_ମ୍ୟାପ୍_ଚିତ୍ର()
            if ଅଙ୍କନ_ମୂଲ୍ୟ.getpixel(ସଂଯୋଜନ_ମୂଲ୍ୟ) == 색: return ଅଙ୍କନ_ମୂଲ୍ୟ
            if time.monotonic() > 마감: raise AssertionError((ସଂଯୋଜନ_ମୂଲ୍ୟ, ଅଙ୍କନ_ମୂଲ୍ୟ.getpixel(ସଂଯୋଜନ_ମୂଲ୍ୟ), 색))

    def ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ(ନାମ, ଡାଟା): ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.storbinary('STOR '+ନାମ, io.BytesIO(ଡାଟା))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ଅକାର_ପାଠ+' RGB32').encode() in ଲଗ୍_ଧାଡ଼ି
        print('BOOT:', ଅକାର_ପାଠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ଲଗ୍_ଧାଡ଼ି).group(1))
        ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 12) == b'RFB 003.008\n'; ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 1)[0]); ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(b'\x01')
        assert 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 4) == b'\0'*4; ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(b'\x01')
        초기 = 정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ, struct.unpack('>I', 초기[20:])[0])
        ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ଘଟଣା,_ in ଚୟନକାରୀ_a916db4e.select(.02):
                    ଡାଟା=ଘଟଣା.fileobj.read(65536)
                    if ଡାଟା:ଲଗ୍_ଧାଡ଼ି.extend(ଡାଟା)
        ଓ୍ୱିଣ୍ଡୋ=[12,48,568,360]
        def ଯାଞ୍ଚ୍_କରିବା_ଅକାର():
            ସ୍ତମ୍ଭ_ମୂଲ୍ୟ,ଧାଡ଼ି_ମୂଲ୍ୟ=(ଓ୍ୱିଣ୍ଡୋ[2]-24)//8,(ଓ୍ୱିଣ୍ଡୋ[3]-56)//16
            ପାଠ୍ଯ=ଖୋଳ('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ସ୍ତମ୍ଭ_ମୂଲ୍ୟ,ଧାଡ଼ି_ମୂଲ୍ୟ) in ପାଠ୍ଯ,ପାଠ୍ଯ
            # ପ୍ରକୃତ_ଡାଟା ଓ୍ୱିଣ୍ଡୋ 테두리: 단지 ଆକାର ଜିଜ୍ଞାସା_ମୂଲ୍ୟ 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((ଓ୍ୱିଣ୍ଡୋ[0],ଓ୍ୱିଣ୍ଡୋ[1]),(32,80,144))
            ଅଙ୍କନ_ମୂଲ୍ୟ=ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍((ଓ୍ୱିଣ୍ଡୋ[0]+ଓ୍ୱିଣ୍ଡୋ[2]-1,ଓ୍ୱିଣ୍ଡୋ[1]+ଓ୍ୱିଣ୍ଡୋ[3]-1),(39,49,64))
            return ଅଙ୍କନ_ମୂଲ୍ୟ
        def 모서리(방향):
            return (ଓ୍ୱିଣ୍ଡୋ[0]+(3 if 방향 in (1,3) else ଓ୍ୱିଣ୍ଡୋ[2]-4),ଓ୍ୱିଣ୍ଡୋ[1]+(3 if 방향<=2 else ଓ୍ୱିଣ୍ଡୋ[3]-4))
        def ପୁନରାକାର_ଡ୍ରାଗ୍(방향,차이,ବଟନ୍=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ପରୀକ୍ଷିତ_ପିକ୍ସେଲ୍(흰점,(255,255,255))
            가리키기(가,세,ବଟନ୍)
            끝가=max(0,min(너비-1,가+차이[0]));ଶେଷ_କରନ୍ତୁ_ଅନୁଲମ୍ବ=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ଶେଷ_କରନ୍ତୁ_ଅନୁଲମ୍ବ,ବଟନ୍);가리키기(끝가,ଶେଷ_କରନ୍ତୁ_ଅନୁଲମ୍ବ,0);숨고르기()
            if ବଟନ୍==1:
                왼,위,폭,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ=ଓ୍ୱିଣ୍ଡୋ;오른,아래=왼+폭,위+ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ଶେଷ_କରନ୍ତୁ_ଅନୁଲମ୍ବ-세))
                else:아래=max(위+216,min(높이,아래+ଶେଷ_କରନ୍ତୁ_ଅନୁଲମ୍ବ-세))
                ଓ୍ୱିଣ୍ଡୋ[:]=[왼,위,오른-왼,아래-위]
        ଯାଞ୍ଚ୍_କରିବା_ଅକାର();assert ପଏଣ୍ଟର୍_ଲୁକ୍କାୟିତ[0]
        ପୁନରାକାର_ଡ୍ରାଗ୍(4,(-100,-60),4);ଯାଞ୍ଚ୍_କରିବା_ଅକାର() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ପୁନରାକାର_ଡ୍ରାଗ୍(방향,차이);ଯାଞ୍ଚ୍_କରିବା_ଅକାର()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_ପ୍ରେରଣ_କରନ୍ତୁ("echo '"+긴글+"'");숨고르기()
        ପୁନରାକାର_ଡ୍ରାଗ୍(4,(-1000,-1000));assert ଓ୍ୱିଣ୍ଡୋ[2:]==[360,216]
        ପୁନରାକାର_ଡ୍ରାଗ୍(4,(너비,높이))
        ଚଳାନ୍ତୁ=SMS_ପ୍ରେରଣ_କରନ୍ତୁ('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ଚଳାନ୍ତୁ);ଯାଞ୍ଚ୍_କରିବା_ଅକାର()
        # vi가 ସଂପାଦନା_ମୂଲ୍ୟ 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ଖୋଳ('ftpd start')
        ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ=ftplib.FTP();ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.encoding='utf-8';ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.connect('127.0.0.1',ପୋର୍ଟ୍_ନମ୍ଵର୍,timeout=20);ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.login()
        기다리기(b'NORMAL',SMS_ପ୍ରେରଣ_କରନ୍ତୁ('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_ପ୍ରେରଣ_କରନ୍ତୁ('i미저장 한글 ଡାଟା\n'));숨고르기()
        ପୁନରାକାର_ଡ୍ରାଗ୍(4,(-너비,-높이))
        # ANSI ଧାଡ଼ି_ମୂଲ୍ୟ 이동에 새 ଧାଡ଼ି_ମୂଲ୍ୟ 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ଓ୍ୱିଣ୍ଡୋ[3]-56)//16)).encode() in ଲଗ୍_ଧାଡ଼ି[-4096:]
        SMS_ପ୍ରେରଣ_କରନ୍ତୁ('작은 창에서도 이어 ଲେଖନ୍ତୁ\n');숨고르기()
        ପୁନରାକାର_ଡ୍ରାଗ୍(4,(너비,높이))
        SMS_ପ୍ରେରଣ_କରନ୍ତୁ('큰 창에서도 이어 ଲେଖନ୍ତୁ\n');숨고르기()
        କ୍ଲିକ୍_କରିବା_ବଟନ୍(0xff1b);କ୍ଲିକ୍_କରିବା_ବଟନ୍(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_ପ୍ରେରଣ_କରନ୍ତୁ(':wq\n'))
        ବିଷୟ_ମୂଲ୍ୟ=bytearray();ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.retrbinary('RETR 크기자료.txt',ବିଷୟ_ମୂଲ୍ୟ.extend)
        assert ବିଷୟ_ମୂଲ୍ୟ=='미저장 한글 ଡାଟା\n작은 창에서도 이어 ଲେଖନ୍ତୁ\n큰 창에서도 이어 ଲେଖନ୍ତୁ\n'.encode(),ବିଷୟ_ମୂଲ୍ୟ
        ଯାଞ୍ଚ୍_କରିବା_ଅକାର().save(str(ମାପ_ପଥ/(ଅକାର_ପାଠ+'-large.png')))
        # 두 번째 창은 ଡିଫଲ୍ଟ_ମାନ ଆକାର, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ଚଳାନ୍ତୁ=len(ଲଗ୍_ଧାଡ଼ି);କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(70,16);기다리기(b'TERMINAL FOCUS 2',ଚଳାନ୍ତୁ)
        assert 'TERMINAL SIZE 68x19' in ଖୋଳ('terminal size')
        ଚଳାନ୍ତୁ=len(ଲଗ୍_ଧାଡ଼ି);କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(180,16);기다리기(b'TERMINAL FOCUS 1',ଚଳାନ୍ତୁ);ଯାଞ୍ଚ୍_କରିବା_ଅକାର()
        ପୁନରାକାର_ଡ୍ରାଗ୍(4,(-너비,-높이));ଯାଞ୍ଚ୍_କରିବା_ଅକାର().save(str(ମାପ_ପଥ/(ଅକାର_ପାଠ+'-small.png')))
        # ଆକାର ପରିବର୍ତ୍ତନ_ମୂଲ୍ୟ ପଛ_ମୂଲ୍ୟ X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ଚଳାନ୍ତୁ=len(ଲଗ୍_ଧାଡ଼ି);କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(ଓ୍ୱିଣ୍ଡୋ[0]+ଓ୍ୱିଣ୍ଡୋ[2]-20,ଓ୍ୱିଣ୍ଡୋ[1]+15);기다리기(b'TERMINAL FOCUS 2',ଚଳାନ୍ତୁ)
        assert 'RESIZE CLOSED' in ଖୋଳ('echo RESIZE CLOSED')
        print('PASS:',ଅକାର_ପାଠ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ:ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.close()
        if ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ:ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.close()
        if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is None:
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.terminate()
            try:ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=8)
            except subprocess.TimeoutExpired:ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.kill();ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait()
        ଚୟନକାରୀ_a916db4e.close();ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdout.close();(ମାପ_ପଥ/(ଅକାର_ପାଠ+'.log')).write_bytes(ଲଗ୍_ଧାଡ଼ି)


def ଚଳାନ୍ତୁ():
    ମାପ_ପଥ=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/resize';ମାପ_ପଥ.mkdir(parents=True,exist_ok=True)
    ଲଗ୍_ଧାଡ଼ି={'passed':False,'kernel_sha256':hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,ମାପ_ପଥ);ଲଗ୍_ଧାଡ଼ି['resolutions'].append([너비,높이])
        ଲଗ୍_ଧାଡ଼ି.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ମାପ_ପଥ/'report.json').write_text(json.dumps(ଲଗ୍_ଧାଡ଼ି,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ଚଳାନ୍ତୁ()
