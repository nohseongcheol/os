#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, কী_মান 입력은 নিজ কারনেল_মান UART로 전달한다. localhost 전용, 단일 নিয়ন্ত্রণ_মান 클라이언트.
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
from কার্যকর_করুন_আদেশ import আদেশ
from local_input import create


def 정확한값(소켓, আকার):
    ডাটা = bytearray()
    while len(ডাটা) < আকার:
        조각 = 소켓.recv(আকার - len(ডাটা))
        if not 조각: raise EOFError()
        ডাটা.extend(조각)
    return bytes(ডাটা)


class কীবোর্ড:
    def __init__(자신, পাঠান, 입력방식알림=None):
        자신.바이트전송 = পাঠান; 자신.সংশোধক_কী = set(); 자신.ক্লিপবোর্ড_মান = b''
        자신.한글조합기 = create(পাঠান, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.সুইচ_কী = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def পাঠান(자신, ডাটা):
        자신.한글조합기.조합확정()
        자신.바이트전송(ডাটা)

    def সুইচ_মোড(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, কী_প্রতীক):
        if কী_প্রতীক in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.সংশোধক_কী.add(কী_প্রতীক)
            else: 자신.সংশোধক_কী.discard(কী_প্রতীক)
            return
        if not 누르는중:
            자신.সুইচ_কী.discard(কী_প্রতীক)
            return
        CTRL_কী = bool(자신.সংশোধক_কী & {0xffe3, 0xffe4})
        SHIFT_কী = bool(자신.সংশোধক_কী & {0xffe1, 0xffe2})
        if CTRL_কী and SHIFT_কী and কী_প্রতীক in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if কী_প্রতীক in (32,0xff0d):
                try:
                    মান=int(자신.유니코드입력,16)
                    if 32<=মান<=0x10ffff and not 0xd800<=মান<=0xdfff: 자신.পাঠান(chr(মান).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif কী_প্রতীক==0xff1b: 자신.유니코드입력=None
            elif কী_প্রতীক==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif কী_প্রতীক<128 and chr(কী_প্রতীক) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(কী_প্রতীক)
            return
        if কী_প্রতীক in (0xff31,0xffc6) or কী_প্রতীক==32 and SHIFT_কী and not CTRL_কী:
            if কী_প্রতীক not in 자신.সুইচ_কী: 자신.সুইচ_মোড()
            자신.সুইচ_কী.add(কী_প্রতীক)
            return
        if কী_প্রতীক==0xff08 and 자신.한글여부 and not CTRL_কী and 자신.한글조합기.앞글자지우기(): return
        if CTRL_কী and SHIFT_কী and কী_প্রতীক in (ord('t'),ord('T')):
            자신.পাঠান(bytes([30,2,1,0,0,0,0])); return
        if কী_প্রতীক==0xffc3: 자신.পাঠান(bytes([30,2,2,0,0,0,0])); return
        if কী_প্রতীক==0xffc9: 자신.পাঠান(bytes([30,2,3,0,0,0,0])); return
        if CTRL_কী and SHIFT_কী and কী_প্রতীক in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.পাঠান(자신.ক্লিপবোর্ড_মান); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if কী_প্রতীক in 특수글쇠: 자신.পাঠান(특수글쇠[কী_প্রতীক]); return
        অক্ষর_এনকোড_করা = কী_প্রতীক & 0xffffff if কী_প্রতীক & 0xff000000 == 0x01000000 else কী_প্রতীক
        if অক্ষর_এনকোড_করা > 0x10ffff or 0xd800 <= অক্ষর_এনকোড_করা <= 0xdfff or কী_প্রতীক >= 0xff00 and কী_প্রতীক < 0x1000000: return
        if CTRL_কী and 0x40 <= অক্ষর_এনকোড_করা <= 0x7f: 자신.পাঠান(bytes([অক্ষর_এনকোড_করা & 31])); return
        if অক্ষর_এনকোড_করা < 32: return
        if 자신.한글여부 and 자신.সংশোধক_কী & {0xffea,0xfe03,0xff7e} and not CTRL_কী and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ফিড_কী(chr(অক্ষর_এনকোড_করা), altgr=True): return
        앞부분 = b'\x1b' if 자신.সংশোধক_কী & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_কী and not 앞부분 and 32<=অক্ষর_এনকোড_করা<127:
            অক্ষর_ডাটা=chr(অক্ষর_এনকোড_করা).upper() if SHIFT_কী else chr(অক্ষর_এনকোড_করা)
            if 자신.한글조합기.ফিড_কী(অক্ষর_ডাটা): return
        자신.পাঠান(앞부분 + chr(অক্ষর_এনকোড_করা).encode('utf-8'))


class সংযোগ_ডেস্কটপ:
    def __init__(자신, প্রসেস):
        자신.প্রসেস=প্রসেস; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.আদেশ_ব্যাখ্যাকারী=False; 자신.시작화면=False; 자신.닫힘=False

    def পাঠান(자신, ডাটা):
        if not ডাটা or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.প্রসেস.stdin.write(ডাটা); 자신.প্রসেস.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ডাটা=자신.প্রসেস.stdout.read(4096)
                if not ডাটা: break
                sys.stdout.buffer.write(ডাটা); sys.stdout.buffer.flush()
                끝부분=(끝부분+ডাটা)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.আদেশ_ব্যাখ্যাকারী=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.পাঠান(b'terminal\n')
        finally: 자신.닫힘=True

    def গ্রাহক(자신, গ্রাহক, পথ_2):
        সার্ভার_মান=socket.socket(socket.AF_UNIX); সার্ভার_মান.settimeout(10); গ্রাহক.settimeout(10)
        কীবোর্ড_ভুক্তি=কীবোর্ড(자신.পাঠান,lambda 한글여부:자신.পাঠান(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            সার্ভার_মান.connect(str(পথ_2))
            # 초기 협상은 순서대로 끝낸다. 이후 নির্গম 가닥만 클라이언트에 쓴다.
            গ্রাহক.sendall(정확한값(সার্ভার_মান,12))
            판번호=정확한값(গ্রাহক,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            সার্ভার_মান.sendall(판번호)
            개수=정확한값(সার্ভার_মান,1);গ্রাহক.sendall(개수+정확한값(সার্ভার_মান,개수[0]))
            নিরাপত্তা=정확한값(গ্রাহক,1)
            if নিরাপত্তা!=b'\x01': raise ValueError('unexpected security type')
            সার্ভার_মান.sendall(নিরাপত্তা)
            if 판번호==b'RFB 003.008\n':গ্রাহক.sendall(정확한값(সার্ভার_মান,4))
            সার্ভার_মান.sendall(정확한값(গ্রাহক,1))
            초기값=정확한값(সার্ভার_মান,24)
            গ্রাহক.sendall(초기값+정확한값(সার্ভার_মান,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            গ্রাহক.settimeout(None);সার্ভার_মান.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        বিভাগ_মান=정확한값(সার্ভার_মান,1)[0]
                        if বিভাগ_মান==0:
                            머리=정확한값(সার্ভার_মান,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 দূরবর্তী_মান 포인터의 중복을 피한다.
                            লুকায়িত_মান=포인터지원
                            if লুকায়িত_মান:গ্রাহক.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            গ্রাহক.sendall(bytes([বিভাগ_মান])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(সার্ভার_মান,12);가로,উল্লম্ব_পদ,폭,높이,এনকোড_করা_মান=struct.unpack('>HHHHi',사각형)
                                if এনকোড_করা_মান!=0:raise ValueError('unexpected framebuffer encoding: '+str(এনকোড_করা_মান))
                                গ্রাহক.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ডাটা=정확한값(সার্ভার_মান,min(남음,65536));গ্রাহক.sendall(ডাটা);남음-=len(ডাটা)
                        elif বিভাগ_মান==1:
                            머리=정확한값(সার্ভার_মান,5);개수=struct.unpack('>H',머리[3:])[0]
                            গ্রাহক.sendall(bytes([বিভাগ_মান])+머리+정확한값(সার্ভার_মান,개수*6))
                        elif বিভাগ_মান==2:গ্রাহক.sendall(bytes([বিভাগ_মান]))
                        elif বিভাগ_মান==3:
                            머리=정확한값(সার্ভার_মান,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            গ্রাহক.sendall(bytes([বিভাগ_মান])+머리+정확한값(সার্ভার_মান,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(বিভাগ_মান))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:গ্রাহক.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                বিভাগ_মান=정확한값(গ্রাহক,1)[0]
                if বিভাগ_মান==4:
                    মুখ্য_পাঠ=정확한값(গ্রাহক,7); কীবোর্ড_ভুক্তি.누름값(মুখ্য_পাঠ[0]!=0,struct.unpack('>I',মুখ্য_পাঠ[3:])[0]); continue
                if বিভাগ_মান==255:
                    মুখ্য_পাঠ=정확한값(গ্রাহক,11)
                    if মুখ্য_পাঠ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    কীবোর্ড_ভুক্তি.누름값(struct.unpack('>H',মুখ্য_পাঠ[1:3])[0]!=0,struct.unpack('>I',মুখ্য_পাঠ[3:7])[0]); continue
                if বিভাগ_মান==5:
                    মুখ্য_পাঠ=정확한값(গ্রাহক,5); 단추들,X_বোতাম_অক্ষবিন্দু,Y_বোতাম_অক্ষবিন্দু=struct.unpack('>BHH',মুখ্য_পাঠ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: কীবোর্ড_ভুক্তি.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=X_বোতাম_অক্ষবিন্দু<576 and 112<=Y_বোতাম_অক্ষবিন্দু<372:
                        লুকআপ_সূচি=(Y_বোতাম_অক্ষবিন্দু-112)//52
                        if (Y_বোতাম_অক্ষবিন্দু-112)%52<40 and লুকআপ_সূচি<5: 자신.পাঠান(bytes([ord('1')+লুকআপ_সূচি]))
                    else: 자신.পাঠান(bytes([30,1,단추들,X_বোতাম_অক্ষবিন্দু&255,X_বোতাম_অক্ষবিন্দু>>8,Y_বোতাম_অক্ষবিন্দু&255,Y_বোতাম_অক্ষবিন্দু>>8]))
                    continue
                if বিভাগ_মান==6:
                    মুখ্য_পাঠ=정확한값(গ্রাহক,7); দৈর্ঘ্য_মান=struct.unpack('>i',মুখ্য_পাঠ[3:])[0]
                    if abs(দৈর্ঘ্য_মান)>65536: raise ValueError('clipboard too large')
                    পাঠ=정확한값(গ্রাহক,abs(দৈর্ঘ্য_মান))
                    if দৈর্ঘ্য_মান>=0:
                        try: কীবোর্ড_ভুক্তি.ক্লিপবোর্ড_মান=পাঠ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: কীবোর্ড_ভুক্তি.ক্লিপবোর্ড_মান=পাঠ.decode('latin-1').encode('utf-8')
                        কীবোর্ড_ভুক্তি.ক্লিপবোর্ড_মান=কীবোর্ড_ভুক্তি.ক্লিপবোর্ড_মান[:65536].decode('utf-8','ignore').encode('utf-8')
                    সার্ভার_মান.sendall(bytes([বিভাগ_মান])+মুখ্য_পাঠ+পাঠ); continue
                if বিভাগ_মান==0:
                    মুখ্য_পাঠ=정확한값(গ্রাহক,19)
                    if মুখ্য_পাঠ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=মুখ্য_পাঠ[3]//8
                elif বিভাগ_মান==2:
                    মুখ্য_পাঠ=정확한값(গ্রাহক,3); 항목수=struct.unpack('>H',মুখ্য_পাঠ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(গ্রাহক,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 অমনোনীত_মান Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    মুখ্য_পাঠ=struct.pack('>BHi',0,1,0)
                elif বিভাগ_মান in (3,150): মুখ্য_পাঠ=정확한값(গ্রাহক,9)
                elif বিভাগ_মান==248:
                    মুখ্য_পাঠ=정확한값(গ্রাহক,8)
                    if মুখ্য_পাঠ[7]>64: raise ValueError('fence too large')
                    মুখ্য_পাঠ+=정확한값(গ্রাহক,মুখ্য_পাঠ[7])
                elif বিভাগ_মান==250: মুখ্য_পাঠ=정확한값(গ্রাহক,3)
                elif বিভাগ_মান==251:
                    মুখ্য_পাঠ=정확한값(গ্রাহক,7)
                    if মুখ্য_পাঠ[5]>16: raise ValueError('too many screens')
                    মুখ্য_পাঠ+=정확한값(গ্রাহক,মুখ্য_পাঠ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(বিভাগ_মান))
                সার্ভার_মান.sendall(bytes([বিভাগ_মান])+মুখ্য_পাঠ)
        except (OSError,EOFError,ValueError) as ত্রুটি:
            if str(ত্রুটি): print('VNC client:',ত্রুটি,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (গ্রাহক,সার্ভার_মান):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def রান_ডেস্কটপ(পোর্ট_নম্বর=5902, নেটওয়ার্ক_9b2e3222=False, ফাইল_স্থানান্তর_পোর্ট_নম্বর=2121, 전달규칙들=(), রেজোলিউশন_মান=(640, 480), অতিথি_ইমেইল=None, হোস্ট_ইমেইল='127.0.0.1'):
    with ExitStack() as সম্পদগুলি, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        নেটওয়ার্ক_ব্রিজ_ভুক্তি = None
        if নেটওয়ার্ক_9b2e3222:
            from নেটওয়ার্ক_ব্রিজ import নেটওয়ার্ক_ব্রিজ
            নেটওয়ার্ক_ব্রিজ_ভুক্তি = সম্পদগুলি.enter_context(নেটওয়ার্ক_ব্রিজ(ফাইল_স্থানান্তর_পোর্ট_নম্বর, 전달규칙들, অতিথি_ইমেইল=অতিথি_ইমেইল, হোস্ট_ইমেইল=হোস্ট_ইমেইল))
        পথ_2=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',পোর্ট_নম্বর)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if নেটওয়ার্ক_ব্রিজ_ভুক্তি and (원격화면접속번호==ফাইল_স্থানান্তর_পোর্ট_নম্বর or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and হোস্ট==원격화면접속번호 for 통신규약,হোস্ট,_ in নেটওয়ার্ক_ব্রিজ_ভুক্তি.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            প্রসেস=subprocess.Popen(আদেশ(রেজোলিউশন_মান)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(পথ_2)]+(নেটওয়ার্ক_ব্রিজ_ভুক্তি.전달인수() if নেটওয়ার্ক_ব্রিজ_ভুক্তি else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ব্রিজ=সংযোগ_ডেস্কটপ(প্রসেস); পাঠক=threading.Thread(target=ব্রিজ.직렬입출력,daemon=True); পাঠক.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if নেটওয়ার্ক_ব্রিজ_ভুক্তি: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(হোস্ট_ইমেইল,ফাইল_স্থানান্তর_পোর্ট_নম্বর),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while প্রসেস.poll() is None:
                    try: গ্রাহক,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): গ্রাহক.close(); continue
                    if not পথ_2.exists(): গ্রাহক.close(); continue
                    처리작업=threading.Thread(target=ব্রিজ.গ্রাহক,args=(গ্রাহক,পথ_2),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ব্রিজ.닫힘=True
                if নেটওয়ার্ক_ব্রিজ_ভুক্তি: নেটওয়ার্ক_ব্রিজ_ভুক্তি.বিরতি_ঘটনা.set()
                if প্রসেস.poll() is None:
                    প্রসেস.terminate()
                    try: প্রসেস.wait(timeout=5)
                    except subprocess.TimeoutExpired: প্রসেস.kill(); প্রসেস.wait()
                পাঠক.join(timeout=2); প্রসেস.stdin.close(); প্রসেস.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if নেটওয়ার্ক_ব্রিজ_ভুক্তি and নেটওয়ার্ক_ব্রিজ_ভুক্তি.ত্রুটি: raise RuntimeError('network bridge: '+নেটওয়ার্ক_ব্রিজ_ভুক্তি.ত্রুটি)
            return 0 if 가로채기됨 else প্রসেস.returncode


if __name__=='__main__':
    from কার্যকর_করুন_আদেশ import 해상도읽기
    পার্সার=argparse.ArgumentParser(description=__doc__); পার্সার.add_argument('--port',type=int,default=5902)
    পার্সার.add_argument('--resolution',type=해상도읽기,default=(640,480))
    পার্সার.add_argument('--network',action='store_true'); পার্সার.add_argument('--ftp-port',type=int,default=2121)
    পার্সার.add_argument('--forward',action='append',default=[])
    যুক্তি_অ্যারে=পার্সার.parse_args()
    if যুক্তি_অ্যারে.forward and not যুক্তি_অ্যারে.network: পার্সার.error('--forward requires --network')
    raise SystemExit(রান_ডেস্কটপ(যুক্তি_অ্যারে.port,নেটওয়ার্ক_9b2e3222=যুক্তি_অ্যারে.network,ফাইল_স্থানান্তর_পোর্ট_নম্বর=যুক্তি_অ্যারে.ftp_port,전달규칙들=যুক্তি_অ্যারে.forward,রেজোলিউশন_মান=যুক্তি_অ্যারে.resolution))
