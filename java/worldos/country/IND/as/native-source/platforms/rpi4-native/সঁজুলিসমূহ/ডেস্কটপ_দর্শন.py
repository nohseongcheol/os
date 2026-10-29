#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, কী_মান 입력은 자체 কাৰ্ণেল_মান UART로 전달한다. localhost 전용, 단일 নিয়ন্ত্রণ_মান 클라이언트.
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
from নিষ্পাদন_আদেশ import কমান্ড
from local_input import create


def 정확한값(소켓, মাপ):
    ডাটা = bytearray()
    while len(ডাটা) < মাপ:
        조각 = 소켓.recv(মাপ - len(ডাটা))
        if not 조각: raise EOFError()
        ডাটা.extend(조각)
    return bytes(ডাটা)


class কীবোর্ড:
    def __init__(자신, ই_মেইল_কৰক, 입력방식알림=None):
        자신.바이트전송 = ই_মেইল_কৰক; 자신.সংশোধক_কী = set(); 자신.ক্লিপ_বোৰ্ড_মান = b''
        자신.한글조합기 = create(ই_মেইল_কৰক, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.সাল_সলনি_কী = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ই_মেইল_কৰক(자신, ডাটা):
        자신.한글조합기.조합확정()
        자신.바이트전송(ডাটা)

    def সাল_সলনি_মোড(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, কী_প্ৰতীক):
        if কী_প্ৰতীক in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.সংশোধক_কী.add(কী_প্ৰতীক)
            else: 자신.সংশোধক_কী.discard(কী_প্ৰতীক)
            return
        if not 누르는중:
            자신.সাল_সলনি_কী.discard(কী_প্ৰতীক)
            return
        CTRL_কী = bool(자신.সংশোধক_কী & {0xffe3, 0xffe4})
        SHIFT_কী = bool(자신.সংশোধক_কী & {0xffe1, 0xffe2})
        if CTRL_কী and SHIFT_কী and কী_প্ৰতীক in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if কী_প্ৰতীক in (32,0xff0d):
                try:
                    মান=int(자신.유니코드입력,16)
                    if 32<=মান<=0x10ffff and not 0xd800<=মান<=0xdfff: 자신.ই_মেইল_কৰক(chr(মান).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif কী_প্ৰতীক==0xff1b: 자신.유니코드입력=None
            elif কী_প্ৰতীক==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif কী_প্ৰতীক<128 and chr(কী_প্ৰতীক) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(কী_প্ৰতীক)
            return
        if কী_প্ৰতীক in (0xff31,0xffc6) or কী_প্ৰতীক==32 and SHIFT_কী and not CTRL_কী:
            if কী_প্ৰতীক not in 자신.সাল_সলনি_কী: 자신.সাল_সলনি_মোড()
            자신.সাল_সলনি_কী.add(কী_প্ৰতীক)
            return
        if কী_প্ৰতীক==0xff08 and 자신.한글여부 and not CTRL_কী and 자신.한글조합기.앞글자지우기(): return
        if CTRL_কী and SHIFT_কী and কী_প্ৰতীক in (ord('t'),ord('T')):
            자신.ই_মেইল_কৰক(bytes([30,2,1,0,0,0,0])); return
        if কী_প্ৰতীক==0xffc3: 자신.ই_মেইল_কৰক(bytes([30,2,2,0,0,0,0])); return
        if কী_প্ৰতীক==0xffc9: 자신.ই_মেইল_কৰক(bytes([30,2,3,0,0,0,0])); return
        if CTRL_কী and SHIFT_কী and কী_প্ৰতীক in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ই_মেইল_কৰক(자신.ক্লিপ_বোৰ্ড_মান); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if কী_প্ৰতীক in 특수글쇠: 자신.ই_মেইল_কৰক(특수글쇠[কী_প্ৰতীক]); return
        বৰ্ণ_এনকোডিং = কী_প্ৰতীক & 0xffffff if কী_প্ৰতীক & 0xff000000 == 0x01000000 else কী_প্ৰতীক
        if বৰ্ণ_এনকোডিং > 0x10ffff or 0xd800 <= বৰ্ণ_এনকোডিং <= 0xdfff or কী_প্ৰতীক >= 0xff00 and কী_প্ৰতীক < 0x1000000: return
        if CTRL_কী and 0x40 <= বৰ্ণ_এনকোডিং <= 0x7f: 자신.ই_মেইল_কৰক(bytes([বৰ্ণ_এনকোডিং & 31])); return
        if বৰ্ণ_এনকোডিং < 32: return
        if 자신.한글여부 and 자신.সংশোধক_কী & {0xffea,0xfe03,0xff7e} and not CTRL_কী and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ফীড_কী(chr(বৰ্ণ_এনকোডিং), altgr=True): return
        앞부분 = b'\x1b' if 자신.সংশোধক_কী & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_কী and not 앞부분 and 32<=বৰ্ণ_এনকোডিং<127:
            বৰ্ণ_ডাটা=chr(বৰ্ণ_এনকোডিং).upper() if SHIFT_কী else chr(বৰ্ণ_এনকোডিং)
            if 자신.한글조합기.ফীড_কী(বৰ্ণ_ডাটা): return
        자신.ই_মেইল_কৰক(앞부분 + chr(বৰ্ণ_এনকোডিং).encode('utf-8'))


class সংযোগ_ডেস্কটপ:
    def __init__(자신, প্ৰসেস):
        자신.প্ৰসেস=প্ৰসেস; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.টাৰ্মিনেল=False; 자신.시작화면=False; 자신.닫힘=False

    def ই_মেইল_কৰক(자신, ডাটা):
        if not ডাটা or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.প্ৰসেস.stdin.write(ডাটা); 자신.প্ৰসেস.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ডাটা=자신.প্ৰসেস.stdout.read(4096)
                if not ডাটা: break
                sys.stdout.buffer.write(ডাটা); sys.stdout.buffer.flush()
                끝부분=(끝부분+ডাটা)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.টাৰ্মিনেল=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ই_মেইল_কৰক(b'terminal\n')
        finally: 자신.닫힘=True

    def ক্লায়েণ্ট(자신, ক্লায়েণ্ট, পথ):
        ছাৰ্ভাৰ_মান=socket.socket(socket.AF_UNIX); ছাৰ্ভাৰ_মান.settimeout(10); ক্লায়েণ্ট.settimeout(10)
        কীবোর্ড_প্রবিষ্ট=কীবোর্ড(자신.ই_মেইল_কৰক,lambda 한글여부:자신.ই_মেইল_কৰক(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ছাৰ্ভাৰ_মান.connect(str(পথ))
            # 초기 협상은 순서대로 끝낸다. 이후 নিৰ্গম 가닥만 클라이언트에 쓴다.
            ক্লায়েণ্ট.sendall(정확한값(ছাৰ্ভাৰ_মান,12))
            판번호=정확한값(ক্লায়েণ্ট,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ছাৰ্ভাৰ_মান.sendall(판번호)
            개수=정확한값(ছাৰ্ভাৰ_মান,1);ক্লায়েণ্ট.sendall(개수+정확한값(ছাৰ্ভাৰ_মান,개수[0]))
            নিৰাপত্তা=정확한값(ক্লায়েণ্ট,1)
            if নিৰাপত্তা!=b'\x01': raise ValueError('unexpected security type')
            ছাৰ্ভাৰ_মান.sendall(নিৰাপত্তা)
            if 판번호==b'RFB 003.008\n':ক্লায়েণ্ট.sendall(정확한값(ছাৰ্ভাৰ_মান,4))
            ছাৰ্ভাৰ_মান.sendall(정확한값(ক্লায়েণ্ট,1))
            초기값=정확한값(ছাৰ্ভাৰ_মান,24)
            ক্লায়েণ্ট.sendall(초기값+정확한값(ছাৰ্ভাৰ_মান,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ক্লায়েণ্ট.settimeout(None);ছাৰ্ভাৰ_মান.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        বর্গ_মান=정확한값(ছাৰ্ভাৰ_মান,1)[0]
                        if বর্গ_মান==0:
                            머리=정확한값(ছাৰ্ভাৰ_মান,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 দূৰবৰ্তী_মান 포인터의 중복을 피한다.
                            লুকাই_থকা_মান=포인터지원
                            if লুকাই_থকা_মান:ক্লায়েণ্ট.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ক্লায়েণ্ট.sendall(bytes([বর্গ_মান])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ছাৰ্ভাৰ_মান,12);가로,উলম্ব_স্থান_সলনি_কৰক,폭,높이,এনকোডিং_মান=struct.unpack('>HHHHi',사각형)
                                if এনকোডিং_মান!=0:raise ValueError('unexpected framebuffer encoding: '+str(এনকোডিং_মান))
                                ক্লায়েণ্ট.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ডাটা=정확한값(ছাৰ্ভাৰ_মান,min(남음,65536));ক্লায়েণ্ট.sendall(ডাটা);남음-=len(ডাটা)
                        elif বর্গ_মান==1:
                            머리=정확한값(ছাৰ্ভাৰ_মান,5);개수=struct.unpack('>H',머리[3:])[0]
                            ক্লায়েণ্ট.sendall(bytes([বর্গ_মান])+머리+정확한값(ছাৰ্ভাৰ_মান,개수*6))
                        elif বর্গ_মান==2:ক্লায়েণ্ট.sendall(bytes([বর্গ_মান]))
                        elif বর্গ_মান==3:
                            머리=정확한값(ছাৰ্ভাৰ_মান,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ক্লায়েণ্ট.sendall(bytes([বর্গ_মান])+머리+정확한값(ছাৰ্ভাৰ_মান,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(বর্গ_মান))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ক্লায়েণ্ট.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                বর্গ_মান=정확한값(ক্লায়েণ্ট,1)[0]
                if বর্গ_মান==4:
                    মূল_পাঠ=정확한값(ক্লায়েণ্ট,7); কীবোর্ড_প্রবিষ্ট.누름값(মূল_পাঠ[0]!=0,struct.unpack('>I',মূল_পাঠ[3:])[0]); continue
                if বর্গ_মান==255:
                    মূল_পাঠ=정확한값(ক্লায়েণ্ট,11)
                    if মূল_পাঠ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    কীবোর্ড_প্রবিষ্ট.누름값(struct.unpack('>H',মূল_পাঠ[1:3])[0]!=0,struct.unpack('>I',মূল_পাঠ[3:7])[0]); continue
                if বর্গ_মান==5:
                    মূল_পাঠ=정확한값(ক্লায়েণ্ট,5); 단추들,x_ক_ৰ্ডিনেট,세로좌표=struct.unpack('>BHH',মূল_পাঠ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: কীবোর্ড_প্রবিষ্ট.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_ক_ৰ্ডিনেট<576 and 112<=세로좌표<372:
                        লুকআপ_ইনডেক্স=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and লুকআপ_ইনডেক্স<5: 자신.ই_মেইল_কৰক(bytes([ord('1')+লুকআপ_ইনডেক্স]))
                    else: 자신.ই_মেইল_কৰক(bytes([30,1,단추들,x_ক_ৰ্ডিনেট&255,x_ক_ৰ্ডিনেট>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if বর্গ_মান==6:
                    মূল_পাঠ=정확한값(ক্লায়েণ্ট,7); দৈর্ঘ্য_মান=struct.unpack('>i',মূল_পাঠ[3:])[0]
                    if abs(দৈর্ঘ্য_মান)>65536: raise ValueError('clipboard too large')
                    টেক্সট=정확한값(ক্লায়েণ্ট,abs(দৈর্ঘ্য_মান))
                    if দৈর্ঘ্য_মান>=0:
                        try: কীবোর্ড_প্রবিষ্ট.ক্লিপ_বোৰ্ড_মান=টেক্সট.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: কীবোর্ড_প্রবিষ্ট.ক্লিপ_বোৰ্ড_মান=টেক্সট.decode('latin-1').encode('utf-8')
                        কীবোর্ড_প্রবিষ্ট.ক্লিপ_বোৰ্ড_মান=কীবোর্ড_প্রবিষ্ট.ক্লিপ_বোৰ্ড_মান[:65536].decode('utf-8','ignore').encode('utf-8')
                    ছাৰ্ভাৰ_মান.sendall(bytes([বর্গ_মান])+মূল_পাঠ+টেক্সট); continue
                if বর্গ_মান==0:
                    মূল_পাঠ=정확한값(ক্লায়েণ্ট,19)
                    if মূল_পাঠ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=মূল_পাঠ[3]//8
                elif বর্গ_মান==2:
                    মূল_পাঠ=정확한값(ক্লায়েণ্ট,3); 항목수=struct.unpack('>H',মূল_পাঠ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ক্লায়েণ্ট,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ডিফ_ল্ট_মান Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    মূল_পাঠ=struct.pack('>BHi',0,1,0)
                elif বর্গ_মান in (3,150): মূল_পাঠ=정확한값(ক্লায়েণ্ট,9)
                elif বর্গ_মান==248:
                    মূল_পাঠ=정확한값(ক্লায়েণ্ট,8)
                    if মূল_পাঠ[7]>64: raise ValueError('fence too large')
                    মূল_পাঠ+=정확한값(ক্লায়েণ্ট,মূল_পাঠ[7])
                elif বর্গ_মান==250: মূল_পাঠ=정확한값(ক্লায়েণ্ট,3)
                elif বর্গ_মান==251:
                    মূল_পাঠ=정확한값(ক্লায়েণ্ট,7)
                    if মূল_পাঠ[5]>16: raise ValueError('too many screens')
                    মূল_পাঠ+=정확한값(ক্লায়েণ্ট,মূল_পাঠ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(বর্গ_মান))
                ছাৰ্ভাৰ_মান.sendall(bytes([বর্গ_মান])+মূল_পাঠ)
        except (OSError,EOFError,ValueError) as ত্ৰুটি:
            if str(ত্ৰুটি): print('VNC client:',ত্ৰুটি,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ক্লায়েণ্ট,ছাৰ্ভাৰ_মান):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def চলন_ডেস্কটপ(접속번호=5902, নেটৱৰ্ক=False, 파일전송접속번호=2121, 전달규칙들=(), প্রতিচ্ছায়া_মান=(640, 480), অতিথি_ঠিকনা=None, হ_ষ্ট_ঠিকনা='127.0.0.1'):
    with ExitStack() as সম্পদসমূহ, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট = None
        if নেটৱৰ্ক:
            from নেটৱৰ্ক_ব্ৰীজ import নেটৱৰ্ক_ব্ৰীজ
            নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট = সম্পদসমূহ.enter_context(নেটৱৰ্ক_ব্ৰীজ(파일전송접속번호, 전달규칙들, অতিথি_ঠিকনা=অতিথি_ঠিকনা, হ_ষ্ট_ঠিকনা=হ_ষ্ট_ঠিকনা))
        পথ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and হ_ষ্ট==원격화면접속번호 for 통신규약,হ_ষ্ট,_ in নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            প্ৰসেস=subprocess.Popen(কমান্ড(প্রতিচ্ছায়া_মান)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(পথ)]+(নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট.전달인수() if নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ব্ৰীজ=সংযোগ_ডেস্কটপ(প্ৰসেস); পাঠক=threading.Thread(target=ব্ৰীজ.직렬입출력,daemon=True); পাঠক.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(হ_ষ্ট_ঠিকনা,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while প্ৰসেস.poll() is None:
                    try: ক্লায়েণ্ট,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ক্লায়েণ্ট.close(); continue
                    if not পথ.exists(): ক্লায়েণ্ট.close(); continue
                    처리작업=threading.Thread(target=ব্ৰীজ.ক্লায়েণ্ট,args=(ক্লায়েণ্ট,পথ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ব্ৰীজ.닫힘=True
                if নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট: নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট.বিৰাম_কৰক_ইভেণ্ট.set()
                if প্ৰসেস.poll() is None:
                    প্ৰসেস.terminate()
                    try: প্ৰসেস.wait(timeout=5)
                    except subprocess.TimeoutExpired: প্ৰসেস.kill(); প্ৰসেস.wait()
                পাঠক.join(timeout=2); প্ৰসেস.stdin.close(); প্ৰসেস.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট and নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট.ত্ৰুটি: raise RuntimeError('network bridge: '+নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট.ত্ৰুটি)
            return 0 if 가로채기됨 else প্ৰসেস.returncode


if __name__=='__main__':
    from নিষ্পাদন_আদেশ import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    যুক্তি_শৃঙ্খলা=인수해석기.parse_args()
    if যুক্তি_শৃঙ্খলা.forward and not যুক্তি_শৃঙ্খলা.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(চলন_ডেস্কটপ(যুক্তি_শৃঙ্খলা.port,নেটৱৰ্ক=যুক্তি_শৃঙ্খলা.network,파일전송접속번호=যুক্তি_শৃঙ্খলা.ftp_port,전달규칙들=যুক্তি_শৃঙ্খলা.forward,প্রতিচ্ছায়া_মান=যুক্তি_শৃঙ্খলা.resolution))
