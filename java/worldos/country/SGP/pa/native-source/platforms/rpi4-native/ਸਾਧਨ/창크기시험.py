#!/usr/bin/env python3
"""ਅਸਲ_ਸਮੱਗਰੀ QEMU/VNC에서 ਟਰਮੀਨਲ 모서리 ਖਿੱਚੋ_ਕੀਮਤ·ਪੌਇੰਟਰ·동적 ਵਰਣ_ਕੀਮਤ ਸਲੌਟ_ਦਾਖਲਾ·ਸੰਪਾਦਨ_ਕੀਮਤ ਤਤਕਰਾ_ਕੀਮਤ 보존를 검사한다."""
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
from ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼ import 정확한값
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def 창크기시험(너비, 높이, ਮਾਪ_ਰਸਤਾ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ਆਕਾਰ_ਪਾਠ = '{}x{}'.format(너비, 높이)
    ਕਾਰਵਾਈ_ਕੀਮਤ = subprocess.Popen(['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ਆਕਾਰ_ਪਾਠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ਚੋਣਕਰਤਾ_a916db4e = selectors.DefaultSelector(); ਚੋਣਕਰਤਾ_a916db4e.register(ਕਾਰਵਾਈ_ਕੀਮਤ.stdout, selectors.EVENT_READ)
    ਲੌਗ_ਕਤਾਰ = bytearray(); ਰਿਮੋਟ_ਕੀਮਤ = None; ਸਥਾਂਨਤਰ_ਕੀਮਤ = None; ਪੌਇੰਟਰ_ਲੁਕਿਆ_ਹੋਇਆ=[False]

    def 기다리기(ਸ਼ੋਅ_ਕੀਮਤ, ਚਲਾਓ_2=0):
        마감 = time.monotonic() + 60
        while ਸ਼ੋਅ_ਕੀਮਤ not in ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:]:
            if time.monotonic() > 마감 or ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None or b'HALTED' in ਲੌਗ_ਕਤਾਰ or b'PANIC:' in ਲੌਗ_ਕਤਾਰ:
                raise AssertionError(ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:].decode('utf-8', 'replace'))
            for ਇਵੈਂਟ, _ in ਚੋਣਕਰਤਾ_a916db4e.select(.1):
                ਸਮੱਗਰੀ = ਇਵੈਂਟ.fileobj.read(65536)
                if ਸਮੱਗਰੀ: ਲੌਗ_ਕਤਾਰ.extend(ਸਮੱਗਰੀ)
        return ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:].decode('utf-8', 'replace')

    def ਕਲਿਕ_ਕਰੋ_ਬਟਨ(ਪ੍ਰਤੀਕ, 눌림=True): ਰਿਮੋਟ_ਕੀਮਤ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ਪ੍ਰਤੀਕ))

    def SMS_ਭੇਜੋ(ਟੈਕਸਟ):
        ਚਲਾਓ_2 = len(ਲੌਗ_ਕਤਾਰ)
        for ਵਰਣ_ਕੀਮਤ in ਟੈਕਸਟ:
            ਪ੍ਰਤੀਕ = 0xff0d if ਵਰਣ_ਕੀਮਤ == '\n' else ord(ਵਰਣ_ਕੀਮਤ) if ord(ਵਰਣ_ਕੀਮਤ) < 256 else 0x1000000 | ord(ਵਰਣ_ਕੀਮਤ)
            ਕਲਿਕ_ਕਰੋ_ਬਟਨ(ਪ੍ਰਤੀਕ); ਕਲਿਕ_ਕਰੋ_ਬਟਨ(ਪ੍ਰਤੀਕ, False)
        return ਚਲਾਓ_2

    def ਸ਼ੈਲ(ਟੈਕਸਟ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_ਭੇਜੋ(ਟੈਕਸਟ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 눌림): ਰਿਮੋਟ_ਕੀਮਤ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ))

    def ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ): 가리키기(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 1); 가리키기(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 0)

    def ਬਿਟਮੈਪ_ਤਸਵੀਰ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ਅਸਲ_ਸਮੱਗਰੀ 너비를 쓴다.
        ਰਿਮੋਟ_ਕੀਮਤ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ = Image.new('RGB', (너비, 높이)); ਖੇਤਰ_ਕੀਮਤ = 0
        while True:
            종류 = 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ਲੰਬਾਈ_ਕੀਮਤ = struct.unpack('>I', 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 7)[3:])[0]; 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, ਲੰਬਾਈ_ਕੀਮਤ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 3)[1:])[0]
            for _ in range(개수):
                가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 폭, ਲੰਬਾਈ_ਕੀਮਤ, ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ_ਕੀਮਤ = struct.unpack('>HHHHi', 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 12))
                if ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ_ਕੀਮਤ == -239:
                    assert 폭==0 and ਲੰਬਾਈ_ਕੀਮਤ==0, 'remote cursor must be hidden'
                    ਪੌਇੰਟਰ_ਲੁਕਿਆ_ਹੋਇਆ[0]=True
                    continue
                assert ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ_ਕੀਮਤ == 0 and 가로+폭 <= 너비 and ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ+ਲੰਬਾਈ_ਕੀਮਤ <= 높이
                ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.paste(Image.frombytes('RGB', (폭, ਲੰਬਾਈ_ਕੀਮਤ), 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 폭*ਲੰਬਾਈ_ਕੀਮਤ*4), 'raw', 'BGRX'), (가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ))
                ਖੇਤਰ_ਕੀਮਤ += 폭*ਲੰਬਾਈ_ਕੀਮਤ
            if ਖੇਤਰ_ਕੀਮਤ:
                assert ਖੇਤਰ_ਕੀਮਤ == 너비*높이, ਖੇਤਰ_ਕੀਮਤ
                return ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ

    def ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ(ਸਮਾਨ_ਕੀਮਤ, 색):
        마감 = time.monotonic()+10
        while True:
            ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ = ਬਿਟਮੈਪ_ਤਸਵੀਰ()
            if ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.getpixel(ਸਮਾਨ_ਕੀਮਤ) == 색: return ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ
            if time.monotonic() > 마감: raise AssertionError((ਸਮਾਨ_ਕੀਮਤ, ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.getpixel(ਸਮਾਨ_ਕੀਮਤ), 색))

    def ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ(ਨਾਂ, ਸਮੱਗਰੀ): ਸਥਾਂਨਤਰ_ਕੀਮਤ.storbinary('STOR '+ਨਾਂ, io.BytesIO(ਸਮੱਗਰੀ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ਆਕਾਰ_ਪਾਠ+' RGB32').encode() in ਲੌਗ_ਕਤਾਰ
        print('BOOT:', ਆਕਾਰ_ਪਾਠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ਲੌਗ_ਕਤਾਰ).group(1))
        ਰਿਮੋਟ_ਕੀਮਤ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 12) == b'RFB 003.008\n'; ਰਿਮੋਟ_ਕੀਮਤ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 1)[0]); ਰਿਮੋਟ_ਕੀਮਤ.sendall(b'\x01')
        assert 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 4) == b'\0'*4; ਰਿਮੋਟ_ਕੀਮਤ.sendall(b'\x01')
        초기 = 정확한값(ਰਿਮੋਟ_ਕੀਮਤ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ਰਿਮੋਟ_ਕੀਮਤ, struct.unpack('>I', 초기[20:])[0])
        ਰਿਮੋਟ_ਕੀਮਤ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ਰਿਮੋਟ_ਕੀਮਤ.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ਇਵੈਂਟ,_ in ਚੋਣਕਰਤਾ_a916db4e.select(.02):
                    ਸਮੱਗਰੀ=ਇਵੈਂਟ.fileobj.read(65536)
                    if ਸਮੱਗਰੀ:ਲੌਗ_ਕਤਾਰ.extend(ਸਮੱਗਰੀ)
        ਵਿੰਡੋ=[12,48,568,360]
        def ਤਸਦੀਕ_ਆਕਾਰ():
            ਕੋਲਮ_ਕੀਮਤ,ਕਤਾਰ_ਕੀਮਤ=(ਵਿੰਡੋ[2]-24)//8,(ਵਿੰਡੋ[3]-56)//16
            ਟੈਕਸਟ=ਸ਼ੈਲ('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ਕੋਲਮ_ਕੀਮਤ,ਕਤਾਰ_ਕੀਮਤ) in ਟੈਕਸਟ,ਟੈਕਸਟ
            # ਅਸਲ_ਸਮੱਗਰੀ ਵਿੰਡੋ 테두리: 단지 ਆਕਾਰ ਪੜਤਾਲ_ਕੀਮਤ 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((ਵਿੰਡੋ[0],ਵਿੰਡੋ[1]),(32,80,144))
            ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ=ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ((ਵਿੰਡੋ[0]+ਵਿੰਡੋ[2]-1,ਵਿੰਡੋ[1]+ਵਿੰਡੋ[3]-1),(39,49,64))
            return ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ
        def 모서리(방향):
            return (ਵਿੰਡੋ[0]+(3 if 방향 in (1,3) else ਵਿੰਡੋ[2]-4),ਵਿੰਡੋ[1]+(3 if 방향<=2 else ਵਿੰਡੋ[3]-4))
        def ਮੁੜ_ਆਕਾਰ_ਬਣਾਓ_ਖਿੱਚੋ(방향,차이,ਬਟਨ=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ਚੈਕ_ਕਰੋ_ਬਿੰਦੂ(흰점,(255,255,255))
            가리키기(가,세,ਬਟਨ)
            끝가=max(0,min(너비-1,가+차이[0]));ਅੰਤ_ਲੰਬਵਤ=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ਅੰਤ_ਲੰਬਵਤ,ਬਟਨ);가리키기(끝가,ਅੰਤ_ਲੰਬਵਤ,0);숨고르기()
            if ਬਟਨ==1:
                왼,위,폭,ਲੰਬਾਈ_ਕੀਮਤ=ਵਿੰਡੋ;오른,아래=왼+폭,위+ਲੰਬਾਈ_ਕੀਮਤ
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ਅੰਤ_ਲੰਬਵਤ-세))
                else:아래=max(위+216,min(높이,아래+ਅੰਤ_ਲੰਬਵਤ-세))
                ਵਿੰਡੋ[:]=[왼,위,오른-왼,아래-위]
        ਤਸਦੀਕ_ਆਕਾਰ();assert ਪੌਇੰਟਰ_ਲੁਕਿਆ_ਹੋਇਆ[0]
        ਮੁੜ_ਆਕਾਰ_ਬਣਾਓ_ਖਿੱਚੋ(4,(-100,-60),4);ਤਸਦੀਕ_ਆਕਾਰ() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ਮੁੜ_ਆਕਾਰ_ਬਣਾਓ_ਖਿੱਚੋ(방향,차이);ਤਸਦੀਕ_ਆਕਾਰ()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_ਭੇਜੋ("echo '"+긴글+"'");숨고르기()
        ਮੁੜ_ਆਕਾਰ_ਬਣਾਓ_ਖਿੱਚੋ(4,(-1000,-1000));assert ਵਿੰਡੋ[2:]==[360,216]
        ਮੁੜ_ਆਕਾਰ_ਬਣਾਓ_ਖਿੱਚੋ(4,(너비,높이))
        ਚਲਾਓ_2=SMS_ਭੇਜੋ('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ਚਲਾਓ_2);ਤਸਦੀਕ_ਆਕਾਰ()
        # vi가 ਸੰਪਾਦਨ_ਕੀਮਤ 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ਸ਼ੈਲ('ftpd start')
        ਸਥਾਂਨਤਰ_ਕੀਮਤ=ftplib.FTP();ਸਥਾਂਨਤਰ_ਕੀਮਤ.encoding='utf-8';ਸਥਾਂਨਤਰ_ਕੀਮਤ.connect('127.0.0.1',접속번호,timeout=20);ਸਥਾਂਨਤਰ_ਕੀਮਤ.login()
        기다리기(b'NORMAL',SMS_ਭੇਜੋ('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_ਭੇਜੋ('i미저장 한글 ਸਮੱਗਰੀ\n'));숨고르기()
        ਮੁੜ_ਆਕਾਰ_ਬਣਾਓ_ਖਿੱਚੋ(4,(-너비,-높이))
        # ANSI ਕਤਾਰ_ਕੀਮਤ 이동에 새 ਕਤਾਰ_ਕੀਮਤ 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ਵਿੰਡੋ[3]-56)//16)).encode() in ਲੌਗ_ਕਤਾਰ[-4096:]
        SMS_ਭੇਜੋ('작은 창에서도 이어 ਲਿਖਣ\n');숨고르기()
        ਮੁੜ_ਆਕਾਰ_ਬਣਾਓ_ਖਿੱਚੋ(4,(너비,높이))
        SMS_ਭੇਜੋ('큰 창에서도 이어 ਲਿਖਣ\n');숨고르기()
        ਕਲਿਕ_ਕਰੋ_ਬਟਨ(0xff1b);ਕਲਿਕ_ਕਰੋ_ਬਟਨ(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_ਭੇਜੋ(':wq\n'))
        ਤਤਕਰਾ_ਕੀਮਤ=bytearray();ਸਥਾਂਨਤਰ_ਕੀਮਤ.retrbinary('RETR 크기자료.txt',ਤਤਕਰਾ_ਕੀਮਤ.extend)
        assert ਤਤਕਰਾ_ਕੀਮਤ=='미저장 한글 ਸਮੱਗਰੀ\n작은 창에서도 이어 ਲਿਖਣ\n큰 창에서도 이어 ਲਿਖਣ\n'.encode(),ਤਤਕਰਾ_ਕੀਮਤ
        ਤਸਦੀਕ_ਆਕਾਰ().save(str(ਮਾਪ_ਰਸਤਾ/(ਆਕਾਰ_ਪਾਠ+'-large.png')))
        # 두 번째 창은 ਡਿਫੌਲਟ_ਵੈਲਯੂ ਆਕਾਰ, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ਚਲਾਓ_2=len(ਲੌਗ_ਕਤਾਰ);ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(70,16);기다리기(b'TERMINAL FOCUS 2',ਚਲਾਓ_2)
        assert 'TERMINAL SIZE 68x19' in ਸ਼ੈਲ('terminal size')
        ਚਲਾਓ_2=len(ਲੌਗ_ਕਤਾਰ);ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(180,16);기다리기(b'TERMINAL FOCUS 1',ਚਲਾਓ_2);ਤਸਦੀਕ_ਆਕਾਰ()
        ਮੁੜ_ਆਕਾਰ_ਬਣਾਓ_ਖਿੱਚੋ(4,(-너비,-높이));ਤਸਦੀਕ_ਆਕਾਰ().save(str(ਮਾਪ_ਰਸਤਾ/(ਆਕਾਰ_ਪਾਠ+'-small.png')))
        # ਆਕਾਰ ਬਦਲੋ_ਕੀਮਤ ਪਿਛਲਾ_ਕੀਮਤ X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ਚਲਾਓ_2=len(ਲੌਗ_ਕਤਾਰ);ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(ਵਿੰਡੋ[0]+ਵਿੰਡੋ[2]-20,ਵਿੰਡੋ[1]+15);기다리기(b'TERMINAL FOCUS 2',ਚਲਾਓ_2)
        assert 'RESIZE CLOSED' in ਸ਼ੈਲ('echo RESIZE CLOSED')
        print('PASS:',ਆਕਾਰ_ਪਾਠ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ਸਥਾਂਨਤਰ_ਕੀਮਤ:ਸਥਾਂਨਤਰ_ਕੀਮਤ.close()
        if ਰਿਮੋਟ_ਕੀਮਤ:ਰਿਮੋਟ_ਕੀਮਤ.close()
        if ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is None:
            ਕਾਰਵਾਈ_ਕੀਮਤ.terminate()
            try:ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=8)
            except subprocess.TimeoutExpired:ਕਾਰਵਾਈ_ਕੀਮਤ.kill();ਕਾਰਵਾਈ_ਕੀਮਤ.wait()
        ਚੋਣਕਰਤਾ_a916db4e.close();ਕਾਰਵਾਈ_ਕੀਮਤ.stdout.close();(ਮਾਪ_ਰਸਤਾ/(ਆਕਾਰ_ਪਾਠ+'.log')).write_bytes(ਲੌਗ_ਕਤਾਰ)


def ਚਲਾਓ_2():
    ਮਾਪ_ਰਸਤਾ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/resize';ਮਾਪ_ਰਸਤਾ.mkdir(parents=True,exist_ok=True)
    ਲੌਗ_ਕਤਾਰ={'passed':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,ਮਾਪ_ਰਸਤਾ);ਲੌਗ_ਕਤਾਰ['resolutions'].append([너비,높이])
        ਲੌਗ_ਕਤਾਰ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ਮਾਪ_ਰਸਤਾ/'report.json').write_text(json.dumps(ਲੌਗ_ਕਤਾਰ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ਚਲਾਓ_2()
