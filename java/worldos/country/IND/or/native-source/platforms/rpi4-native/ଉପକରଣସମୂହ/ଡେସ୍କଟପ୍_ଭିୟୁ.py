#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, କୀ_ମୂଲ୍ୟ 입력은 자체 କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ UART로 전달한다. localhost 전용, 단일 ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ 클라이언트.
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
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ନିର୍ଦ୍ଦେଶ
from local_input import create


def 정확한값(소켓, ଆକାର):
    ଡାଟା = bytearray()
    while len(ଡାଟା) < ଆକାର:
        조각 = 소켓.recv(ଆକାର - len(ଡାଟା))
        if not 조각: raise EOFError()
        ଡାଟା.extend(조각)
    return bytes(ଡାଟା)


class କୀବୋର୍ଡ୍:
    def __init__(자신, ପଠାନ୍ତୁ, 입력방식알림=None):
        자신.바이트전송 = ପଠାନ୍ତୁ; 자신.ମୋଡ଼ିଫାୟାର_କୀ = set(); 자신.କ୍ଲିପ୍_ବୋର୍ଡ଼_ମୂଲ୍ୟ = b''
        자신.한글조합기 = create(ପଠାନ୍ତୁ, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ସୁଇଚ୍_କୀ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ପଠାନ୍ତୁ(자신, ଡାଟା):
        자신.한글조합기.조합확정()
        자신.바이트전송(ଡାଟା)

    def ସୁଇଚ୍_ମୋଡ୍(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, କୀ_ସଙ୍କେତ):
        if କୀ_ସଙ୍କେତ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ମୋଡ଼ିଫାୟାର_କୀ.add(କୀ_ସଙ୍କେତ)
            else: 자신.ମୋଡ଼ିଫାୟାର_କୀ.discard(କୀ_ସଙ୍କେତ)
            return
        if not 누르는중:
            자신.ସୁଇଚ୍_କୀ.discard(କୀ_ସଙ୍କେତ)
            return
        CTRL_କୀ = bool(자신.ମୋଡ଼ିଫାୟାର_କୀ & {0xffe3, 0xffe4})
        SHIFT_କୀ = bool(자신.ମୋଡ଼ିଫାୟାର_କୀ & {0xffe1, 0xffe2})
        if CTRL_କୀ and SHIFT_କୀ and କୀ_ସଙ୍କେତ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if କୀ_ସଙ୍କେତ in (32,0xff0d):
                try:
                    ମୂଲ୍ୟ=int(자신.유니코드입력,16)
                    if 32<=ମୂଲ୍ୟ<=0x10ffff and not 0xd800<=ମୂଲ୍ୟ<=0xdfff: 자신.ପଠାନ୍ତୁ(chr(ମୂଲ୍ୟ).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif କୀ_ସଙ୍କେତ==0xff1b: 자신.유니코드입력=None
            elif କୀ_ସଙ୍କେତ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif କୀ_ସଙ୍କେତ<128 and chr(କୀ_ସଙ୍କେତ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(କୀ_ସଙ୍କେତ)
            return
        if କୀ_ସଙ୍କେତ in (0xff31,0xffc6) or କୀ_ସଙ୍କେତ==32 and SHIFT_କୀ and not CTRL_କୀ:
            if କୀ_ସଙ୍କେତ not in 자신.ସୁଇଚ୍_କୀ: 자신.ସୁଇଚ୍_ମୋଡ୍()
            자신.ସୁଇଚ୍_କୀ.add(କୀ_ସଙ୍କେତ)
            return
        if କୀ_ସଙ୍କେତ==0xff08 and 자신.한글여부 and not CTRL_କୀ and 자신.한글조합기.앞글자지우기(): return
        if CTRL_କୀ and SHIFT_କୀ and କୀ_ସଙ୍କେତ in (ord('t'),ord('T')):
            자신.ପଠାନ୍ତୁ(bytes([30,2,1,0,0,0,0])); return
        if କୀ_ସଙ୍କେତ==0xffc3: 자신.ପଠାନ୍ତୁ(bytes([30,2,2,0,0,0,0])); return
        if କୀ_ସଙ୍କେତ==0xffc9: 자신.ପଠାନ୍ତୁ(bytes([30,2,3,0,0,0,0])); return
        if CTRL_କୀ and SHIFT_କୀ and କୀ_ସଙ୍କେତ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ପଠାନ୍ତୁ(자신.କ୍ଲିପ୍_ବୋର୍ଡ଼_ମୂଲ୍ୟ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if କୀ_ସଙ୍କେତ in 특수글쇠: 자신.ପଠାନ୍ତୁ(특수글쇠[କୀ_ସଙ୍କେତ]); return
        ବର୍ଣ୍ଣ_ଏନକୋଡିଂ = କୀ_ସଙ୍କେତ & 0xffffff if କୀ_ସଙ୍କେତ & 0xff000000 == 0x01000000 else କୀ_ସଙ୍କେତ
        if ବର୍ଣ୍ଣ_ଏନକୋଡିଂ > 0x10ffff or 0xd800 <= ବର୍ଣ୍ଣ_ଏନକୋଡିଂ <= 0xdfff or କୀ_ସଙ୍କେତ >= 0xff00 and କୀ_ସଙ୍କେତ < 0x1000000: return
        if CTRL_କୀ and 0x40 <= ବର୍ଣ୍ଣ_ଏନକୋଡିଂ <= 0x7f: 자신.ପଠାନ୍ତୁ(bytes([ବର୍ଣ୍ଣ_ଏନକୋଡିଂ & 31])); return
        if ବର୍ଣ୍ଣ_ଏନକୋଡିଂ < 32: return
        if 자신.한글여부 and 자신.ମୋଡ଼ିଫାୟାର_କୀ & {0xffea,0xfe03,0xff7e} and not CTRL_କୀ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ଫିଡ୍_କୀ(chr(ବର୍ଣ୍ଣ_ଏନକୋଡିଂ), altgr=True): return
        앞부분 = b'\x1b' if 자신.ମୋଡ଼ିଫାୟାର_କୀ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_କୀ and not 앞부분 and 32<=ବର୍ଣ୍ଣ_ଏନକୋଡିଂ<127:
            ବର୍ଣ୍ଣ_ଡାଟା=chr(ବର୍ଣ୍ଣ_ଏନକୋଡିଂ).upper() if SHIFT_କୀ else chr(ବର୍ଣ୍ଣ_ଏନକୋଡିଂ)
            if 자신.한글조합기.ଫିଡ୍_କୀ(ବର୍ଣ୍ଣ_ଡାଟା): return
        자신.ପଠାନ୍ତୁ(앞부분 + chr(ବର୍ଣ୍ଣ_ଏନକୋଡିଂ).encode('utf-8'))


class ସଂଯୋଗ_ଡେସ୍କଟପ୍:
    def __init__(자신, ପ୍ରକ୍ରିୟା):
        자신.ପ୍ରକ୍ରିୟା=ପ୍ରକ୍ରିୟା; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.ଟର୍ମିନାଲ=False; 자신.시작화면=False; 자신.닫힘=False

    def ପଠାନ୍ତୁ(자신, ଡାଟା):
        if not ଡାଟା or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.ପ୍ରକ୍ରିୟା.stdin.write(ଡାଟା); 자신.ପ୍ରକ୍ରିୟା.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ଡାଟା=자신.ପ୍ରକ୍ରିୟା.stdout.read(4096)
                if not ଡାଟା: break
                sys.stdout.buffer.write(ଡାଟା); sys.stdout.buffer.flush()
                끝부분=(끝부분+ଡାଟା)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ଟର୍ମିନାଲ=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ପଠାନ୍ତୁ(b'terminal\n')
        finally: 자신.닫힘=True

    def କ୍ଲାଏଣ୍ଟ(자신, କ୍ଲାଏଣ୍ଟ, ପଥ):
        ସର୍ଭର୍_ମୂଲ୍ୟ=socket.socket(socket.AF_UNIX); ସର୍ଭର୍_ମୂଲ୍ୟ.settimeout(10); କ୍ଲାଏଣ୍ଟ.settimeout(10)
        କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି=କୀବୋର୍ଡ୍(자신.ପଠାନ୍ତୁ,lambda 한글여부:자신.ପଠାନ୍ତୁ(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ସର୍ଭର୍_ମୂଲ୍ୟ.connect(str(ପଥ))
            # 초기 협상은 순서대로 끝낸다. 이후 ନିର୍ଗମ 가닥만 클라이언트에 쓴다.
            କ୍ଲାଏଣ୍ଟ.sendall(정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,12))
            판번호=정확한값(କ୍ଲାଏଣ୍ଟ,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ସର୍ଭର୍_ମୂଲ୍ୟ.sendall(판번호)
            개수=정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,1);କ୍ଲାଏଣ୍ଟ.sendall(개수+정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,개수[0]))
            ନିରାପତ୍ତା=정확한값(କ୍ଲାଏଣ୍ଟ,1)
            if ନିରାପତ୍ତା!=b'\x01': raise ValueError('unexpected security type')
            ସର୍ଭର୍_ମୂଲ୍ୟ.sendall(ନିରାପତ୍ତା)
            if 판번호==b'RFB 003.008\n':କ୍ଲାଏଣ୍ଟ.sendall(정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,4))
            ସର୍ଭର୍_ମୂଲ୍ୟ.sendall(정확한값(କ୍ଲାଏଣ୍ଟ,1))
            초기값=정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,24)
            କ୍ଲାଏଣ୍ଟ.sendall(초기값+정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            କ୍ଲାଏଣ୍ଟ.settimeout(None);ସର୍ଭର୍_ମୂଲ୍ୟ.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ବର୍ଗ_ମୂଲ୍ୟ=정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,1)[0]
                        if ବର୍ଗ_ମୂଲ୍ୟ==0:
                            머리=정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ 포인터의 중복을 피한다.
                            ଲୁକ୍କାୟିତ_ମୂଲ୍ୟ=포인터지원
                            if ଲୁକ୍କାୟିତ_ମୂଲ୍ୟ:କ୍ଲାଏଣ୍ଟ.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            କ୍ଲାଏଣ୍ଟ.sendall(bytes([ବର୍ଗ_ମୂଲ୍ୟ])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,12);가로,ଅନୁଲମ୍ବ_ସ୍ଥିତି,폭,높이,ଏନକୋଡିଂ_ମୂଲ୍ୟ=struct.unpack('>HHHHi',사각형)
                                if ଏନକୋଡିଂ_ମୂଲ୍ୟ!=0:raise ValueError('unexpected framebuffer encoding: '+str(ଏନକୋଡିଂ_ମୂଲ୍ୟ))
                                କ୍ଲାଏଣ୍ଟ.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ଡାଟା=정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,min(남음,65536));କ୍ଲାଏଣ୍ଟ.sendall(ଡାଟା);남음-=len(ଡାଟା)
                        elif ବର୍ଗ_ମୂଲ୍ୟ==1:
                            머리=정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,5);개수=struct.unpack('>H',머리[3:])[0]
                            କ୍ଲାଏଣ୍ଟ.sendall(bytes([ବର୍ଗ_ମୂଲ୍ୟ])+머리+정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,개수*6))
                        elif ବର୍ଗ_ମୂଲ୍ୟ==2:କ୍ଲାଏଣ୍ଟ.sendall(bytes([ବର୍ଗ_ମୂଲ୍ୟ]))
                        elif ବର୍ଗ_ମୂଲ୍ୟ==3:
                            머리=정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            କ୍ଲାଏଣ୍ଟ.sendall(bytes([ବର୍ଗ_ମୂଲ୍ୟ])+머리+정확한값(ସର୍ଭର୍_ମୂଲ୍ୟ,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ବର୍ଗ_ମୂଲ୍ୟ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:କ୍ଲାଏଣ୍ଟ.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ବର୍ଗ_ମୂଲ୍ୟ=정확한값(କ୍ଲାଏଣ୍ଟ,1)[0]
                if ବର୍ଗ_ମୂଲ୍ୟ==4:
                    ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,7); କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି.누름값(ମୂଳ_ପାଠ[0]!=0,struct.unpack('>I',ମୂଳ_ପାଠ[3:])[0]); continue
                if ବର୍ଗ_ମୂଲ୍ୟ==255:
                    ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,11)
                    if ମୂଳ_ପାଠ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି.누름값(struct.unpack('>H',ମୂଳ_ପାଠ[1:3])[0]!=0,struct.unpack('>I',ମୂଳ_ପାଠ[3:7])[0]); continue
                if ବର୍ଗ_ମୂଲ୍ୟ==5:
                    ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,5); 단추들,x_ସଂଯୋଜନ,세로좌표=struct.unpack('>BHH',ମୂଳ_ପାଠ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_ସଂଯୋଜନ<576 and 112<=세로좌표<372:
                        ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା<5: 자신.ପଠାନ୍ତୁ(bytes([ord('1')+ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା]))
                    else: 자신.ପଠାନ୍ତୁ(bytes([30,1,단추들,x_ସଂଯୋଜନ&255,x_ସଂଯୋଜନ>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ବର୍ଗ_ମୂଲ୍ୟ==6:
                    ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,7); ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ=struct.unpack('>i',ମୂଳ_ପାଠ[3:])[0]
                    if abs(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ)>65536: raise ValueError('clipboard too large')
                    ପାଠ୍ଯ=정확한값(କ୍ଲାଏଣ୍ଟ,abs(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ))
                    if ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ>=0:
                        try: କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି.କ୍ଲିପ୍_ବୋର୍ଡ଼_ମୂଲ୍ୟ=ପାଠ୍ଯ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି.କ୍ଲିପ୍_ବୋର୍ଡ଼_ମୂଲ୍ୟ=ପାଠ୍ଯ.decode('latin-1').encode('utf-8')
                        କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି.କ୍ଲିପ୍_ବୋର୍ଡ଼_ମୂଲ୍ୟ=କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି.କ୍ଲିପ୍_ବୋର୍ଡ଼_ମୂଲ୍ୟ[:65536].decode('utf-8','ignore').encode('utf-8')
                    ସର୍ଭର୍_ମୂଲ୍ୟ.sendall(bytes([ବର୍ଗ_ମୂଲ୍ୟ])+ମୂଳ_ପାଠ+ପାଠ୍ଯ); continue
                if ବର୍ଗ_ମୂଲ୍ୟ==0:
                    ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,19)
                    if ମୂଳ_ପାଠ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=ମୂଳ_ପାଠ[3]//8
                elif ବର୍ଗ_ମୂଲ୍ୟ==2:
                    ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,3); 항목수=struct.unpack('>H',ମୂଳ_ପାଠ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(କ୍ଲାଏଣ୍ଟ,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ଡିଫଲ୍ଟ_ମାନ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ମୂଳ_ପାଠ=struct.pack('>BHi',0,1,0)
                elif ବର୍ଗ_ମୂଲ୍ୟ in (3,150): ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,9)
                elif ବର୍ଗ_ମୂଲ୍ୟ==248:
                    ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,8)
                    if ମୂଳ_ପାଠ[7]>64: raise ValueError('fence too large')
                    ମୂଳ_ପାଠ+=정확한값(କ୍ଲାଏଣ୍ଟ,ମୂଳ_ପାଠ[7])
                elif ବର୍ଗ_ମୂଲ୍ୟ==250: ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,3)
                elif ବର୍ଗ_ମୂଲ୍ୟ==251:
                    ମୂଳ_ପାଠ=정확한값(କ୍ଲାଏଣ୍ଟ,7)
                    if ମୂଳ_ପାଠ[5]>16: raise ValueError('too many screens')
                    ମୂଳ_ପାଠ+=정확한값(କ୍ଲାଏଣ୍ଟ,ମୂଳ_ପାଠ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ବର୍ଗ_ମୂଲ୍ୟ))
                ସର୍ଭର୍_ମୂଲ୍ୟ.sendall(bytes([ବର୍ଗ_ମୂଲ୍ୟ])+ମୂଳ_ପାଠ)
        except (OSError,EOFError,ValueError) as ତ୍ରୁଟି:
            if str(ତ୍ରୁଟି): print('VNC client:',ତ୍ରୁଟି,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (କ୍ଲାଏଣ୍ଟ,ସର୍ଭର୍_ମୂଲ୍ୟ):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ରନ୍_ଡେସ୍କଟପ୍(ପୋର୍ଟ୍_ନମ୍ଵର୍=5902, ନେଟ୍_ୱାର୍କ୍=False, ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍=2121, 전달규칙들=(), ସ୍ପଷ୍ଟତା_ମୂଲ୍ୟ=(640, 480), ଅତିଥି_ଠିକଣା=None, ଆୟୋଜକ_ଠିକଣା='127.0.0.1'):
    with ExitStack() as ସମ୍ପଦ, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି = None
        if ନେଟ୍_ୱାର୍କ୍:
            from ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍ import ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍
            ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି = ସମ୍ପଦ.enter_context(ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍(ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍, 전달규칙들, ଅତିଥି_ଠିକଣା=ଅତିଥି_ଠିକଣା, ଆୟୋଜକ_ଠିକଣା=ଆୟୋଜକ_ଠିକଣା))
        ପଥ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',ପୋର୍ଟ୍_ନମ୍ଵର୍)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି and (원격화면접속번호==ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍ or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ଆୟୋଜକ==원격화면접속번호 for 통신규약,ଆୟୋଜକ,_ in ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            ପ୍ରକ୍ରିୟା=subprocess.Popen(ନିର୍ଦ୍ଦେଶ(ସ୍ପଷ୍ଟତା_ମୂଲ୍ୟ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ପଥ)]+(ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି.전달인수() if ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ବ୍ରିଜ୍=ସଂଯୋଗ_ଡେସ୍କଟପ୍(ପ୍ରକ୍ରିୟା); ପାଠକ=threading.Thread(target=ବ୍ରିଜ୍.직렬입출력,daemon=True); ପାଠକ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ଆୟୋଜକ_ଠିକଣା,ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while ପ୍ରକ୍ରିୟା.poll() is None:
                    try: କ୍ଲାଏଣ୍ଟ,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): କ୍ଲାଏଣ୍ଟ.close(); continue
                    if not ପଥ.exists(): କ୍ଲାଏଣ୍ଟ.close(); continue
                    처리작업=threading.Thread(target=ବ୍ରିଜ୍.କ୍ଲାଏଣ୍ଟ,args=(କ୍ଲାଏଣ୍ଟ,ପଥ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ବ୍ରିଜ୍.닫힘=True
                if ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି: ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି.ବିରାମ_ଘଟଣା.set()
                if ପ୍ରକ୍ରିୟା.poll() is None:
                    ପ୍ରକ୍ରିୟା.terminate()
                    try: ପ୍ରକ୍ରିୟା.wait(timeout=5)
                    except subprocess.TimeoutExpired: ପ୍ରକ୍ରିୟା.kill(); ପ୍ରକ୍ରିୟା.wait()
                ପାଠକ.join(timeout=2); ପ୍ରକ୍ରିୟା.stdin.close(); ପ୍ରକ୍ରିୟା.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି and ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି.ତ୍ରୁଟି: raise RuntimeError('network bridge: '+ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି.ତ୍ରୁଟି)
            return 0 if 가로채기됨 else ପ୍ରକ୍ରିୟା.returncode


if __name__=='__main__':
    from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ଯୁକ୍ତି_ଆରେ=인수해석기.parse_args()
    if ଯୁକ୍ତି_ଆରେ.forward and not ଯୁକ୍ତି_ଆରେ.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ରନ୍_ଡେସ୍କଟପ୍(ଯୁକ୍ତି_ଆରେ.port,ନେଟ୍_ୱାର୍କ୍=ଯୁକ୍ତି_ଆରେ.network,ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍=ଯୁକ୍ତି_ଆରେ.ftp_port,전달규칙들=ଯୁକ୍ତି_ଆରେ.forward,ସ୍ପଷ୍ଟତା_ମୂଲ୍ୟ=ଯୁକ୍ତି_ଆରେ.resolution))
