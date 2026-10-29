#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ստեղն_արժեք 입력은 자체 միջուկ_արժեք UART로 전달한다. localhost 전용, 단일 հսկում_արժեք 클라이언트.
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
from կատարել_հրաման import Հրահանգ
from local_input import create


def 정확한값(소켓, Չափս):
    տվյալ = bytearray()
    while len(տվյալ) < Չափս:
        조각 = 소켓.recv(Չափս - len(տվյալ))
        if not 조각: raise EOFError()
        տվյալ.extend(조각)
    return bytes(տվյալ)


class ստեղնաշար:
    def __init__(자신, ուղարկել, 입력방식알림=None):
        자신.바이트전송 = ուղարկել; 자신.կերպափոխիչ_ստեղն = set(); 자신.սեղմատախտակ_արժեք = b''
        자신.한글조합기 = create(ուղարկել, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.փոխարկել_ստեղն = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ուղարկել(자신, տվյալ):
        자신.한글조합기.조합확정()
        자신.바이트전송(տվյալ)

    def փոխարկել_կերպ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ստեղն_նշան):
        if ստեղն_նշան in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.կերպափոխիչ_ստեղն.add(ստեղն_նշան)
            else: 자신.կերպափոխիչ_ստեղն.discard(ստեղն_նշան)
            return
        if not 누르는중:
            자신.փոխարկել_ստեղն.discard(ստեղն_նշան)
            return
        CTRL_ստեղն = bool(자신.կերպափոխիչ_ստեղն & {0xffe3, 0xffe4})
        SHIFT_ստեղն = bool(자신.կերպափոխիչ_ստեղն & {0xffe1, 0xffe2})
        if CTRL_ստեղն and SHIFT_ստեղն and ստեղն_նշան in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ստեղն_նշան in (32,0xff0d):
                try:
                    արժեք=int(자신.유니코드입력,16)
                    if 32<=արժեք<=0x10ffff and not 0xd800<=արժեք<=0xdfff: 자신.ուղարկել(chr(արժեք).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ստեղն_նշան==0xff1b: 자신.유니코드입력=None
            elif ստեղն_նշան==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ստեղն_նշան<128 and chr(ստեղն_նշան) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ստեղն_նշան)
            return
        if ստեղն_նշան in (0xff31,0xffc6) or ստեղն_նշան==32 and SHIFT_ստեղն and not CTRL_ստեղն:
            if ստեղն_նշան not in 자신.փոխարկել_ստեղն: 자신.փոխարկել_կերպ()
            자신.փոխարկել_ստեղն.add(ստեղն_նշան)
            return
        if ստեղն_նշան==0xff08 and 자신.한글여부 and not CTRL_ստեղն and 자신.한글조합기.앞글자지우기(): return
        if CTRL_ստեղն and SHIFT_ստեղն and ստեղն_նշան in (ord('t'),ord('T')):
            자신.ուղարկել(bytes([30,2,1,0,0,0,0])); return
        if ստեղն_նշան==0xffc3: 자신.ուղարկել(bytes([30,2,2,0,0,0,0])); return
        if ստեղն_նշան==0xffc9: 자신.ուղարկել(bytes([30,2,3,0,0,0,0])); return
        if CTRL_ստեղն and SHIFT_ստեղն and ստեղն_նշան in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ուղարկել(자신.սեղմատախտակ_արժեք); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ստեղն_նշան in 특수글쇠: 자신.ուղարկել(특수글쇠[ստեղն_նշան]); return
        գրանշան_կոդավորում = ստեղն_նշան & 0xffffff if ստեղն_նշան & 0xff000000 == 0x01000000 else ստեղն_նշան
        if գրանշան_կոդավորում > 0x10ffff or 0xd800 <= գրանշան_կոդավորում <= 0xdfff or ստեղն_նշան >= 0xff00 and ստեղն_նշան < 0x1000000: return
        if CTRL_ստեղն and 0x40 <= գրանշան_կոդավորում <= 0x7f: 자신.ուղարկել(bytes([գրանշան_կոդավորում & 31])); return
        if գրանշան_կոդավորում < 32: return
        if 자신.한글여부 and 자신.կերպափոխիչ_ստեղն & {0xffea,0xfe03,0xff7e} and not CTRL_ստեղն and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.հոսք_ստեղն(chr(գրանշան_կոդավորում), altgr=True): return
        앞부분 = b'\x1b' if 자신.կերպափոխիչ_ստեղն & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_ստեղն and not 앞부분 and 32<=գրանշան_կոդավորում<127:
            գրանշան_տվյալ=chr(գրանշան_կոդավորում).upper() if SHIFT_ստեղն else chr(գրանշան_կոդավորում)
            if 자신.한글조합기.հոսք_ստեղն(գրանշան_տվյալ): return
        자신.ուղարկել(앞부분 + chr(գրանշան_կոդավորում).encode('utf-8'))


class Կապակցել_սեղան:
    def __init__(자신, Գործընթաց):
        자신.Գործընթաց=Գործընթաց; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Տերմինալ=False; 자신.시작화면=False; 자신.닫힘=False

    def ուղարկել(자신, տվյալ):
        if not տվյալ or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Գործընթաց.stdin.write(տվյալ); 자신.Գործընթաց.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                տվյալ=자신.Գործընթաց.stdout.read(4096)
                if not տվյալ: break
                sys.stdout.buffer.write(տվյալ); sys.stdout.buffer.flush()
                끝부분=(끝부분+տվյալ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Տերմինալ=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ուղարկել(b'terminal\n')
        finally: 자신.닫힘=True

    def սպասառու(자신, սպասառու, Ճանապարհ):
        սպասարկիչ_արժեք=socket.socket(socket.AF_UNIX); սպասարկիչ_արժեք.settimeout(10); սպասառու.settimeout(10)
        ստեղնաշար_մուտքագրում=ստեղնաշար(자신.ուղարկել,lambda 한글여부:자신.ուղարկել(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            սպասարկիչ_արժեք.connect(str(Ճանապարհ))
            # 초기 협상은 순서대로 끝낸다. 이후 Ելք 가닥만 클라이언트에 쓴다.
            սպասառու.sendall(정확한값(սպասարկիչ_արժեք,12))
            판번호=정확한값(սպասառու,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            սպասարկիչ_արժեք.sendall(판번호)
            개수=정확한값(սպասարկիչ_արժեք,1);սպասառու.sendall(개수+정확한값(սպասարկիչ_արժեք,개수[0]))
            Անվտանգություն=정확한값(սպասառու,1)
            if Անվտանգություն!=b'\x01': raise ValueError('unexpected security type')
            սպասարկիչ_արժեք.sendall(Անվտանգություն)
            if 판번호==b'RFB 003.008\n':սպասառու.sendall(정확한값(սպասարկիչ_արժեք,4))
            սպասարկիչ_արժեք.sendall(정확한값(սպասառու,1))
            초기값=정확한값(սպասարկիչ_արժեք,24)
            սպասառու.sendall(초기값+정확한값(սպասարկիչ_արժեք,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            սպասառու.settimeout(None);սպասարկիչ_արժեք.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        անվանակարգ_արժեք=정확한값(սպասարկիչ_արժեք,1)[0]
                        if անվանակարգ_արժեք==0:
                            머리=정확한값(սպասարկիչ_արժեք,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 հեռակա_արժեք 포인터의 중복을 피한다.
                            թաքնված_արժեք=포인터지원
                            if թաքնված_արժեք:սպասառու.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            սպասառու.sendall(bytes([անվանակարգ_արժեք])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(սպասարկիչ_արժեք,12);가로,Ուղղահայաց_դիրք,폭,높이,կոդավորում_արժեք=struct.unpack('>HHHHi',사각형)
                                if կոդավորում_արժեք!=0:raise ValueError('unexpected framebuffer encoding: '+str(կոդավորում_արժեք))
                                սպասառու.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    տվյալ=정확한값(սպասարկիչ_արժեք,min(남음,65536));սպասառու.sendall(տվյալ);남음-=len(տվյալ)
                        elif անվանակարգ_արժեք==1:
                            머리=정확한값(սպասարկիչ_արժեք,5);개수=struct.unpack('>H',머리[3:])[0]
                            սպասառու.sendall(bytes([անվանակարգ_արժեք])+머리+정확한값(սպասարկիչ_արժեք,개수*6))
                        elif անվանակարգ_արժեք==2:սպասառու.sendall(bytes([անվանակարգ_արժեք]))
                        elif անվանակարգ_արժեք==3:
                            머리=정확한값(սպասարկիչ_արժեք,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            սպասառու.sendall(bytes([անվանակարգ_արժեք])+머리+정확한값(սպասարկիչ_արժեք,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(անվանակարգ_արժեք))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:սպասառու.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                անվանակարգ_արժեք=정확한값(սպասառու,1)[0]
                if անվանակարգ_արժեք==4:
                    հիմնական_գրվածք=정확한값(սպասառու,7); ստեղնաշար_մուտքագրում.누름값(հիմնական_գրվածք[0]!=0,struct.unpack('>I',հիմնական_գրվածք[3:])[0]); continue
                if անվանակարգ_արժեք==255:
                    հիմնական_գրվածք=정확한값(սպասառու,11)
                    if հիմնական_գրվածք[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ստեղնաշար_մուտքագրում.누름값(struct.unpack('>H',հիմնական_գրվածք[1:3])[0]!=0,struct.unpack('>I',հիմնական_գրվածք[3:7])[0]); continue
                if անվանակարգ_արժեք==5:
                    հիմնական_գրվածք=정확한값(սպասառու,5); 단추들,x_կոորդինատ,세로좌표=struct.unpack('>BHH',հիմնական_գրվածք)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ստեղնաշար_մուտքագրում.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_կոորդինատ<576 and 112<=세로좌표<372:
                        Փնտրում_դասիչ=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and Փնտրում_դասիչ<5: 자신.ուղարկել(bytes([ord('1')+Փնտրում_դասիչ]))
                    else: 자신.ուղարկել(bytes([30,1,단추들,x_կոորդինատ&255,x_կոորդինատ>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if անվանակարգ_արժեք==6:
                    հիմնական_գրվածք=정확한값(սպասառու,7); տեւողություն_արժեք=struct.unpack('>i',հիմնական_գրվածք[3:])[0]
                    if abs(տեւողություն_արժեք)>65536: raise ValueError('clipboard too large')
                    Տեքստ=정확한값(սպասառու,abs(տեւողություն_արժեք))
                    if տեւողություն_արժեք>=0:
                        try: ստեղնաշար_մուտքագրում.սեղմատախտակ_արժեք=Տեքստ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ստեղնաշար_մուտքագրում.սեղմատախտակ_արժեք=Տեքստ.decode('latin-1').encode('utf-8')
                        ստեղնաշար_մուտքագրում.սեղմատախտակ_արժեք=ստեղնաշար_մուտքագրում.սեղմատախտակ_արժեք[:65536].decode('utf-8','ignore').encode('utf-8')
                    սպասարկիչ_արժեք.sendall(bytes([անվանակարգ_արժեք])+հիմնական_գրվածք+Տեքստ); continue
                if անվանակարգ_արժեք==0:
                    հիմնական_գրվածք=정확한값(սպասառու,19)
                    if հիմնական_գրվածք[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=հիմնական_գրվածք[3]//8
                elif անվանակարգ_արժեք==2:
                    հիմնական_գրվածք=정확한값(սպասառու,3); 항목수=struct.unpack('>H',հիմնական_գրվածք[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(սպասառու,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 սկզբնադիր_արժեք Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    հիմնական_գրվածք=struct.pack('>BHi',0,1,0)
                elif անվանակարգ_արժեք in (3,150): հիմնական_գրվածք=정확한값(սպասառու,9)
                elif անվանակարգ_արժեք==248:
                    հիմնական_գրվածք=정확한값(սպասառու,8)
                    if հիմնական_գրվածք[7]>64: raise ValueError('fence too large')
                    հիմնական_գրվածք+=정확한값(սպասառու,հիմնական_գրվածք[7])
                elif անվանակարգ_արժեք==250: հիմնական_գրվածք=정확한값(սպասառու,3)
                elif անվանակարգ_արժեք==251:
                    հիմնական_գրվածք=정확한값(սպասառու,7)
                    if հիմնական_գրվածք[5]>16: raise ValueError('too many screens')
                    հիմնական_գրվածք+=정확한값(սպասառու,հիմնական_գրվածք[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(անվանակարգ_արժեք))
                սպասարկիչ_արժեք.sendall(bytes([անվանակարգ_արժեք])+հիմնական_գրվածք)
        except (OSError,EOFError,ValueError) as Սխալ:
            if str(Սխալ): print('VNC client:',Սխալ,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (սպասառու,սպասարկիչ_արժեք):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def աշխատեցնել_սեղան(접속번호=5902, Ցանց=False, 파일전송접속번호=2121, 전달규칙들=(), տարլուծում_արժեք=(640, 480), հյուր_հասցե=None, հոստ_հասցե='127.0.0.1'):
    with ExitStack() as Միջոցներ, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Ցանց_կամուրջ_մուտքագրում = None
        if Ցանց:
            from Ցանց_կամուրջ import Ցանց_կամուրջ
            Ցանց_կամուրջ_մուտքագրում = Միջոցներ.enter_context(Ցանց_կամուրջ(파일전송접속번호, 전달규칙들, հյուր_հասցե=հյուր_հասցե, հոստ_հասցե=հոստ_հասցե))
        Ճանապարհ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Ցանց_կամուրջ_մուտքագրում and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and հոստ==원격화면접속번호 for 통신규약,հոստ,_ in Ցանց_կամուրջ_մուտքագրում.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Գործընթաց=subprocess.Popen(Հրահանգ(տարլուծում_արժեք)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Ճանապարհ)]+(Ցանց_կամուրջ_մուտքագրում.전달인수() if Ցանց_կամուրջ_մուտքագրում else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            կամուրջ=Կապակցել_սեղան(Գործընթաց); Ընթերցիչ=threading.Thread(target=կամուրջ.직렬입출력,daemon=True); Ընթերցիչ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Ցանց_կամուրջ_մուտքագրում: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(հոստ_հասցե,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Գործընթաց.poll() is None:
                    try: սպասառու,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): սպասառու.close(); continue
                    if not Ճանապարհ.exists(): սպասառու.close(); continue
                    처리작업=threading.Thread(target=կամուրջ.սպասառու,args=(սպասառու,Ճանապարհ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                կամուրջ.닫힘=True
                if Ցանց_կամուրջ_մուտքագրում: Ցանց_կամուրջ_մուտքագրում.դադար_միջոցառում.set()
                if Գործընթաց.poll() is None:
                    Գործընթաց.terminate()
                    try: Գործընթաց.wait(timeout=5)
                    except subprocess.TimeoutExpired: Գործընթաց.kill(); Գործընթաց.wait()
                Ընթերցիչ.join(timeout=2); Գործընթաց.stdin.close(); Գործընթաց.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Ցանց_կամուրջ_մուտքագրում and Ցանց_կամուրջ_մուտքագրում.Սխալ: raise RuntimeError('network bridge: '+Ցանց_կամուրջ_մուտքագրում.Սխալ)
            return 0 if 가로채기됨 else Գործընթաց.returncode


if __name__=='__main__':
    from կատարել_հրաման import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    արգումենտ_ԶԱՆԳՎԱԾ=인수해석기.parse_args()
    if արգումենտ_ԶԱՆԳՎԱԾ.forward and not արգումենտ_ԶԱՆԳՎԱԾ.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(աշխատեցնել_սեղան(արգումենտ_ԶԱՆԳՎԱԾ.port,Ցանց=արգումենտ_ԶԱՆԳՎԱԾ.network,파일전송접속번호=արգումենտ_ԶԱՆԳՎԱԾ.ftp_port,전달규칙들=արգումենտ_ԶԱՆԳՎԱԾ.forward,տարլուծում_արժեք=արգումենտ_ԶԱՆԳՎԱԾ.resolution))
