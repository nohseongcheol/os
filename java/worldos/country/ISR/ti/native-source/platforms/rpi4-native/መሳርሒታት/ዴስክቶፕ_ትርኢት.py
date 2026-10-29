#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, መፍትሕ_ዋጋ 입력은 자체 ፍረ_ዋጋ UART로 전달한다. localhost 전용, 단일 ቁጽጽር_ዋጋ 클라이언트.
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
from ተግብር_ትእዛዝ import ትእዛዝ
from local_input import create


def 정확한값(소켓, መጠን):
    ሓበሬታ = bytearray()
    while len(ሓበሬታ) < መጠን:
        조각 = 소켓.recv(መጠን - len(ሓበሬታ))
        if not 조각: raise EOFError()
        ሓበሬታ.extend(조각)
    return bytes(ሓበሬታ)


class ናይ_መፍትሕ_ሰሌዳ:
    def __init__(자신, ለኣኽ, 입력방식알림=None):
        자신.바이트전송 = ለኣኽ; 자신.ቀያሪ_መፍትሕ = set(); 자신.ናይ_ቅንጣብ_ሰሌዳ_ዋጋ = b''
        자신.한글조합기 = create(ለኣኽ, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ቀይር_መፍትሕ = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ለኣኽ(자신, ሓበሬታ):
        자신.한글조합기.조합확정()
        자신.바이트전송(ሓበሬታ)

    def ቀይር_ኹነት(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, መፍትሕ_ምልክት):
        if መፍትሕ_ምልክት in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ቀያሪ_መፍትሕ.add(መፍትሕ_ምልክት)
            else: 자신.ቀያሪ_መፍትሕ.discard(መፍትሕ_ምልክት)
            return
        if not 누르는중:
            자신.ቀይር_መፍትሕ.discard(መፍትሕ_ምልክት)
            return
        ቁጽጽር_መፍትሕ = bool(자신.ቀያሪ_መፍትሕ & {0xffe3, 0xffe4})
        SHIFT_መፍትሕ = bool(자신.ቀያሪ_መፍትሕ & {0xffe1, 0xffe2})
        if ቁጽጽር_መፍትሕ and SHIFT_መፍትሕ and መፍትሕ_ምልክት in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if መፍትሕ_ምልክት in (32,0xff0d):
                try:
                    ዋጋ=int(자신.유니코드입력,16)
                    if 32<=ዋጋ<=0x10ffff and not 0xd800<=ዋጋ<=0xdfff: 자신.ለኣኽ(chr(ዋጋ).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif መፍትሕ_ምልክት==0xff1b: 자신.유니코드입력=None
            elif መፍትሕ_ምልክት==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif መፍትሕ_ምልክት<128 and chr(መፍትሕ_ምልክት) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(መፍትሕ_ምልክት)
            return
        if መፍትሕ_ምልክት in (0xff31,0xffc6) or መፍትሕ_ምልክት==32 and SHIFT_መፍትሕ and not ቁጽጽር_መፍትሕ:
            if መፍትሕ_ምልክት not in 자신.ቀይር_መፍትሕ: 자신.ቀይር_ኹነት()
            자신.ቀይር_መፍትሕ.add(መፍትሕ_ምልክት)
            return
        if መፍትሕ_ምልክት==0xff08 and 자신.한글여부 and not ቁጽጽር_መፍትሕ and 자신.한글조합기.앞글자지우기(): return
        if ቁጽጽር_መፍትሕ and SHIFT_መፍትሕ and መፍትሕ_ምልክት in (ord('t'),ord('T')):
            자신.ለኣኽ(bytes([30,2,1,0,0,0,0])); return
        if መፍትሕ_ምልክት==0xffc3: 자신.ለኣኽ(bytes([30,2,2,0,0,0,0])); return
        if መፍትሕ_ምልክት==0xffc9: 자신.ለኣኽ(bytes([30,2,3,0,0,0,0])); return
        if ቁጽጽር_መፍትሕ and SHIFT_መፍትሕ and መፍትሕ_ምልክት in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ለኣኽ(자신.ናይ_ቅንጣብ_ሰሌዳ_ዋጋ); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if መፍትሕ_ምልክት in 특수글쇠: 자신.ለኣኽ(특수글쇠[መፍትሕ_ምልክት]); return
        ፊደል_ምምስጣር = መፍትሕ_ምልክት & 0xffffff if መፍትሕ_ምልክት & 0xff000000 == 0x01000000 else መፍትሕ_ምልክት
        if ፊደል_ምምስጣር > 0x10ffff or 0xd800 <= ፊደል_ምምስጣር <= 0xdfff or መፍትሕ_ምልክት >= 0xff00 and መፍትሕ_ምልክት < 0x1000000: return
        if ቁጽጽር_መፍትሕ and 0x40 <= ፊደል_ምምስጣር <= 0x7f: 자신.ለኣኽ(bytes([ፊደል_ምምስጣር & 31])); return
        if ፊደል_ምምስጣር < 32: return
        if 자신.한글여부 and 자신.ቀያሪ_መፍትሕ & {0xffea,0xfe03,0xff7e} and not ቁጽጽር_መፍትሕ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ቀለብ_መፍትሕ(chr(ፊደል_ምምስጣር), altgr=True): return
        앞부분 = b'\x1b' if 자신.ቀያሪ_መፍትሕ & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not ቁጽጽር_መፍትሕ and not 앞부분 and 32<=ፊደል_ምምስጣር<127:
            ፊደል_ሓበሬታ=chr(ፊደል_ምምስጣር).upper() if SHIFT_መፍትሕ else chr(ፊደል_ምምስጣር)
            if 자신.한글조합기.ቀለብ_መፍትሕ(ፊደል_ሓበሬታ): return
        자신.ለኣኽ(앞부분 + chr(ፊደል_ምምስጣር).encode('utf-8'))


class ኣላግብ_ዴስክቶፕ:
    def __init__(자신, መስርሕ):
        자신.መስርሕ=መስርሕ; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def ለኣኽ(자신, ሓበሬታ):
        if not ሓበሬታ or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.መስርሕ.stdin.write(ሓበሬታ); 자신.መስርሕ.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ሓበሬታ=자신.መስርሕ.stdout.read(4096)
                if not ሓበሬታ: break
                sys.stdout.buffer.write(ሓበሬታ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ሓበሬታ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ለኣኽ(b'terminal\n')
        finally: 자신.닫힘=True

    def ዓሚል(자신, ዓሚል, መገዲ):
        ኣገልጋሊ_ዋጋ=socket.socket(socket.AF_UNIX); ኣገልጋሊ_ዋጋ.settimeout(10); ዓሚል.settimeout(10)
        ናይ_መፍትሕ_ሰሌዳ_ምእታው=ናይ_መፍትሕ_ሰሌዳ(자신.ለኣኽ,lambda 한글여부:자신.ለኣኽ(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ኣገልጋሊ_ዋጋ.connect(str(መገዲ))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            ዓሚል.sendall(정확한값(ኣገልጋሊ_ዋጋ,12))
            판번호=정확한값(ዓሚል,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ኣገልጋሊ_ዋጋ.sendall(판번호)
            개수=정확한값(ኣገልጋሊ_ዋጋ,1);ዓሚል.sendall(개수+정확한값(ኣገልጋሊ_ዋጋ,개수[0]))
            ሓለዋ=정확한값(ዓሚል,1)
            if ሓለዋ!=b'\x01': raise ValueError('unexpected security type')
            ኣገልጋሊ_ዋጋ.sendall(ሓለዋ)
            if 판번호==b'RFB 003.008\n':ዓሚል.sendall(정확한값(ኣገልጋሊ_ዋጋ,4))
            ኣገልጋሊ_ዋጋ.sendall(정확한값(ዓሚል,1))
            초기값=정확한값(ኣገልጋሊ_ዋጋ,24)
            ዓሚል.sendall(초기값+정확한값(ኣገልጋሊ_ዋጋ,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ዓሚል.settimeout(None);ኣገልጋሊ_ዋጋ.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        መደብ_ዋጋ=정확한값(ኣገልጋሊ_ዋጋ,1)[0]
                        if መደብ_ዋጋ==0:
                            머리=정확한값(ኣገልጋሊ_ዋጋ,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 ርሑቕ_ዋጋ 포인터의 중복을 피한다.
                            ሕቡእ_ዋጋ=포인터지원
                            if ሕቡእ_ዋጋ:ዓሚል.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ዓሚል.sendall(bytes([መደብ_ዋጋ])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(ኣገልጋሊ_ዋጋ,12);가로,세로,폭,높이,ምምስጣር_ዋጋ=struct.unpack('>HHHHi',사각형)
                                if ምምስጣር_ዋጋ!=0:raise ValueError('unexpected framebuffer encoding: '+str(ምምስጣር_ዋጋ))
                                ዓሚል.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ሓበሬታ=정확한값(ኣገልጋሊ_ዋጋ,min(남음,65536));ዓሚል.sendall(ሓበሬታ);남음-=len(ሓበሬታ)
                        elif መደብ_ዋጋ==1:
                            머리=정확한값(ኣገልጋሊ_ዋጋ,5);개수=struct.unpack('>H',머리[3:])[0]
                            ዓሚል.sendall(bytes([መደብ_ዋጋ])+머리+정확한값(ኣገልጋሊ_ዋጋ,개수*6))
                        elif መደብ_ዋጋ==2:ዓሚል.sendall(bytes([መደብ_ዋጋ]))
                        elif መደብ_ዋጋ==3:
                            머리=정확한값(ኣገልጋሊ_ዋጋ,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ዓሚል.sendall(bytes([መደብ_ዋጋ])+머리+정확한값(ኣገልጋሊ_ዋጋ,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(መደብ_ዋጋ))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ዓሚል.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                መደብ_ዋጋ=정확한값(ዓሚል,1)[0]
                if መደብ_ዋጋ==4:
                    ዋና_ጽሑፍ=정확한값(ዓሚል,7); ናይ_መፍትሕ_ሰሌዳ_ምእታው.누름값(ዋና_ጽሑፍ[0]!=0,struct.unpack('>I',ዋና_ጽሑፍ[3:])[0]); continue
                if መደብ_ዋጋ==255:
                    ዋና_ጽሑፍ=정확한값(ዓሚል,11)
                    if ዋና_ጽሑፍ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ናይ_መፍትሕ_ሰሌዳ_ምእታው.누름값(struct.unpack('>H',ዋና_ጽሑፍ[1:3])[0]!=0,struct.unpack('>I',ዋና_ጽሑፍ[3:7])[0]); continue
                if መደብ_ዋጋ==5:
                    ዋና_ጽሑፍ=정확한값(ዓሚል,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',ዋና_ጽሑፍ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ናይ_መፍትሕ_ሰሌዳ_ምእታው.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.ለኣኽ(bytes([ord('1')+색인]))
                    else: 자신.ለኣኽ(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if መደብ_ዋጋ==6:
                    ዋና_ጽሑፍ=정확한값(ዓሚል,7); ንውሓት_ዋጋ=struct.unpack('>i',ዋና_ጽሑፍ[3:])[0]
                    if abs(ንውሓት_ዋጋ)>65536: raise ValueError('clipboard too large')
                    ጽሑፍ=정확한값(ዓሚል,abs(ንውሓት_ዋጋ))
                    if ንውሓት_ዋጋ>=0:
                        try: ናይ_መፍትሕ_ሰሌዳ_ምእታው.ናይ_ቅንጣብ_ሰሌዳ_ዋጋ=ጽሑፍ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ናይ_መፍትሕ_ሰሌዳ_ምእታው.ናይ_ቅንጣብ_ሰሌዳ_ዋጋ=ጽሑፍ.decode('latin-1').encode('utf-8')
                        ናይ_መፍትሕ_ሰሌዳ_ምእታው.ናይ_ቅንጣብ_ሰሌዳ_ዋጋ=ናይ_መፍትሕ_ሰሌዳ_ምእታው.ናይ_ቅንጣብ_ሰሌዳ_ዋጋ[:65536].decode('utf-8','ignore').encode('utf-8')
                    ኣገልጋሊ_ዋጋ.sendall(bytes([መደብ_ዋጋ])+ዋና_ጽሑፍ+ጽሑፍ); continue
                if መደብ_ዋጋ==0:
                    ዋና_ጽሑፍ=정확한값(ዓሚል,19)
                    if ዋና_ጽሑፍ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=ዋና_ጽሑፍ[3]//8
                elif መደብ_ዋጋ==2:
                    ዋና_ጽሑፍ=정확한값(ዓሚል,3); 항목수=struct.unpack('>H',ዋና_ጽሑፍ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ዓሚል,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ንቡር_ዋጋ Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ዋና_ጽሑፍ=struct.pack('>BHi',0,1,0)
                elif መደብ_ዋጋ in (3,150): ዋና_ጽሑፍ=정확한값(ዓሚል,9)
                elif መደብ_ዋጋ==248:
                    ዋና_ጽሑፍ=정확한값(ዓሚል,8)
                    if ዋና_ጽሑፍ[7]>64: raise ValueError('fence too large')
                    ዋና_ጽሑፍ+=정확한값(ዓሚል,ዋና_ጽሑፍ[7])
                elif መደብ_ዋጋ==250: ዋና_ጽሑፍ=정확한값(ዓሚል,3)
                elif መደብ_ዋጋ==251:
                    ዋና_ጽሑፍ=정확한값(ዓሚል,7)
                    if ዋና_ጽሑፍ[5]>16: raise ValueError('too many screens')
                    ዋና_ጽሑፍ+=정확한값(ዓሚል,ዋና_ጽሑፍ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(መደብ_ዋጋ))
                ኣገልጋሊ_ዋጋ.sendall(bytes([መደብ_ዋጋ])+ዋና_ጽሑፍ)
        except (OSError,EOFError,ValueError) as ጌጋ:
            if str(ጌጋ): print('VNC client:',ጌጋ,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ዓሚል,ኣገልጋሊ_ዋጋ):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ኣኺድ_ዴስክቶፕ(접속번호=5902, ማሕበራዊ_ኔትወርክ=False, 파일전송접속번호=2121, 전달규칙들=(), ንጹርነት_ዋጋ=(640, 480), 게스트주소=None, አዐንግድ_ኣድራሻ='127.0.0.1'):
    with ExitStack() as ጸጋታት, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if ማሕበራዊ_ኔትወርክ:
            from 통신다리 import 통신다리
            통신다리항목 = ጸጋታት.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, አዐንግድ_ኣድራሻ=አዐንግድ_ኣድራሻ))
        መገዲ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and አዐንግድ==원격화면접속번호 for 통신규약,አዐንግድ,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            መስርሕ=subprocess.Popen(ትእዛዝ(ንጹርነት_ዋጋ)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(መገዲ)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=ኣላግብ_ዴስክቶፕ(መስርሕ); ኣንባቢ=threading.Thread(target=연결다리.직렬입출력,daemon=True); ኣንባቢ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(አዐንግድ_ኣድራሻ,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while መስርሕ.poll() is None:
                    try: ዓሚል,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ዓሚል.close(); continue
                    if not መገዲ.exists(): ዓሚል.close(); continue
                    처리작업=threading.Thread(target=연결다리.ዓሚል,args=(ዓሚል,መገዲ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.ንግዚኡ_ደው_ኣብል_ፍጻመ.set()
                if መስርሕ.poll() is None:
                    መስርሕ.terminate()
                    try: መስርሕ.wait(timeout=5)
                    except subprocess.TimeoutExpired: መስርሕ.kill(); መስርሕ.wait()
                ኣንባቢ.join(timeout=2); መስርሕ.stdin.close(); መስርሕ.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.ጌጋ: raise RuntimeError('network bridge: '+통신다리항목.ጌጋ)
            return 0 if 가로채기됨 else መስርሕ.returncode


if __name__=='__main__':
    from ተግብር_ትእዛዝ import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ሓባሪ_ቁጽሪ_ተርታ=인수해석기.parse_args()
    if ሓባሪ_ቁጽሪ_ተርታ.forward and not ሓባሪ_ቁጽሪ_ተርታ.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ኣኺድ_ዴስክቶፕ(ሓባሪ_ቁጽሪ_ተርታ.port,ማሕበራዊ_ኔትወርክ=ሓባሪ_ቁጽሪ_ተርታ.network,파일전송접속번호=ሓባሪ_ቁጽሪ_ተርታ.ftp_port,전달규칙들=ሓባሪ_ቁጽሪ_ተርታ.forward,ንጹርነት_ዋጋ=ሓባሪ_ቁጽሪ_ተርታ.resolution))
