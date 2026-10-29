#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, കീ_മൂല്യം 입력은 자체 കെര്_ണല്_മൂല്യം UART로 전달한다. localhost 전용, 단일 നിയന്ത്രണം_മൂല്യം 클라이언트.
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
from നടപ്പാക്കുക_കമാന്_ഡ് import ആജ്ഞ
from local_input import create


def 정확한값(소켓, വലിപ്പം):
    ഡാറ്റാ = bytearray()
    while len(ഡാറ്റാ) < വലിപ്പം:
        조각 = 소켓.recv(വലിപ്പം - len(ഡാറ്റാ))
        if not 조각: raise EOFError()
        ഡാറ്റാ.extend(조각)
    return bytes(ഡാറ്റാ)


class കീബോര്_ഡ്:
    def __init__(자신, അയയ്ക്കുക, 입력방식알림=None):
        자신.바이트전송 = അയയ്ക്കുക; 자신.മോഡിഫൈയര്_കീ = set(); 자신.പകര്_പ്പിടം_മൂല്യം = b''
        자신.한글조합기 = create(അയയ്ക്കുക, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.സ്വിച്ച്_കീ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def അയയ്ക്കുക(자신, ഡാറ്റാ):
        자신.한글조합기.조합확정()
        자신.바이트전송(ഡാറ്റാ)

    def സ്വിച്ച്_മോഡ്(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, കീ_nbsp_ചിഹ്നം):
        if കീ_nbsp_ചിഹ്നം in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.മോഡിഫൈയര്_കീ.add(കീ_nbsp_ചിഹ്നം)
            else: 자신.മോഡിഫൈയര്_കീ.discard(കീ_nbsp_ചിഹ്നം)
            return
        if not 누르는중:
            자신.സ്വിച്ച്_കീ.discard(കീ_nbsp_ചിഹ്നം)
            return
        CTRL_കീ = bool(자신.മോഡിഫൈയര്_കീ & {0xffe3, 0xffe4})
        SHIFT_കീ = bool(자신.മോഡിഫൈയര്_കീ & {0xffe1, 0xffe2})
        if CTRL_കീ and SHIFT_കീ and കീ_nbsp_ചിഹ്നം in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if കീ_nbsp_ചിഹ്നം in (32,0xff0d):
                try:
                    മൂല്യം=int(자신.유니코드입력,16)
                    if 32<=മൂല്യം<=0x10ffff and not 0xd800<=മൂല്യം<=0xdfff: 자신.അയയ്ക്കുക(chr(മൂല്യം).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif കീ_nbsp_ചിഹ്നം==0xff1b: 자신.유니코드입력=None
            elif കീ_nbsp_ചിഹ്നം==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif കീ_nbsp_ചിഹ്നം<128 and chr(കീ_nbsp_ചിഹ്നം) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(കീ_nbsp_ചിഹ്നം)
            return
        if കീ_nbsp_ചിഹ്നം in (0xff31,0xffc6) or കീ_nbsp_ചിഹ്നം==32 and SHIFT_കീ and not CTRL_കീ:
            if കീ_nbsp_ചിഹ്നം not in 자신.സ്വിച്ച്_കീ: 자신.സ്വിച്ച്_മോഡ്()
            자신.സ്വിച്ച്_കീ.add(കീ_nbsp_ചിഹ്നം)
            return
        if കീ_nbsp_ചിഹ്നം==0xff08 and 자신.한글여부 and not CTRL_കീ and 자신.한글조합기.앞글자지우기(): return
        if CTRL_കീ and SHIFT_കീ and കീ_nbsp_ചിഹ്നം in (ord('t'),ord('T')):
            자신.അയയ്ക്കുക(bytes([30,2,1,0,0,0,0])); return
        if കീ_nbsp_ചിഹ്നം==0xffc3: 자신.അയയ്ക്കുക(bytes([30,2,2,0,0,0,0])); return
        if കീ_nbsp_ചിഹ്നം==0xffc9: 자신.അയയ്ക്കുക(bytes([30,2,3,0,0,0,0])); return
        if CTRL_കീ and SHIFT_കീ and കീ_nbsp_ചിഹ്നം in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.അയയ്ക്കുക(자신.പകര്_പ്പിടം_മൂല്യം); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if കീ_nbsp_ചിഹ്നം in 특수글쇠: 자신.അയയ്ക്കുക(특수글쇠[കീ_nbsp_ചിഹ്നം]); return
        പ്രതീകം_എന്_കോഡുചെയ്യല് = കീ_nbsp_ചിഹ്നം & 0xffffff if കീ_nbsp_ചിഹ്നം & 0xff000000 == 0x01000000 else കീ_nbsp_ചിഹ്നം
        if പ്രതീകം_എന്_കോഡുചെയ്യല് > 0x10ffff or 0xd800 <= പ്രതീകം_എന്_കോഡുചെയ്യല് <= 0xdfff or കീ_nbsp_ചിഹ്നം >= 0xff00 and കീ_nbsp_ചിഹ്നം < 0x1000000: return
        if CTRL_കീ and 0x40 <= പ്രതീകം_എന്_കോഡുചെയ്യല് <= 0x7f: 자신.അയയ്ക്കുക(bytes([പ്രതീകം_എന്_കോഡുചെയ്യല് & 31])); return
        if പ്രതീകം_എന്_കോഡുചെയ്യല് < 32: return
        if 자신.한글여부 and 자신.മോഡിഫൈയര്_കീ & {0xffea,0xfe03,0xff7e} and not CTRL_കീ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ഫീഡ്_കീ(chr(പ്രതീകം_എന്_കോഡുചെയ്യല്), altgr=True): return
        앞부분 = b'\x1b' if 자신.മോഡിഫൈയര്_കീ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_കീ and not 앞부분 and 32<=പ്രതീകം_എന്_കോഡുചെയ്യല്<127:
            പ്രതീക_ഡാറ്റ=chr(പ്രതീകം_എന്_കോഡുചെയ്യല്).upper() if SHIFT_കീ else chr(പ്രതീകം_എന്_കോഡുചെയ്യല്)
            if 자신.한글조합기.ഫീഡ്_കീ(പ്രതീക_ഡാറ്റ): return
        자신.അയയ്ക്കുക(앞부분 + chr(പ്രതീകം_എന്_കോഡുചെയ്യല്).encode('utf-8'))


class കണക്റ്റ്_ഡെസ്ക്ടോപ്പ്:
    def __init__(자신, പ്രക്രിയ):
        자신.പ്രക്രിയ=പ്രക്രിയ; 자신.ലോക്ക്_മൂല്യം=threading.Lock(); 자신.준비완료=False; 자신.ടെ_ര്മിനല്=False; 자신.시작화면=False; 자신.닫힘=False

    def അയയ്ക്കുക(자신, ഡാറ്റാ):
        if not ഡാറ്റാ or 자신.닫힘: return
        with 자신.ലോക്ക്_മൂല്യം:
            try: 자신.പ്രക്രിയ.stdin.write(ഡാറ്റാ); 자신.പ്രക്രിയ.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ഡാറ്റാ=자신.പ്രക്രിയ.stdout.read(4096)
                if not ഡാറ്റാ: break
                sys.stdout.buffer.write(ഡാറ്റാ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ഡാറ്റാ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ടെ_ര്മിനല്=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.അയയ്ക്കുക(b'terminal\n')
        finally: 자신.닫힘=True

    def ക്ലയന്_റ്(자신, ക്ലയന്_റ്, വഴി):
        സെര്_വര്_മൂല്യം=socket.socket(socket.AF_UNIX); സെര്_വര്_മൂല്യം.settimeout(10); ക്ലയന്_റ്.settimeout(10)
        കീബോര്_ഡ്_എന്_ട്രി=കീബോര്_ഡ്(자신.അയയ്ക്കുക,lambda 한글여부:자신.അയയ്ക്കുക(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            സെര്_വര്_മൂല്യം.connect(str(വഴി))
            # 초기 협상은 순서대로 끝낸다. 이후 ഫലം 가닥만 클라이언트에 쓴다.
            ക്ലയന്_റ്.sendall(정확한값(സെര്_വര്_മൂല്യം,12))
            പതിപ്പ്_സംഖ്യ=정확한값(ക്ലയന്_റ്,12)
            if പതിപ്പ്_സംഖ്യ not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            സെര്_വര്_മൂല്യം.sendall(പതിപ്പ്_സംഖ്യ)
            개수=정확한값(സെര്_വര്_മൂല്യം,1);ക്ലയന്_റ്.sendall(개수+정확한값(സെര്_വര്_മൂല്യം,개수[0]))
            സുരക്ഷ=정확한값(ക്ലയന്_റ്,1)
            if സുരക്ഷ!=b'\x01': raise ValueError('unexpected security type')
            സെര്_വര്_മൂല്യം.sendall(സുരക്ഷ)
            if പതിപ്പ്_സംഖ്യ==b'RFB 003.008\n':ക്ലയന്_റ്.sendall(정확한값(സെര്_വര്_മൂല്യം,4))
            സെര്_വര്_മൂല്യം.sendall(정확한값(ക്ലയന്_റ്,1))
            초기값=정확한값(സെര്_വര്_മൂല്യം,24)
            ക്ലയന്_റ്.sendall(초기값+정확한값(സെര്_വര്_മൂല്യം,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ക്ലയന്_റ്.settimeout(None);സെര്_വര്_മൂല്യം.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        വകുപ്പ്_മൂല്യം=정확한값(സെര്_വര്_മൂല്യം,1)[0]
                        if വകുപ്പ്_മൂല്യം==0:
                            머리=정확한값(സെര്_വര്_മൂല്യം,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 വിദൂര_മൂല്യം 포인터의 중복을 피한다.
                            മറഞ്ഞ_മൂല്യം=포인터지원
                            if മറഞ്ഞ_മൂല്യം:ക്ലയന്_റ്.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ക്ലയന്_റ്.sendall(bytes([വകുപ്പ്_മൂല്യം])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(സെര്_വര്_മൂല്യം,12);가로,ലംബം_പദവി,폭,높이,എന്_കോഡുചെയ്യല്_മൂല്യം=struct.unpack('>HHHHi',사각형)
                                if എന്_കോഡുചെയ്യല്_മൂല്യം!=0:raise ValueError('unexpected framebuffer encoding: '+str(എന്_കോഡുചെയ്യല്_മൂല്യം))
                                ക്ലയന്_റ്.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ഡാറ്റാ=정확한값(സെര്_വര്_മൂല്യം,min(남음,65536));ക്ലയന്_റ്.sendall(ഡാറ്റാ);남음-=len(ഡാറ്റാ)
                        elif വകുപ്പ്_മൂല്യം==1:
                            머리=정확한값(സെര്_വര്_മൂല്യം,5);개수=struct.unpack('>H',머리[3:])[0]
                            ക്ലയന്_റ്.sendall(bytes([വകുപ്പ്_മൂല്യം])+머리+정확한값(സെര്_വര്_മൂല്യം,개수*6))
                        elif വകുപ്പ്_മൂല്യം==2:ക്ലയന്_റ്.sendall(bytes([വകുപ്പ്_മൂല്യം]))
                        elif വകുപ്പ്_മൂല്യം==3:
                            머리=정확한값(സെര്_വര്_മൂല്യം,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ക്ലയന്_റ്.sendall(bytes([വകുപ്പ്_മൂല്യം])+머리+정확한값(സെര്_വര്_മൂല്യം,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(വകുപ്പ്_മൂല്യം))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ക്ലയന്_റ്.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                വകുപ്പ്_മൂല്യം=정확한값(ക്ലയന്_റ്,1)[0]
                if വകുപ്പ്_മൂല്യം==4:
                    മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,7); കീബോര്_ഡ്_എന്_ട്രി.누름값(മുഖ്യ_പാഠം[0]!=0,struct.unpack('>I',മുഖ്യ_പാഠം[3:])[0]); continue
                if വകുപ്പ്_മൂല്യം==255:
                    മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,11)
                    if മുഖ്യ_പാഠം[0]!=0: raise ValueError('unsupported QEMU input extension')
                    കീബോര്_ഡ്_എന്_ട്രി.누름값(struct.unpack('>H',മുഖ്യ_പാഠം[1:3])[0]!=0,struct.unpack('>I',മുഖ്യ_പാഠം[3:7])[0]); continue
                if വകുപ്പ്_മൂല്യം==5:
                    മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,5); 단추들,x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം=struct.unpack('>BHH',മുഖ്യ_പാഠം)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: കീബോര്_ഡ്_എന്_ട്രി.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_ഏകോപനം<576 and 112<=Y_ബട്ടൺ_ഏകോപനം<372:
                        തിരഞ്ഞു_നോക്കൽ_സൂചിക=(Y_ബട്ടൺ_ഏകോപനം-112)//52
                        if (Y_ബട്ടൺ_ഏകോപനം-112)%52<40 and തിരഞ്ഞു_നോക്കൽ_സൂചിക<5: 자신.അയയ്ക്കുക(bytes([ord('1')+തിരഞ്ഞു_നോക്കൽ_സൂചിക]))
                    else: 자신.അയയ്ക്കുക(bytes([30,1,단추들,x_ഏകോപനം&255,x_ഏകോപനം>>8,Y_ബട്ടൺ_ഏകോപനം&255,Y_ബട്ടൺ_ഏകോപനം>>8]))
                    continue
                if വകുപ്പ്_മൂല്യം==6:
                    മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,7); ദൈര്_ഘ്യം_മൂല്യം=struct.unpack('>i',മുഖ്യ_പാഠം[3:])[0]
                    if abs(ദൈര്_ഘ്യം_മൂല്യം)>65536: raise ValueError('clipboard too large')
                    പദാവലി=정확한값(ക്ലയന്_റ്,abs(ദൈര്_ഘ്യം_മൂല്യം))
                    if ദൈര്_ഘ്യം_മൂല്യം>=0:
                        try: കീബോര്_ഡ്_എന്_ട്രി.പകര്_പ്പിടം_മൂല്യം=പദാവലി.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: കീബോര്_ഡ്_എന്_ട്രി.പകര്_പ്പിടം_മൂല്യം=പദാവലി.decode('latin-1').encode('utf-8')
                        കീബോര്_ഡ്_എന്_ട്രി.പകര്_പ്പിടം_മൂല്യം=കീബോര്_ഡ്_എന്_ട്രി.പകര്_പ്പിടം_മൂല്യം[:65536].decode('utf-8','ignore').encode('utf-8')
                    സെര്_വര്_മൂല്യം.sendall(bytes([വകുപ്പ്_മൂല്യം])+മുഖ്യ_പാഠം+പദാവലി); continue
                if വകുപ്പ്_മൂല്യം==0:
                    മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,19)
                    if മുഖ്യ_പാഠം[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=മുഖ്യ_പാഠം[3]//8
                elif വകുപ്പ്_മൂല്യം==2:
                    മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,3); 항목수=struct.unpack('>H',മുഖ്യ_പാഠം[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ക്ലയന്_റ്,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 സ്ഥിരസ്ഥിതി_മൂല്യം Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    മുഖ്യ_പാഠം=struct.pack('>BHi',0,1,0)
                elif വകുപ്പ്_മൂല്യം in (3,150): മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,9)
                elif വകുപ്പ്_മൂല്യം==248:
                    മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,8)
                    if മുഖ്യ_പാഠം[7]>64: raise ValueError('fence too large')
                    മുഖ്യ_പാഠം+=정확한값(ക്ലയന്_റ്,മുഖ്യ_പാഠം[7])
                elif വകുപ്പ്_മൂല്യം==250: മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,3)
                elif വകുപ്പ്_മൂല്യം==251:
                    മുഖ്യ_പാഠം=정확한값(ക്ലയന്_റ്,7)
                    if മുഖ്യ_പാഠം[5]>16: raise ValueError('too many screens')
                    മുഖ്യ_പാഠം+=정확한값(ക്ലയന്_റ്,മുഖ്യ_പാഠം[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(വകുപ്പ്_മൂല്യം))
                സെര്_വര്_മൂല്യം.sendall(bytes([വകുപ്പ്_മൂല്യം])+മുഖ്യ_പാഠം)
        except (OSError,EOFError,ValueError) as പിശക്:
            if str(പിശക്): print('VNC client:',പിശക്,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ക്ലയന്_റ്,സെര്_വര്_മൂല്യം):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def റണ്_ഡെസ്ക്ടോപ്പ്(പോര്_ട്ട്_നമ്പര്=5902, നെറ്റ്_വർക്ക്=False, ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്=2121, 전달규칙들=(), റെസലൂഷന്_മൂല്യം=(640, 480), അതിഥി_ഇമെയിൽ=None, ഹോസ്റ്റ്_ഇമെയിൽ='127.0.0.1'):
    with ExitStack() as വിഭവങ്ങള്, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി = None
        if നെറ്റ്_വർക്ക്:
            from നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ് import നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്
            നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി = വിഭവങ്ങള്.enter_context(നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്(ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്, 전달규칙들, അതിഥി_ഇമെയിൽ=അതിഥി_ഇമെയിൽ, ഹോസ്റ്റ്_ഇമെയിൽ=ഹോസ്റ്റ്_ഇമെയിൽ))
        വഴി=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',പോര്_ട്ട്_നമ്പര്)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി and (원격화면접속번호==ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര് or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ഹോസ്റ്റ്==원격화면접속번호 for 통신규약,ഹോസ്റ്റ്,_ in നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            പ്രക്രിയ=subprocess.Popen(ആജ്ഞ(റെസലൂഷന്_മൂല്യം)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(വഴി)]+(നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി.전달인수() if നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ബ്രിഡ്_ജ്=കണക്റ്റ്_ഡെസ്ക്ടോപ്പ്(പ്രക്രിയ); റീഡര്=threading.Thread(target=ബ്രിഡ്_ജ്.직렬입출력,daemon=True); റീഡര്.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ഹോസ്റ്റ്_ഇമെയിൽ,ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്),flush=True)
            def അവസാനിപ്പിക്കുക(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,അവസാനിപ്പിക്കുക)
            처리작업=None; 가로채기됨=False
            try:
                while പ്രക്രിയ.poll() is None:
                    try: ക്ലയന്_റ്,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ക്ലയന്_റ്.close(); continue
                    if not വഴി.exists(): ക്ലയന്_റ്.close(); continue
                    처리작업=threading.Thread(target=ബ്രിഡ്_ജ്.ക്ലയന്_റ്,args=(ക്ലയന്_റ്,വഴി),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ബ്രിഡ്_ജ്.닫힘=True
                if നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി: നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി.അല്_പം_നിര്_ത്തുക_ഇവന്റ്.set()
                if പ്രക്രിയ.poll() is None:
                    പ്രക്രിയ.terminate()
                    try: പ്രക്രിയ.wait(timeout=5)
                    except subprocess.TimeoutExpired: പ്രക്രിയ.kill(); പ്രക്രിയ.wait()
                റീഡര്.join(timeout=2); പ്രക്രിയ.stdin.close(); പ്രക്രിയ.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി and നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി.പിശക്: raise RuntimeError('network bridge: '+നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്_എന്_ട്രി.പിശക്)
            return 0 if 가로채기됨 else പ്രക്രിയ.returncode


if __name__=='__main__':
    from നടപ്പാക്കുക_കമാന്_ഡ് import 해상도읽기
    പാഴ്_സർ=argparse.ArgumentParser(description=__doc__); പാഴ്_സർ.add_argument('--port',type=int,default=5902)
    പാഴ്_സർ.add_argument('--resolution',type=해상도읽기,default=(640,480))
    പാഴ്_സർ.add_argument('--network',action='store_true'); പാഴ്_സർ.add_argument('--ftp-port',type=int,default=2121)
    പാഴ്_സർ.add_argument('--forward',action='append',default=[])
    ആര്_ഗ്യുമെന്_റ്_അരേ=പാഴ്_സർ.parse_args()
    if ആര്_ഗ്യുമെന്_റ്_അരേ.forward and not ആര്_ഗ്യുമെന്_റ്_അരേ.network: പാഴ്_സർ.error('--forward requires --network')
    raise SystemExit(റണ്_ഡെസ്ക്ടോപ്പ്(ആര്_ഗ്യുമെന്_റ്_അരേ.port,നെറ്റ്_വർക്ക്=ആര്_ഗ്യുമെന്_റ്_അരേ.network,ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്=ആര്_ഗ്യുമെന്_റ്_അരേ.ftp_port,전달규칙들=ആര്_ഗ്യുമെന്_റ്_അരേ.forward,റെസലൂഷന്_മൂല്യം=ആര്_ഗ്യുമെന്_റ്_അരേ.resolution))
