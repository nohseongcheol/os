#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, کلیل_نرخ 입력은 자체 کوورەک_نرخ UART로 전달한다. localhost 전용, 단일 کۆنترۆڵ_نرخ 클라이언트.
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
from جێبەجێکردن_فەرمان import فەرمان
from local_input import create


def 정확한값(소켓, گۆڕینی_ئەندازە):
    دەیتا = bytearray()
    while len(دەیتا) < گۆڕینی_ئەندازە:
        조각 = 소켓.recv(گۆڕینی_ئەندازە - len(دەیتا))
        if not 조각: raise EOFError()
        دەیتا.extend(조각)
    return bytes(دەیتا)


class تەختەکلیل:
    def __init__(자신, ناردن, 입력방식알림=None):
        자신.바이트전송 = ناردن; 자신.کلیلی_گۆڕین = set(); 자신.ڕوونووسگە_نرخ = b''
        자신.한글조합기 = create(ناردن, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.گۆڕین_کلیل = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ناردن(자신, دەیتا):
        자신.한글조합기.조합확정()
        자신.바이트전송(دەیتا)

    def گۆڕین_دۆخ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, کلیل_سیمبۆل):
        if کلیل_سیمبۆل in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.کلیلی_گۆڕین.add(کلیل_سیمبۆل)
            else: 자신.کلیلی_گۆڕین.discard(کلیل_سیمبۆل)
            return
        if not 누르는중:
            자신.گۆڕین_کلیل.discard(کلیل_سیمبۆل)
            return
        CTRL = bool(자신.کلیلی_گۆڕین & {0xffe3, 0xffe4})
        کلیلی_SHIFT = bool(자신.کلیلی_گۆڕین & {0xffe1, 0xffe2})
        if CTRL and کلیلی_SHIFT and کلیل_سیمبۆل in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if کلیل_سیمبۆل in (32,0xff0d):
                try:
                    نرخ=int(자신.유니코드입력,16)
                    if 32<=نرخ<=0x10ffff and not 0xd800<=نرخ<=0xdfff: 자신.ناردن(chr(نرخ).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif کلیل_سیمبۆل==0xff1b: 자신.유니코드입력=None
            elif کلیل_سیمبۆل==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif کلیل_سیمبۆل<128 and chr(کلیل_سیمبۆل) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(کلیل_سیمبۆل)
            return
        if کلیل_سیمبۆل in (0xff31,0xffc6) or کلیل_سیمبۆل==32 and کلیلی_SHIFT and not CTRL:
            if کلیل_سیمبۆل not in 자신.گۆڕین_کلیل: 자신.گۆڕین_دۆخ()
            자신.گۆڕین_کلیل.add(کلیل_سیمبۆل)
            return
        if کلیل_سیمبۆل==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and کلیلی_SHIFT and کلیل_سیمبۆل in (ord('t'),ord('T')):
            자신.ناردن(bytes([30,2,1,0,0,0,0])); return
        if کلیل_سیمبۆل==0xffc3: 자신.ناردن(bytes([30,2,2,0,0,0,0])); return
        if کلیل_سیمبۆل==0xffc9: 자신.ناردن(bytes([30,2,3,0,0,0,0])); return
        if CTRL and کلیلی_SHIFT and کلیل_سیمبۆل in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ناردن(자신.ڕوونووسگە_نرخ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if کلیل_سیمبۆل in 특수글쇠: 자신.ناردن(특수글쇠[کلیل_سیمبۆل]); return
        نووسە_نهێنبەندی = کلیل_سیمبۆل & 0xffffff if کلیل_سیمبۆل & 0xff000000 == 0x01000000 else کلیل_سیمبۆل
        if نووسە_نهێنبەندی > 0x10ffff or 0xd800 <= نووسە_نهێنبەندی <= 0xdfff or کلیل_سیمبۆل >= 0xff00 and کلیل_سیمبۆل < 0x1000000: return
        if CTRL and 0x40 <= نووسە_نهێنبەندی <= 0x7f: 자신.ناردن(bytes([نووسە_نهێنبەندی & 31])); return
        if نووسە_نهێنبەندی < 32: return
        if 자신.한글여부 and 자신.کلیلی_گۆڕین & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.فید_کلیل(chr(نووسە_نهێنبەندی), altgr=True): return
        앞부분 = b'\x1b' if 자신.کلیلی_گۆڕین & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=نووسە_نهێنبەندی<127:
            نووسە_دەیتا=chr(نووسە_نهێنبەندی).upper() if کلیلی_SHIFT else chr(نووسە_نهێنبەندی)
            if 자신.한글조합기.فید_کلیل(نووسە_دەیتا): return
        자신.ناردن(앞부분 + chr(نووسە_نهێنبەندی).encode('utf-8'))


class لكاندن_دێسکتۆپ:
    def __init__(자신, پرۆسە):
        자신.پرۆسە=پرۆسە; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def ناردن(자신, دەیتا):
        if not دەیتا or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.پرۆسە.stdin.write(دەیتا); 자신.پرۆسە.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                دەیتا=자신.پرۆسە.stdout.read(4096)
                if not دەیتا: break
                sys.stdout.buffer.write(دەیتا); sys.stdout.buffer.flush()
                끝부분=(끝부분+دەیتا)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ناردن(b'terminal\n')
        finally: 자신.닫힘=True

    def کلایەنت(자신, کلایەنت, گوزەر):
        ڕاژەکار_نرخ=socket.socket(socket.AF_UNIX); ڕاژەکار_نرخ.settimeout(10); کلایەنت.settimeout(10)
        تەختەکلیل_تێنووسین=تەختەکلیل(자신.ناردن,lambda 한글여부:자신.ناردن(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ڕاژەکار_نرخ.connect(str(گوزەر))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            کلایەنت.sendall(정확한값(ڕاژەکار_نرخ,12))
            판번호=정확한값(کلایەنت,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ڕاژەکار_نرخ.sendall(판번호)
            개수=정확한값(ڕاژەکار_نرخ,1);کلایەنت.sendall(개수+정확한값(ڕاژەکار_نرخ,개수[0]))
            ئاسایش=정확한값(کلایەنت,1)
            if ئاسایش!=b'\x01': raise ValueError('unexpected security type')
            ڕاژەکار_نرخ.sendall(ئاسایش)
            if 판번호==b'RFB 003.008\n':کلایەنت.sendall(정확한값(ڕاژەکار_نرخ,4))
            ڕاژەکار_نرخ.sendall(정확한값(کلایەنت,1))
            초기값=정확한값(ڕاژەکار_نرخ,24)
            کلایەنت.sendall(초기값+정확한값(ڕاژەکار_نرخ,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            کلایەنت.settimeout(None);ڕاژەکار_نرخ.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        پۆل_نرخ=정확한값(ڕاژەکار_نرخ,1)[0]
                        if پۆل_نرخ==0:
                            머리=정확한값(ڕاژەکار_نرخ,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 دوورەدەس_نرخ 포인터의 중복을 피한다.
                            شاراوە_نرخ=포인터지원
                            if شاراوە_نرخ:کلایەنت.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            کلایەنت.sendall(bytes([پۆل_نرخ])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ڕاژەکار_نرخ,12);가로,세로,폭,높이,نهێنبەندی_نرخ=struct.unpack('>HHHHi',사각형)
                                if نهێنبەندی_نرخ!=0:raise ValueError('unexpected framebuffer encoding: '+str(نهێنبەندی_نرخ))
                                کلایەنت.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    دەیتا=정확한값(ڕاژەکار_نرخ,min(남음,65536));کلایەنت.sendall(دەیتا);남음-=len(دەیتا)
                        elif پۆل_نرخ==1:
                            머리=정확한값(ڕاژەکار_نرخ,5);개수=struct.unpack('>H',머리[3:])[0]
                            کلایەنت.sendall(bytes([پۆل_نرخ])+머리+정확한값(ڕاژەکار_نرخ,개수*6))
                        elif پۆل_نرخ==2:کلایەنت.sendall(bytes([پۆل_نرخ]))
                        elif پۆل_نرخ==3:
                            머리=정확한값(ڕاژەکار_نرخ,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            کلایەنت.sendall(bytes([پۆل_نرخ])+머리+정확한값(ڕاژەکار_نرخ,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(پۆل_نرخ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:کلایەنت.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                پۆل_نرخ=정확한값(کلایەنت,1)[0]
                if پۆل_نرخ==4:
                    دەقی_تێکستەکە=정확한값(کلایەنت,7); تەختەکلیل_تێنووسین.누름값(دەقی_تێکستەکە[0]!=0,struct.unpack('>I',دەقی_تێکستەکە[3:])[0]); continue
                if پۆل_نرخ==255:
                    دەقی_تێکستەکە=정확한값(کلایەنت,11)
                    if دەقی_تێکستەکە[0]!=0: raise ValueError('unsupported QEMU input extension')
                    تەختەکلیل_تێنووسین.누름값(struct.unpack('>H',دەقی_تێکستەکە[1:3])[0]!=0,struct.unpack('>I',دەقی_تێکستەکە[3:7])[0]); continue
                if پۆل_نرخ==5:
                    دەقی_تێکستەکە=정확한값(کلایەنت,5); 단추들,پۆوتانی_x,세로좌표=struct.unpack('>BHH',دەقی_تێکستەکە)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: تەختەکلیل_تێنووسین.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=پۆوتانی_x<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.ناردن(bytes([ord('1')+색인]))
                    else: 자신.ناردن(bytes([30,1,단추들,پۆوتانی_x&255,پۆوتانی_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if پۆل_نرخ==6:
                    دەقی_تێکستەکە=정확한값(کلایەنت,7); درێژی_نرخ=struct.unpack('>i',دەقی_تێکستەکە[3:])[0]
                    if abs(درێژی_نرخ)>65536: raise ValueError('clipboard too large')
                    دەق=정확한값(کلایەنت,abs(درێژی_نرخ))
                    if درێژی_نرخ>=0:
                        try: تەختەکلیل_تێنووسین.ڕوونووسگە_نرخ=دەق.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: تەختەکلیل_تێنووسین.ڕوونووسگە_نرخ=دەق.decode('latin-1').encode('utf-8')
                        تەختەکلیل_تێنووسین.ڕوونووسگە_نرخ=تەختەکلیل_تێنووسین.ڕوونووسگە_نرخ[:65536].decode('utf-8','ignore').encode('utf-8')
                    ڕاژەکار_نرخ.sendall(bytes([پۆل_نرخ])+دەقی_تێکستەکە+دەق); continue
                if پۆل_نرخ==0:
                    دەقی_تێکستەکە=정확한값(کلایەنت,19)
                    if دەقی_تێکستەکە[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=دەقی_تێکستەکە[3]//8
                elif پۆل_نرخ==2:
                    دەقی_تێکستەکە=정확한값(کلایەنت,3); 항목수=struct.unpack('>H',دەقی_تێکستەکە[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(کلایەنت,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 بەهای_گریمانە Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    دەقی_تێکستەکە=struct.pack('>BHi',0,1,0)
                elif پۆل_نرخ in (3,150): دەقی_تێکستەکە=정확한값(کلایەنت,9)
                elif پۆل_نرخ==248:
                    دەقی_تێکستەکە=정확한값(کلایەنت,8)
                    if دەقی_تێکستەکە[7]>64: raise ValueError('fence too large')
                    دەقی_تێکستەکە+=정확한값(کلایەنت,دەقی_تێکستەکە[7])
                elif پۆل_نرخ==250: دەقی_تێکستەکە=정확한값(کلایەنت,3)
                elif پۆل_نرخ==251:
                    دەقی_تێکستەکە=정확한값(کلایەنت,7)
                    if دەقی_تێکستەکە[5]>16: raise ValueError('too many screens')
                    دەقی_تێکستەکە+=정확한값(کلایەنت,دەقی_تێکستەکە[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(پۆل_نرخ))
                ڕاژەکار_نرخ.sendall(bytes([پۆل_نرخ])+دەقی_تێکستەکە)
        except (OSError,EOFError,ValueError) as هەڵە:
            if str(هەڵە): print('VNC client:',هەڵە,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (کلایەنت,ڕاژەکار_نرخ):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ڕادان_دێسکتۆپ(접속번호=5902, تۆڕ=False, 파일전송접속번호=2121, 전달규칙들=(), وردبینی_نرخ=(640, 480), 게스트주소=None, جێدەر_ناونیشان='127.0.0.1'):
    with ExitStack() as سەرچاوە_50487cae, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if تۆڕ:
            from 통신다리 import 통신다리
            통신다리항목 = سەرچاوە_50487cae.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, جێدەر_ناونیشان=جێدەر_ناونیشان))
        گوزەر=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and جێدەر==원격화면접속번호 for 통신규약,جێدەر,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            پرۆسە=subprocess.Popen(فەرمان(وردبینی_نرخ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(گوزەر)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=لكاندن_دێسکتۆپ(پرۆسە); خوێنەر=threading.Thread(target=연결다리.직렬입출력,daemon=True); خوێنەر.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(جێدەر_ناونیشان,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while پرۆسە.poll() is None:
                    try: کلایەنت,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): کلایەنت.close(); continue
                    if not گوزەر.exists(): کلایەنت.close(); continue
                    처리작업=threading.Thread(target=연결다리.کلایەنت,args=(کلایەنت,گوزەر),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.ڕاگرتن_پێشهات.set()
                if پرۆسە.poll() is None:
                    پرۆسە.terminate()
                    try: پرۆسە.wait(timeout=5)
                    except subprocess.TimeoutExpired: پرۆسە.kill(); پرۆسە.wait()
                خوێنەر.join(timeout=2); پرۆسە.stdin.close(); پرۆسە.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.هەڵە: raise RuntimeError('network bridge: '+통신다리항목.هەڵە)
            return 0 if 가로채기됨 else پرۆسە.returncode


if __name__=='__main__':
    from جێبەجێکردن_فەرمان import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ئارگیومێنت_ڕیزی_داتا=인수해석기.parse_args()
    if ئارگیومێنت_ڕیزی_داتا.forward and not ئارگیومێنت_ڕیزی_داتا.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ڕادان_دێسکتۆپ(ئارگیومێنت_ڕیزی_داتا.port,تۆڕ=ئارگیومێنت_ڕیزی_داتا.network,파일전송접속번호=ئارگیومێنت_ڕیزی_داتا.ftp_port,전달규칙들=ئارگیومێنت_ڕیزی_داتا.forward,وردبینی_نرخ=ئارگیومێنت_ڕیزی_داتا.resolution))
