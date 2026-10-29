#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ಕೀ_ಮೌಲ್ಯ 입력은 자체 ಕರ್ನಲ್_ಮೌಲ್ಯ UART로 전달한다. localhost 전용, 단일 ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ 클라이언트.
RFB 3.8: https://www.rfc-editor.org/rfc/rfc6143.html
"""
import argparse
from contextlib import ExitStack
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from ಪೂರೈಸು_ಆದೇಶ import ಆಜ್ಞೆ
from local_input import create


def 정확한값(소켓, ಗಾತ್ರ):
    ಡೇಟಾ = bytearray()
    while len(ಡೇಟಾ) < ಗಾತ್ರ:
        조각 = 소켓.recv(ಗಾತ್ರ - len(ಡೇಟಾ))
        if not 조각: raise EOFError()
        ಡೇಟಾ.extend(조각)
    return bytes(ಡೇಟಾ)


class ಕೀಲಿಮಣೆ:
    def __init__(자신, ಕಳುಹಿಸಿ, 입력방식알림=None):
        자신.바이트전송 = ಕಳುಹಿಸಿ; 자신.ಮಾಡಿಫಯರ್_ಕೀಲಿ = set(); 자신.ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ = b''
        자신.한글조합기 = create(ಕಳುಹಿಸಿ, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ಸ್ವಿಚ್_ಮಾಡಿ_ಕೀ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ಕಳುಹಿಸಿ(자신, ಡೇಟಾ):
        자신.한글조합기.조합확정()
        자신.바이트전송(ಡೇಟಾ)

    def ಸ್ವಿಚ್_ಮಾಡಿ_ಮೋಡ್(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ಕೀ_ಚಿಹ್ನೆ):
        if ಕೀ_ಚಿಹ್ನೆ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ಮಾಡಿಫಯರ್_ಕೀಲಿ.add(ಕೀ_ಚಿಹ್ನೆ)
            else: 자신.ಮಾಡಿಫಯರ್_ಕೀಲಿ.discard(ಕೀ_ಚಿಹ್ನೆ)
            return
        if not 누르는중:
            자신.ಸ್ವಿಚ್_ಮಾಡಿ_ಕೀ.discard(ಕೀ_ಚಿಹ್ನೆ)
            return
        ಕೀಲಿ = bool(자신.ಮಾಡಿಫಯರ್_ಕೀಲಿ & {0xffe3, 0xffe4})
        SHIFT_ಕೀಲಿ = bool(자신.ಮಾಡಿಫಯರ್_ಕೀಲಿ & {0xffe1, 0xffe2})
        if ಕೀಲಿ and SHIFT_ಕೀಲಿ and ಕೀ_ಚಿಹ್ನೆ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ಕೀ_ಚಿಹ್ನೆ in (32,0xff0d):
                try:
                    ಮೌಲ್ಯ=int(자신.유니코드입력,16)
                    if 32<=ಮೌಲ್ಯ<=0x10ffff and not 0xd800<=ಮೌಲ್ಯ<=0xdfff: 자신.ಕಳುಹಿಸಿ(chr(ಮೌಲ್ಯ).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ಕೀ_ಚಿಹ್ನೆ==0xff1b: 자신.유니코드입력=None
            elif ಕೀ_ಚಿಹ್ನೆ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ಕೀ_ಚಿಹ್ನೆ<128 and chr(ಕೀ_ಚಿಹ್ನೆ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ಕೀ_ಚಿಹ್ನೆ)
            return
        if ಕೀ_ಚಿಹ್ನೆ in (0xff31,0xffc6) or ಕೀ_ಚಿಹ್ನೆ==32 and SHIFT_ಕೀಲಿ and not ಕೀಲಿ:
            if ಕೀ_ಚಿಹ್ನೆ not in 자신.ಸ್ವಿಚ್_ಮಾಡಿ_ಕೀ: 자신.ಸ್ವಿಚ್_ಮಾಡಿ_ಮೋಡ್()
            자신.ಸ್ವಿಚ್_ಮಾಡಿ_ಕೀ.add(ಕೀ_ಚಿಹ್ನೆ)
            return
        if ಕೀ_ಚಿಹ್ನೆ==0xff08 and 자신.한글여부 and not ಕೀಲಿ and 자신.한글조합기.앞글자지우기(): return
        if ಕೀಲಿ and SHIFT_ಕೀಲಿ and ಕೀ_ಚಿಹ್ನೆ in (ord('t'),ord('T')):
            자신.ಕಳುಹಿಸಿ(bytes([30,2,1,0,0,0,0])); return
        if ಕೀ_ಚಿಹ್ನೆ==0xffc3: 자신.ಕಳುಹಿಸಿ(bytes([30,2,2,0,0,0,0])); return
        if ಕೀ_ಚಿಹ್ನೆ==0xffc9: 자신.ಕಳುಹಿಸಿ(bytes([30,2,3,0,0,0,0])); return
        if ಕೀಲಿ and SHIFT_ಕೀಲಿ and ಕೀ_ಚಿಹ್ನೆ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ಕಳುಹಿಸಿ(자신.ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ಕೀ_ಚಿಹ್ನೆ in 특수글쇠: 자신.ಕಳುಹಿಸಿ(특수글쇠[ಕೀ_ಚಿಹ್ನೆ]); return
        ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ = ಕೀ_ಚಿಹ್ನೆ & 0xffffff if ಕೀ_ಚಿಹ್ನೆ & 0xff000000 == 0x01000000 else ಕೀ_ಚಿಹ್ನೆ
        if ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ > 0x10ffff or 0xd800 <= ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ <= 0xdfff or ಕೀ_ಚಿಹ್ನೆ >= 0xff00 and ಕೀ_ಚಿಹ್ನೆ < 0x1000000: return
        if ಕೀಲಿ and 0x40 <= ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ <= 0x7f: 자신.ಕಳುಹಿಸಿ(bytes([ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ & 31])); return
        if ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ < 32: return
        if 자신.한글여부 and 자신.ಮಾಡಿಫಯರ್_ಕೀಲಿ & {0xffea,0xfe03,0xff7e} and not ಕೀಲಿ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ಫೀಡ್_ಕೀ(chr(ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್), altgr=True): return
        앞부분 = b'\x1b' if 자신.ಮಾಡಿಫಯರ್_ಕೀಲಿ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not ಕೀಲಿ and not 앞부분 and 32<=ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್<127:
            ಅಕ್ಷರ_ಡೇಟಾ=chr(ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್).upper() if SHIFT_ಕೀಲಿ else chr(ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್)
            if 자신.한글조합기.ಫೀಡ್_ಕೀ(ಅಕ್ಷರ_ಡೇಟಾ): return
        자신.ಕಳುಹಿಸಿ(앞부분 + chr(ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್).encode('utf-8'))


class ಕನೆಕ್ಟ್_ಡೆಸ್ಕ್_ಟಾಪ್:
    def __init__(자신, ಪ್ರಕ್ರಿಯೆ):
        자신.ಪ್ರಕ್ರಿಯೆ=ಪ್ರಕ್ರಿಯೆ; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.ಟರ್ಮಿನಲ್=False; 자신.시작화면=False; 자신.닫힘=False

    def ಕಳುಹಿಸಿ(자신, ಡೇಟಾ):
        if not ಡೇಟಾ or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.ಪ್ರಕ್ರಿಯೆ.stdin.write(ಡೇಟಾ); 자신.ಪ್ರಕ್ರಿಯೆ.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ಡೇಟಾ=자신.ಪ್ರಕ್ರಿಯೆ.stdout.read(4096)
                if not ಡೇಟಾ: break
                sys.stdout.buffer.write(ಡೇಟಾ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ಡೇಟಾ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ಟರ್ಮಿನಲ್=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ಕಳುಹಿಸಿ(b'terminal\n')
        finally: 자신.닫힘=True

    def ಕ್ಲೈಂಟ್(자신, ಕ್ಲೈಂಟ್, ಮಾರ್ಗ):
        ಸರ್ವರ್_ಮೌಲ್ಯ=socket.socket(socket.AF_UNIX); ಸರ್ವರ್_ಮೌಲ್ಯ.settimeout(10); ಕ್ಲೈಂಟ್.settimeout(10)
        ಕೀಲಿಮಣೆ_ನಮೂದು=ಕೀಲಿಮಣೆ(자신.ಕಳುಹಿಸಿ,lambda 한글여부:자신.ಕಳುಹಿಸಿ(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ಸರ್ವರ್_ಮೌಲ್ಯ.connect(str(ಮಾರ್ಗ))
            # 초기 협상은 순서대로 끝낸다. 이후 ಔಟ್_ಪುಟ್ 가닥만 클라이언트에 쓴다.
            ಕ್ಲೈಂಟ್.sendall(정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,12))
            판번호=정확한값(ಕ್ಲೈಂಟ್,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ಸರ್ವರ್_ಮೌಲ್ಯ.sendall(판번호)
            개수=정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,1);ಕ್ಲೈಂಟ್.sendall(개수+정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,개수[0]))
            ಭದ್ರತೆ=정확한값(ಕ್ಲೈಂಟ್,1)
            if ಭದ್ರತೆ!=b'\x01': raise ValueError('unexpected security type')
            ಸರ್ವರ್_ಮೌಲ್ಯ.sendall(ಭದ್ರತೆ)
            if 판번호==b'RFB 003.008\n':ಕ್ಲೈಂಟ್.sendall(정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,4))
            ಸರ್ವರ್_ಮೌಲ್ಯ.sendall(정확한값(ಕ್ಲೈಂಟ್,1))
            초기값=정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,24)
            ಕ್ಲೈಂಟ್.sendall(초기값+정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ಕ್ಲೈಂಟ್.settimeout(None);ಸರ್ವರ್_ಮೌಲ್ಯ.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ವರ್ಗ_ಮೌಲ್ಯ=정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,1)[0]
                        if ವರ್ಗ_ಮೌಲ್ಯ==0:
                            머리=정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ರಿಮೋಟ್_ಮೌಲ್ಯ 포인터의 중복을 피한다.
                            ಹುದುಗಿಟ್ಟ_ಮೌಲ್ಯ=포인터지원
                            if ಹುದುಗಿಟ್ಟ_ಮೌಲ್ಯ:ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ಕ್ಲೈಂಟ್.sendall(bytes([ವರ್ಗ_ಮೌಲ್ಯ])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,12);가로,ಲಂಬ_ಹುದ್ದೆ,폭,높이,ಎನ್ಕೋಡಿಂಗ್_ಮೌಲ್ಯ=struct.unpack('>HHHHi',사각형)
                                if ಎನ್ಕೋಡಿಂಗ್_ಮೌಲ್ಯ!=0:raise ValueError('unexpected framebuffer encoding: '+str(ಎನ್ಕೋಡಿಂಗ್_ಮೌಲ್ಯ))
                                ಕ್ಲೈಂಟ್.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ಡೇಟಾ=정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,min(남음,65536));ಕ್ಲೈಂಟ್.sendall(ಡೇಟಾ);남음-=len(ಡೇಟಾ)
                        elif ವರ್ಗ_ಮೌಲ್ಯ==1:
                            머리=정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,5);개수=struct.unpack('>H',머리[3:])[0]
                            ಕ್ಲೈಂಟ್.sendall(bytes([ವರ್ಗ_ಮೌಲ್ಯ])+머리+정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,개수*6))
                        elif ವರ್ಗ_ಮೌಲ್ಯ==2:ಕ್ಲೈಂಟ್.sendall(bytes([ವರ್ಗ_ಮೌಲ್ಯ]))
                        elif ವರ್ಗ_ಮೌಲ್ಯ==3:
                            머리=정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ಕ್ಲೈಂಟ್.sendall(bytes([ವರ್ಗ_ಮೌಲ್ಯ])+머리+정확한값(ಸರ್ವರ್_ಮೌಲ್ಯ,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ವರ್ಗ_ಮೌಲ್ಯ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ಕ್ಲೈಂಟ್.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ವರ್ಗ_ಮೌಲ್ಯ=정확한값(ಕ್ಲೈಂಟ್,1)[0]
                if ವರ್ಗ_ಮೌಲ್ಯ==4:
                    ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,7); ಕೀಲಿಮಣೆ_ನಮೂದು.누름값(ಮುಖ್ಯ_ಪಠ್ಯ[0]!=0,struct.unpack('>I',ಮುಖ್ಯ_ಪಠ್ಯ[3:])[0]); continue
                if ವರ್ಗ_ಮೌಲ್ಯ==255:
                    ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,11)
                    if ಮುಖ್ಯ_ಪಠ್ಯ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ಕೀಲಿಮಣೆ_ನಮೂದು.누름값(struct.unpack('>H',ಮುಖ್ಯ_ಪಠ್ಯ[1:3])[0]!=0,struct.unpack('>I',ಮುಖ್ಯ_ಪಠ್ಯ[3:7])[0]); continue
                if ವರ್ಗ_ಮೌಲ್ಯ==5:
                    ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,5); 단추들,x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ=struct.unpack('>BHH',ಮುಖ್ಯ_ಪಠ್ಯ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ಕೀಲಿಮಣೆ_ನಮೂದು.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_ಸಮಭಾಜಕ<576 and 112<=Y_ಬಟನ್_ಸಮನ್ವಯ<372:
                        ನೋಡುವ_ಪದಸೂಚಿ=(Y_ಬಟನ್_ಸಮನ್ವಯ-112)//52
                        if (Y_ಬಟನ್_ಸಮನ್ವಯ-112)%52<40 and ನೋಡುವ_ಪದಸೂಚಿ<5: 자신.ಕಳುಹಿಸಿ(bytes([ord('1')+ನೋಡುವ_ಪದಸೂಚಿ]))
                    else: 자신.ಕಳುಹಿಸಿ(bytes([30,1,단추들,x_ಸಮಭಾಜಕ&255,x_ಸಮಭಾಜಕ>>8,Y_ಬಟನ್_ಸಮನ್ವಯ&255,Y_ಬಟನ್_ಸಮನ್ವಯ>>8]))
                    continue
                if ವರ್ಗ_ಮೌಲ್ಯ==6:
                    ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,7); ಉದ್ದ_ಮೌಲ್ಯ=struct.unpack('>i',ಮುಖ್ಯ_ಪಠ್ಯ[3:])[0]
                    if abs(ಉದ್ದ_ಮೌಲ್ಯ)>65536: raise ValueError('clipboard too large')
                    ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,abs(ಉದ್ದ_ಮೌಲ್ಯ))
                    if ಉದ್ದ_ಮೌಲ್ಯ>=0:
                        try: ಕೀಲಿಮಣೆ_ನಮೂದು.ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ=ಪಠ್ಯ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ಕೀಲಿಮಣೆ_ನಮೂದು.ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ=ಪಠ್ಯ.decode('latin-1').encode('utf-8')
                        ಕೀಲಿಮಣೆ_ನಮೂದು.ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ=ಕೀಲಿಮಣೆ_ನಮೂದು.ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ[:65536].decode('utf-8','ignore').encode('utf-8')
                    ಸರ್ವರ್_ಮೌಲ್ಯ.sendall(bytes([ವರ್ಗ_ಮೌಲ್ಯ])+ಮುಖ್ಯ_ಪಠ್ಯ+ಪಠ್ಯ); continue
                if ವರ್ಗ_ಮೌಲ್ಯ==0:
                    ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,19)
                    if ಮುಖ್ಯ_ಪಠ್ಯ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=ಮುಖ್ಯ_ಪಠ್ಯ[3]//8
                elif ವರ್ಗ_ಮೌಲ್ಯ==2:
                    ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,3); 항목수=struct.unpack('>H',ಮುಖ್ಯ_ಪಠ್ಯ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ಕ್ಲೈಂಟ್,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ಅಕ್ಷಮ_ಬೆಲೆ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ಮುಖ್ಯ_ಪಠ್ಯ=struct.pack('>BHi',0,1,0)
                elif ವರ್ಗ_ಮೌಲ್ಯ in (3,150): ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,9)
                elif ವರ್ಗ_ಮೌಲ್ಯ==248:
                    ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,8)
                    if ಮುಖ್ಯ_ಪಠ್ಯ[7]>64: raise ValueError('fence too large')
                    ಮುಖ್ಯ_ಪಠ್ಯ+=정확한값(ಕ್ಲೈಂಟ್,ಮುಖ್ಯ_ಪಠ್ಯ[7])
                elif ವರ್ಗ_ಮೌಲ್ಯ==250: ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,3)
                elif ವರ್ಗ_ಮೌಲ್ಯ==251:
                    ಮುಖ್ಯ_ಪಠ್ಯ=정확한값(ಕ್ಲೈಂಟ್,7)
                    if ಮುಖ್ಯ_ಪಠ್ಯ[5]>16: raise ValueError('too many screens')
                    ಮುಖ್ಯ_ಪಠ್ಯ+=정확한값(ಕ್ಲೈಂಟ್,ಮುಖ್ಯ_ಪಠ್ಯ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ವರ್ಗ_ಮೌಲ್ಯ))
                ಸರ್ವರ್_ಮೌಲ್ಯ.sendall(bytes([ವರ್ಗ_ಮೌಲ್ಯ])+ಮುಖ್ಯ_ಪಠ್ಯ)
        except (OSError,EOFError,ValueError) as ದೋಷ:
            if str(ದೋಷ): print('VNC client:',ದೋಷ,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ಕ್ಲೈಂಟ್,ಸರ್ವರ್_ಮೌಲ್ಯ):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ಚಲನೆ_ಡೆಸ್ಕ್_ಟಾಪ್(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=5902, ನೆಟ್_ವರ್ಕ್=False, ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=2121, 전달규칙들=(), ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ=(640, 480), ಅತಿಥಿ_ಇಮೇಲ್=None, ಹೋಸ್ಟ್_ಇಮೇಲ್='127.0.0.1'):
    with ExitStack() as ಸಂಪನ್ಮೂಲಗಳು, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು = None
        if ನೆಟ್_ವರ್ಕ್:
            from ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ import ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ
            ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು = ಸಂಪನ್ಮೂಲಗಳು.enter_context(ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ(ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, 전달규칙들, ಅತಿಥಿ_ಇಮೇಲ್=ಅತಿಥಿ_ಇಮೇಲ್, ಹೋಸ್ಟ್_ಇಮೇಲ್=ಹೋಸ್ಟ್_ಇಮೇಲ್))
        ಮಾರ್ಗ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',ಪೋರ್ಟ್_ಸಂಖ್ಯೆ)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು and (원격화면접속번호==ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ಹೋಸ್ಟ್==원격화면접속번호 for 통신규약,ಹೋಸ್ಟ್,_ in ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            ಪ್ರಕ್ರಿಯೆ=subprocess.Popen(ಆಜ್ಞೆ(ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ಮಾರ್ಗ)]+(ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು.전달인수() if ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ಸೇತುವೆ=ಕನೆಕ್ಟ್_ಡೆಸ್ಕ್_ಟಾಪ್(ಪ್ರಕ್ರಿಯೆ); ಓದುಗ=threading.Thread(target=ಸೇತುವೆ.직렬입출력,daemon=True); ಓದುಗ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ಹೋಸ್ಟ್_ಇಮೇಲ್,ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while ಪ್ರಕ್ರಿಯೆ.poll() is None:
                    try: ಕ್ಲೈಂಟ್,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ಕ್ಲೈಂಟ್.close(); continue
                    if not ಮಾರ್ಗ.exists(): ಕ್ಲೈಂಟ್.close(); continue
                    처리작업=threading.Thread(target=ಸೇತುವೆ.ಕ್ಲೈಂಟ್,args=(ಕ್ಲೈಂಟ್,ಮಾರ್ಗ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ಸೇತುವೆ.닫힘=True
                if ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು: ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು.ವಿರಾಮ_ಸಂಗತಿ.set()
                if ಪ್ರಕ್ರಿಯೆ.poll() is None:
                    ಪ್ರಕ್ರಿಯೆ.terminate()
                    try: ಪ್ರಕ್ರಿಯೆ.wait(timeout=5)
                    except subprocess.TimeoutExpired: ಪ್ರಕ್ರಿಯೆ.kill(); ಪ್ರಕ್ರಿಯೆ.wait()
                ಓದುಗ.join(timeout=2); ಪ್ರಕ್ರಿಯೆ.stdin.close(); ಪ್ರಕ್ರಿಯೆ.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು and ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು.ದೋಷ: raise RuntimeError('network bridge: '+ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ_ನಮೂದು.ದೋಷ)
            return 0 if 가로채기됨 else ಪ್ರಕ್ರಿಯೆ.returncode


if __name__=='__main__':
    from ಪೂರೈಸು_ಆದೇಶ import 해상도읽기
    ಪಾರ್ಸರ್=argparse.ArgumentParser(description=__doc__); ಪಾರ್ಸರ್.add_argument('--port',type=int,default=5902)
    ಪಾರ್ಸರ್.add_argument('--resolution',type=해상도읽기,default=(640,480))
    ಪಾರ್ಸರ್.add_argument('--network',action='store_true'); ಪಾರ್ಸರ್.add_argument('--ftp-port',type=int,default=2121)
    ಪಾರ್ಸರ್.add_argument('--forward',action='append',default=[])
    ವಾದ_ಅರೇ=ಪಾರ್ಸರ್.parse_args()
    if ವಾದ_ಅರೇ.forward and not ವಾದ_ಅರೇ.network: ಪಾರ್ಸರ್.error('--forward requires --network')
    raise SystemExit(ಚಲನೆ_ಡೆಸ್ಕ್_ಟಾಪ್(ವಾದ_ಅರೇ.port,ನೆಟ್_ವರ್ಕ್=ವಾದ_ಅರೇ.network,ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=ವಾದ_ಅರೇ.ftp_port,전달규칙들=ವಾದ_ಅರೇ.forward,ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ=ವಾದ_ಅರೇ.resolution))
