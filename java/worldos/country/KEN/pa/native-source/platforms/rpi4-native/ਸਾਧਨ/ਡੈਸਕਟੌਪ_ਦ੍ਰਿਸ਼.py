#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ਕੀ_ਕੀਮਤ 입력은 자체 ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ UART로 전달한다. localhost 전용, 단일 ਨਿਯੰਤਰਣ_ਕੀਮਤ 클라이언트.
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
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਕਮਾਂਡ
from local_input import create


def 정확한값(소켓, ਆਕਾਰ):
    ਸਮੱਗਰੀ = bytearray()
    while len(ਸਮੱਗਰੀ) < ਆਕਾਰ:
        조각 = 소켓.recv(ਆਕਾਰ - len(ਸਮੱਗਰੀ))
        if not 조각: raise EOFError()
        ਸਮੱਗਰੀ.extend(조각)
    return bytes(ਸਮੱਗਰੀ)


class ਕੀਬੋਰਡ:
    def __init__(자신, ਈਮੇਲ, 입력방식알림=None):
        자신.바이트전송 = ਈਮੇਲ; 자신.ਬਦਲਣ_ਕੁੰਜੀ = set(); 자신.ਕਲਿਪਬੋਰਡ_ਕੀਮਤ = b''
        자신.한글조합기 = create(ਈਮੇਲ, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ਸਵਿੱਚ_ਕੀ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ਈਮੇਲ(자신, ਸਮੱਗਰੀ):
        자신.한글조합기.조합확정()
        자신.바이트전송(ਸਮੱਗਰੀ)

    def ਸਵਿੱਚ_ਮੋਡ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ਕੀ_ਪ੍ਰਤੀਕ):
        if ਕੀ_ਪ੍ਰਤੀਕ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ਬਦਲਣ_ਕੁੰਜੀ.add(ਕੀ_ਪ੍ਰਤੀਕ)
            else: 자신.ਬਦਲਣ_ਕੁੰਜੀ.discard(ਕੀ_ਪ੍ਰਤੀਕ)
            return
        if not 누르는중:
            자신.ਸਵਿੱਚ_ਕੀ.discard(ਕੀ_ਪ੍ਰਤੀਕ)
            return
        CTRL_ਕੀ = bool(자신.ਬਦਲਣ_ਕੁੰਜੀ & {0xffe3, 0xffe4})
        SHIFT_ਕੀ = bool(자신.ਬਦਲਣ_ਕੁੰਜੀ & {0xffe1, 0xffe2})
        if CTRL_ਕੀ and SHIFT_ਕੀ and ਕੀ_ਪ੍ਰਤੀਕ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ਕੀ_ਪ੍ਰਤੀਕ in (32,0xff0d):
                try:
                    ਕੀਮਤ=int(자신.유니코드입력,16)
                    if 32<=ਕੀਮਤ<=0x10ffff and not 0xd800<=ਕੀਮਤ<=0xdfff: 자신.ਈਮੇਲ(chr(ਕੀਮਤ).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ਕੀ_ਪ੍ਰਤੀਕ==0xff1b: 자신.유니코드입력=None
            elif ਕੀ_ਪ੍ਰਤੀਕ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ਕੀ_ਪ੍ਰਤੀਕ<128 and chr(ਕੀ_ਪ੍ਰਤੀਕ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ਕੀ_ਪ੍ਰਤੀਕ)
            return
        if ਕੀ_ਪ੍ਰਤੀਕ in (0xff31,0xffc6) or ਕੀ_ਪ੍ਰਤੀਕ==32 and SHIFT_ਕੀ and not CTRL_ਕੀ:
            if ਕੀ_ਪ੍ਰਤੀਕ not in 자신.ਸਵਿੱਚ_ਕੀ: 자신.ਸਵਿੱਚ_ਮੋਡ()
            자신.ਸਵਿੱਚ_ਕੀ.add(ਕੀ_ਪ੍ਰਤੀਕ)
            return
        if ਕੀ_ਪ੍ਰਤੀਕ==0xff08 and 자신.한글여부 and not CTRL_ਕੀ and 자신.한글조합기.앞글자지우기(): return
        if CTRL_ਕੀ and SHIFT_ਕੀ and ਕੀ_ਪ੍ਰਤੀਕ in (ord('t'),ord('T')):
            자신.ਈਮੇਲ(bytes([30,2,1,0,0,0,0])); return
        if ਕੀ_ਪ੍ਰਤੀਕ==0xffc3: 자신.ਈਮੇਲ(bytes([30,2,2,0,0,0,0])); return
        if ਕੀ_ਪ੍ਰਤੀਕ==0xffc9: 자신.ਈਮੇਲ(bytes([30,2,3,0,0,0,0])); return
        if CTRL_ਕੀ and SHIFT_ਕੀ and ਕੀ_ਪ੍ਰਤੀਕ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ਈਮੇਲ(자신.ਕਲਿਪਬੋਰਡ_ਕੀਮਤ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ਕੀ_ਪ੍ਰਤੀਕ in 특수글쇠: 자신.ਈਮੇਲ(특수글쇠[ਕੀ_ਪ੍ਰਤੀਕ]); return
        ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ = ਕੀ_ਪ੍ਰਤੀਕ & 0xffffff if ਕੀ_ਪ੍ਰਤੀਕ & 0xff000000 == 0x01000000 else ਕੀ_ਪ੍ਰਤੀਕ
        if ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ > 0x10ffff or 0xd800 <= ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ <= 0xdfff or ਕੀ_ਪ੍ਰਤੀਕ >= 0xff00 and ਕੀ_ਪ੍ਰਤੀਕ < 0x1000000: return
        if CTRL_ਕੀ and 0x40 <= ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ <= 0x7f: 자신.ਈਮੇਲ(bytes([ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ & 31])); return
        if ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ < 32: return
        if 자신.한글여부 and 자신.ਬਦਲਣ_ਕੁੰਜੀ & {0xffea,0xfe03,0xff7e} and not CTRL_ਕੀ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ਫੀਡ_ਕੀ(chr(ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ), altgr=True): return
        앞부분 = b'\x1b' if 자신.ਬਦਲਣ_ਕੁੰਜੀ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_ਕੀ and not 앞부분 and 32<=ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ<127:
            ਵਰਣ_ਸਮੱਗਰੀ=chr(ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ).upper() if SHIFT_ਕੀ else chr(ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ)
            if 자신.한글조합기.ਫੀਡ_ਕੀ(ਵਰਣ_ਸਮੱਗਰੀ): return
        자신.ਈਮੇਲ(앞부분 + chr(ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ).encode('utf-8'))


class ਕਨੈਕਟ_ਕਰੋ_ਡੈਸਕਟੌਪ:
    def __init__(자신, ਪਰੋਸੈੱਸ):
        자신.ਪਰੋਸੈੱਸ=ਪਰੋਸੈੱਸ; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.ਟਰਮੀਨਲ=False; 자신.시작화면=False; 자신.닫힘=False

    def ਈਮੇਲ(자신, ਸਮੱਗਰੀ):
        if not ਸਮੱਗਰੀ or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.ਪਰੋਸੈੱਸ.stdin.write(ਸਮੱਗਰੀ); 자신.ਪਰੋਸੈੱਸ.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ਸਮੱਗਰੀ=자신.ਪਰੋਸੈੱਸ.stdout.read(4096)
                if not ਸਮੱਗਰੀ: break
                sys.stdout.buffer.write(ਸਮੱਗਰੀ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ਸਮੱਗਰੀ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ਟਰਮੀਨਲ=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ਈਮੇਲ(b'terminal\n')
        finally: 자신.닫힘=True

    def ਗਾਹਕ(자신, ਗਾਹਕ, ਮਾਰਗ):
        ਸਰਵਰ_ਕੀਮਤ=socket.socket(socket.AF_UNIX); ਸਰਵਰ_ਕੀਮਤ.settimeout(10); ਗਾਹਕ.settimeout(10)
        ਕੀਬੋਰਡ_ਦਾਖਲਾ=ਕੀਬੋਰਡ(자신.ਈਮੇਲ,lambda 한글여부:자신.ਈਮੇਲ(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ਸਰਵਰ_ਕੀਮਤ.connect(str(ਮਾਰਗ))
            # 초기 협상은 순서대로 끝낸다. 이후 ਆਉਟਪੁੱਟ 가닥만 클라이언트에 쓴다.
            ਗਾਹਕ.sendall(정확한값(ਸਰਵਰ_ਕੀਮਤ,12))
            판번호=정확한값(ਗਾਹਕ,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ਸਰਵਰ_ਕੀਮਤ.sendall(판번호)
            개수=정확한값(ਸਰਵਰ_ਕੀਮਤ,1);ਗਾਹਕ.sendall(개수+정확한값(ਸਰਵਰ_ਕੀਮਤ,개수[0]))
            ਸੁਰੱਖਿਆ=정확한값(ਗਾਹਕ,1)
            if ਸੁਰੱਖਿਆ!=b'\x01': raise ValueError('unexpected security type')
            ਸਰਵਰ_ਕੀਮਤ.sendall(ਸੁਰੱਖਿਆ)
            if 판번호==b'RFB 003.008\n':ਗਾਹਕ.sendall(정확한값(ਸਰਵਰ_ਕੀਮਤ,4))
            ਸਰਵਰ_ਕੀਮਤ.sendall(정확한값(ਗਾਹਕ,1))
            초기값=정확한값(ਸਰਵਰ_ਕੀਮਤ,24)
            ਗਾਹਕ.sendall(초기값+정확한값(ਸਰਵਰ_ਕੀਮਤ,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ਗਾਹਕ.settimeout(None);ਸਰਵਰ_ਕੀਮਤ.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ਸ਼੍ਰੇਣੀ_ਕੀਮਤ=정확한값(ਸਰਵਰ_ਕੀਮਤ,1)[0]
                        if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==0:
                            머리=정확한값(ਸਰਵਰ_ਕੀਮਤ,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ਰਿਮੋਟ_ਕੀਮਤ 포인터의 중복을 피한다.
                            ਲੁਕਿਆ_ਹੋਇਆ_ਕੀਮਤ=포인터지원
                            if ਲੁਕਿਆ_ਹੋਇਆ_ਕੀਮਤ:ਗਾਹਕ.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ਗਾਹਕ.sendall(bytes([ਸ਼੍ਰੇਣੀ_ਕੀਮਤ])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ਸਰਵਰ_ਕੀਮਤ,12);가로,ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ,폭,높이,ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ_ਕੀਮਤ=struct.unpack('>HHHHi',사각형)
                                if ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ_ਕੀਮਤ!=0:raise ValueError('unexpected framebuffer encoding: '+str(ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ_ਕੀਮਤ))
                                ਗਾਹਕ.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ਸਮੱਗਰੀ=정확한값(ਸਰਵਰ_ਕੀਮਤ,min(남음,65536));ਗਾਹਕ.sendall(ਸਮੱਗਰੀ);남음-=len(ਸਮੱਗਰੀ)
                        elif ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==1:
                            머리=정확한값(ਸਰਵਰ_ਕੀਮਤ,5);개수=struct.unpack('>H',머리[3:])[0]
                            ਗਾਹਕ.sendall(bytes([ਸ਼੍ਰੇਣੀ_ਕੀਮਤ])+머리+정확한값(ਸਰਵਰ_ਕੀਮਤ,개수*6))
                        elif ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==2:ਗਾਹਕ.sendall(bytes([ਸ਼੍ਰੇਣੀ_ਕੀਮਤ]))
                        elif ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==3:
                            머리=정확한값(ਸਰਵਰ_ਕੀਮਤ,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ਗਾਹਕ.sendall(bytes([ਸ਼੍ਰੇਣੀ_ਕੀਮਤ])+머리+정확한값(ਸਰਵਰ_ਕੀਮਤ,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ਸ਼੍ਰੇਣੀ_ਕੀਮਤ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ਗਾਹਕ.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ਸ਼੍ਰੇਣੀ_ਕੀਮਤ=정확한값(ਗਾਹਕ,1)[0]
                if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==4:
                    ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,7); ਕੀਬੋਰਡ_ਦਾਖਲਾ.누름값(ਮੁੱਖ_ਪਾਠ[0]!=0,struct.unpack('>I',ਮੁੱਖ_ਪਾਠ[3:])[0]); continue
                if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==255:
                    ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,11)
                    if ਮੁੱਖ_ਪਾਠ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ਕੀਬੋਰਡ_ਦਾਖਲਾ.누름값(struct.unpack('>H',ਮੁੱਖ_ਪਾਠ[1:3])[0]!=0,struct.unpack('>I',ਮੁੱਖ_ਪਾਠ[3:7])[0]); continue
                if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==5:
                    ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,5); 단추들,x_ਕੌਔਰਡੀਨੇਟ,세로좌표=struct.unpack('>BHH',ਮੁੱਖ_ਪਾਠ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ਕੀਬੋਰਡ_ਦਾਖਲਾ.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_ਕੌਔਰਡੀਨੇਟ<576 and 112<=세로좌표<372:
                        ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ<5: 자신.ਈਮੇਲ(bytes([ord('1')+ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ]))
                    else: 자신.ਈਮੇਲ(bytes([30,1,단추들,x_ਕੌਔਰਡੀਨੇਟ&255,x_ਕੌਔਰਡੀਨੇਟ>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==6:
                    ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,7); ਲੰਬਾਈ_ਕੀਮਤ=struct.unpack('>i',ਮੁੱਖ_ਪਾਠ[3:])[0]
                    if abs(ਲੰਬਾਈ_ਕੀਮਤ)>65536: raise ValueError('clipboard too large')
                    ਟੈਕਸਟ=정확한값(ਗਾਹਕ,abs(ਲੰਬਾਈ_ਕੀਮਤ))
                    if ਲੰਬਾਈ_ਕੀਮਤ>=0:
                        try: ਕੀਬੋਰਡ_ਦਾਖਲਾ.ਕਲਿਪਬੋਰਡ_ਕੀਮਤ=ਟੈਕਸਟ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ਕੀਬੋਰਡ_ਦਾਖਲਾ.ਕਲਿਪਬੋਰਡ_ਕੀਮਤ=ਟੈਕਸਟ.decode('latin-1').encode('utf-8')
                        ਕੀਬੋਰਡ_ਦਾਖਲਾ.ਕਲਿਪਬੋਰਡ_ਕੀਮਤ=ਕੀਬੋਰਡ_ਦਾਖਲਾ.ਕਲਿਪਬੋਰਡ_ਕੀਮਤ[:65536].decode('utf-8','ignore').encode('utf-8')
                    ਸਰਵਰ_ਕੀਮਤ.sendall(bytes([ਸ਼੍ਰੇਣੀ_ਕੀਮਤ])+ਮੁੱਖ_ਪਾਠ+ਟੈਕਸਟ); continue
                if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==0:
                    ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,19)
                    if ਮੁੱਖ_ਪਾਠ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=ਮੁੱਖ_ਪਾਠ[3]//8
                elif ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==2:
                    ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,3); 항목수=struct.unpack('>H',ਮੁੱਖ_ਪਾਠ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ਗਾਹਕ,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ਡਿਫੌਲਟ_ਵੈਲਯੂ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ਮੁੱਖ_ਪਾਠ=struct.pack('>BHi',0,1,0)
                elif ਸ਼੍ਰੇਣੀ_ਕੀਮਤ in (3,150): ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,9)
                elif ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==248:
                    ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,8)
                    if ਮੁੱਖ_ਪਾਠ[7]>64: raise ValueError('fence too large')
                    ਮੁੱਖ_ਪਾਠ+=정확한값(ਗਾਹਕ,ਮੁੱਖ_ਪਾਠ[7])
                elif ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==250: ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,3)
                elif ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==251:
                    ਮੁੱਖ_ਪਾਠ=정확한값(ਗਾਹਕ,7)
                    if ਮੁੱਖ_ਪਾਠ[5]>16: raise ValueError('too many screens')
                    ਮੁੱਖ_ਪਾਠ+=정확한값(ਗਾਹਕ,ਮੁੱਖ_ਪਾਠ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ਸ਼੍ਰੇਣੀ_ਕੀਮਤ))
                ਸਰਵਰ_ਕੀਮਤ.sendall(bytes([ਸ਼੍ਰੇਣੀ_ਕੀਮਤ])+ਮੁੱਖ_ਪਾਠ)
        except (OSError,EOFError,ValueError) as ਗਲਤੀ:
            if str(ਗਲਤੀ): print('VNC client:',ਗਲਤੀ,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ਗਾਹਕ,ਸਰਵਰ_ਕੀਮਤ):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ਚਲਾਉ_ਡੈਸਕਟੌਪ(접속번호=5902, ਨੈਟਵਰਕ=False, 파일전송접속번호=2121, 전달규칙들=(), ਰੂਪਾਂਤਰ_ਕੀਮਤ=(640, 480), ਗੈਸਟ_ਪਤਾ=None, ਹੋਸਟ_ਪਤਾ='127.0.0.1'):
    with ExitStack() as ਸੋਮੇ, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ = None
        if ਨੈਟਵਰਕ:
            from ਨੈਟਵਰਕ_ਬਰਿਜ import ਨੈਟਵਰਕ_ਬਰਿਜ
            ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ = ਸੋਮੇ.enter_context(ਨੈਟਵਰਕ_ਬਰਿਜ(파일전송접속번호, 전달규칙들, ਗੈਸਟ_ਪਤਾ=ਗੈਸਟ_ਪਤਾ, ਹੋਸਟ_ਪਤਾ=ਹੋਸਟ_ਪਤਾ))
        ਮਾਰਗ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ਹੋਸਟ==원격화면접속번호 for 통신규약,ਹੋਸਟ,_ in ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            ਪਰੋਸੈੱਸ=subprocess.Popen(ਕਮਾਂਡ(ਰੂਪਾਂਤਰ_ਕੀਮਤ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ਮਾਰਗ)]+(ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ.전달인수() if ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ਬਰਿਜ=ਕਨੈਕਟ_ਕਰੋ_ਡੈਸਕਟੌਪ(ਪਰੋਸੈੱਸ); ਪਾਠਕ=threading.Thread(target=ਬਰਿਜ.직렬입출력,daemon=True); ਪਾਠਕ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ਹੋਸਟ_ਪਤਾ,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while ਪਰੋਸੈੱਸ.poll() is None:
                    try: ਗਾਹਕ,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ਗਾਹਕ.close(); continue
                    if not ਮਾਰਗ.exists(): ਗਾਹਕ.close(); continue
                    처리작업=threading.Thread(target=ਬਰਿਜ.ਗਾਹਕ,args=(ਗਾਹਕ,ਮਾਰਗ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ਬਰਿਜ.닫힘=True
                if ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ: ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ.ਰੁਕਣਾ_ਇਵੈਂਟ.set()
                if ਪਰੋਸੈੱਸ.poll() is None:
                    ਪਰੋਸੈੱਸ.terminate()
                    try: ਪਰੋਸੈੱਸ.wait(timeout=5)
                    except subprocess.TimeoutExpired: ਪਰੋਸੈੱਸ.kill(); ਪਰੋਸੈੱਸ.wait()
                ਪਾਠਕ.join(timeout=2); ਪਰੋਸੈੱਸ.stdin.close(); ਪਰੋਸੈੱਸ.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ and ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ.ਗਲਤੀ: raise RuntimeError('network bridge: '+ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ.ਗਲਤੀ)
            return 0 if 가로채기됨 else ਪਰੋਸੈੱਸ.returncode


if __name__=='__main__':
    from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ=인수해석기.parse_args()
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.forward and not ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ਚਲਾਉ_ਡੈਸਕਟੌਪ(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.port,ਨੈਟਵਰਕ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network,파일전송접속번호=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.ftp_port,전달규칙들=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.forward,ਰੂਪਾਂਤਰ_ਕੀਮਤ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.resolution))
