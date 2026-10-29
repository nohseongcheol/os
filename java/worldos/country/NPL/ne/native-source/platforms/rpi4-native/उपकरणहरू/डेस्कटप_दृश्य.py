#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, कुञ्जी_मान 입력은 निज कर्णेल_मान UART로 전달한다. localhost 전용, 단일 नियन्त्रण_मान 클라이언트.
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
from कार्यान्वयन_गर्नुहोस्_आदेश import आदेश
from local_input import create


def 정확한값(소켓, आकार):
    लगत = bytearray()
    while len(लगत) < आकार:
        조각 = 소켓.recv(आकार - len(लगत))
        if not 조각: raise EOFError()
        लगत.extend(조각)
    return bytes(लगत)


class कुञ्जीपाटी:
    def __init__(자신, पठाउनुहोस्, 입력방식알림=None):
        자신.바이트전송 = पठाउनुहोस्; 자신.परिमार्जनकुञ्जी = set(); 자신.क्लिपबोर्ड_मान = b''
        자신.한글조합기 = create(पठाउनुहोस्, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.परिवर्तन_कुञ्जी = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def पठाउनुहोस्(자신, लगत):
        자신.한글조합기.조합확정()
        자신.바이트전송(लगत)

    def परिवर्तन_मोड(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, कुञ्जी_चिन्ह):
        if कुञ्जी_चिन्ह in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.परिमार्जनकुञ्जी.add(कुञ्जी_चिन्ह)
            else: 자신.परिमार्जनकुञ्जी.discard(कुञ्जी_चिन्ह)
            return
        if not 누르는중:
            자신.परिवर्तन_कुञ्जी.discard(कुञ्जी_चिन्ह)
            return
        CTRL_कुञ्जी = bool(자신.परिमार्जनकुञ्जी & {0xffe3, 0xffe4})
        SHIFT_कुञ्जी = bool(자신.परिमार्जनकुञ्जी & {0xffe1, 0xffe2})
        if CTRL_कुञ्जी and SHIFT_कुञ्जी and कुञ्जी_चिन्ह in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if कुञ्जी_चिन्ह in (32,0xff0d):
                try:
                    मान=int(자신.유니코드입력,16)
                    if 32<=मान<=0x10ffff and not 0xd800<=मान<=0xdfff: 자신.पठाउनुहोस्(chr(मान).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif कुञ्जी_चिन्ह==0xff1b: 자신.유니코드입력=None
            elif कुञ्जी_चिन्ह==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif कुञ्जी_चिन्ह<128 and chr(कुञ्जी_चिन्ह) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(कुञ्जी_चिन्ह)
            return
        if कुञ्जी_चिन्ह in (0xff31,0xffc6) or कुञ्जी_चिन्ह==32 and SHIFT_कुञ्जी and not CTRL_कुञ्जी:
            if कुञ्जी_चिन्ह not in 자신.परिवर्तन_कुञ्जी: 자신.परिवर्तन_मोड()
            자신.परिवर्तन_कुञ्जी.add(कुञ्जी_चिन्ह)
            return
        if कुञ्जी_चिन्ह==0xff08 and 자신.한글여부 and not CTRL_कुञ्जी and 자신.한글조합기.앞글자지우기(): return
        if CTRL_कुञ्जी and SHIFT_कुञ्जी and कुञ्जी_चिन्ह in (ord('t'),ord('T')):
            자신.पठाउनुहोस्(bytes([30,2,1,0,0,0,0])); return
        if कुञ्जी_चिन्ह==0xffc3: 자신.पठाउनुहोस्(bytes([30,2,2,0,0,0,0])); return
        if कुञ्जी_चिन्ह==0xffc9: 자신.पठाउनुहोस्(bytes([30,2,3,0,0,0,0])); return
        if CTRL_कुञ्जी and SHIFT_कुञ्जी and कुञ्जी_चिन्ह in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.पठाउनुहोस्(자신.क्लिपबोर्ड_मान); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if कुञ्जी_चिन्ह in 특수글쇠: 자신.पठाउनुहोस्(특수글쇠[कुञ्जी_चिन्ह]); return
        वर्ण_एनकोडिङ = कुञ्जी_चिन्ह & 0xffffff if कुञ्जी_चिन्ह & 0xff000000 == 0x01000000 else कुञ्जी_चिन्ह
        if वर्ण_एनकोडिङ > 0x10ffff or 0xd800 <= वर्ण_एनकोडिङ <= 0xdfff or कुञ्जी_चिन्ह >= 0xff00 and कुञ्जी_चिन्ह < 0x1000000: return
        if CTRL_कुञ्जी and 0x40 <= वर्ण_एनकोडिङ <= 0x7f: 자신.पठाउनुहोस्(bytes([वर्ण_एनकोडिङ & 31])); return
        if वर्ण_एनकोडिङ < 32: return
        if 자신.한글여부 and 자신.परिमार्जनकुञ्जी & {0xffea,0xfe03,0xff7e} and not CTRL_कुञ्जी and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.फिड_कुञ्जी(chr(वर्ण_एनकोडिङ), altgr=True): return
        앞부분 = b'\x1b' if 자신.परिमार्जनकुञ्जी & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_कुञ्जी and not 앞부분 and 32<=वर्ण_एनकोडिङ<127:
            वर्ण_लगत=chr(वर्ण_एनकोडिङ).upper() if SHIFT_कुञ्जी else chr(वर्ण_एनकोडिङ)
            if 자신.한글조합기.फिड_कुञ्जी(वर्ण_लगत): return
        자신.पठाउनुहोस्(앞부분 + chr(वर्ण_एनकोडिङ).encode('utf-8'))


class कनेक्ट_डेस्कटप:
    def __init__(자신, प्रक्रिया):
        자신.प्रक्रिया=प्रक्रिया; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.टर्मिनल=False; 자신.시작화면=False; 자신.닫힘=False

    def पठाउनुहोस्(자신, लगत):
        if not लगत or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.प्रक्रिया.stdin.write(लगत); 자신.प्रक्रिया.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                लगत=자신.प्रक्रिया.stdout.read(4096)
                if not लगत: break
                sys.stdout.buffer.write(लगत); sys.stdout.buffer.flush()
                끝부분=(끝부분+लगत)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.टर्मिनल=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.पठाउनुहोस्(b'terminal\n')
        finally: 자신.닫힘=True

    def ग्राहक(자신, ग्राहक, मार्ग):
        सर्भर_मान=socket.socket(socket.AF_UNIX); सर्भर_मान.settimeout(10); ग्राहक.settimeout(10)
        कुञ्जीपाटी_प्रविष्टि=कुञ्जीपाटी(자신.पठाउनुहोस्,lambda 한글여부:자신.पठाउनुहोस्(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            सर्भर_मान.connect(str(मार्ग))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            ग्राहक.sendall(정확한값(सर्भर_मान,12))
            판번호=정확한값(ग्राहक,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            सर्भर_मान.sendall(판번호)
            개수=정확한값(सर्भर_मान,1);ग्राहक.sendall(개수+정확한값(सर्भर_मान,개수[0]))
            सुरक्षा=정확한값(ग्राहक,1)
            if सुरक्षा!=b'\x01': raise ValueError('unexpected security type')
            सर्भर_मान.sendall(सुरक्षा)
            if 판번호==b'RFB 003.008\n':ग्राहक.sendall(정확한값(सर्भर_मान,4))
            सर्भर_मान.sendall(정확한값(ग्राहक,1))
            초기값=정확한값(सर्भर_मान,24)
            ग्राहक.sendall(초기값+정확한값(सर्भर_मान,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            ग्राहक.settimeout(None);सर्भर_मान.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        कोटि_मान=정확한값(सर्भर_मान,1)[0]
                        if कोटि_मान==0:
                            머리=정확한값(सर्भर_मान,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 दूर_मान 포인터의 중복을 피한다.
                            लुकाएको_मान=포인터지원
                            if लुकाएको_मान:ग्राहक.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            ग्राहक.sendall(bytes([कोटि_मान])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(सर्भर_मान,12);가로,ठाडो_राख्नुहोस्,폭,높이,एनकोडिङ_मान=struct.unpack('>HHHHi',사각형)
                                if एनकोडिङ_मान!=0:raise ValueError('unexpected framebuffer encoding: '+str(एनकोडिङ_मान))
                                ग्राहक.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    लगत=정확한값(सर्भर_मान,min(남음,65536));ग्राहक.sendall(लगत);남음-=len(लगत)
                        elif कोटि_मान==1:
                            머리=정확한값(सर्भर_मान,5);개수=struct.unpack('>H',머리[3:])[0]
                            ग्राहक.sendall(bytes([कोटि_मान])+머리+정확한값(सर्भर_मान,개수*6))
                        elif कोटि_मान==2:ग्राहक.sendall(bytes([कोटि_मान]))
                        elif कोटि_मान==3:
                            머리=정확한값(सर्भर_मान,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            ग्राहक.sendall(bytes([कोटि_मान])+머리+정확한값(सर्भर_मान,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(कोटि_मान))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:ग्राहक.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                कोटि_मान=정확한값(ग्राहक,1)[0]
                if कोटि_मान==4:
                    मुख्य_पाठ=정확한값(ग्राहक,7); कुञ्जीपाटी_प्रविष्टि.누름값(मुख्य_पाठ[0]!=0,struct.unpack('>I',मुख्य_पाठ[3:])[0]); continue
                if कोटि_मान==255:
                    मुख्य_पाठ=정확한값(ग्राहक,11)
                    if मुख्य_पाठ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    कुञ्जीपाटी_प्रविष्टि.누름값(struct.unpack('>H',मुख्य_पाठ[1:3])[0]!=0,struct.unpack('>I',मुख्य_पाठ[3:7])[0]); continue
                if कोटि_मान==5:
                    मुख्य_पाठ=정확한값(ग्राहक,5); 단추들,x_समन्वय,세로좌표=struct.unpack('>BHH',मुख्य_पाठ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: कुञ्जीपाटी_प्रविष्टि.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_समन्वय<576 and 112<=세로좌표<372:
                        विवरण_हेर्ने_सुविधा_अनुक्रमणिका=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and विवरण_हेर्ने_सुविधा_अनुक्रमणिका<5: 자신.पठाउनुहोस्(bytes([ord('1')+विवरण_हेर्ने_सुविधा_अनुक्रमणिका]))
                    else: 자신.पठाउनुहोस्(bytes([30,1,단추들,x_समन्वय&255,x_समन्वय>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if कोटि_मान==6:
                    मुख्य_पाठ=정확한값(ग्राहक,7); लम्बाइ_मान=struct.unpack('>i',मुख्य_पाठ[3:])[0]
                    if abs(लम्बाइ_मान)>65536: raise ValueError('clipboard too large')
                    पाठ=정확한값(ग्राहक,abs(लम्बाइ_मान))
                    if लम्बाइ_मान>=0:
                        try: कुञ्जीपाटी_प्रविष्टि.क्लिपबोर्ड_मान=पाठ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: कुञ्जीपाटी_प्रविष्टि.क्लिपबोर्ड_मान=पाठ.decode('latin-1').encode('utf-8')
                        कुञ्जीपाटी_प्रविष्टि.क्लिपबोर्ड_मान=कुञ्जीपाटी_प्रविष्टि.क्लिपबोर्ड_मान[:65536].decode('utf-8','ignore').encode('utf-8')
                    सर्भर_मान.sendall(bytes([कोटि_मान])+मुख्य_पाठ+पाठ); continue
                if कोटि_मान==0:
                    मुख्य_पाठ=정확한값(ग्राहक,19)
                    if मुख्य_पाठ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=मुख्य_पाठ[3]//8
                elif कोटि_मान==2:
                    मुख्य_पाठ=정확한값(ग्राहक,3); 항목수=struct.unpack('>H',मुख्य_पाठ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(ग्राहक,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 पूर्वनिर्धारित_मान Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    मुख्य_पाठ=struct.pack('>BHi',0,1,0)
                elif कोटि_मान in (3,150): मुख्य_पाठ=정확한값(ग्राहक,9)
                elif कोटि_मान==248:
                    मुख्य_पाठ=정확한값(ग्राहक,8)
                    if मुख्य_पाठ[7]>64: raise ValueError('fence too large')
                    मुख्य_पाठ+=정확한값(ग्राहक,मुख्य_पाठ[7])
                elif कोटि_मान==250: मुख्य_पाठ=정확한값(ग्राहक,3)
                elif कोटि_मान==251:
                    मुख्य_पाठ=정확한값(ग्राहक,7)
                    if मुख्य_पाठ[5]>16: raise ValueError('too many screens')
                    मुख्य_पाठ+=정확한값(ग्राहक,मुख्य_पाठ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(कोटि_मान))
                सर्भर_मान.sendall(bytes([कोटि_मान])+मुख्य_पाठ)
        except (OSError,EOFError,ValueError) as त्रुटि:
            if str(त्रुटि): print('VNC client:',त्रुटि,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (ग्राहक,सर्भर_मान):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def चलाउनुहोस्_डेस्कटप(접속번호=5902, सञ्जाल=False, 파일전송접속번호=2121, 전달규칙들=(), रिजोल्यूशन_मान=(640, 480), अतिथि_ठेगाना=None, होस्ट_ठेगाना='127.0.0.1'):
    with ExitStack() as संसाधनहरू, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        सञ्जाल_ब्रिज_प्रविष्टि = None
        if सञ्जाल:
            from सञ्जाल_ब्रिज import सञ्जाल_ब्रिज
            सञ्जाल_ब्रिज_प्रविष्टि = संसाधनहरू.enter_context(सञ्जाल_ब्रिज(파일전송접속번호, 전달규칙들, अतिथि_ठेगाना=अतिथि_ठेगाना, होस्ट_ठेगाना=होस्ट_ठेगाना))
        मार्ग=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if सञ्जाल_ब्रिज_प्रविष्टि and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and होस्ट==원격화면접속번호 for 통신규약,होस्ट,_ in सञ्जाल_ब्रिज_प्रविष्टि.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            प्रक्रिया=subprocess.Popen(आदेश(रिजोल्यूशन_मान)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(मार्ग)]+(सञ्जाल_ब्रिज_प्रविष्टि.전달인수() if सञ्जाल_ब्रिज_प्रविष्टि else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ब्रिज=कनेक्ट_डेस्कटप(प्रक्रिया); पाठक=threading.Thread(target=ब्रिज.직렬입출력,daemon=True); पाठक.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if सञ्जाल_ब्रिज_प्रविष्टि: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(होस्ट_ठेगाना,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while प्रक्रिया.poll() is None:
                    try: ग्राहक,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): ग्राहक.close(); continue
                    if not मार्ग.exists(): ग्राहक.close(); continue
                    처리작업=threading.Thread(target=ब्रिज.ग्राहक,args=(ग्राहक,मार्ग),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ब्रिज.닫힘=True
                if सञ्जाल_ब्रिज_प्रविष्टि: सञ्जाल_ब्रिज_प्रविष्टि.पज_घटना.set()
                if प्रक्रिया.poll() is None:
                    प्रक्रिया.terminate()
                    try: प्रक्रिया.wait(timeout=5)
                    except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
                पाठक.join(timeout=2); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if सञ्जाल_ब्रिज_प्रविष्टि and सञ्जाल_ब्रिज_प्रविष्टि.त्रुटि: raise RuntimeError('network bridge: '+सञ्जाल_ब्रिज_प्रविष्टि.त्रुटि)
            return 0 if 가로채기됨 else प्रक्रिया.returncode


if __name__=='__main__':
    from कार्यान्वयन_गर्नुहोस्_आदेश import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    तर्क_विन्यास=인수해석기.parse_args()
    if तर्क_विन्यास.forward and not तर्क_विन्यास.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(चलाउनुहोस्_डेस्कटप(तर्क_विन्यास.port,सञ्जाल=तर्क_विन्यास.network,파일전송접속번호=तर्क_विन्यास.ftp_port,전달규칙들=तर्क_विन्यास.forward,रिजोल्यूशन_मान=तर्क_विन्यास.resolution))
