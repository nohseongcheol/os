#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, कळ_मूल्य 입력은 स्वकीय गाभा_मूल्य UART로 전달한다. localhost 전용, 단일 नियंत्रण_मूल्य 클라이언트.
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
from आज्ञा_कार्यवाही_करा import आदेश
from local_input import create


def तंतोतंत_मूल्य(संचारद्वार_मूल्य, आकार):
    डेटा = bytearray()
    while len(डेटा) < आकार:
        तुकडा_मूल्य = संचारद्वार_मूल्य.recv(आकार - len(डेटा))
        if not तुकडा_मूल्य: raise EOFError()
        डेटा.extend(तुकडा_मूल्य)
    return bytes(डेटा)


class कीबोर्ड:
    def __init__(स्वतः, पाठवा, मोड_बदललेले=None):
        स्वतः.स्थानांतर_बाइट = पाठवा; स्वतः.मॉडिफायर_कळ = set(); स्वतः.क्लिपबोर्ड_मूल्य = b''
        स्वतः.हांगुल_संयोजक = create(पाठवा, Path(__file__).resolve().parents[1]); स्वतः.कोरियन = False; स्वतः.स्विच_कळ = set()
        स्वतः.युनिकोड_आदान = None
        स्वतः.मोड_बदललेले = मोड_बदललेले
        if मोड_बदललेले: मोड_बदललेले(False)

    def पाठवा(स्वतः, डेटा):
        स्वतः.हांगुल_संयोजक.स्थिरकरा_संयोजन()
        स्वतः.स्थानांतर_बाइट(डेटा)

    def स्विच_मोड(स्वतः):
        स्वतः.हांगुल_संयोजक.स्थिरकरा_संयोजन(); स्वतः.कोरियन = not स्वतः.कोरियन
        if स्वतः.मोड_बदललेले: स्वतः.मोड_बदललेले(स्वतः.कोरियन)

    def दाबलेले_मूल्य(स्वतः, आहे_दाबणे, कळ_चिन्ह):
        if कळ_चिन्ह in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if आहे_दाबणे: स्वतः.मॉडिफायर_कळ.add(कळ_चिन्ह)
            else: स्वतः.मॉडिफायर_कळ.discard(कळ_चिन्ह)
            return
        if not आहे_दाबणे:
            स्वतः.स्विच_कळ.discard(कळ_चिन्ह)
            return
        CTRL_कळ = bool(स्वतः.मॉडिफायर_कळ & {0xffe3, 0xffe4})
        SHIFT_कळ = bool(स्वतः.मॉडिफायर_कळ & {0xffe1, 0xffe2})
        if CTRL_कळ and SHIFT_कळ and कळ_चिन्ह in (ord('u'),ord('U')):
            स्वतः.हांगुल_संयोजक.स्थिरकरा_संयोजन(); स्वतः.युनिकोड_आदान = ''; return
        if स्वतः.युनिकोड_आदान is not None:
            if कळ_चिन्ह in (32,0xff0d):
                try:
                    मूल्य=int(स्वतः.युनिकोड_आदान,16)
                    if 32<=मूल्य<=0x10ffff and not 0xd800<=मूल्य<=0xdfff: स्वतः.पाठवा(chr(मूल्य).encode('utf-8'))
                except ValueError: pass
                स्वतः.युनिकोड_आदान=None
            elif कळ_चिन्ह==0xff1b: स्वतः.युनिकोड_आदान=None
            elif कळ_चिन्ह==0xff08: स्वतः.युनिकोड_आदान=स्वतः.युनिकोड_आदान[:-1]
            elif कळ_चिन्ह<128 and chr(कळ_चिन्ह) in '0123456789abcdefABCDEF' and len(स्वतः.युनिकोड_आदान)<6: स्वतः.युनिकोड_आदान+=chr(कळ_चिन्ह)
            return
        if कळ_चिन्ह in (0xff31,0xffc6) or कळ_चिन्ह==32 and SHIFT_कळ and not CTRL_कळ:
            if कळ_चिन्ह not in स्वतः.स्विच_कळ: स्वतः.स्विच_मोड()
            स्वतः.स्विच_कळ.add(कळ_चिन्ह)
            return
        if कळ_चिन्ह==0xff08 and स्वतः.कोरियन and not CTRL_कळ and स्वतः.हांगुल_संयोजक.मागीलवर्णपुसा(): return
        if CTRL_कळ and SHIFT_कळ and कळ_चिन्ह in (ord('t'),ord('T')):
            स्वतः.पाठवा(bytes([30,2,1,0,0,0,0])); return
        if कळ_चिन्ह==0xffc3: स्वतः.पाठवा(bytes([30,2,2,0,0,0,0])); return
        if कळ_चिन्ह==0xffc9: स्वतः.पाठवा(bytes([30,2,3,0,0,0,0])); return
        if CTRL_कळ and SHIFT_कळ and कळ_चिन्ह in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            स्वतः.पाठवा(स्वतः.क्लिपबोर्ड_मूल्य); return
        विशेष_कळ = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if कळ_चिन्ह in विशेष_कळ: स्वतः.पाठवा(विशेष_कळ[कळ_चिन्ह]); return
        वर्ण_एन्कोडिंग = कळ_चिन्ह & 0xffffff if कळ_चिन्ह & 0xff000000 == 0x01000000 else कळ_चिन्ह
        if वर्ण_एन्कोडिंग > 0x10ffff or 0xd800 <= वर्ण_एन्कोडिंग <= 0xdfff or कळ_चिन्ह >= 0xff00 and कळ_चिन्ह < 0x1000000: return
        if CTRL_कळ and 0x40 <= वर्ण_एन्कोडिंग <= 0x7f: स्वतः.पाठवा(bytes([वर्ण_एन्कोडिंग & 31])); return
        if वर्ण_एन्कोडिंग < 32: return
        if स्वतः.कोरियन and स्वतः.मॉडिफायर_कळ & {0xffea,0xfe03,0xff7e} and not CTRL_कळ and hasattr(स्वतः.हांगुल_संयोजक, 'profile'):
            if स्वतः.हांगुल_संयोजक.फीड_कळ(chr(वर्ण_एन्कोडिंग), altgr=True): return
        अग्रस्थान_भाग = b'\x1b' if स्वतः.मॉडिफायर_कळ & {0xffe9, 0xffea} else b''
        if स्वतः.कोरियन and not CTRL_कळ and not अग्रस्थान_भाग and 32<=वर्ण_एन्कोडिंग<127:
            वर्ण_डेटा=chr(वर्ण_एन्कोडिंग).upper() if SHIFT_कळ else chr(वर्ण_एन्कोडिंग)
            if स्वतः.हांगुल_संयोजक.फीड_कळ(वर्ण_डेटा): return
        स्वतः.पाठवा(अग्रस्थान_भाग + chr(वर्ण_एन्कोडिंग).encode('utf-8'))


class कनेक्ट_डेस्कटॉप:
    def __init__(स्वतः, प्रक्रिया):
        स्वतः.प्रक्रिया=प्रक्रिया; स्वतः.कुलूप_मूल्य=threading.Lock(); स्वतः.तयारी_पूर्ण=False; स्वतः.टर्मिनल=False; स्वतः.प्रारंभिक_पडदा=False; स्वतः.आहे_बंदकेलेले=False

    def पाठवा(स्वतः, डेटा):
        if not डेटा or स्वतः.आहे_बंदकेलेले: return
        with स्वतः.कुलूप_मूल्य:
            try: स्वतः.प्रक्रिया.stdin.write(डेटा); स्वतः.प्रक्रिया.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def अनुक्रमिक_आदानप्रदान(स्वतः):
        शेवट_भाग=b''
        try:
            while True:
                डेटा=स्वतः.प्रक्रिया.stdout.read(4096)
                if not डेटा: break
                sys.stdout.buffer.write(डेटा); sys.stdout.buffer.flush()
                शेवट_भाग=(शेवट_भाग+डेटा)[-8192:]
                उघडलेले=शेवट_भाग.rfind(b'TERMINAL READY'); आहे_बंदकेलेले=शेवट_भाग.rfind(b'TERMINAL CLOSED'); रेखांकन_पडदा=शेवट_भाग.rfind(b'GUI READY:'); आहे_बाहेरपडलेले=शेवट_भाग.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(उघडलेले,आहे_बंदकेलेले,रेखांकन_पडदा,आहे_बाहेरपडलेले)>=0:
                    स्वतः.टर्मिनल=उघडलेले>max(आहे_बंदकेलेले,रेखांकन_पडदा,आहे_बाहेरपडलेले)
                    स्वतः.प्रारंभिक_पडदा=रेखांकन_पडदा>max(उघडलेले,आहे_बंदकेलेले,आहे_बाहेरपडलेले)
                if not स्वतः.तयारी_पूर्ण and b'jkoros-native> ' in शेवट_भाग:
                    स्वतः.तयारी_पूर्ण=True; स्वतः.पाठवा(b'terminal\n')
        finally: स्वतः.आहे_बंदकेलेले=True

    def क्लायंट(स्वतः, क्लायंट, मार्ग):
        सर्व्हर_मूल्य=socket.socket(socket.AF_UNIX); सर्व्हर_मूल्य.settimeout(10); क्लायंट.settimeout(10)
        कीबोर्ड_प्रविष्टी=कीबोर्ड(स्वतः.पाठवा,lambda कोरियन:स्वतः.पाठवा(bytes([30,3,int(कोरियन),0,0,0,0])))
        मागील_बटणे=0
        try:
            सर्व्हर_मूल्य.connect(str(मार्ग))
            # प्रारंभिक_राज्य 협상은 순서대로 끝낸다. नंतर_मूल्य_ee1d8655 आउटपुट 가닥만 클라이언트에 쓴다.
            क्लायंट.sendall(तंतोतंत_मूल्य(सर्व्हर_मूल्य,12))
            आवृत्ती_संख्या=तंतोतंत_मूल्य(क्लायंट,12)
            if आवृत्ती_संख्या not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            सर्व्हर_मूल्य.sendall(आवृत्ती_संख्या)
            आयटम_संख्या=तंतोतंत_मूल्य(सर्व्हर_मूल्य,1);क्लायंट.sendall(आयटम_संख्या+तंतोतंत_मूल्य(सर्व्हर_मूल्य,आयटम_संख्या[0]))
            सुरक्षा=तंतोतंत_मूल्य(क्लायंट,1)
            if सुरक्षा!=b'\x01': raise ValueError('unexpected security type')
            सर्व्हर_मूल्य.sendall(सुरक्षा)
            if आवृत्ती_संख्या==b'RFB 003.008\n':क्लायंट.sendall(तंतोतंत_मूल्य(सर्व्हर_मूल्य,4))
            सर्व्हर_मूल्य.sendall(तंतोतंत_मूल्य(क्लायंट,1))
            प्रारंभिक_मूल्य=तंतोतंत_मूल्य(सर्व्हर_मूल्य,24)
            क्लायंट.sendall(प्रारंभिक_मूल्य+तंतोतंत_मूल्य(सर्व्हर_मूल्य,struct.unpack('>I',प्रारंभिक_मूल्य[20:])[0]))
            पिक्सेल_बाइट=प्रारंभिक_मूल्य[4]//8;निर्देशक_समर्थित=False
            क्लायंट.settimeout(None);सर्व्हर_मूल्य.settimeout(None)
            def प्रदान():
                try:
                    while True:
                        वर्गवारी_मूल्य=तंतोतंत_मूल्य(सर्व्हर_मूल्य,1)[0]
                        if वर्गवारी_मूल्य==0:
                            शीर्ष_मूल्य=तंतोतंत_मूल्य(सर्व्हर_मूल्य,3);प्रविष्टी_संख्या=struct.unpack('>H',शीर्ष_मूल्य[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 दूरस्_थ_मूल्य 포인터의 중복을 피한다.
                            लपलेले_मूल्य=निर्देशक_समर्थित
                            if लपलेले_मूल्य:क्लायंट.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            क्लायंट.sendall(bytes([वर्गवारी_मूल्य])+शीर्ष_मूल्य)
                            for _ in range(प्रविष्टी_संख्या):
                                आयत=तंतोतंत_मूल्य(सर्व्हर_मूल्य,12);आडवे_स्थान,अनुलंब_स्थान,रुंदी_विस्तार,उंची_मूल्य,एन्कोडिंग_मूल्य=struct.unpack('>HHHHi',आयत)
                                if एन्कोडिंग_मूल्य!=0:raise ValueError('unexpected framebuffer encoding: '+str(एन्कोडिंग_मूल्य))
                                क्लायंट.sendall(आयत)
                                बाकी_डेटा=रुंदी_विस्तार*उंची_मूल्य*पिक्सेल_बाइट
                                while बाकी_डेटा:
                                    डेटा=तंतोतंत_मूल्य(सर्व्हर_मूल्य,min(बाकी_डेटा,65536));क्लायंट.sendall(डेटा);बाकी_डेटा-=len(डेटा)
                        elif वर्गवारी_मूल्य==1:
                            शीर्ष_मूल्य=तंतोतंत_मूल्य(सर्व्हर_मूल्य,5);आयटम_संख्या=struct.unpack('>H',शीर्ष_मूल्य[3:])[0]
                            क्लायंट.sendall(bytes([वर्गवारी_मूल्य])+शीर्ष_मूल्य+तंतोतंत_मूल्य(सर्व्हर_मूल्य,आयटम_संख्या*6))
                        elif वर्गवारी_मूल्य==2:क्लायंट.sendall(bytes([वर्गवारी_मूल्य]))
                        elif वर्गवारी_मूल्य==3:
                            शीर्ष_मूल्य=तंतोतंत_मूल्य(सर्व्हर_मूल्य,7);आयटम_संख्या=struct.unpack('>I',शीर्ष_मूल्य[3:])[0]
                            if आयटम_संख्या>1048576:raise ValueError('server clipboard too large')
                            क्लायंट.sendall(bytes([वर्गवारी_मूल्य])+शीर्ष_मूल्य+तंतोतंत_मूल्य(सर्व्हर_मूल्य,आयटम_संख्या))
                        else:raise ValueError('unexpected RFB server message: '+str(वर्गवारी_मूल्य))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:क्लायंट.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            कार्यसूत्र=threading.Thread(target=प्रदान,daemon=True);कार्यसूत्र.start()
            while not स्वतः.आहे_बंदकेलेले:
                वर्गवारी_मूल्य=तंतोतंत_मूल्य(क्लायंट,1)[0]
                if वर्गवारी_मूल्य==4:
                    मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,7); कीबोर्ड_प्रविष्टी.दाबलेले_मूल्य(मुख्य_मजकूर[0]!=0,struct.unpack('>I',मुख्य_मजकूर[3:])[0]); continue
                if वर्गवारी_मूल्य==255:
                    मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,11)
                    if मुख्य_मजकूर[0]!=0: raise ValueError('unsupported QEMU input extension')
                    कीबोर्ड_प्रविष्टी.दाबलेले_मूल्य(struct.unpack('>H',मुख्य_मजकूर[1:3])[0]!=0,struct.unpack('>I',मुख्य_मजकूर[3:7])[0]); continue
                if वर्गवारी_मूल्य==5:
                    मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,5); बटणे,आडवे_समन्वयीत,उभे_समन्वयीत=struct.unpack('>BHH',मुख्य_मजकूर)
                    आहे_दाबलेले=बटणे&~मागील_बटणे; मागील_बटणे=बटणे
                    if आहे_दाबलेले: कीबोर्ड_प्रविष्टी.हांगुल_संयोजक.स्थिरकरा_संयोजन()
                    if आहे_दाबलेले&1 and स्वतः.प्रारंभिक_पडदा and 64<=आडवे_समन्वयीत<576 and 112<=उभे_समन्वयीत<372:
                        लुकअप_अनुक्रमणिका=(उभे_समन्वयीत-112)//52
                        if (उभे_समन्वयीत-112)%52<40 and लुकअप_अनुक्रमणिका<5: स्वतः.पाठवा(bytes([ord('1')+लुकअप_अनुक्रमणिका]))
                    else: स्वतः.पाठवा(bytes([30,1,बटणे,आडवे_समन्वयीत&255,आडवे_समन्वयीत>>8,उभे_समन्वयीत&255,उभे_समन्वयीत>>8]))
                    continue
                if वर्गवारी_मूल्य==6:
                    मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,7); लांबी_मूल्य=struct.unpack('>i',मुख्य_मजकूर[3:])[0]
                    if abs(लांबी_मूल्य)>65536: raise ValueError('clipboard too large')
                    पाठ्य=तंतोतंत_मूल्य(क्लायंट,abs(लांबी_मूल्य))
                    if लांबी_मूल्य>=0:
                        try: कीबोर्ड_प्रविष्टी.क्लिपबोर्ड_मूल्य=पाठ्य.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: कीबोर्ड_प्रविष्टी.क्लिपबोर्ड_मूल्य=पाठ्य.decode('latin-1').encode('utf-8')
                        कीबोर्ड_प्रविष्टी.क्लिपबोर्ड_मूल्य=कीबोर्ड_प्रविष्टी.क्लिपबोर्ड_मूल्य[:65536].decode('utf-8','ignore').encode('utf-8')
                    सर्व्हर_मूल्य.sendall(bytes([वर्गवारी_मूल्य])+मुख्य_मजकूर+पाठ्य); continue
                if वर्गवारी_मूल्य==0:
                    मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,19)
                    if मुख्य_मजकूर[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    पिक्सेल_बाइट=मुख्य_मजकूर[3]//8
                elif वर्गवारी_मूल्य==2:
                    मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,3); प्रविष्टी_संख्या=struct.unpack('>H',मुख्य_मजकूर[1:])[0]
                    if प्रविष्टी_संख्या>512: raise ValueError('too many encodings')
                    संकेतित_मूल्ये=struct.unpack('>'+str(प्रविष्टी_संख्या)+'i',तंतोतंत_मूल्य(क्लायंट,प्रविष्टी_संख्या*4))
                    निर्देशक_समर्थित=-239 in संकेतित_मूल्ये
                    # 로컬 पडदा 중계는 डिफॉल्ट_मूल्य Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    मुख्य_मजकूर=struct.pack('>BHi',0,1,0)
                elif वर्गवारी_मूल्य in (3,150): मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,9)
                elif वर्गवारी_मूल्य==248:
                    मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,8)
                    if मुख्य_मजकूर[7]>64: raise ValueError('fence too large')
                    मुख्य_मजकूर+=तंतोतंत_मूल्य(क्लायंट,मुख्य_मजकूर[7])
                elif वर्गवारी_मूल्य==250: मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,3)
                elif वर्गवारी_मूल्य==251:
                    मुख्य_मजकूर=तंतोतंत_मूल्य(क्लायंट,7)
                    if मुख्य_मजकूर[5]>16: raise ValueError('too many screens')
                    मुख्य_मजकूर+=तंतोतंत_मूल्य(क्लायंट,मुख्य_मजकूर[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(वर्गवारी_मूल्य))
                सर्व्हर_मूल्य.sendall(bytes([वर्गवारी_मूल्य])+मुख्य_मजकूर)
        except (OSError,EOFError,ValueError) as त्रुटी:
            if str(त्रुटी): print('VNC client:',त्रुटी,file=sys.stderr,flush=True)
        finally:
            for संचारद्वार_मूल्य in (क्लायंट,सर्व्हर_मूल्य):
                try: संचारद्वार_मूल्य.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                संचारद्वार_मूल्य.close()


def रन_डेस्कटॉप(पोर्ट_नंबर=5902, संचारजाळे=False, संचिका_स्थानांतर_पोर्ट_नंबर=2121, अग्रेषण_नियम_f4578a27=(), बिंदूघनता_मूल्य=(640, 480), अतिथी_पत्ता=None, होस्ट_पत्ता='127.0.0.1'):
    with ExitStack() as संसाधने, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as कार्यरत_पथ:
        संचारजाळे_ब्रिज_प्रविष्टी = None
        if संचारजाळे:
            from संचारजाळे_ब्रिज import संचारजाळे_ब्रिज
            संचारजाळे_ब्रिज_प्रविष्टी = संसाधने.enter_context(संचारजाळे_ब्रिज(संचिका_स्थानांतर_पोर्ट_नंबर, अग्रेषण_नियम_f4578a27, अतिथी_पत्ता=अतिथी_पत्ता, होस्ट_पत्ता=होस्ट_पत्ता))
        मार्ग=Path(कार्यरत_पथ)/'display.sock'
        with socket.socket() as पॉर्ट_स्वीकारा:
            पॉर्ट_स्वीकारा.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            पॉर्ट_स्वीकारा.bind(('127.0.0.1',पोर्ट_नंबर)); पॉर्ट_स्वीकारा.listen(1); पॉर्ट_स्वीकारा.settimeout(.2)
            दूरचित्रसंचार_पॉर्ट=पॉर्ट_स्वीकारा.getsockname()[1]
            if संचारजाळे_ब्रिज_प्रविष्टी and (दूरचित्रसंचार_पॉर्ट==संचिका_स्थानांतर_पोर्ट_नंबर or 50000<=दूरचित्रसंचार_पॉर्ट<=50007 or any(संचारजाळे_द्विमानजोडणी=='tcp' and होस्ट==दूरचित्रसंचार_पॉर्ट for संचारजाळे_द्विमानजोडणी,होस्ट,_ in संचारजाळे_ब्रिज_प्रविष्टी.अग्रेषण_नियम_f4578a27)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            प्रक्रिया=subprocess.Popen(आदेश(बिंदूघनता_मूल्य)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(मार्ग)]+(संचारजाळे_ब्रिज_प्रविष्टी.अग्रेषित_वितर्क() if संचारजाळे_ब्रिज_प्रविष्टी else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ब्रिज=कनेक्ट_डेस्कटॉप(प्रक्रिया); रीडर=threading.Thread(target=ब्रिज.अनुक्रमिक_आदानप्रदान,daemon=True); रीडर.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(पॉर्ट_स्वीकारा.getsockname()[1]),flush=True)
            if संचारजाळे_ब्रिज_प्रविष्टी: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(होस्ट_पत्ता,संचिका_स्थानांतर_पोर्ट_नंबर),flush=True)
            def समाप्तकरा(संकेत_संख्या,निष्पादन_फ्रेम): raise KeyboardInterrupt()
            मागील=signal.signal(signal.SIGTERM,समाप्तकरा)
            प्रक्रियाकरण_कार्य=None; खंडित=False
            try:
                while प्रक्रिया.poll() is None:
                    try: क्लायंट,_=पॉर्ट_स्वीकारा.accept()
                    except socket.timeout: continue
                    if प्रक्रियाकरण_कार्य is not None and प्रक्रियाकरण_कार्य.is_alive(): क्लायंट.close(); continue
                    if not मार्ग.exists(): क्लायंट.close(); continue
                    प्रक्रियाकरण_कार्य=threading.Thread(target=ब्रिज.क्लायंट,args=(क्लायंट,मार्ग),daemon=True); प्रक्रियाकरण_कार्य.start()
            except KeyboardInterrupt: खंडित=True
            finally:
                ब्रिज.आहे_बंदकेलेले=True
                if संचारजाळे_ब्रिज_प्रविष्टी: संचारजाळे_ब्रिज_प्रविष्टी.विराम_इव्हेंट.set()
                if प्रक्रिया.poll() is None:
                    प्रक्रिया.terminate()
                    try: प्रक्रिया.wait(timeout=5)
                    except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
                रीडर.join(timeout=2); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close(); signal.signal(signal.SIGTERM,मागील)
            if संचारजाळे_ब्रिज_प्रविष्टी and संचारजाळे_ब्रिज_प्रविष्टी.त्रुटी: raise RuntimeError('network bridge: '+संचारजाळे_ब्रिज_प्रविष्टी.त्रुटी)
            return 0 if खंडित else प्रक्रिया.returncode


if __name__=='__main__':
    from आज्ञा_कार्यवाही_करा import बिंदूघनता_वाचा
    व्याकरणविश्लेषक=argparse.ArgumentParser(description=__doc__); व्याकरणविश्लेषक.add_argument('--port',type=int,default=5902)
    व्याकरणविश्लेषक.add_argument('--resolution',type=बिंदूघनता_वाचा,default=(640,480))
    व्याकरणविश्लेषक.add_argument('--network',action='store_true'); व्याकरणविश्लेषक.add_argument('--ftp-port',type=int,default=2121)
    व्याकरणविश्लेषक.add_argument('--forward',action='append',default=[])
    वितर्क_ऍरे=व्याकरणविश्लेषक.parse_args()
    if वितर्क_ऍरे.forward and not वितर्क_ऍरे.network: व्याकरणविश्लेषक.error('--forward requires --network')
    raise SystemExit(रन_डेस्कटॉप(वितर्क_ऍरे.port,संचारजाळे=वितर्क_ऍरे.network,संचिका_स्थानांतर_पोर्ट_नंबर=वितर्क_ऍरे.ftp_port,अग्रेषण_नियम_f4578a27=वितर्क_ऍरे.forward,बिंदूघनता_मूल्य=वितर्क_ऍरे.resolution))
