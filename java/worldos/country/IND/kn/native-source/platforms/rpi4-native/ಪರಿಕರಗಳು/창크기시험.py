#!/usr/bin/env python3
"""ನಿಜವಾದ_ಡೇಟಾ QEMU/VNC에서 ಟರ್ಮಿನಲ್ 모서리 ಜಗ್ಗು_ಮೌಲ್ಯ·ಸೂಚಕ·동적 ಅಕ್ಷರ_ಮೌಲ್ಯ ಸ್ಲಾಟ್_ನಮೂದು·ಸಂಪಾದನೆ_ಮೌಲ್ಯ ವಿಷಯ_ಮೌಲ್ಯ 보존를 검사한다."""
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
from ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ import 정확한값
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def 창크기시험(너비, 높이, ಮಾಪನ_ಹಾದಿ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = 임시.getsockname()[1]
    ಗಾತ್ರಿಸು_ಪಠ್ಯ = '{}x{}'.format(너비, 높이)
    ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = subprocess.Popen(['python3', str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), '--resolution', ಗಾತ್ರಿಸು_ಪಠ್ಯ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ಸೆಲೆಕ್ಟರ್_a916db4e = selectors.DefaultSelector(); ಸೆಲೆಕ್ಟರ್_a916db4e.register(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdout, selectors.EVENT_READ)
    ಲಾಗ್_ದಾಖಲೆ = bytearray(); ರಿಮೋಟ್_ಮೌಲ್ಯ = None; ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ = None; ಸೂಚಕ_ಹುದುಗಿಟ್ಟ=[False]

    def 기다리기(ಶೋ_ಮೌಲ್ಯ, ಚಲಾಯಿಸು_2=0):
        마감 = time.monotonic() + 60
        while ಶೋ_ಮೌಲ್ಯ not in ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:]:
            if time.monotonic() > 마감 or ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None or b'HALTED' in ಲಾಗ್_ದಾಖಲೆ or b'PANIC:' in ಲಾಗ್_ದಾಖಲೆ:
                raise AssertionError(ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:].decode('utf-8', 'replace'))
            for ಸಂಗತಿ, _ in ಸೆಲೆಕ್ಟರ್_a916db4e.select(.1):
                ಡೇಟಾ = ಸಂಗತಿ.fileobj.read(65536)
                if ಡೇಟಾ: ಲಾಗ್_ದಾಖಲೆ.extend(ಡೇಟಾ)
        return ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:].decode('utf-8', 'replace')

    def ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(ಚಿಹ್ನೆ, 눌림=True): ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ಚಿಹ್ನೆ))

    def SMS_ಕಳುಹಿಸು(ಪಠ್ಯ):
        ಚಲಾಯಿಸು_2 = len(ಲಾಗ್_ದಾಖಲೆ)
        for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಪಠ್ಯ:
            ಚಿಹ್ನೆ = 0xff0d if ಅಕ್ಷರ_ಮೌಲ್ಯ == '\n' else ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) if ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) < 256 else 0x1000000 | ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)
            ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(ಚಿಹ್ನೆ); ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(ಚಿಹ್ನೆ, False)
        return ಚಲಾಯಿಸು_2

    def ಶೆಲ್(ಪಠ್ಯ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_ಕಳುಹಿಸು(ಪಠ್ಯ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, ಲಂಬ_ಹುದ್ದೆ, 눌림): ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ಲಂಬ_ಹುದ್ದೆ))

    def ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(가로, ಲಂಬ_ಹುದ್ದೆ): 가리키기(가로, ಲಂಬ_ಹುದ್ದೆ, 1); 가리키기(가로, ಲಂಬ_ಹುದ್ದೆ, 0)

    def ಬಿಟ್_ಮ್ಯಾಪ್_ಇಮೇಜ್():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ನಿಜವಾದ_ಡೇಟಾ 너비를 쓴다.
        ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ = Image.new('RGB', (너비, 높이)); ವರ್ಗ_ಮೌಲ್ಯ_9285603e = 0
        while True:
            종류 = 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ಉದ್ದ_ಮೌಲ್ಯ = struct.unpack('>I', 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 7)[3:])[0]; 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, ಉದ್ದ_ಮೌಲ್ಯ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 3)[1:])[0]
            for _ in range(개수):
                가로, ಲಂಬ_ಹುದ್ದೆ, 폭, ಉದ್ದ_ಮೌಲ್ಯ, ಎನ್ಕೋಡಿಂಗ್_ಮೌಲ್ಯ = struct.unpack('>HHHHi', 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 12))
                if ಎನ್ಕೋಡಿಂಗ್_ಮೌಲ್ಯ == -239:
                    assert 폭==0 and ಉದ್ದ_ಮೌಲ್ಯ==0, 'remote cursor must be hidden'
                    ಸೂಚಕ_ಹುದುಗಿಟ್ಟ[0]=True
                    continue
                assert ಎನ್ಕೋಡಿಂಗ್_ಮೌಲ್ಯ == 0 and 가로+폭 <= 너비 and ಲಂಬ_ಹುದ್ದೆ+ಉದ್ದ_ಮೌಲ್ಯ <= 높이
                ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.paste(Image.frombytes('RGB', (폭, ಉದ್ದ_ಮೌಲ್ಯ), 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 폭*ಉದ್ದ_ಮೌಲ್ಯ*4), 'raw', 'BGRX'), (가로, ಲಂಬ_ಹುದ್ದೆ))
                ವರ್ಗ_ಮೌಲ್ಯ_9285603e += 폭*ಉದ್ದ_ಮೌಲ್ಯ
            if ವರ್ಗ_ಮೌಲ್ಯ_9285603e:
                assert ವರ್ಗ_ಮೌಲ್ಯ_9285603e == 너비*높이, ವರ್ಗ_ಮೌಲ್ಯ_9285603e
                return ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ

    def ಚೆಕ್_ಪೆಲ್(ಸಮನ್ವಯ_ಮೌಲ್ಯ, 색):
        마감 = time.monotonic()+10
        while True:
            ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ = ಬಿಟ್_ಮ್ಯಾಪ್_ಇಮೇಜ್()
            if ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.getpixel(ಸಮನ್ವಯ_ಮೌಲ್ಯ) == 색: return ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ
            if time.monotonic() > 마감: raise AssertionError((ಸಮನ್ವಯ_ಮೌಲ್ಯ, ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.getpixel(ಸಮನ್ವಯ_ಮೌಲ್ಯ), 색))

    def ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು(ಹೆಸರು, ಡೇಟಾ): ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.storbinary('STOR '+ಹೆಸರು, io.BytesIO(ಡೇಟಾ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ಗಾತ್ರಿಸು_ಪಠ್ಯ+' RGB32').encode() in ಲಾಗ್_ದಾಖಲೆ
        print('BOOT:', ಗಾತ್ರಿಸು_ಪಠ್ಯ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ಲಾಗ್_ದಾಖಲೆ).group(1))
        ರಿಮೋಟ್_ಮೌಲ್ಯ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 12) == b'RFB 003.008\n'; ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 1)[0]); ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(b'\x01')
        assert 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 4) == b'\0'*4; ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(b'\x01')
        초기 = 정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ರಿಮೋಟ್_ಮೌಲ್ಯ, struct.unpack('>I', 초기[20:])[0])
        ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ರಿಮೋಟ್_ಮೌಲ್ಯ.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ಚೆಕ್_ಪೆಲ್((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ಸಂಗತಿ,_ in ಸೆಲೆಕ್ಟರ್_a916db4e.select(.02):
                    ಡೇಟಾ=ಸಂಗತಿ.fileobj.read(65536)
                    if ಡೇಟಾ:ಲಾಗ್_ದಾಖಲೆ.extend(ಡೇಟಾ)
        ವಿಂಡೋ=[12,48,568,360]
        def ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಗಾತ್ರಿಸು():
            ಲಂಬಸಾಲು_ಮೌಲ್ಯ,ಅಡ್ಡಸಾಲು_ಮೌಲ್ಯ=(ವಿಂಡೋ[2]-24)//8,(ವಿಂಡೋ[3]-56)//16
            ಪಠ್ಯ=ಶೆಲ್('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ಲಂಬಸಾಲು_ಮೌಲ್ಯ,ಅಡ್ಡಸಾಲು_ಮೌಲ್ಯ) in ಪಠ್ಯ,ಪಠ್ಯ
            # ನಿಜವಾದ_ಡೇಟಾ ವಿಂಡೋ 테두리: 단지 ಗಾತ್ರ ಪ್ರಶ್ನಾವಳಿ_ಮೌಲ್ಯ 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ಚೆಕ್_ಪೆಲ್((ವಿಂಡೋ[0],ವಿಂಡೋ[1]),(32,80,144))
            ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ=ಚೆಕ್_ಪೆಲ್((ವಿಂಡೋ[0]+ವಿಂಡೋ[2]-1,ವಿಂಡೋ[1]+ವಿಂಡೋ[3]-1),(39,49,64))
            return ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ
        def 모서리(방향):
            return (ವಿಂಡೋ[0]+(3 if 방향 in (1,3) else ವಿಂಡೋ[2]-4),ವಿಂಡೋ[1]+(3 if 방향<=2 else ವಿಂಡೋ[3]-4))
        def ಗಾತ್ರ_ಮರುಹೊಂದಿಸು_ಜಗ್ಗು(방향,차이,ಬಟನ್=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ಚೆಕ್_ಪೆಲ್(흰점,(255,255,255))
            가리키기(가,세,ಬಟನ್)
            끝가=max(0,min(너비-1,가+차이[0]));ಅಂತ್ಯಗೊಳಿಸು_ಲಂಬ=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ಅಂತ್ಯಗೊಳಿಸು_ಲಂಬ,ಬಟನ್);가리키기(끝가,ಅಂತ್ಯಗೊಳಿಸು_ಲಂಬ,0);숨고르기()
            if ಬಟನ್==1:
                왼,위,폭,ಉದ್ದ_ಮೌಲ್ಯ=ವಿಂಡೋ;오른,아래=왼+폭,위+ಉದ್ದ_ಮೌಲ್ಯ
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ಅಂತ್ಯಗೊಳಿಸು_ಲಂಬ-세))
                else:아래=max(위+216,min(높이,아래+ಅಂತ್ಯಗೊಳಿಸು_ಲಂಬ-세))
                ವಿಂಡೋ[:]=[왼,위,오른-왼,아래-위]
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಗಾತ್ರಿಸು();assert ಸೂಚಕ_ಹುದುಗಿಟ್ಟ[0]
        ಗಾತ್ರ_ಮರುಹೊಂದಿಸು_ಜಗ್ಗು(4,(-100,-60),4);ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಗಾತ್ರಿಸು() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ಗಾತ್ರ_ಮರುಹೊಂದಿಸು_ಜಗ್ಗು(방향,차이);ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಗಾತ್ರಿಸು()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_ಕಳುಹಿಸು("echo '"+긴글+"'");숨고르기()
        ಗಾತ್ರ_ಮರುಹೊಂದಿಸು_ಜಗ್ಗು(4,(-1000,-1000));assert ವಿಂಡೋ[2:]==[360,216]
        ಗಾತ್ರ_ಮರುಹೊಂದಿಸು_ಜಗ್ಗು(4,(너비,높이))
        ಚಲಾಯಿಸು_2=SMS_ಕಳುಹಿಸು('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ಚಲಾಯಿಸು_2);ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಗಾತ್ರಿಸು()
        # vi가 ಸಂಪಾದನೆ_ಮೌಲ್ಯ 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ಶೆಲ್('ftpd start')
        ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ=ftplib.FTP();ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.encoding='utf-8';ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.connect('127.0.0.1',ಪೋರ್ಟ್_ಸಂಖ್ಯೆ,timeout=20);ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.login()
        기다리기(b'NORMAL',SMS_ಕಳುಹಿಸು('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_ಕಳುಹಿಸು('i미저장 한글 ಡೇಟಾ\n'));숨고르기()
        ಗಾತ್ರ_ಮರುಹೊಂದಿಸು_ಜಗ್ಗು(4,(-너비,-높이))
        # ANSI ಅಡ್ಡಸಾಲು_ಮೌಲ್ಯ 이동에 새 ಅಡ್ಡಸಾಲು_ಮೌಲ್ಯ 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ವಿಂಡೋ[3]-56)//16)).encode() in ಲಾಗ್_ದಾಖಲೆ[-4096:]
        SMS_ಕಳುಹಿಸು('작은 창에서도 이어 ಬರೆ\n');숨고르기()
        ಗಾತ್ರ_ಮರುಹೊಂದಿಸು_ಜಗ್ಗು(4,(너비,높이))
        SMS_ಕಳುಹಿಸು('큰 창에서도 이어 ಬರೆ\n');숨고르기()
        ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(0xff1b);ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_ಕಳುಹಿಸು(':wq\n'))
        ವಿಷಯ_ಮೌಲ್ಯ=bytearray();ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.retrbinary('RETR 크기자료.txt',ವಿಷಯ_ಮೌಲ್ಯ.extend)
        assert ವಿಷಯ_ಮೌಲ್ಯ=='미저장 한글 ಡೇಟಾ\n작은 창에서도 이어 ಬರೆ\n큰 창에서도 이어 ಬರೆ\n'.encode(),ವಿಷಯ_ಮೌಲ್ಯ
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಗಾತ್ರಿಸು().save(str(ಮಾಪನ_ಹಾದಿ/(ಗಾತ್ರಿಸು_ಪಠ್ಯ+'-large.png')))
        # 두 번째 창은 ಅಕ್ಷಮ_ಬೆಲೆ ಗಾತ್ರ, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ಚಲಾಯಿಸು_2=len(ಲಾಗ್_ದಾಖಲೆ);ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(70,16);기다리기(b'TERMINAL FOCUS 2',ಚಲಾಯಿಸು_2)
        assert 'TERMINAL SIZE 68x19' in ಶೆಲ್('terminal size')
        ಚಲಾಯಿಸು_2=len(ಲಾಗ್_ದಾಖಲೆ);ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(180,16);기다리기(b'TERMINAL FOCUS 1',ಚಲಾಯಿಸು_2);ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಗಾತ್ರಿಸು()
        ಗಾತ್ರ_ಮರುಹೊಂದಿಸು_ಜಗ್ಗು(4,(-너비,-높이));ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಗಾತ್ರಿಸು().save(str(ಮಾಪನ_ಹಾದಿ/(ಗಾತ್ರಿಸು_ಪಠ್ಯ+'-small.png')))
        # ಗಾತ್ರ ಬದಲಿಸು_ಮೌಲ್ಯ ಹಿಂದೆ_ಮೌಲ್ಯ X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ಚಲಾಯಿಸು_2=len(ಲಾಗ್_ದಾಖಲೆ);ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(ವಿಂಡೋ[0]+ವಿಂಡೋ[2]-20,ವಿಂಡೋ[1]+15);기다리기(b'TERMINAL FOCUS 2',ಚಲಾಯಿಸು_2)
        assert 'RESIZE CLOSED' in ಶೆಲ್('echo RESIZE CLOSED')
        print('PASS:',ಗಾತ್ರಿಸು_ಪಠ್ಯ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ:ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.close()
        if ರಿಮೋಟ್_ಮೌಲ್ಯ:ರಿಮೋಟ್_ಮೌಲ್ಯ.close()
        if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is None:
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.terminate()
            try:ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=8)
            except subprocess.TimeoutExpired:ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.kill();ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait()
        ಸೆಲೆಕ್ಟರ್_a916db4e.close();ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdout.close();(ಮಾಪನ_ಹಾದಿ/(ಗಾತ್ರಿಸು_ಪಠ್ಯ+'.log')).write_bytes(ಲಾಗ್_ದಾಖಲೆ)


def ಚಲಾಯಿಸು_2():
    ಮಾಪನ_ಹಾದಿ=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/resize';ಮಾಪನ_ಹಾದಿ.mkdir(parents=True,exist_ok=True)
    ಲಾಗ್_ದಾಖಲೆ={'passed':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,ಮಾಪನ_ಹಾದಿ);ಲಾಗ್_ದಾಖಲೆ['resolutions'].append([너비,높이])
        ಲಾಗ್_ದಾಖಲೆ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ಮಾಪನ_ಹಾದಿ/'report.json').write_text(json.dumps(ಲಾಗ್_ದಾಖಲೆ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ಚಲಾಯಿಸು_2()
