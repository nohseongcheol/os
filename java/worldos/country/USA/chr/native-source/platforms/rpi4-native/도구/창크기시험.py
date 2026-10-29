#!/usr/bin/env python3
"""ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ QEMU/VNC에서 터미널 모서리 ᎦᎾᏏᏁᎦ_ᏧᎬᏩᎶᏗᏯ·ᎠᏎᎯᎯ·동적 ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ 칸·ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ 보존를 검사한다."""
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
from ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ import 정확한값
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ᎢᎩᏓ_ᎠᎪᎵᏰᏗ = '{}x{}'.format(너비, 높이)
    ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = subprocess.Popen(['python3', str(기준/'도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ᎢᎩᏓ_ᎠᎪᎵᏰᏗ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ᎠᏑᏰᏍᎩ_a916db4e = selectors.DefaultSelector(); ᎠᏑᏰᏍᎩ_a916db4e.register(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdout, selectors.EVENT_READ)
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = bytearray(); 원격 = None; ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ = None; ᎠᏎᎯᎯ_ᎬᏍᎦᏝ=[False]

    def 기다리기(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ, ᎠᎢᏎᏍᏗ=0):
        마감 = time.monotonic() + 60
        while ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:]:
            if time.monotonic() > 마감 or ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is not None or b'HALTED' in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ or b'PANIC:' in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ:
                raise AssertionError(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:].decode('utf-8', 'replace'))
            for ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ, _ in ᎠᏑᏰᏍᎩ_a916db4e.select(.1):
                ᎦᏟᏌᏅᎯ = ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.fileobj.read(65536)
                if ᎦᏟᏌᏅᎯ: ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(ᎦᏟᏌᏅᎯ)
        return ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:].decode('utf-8', 'replace')

    def ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(기호, 눌림=True): 원격.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ(ᎠᎪᎵᏰᏗ):
        ᎠᎢᏎᏍᏗ = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in ᎠᎪᎵᏰᏗ:
            기호 = 0xff0d if ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ == '\n' else ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) if ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) < 256 else 0x1000000 | ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ)
            ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(기호); ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(기호, False)
        return ᎠᎢᏎᏍᏗ

    def ᎤᏯᏍᎦ(ᎠᎪᎵᏰᏗ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ(ᎠᎪᎵᏰᏗ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): 원격.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitmap_ᎤᏓᏴᎳᏛ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 너비를 쓴다.
        원격.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ = Image.new('RGB', (너비, 높이)); ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ = 0
        while True:
            종류 = 정확한값(원격, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = struct.unpack('>I', 정확한값(원격, 7)[3:])[0]; 정확한값(원격, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(원격, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ, ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ = struct.unpack('>HHHHi', 정확한값(원격, 12))
                if ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ == -239:
                    assert 폭==0 and ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ==0, 'remote cursor must be hidden'
                    ᎠᏎᎯᎯ_ᎬᏍᎦᏝ[0]=True
                    continue
                assert ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ == 0 and 가로+폭 <= 너비 and 세로+ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ <= 높이
                ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.paste(Image.frombytes('RGB', (폭, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ), 정확한값(원격, 폭*ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ*4), 'raw', 'BGRX'), (가로, 세로))
                ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ += 폭*ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ
            if ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ:
                assert ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ == 너비*높이, ᎢᎬᎾᏕᎾ_ᏧᎬᏩᎶᏗᏯ
                return ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ

    def ᎪᎯᏳᏔᏅ_pel(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ = bitmap_ᎤᏓᏴᎳᏛ()
            if ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.getpixel(좌표) == 색: return ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ
            if time.monotonic() > 마감: raise AssertionError((좌표, ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.getpixel(좌표), 색))

    def 올리기(ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ): ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.storbinary('STOR '+ᏚᏙᎥᎢ, io.BytesIO(ᎦᏟᏌᏅᎯ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ᎢᎩᏓ_ᎠᎪᎵᏰᏗ+' RGB32').encode() in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ
        print('BOOT:', ᎢᎩᏓ_ᎠᎪᎵᏰᏗ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ).group(1))
        원격 = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(원격, 12) == b'RFB 003.008\n'; 원격.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(원격, 정확한값(원격, 1)[0]); 원격.sendall(b'\x01')
        assert 정확한값(원격, 4) == b'\0'*4; 원격.sendall(b'\x01')
        초기 = 정확한값(원격, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(원격, struct.unpack('>I', 초기[20:])[0])
        원격.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        원격.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ᎪᎯᏳᏔᏅ_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ,_ in ᎠᏑᏰᏍᎩ_a916db4e.select(.02):
                    ᎦᏟᏌᏅᎯ=ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.fileobj.read(65536)
                    if ᎦᏟᏌᏅᎯ:ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(ᎦᏟᏌᏅᎯ)
        ᏦᎳᏂ=[12,48,568,360]
        def ᎰᎯᏳᏓ_ᎢᎩᏓ():
            ᎨᏛᎢ_ᏧᎬᏩᎶᏗᏯ,ᎤᏓᏅᏅ_ᏧᎬᏩᎶᏗᏯ=(ᏦᎳᏂ[2]-24)//8,(ᏦᎳᏂ[3]-56)//16
            ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ᎨᏛᎢ_ᏧᎬᏩᎶᏗᏯ,ᎤᏓᏅᏅ_ᏧᎬᏩᎶᏗᏯ) in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            # ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ ᏦᎳᏂ 테두리: 단지 ᎢᎩᏓ ᎠᏛᏛᎲᏍᎩ_ᏧᎬᏩᎶᏗᏯ 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ᎪᎯᏳᏔᏅ_pel((ᏦᎳᏂ[0],ᏦᎳᏂ[1]),(32,80,144))
            ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ=ᎪᎯᏳᏔᏅ_pel((ᏦᎳᏂ[0]+ᏦᎳᏂ[2]-1,ᏦᎳᏂ[1]+ᏦᎳᏂ[3]-1),(39,49,64))
            return ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ
        def 모서리(방향):
            return (ᏦᎳᏂ[0]+(3 if 방향 in (1,3) else ᏦᎳᏂ[2]-4),ᏦᎳᏂ[1]+(3 if 방향<=2 else ᏦᎳᏂ[3]-4))
        def ᏂᎬ_ᎯᏁᏟᏴᎾ_ᎦᎾᏏᏁᎦ(방향,차이,ᎠᏐᏅᏍᏙᏗ=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ᎪᎯᏳᏔᏅ_pel(흰점,(255,255,255))
            가리키기(가,세,ᎠᏐᏅᏍᏙᏗ)
            끝가=max(0,min(너비-1,가+차이[0]));끝세=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,끝세,ᎠᏐᏅᏍᏙᏗ);가리키기(끝가,끝세,0);숨고르기()
            if ᎠᏐᏅᏍᏙᏗ==1:
                왼,위,폭,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=ᏦᎳᏂ;오른,아래=왼+폭,위+ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+끝세-세))
                else:아래=max(위+216,min(높이,아래+끝세-세))
                ᏦᎳᏂ[:]=[왼,위,오른-왼,아래-위]
        ᎰᎯᏳᏓ_ᎢᎩᏓ();assert ᎠᏎᎯᎯ_ᎬᏍᎦᏝ[0]
        ᏂᎬ_ᎯᏁᏟᏴᎾ_ᎦᎾᏏᏁᎦ(4,(-100,-60),4);ᎰᎯᏳᏓ_ᎢᎩᏓ() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ᏂᎬ_ᎯᏁᏟᏴᎾ_ᎦᎾᏏᏁᎦ(방향,차이);ᎰᎯᏳᏓ_ᎢᎩᏓ()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ("echo '"+긴글+"'");숨고르기()
        ᏂᎬ_ᎯᏁᏟᏴᎾ_ᎦᎾᏏᏁᎦ(4,(-1000,-1000));assert ᏦᎳᏂ[2:]==[360,216]
        ᏂᎬ_ᎯᏁᏟᏴᎾ_ᎦᎾᏏᏁᎦ(4,(너비,높이))
        ᎠᎢᏎᏍᏗ=ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ᎠᎢᏎᏍᏗ);ᎰᎯᏳᏓ_ᎢᎩᏓ()
        # vi가 ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ᎤᏯᏍᎦ('ftpd start')
        ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ=ftplib.FTP();ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.encoding='utf-8';ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.connect('127.0.0.1',접속번호,timeout=20);ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.login()
        기다리기(b'NORMAL',ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('vi /크기자료.txt\n'))
        기다리기(b'INSERT',ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('i미저장 한글 ᎦᏟᏌᏅᎯ\n'));숨고르기()
        ᏂᎬ_ᎯᏁᏟᏴᎾ_ᎦᎾᏏᏁᎦ(4,(-너비,-높이))
        # ANSI ᎤᏓᏅᏅ_ᏧᎬᏩᎶᏗᏯ 이동에 새 ᎤᏓᏅᏅ_ᏧᎬᏩᎶᏗᏯ 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ᏦᎳᏂ[3]-56)//16)).encode() in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[-4096:]
        ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('작은 창에서도 이어 ᎪᏪᎶᏗ\n');숨고르기()
        ᏂᎬ_ᎯᏁᏟᏴᎾ_ᎦᎾᏏᏁᎦ(4,(너비,높이))
        ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ('큰 창에서도 이어 ᎪᏪᎶᏗ\n');숨고르기()
        ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(0xff1b);ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',ᏫᎦᏅᏗ_ᎠᎪᎵᏰᏗ(':wq\n'))
        ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ=bytearray();ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.retrbinary('RETR 크기자료.txt',ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.extend)
        assert ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ=='미저장 한글 ᎦᏟᏌᏅᎯ\n작은 창에서도 이어 ᎪᏪᎶᏗ\n큰 창에서도 이어 ᎪᏪᎶᏗ\n'.encode(),ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ
        ᎰᎯᏳᏓ_ᎢᎩᏓ().save(str(결과경로/(ᎢᎩᏓ_ᎠᎪᎵᏰᏗ+'-large.png')))
        # 두 번째 창은 ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ ᎢᎩᏓ, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ᎠᎢᏎᏍᏗ=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(70,16);기다리기(b'TERMINAL FOCUS 2',ᎠᎢᏎᏍᏗ)
        assert 'TERMINAL SIZE 68x19' in ᎤᏯᏍᎦ('terminal size')
        ᎠᎢᏎᏍᏗ=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(180,16);기다리기(b'TERMINAL FOCUS 1',ᎠᎢᏎᏍᏗ);ᎰᎯᏳᏓ_ᎢᎩᏓ()
        ᏂᎬ_ᎯᏁᏟᏴᎾ_ᎦᎾᏏᏁᎦ(4,(-너비,-높이));ᎰᎯᏳᏓ_ᎢᎩᏓ().save(str(결과경로/(ᎢᎩᏓ_ᎠᎪᎵᏰᏗ+'-small.png')))
        # ᎢᎩᏓ ᎯᏁᏟᏴᎾ_ᏧᎬᏩᎶᏗᏯ ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ᎠᎢᏎᏍᏗ=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(ᏦᎳᏂ[0]+ᏦᎳᏂ[2]-20,ᏦᎳᏂ[1]+15);기다리기(b'TERMINAL FOCUS 2',ᎠᎢᏎᏍᏗ)
        assert 'RESIZE CLOSED' in ᎤᏯᏍᎦ('echo RESIZE CLOSED')
        print('PASS:',ᎢᎩᏓ_ᎠᎪᎵᏰᏗ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ:ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.close()
        if 원격:원격.close()
        if ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is None:
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.terminate()
            try:ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=8)
            except subprocess.TimeoutExpired:ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.kill();ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait()
        ᎠᏑᏰᏍᎩ_a916db4e.close();ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdout.close();(결과경로/(ᎢᎩᏓ_ᎠᎪᎵᏰᏗ+'.log')).write_bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)


def ᎠᎢᏎᏍᏗ():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['resolutions'].append([너비,높이])
        ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ᎠᎢᏎᏍᏗ()
