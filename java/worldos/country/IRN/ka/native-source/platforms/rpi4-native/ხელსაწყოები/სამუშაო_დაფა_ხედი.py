#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, კლავიში_მნიშვნელობა 입력은 자체 ბირთვი_მნიშვნელობა UART로 전달한다. localhost 전용, 단일 მართვა_მნიშვნელობა 클라이언트.
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
from შესრულება_ბრძანება import ბრძანება
from local_input import create


def 정확한값(소켓, ზომა):
    მონაცემები = bytearray()
    while len(მონაცემები) < ზომა:
        조각 = 소켓.recv(ზომა - len(მონაცემები))
        if not 조각: raise EOFError()
        მონაცემები.extend(조각)
    return bytes(მონაცემები)


class კლავიატურა:
    def __init__(자신, გაგზავნა, 입력방식알림=None):
        자신.바이트전송 = გაგზავნა; 자신.მართვის_კლავიში = set(); 자신.გაცვლის_ბუფერი_მნიშვნელობა = b''
        자신.한글조합기 = create(გაგზავნა, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.გადართვა_კლავიში = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def გაგზავნა(자신, მონაცემები):
        자신.한글조합기.조합확정()
        자신.바이트전송(მონაცემები)

    def გადართვა_რეჟიმი(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, კლავიში_სიმბოლო):
        if კლავიში_სიმბოლო in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.მართვის_კლავიში.add(კლავიში_სიმბოლო)
            else: 자신.მართვის_კლავიში.discard(კლავიში_სიმბოლო)
            return
        if not 누르는중:
            자신.გადართვა_კლავიში.discard(კლავიში_სიმბოლო)
            return
        CTRL_კლავიში = bool(자신.მართვის_კლავიში & {0xffe3, 0xffe4})
        SHIFT_კლავიში = bool(자신.მართვის_კლავიში & {0xffe1, 0xffe2})
        if CTRL_კლავიში and SHIFT_კლავიში and კლავიში_სიმბოლო in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if კლავიში_სიმბოლო in (32,0xff0d):
                try:
                    მნიშვნელობა=int(자신.유니코드입력,16)
                    if 32<=მნიშვნელობა<=0x10ffff and not 0xd800<=მნიშვნელობა<=0xdfff: 자신.გაგზავნა(chr(მნიშვნელობა).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif კლავიში_სიმბოლო==0xff1b: 자신.유니코드입력=None
            elif კლავიში_სიმბოლო==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif კლავიში_სიმბოლო<128 and chr(კლავიში_სიმბოლო) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(კლავიში_სიმბოლო)
            return
        if კლავიში_სიმბოლო in (0xff31,0xffc6) or კლავიში_სიმბოლო==32 and SHIFT_კლავიში and not CTRL_კლავიში:
            if კლავიში_სიმბოლო not in 자신.გადართვა_კლავიში: 자신.გადართვა_რეჟიმი()
            자신.გადართვა_კლავიში.add(კლავიში_სიმბოლო)
            return
        if კლავიში_სიმბოლო==0xff08 and 자신.한글여부 and not CTRL_კლავიში and 자신.한글조합기.앞글자지우기(): return
        if CTRL_კლავიში and SHIFT_კლავიში and კლავიში_სიმბოლო in (ord('t'),ord('T')):
            자신.გაგზავნა(bytes([30,2,1,0,0,0,0])); return
        if კლავიში_სიმბოლო==0xffc3: 자신.გაგზავნა(bytes([30,2,2,0,0,0,0])); return
        if კლავიში_სიმბოლო==0xffc9: 자신.გაგზავნა(bytes([30,2,3,0,0,0,0])); return
        if CTRL_კლავიში and SHIFT_კლავიში and კლავიში_სიმბოლო in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.გაგზავნა(자신.გაცვლის_ბუფერი_მნიშვნელობა); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if კლავიში_სიმბოლო in 특수글쇠: 자신.გაგზავნა(특수글쇠[კლავიში_სიმბოლო]); return
        სიმბოლო_კოდირება = კლავიში_სიმბოლო & 0xffffff if კლავიში_სიმბოლო & 0xff000000 == 0x01000000 else კლავიში_სიმბოლო
        if სიმბოლო_კოდირება > 0x10ffff or 0xd800 <= სიმბოლო_კოდირება <= 0xdfff or კლავიში_სიმბოლო >= 0xff00 and კლავიში_სიმბოლო < 0x1000000: return
        if CTRL_კლავიში and 0x40 <= სიმბოლო_კოდირება <= 0x7f: 자신.გაგზავნა(bytes([სიმბოლო_კოდირება & 31])); return
        if სიმბოლო_კოდირება < 32: return
        if 자신.한글여부 and 자신.მართვის_კლავიში & {0xffea,0xfe03,0xff7e} and not CTRL_კლავიში and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.არხი_კლავიში(chr(სიმბოლო_კოდირება), altgr=True): return
        앞부분 = b'\x1b' if 자신.მართვის_კლავიში & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_კლავიში and not 앞부분 and 32<=სიმბოლო_კოდირება<127:
            სიმბოლო_მონაცემები_4d9f8719=chr(სიმბოლო_კოდირება).upper() if SHIFT_კლავიში else chr(სიმბოლო_კოდირება)
            if 자신.한글조합기.არხი_კლავიში(სიმბოლო_მონაცემები_4d9f8719): return
        자신.გაგზავნა(앞부분 + chr(სიმბოლო_კოდირება).encode('utf-8'))


class დაკავშირება_სამუშაო_დაფა:
    def __init__(자신, პროცესი):
        자신.პროცესი=პროცესი; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.ტერმინალი=False; 자신.시작화면=False; 자신.닫힘=False

    def გაგზავნა(자신, მონაცემები):
        if not მონაცემები or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.პროცესი.stdin.write(მონაცემები); 자신.პროცესი.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                მონაცემები=자신.პროცესი.stdout.read(4096)
                if not მონაცემები: break
                sys.stdout.buffer.write(მონაცემები); sys.stdout.buffer.flush()
                끝부분=(끝부분+მონაცემები)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ტერმინალი=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.გაგზავნა(b'terminal\n')
        finally: 자신.닫힘=True

    def კლიენტი(자신, კლიენტი, გეზი):
        სერვერი_მნიშვნელობა=socket.socket(socket.AF_UNIX); სერვერი_მნიშვნელობა.settimeout(10); კლიენტი.settimeout(10)
        კლავიატურა_შენატანი=კლავიატურა(자신.გაგზავნა,lambda 한글여부:자신.გაგზავნა(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            სერვერი_მნიშვნელობა.connect(str(გეზი))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            კლიენტი.sendall(정확한값(სერვერი_მნიშვნელობა,12))
            판번호=정확한값(კლიენტი,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            სერვერი_მნიშვნელობა.sendall(판번호)
            개수=정확한값(სერვერი_მნიშვნელობა,1);კლიენტი.sendall(개수+정확한값(სერვერი_მნიშვნელობა,개수[0]))
            უსაფრთხოება=정확한값(კლიენტი,1)
            if უსაფრთხოება!=b'\x01': raise ValueError('unexpected security type')
            სერვერი_მნიშვნელობა.sendall(უსაფრთხოება)
            if 판번호==b'RFB 003.008\n':კლიენტი.sendall(정확한값(სერვერი_მნიშვნელობა,4))
            სერვერი_მნიშვნელობა.sendall(정확한값(კლიენტი,1))
            초기값=정확한값(სერვერი_მნიშვნელობა,24)
            კლიენტი.sendall(초기값+정확한값(სერვერი_მნიშვნელობა,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            კლიენტი.settimeout(None);სერვერი_მნიშვნელობა.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        კატეგორია_მნიშვნელობა=정확한값(სერვერი_მნიშვნელობა,1)[0]
                        if კატეგორია_მნიშვნელობა==0:
                            머리=정확한값(სერვერი_მნიშვნელობა,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 დისტანციური_მნიშვნელობა 포인터의 중복을 피한다.
                            დამალვა_მნიშვნელობა=포인터지원
                            if დამალვა_მნიშვნელობა:კლიენტი.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            კლიენტი.sendall(bytes([კატეგორია_მნიშვნელობა])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(სერვერი_მნიშვნელობა,12);가로,ვერტიკალური_პოზიცია,폭,높이,კოდირება_მნიშვნელობა=struct.unpack('>HHHHi',사각형)
                                if კოდირება_მნიშვნელობა!=0:raise ValueError('unexpected framebuffer encoding: '+str(კოდირება_მნიშვნელობა))
                                კლიენტი.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    მონაცემები=정확한값(სერვერი_მნიშვნელობა,min(남음,65536));კლიენტი.sendall(მონაცემები);남음-=len(მონაცემები)
                        elif კატეგორია_მნიშვნელობა==1:
                            머리=정확한값(სერვერი_მნიშვნელობა,5);개수=struct.unpack('>H',머리[3:])[0]
                            კლიენტი.sendall(bytes([კატეგორია_მნიშვნელობა])+머리+정확한값(სერვერი_მნიშვნელობა,개수*6))
                        elif კატეგორია_მნიშვნელობა==2:კლიენტი.sendall(bytes([კატეგორია_მნიშვნელობა]))
                        elif კატეგორია_მნიშვნელობა==3:
                            머리=정확한값(სერვერი_მნიშვნელობა,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            კლიენტი.sendall(bytes([კატეგორია_მნიშვნელობა])+머리+정확한값(სერვერი_მნიშვნელობა,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(კატეგორია_მნიშვნელობა))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:კლიენტი.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                კატეგორია_მნიშვნელობა=정확한값(კლიენტი,1)[0]
                if კატეგორია_მნიშვნელობა==4:
                    ძირითადი_ტექსტი=정확한값(კლიენტი,7); კლავიატურა_შენატანი.누름값(ძირითადი_ტექსტი[0]!=0,struct.unpack('>I',ძირითადი_ტექსტი[3:])[0]); continue
                if კატეგორია_მნიშვნელობა==255:
                    ძირითადი_ტექსტი=정확한값(კლიენტი,11)
                    if ძირითადი_ტექსტი[0]!=0: raise ValueError('unsupported QEMU input extension')
                    კლავიატურა_შენატანი.누름값(struct.unpack('>H',ძირითადი_ტექსტი[1:3])[0]!=0,struct.unpack('>I',ძირითადი_ტექსტი[3:7])[0]); continue
                if კატეგორია_მნიშვნელობა==5:
                    ძირითადი_ტექსტი=정확한값(კლიენტი,5); 단추들,x_კოორდინატა,Y_ღილაკი_კოორდინატი=struct.unpack('>BHH',ძირითადი_ტექსტი)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: კლავიატურა_შენატანი.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_კოორდინატა<576 and 112<=Y_ღილაკი_კოორდინატი<372:
                        ძებნა_ინდექსი=(Y_ღილაკი_კოორდინატი-112)//52
                        if (Y_ღილაკი_კოორდინატი-112)%52<40 and ძებნა_ინდექსი<5: 자신.გაგზავნა(bytes([ord('1')+ძებნა_ინდექსი]))
                    else: 자신.გაგზავნა(bytes([30,1,단추들,x_კოორდინატა&255,x_კოორდინატა>>8,Y_ღილაკი_კოორდინატი&255,Y_ღილაკი_კოორდინატი>>8]))
                    continue
                if კატეგორია_მნიშვნელობა==6:
                    ძირითადი_ტექსტი=정확한값(კლიენტი,7); სიგრძე_მნიშვნელობა=struct.unpack('>i',ძირითადი_ტექსტი[3:])[0]
                    if abs(სიგრძე_მნიშვნელობა)>65536: raise ValueError('clipboard too large')
                    ტექსტი=정확한값(კლიენტი,abs(სიგრძე_მნიშვნელობა))
                    if სიგრძე_მნიშვნელობა>=0:
                        try: კლავიატურა_შენატანი.გაცვლის_ბუფერი_მნიშვნელობა=ტექსტი.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: კლავიატურა_შენატანი.გაცვლის_ბუფერი_მნიშვნელობა=ტექსტი.decode('latin-1').encode('utf-8')
                        კლავიატურა_შენატანი.გაცვლის_ბუფერი_მნიშვნელობა=კლავიატურა_შენატანი.გაცვლის_ბუფერი_მნიშვნელობა[:65536].decode('utf-8','ignore').encode('utf-8')
                    სერვერი_მნიშვნელობა.sendall(bytes([კატეგორია_მნიშვნელობა])+ძირითადი_ტექსტი+ტექსტი); continue
                if კატეგორია_მნიშვნელობა==0:
                    ძირითადი_ტექსტი=정확한값(კლიენტი,19)
                    if ძირითადი_ტექსტი[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=ძირითადი_ტექსტი[3]//8
                elif კატეგორია_მნიშვნელობა==2:
                    ძირითადი_ტექსტი=정확한값(კლიენტი,3); 항목수=struct.unpack('>H',ძირითადი_ტექსტი[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(კლიენტი,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ნაგულისხმევი_მნიშვნელობა Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ძირითადი_ტექსტი=struct.pack('>BHi',0,1,0)
                elif კატეგორია_მნიშვნელობა in (3,150): ძირითადი_ტექსტი=정확한값(კლიენტი,9)
                elif კატეგორია_მნიშვნელობა==248:
                    ძირითადი_ტექსტი=정확한값(კლიენტი,8)
                    if ძირითადი_ტექსტი[7]>64: raise ValueError('fence too large')
                    ძირითადი_ტექსტი+=정확한값(კლიენტი,ძირითადი_ტექსტი[7])
                elif კატეგორია_მნიშვნელობა==250: ძირითადი_ტექსტი=정확한값(კლიენტი,3)
                elif კატეგორია_მნიშვნელობა==251:
                    ძირითადი_ტექსტი=정확한값(კლიენტი,7)
                    if ძირითადი_ტექსტი[5]>16: raise ValueError('too many screens')
                    ძირითადი_ტექსტი+=정확한값(კლიენტი,ძირითადი_ტექსტი[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(კატეგორია_მნიშვნელობა))
                სერვერი_მნიშვნელობა.sendall(bytes([კატეგორია_მნიშვნელობა])+ძირითადი_ტექსტი)
        except (OSError,EOFError,ValueError) as შეცდომა:
            if str(შეცდომა): print('VNC client:',შეცდომა,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (კლიენტი,სერვერი_მნიშვნელობა):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def სერია_სამუშაო_დაფა(접속번호=5902, ქსელი=False, 파일전송접속번호=2121, 전달규칙들=(), გარჩევადობა_მნიშვნელობა=(640, 480), სტუმარი_მისამართი=None, მასპინძელი_მისამართი='127.0.0.1'):
    with ExitStack() as რესურსები, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        ქსელი_ხიდი_შენატანი = None
        if ქსელი:
            from ქსელი_ხიდი import ქსელი_ხიდი
            ქსელი_ხიდი_შენატანი = რესურსები.enter_context(ქსელი_ხიდი(파일전송접속번호, 전달규칙들, სტუმარი_მისამართი=სტუმარი_მისამართი, მასპინძელი_მისამართი=მასპინძელი_მისამართი))
        გეზი=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if ქსელი_ხიდი_შენატანი and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and მასპინძელი==원격화면접속번호 for 통신규약,მასპინძელი,_ in ქსელი_ხიდი_შენატანი.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            პროცესი=subprocess.Popen(ბრძანება(გარჩევადობა_მნიშვნელობა)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(გეზი)]+(ქსელი_ხიდი_შენატანი.전달인수() if ქსელი_ხიდი_შენატანი else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ხიდი=დაკავშირება_სამუშაო_დაფა(პროცესი); წამკითხველი=threading.Thread(target=ხიდი.직렬입출력,daemon=True); წამკითხველი.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if ქსელი_ხიდი_შენატანი: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(მასპინძელი_მისამართი,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while პროცესი.poll() is None:
                    try: კლიენტი,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): კლიენტი.close(); continue
                    if not გეზი.exists(): კლიენტი.close(); continue
                    처리작업=threading.Thread(target=ხიდი.კლიენტი,args=(კლიენტი,გეზი),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ხიდი.닫힘=True
                if ქსელი_ხიდი_შენატანი: ქსელი_ხიდი_შენატანი.პაუზა_მოვლენა.set()
                if პროცესი.poll() is None:
                    პროცესი.terminate()
                    try: პროცესი.wait(timeout=5)
                    except subprocess.TimeoutExpired: პროცესი.kill(); პროცესი.wait()
                წამკითხველი.join(timeout=2); პროცესი.stdin.close(); პროცესი.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if ქსელი_ხიდი_შენატანი and ქსელი_ხიდი_შენატანი.შეცდომა: raise RuntimeError('network bridge: '+ქსელი_ხიდი_შენატანი.შეცდომა)
            return 0 if 가로채기됨 else პროცესი.returncode


if __name__=='__main__':
    from შესრულება_ბრძანება import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    არგუმენტი_მასივი=인수해석기.parse_args()
    if არგუმენტი_მასივი.forward and not არგუმენტი_მასივი.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(სერია_სამუშაო_დაფა(არგუმენტი_მასივი.port,ქსელი=არგუმენტი_მასივი.network,파일전송접속번호=არგუმენტი_მასივი.ftp_port,전달규칙들=არგუმენტი_მასივი.forward,გარჩევადობა_მნიშვნელობა=არგუმენტი_მასივი.resolution))
