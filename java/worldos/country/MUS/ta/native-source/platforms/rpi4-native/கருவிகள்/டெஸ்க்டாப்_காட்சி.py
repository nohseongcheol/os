#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, சாவி_மதிப்பு 입력은 자체 கரு_மதிப்பு UART로 전달한다. localhost 전용, 단일 கட்டுப்பாடு_மதிப்பு 클라이언트.
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
from இயக்கு_கட்டளை import கட்டளை
from local_input import create


def 정확한값(소켓, அளவு):
    தரவு = bytearray()
    while len(தரவு) < அளவு:
        조각 = 소켓.recv(அளவு - len(தரவு))
        if not 조각: raise EOFError()
        தரவு.extend(조각)
    return bytes(தரவு)


class விசைப்பலகை:
    def __init__(자신, அனுப்பு, 입력방식알림=None):
        자신.바이트전송 = அனுப்பு; 자신.நிலைமாற்று_விசை = set(); 자신.நகலகம்_மதிப்பு = b''
        자신.한글조합기 = create(அனுப்பு, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.சுவிட்ச்_சாவி = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def அனுப்பு(자신, தரவு):
        자신.한글조합기.조합확정()
        자신.바이트전송(தரவு)

    def சுவிட்ச்_பயன்முறை(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, சாவி_சின்னம்):
        if சாவி_சின்னம் in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.நிலைமாற்று_விசை.add(சாவி_சின்னம்)
            else: 자신.நிலைமாற்று_விசை.discard(சாவி_சின்னம்)
            return
        if not 누르는중:
            자신.சுவிட்ச்_சாவி.discard(சாவி_சின்னம்)
            return
        CTRL_விசை = bool(자신.நிலைமாற்று_விசை & {0xffe3, 0xffe4})
        SHIFT_விசை = bool(자신.நிலைமாற்று_விசை & {0xffe1, 0xffe2})
        if CTRL_விசை and SHIFT_விசை and சாவி_சின்னம் in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if சாவி_சின்னம் in (32,0xff0d):
                try:
                    மதிப்பு=int(자신.유니코드입력,16)
                    if 32<=மதிப்பு<=0x10ffff and not 0xd800<=மதிப்பு<=0xdfff: 자신.அனுப்பு(chr(மதிப்பு).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif சாவி_சின்னம்==0xff1b: 자신.유니코드입력=None
            elif சாவி_சின்னம்==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif சாவி_சின்னம்<128 and chr(சாவி_சின்னம்) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(சாவி_சின்னம்)
            return
        if சாவி_சின்னம் in (0xff31,0xffc6) or சாவி_சின்னம்==32 and SHIFT_விசை and not CTRL_விசை:
            if சாவி_சின்னம் not in 자신.சுவிட்ச்_சாவி: 자신.சுவிட்ச்_பயன்முறை()
            자신.சுவிட்ச்_சாவி.add(சாவி_சின்னம்)
            return
        if சாவி_சின்னம்==0xff08 and 자신.한글여부 and not CTRL_விசை and 자신.한글조합기.앞글자지우기(): return
        if CTRL_விசை and SHIFT_விசை and சாவி_சின்னம் in (ord('t'),ord('T')):
            자신.அனுப்பு(bytes([30,2,1,0,0,0,0])); return
        if சாவி_சின்னம்==0xffc3: 자신.அனுப்பு(bytes([30,2,2,0,0,0,0])); return
        if சாவி_சின்னம்==0xffc9: 자신.அனுப்பு(bytes([30,2,3,0,0,0,0])); return
        if CTRL_விசை and SHIFT_விசை and சாவி_சின்னம் in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.அனுப்பு(자신.நகலகம்_மதிப்பு); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if சாவி_சின்னம் in 특수글쇠: 자신.அனுப்பு(특수글쇠[சாவி_சின்னம்]); return
        எழுத்துக்குறி_குறியீட்டு_முறை = சாவி_சின்னம் & 0xffffff if சாவி_சின்னம் & 0xff000000 == 0x01000000 else சாவி_சின்னம்
        if எழுத்துக்குறி_குறியீட்டு_முறை > 0x10ffff or 0xd800 <= எழுத்துக்குறி_குறியீட்டு_முறை <= 0xdfff or சாவி_சின்னம் >= 0xff00 and சாவி_சின்னம் < 0x1000000: return
        if CTRL_விசை and 0x40 <= எழுத்துக்குறி_குறியீட்டு_முறை <= 0x7f: 자신.அனுப்பு(bytes([எழுத்துக்குறி_குறியீட்டு_முறை & 31])); return
        if எழுத்துக்குறி_குறியீட்டு_முறை < 32: return
        if 자신.한글여부 and 자신.நிலைமாற்று_விசை & {0xffea,0xfe03,0xff7e} and not CTRL_விசை and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ஃபீடு_சாவி(chr(எழுத்துக்குறி_குறியீட்டு_முறை), altgr=True): return
        앞부분 = b'\x1b' if 자신.நிலைமாற்று_விசை & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_விசை and not 앞부분 and 32<=எழுத்துக்குறி_குறியீட்டு_முறை<127:
            எழுத்துருத்_தரவு=chr(எழுத்துக்குறி_குறியீட்டு_முறை).upper() if SHIFT_விசை else chr(எழுத்துக்குறி_குறியீட்டு_முறை)
            if 자신.한글조합기.ஃபீடு_சாவி(எழுத்துருத்_தரவு): return
        자신.அனுப்பு(앞부분 + chr(எழுத்துக்குறி_குறியீட்டு_முறை).encode('utf-8'))


class இணை_டெஸ்க்டாப்:
    def __init__(자신, செயல்பாடு):
        자신.செயல்பாடு=செயல்பாடு; 자신.பூட்டு_மதிப்பு=threading.Lock(); 자신.준비완료=False; 자신.கட்டளை_விளக்கி=False; 자신.시작화면=False; 자신.닫힘=False

    def அனுப்பு(자신, தரவு):
        if not தரவு or 자신.닫힘: return
        with 자신.பூட்டு_மதிப்பு:
            try: 자신.செயல்பாடு.stdin.write(தரவு); 자신.செயல்பாடு.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                தரவு=자신.செயல்பாடு.stdout.read(4096)
                if not தரவு: break
                sys.stdout.buffer.write(தரவு); sys.stdout.buffer.flush()
                끝부분=(끝부분+தரவு)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.கட்டளை_விளக்கி=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.அனுப்பு(b'terminal\n')
        finally: 자신.닫힘=True

    def பயனகம்(자신, பயனகம், பாதை_2):
        சேவையகம்_மதிப்பு=socket.socket(socket.AF_UNIX); சேவையகம்_மதிப்பு.settimeout(10); பயனகம்.settimeout(10)
        விசைப்பலகை_உள்ளீடு=விசைப்பலகை(자신.அனுப்பு,lambda 한글여부:자신.அனுப்பு(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            சேவையகம்_மதிப்பு.connect(str(பாதை_2))
            # 초기 협상은 순서대로 끝낸다. 이후 வெளியீட்டு_இடம் 가닥만 클라이언트에 쓴다.
            பயனகம்.sendall(정확한값(சேவையகம்_மதிப்பு,12))
            பதிப்புரு_எண்=정확한값(பயனகம்,12)
            if பதிப்புரு_எண் not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            சேவையகம்_மதிப்பு.sendall(பதிப்புரு_எண்)
            개수=정확한값(சேவையகம்_மதிப்பு,1);பயனகம்.sendall(개수+정확한값(சேவையகம்_மதிப்பு,개수[0]))
            பாதுகாப்பு=정확한값(பயனகம்,1)
            if பாதுகாப்பு!=b'\x01': raise ValueError('unexpected security type')
            சேவையகம்_மதிப்பு.sendall(பாதுகாப்பு)
            if பதிப்புரு_எண்==b'RFB 003.008\n':பயனகம்.sendall(정확한값(சேவையகம்_மதிப்பு,4))
            சேவையகம்_மதிப்பு.sendall(정확한값(பயனகம்,1))
            초기값=정확한값(சேவையகம்_மதிப்பு,24)
            பயனகம்.sendall(초기값+정확한값(சேவையகம்_மதிப்பு,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            பயனகம்.settimeout(None);சேவையகம்_மதிப்பு.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        வகை_மதிப்பு_4b6d6445=정확한값(சேவையகம்_மதிப்பு,1)[0]
                        if வகை_மதிப்பு_4b6d6445==0:
                            머리=정확한값(சேவையகம்_மதிப்பு,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 தொலைநிலை_மதிப்பு 포인터의 중복을 피한다.
                            மறைந்த_மதிப்பு=포인터지원
                            if மறைந்த_மதிப்பு:பயனகம்.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            பயனகம்.sendall(bytes([வகை_மதிப்பு_4b6d6445])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(சேவையகம்_மதிப்பு,12);가로,வெர்டிகல்_நிலை,폭,높이,குறியீட்டு_முறை_மதிப்பு=struct.unpack('>HHHHi',사각형)
                                if குறியீட்டு_முறை_மதிப்பு!=0:raise ValueError('unexpected framebuffer encoding: '+str(குறியீட்டு_முறை_மதிப்பு))
                                பயனகம்.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    தரவு=정확한값(சேவையகம்_மதிப்பு,min(남음,65536));பயனகம்.sendall(தரவு);남음-=len(தரவு)
                        elif வகை_மதிப்பு_4b6d6445==1:
                            머리=정확한값(சேவையகம்_மதிப்பு,5);개수=struct.unpack('>H',머리[3:])[0]
                            பயனகம்.sendall(bytes([வகை_மதிப்பு_4b6d6445])+머리+정확한값(சேவையகம்_மதிப்பு,개수*6))
                        elif வகை_மதிப்பு_4b6d6445==2:பயனகம்.sendall(bytes([வகை_மதிப்பு_4b6d6445]))
                        elif வகை_மதிப்பு_4b6d6445==3:
                            머리=정확한값(சேவையகம்_மதிப்பு,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            பயனகம்.sendall(bytes([வகை_மதிப்பு_4b6d6445])+머리+정확한값(சேவையகம்_மதிப்பு,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(வகை_மதிப்பு_4b6d6445))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:பயனகம்.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                வகை_மதிப்பு_4b6d6445=정확한값(பயனகம்,1)[0]
                if வகை_மதிப்பு_4b6d6445==4:
                    தகவல்_உரை=정확한값(பயனகம்,7); விசைப்பலகை_உள்ளீடு.누름값(தகவல்_உரை[0]!=0,struct.unpack('>I',தகவல்_உரை[3:])[0]); continue
                if வகை_மதிப்பு_4b6d6445==255:
                    தகவல்_உரை=정확한값(பயனகம்,11)
                    if தகவல்_உரை[0]!=0: raise ValueError('unsupported QEMU input extension')
                    விசைப்பலகை_உள்ளீடு.누름값(struct.unpack('>H',தகவல்_உரை[1:3])[0]!=0,struct.unpack('>I',தகவல்_உரை[3:7])[0]); continue
                if வகை_மதிப்பு_4b6d6445==5:
                    தகவல்_உரை=정확한값(பயனகம்,5); 단추들,x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு=struct.unpack('>BHH',தகவல்_உரை)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: விசைப்பலகை_உள்ளீடு.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_ஒத்ததரமுள்ளது<576 and 112<=Y_பொத்தான்_அச்சுத்_தொகுப்பு<372:
                        தேடுதல்_அடைவு=(Y_பொத்தான்_அச்சுத்_தொகுப்பு-112)//52
                        if (Y_பொத்தான்_அச்சுத்_தொகுப்பு-112)%52<40 and தேடுதல்_அடைவு<5: 자신.அனுப்பு(bytes([ord('1')+தேடுதல்_அடைவு]))
                    else: 자신.அனுப்பு(bytes([30,1,단추들,x_ஒத்ததரமுள்ளது&255,x_ஒத்ததரமுள்ளது>>8,Y_பொத்தான்_அச்சுத்_தொகுப்பு&255,Y_பொத்தான்_அச்சுத்_தொகுப்பு>>8]))
                    continue
                if வகை_மதிப்பு_4b6d6445==6:
                    தகவல்_உரை=정확한값(பயனகம்,7); நீளம்_மதிப்பு=struct.unpack('>i',தகவல்_உரை[3:])[0]
                    if abs(நீளம்_மதிப்பு)>65536: raise ValueError('clipboard too large')
                    உரை=정확한값(பயனகம்,abs(நீளம்_மதிப்பு))
                    if நீளம்_மதிப்பு>=0:
                        try: விசைப்பலகை_உள்ளீடு.நகலகம்_மதிப்பு=உரை.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: விசைப்பலகை_உள்ளீடு.நகலகம்_மதிப்பு=உரை.decode('latin-1').encode('utf-8')
                        விசைப்பலகை_உள்ளீடு.நகலகம்_மதிப்பு=விசைப்பலகை_உள்ளீடு.நகலகம்_மதிப்பு[:65536].decode('utf-8','ignore').encode('utf-8')
                    சேவையகம்_மதிப்பு.sendall(bytes([வகை_மதிப்பு_4b6d6445])+தகவல்_உரை+உரை); continue
                if வகை_மதிப்பு_4b6d6445==0:
                    தகவல்_உரை=정확한값(பயனகம்,19)
                    if தகவல்_உரை[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=தகவல்_உரை[3]//8
                elif வகை_மதிப்பு_4b6d6445==2:
                    தகவல்_உரை=정확한값(பயனகம்,3); 항목수=struct.unpack('>H',தகவல்_உரை[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(பயனகம்,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 இயல்புநிலை_மதிப்பு Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    தகவல்_உரை=struct.pack('>BHi',0,1,0)
                elif வகை_மதிப்பு_4b6d6445 in (3,150): தகவல்_உரை=정확한값(பயனகம்,9)
                elif வகை_மதிப்பு_4b6d6445==248:
                    தகவல்_உரை=정확한값(பயனகம்,8)
                    if தகவல்_உரை[7]>64: raise ValueError('fence too large')
                    தகவல்_உரை+=정확한값(பயனகம்,தகவல்_உரை[7])
                elif வகை_மதிப்பு_4b6d6445==250: தகவல்_உரை=정확한값(பயனகம்,3)
                elif வகை_மதிப்பு_4b6d6445==251:
                    தகவல்_உரை=정확한값(பயனகம்,7)
                    if தகவல்_உரை[5]>16: raise ValueError('too many screens')
                    தகவல்_உரை+=정확한값(பயனகம்,தகவல்_உரை[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(வகை_மதிப்பு_4b6d6445))
                சேவையகம்_மதிப்பு.sendall(bytes([வகை_மதிப்பு_4b6d6445])+தகவல்_உரை)
        except (OSError,EOFError,ValueError) as பிழை:
            if str(பிழை): print('VNC client:',பிழை,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (பயனகம்,சேவையகம்_மதிப்பு):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def இயக்கு_டெஸ்க்டாப்(முனைய_எண்=5902, பிணையம்=False, கோப்பு_இடமாற்று_முனைய_எண்=2121, 전달규칙들=(), தெளிவுத்திறன்_மதிப்பு=(640, 480), விருந்தினர்_முகவரி=None, ஓம்பு_முகவரி='127.0.0.1'):
    with ExitStack() as ஆதாரங்கள, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        பிணையம்_பிரிட்ஜ்_உள்ளீடு = None
        if பிணையம்:
            from பிணையம்_பிரிட்ஜ் import பிணையம்_பிரிட்ஜ்
            பிணையம்_பிரிட்ஜ்_உள்ளீடு = ஆதாரங்கள.enter_context(பிணையம்_பிரிட்ஜ்(கோப்பு_இடமாற்று_முனைய_எண், 전달규칙들, விருந்தினர்_முகவரி=விருந்தினர்_முகவரி, ஓம்பு_முகவரி=ஓம்பு_முகவரி))
        பாதை_2=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',முனைய_எண்)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if பிணையம்_பிரிட்ஜ்_உள்ளீடு and (원격화면접속번호==கோப்பு_இடமாற்று_முனைய_எண் or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ஓம்பு==원격화면접속번호 for 통신규약,ஓம்பு,_ in பிணையம்_பிரிட்ஜ்_உள்ளீடு.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            செயல்பாடு=subprocess.Popen(கட்டளை(தெளிவுத்திறன்_மதிப்பு)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(பாதை_2)]+(பிணையம்_பிரிட்ஜ்_உள்ளீடு.전달인수() if பிணையம்_பிரிட்ஜ்_உள்ளீடு else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            பிரிட்ஜ்=இணை_டெஸ்க்டாப்(செயல்பாடு); படிப்பவர்=threading.Thread(target=பிரிட்ஜ்.직렬입출력,daemon=True); படிப்பவர்.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if பிணையம்_பிரிட்ஜ்_உள்ளீடு: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ஓம்பு_முகவரி,கோப்பு_இடமாற்று_முனைய_எண்),flush=True)
            def முடி(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,முடி)
            처리작업=None; 가로채기됨=False
            try:
                while செயல்பாடு.poll() is None:
                    try: பயனகம்,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): பயனகம்.close(); continue
                    if not பாதை_2.exists(): பயனகம்.close(); continue
                    처리작업=threading.Thread(target=பிரிட்ஜ்.பயனகம்,args=(பயனகம்,பாதை_2),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                பிரிட்ஜ்.닫힘=True
                if பிணையம்_பிரிட்ஜ்_உள்ளீடு: பிணையம்_பிரிட்ஜ்_உள்ளீடு.நிற்க_நிகழ்வு.set()
                if செயல்பாடு.poll() is None:
                    செயல்பாடு.terminate()
                    try: செயல்பாடு.wait(timeout=5)
                    except subprocess.TimeoutExpired: செயல்பாடு.kill(); செயல்பாடு.wait()
                படிப்பவர்.join(timeout=2); செயல்பாடு.stdin.close(); செயல்பாடு.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if பிணையம்_பிரிட்ஜ்_உள்ளீடு and பிணையம்_பிரிட்ஜ்_உள்ளீடு.பிழை: raise RuntimeError('network bridge: '+பிணையம்_பிரிட்ஜ்_உள்ளீடு.பிழை)
            return 0 if 가로채기됨 else செயல்பாடு.returncode


if __name__=='__main__':
    from இயக்கு_கட்டளை import 해상도읽기
    பார்சர்=argparse.ArgumentParser(description=__doc__); பார்சர்.add_argument('--port',type=int,default=5902)
    பார்சர்.add_argument('--resolution',type=해상도읽기,default=(640,480))
    பார்சர்.add_argument('--network',action='store_true'); பார்சர்.add_argument('--ftp-port',type=int,default=2121)
    பார்சர்.add_argument('--forward',action='append',default=[])
    மதிப்புரு_கோவை=பார்சர்.parse_args()
    if மதிப்புரு_கோவை.forward and not மதிப்புரு_கோவை.network: பார்சர்.error('--forward requires --network')
    raise SystemExit(இயக்கு_டெஸ்க்டாப்(மதிப்புரு_கோவை.port,பிணையம்=மதிப்புரு_கோவை.network,கோப்பு_இடமாற்று_முனைய_எண்=மதிப்புரு_கோவை.ftp_port,전달규칙들=மதிப்புரு_கோவை.forward,தெளிவுத்திறன்_மதிப்பு=மதிப்புரு_கோவை.resolution))
