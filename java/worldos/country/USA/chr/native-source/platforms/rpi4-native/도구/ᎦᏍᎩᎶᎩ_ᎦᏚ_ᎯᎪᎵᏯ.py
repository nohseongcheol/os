#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ 입력은 자체 kernel_ᏧᎬᏩᎶᏗᏯ UART로 전달한다. localhost 전용, 단일 ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ 클라이언트.
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
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import ᎤᏁᏤᎸᎩ
from local_input import create


def 정확한값(소켓, ᎢᎩᏓ):
    ᎦᏟᏌᏅᎯ = bytearray()
    while len(ᎦᏟᏌᏅᎯ) < ᎢᎩᏓ:
        조각 = 소켓.recv(ᎢᎩᏓ - len(ᎦᏟᏌᏅᎯ))
        if not 조각: raise EOFError()
        ᎦᏟᏌᏅᎯ.extend(조각)
    return bytes(ᎦᏟᏌᏅᎯ)


class ᏗᏐᏅᏍᏙᏗ:
    def __init__(자신, ᏫᎦᏅᏗ, 입력방식알림=None):
        자신.바이트전송 = ᏫᎦᏅᏗ; 자신.ᎦᏁᏟᏴᏍᏙᏗ_ᏍᏚᎢᏍᏗ = set(); 자신.ᏗᎬᎭᎸᏓ_ᏗᏍᏆᏂᎪᏙᏗ_ᏧᎬᏩᎶᏗᏯ = b''
        자신.한글조합기 = create(ᏫᎦᏅᏗ, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ᎦᏁᏟᏴᏍᏗ_ᏍᏚᎢᏍᏗ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ᏫᎦᏅᏗ(자신, ᎦᏟᏌᏅᎯ):
        자신.한글조합기.조합확정()
        자신.바이트전송(ᎦᏟᏌᏅᎯ)

    def ᎦᏁᏟᏴᏍᏗ_ᎬᏙᏗ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, 글쇠기호):
        if 글쇠기호 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ᎦᏁᏟᏴᏍᏙᏗ_ᏍᏚᎢᏍᏗ.add(글쇠기호)
            else: 자신.ᎦᏁᏟᏴᏍᏙᏗ_ᏍᏚᎢᏍᏗ.discard(글쇠기호)
            return
        if not 누르는중:
            자신.ᎦᏁᏟᏴᏍᏗ_ᏍᏚᎢᏍᏗ.discard(글쇠기호)
            return
        CTRL = bool(자신.ᎦᏁᏟᏴᏍᏙᏗ_ᏍᏚᎢᏍᏗ & {0xffe3, 0xffe4})
        SHIFT_ᏍᏚᎢᏍᏗ = bool(자신.ᎦᏁᏟᏴᏍᏙᏗ_ᏍᏚᎢᏍᏗ & {0xffe1, 0xffe2})
        if CTRL and SHIFT_ᏍᏚᎢᏍᏗ and 글쇠기호 in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if 글쇠기호 in (32,0xff0d):
                try:
                    ᏧᎬᏩᎶᏗᏯ=int(자신.유니코드입력,16)
                    if 32<=ᏧᎬᏩᎶᏗᏯ<=0x10ffff and not 0xd800<=ᏧᎬᏩᎶᏗᏯ<=0xdfff: 자신.ᏫᎦᏅᏗ(chr(ᏧᎬᏩᎶᏗᏯ).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif 글쇠기호==0xff1b: 자신.유니코드입력=None
            elif 글쇠기호==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif 글쇠기호<128 and chr(글쇠기호) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(글쇠기호)
            return
        if 글쇠기호 in (0xff31,0xffc6) or 글쇠기호==32 and SHIFT_ᏍᏚᎢᏍᏗ and not CTRL:
            if 글쇠기호 not in 자신.ᎦᏁᏟᏴᏍᏗ_ᏍᏚᎢᏍᏗ: 자신.ᎦᏁᏟᏴᏍᏗ_ᎬᏙᏗ()
            자신.ᎦᏁᏟᏴᏍᏗ_ᏍᏚᎢᏍᏗ.add(글쇠기호)
            return
        if 글쇠기호==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_ᏍᏚᎢᏍᏗ and 글쇠기호 in (ord('t'),ord('T')):
            자신.ᏫᎦᏅᏗ(bytes([30,2,1,0,0,0,0])); return
        if 글쇠기호==0xffc3: 자신.ᏫᎦᏅᏗ(bytes([30,2,2,0,0,0,0])); return
        if 글쇠기호==0xffc9: 자신.ᏫᎦᏅᏗ(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_ᏍᏚᎢᏍᏗ and 글쇠기호 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ᏫᎦᏅᏗ(자신.ᏗᎬᎭᎸᏓ_ᏗᏍᏆᏂᎪᏙᏗ_ᏧᎬᏩᎶᏗᏯ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 글쇠기호 in 특수글쇠: 자신.ᏫᎦᏅᏗ(특수글쇠[글쇠기호]); return
        ᎪᏪᎸ_ᎪᏗᏍᎩ = 글쇠기호 & 0xffffff if 글쇠기호 & 0xff000000 == 0x01000000 else 글쇠기호
        if ᎪᏪᎸ_ᎪᏗᏍᎩ > 0x10ffff or 0xd800 <= ᎪᏪᎸ_ᎪᏗᏍᎩ <= 0xdfff or 글쇠기호 >= 0xff00 and 글쇠기호 < 0x1000000: return
        if CTRL and 0x40 <= ᎪᏪᎸ_ᎪᏗᏍᎩ <= 0x7f: 자신.ᏫᎦᏅᏗ(bytes([ᎪᏪᎸ_ᎪᏗᏍᎩ & 31])); return
        if ᎪᏪᎸ_ᎪᏗᏍᎩ < 32: return
        if 자신.한글여부 and 자신.ᎦᏁᏟᏴᏍᏙᏗ_ᏍᏚᎢᏍᏗ & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ᎨᎵᏍᏗᎢ_ᏍᏚᎢᏍᏗ(chr(ᎪᏪᎸ_ᎪᏗᏍᎩ), altgr=True): return
        앞부분 = b'\x1b' if 자신.ᎦᏁᏟᏴᏍᏙᏗ_ᏍᏚᎢᏍᏗ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=ᎪᏪᎸ_ᎪᏗᏍᎩ<127:
            ᎪᏪᎸ_ᎦᏟᏌᏅᎯ=chr(ᎪᏪᎸ_ᎪᏗᏍᎩ).upper() if SHIFT_ᏍᏚᎢᏍᏗ else chr(ᎪᏪᎸ_ᎪᏗᏍᎩ)
            if 자신.한글조합기.ᎨᎵᏍᏗᎢ_ᏍᏚᎢᏍᏗ(ᎪᏪᎸ_ᎦᏟᏌᏅᎯ): return
        자신.ᏫᎦᏅᏗ(앞부분 + chr(ᎪᏪᎸ_ᎪᏗᏍᎩ).encode('utf-8'))


class ᎫᏓᎳ_ᎦᏍᎩᎶᎩ_ᎦᏚ:
    def __init__(자신, ᎢᏯᏛᏁᎵᏓᏍᏗ):
        자신.ᎢᏯᏛᏁᎵᏓᏍᏗ=ᎢᏯᏛᏁᎵᏓᏍᏗ; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def ᏫᎦᏅᏗ(자신, ᎦᏟᏌᏅᎯ):
        if not ᎦᏟᏌᏅᎯ or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(ᎦᏟᏌᏅᎯ); 자신.ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ᎦᏟᏌᏅᎯ=자신.ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout.read(4096)
                if not ᎦᏟᏌᏅᎯ: break
                sys.stdout.buffer.write(ᎦᏟᏌᏅᎯ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ᎦᏟᏌᏅᎯ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ᏫᎦᏅᏗ(b'terminal\n')
        finally: 자신.닫힘=True

    def ᎠᏥᏍᏕᎵᏍᎩ(자신, ᎠᏥᏍᏕᎵᏍᎩ, ᎠᏍᏓᏩᏛᏍᏗ):
        ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ=socket.socket(socket.AF_UNIX); ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.settimeout(10); ᎠᏥᏍᏕᎵᏍᎩ.settimeout(10)
        ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ=ᏗᏐᏅᏍᏙᏗ(자신.ᏫᎦᏅᏗ,lambda 한글여부:자신.ᏫᎦᏅᏗ(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.connect(str(ᎠᏍᏓᏩᏛᏍᏗ))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            ᎠᏥᏍᏕᎵᏍᎩ.sendall(정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,12))
            판번호=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.sendall(판번호)
            개수=정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,1);ᎠᏥᏍᏕᎵᏍᎩ.sendall(개수+정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,개수[0]))
            ᎤᎦᏎᏍᏗ=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,1)
            if ᎤᎦᏎᏍᏗ!=b'\x01': raise ValueError('unexpected security type')
            ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.sendall(ᎤᎦᏎᏍᏗ)
            if 판번호==b'RFB 003.008\n':ᎠᏥᏍᏕᎵᏍᎩ.sendall(정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,4))
            ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.sendall(정확한값(ᎠᏥᏍᏕᎵᏍᎩ,1))
            초기값=정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,24)
            ᎠᏥᏍᏕᎵᏍᎩ.sendall(초기값+정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ᎠᏥᏍᏕᎵᏍᎩ.settimeout(None);ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ=정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,1)[0]
                        if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==0:
                            머리=정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 원격 포인터의 중복을 피한다.
                            ᎬᏍᎦᏝ_ᏧᎬᏩᎶᏗᏯ=포인터지원
                            if ᎬᏍᎦᏝ_ᏧᎬᏩᎶᏗᏯ:ᎠᏥᏍᏕᎵᏍᎩ.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ᎠᏥᏍᏕᎵᏍᎩ.sendall(bytes([ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,12);가로,세로,폭,높이,ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ=struct.unpack('>HHHHi',사각형)
                                if ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ!=0:raise ValueError('unexpected framebuffer encoding: '+str(ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ))
                                ᎠᏥᏍᏕᎵᏍᎩ.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ᎦᏟᏌᏅᎯ=정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,min(남음,65536));ᎠᏥᏍᏕᎵᏍᎩ.sendall(ᎦᏟᏌᏅᎯ);남음-=len(ᎦᏟᏌᏅᎯ)
                        elif ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==1:
                            머리=정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,5);개수=struct.unpack('>H',머리[3:])[0]
                            ᎠᏥᏍᏕᎵᏍᎩ.sendall(bytes([ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ])+머리+정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,개수*6))
                        elif ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==2:ᎠᏥᏍᏕᎵᏍᎩ.sendall(bytes([ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ]))
                        elif ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==3:
                            머리=정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ᎠᏥᏍᏕᎵᏍᎩ.sendall(bytes([ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ])+머리+정확한값(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ᎠᏥᏍᏕᎵᏍᎩ.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,1)[0]
                if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==4:
                    본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,7); ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.누름값(본문[0]!=0,struct.unpack('>I',본문[3:])[0]); continue
                if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==255:
                    본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,11)
                    if 본문[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.누름값(struct.unpack('>H',본문[1:3])[0]!=0,struct.unpack('>I',본문[3:7])[0]); continue
                if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==5:
                    본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',본문)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.ᏫᎦᏅᏗ(bytes([ord('1')+색인]))
                    else: 자신.ᏫᎦᏅᏗ(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==6:
                    본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,7); ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=struct.unpack('>i',본문[3:])[0]
                    if abs(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ)>65536: raise ValueError('clipboard too large')
                    ᎠᎪᎵᏰᏗ=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,abs(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ))
                    if ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ>=0:
                        try: ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.ᏗᎬᎭᎸᏓ_ᏗᏍᏆᏂᎪᏙᏗ_ᏧᎬᏩᎶᏗᏯ=ᎠᎪᎵᏰᏗ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.ᏗᎬᎭᎸᏓ_ᏗᏍᏆᏂᎪᏙᏗ_ᏧᎬᏩᎶᏗᏯ=ᎠᎪᎵᏰᏗ.decode('latin-1').encode('utf-8')
                        ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.ᏗᎬᎭᎸᏓ_ᏗᏍᏆᏂᎪᏙᏗ_ᏧᎬᏩᎶᏗᏯ=ᏗᏐᏅᏍᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.ᏗᎬᎭᎸᏓ_ᏗᏍᏆᏂᎪᏙᏗ_ᏧᎬᏩᎶᏗᏯ[:65536].decode('utf-8','ignore').encode('utf-8')
                    ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.sendall(bytes([ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ])+본문+ᎠᎪᎵᏰᏗ); continue
                if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==0:
                    본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,19)
                    if 본문[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=본문[3]//8
                elif ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==2:
                    본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,3); 항목수=struct.unpack('>H',본문[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ᎠᏥᏍᏕᎵᏍᎩ,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    본문=struct.pack('>BHi',0,1,0)
                elif ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ in (3,150): 본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,9)
                elif ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==248:
                    본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,8)
                    if 본문[7]>64: raise ValueError('fence too large')
                    본문+=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,본문[7])
                elif ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==250: 본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,3)
                elif ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==251:
                    본문=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,7)
                    if 본문[5]>16: raise ValueError('too many screens')
                    본문+=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,본문[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ))
                ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.sendall(bytes([ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ])+본문)
        except (OSError,EOFError,ValueError) as ᎦᎵᏓᏍᏔᏅ:
            if str(ᎦᎵᏓᏍᏔᏅ): print('VNC client:',ᎦᎵᏓᏍᏔᏅ,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ᎠᏥᏍᏕᎵᏍᎩ,ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ᎠᎢᏎᏍᏗ_ᎦᏍᎩᎶᎩ_ᎦᏚ(접속번호=5902, ᏧᎾᏚᏓᎵ=False, 파일전송접속번호=2121, 전달규칙들=(), ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ=(640, 480), ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=None, ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ='127.0.0.1'):
    with ExitStack() as ᏗᏓᏁᏢᎢ, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if ᏧᎾᏚᏓᎵ:
            from 통신다리 import 통신다리
            통신다리항목 = ᏗᏓᏁᏢᎢ.enter_context(통신다리(파일전송접속번호, 전달규칙들, ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ))
        ᎠᏍᏓᏩᏛᏍᏗ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ᎠᏁᏢᏍᎩ==원격화면접속번호 for 통신규약,ᎠᏁᏢᏍᎩ,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            ᎢᏯᏛᏁᎵᏓᏍᏗ=subprocess.Popen(ᎤᏁᏤᎸᎩ(ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ᎠᏍᏓᏩᏛᏍᏗ)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=ᎫᏓᎳ_ᎦᏍᎩᎶᎩ_ᎦᏚ(ᎢᏯᏛᏁᎵᏓᏍᏗ); ᏗᎪᎵᏰᏍᎩ=threading.Thread(target=연결다리.직렬입출력,daemon=True); ᏗᎪᎵᏰᏍᎩ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is None:
                    try: ᎠᏥᏍᏕᎵᏍᎩ,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ᎠᏥᏍᏕᎵᏍᎩ.close(); continue
                    if not ᎠᏍᏓᏩᏛᏍᏗ.exists(): ᎠᏥᏍᏕᎵᏍᎩ.close(); continue
                    처리작업=threading.Thread(target=연결다리.ᎠᏥᏍᏕᎵᏍᎩ,args=(ᎠᏥᏍᏕᎵᏍᎩ,ᎠᏍᏓᏩᏛᏍᏗ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.ᎯᏲᎯᏍᏓ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.set()
                if ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is None:
                    ᎢᏯᏛᏁᎵᏓᏍᏗ.terminate()
                    try: ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=5)
                    except subprocess.TimeoutExpired: ᎢᏯᏛᏁᎵᏓᏍᏗ.kill(); ᎢᏯᏛᏁᎵᏓᏍᏗ.wait()
                ᏗᎪᎵᏰᏍᎩ.join(timeout=2); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.ᎦᎵᏓᏍᏔᏅ: raise RuntimeError('network bridge: '+통신다리항목.ᎦᎵᏓᏍᏔᏅ)
            return 0 if 가로채기됨 else ᎢᏯᏛᏁᎵᏓᏍᏗ.returncode


if __name__=='__main__':
    from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ᏗᏓᎦᏘᎸᏍᏗ_array=인수해석기.parse_args()
    if ᏗᏓᎦᏘᎸᏍᏗ_array.forward and not ᏗᏓᎦᏘᎸᏍᏗ_array.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ᎠᎢᏎᏍᏗ_ᎦᏍᎩᎶᎩ_ᎦᏚ(ᏗᏓᎦᏘᎸᏍᏗ_array.port,ᏧᎾᏚᏓᎵ=ᏗᏓᎦᏘᎸᏍᏗ_array.network,파일전송접속번호=ᏗᏓᎦᏘᎸᏍᏗ_array.ftp_port,전달규칙들=ᏗᏓᎦᏘᎸᏍᏗ_array.forward,ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ=ᏗᏓᎦᏘᎸᏍᏗ_array.resolution))
