#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ئاچقۇچ_قىممىتى 입력은 자체 يادرو_قىممىتى UART로 전달한다. localhost 전용, 단일 كونترول_قىممىتى 클라이언트.
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
from ئىجرا_قىلىش_بۇيرۇق import بۇيرۇق
from local_input import create


def 정확한값(소켓, چوڭلۇقى):
    مەلۇمات = bytearray()
    while len(مەلۇمات) < چوڭلۇقى:
        조각 = 소켓.recv(چوڭلۇقى - len(مەلۇمات))
        if not 조각: raise EOFError()
        مەلۇمات.extend(조각)
    return bytes(مەلۇمات)


class كۇنۇپكا_تاختىسى:
    def __init__(자신, ئەۋەتمەك, 입력방식알림=None):
        자신.바이트전송 = ئەۋەتمەك; 자신.ئۆزگەرتىش_كۇنۇپكىسى = set(); 자신.كېسىپ_چاپلاش_تاختىسى_قىممىتى = b''
        자신.한글조합기 = create(ئەۋەتمەك, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ئۆزگەرتمەك_ئاچقۇچ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ئەۋەتمەك(자신, مەلۇمات):
        자신.한글조합기.조합확정()
        자신.바이트전송(مەلۇمات)

    def ئۆزگەرتمەك_ھالەت(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ئاچقۇچ_بەلگە):
        if ئاچقۇچ_بەلگە in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ئۆزگەرتىش_كۇنۇپكىسى.add(ئاچقۇچ_بەلگە)
            else: 자신.ئۆزگەرتىش_كۇنۇپكىسى.discard(ئاچقۇچ_بەلگە)
            return
        if not 누르는중:
            자신.ئۆزگەرتمەك_ئاچقۇچ.discard(ئاچقۇچ_بەلگە)
            return
        كونترول_ئاچقۇچ = bool(자신.ئۆزگەرتىش_كۇنۇپكىسى & {0xffe3, 0xffe4})
        SHIFT_كۇنۇپكىسى = bool(자신.ئۆزگەرتىش_كۇنۇپكىسى & {0xffe1, 0xffe2})
        if كونترول_ئاچقۇچ and SHIFT_كۇنۇپكىسى and ئاچقۇچ_بەلگە in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ئاچقۇچ_بەلگە in (32,0xff0d):
                try:
                    قىممىتى=int(자신.유니코드입력,16)
                    if 32<=قىممىتى<=0x10ffff and not 0xd800<=قىممىتى<=0xdfff: 자신.ئەۋەتمەك(chr(قىممىتى).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ئاچقۇچ_بەلگە==0xff1b: 자신.유니코드입력=None
            elif ئاچقۇچ_بەلگە==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ئاچقۇچ_بەلگە<128 and chr(ئاچقۇچ_بەلگە) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ئاچقۇچ_بەلگە)
            return
        if ئاچقۇچ_بەلگە in (0xff31,0xffc6) or ئاچقۇچ_بەلگە==32 and SHIFT_كۇنۇپكىسى and not كونترول_ئاچقۇچ:
            if ئاچقۇچ_بەلگە not in 자신.ئۆزگەرتمەك_ئاچقۇچ: 자신.ئۆزگەرتمەك_ھالەت()
            자신.ئۆزگەرتمەك_ئاچقۇچ.add(ئاچقۇچ_بەلگە)
            return
        if ئاچقۇچ_بەلگە==0xff08 and 자신.한글여부 and not كونترول_ئاچقۇچ and 자신.한글조합기.앞글자지우기(): return
        if كونترول_ئاچقۇچ and SHIFT_كۇنۇپكىسى and ئاچقۇچ_بەلگە in (ord('t'),ord('T')):
            자신.ئەۋەتمەك(bytes([30,2,1,0,0,0,0])); return
        if ئاچقۇچ_بەلگە==0xffc3: 자신.ئەۋەتمەك(bytes([30,2,2,0,0,0,0])); return
        if ئاچقۇچ_بەلگە==0xffc9: 자신.ئەۋەتمەك(bytes([30,2,3,0,0,0,0])); return
        if كونترول_ئاچقۇچ and SHIFT_كۇنۇپكىسى and ئاچقۇچ_بەلگە in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ئەۋەتمەك(자신.كېسىپ_چاپلاش_تاختىسى_قىممىتى); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ئاچقۇچ_بەلگە in 특수글쇠: 자신.ئەۋەتمەك(특수글쇠[ئاچقۇچ_بەلگە]); return
        ھەرپ_بەلگە_كودىلاش = ئاچقۇچ_بەلگە & 0xffffff if ئاچقۇچ_بەلگە & 0xff000000 == 0x01000000 else ئاچقۇچ_بەلگە
        if ھەرپ_بەلگە_كودىلاش > 0x10ffff or 0xd800 <= ھەرپ_بەلگە_كودىلاش <= 0xdfff or ئاچقۇچ_بەلگە >= 0xff00 and ئاچقۇچ_بەلگە < 0x1000000: return
        if كونترول_ئاچقۇچ and 0x40 <= ھەرپ_بەلگە_كودىلاش <= 0x7f: 자신.ئەۋەتمەك(bytes([ھەرپ_بەلگە_كودىلاش & 31])); return
        if ھەرپ_بەلگە_كودىلاش < 32: return
        if 자신.한글여부 and 자신.ئۆزگەرتىش_كۇنۇپكىسى & {0xffea,0xfe03,0xff7e} and not كونترول_ئاچقۇچ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ئۇچۇر_ئاچقۇچ(chr(ھەرپ_بەلگە_كودىلاش), altgr=True): return
        앞부분 = b'\x1b' if 자신.ئۆزگەرتىش_كۇنۇپكىسى & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not كونترول_ئاچقۇچ and not 앞부분 and 32<=ھەرپ_بەلگە_كودىلاش<127:
            ھەرپ_بەلگە_مەلۇمات=chr(ھەرپ_بەلگە_كودىلاش).upper() if SHIFT_كۇنۇپكىسى else chr(ھەرپ_بەلگە_كودىلاش)
            if 자신.한글조합기.ئۇچۇر_ئاچقۇچ(ھەرپ_بەلگە_مەلۇمات): return
        자신.ئەۋەتمەك(앞부분 + chr(ھەرپ_بەلگە_كودىلاش).encode('utf-8'))


class ئۇلاش_ئۈستەليۈزى:
    def __init__(자신, جەريان):
        자신.جەريان=جەريان; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.تېرمىنال=False; 자신.시작화면=False; 자신.닫힘=False

    def ئەۋەتمەك(자신, مەلۇمات):
        if not مەلۇمات or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.جەريان.stdin.write(مەلۇمات); 자신.جەريان.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                مەلۇمات=자신.جەريان.stdout.read(4096)
                if not مەلۇمات: break
                sys.stdout.buffer.write(مەلۇمات); sys.stdout.buffer.flush()
                끝부분=(끝부분+مەلۇمات)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.تېرمىنال=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ئەۋەتمەك(b'terminal\n')
        finally: 자신.닫힘=True

    def ئابۇنىتېر(자신, ئابۇنىتېر, يول):
        مۇلازىمىتېر_قىممىتى=socket.socket(socket.AF_UNIX); مۇلازىمىتېر_قىممىتى.settimeout(10); ئابۇنىتېر.settimeout(10)
        كۇنۇپكا_تاختىسى_كىرگۈزۈش=كۇنۇپكا_تاختىسى(자신.ئەۋەتمەك,lambda 한글여부:자신.ئەۋەتمەك(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            مۇلازىمىتېر_قىممىتى.connect(str(يول))
            # 초기 협상은 순서대로 끝낸다. 이후 چىقار 가닥만 클라이언트에 쓴다.
            ئابۇنىتېر.sendall(정확한값(مۇلازىمىتېر_قىممىتى,12))
            판번호=정확한값(ئابۇنىتېر,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            مۇلازىمىتېر_قىممىتى.sendall(판번호)
            개수=정확한값(مۇلازىمىتېر_قىممىتى,1);ئابۇنىتېر.sendall(개수+정확한값(مۇلازىمىتېر_قىممىتى,개수[0]))
            خەۋپسىز=정확한값(ئابۇنىتېر,1)
            if خەۋپسىز!=b'\x01': raise ValueError('unexpected security type')
            مۇلازىمىتېر_قىممىتى.sendall(خەۋپسىز)
            if 판번호==b'RFB 003.008\n':ئابۇنىتېر.sendall(정확한값(مۇلازىمىتېر_قىممىتى,4))
            مۇلازىمىتېر_قىممىتى.sendall(정확한값(ئابۇنىتېر,1))
            초기값=정확한값(مۇلازىمىتېر_قىممىتى,24)
            ئابۇنىتېر.sendall(초기값+정확한값(مۇلازىمىتېر_قىممىتى,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ئابۇنىتېر.settimeout(None);مۇلازىمىتېر_قىممىتى.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        تۈر_قىممىتى=정확한값(مۇلازىمىتېر_قىممىتى,1)[0]
                        if تۈر_قىممىتى==0:
                            머리=정확한값(مۇلازىمىتېر_قىممىتى,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 يىراق_قىممىتى 포인터의 중복을 피한다.
                            يوشۇرۇن_قىممىتى=포인터지원
                            if يوشۇرۇن_قىممىتى:ئابۇنىتېر.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ئابۇنىتېر.sendall(bytes([تۈر_قىممىتى])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(مۇلازىمىتېر_قىممىتى,12);가로,تىك_ئورۇنلاشتۇرۇش,폭,높이,كودىلاش_قىممىتى=struct.unpack('>HHHHi',사각형)
                                if كودىلاش_قىممىتى!=0:raise ValueError('unexpected framebuffer encoding: '+str(كودىلاش_قىممىتى))
                                ئابۇنىتېر.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    مەلۇمات=정확한값(مۇلازىمىتېر_قىممىتى,min(남음,65536));ئابۇنىتېر.sendall(مەلۇمات);남음-=len(مەلۇمات)
                        elif تۈر_قىممىتى==1:
                            머리=정확한값(مۇلازىمىتېر_قىممىتى,5);개수=struct.unpack('>H',머리[3:])[0]
                            ئابۇنىتېر.sendall(bytes([تۈر_قىممىتى])+머리+정확한값(مۇلازىمىتېر_قىممىتى,개수*6))
                        elif تۈر_قىممىتى==2:ئابۇنىتېر.sendall(bytes([تۈر_قىممىتى]))
                        elif تۈر_قىممىتى==3:
                            머리=정확한값(مۇلازىمىتېر_قىممىتى,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ئابۇنىتېر.sendall(bytes([تۈر_قىممىتى])+머리+정확한값(مۇلازىمىتېر_قىممىتى,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(تۈر_قىممىتى))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ئابۇنىتېر.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                تۈر_قىممىتى=정확한값(ئابۇنىتېر,1)[0]
                if تۈر_قىممىتى==4:
                    مەزمۇن=정확한값(ئابۇنىتېر,7); كۇنۇپكا_تاختىسى_كىرگۈزۈش.누름값(مەزمۇن[0]!=0,struct.unpack('>I',مەزمۇن[3:])[0]); continue
                if تۈر_قىممىتى==255:
                    مەزمۇن=정확한값(ئابۇنىتېر,11)
                    if مەزمۇن[0]!=0: raise ValueError('unsupported QEMU input extension')
                    كۇنۇپكا_تاختىسى_كىرگۈزۈش.누름값(struct.unpack('>H',مەزمۇن[1:3])[0]!=0,struct.unpack('>I',مەزمۇن[3:7])[0]); continue
                if تۈر_قىممىتى==5:
                    مەزمۇن=정확한값(ئابۇنىتېر,5); 단추들,x_كوردىنات,세로좌표=struct.unpack('>BHH',مەزمۇن)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: كۇنۇپكا_تاختىسى_كىرگۈزۈش.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_كوردىنات<576 and 112<=세로좌표<372:
                        ئىزدەش_ئىندېكس=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and ئىزدەش_ئىندېكس<5: 자신.ئەۋەتمەك(bytes([ord('1')+ئىزدەش_ئىندېكس]))
                    else: 자신.ئەۋەتمەك(bytes([30,1,단추들,x_كوردىنات&255,x_كوردىنات>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if تۈر_قىممىتى==6:
                    مەزمۇن=정확한값(ئابۇنىتېر,7); ئۇزۇنلۇق_قىممىتى=struct.unpack('>i',مەزمۇن[3:])[0]
                    if abs(ئۇزۇنلۇق_قىممىتى)>65536: raise ValueError('clipboard too large')
                    تېكىست=정확한값(ئابۇنىتېر,abs(ئۇزۇنلۇق_قىممىتى))
                    if ئۇزۇنلۇق_قىممىتى>=0:
                        try: كۇنۇپكا_تاختىسى_كىرگۈزۈش.كېسىپ_چاپلاش_تاختىسى_قىممىتى=تېكىست.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: كۇنۇپكا_تاختىسى_كىرگۈزۈش.كېسىپ_چاپلاش_تاختىسى_قىممىتى=تېكىست.decode('latin-1').encode('utf-8')
                        كۇنۇپكا_تاختىسى_كىرگۈزۈش.كېسىپ_چاپلاش_تاختىسى_قىممىتى=كۇنۇپكا_تاختىسى_كىرگۈزۈش.كېسىپ_چاپلاش_تاختىسى_قىممىتى[:65536].decode('utf-8','ignore').encode('utf-8')
                    مۇلازىمىتېر_قىممىتى.sendall(bytes([تۈر_قىممىتى])+مەزمۇن+تېكىست); continue
                if تۈر_قىممىتى==0:
                    مەزمۇن=정확한값(ئابۇنىتېر,19)
                    if مەزمۇن[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=مەزمۇن[3]//8
                elif تۈر_قىممىتى==2:
                    مەزمۇن=정확한값(ئابۇنىتېر,3); 항목수=struct.unpack('>H',مەزمۇن[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ئابۇنىتېر,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 سۈكۈتتىكى_قىممەت Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    مەزمۇن=struct.pack('>BHi',0,1,0)
                elif تۈر_قىممىتى in (3,150): مەزمۇن=정확한값(ئابۇنىتېر,9)
                elif تۈر_قىممىتى==248:
                    مەزمۇن=정확한값(ئابۇنىتېر,8)
                    if مەزمۇن[7]>64: raise ValueError('fence too large')
                    مەزمۇن+=정확한값(ئابۇنىتېر,مەزمۇن[7])
                elif تۈر_قىممىتى==250: مەزمۇن=정확한값(ئابۇنىتېر,3)
                elif تۈر_قىممىتى==251:
                    مەزمۇن=정확한값(ئابۇنىتېر,7)
                    if مەزمۇن[5]>16: raise ValueError('too many screens')
                    مەزمۇن+=정확한값(ئابۇنىتېر,مەزمۇن[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(تۈر_قىممىتى))
                مۇلازىمىتېر_قىممىتى.sendall(bytes([تۈر_قىممىتى])+مەزمۇن)
        except (OSError,EOFError,ValueError) as خاتالىق:
            if str(خاتالىق): print('VNC client:',خاتالىق,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ئابۇنىتېر,مۇلازىمىتېر_قىممىتى):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def قوزغىتىش_ئۈستەليۈزى(접속번호=5902, تور=False, 파일전송접속번호=2121, 전달규칙들=(), ئېنىقلىق_قىممىتى=(640, 480), مېھمان_ئادرېس=None, باقار_ئادرېس='127.0.0.1'):
    with ExitStack() as بايلىقلار, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        تور_كۆۋرۈك_كىرگۈزۈش = None
        if تور:
            from تور_كۆۋرۈك import تور_كۆۋرۈك
            تور_كۆۋرۈك_كىرگۈزۈش = بايلىقلار.enter_context(تور_كۆۋرۈك(파일전송접속번호, 전달규칙들, مېھمان_ئادرېس=مېھمان_ئادرېس, باقار_ئادرېس=باقار_ئادرېس))
        يول=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if تور_كۆۋرۈك_كىرگۈزۈش and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and باقار==원격화면접속번호 for 통신규약,باقار,_ in تور_كۆۋرۈك_كىرگۈزۈش.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            جەريان=subprocess.Popen(بۇيرۇق(ئېنىقلىق_قىممىتى)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(يول)]+(تور_كۆۋرۈك_كىرگۈزۈش.전달인수() if تور_كۆۋرۈك_كىرگۈزۈش else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            كۆۋرۈك=ئۇلاش_ئۈستەليۈزى(جەريان); ئوقۇغۇچ=threading.Thread(target=كۆۋرۈك.직렬입출력,daemon=True); ئوقۇغۇچ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if تور_كۆۋرۈك_كىرگۈزۈش: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(باقار_ئادرېس,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while جەريان.poll() is None:
                    try: ئابۇنىتېر,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ئابۇنىتېر.close(); continue
                    if not يول.exists(): ئابۇنىتېر.close(); continue
                    처리작업=threading.Thread(target=كۆۋرۈك.ئابۇنىتېر,args=(ئابۇنىتېر,يول),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                كۆۋرۈك.닫힘=True
                if تور_كۆۋرۈك_كىرگۈزۈش: تور_كۆۋرۈك_كىرگۈزۈش.تورمۇزلىماق_ھادىسە.set()
                if جەريان.poll() is None:
                    جەريان.terminate()
                    try: جەريان.wait(timeout=5)
                    except subprocess.TimeoutExpired: جەريان.kill(); جەريان.wait()
                ئوقۇغۇچ.join(timeout=2); جەريان.stdin.close(); جەريان.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if تور_كۆۋرۈك_كىرگۈزۈش and تور_كۆۋرۈك_كىرگۈزۈش.خاتالىق: raise RuntimeError('network bridge: '+تور_كۆۋرۈك_كىرگۈزۈش.خاتالىق)
            return 0 if 가로채기됨 else جەريان.returncode


if __name__=='__main__':
    from ئىجرا_قىلىش_بۇيرۇق import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    دەلىل_رەت=인수해석기.parse_args()
    if دەلىل_رەت.forward and not دەلىل_رەت.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(قوزغىتىش_ئۈستەليۈزى(دەلىل_رەت.port,تور=دەلىل_رەت.network,파일전송접속번호=دەلىل_رەت.ftp_port,전달규칙들=دەلىل_رەت.forward,ئېنىقلىق_قىممىتى=دەلىل_رەت.resolution))
