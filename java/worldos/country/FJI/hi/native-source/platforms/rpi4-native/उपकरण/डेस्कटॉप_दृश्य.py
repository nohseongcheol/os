#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, कुंजी_मान 입력은 निज कर्नेल_मान UART로 전달한다. localhost 전용, 단일 नियंत्रण_मान 클라이언트.
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
from निष्पादित_करें_आदेश import आदेश
from local_input import create


def 정확한값(सॉकेट_मान, आकार):
    आँकड़े = bytearray()
    while len(आँकड़े) < आकार:
        조각 = सॉकेट_मान.recv(आकार - len(आँकड़े))
        if not 조각: raise EOFError()
        आँकड़े.extend(조각)
    return bytes(आँकड़े)


class कीबोर्ड:
    def __init__(자신, भेजें, 입력방식알림=None):
        자신.바이트전송 = भेजें; 자신.मॉडिफ़ायर_कुंजी = set(); 자신.क्लिपबोर्ड_मान = b''
        자신.한글조합기 = create(भेजें, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.स्विच_कुंजी = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def भेजें(자신, आँकड़े):
        자신.한글조합기.조합확정()
        자신.바이트전송(आँकड़े)

    def स्विच_मोड(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, कुंजी_प्रतीक):
        if कुंजी_प्रतीक in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.मॉडिफ़ायर_कुंजी.add(कुंजी_प्रतीक)
            else: 자신.मॉडिफ़ायर_कुंजी.discard(कुंजी_प्रतीक)
            return
        if not 누르는중:
            자신.स्विच_कुंजी.discard(कुंजी_प्रतीक)
            return
        नियंत्रण_कुंजी = bool(자신.मॉडिफ़ायर_कुंजी & {0xffe3, 0xffe4})
        SHIFT_कुंजी = bool(자신.मॉडिफ़ायर_कुंजी & {0xffe1, 0xffe2})
        if नियंत्रण_कुंजी and SHIFT_कुंजी and कुंजी_प्रतीक in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if कुंजी_प्रतीक in (32,0xff0d):
                try:
                    मान=int(자신.유니코드입력,16)
                    if 32<=मान<=0x10ffff and not 0xd800<=मान<=0xdfff: 자신.भेजें(chr(मान).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif कुंजी_प्रतीक==0xff1b: 자신.유니코드입력=None
            elif कुंजी_प्रतीक==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif कुंजी_प्रतीक<128 and chr(कुंजी_प्रतीक) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(कुंजी_प्रतीक)
            return
        if कुंजी_प्रतीक in (0xff31,0xffc6) or कुंजी_प्रतीक==32 and SHIFT_कुंजी and not नियंत्रण_कुंजी:
            if कुंजी_प्रतीक not in 자신.स्विच_कुंजी: 자신.स्विच_मोड()
            자신.स्विच_कुंजी.add(कुंजी_प्रतीक)
            return
        if कुंजी_प्रतीक==0xff08 and 자신.한글여부 and not नियंत्रण_कुंजी and 자신.한글조합기.앞글자지우기(): return
        if नियंत्रण_कुंजी and SHIFT_कुंजी and कुंजी_प्रतीक in (ord('t'),ord('T')):
            자신.भेजें(bytes([30,2,1,0,0,0,0])); return
        if कुंजी_प्रतीक==0xffc3: 자신.भेजें(bytes([30,2,2,0,0,0,0])); return
        if कुंजी_प्रतीक==0xffc9: 자신.भेजें(bytes([30,2,3,0,0,0,0])); return
        if नियंत्रण_कुंजी and SHIFT_कुंजी and कुंजी_प्रतीक in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.भेजें(자신.क्लिपबोर्ड_मान); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if कुंजी_प्रतीक in 특수글쇠: 자신.भेजें(특수글쇠[कुंजी_प्रतीक]); return
        वर्ण_एन्_कोडिंग = कुंजी_प्रतीक & 0xffffff if कुंजी_प्रतीक & 0xff000000 == 0x01000000 else कुंजी_प्रतीक
        if वर्ण_एन्_कोडिंग > 0x10ffff or 0xd800 <= वर्ण_एन्_कोडिंग <= 0xdfff or कुंजी_प्रतीक >= 0xff00 and कुंजी_प्रतीक < 0x1000000: return
        if नियंत्रण_कुंजी and 0x40 <= वर्ण_एन्_कोडिंग <= 0x7f: 자신.भेजें(bytes([वर्ण_एन्_कोडिंग & 31])); return
        if वर्ण_एन्_कोडिंग < 32: return
        if 자신.한글여부 and 자신.मॉडिफ़ायर_कुंजी & {0xffea,0xfe03,0xff7e} and not नियंत्रण_कुंजी and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.फ़ीड_कुंजी(chr(वर्ण_एन्_कोडिंग), altgr=True): return
        앞부분 = b'\x1b' if 자신.मॉडिफ़ायर_कुंजी & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not नियंत्रण_कुंजी and not 앞부분 and 32<=वर्ण_एन्_कोडिंग<127:
            वर्ण_डेटा=chr(वर्ण_एन्_कोडिंग).upper() if SHIFT_कुंजी else chr(वर्ण_एन्_कोडिंग)
            if 자신.한글조합기.फ़ीड_कुंजी(वर्ण_डेटा): return
        자신.भेजें(앞부분 + chr(वर्ण_एन्_कोडिंग).encode('utf-8'))


class कनेक्ट_डेस्कटॉप:
    def __init__(자신, प्रक्रिया):
        자신.प्रक्रिया=प्रक्रिया; 자신.लॉक_मान=threading.Lock(); 자신.준비완료=False; 자신.आदेशपटल=False; 자신.시작화면=False; 자신.닫힘=False

    def भेजें(자신, आँकड़े):
        if not आँकड़े or 자신.닫힘: return
        with 자신.लॉक_मान:
            try: 자신.प्रक्रिया.stdin.write(आँकड़े); 자신.प्रक्रिया.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                आँकड़े=자신.प्रक्रिया.stdout.read(4096)
                if not आँकड़े: break
                sys.stdout.buffer.write(आँकड़े); sys.stdout.buffer.flush()
                끝부분=(끝부분+आँकड़े)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.आदेशपटल=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.भेजें(b'terminal\n')
        finally: 자신.닫힘=True

    def क्लायंट(자신, क्लायंट, पथ):
        서버=socket.socket(socket.AF_UNIX); 서버.settimeout(10); क्लायंट.settimeout(10)
        कीबोर्ड_एन्ट्री=कीबोर्ड(자신.भेजें,lambda 한글여부:자신.भेजें(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            서버.connect(str(पथ))
            # प्रारंभिक_स्थिति 협상은 순서대로 끝낸다. 이후 निर्गम 가닥만 클라이언트에 쓴다.
            क्लायंट.sendall(정확한값(서버,12))
            संस्करण_संख्या=정확한값(क्लायंट,12)
            if संस्करण_संख्या not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            서버.sendall(संस्करण_संख्या)
            개수=정확한값(서버,1);क्लायंट.sendall(개수+정확한값(서버,개수[0]))
            सुरक्षा=정확한값(क्लायंट,1)
            if सुरक्षा!=b'\x01': raise ValueError('unexpected security type')
            서버.sendall(सुरक्षा)
            if संस्करण_संख्या==b'RFB 003.008\n':क्लायंट.sendall(정확한값(서버,4))
            서버.sendall(정확한값(क्लायंट,1))
            초기값=정확한값(서버,24)
            क्लायंट.sendall(초기값+정확한값(서버,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            क्लायंट.settimeout(None);서버.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        श्रेणी_मान=정확한값(서버,1)[0]
                        if श्रेणी_मान==0:
                            머리=정확한값(서버,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 दूरस्थ_मान 포인터의 중복을 피한다.
                            छुपा_हुआ_मान=포인터지원
                            if छुपा_हुआ_मान:क्लायंट.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            क्लायंट.sendall(bytes([श्रेणी_मान])+머리)
                            for _ in range(항목수):
                                रेक्_टेंगल=정확한값(서버,12);가로,अनुलंब_पद,폭,높이,एन्कोडिंग_मान=struct.unpack('>HHHHi',रेक्_टेंगल)
                                if एन्कोडिंग_मान!=0:raise ValueError('unexpected framebuffer encoding: '+str(एन्कोडिंग_मान))
                                क्लायंट.sendall(रेक्_टेंगल)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    आँकड़े=정확한값(서버,min(남음,65536));क्लायंट.sendall(आँकड़े);남음-=len(आँकड़े)
                        elif श्रेणी_मान==1:
                            머리=정확한값(서버,5);개수=struct.unpack('>H',머리[3:])[0]
                            क्लायंट.sendall(bytes([श्रेणी_मान])+머리+정확한값(서버,개수*6))
                        elif श्रेणी_मान==2:क्लायंट.sendall(bytes([श्रेणी_मान]))
                        elif श्रेणी_मान==3:
                            머리=정확한값(서버,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            क्लायंट.sendall(bytes([श्रेणी_मान])+머리+정확한값(서버,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(श्रेणी_मान))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:क्लायंट.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            कार्यसूत्र=threading.Thread(target=출력결과,daemon=True);कार्यसूत्र.start()
            while not 자신.닫힘:
                श्रेणी_मान=정확한값(क्लायंट,1)[0]
                if श्रेणी_मान==4:
                    मुख्य_पाठ=정확한값(क्लायंट,7); कीबोर्ड_एन्ट्री.누름값(मुख्य_पाठ[0]!=0,struct.unpack('>I',मुख्य_पाठ[3:])[0]); continue
                if श्रेणी_मान==255:
                    मुख्य_पाठ=정확한값(क्लायंट,11)
                    if मुख्य_पाठ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    कीबोर्ड_एन्ट्री.누름값(struct.unpack('>H',मुख्य_पाठ[1:3])[0]!=0,struct.unpack('>I',मुख्य_पाठ[3:7])[0]); continue
                if श्रेणी_मान==5:
                    मुख्य_पाठ=정확한값(क्लायंट,5); 단추들,x_निर्देशांक,세로좌표=struct.unpack('>BHH',मुख्य_पाठ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: कीबोर्ड_एन्ट्री.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_निर्देशांक<576 and 112<=세로좌표<372:
                        लुकअप_इंडेक्स=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and लुकअप_इंडेक्स<5: 자신.भेजें(bytes([ord('1')+लुकअप_इंडेक्स]))
                    else: 자신.भेजें(bytes([30,1,단추들,x_निर्देशांक&255,x_निर्देशांक>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if श्रेणी_मान==6:
                    मुख्य_पाठ=정확한값(क्लायंट,7); 길이=struct.unpack('>i',मुख्य_पाठ[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    पाठ=정확한값(क्लायंट,abs(길이))
                    if 길이>=0:
                        try: कीबोर्ड_एन्ट्री.क्लिपबोर्ड_मान=पाठ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: कीबोर्ड_एन्ट्री.क्लिपबोर्ड_मान=पाठ.decode('latin-1').encode('utf-8')
                        कीबोर्ड_एन्ट्री.क्लिपबोर्ड_मान=कीबोर्ड_एन्ट्री.क्लिपबोर्ड_मान[:65536].decode('utf-8','ignore').encode('utf-8')
                    서버.sendall(bytes([श्रेणी_मान])+मुख्य_पाठ+पाठ); continue
                if श्रेणी_मान==0:
                    मुख्य_पाठ=정확한값(क्लायंट,19)
                    if मुख्य_पाठ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=मुख्य_पाठ[3]//8
                elif श्रेणी_मान==2:
                    मुख्य_पाठ=정확한값(क्लायंट,3); 항목수=struct.unpack('>H',मुख्य_पाठ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(क्लायंट,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 डिफ़ॉल्ट_मान Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    मुख्य_पाठ=struct.pack('>BHi',0,1,0)
                elif श्रेणी_मान in (3,150): मुख्य_पाठ=정확한값(क्लायंट,9)
                elif श्रेणी_मान==248:
                    मुख्य_पाठ=정확한값(क्लायंट,8)
                    if मुख्य_पाठ[7]>64: raise ValueError('fence too large')
                    मुख्य_पाठ+=정확한값(क्लायंट,मुख्य_पाठ[7])
                elif श्रेणी_मान==250: मुख्य_पाठ=정확한값(क्लायंट,3)
                elif श्रेणी_मान==251:
                    मुख्य_पाठ=정확한값(क्लायंट,7)
                    if मुख्य_पाठ[5]>16: raise ValueError('too many screens')
                    मुख्य_पाठ+=정확한값(क्लायंट,मुख्य_पाठ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(श्रेणी_मान))
                서버.sendall(bytes([श्रेणी_मान])+मुख्य_पाठ)
        except (OSError,EOFError,ValueError) as त्रुटि:
            if str(त्रुटि): print('VNC client:',त्रुटि,file=sys.stderr,flush=True)
        finally:
            for सॉकेट_मान in (क्लायंट,서버):
                try: सॉकेट_मान.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                सॉकेट_मान.close()


def चलाएँ_डेस्कटॉप(पोर्ट_संख्या=5902, नेटवर्क=False, फ़ाइल_स्थानांतरण_पोर्ट_संख्या=2121, 전달규칙들=(), रिज़ॉल्यूशन_मान=(640, 480), अतिथि_पता=None, आयोजक_पता='127.0.0.1'):
    with ExitStack() as संसाधन, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        ब्रिज_एन्ट्री = None
        if नेटवर्क:
            from ब्रिज_3de4fe3a import ब्रिज_3de4fe3a
            ब्रिज_एन्ट्री = संसाधन.enter_context(ब्रिज_3de4fe3a(फ़ाइल_स्थानांतरण_पोर्ट_संख्या, 전달규칙들, अतिथि_पता=अतिथि_पता, आयोजक_पता=आयोजक_पता))
        पथ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',पोर्ट_संख्या)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if ब्रिज_एन्ट्री and (원격화면접속번호==फ़ाइल_स्थानांतरण_पोर्ट_संख्या or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and आयोजक==원격화면접속번호 for 통신규약,आयोजक,_ in ब्रिज_एन्ट्री.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            प्रक्रिया=subprocess.Popen(आदेश(रिज़ॉल्यूशन_मान)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(पथ)]+(ब्रिज_एन्ट्री.전달인수() if ब्रिज_एन्ट्री else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ब्रिज=कनेक्ट_डेस्कटॉप(प्रक्रिया); पाठक=threading.Thread(target=ब्रिज.직렬입출력,daemon=True); पाठक.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if ब्रिज_एन्ट्री: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(आयोजक_पता,फ़ाइल_स्थानांतरण_पोर्ट_संख्या),flush=True)
            def पर्यवसान(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,पर्यवसान)
            संसाधन_कार्य=None; 가로채기됨=False
            try:
                while प्रक्रिया.poll() is None:
                    try: क्लायंट,_=수신창구.accept()
                    except socket.timeout: continue
                    if संसाधन_कार्य is not None and संसाधन_कार्य.is_alive(): क्लायंट.close(); continue
                    if not पथ.exists(): क्लायंट.close(); continue
                    संसाधन_कार्य=threading.Thread(target=ब्रिज.क्लायंट,args=(क्लायंट,पथ),daemon=True); संसाधन_कार्य.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ब्रिज.닫힘=True
                if ब्रिज_एन्ट्री: ब्रिज_एन्ट्री.रोकें_घटना.set()
                if प्रक्रिया.poll() is None:
                    प्रक्रिया.terminate()
                    try: प्रक्रिया.wait(timeout=5)
                    except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
                पाठक.join(timeout=2); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if ब्रिज_एन्ट्री and ब्रिज_एन्ट्री.त्रुटि: raise RuntimeError('network bridge: '+ब्रिज_एन्ट्री.त्रुटि)
            return 0 if 가로채기됨 else प्रक्रिया.returncode


if __name__=='__main__':
    from निष्पादित_करें_आदेश import पढें_रिज़ॉल्यूशन
    पार्सर=argparse.ArgumentParser(description=__doc__); पार्सर.add_argument('--port',type=int,default=5902)
    पार्सर.add_argument('--resolution',type=पढें_रिज़ॉल्यूशन,default=(640,480))
    पार्सर.add_argument('--network',action='store_true'); पार्सर.add_argument('--ftp-port',type=int,default=2121)
    पार्सर.add_argument('--forward',action='append',default=[])
    तर्क_सरणी=पार्सर.parse_args()
    if तर्क_सरणी.forward and not तर्क_सरणी.network: पार्सर.error('--forward requires --network')
    raise SystemExit(चलाएँ_डेस्कटॉप(तर्क_सरणी.port,नेटवर्क=तर्क_सरणी.network,फ़ाइल_स्थानांतरण_पोर्ट_संख्या=तर्क_सरणी.ftp_port,전달규칙들=तर्क_सरणी.forward,रिज़ॉल्यूशन_मान=तर्क_सरणी.resolution))
