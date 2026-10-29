#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, કી_મૂલ્ય 입력은 자체 કર્નેલ_મૂલ્ય UART로 전달한다. localhost 전용, 단일 નિયંત્રણ_મૂલ્ય 클라이언트.
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
from અમલ_કરો_આદેશ import આદેશ
from local_input import create


def 정확한값(소켓, માપ):
    ડેટા = bytearray()
    while len(ડેટા) < માપ:
        조각 = 소켓.recv(માપ - len(ડેટા))
        if not 조각: raise EOFError()
        ડેટા.extend(조각)
    return bytes(ડેટા)


class કીબોર્ડ:
    def __init__(자신, મોકલો, 입력방식알림=None):
        자신.바이트전송 = મોકલો; 자신.સંશોધનકર્તા_કી = set(); 자신.ક્લિપબોર્ડ_મૂલ્ય = b''
        자신.한글조합기 = create(મોકલો, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.સ્વિચ_કી = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def મોકલો(자신, ડેટા):
        자신.한글조합기.조합확정()
        자신.바이트전송(ડેટા)

    def સ્વિચ_મોડ(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, કી_પ્રતીક):
        if કી_પ્રતીક in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.સંશોધનકર્તા_કી.add(કી_પ્રતીક)
            else: 자신.સંશોધનકર્તા_કી.discard(કી_પ્રતીક)
            return
        if not 누르는중:
            자신.સ્વિચ_કી.discard(કી_પ્રતીક)
            return
        CTRL_કી = bool(자신.સંશોધનકર્તા_કી & {0xffe3, 0xffe4})
        SHIFT_કી = bool(자신.સંશોધનકર્તા_કી & {0xffe1, 0xffe2})
        if CTRL_કી and SHIFT_કી and કી_પ્રતીક in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if કી_પ્રતીક in (32,0xff0d):
                try:
                    મૂલ્ય=int(자신.유니코드입력,16)
                    if 32<=મૂલ્ય<=0x10ffff and not 0xd800<=મૂલ્ય<=0xdfff: 자신.મોકલો(chr(મૂલ્ય).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif કી_પ્રતીક==0xff1b: 자신.유니코드입력=None
            elif કી_પ્રતીક==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif કી_પ્રતીક<128 and chr(કી_પ્રતીક) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(કી_પ્રતીક)
            return
        if કી_પ્રતીક in (0xff31,0xffc6) or કી_પ્રતીક==32 and SHIFT_કી and not CTRL_કી:
            if કી_પ્રતીક not in 자신.સ્વિચ_કી: 자신.સ્વિચ_મોડ()
            자신.સ્વિચ_કી.add(કી_પ્રતીક)
            return
        if કી_પ્રતીક==0xff08 and 자신.한글여부 and not CTRL_કી and 자신.한글조합기.앞글자지우기(): return
        if CTRL_કી and SHIFT_કી and કી_પ્રતીક in (ord('t'),ord('T')):
            자신.મોકલો(bytes([30,2,1,0,0,0,0])); return
        if કી_પ્રતીક==0xffc3: 자신.મોકલો(bytes([30,2,2,0,0,0,0])); return
        if કી_પ્રતીક==0xffc9: 자신.મોકલો(bytes([30,2,3,0,0,0,0])); return
        if CTRL_કી and SHIFT_કી and કી_પ્રતીક in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.મોકલો(자신.ક્લિપબોર્ડ_મૂલ્ય); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if કી_પ્રતીક in 특수글쇠: 자신.મોકલો(특수글쇠[કી_પ્રતીક]); return
        વર્ણ_એન્કોડિંગ = કી_પ્રતીક & 0xffffff if કી_પ્રતીક & 0xff000000 == 0x01000000 else કી_પ્રતીક
        if વર્ણ_એન્કોડિંગ > 0x10ffff or 0xd800 <= વર્ણ_એન્કોડિંગ <= 0xdfff or કી_પ્રતીક >= 0xff00 and કી_પ્રતીક < 0x1000000: return
        if CTRL_કી and 0x40 <= વર્ણ_એન્કોડિંગ <= 0x7f: 자신.મોકલો(bytes([વર્ણ_એન્કોડિંગ & 31])); return
        if વર્ણ_એન્કોડિંગ < 32: return
        if 자신.한글여부 and 자신.સંશોધનકર્તા_કી & {0xffea,0xfe03,0xff7e} and not CTRL_કી and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ફીડ_કી(chr(વર્ણ_એન્કોડિંગ), altgr=True): return
        앞부분 = b'\x1b' if 자신.સંશોધનકર્તા_કી & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_કી and not 앞부분 and 32<=વર્ણ_એન્કોડિંગ<127:
            વર્ણ_ડેટા=chr(વર્ણ_એન્કોડિંગ).upper() if SHIFT_કી else chr(વર્ણ_એન્કોડિંગ)
            if 자신.한글조합기.ફીડ_કી(વર્ણ_ડેટા): return
        자신.મોકલો(앞부분 + chr(વર્ણ_એન્કોડિંગ).encode('utf-8'))


class કનેક્ટ_ડેસ્કટૉપ:
    def __init__(자신, પ્રક્રિયા):
        자신.પ્રક્રિયા=પ્રક્રિયા; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.ટર્મિનલ=False; 자신.시작화면=False; 자신.닫힘=False

    def મોકલો(자신, ડેટા):
        if not ડેટા or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.પ્રક્રિયા.stdin.write(ડેટા); 자신.પ્રક્રિયા.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ડેટા=자신.પ્રક્રિયા.stdout.read(4096)
                if not ડેટા: break
                sys.stdout.buffer.write(ડેટા); sys.stdout.buffer.flush()
                끝부분=(끝부분+ડેટા)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.ટર્મિનલ=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.મોકલો(b'terminal\n')
        finally: 자신.닫힘=True

    def ક્લાયંટ(자신, ક્લાયંટ, પથ):
        સર્વર_મૂલ્ય=socket.socket(socket.AF_UNIX); સર્વર_મૂલ્ય.settimeout(10); ક્લાયંટ.settimeout(10)
        કીબોર્ડ_પ્રવેશ=કીબોર્ડ(자신.મોકલો,lambda 한글여부:자신.મોકલો(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            સર્વર_મૂલ્ય.connect(str(પથ))
            # 초기 협상은 순서대로 끝낸다. 이후 આઉટપુટ 가닥만 클라이언트에 쓴다.
            ક્લાયંટ.sendall(정확한값(સર્વર_મૂલ્ય,12))
            판번호=정확한값(ક્લાયંટ,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            સર્વર_મૂલ્ય.sendall(판번호)
            개수=정확한값(સર્વર_મૂલ્ય,1);ક્લાયંટ.sendall(개수+정확한값(સર્વર_મૂલ્ય,개수[0]))
            સુરક્ષા=정확한값(ક્લાયંટ,1)
            if સુરક્ષા!=b'\x01': raise ValueError('unexpected security type')
            સર્વર_મૂલ્ય.sendall(સુરક્ષા)
            if 판번호==b'RFB 003.008\n':ક્લાયંટ.sendall(정확한값(સર્વર_મૂલ્ય,4))
            સર્વર_મૂલ્ય.sendall(정확한값(ક્લાયંટ,1))
            초기값=정확한값(સર્વર_મૂલ્ય,24)
            ક્લાયંટ.sendall(초기값+정확한값(સર્વર_મૂલ્ય,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ક્લાયંટ.settimeout(None);સર્વર_મૂલ્ય.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        શ્રેણી_મૂલ્ય=정확한값(સર્વર_મૂલ્ય,1)[0]
                        if શ્રેણી_મૂલ્ય==0:
                            머리=정확한값(સર્વર_મૂલ્ય,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 રિમોટ_મૂલ્ય 포인터의 중복을 피한다.
                            છુપાવેલું_મૂલ્ય=포인터지원
                            if છુપાવેલું_મૂલ્ય:ક્લાયંટ.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ક્લાયંટ.sendall(bytes([શ્રેણી_મૂલ્ય])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(સર્વર_મૂલ્ય,12);가로,ઊભી_સ્થિતિ,폭,높이,એન્કોડિંગ_મૂલ્ય=struct.unpack('>HHHHi',사각형)
                                if એન્કોડિંગ_મૂલ્ય!=0:raise ValueError('unexpected framebuffer encoding: '+str(એન્કોડિંગ_મૂલ્ય))
                                ક્લાયંટ.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ડેટા=정확한값(સર્વર_મૂલ્ય,min(남음,65536));ક્લાયંટ.sendall(ડેટા);남음-=len(ડેટા)
                        elif શ્રેણી_મૂલ્ય==1:
                            머리=정확한값(સર્વર_મૂલ્ય,5);개수=struct.unpack('>H',머리[3:])[0]
                            ક્લાયંટ.sendall(bytes([શ્રેણી_મૂલ્ય])+머리+정확한값(સર્વર_મૂલ્ય,개수*6))
                        elif શ્રેણી_મૂલ્ય==2:ક્લાયંટ.sendall(bytes([શ્રેણી_મૂલ્ય]))
                        elif શ્રેણી_મૂલ્ય==3:
                            머리=정확한값(સર્વર_મૂલ્ય,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ક્લાયંટ.sendall(bytes([શ્રેણી_મૂલ્ય])+머리+정확한값(સર્વર_મૂલ્ય,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(શ્રેણી_મૂલ્ય))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ક્લાયંટ.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                શ્રેણી_મૂલ્ય=정확한값(ક્લાયંટ,1)[0]
                if શ્રેણી_મૂલ્ય==4:
                    મુખ્ય_પાઠ=정확한값(ક્લાયંટ,7); કીબોર્ડ_પ્રવેશ.누름값(મુખ્ય_પાઠ[0]!=0,struct.unpack('>I',મુખ્ય_પાઠ[3:])[0]); continue
                if શ્રેણી_મૂલ્ય==255:
                    મુખ્ય_પાઠ=정확한값(ક્લાયંટ,11)
                    if મુખ્ય_પાઠ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    કીબોર્ડ_પ્રવેશ.누름값(struct.unpack('>H',મુખ્ય_પાઠ[1:3])[0]!=0,struct.unpack('>I',મુખ્ય_પાઠ[3:7])[0]); continue
                if શ્રેણી_મૂલ્ય==5:
                    મુખ્ય_પાઠ=정확한값(ક્લાયંટ,5); 단추들,x_યામ,세로좌표=struct.unpack('>BHH',મુખ્ય_પાઠ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: કીબોર્ડ_પ્રવેશ.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_યામ<576 and 112<=세로좌표<372:
                        લુકઅપ_અનુક્રમણિકા=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and લુકઅપ_અનુક્રમણિકા<5: 자신.મોકલો(bytes([ord('1')+લુકઅપ_અનુક્રમણિકા]))
                    else: 자신.મોકલો(bytes([30,1,단추들,x_યામ&255,x_યામ>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if શ્રેણી_મૂલ્ય==6:
                    મુખ્ય_પાઠ=정확한값(ક્લાયંટ,7); લંબાઈ_મૂલ્ય=struct.unpack('>i',મુખ્ય_પાઠ[3:])[0]
                    if abs(લંબાઈ_મૂલ્ય)>65536: raise ValueError('clipboard too large')
                    લખાણ=정확한값(ક્લાયંટ,abs(લંબાઈ_મૂલ્ય))
                    if લંબાઈ_મૂલ્ય>=0:
                        try: કીબોર્ડ_પ્રવેશ.ક્લિપબોર્ડ_મૂલ્ય=લખાણ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: કીબોર્ડ_પ્રવેશ.ક્લિપબોર્ડ_મૂલ્ય=લખાણ.decode('latin-1').encode('utf-8')
                        કીબોર્ડ_પ્રવેશ.ક્લિપબોર્ડ_મૂલ્ય=કીબોર્ડ_પ્રવેશ.ક્લિપબોર્ડ_મૂલ્ય[:65536].decode('utf-8','ignore').encode('utf-8')
                    સર્વર_મૂલ્ય.sendall(bytes([શ્રેણી_મૂલ્ય])+મુખ્ય_પાઠ+લખાણ); continue
                if શ્રેણી_મૂલ્ય==0:
                    મુખ્ય_પાઠ=정확한값(ક્લાયંટ,19)
                    if મુખ્ય_પાઠ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=મુખ્ય_પાઠ[3]//8
                elif શ્રેણી_મૂલ્ય==2:
                    મુખ્ય_પાઠ=정확한값(ક્લાયંટ,3); 항목수=struct.unpack('>H',મુખ્ય_પાઠ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ક્લાયંટ,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ડિફૉલ્ટ_મૂલ્ય Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    મુખ્ય_પાઠ=struct.pack('>BHi',0,1,0)
                elif શ્રેણી_મૂલ્ય in (3,150): મુખ્ય_પાઠ=정확한값(ક્લાયંટ,9)
                elif શ્રેણી_મૂલ્ય==248:
                    મુખ્ય_પાઠ=정확한값(ક્લાયંટ,8)
                    if મુખ્ય_પાઠ[7]>64: raise ValueError('fence too large')
                    મુખ્ય_પાઠ+=정확한값(ક્લાયંટ,મુખ્ય_પાઠ[7])
                elif શ્રેણી_મૂલ્ય==250: મુખ્ય_પાઠ=정확한값(ક્લાયંટ,3)
                elif શ્રેણી_મૂલ્ય==251:
                    મુખ્ય_પાઠ=정확한값(ક્લાયંટ,7)
                    if મુખ્ય_પાઠ[5]>16: raise ValueError('too many screens')
                    મુખ્ય_પાઠ+=정확한값(ક્લાયંટ,મુખ્ય_પાઠ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(શ્રેણી_મૂલ્ય))
                સર્વર_મૂલ્ય.sendall(bytes([શ્રેણી_મૂલ્ય])+મુખ્ય_પાઠ)
        except (OSError,EOFError,ValueError) as ભૂલ:
            if str(ભૂલ): print('VNC client:',ભૂલ,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ક્લાયંટ,સર્વર_મૂલ્ય):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ચલાવો_ડેસ્કટૉપ(પોર્ટ_નંબર=5902, નેટવર્ક=False, ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર=2121, 전달규칙들=(), રિઝોલ્યૂશન_મૂલ્ય=(640, 480), અતિથિ_સરનામું=None, હોસ્ટ_સરનામું='127.0.0.1'):
    with ExitStack() as સાધનો, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        નેટવર્ક_બ્રિજ_પ્રવેશ = None
        if નેટવર્ક:
            from નેટવર્ક_બ્રિજ import નેટવર્ક_બ્રિજ
            નેટવર્ક_બ્રિજ_પ્રવેશ = સાધનો.enter_context(નેટવર્ક_બ્રિજ(ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર, 전달규칙들, અતિથિ_સરનામું=અતિથિ_સરનામું, હોસ્ટ_સરનામું=હોસ્ટ_સરનામું))
        પથ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',પોર્ટ_નંબર)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if નેટવર્ક_બ્રિજ_પ્રવેશ and (원격화면접속번호==ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and હોસ્ટ==원격화면접속번호 for 통신규약,હોસ્ટ,_ in નેટવર્ક_બ્રિજ_પ્રવેશ.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            પ્રક્રિયા=subprocess.Popen(આદેશ(રિઝોલ્યૂશન_મૂલ્ય)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(પથ)]+(નેટવર્ક_બ્રિજ_પ્રવેશ.전달인수() if નેટવર્ક_બ્રિજ_પ્રવેશ else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            બ્રિજ=કનેક્ટ_ડેસ્કટૉપ(પ્રક્રિયા); રીડર=threading.Thread(target=બ્રિજ.직렬입출력,daemon=True); રીડર.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if નેટવર્ક_બ્રિજ_પ્રવેશ: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(હોસ્ટ_સરનામું,ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while પ્રક્રિયા.poll() is None:
                    try: ક્લાયંટ,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ક્લાયંટ.close(); continue
                    if not પથ.exists(): ક્લાયંટ.close(); continue
                    처리작업=threading.Thread(target=બ્રિજ.ક્લાયંટ,args=(ક્લાયંટ,પથ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                બ્રિજ.닫힘=True
                if નેટવર્ક_બ્રિજ_પ્રવેશ: નેટવર્ક_બ્રિજ_પ્રવેશ.થોભો_ઇવેંટ.set()
                if પ્રક્રિયા.poll() is None:
                    પ્રક્રિયા.terminate()
                    try: પ્રક્રિયા.wait(timeout=5)
                    except subprocess.TimeoutExpired: પ્રક્રિયા.kill(); પ્રક્રિયા.wait()
                રીડર.join(timeout=2); પ્રક્રિયા.stdin.close(); પ્રક્રિયા.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if નેટવર્ક_બ્રિજ_પ્રવેશ and નેટવર્ક_બ્રિજ_પ્રવેશ.ભૂલ: raise RuntimeError('network bridge: '+નેટવર્ક_બ્રિજ_પ્રવેશ.ભૂલ)
            return 0 if 가로채기됨 else પ્રક્રિયા.returncode


if __name__=='__main__':
    from અમલ_કરો_આદેશ import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    દલીલ_અરે=인수해석기.parse_args()
    if દલીલ_અરે.forward and not દલીલ_અરે.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ચલાવો_ડેસ્કટૉપ(દલીલ_અરે.port,નેટવર્ક=દલીલ_અરે.network,ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર=દલીલ_અરે.ftp_port,전달규칙들=દલીલ_અરે.forward,રિઝોલ્યૂશન_મૂલ્ય=દલીલ_અરે.resolution))
