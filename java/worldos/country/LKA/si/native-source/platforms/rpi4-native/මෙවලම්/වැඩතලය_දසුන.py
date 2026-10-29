#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, යතුර_අගය 입력은 자체 කර්නලය_අගය UART로 전달한다. localhost 전용, 단일 පාලකය_අගය 클라이언트.
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
from ක්_රියාත්මක_කරන්න_විධානය import විධානය
from local_input import create


def 정확한값(소켓, ප්_රමාණය):
    දත්ත = bytearray()
    while len(දත්ත) < ප්_රමාණය:
        조각 = 소켓.recv(ප්_රමාණය - len(දත්ත))
        if not 조각: raise EOFError()
        දත්ත.extend(조각)
    return bytes(දත්ත)


class යතුරුපුවරුව:
    def __init__(자신, ඊමේල්, 입력방식알림=None):
        자신.바이트전송 = ඊමේල්; 자신.විකරණකාරක_යතුර = set(); 자신.පසුරු_පුවරුව_අගය = b''
        자신.한글조합기 = create(ඊමේල්, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.මාරු_වන්න_යතුර = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ඊමේල්(자신, දත්ත):
        자신.한글조합기.조합확정()
        자신.바이트전송(දත්ත)

    def මාරු_වන්න_ප්_රකාරය(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, යතුර_සංකේතය):
        if යතුර_සංකේතය in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.විකරණකාරක_යතුර.add(යතුර_සංකේතය)
            else: 자신.විකරණකාරක_යතුර.discard(යතුර_සංකේතය)
            return
        if not 누르는중:
            자신.මාරු_වන්න_යතුර.discard(යතුර_සංකේතය)
            return
        CTRL_යතුර = bool(자신.විකරණකාරක_යතුර & {0xffe3, 0xffe4})
        SHIFT_යතුර = bool(자신.විකරණකාරක_යතුර & {0xffe1, 0xffe2})
        if CTRL_යතුර and SHIFT_යතුර and යතුර_සංකේතය in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if යතුර_සංකේතය in (32,0xff0d):
                try:
                    අගය=int(자신.유니코드입력,16)
                    if 32<=අගය<=0x10ffff and not 0xd800<=අගය<=0xdfff: 자신.ඊමේල්(chr(අගය).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif යතුර_සංකේතය==0xff1b: 자신.유니코드입력=None
            elif යතුර_සංකේතය==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif යතුර_සංකේතය<128 and chr(යතුර_සංකේතය) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(යතුර_සංකේතය)
            return
        if යතුර_සංකේතය in (0xff31,0xffc6) or යතුර_සංකේතය==32 and SHIFT_යතුර and not CTRL_යතුර:
            if යතුර_සංකේතය not in 자신.මාරු_වන්න_යතුර: 자신.මාරු_වන්න_ප්_රකාරය()
            자신.මාරු_වන්න_යතුර.add(යතුර_සංකේතය)
            return
        if යතුර_සංකේතය==0xff08 and 자신.한글여부 and not CTRL_යතුර and 자신.한글조합기.앞글자지우기(): return
        if CTRL_යතුර and SHIFT_යතුර and යතුර_සංකේතය in (ord('t'),ord('T')):
            자신.ඊමේල්(bytes([30,2,1,0,0,0,0])); return
        if යතුර_සංකේතය==0xffc3: 자신.ඊමේල්(bytes([30,2,2,0,0,0,0])); return
        if යතුර_සංකේතය==0xffc9: 자신.ඊමේල්(bytes([30,2,3,0,0,0,0])); return
        if CTRL_යතුර and SHIFT_යතුර and යතුර_සංකේතය in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ඊමේල්(자신.පසුරු_පුවරුව_අගය); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if යතුර_සංකේතය in 특수글쇠: 자신.ඊමේල්(특수글쇠[යතුර_සංකේතය]); return
        අනුලකුණ_සංකේතනය = යතුර_සංකේතය & 0xffffff if යතුර_සංකේතය & 0xff000000 == 0x01000000 else යතුර_සංකේතය
        if අනුලකුණ_සංකේතනය > 0x10ffff or 0xd800 <= අනුලකුණ_සංකේතනය <= 0xdfff or යතුර_සංකේතය >= 0xff00 and යතුර_සංකේතය < 0x1000000: return
        if CTRL_යතුර and 0x40 <= අනුලකුණ_සංකේතනය <= 0x7f: 자신.ඊමේල්(bytes([අනුලකුණ_සංකේතනය & 31])); return
        if අනුලකුණ_සංකේතනය < 32: return
        if 자신.한글여부 and 자신.විකරණකාරක_යතුර & {0xffea,0xfe03,0xff7e} and not CTRL_යතුර and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.සංග්_රහය_යතුර(chr(අනුලකුණ_සංකේතනය), altgr=True): return
        앞부분 = b'\x1b' if 자신.විකරණකාරක_යතුර & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_යතුර and not 앞부분 and 32<=අනුලකුණ_සංකේතනය<127:
            අනුලකුණ_දත්ත=chr(අනුලකුණ_සංකේතනය).upper() if SHIFT_යතුර else chr(අනුලකුණ_සංකේතනය)
            if 자신.한글조합기.සංග්_රහය_යතුර(අනුලකුණ_දත්ත): return
        자신.ඊමේල්(앞부분 + chr(අනුලකුණ_සංකේතනය).encode('utf-8'))


class සබඳින්න_වැඩතලය:
    def __init__(자신, සැකසුම):
        자신.සැකසුම=සැකසුම; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.අග්_රය=False; 자신.시작화면=False; 자신.닫힘=False

    def ඊමේල්(자신, දත්ත):
        if not දත්ත or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.සැකසුම.stdin.write(දත්ත); 자신.සැකසුම.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                දත්ත=자신.සැකසුම.stdout.read(4096)
                if not දත්ත: break
                sys.stdout.buffer.write(දත්ත); sys.stdout.buffer.flush()
                끝부분=(끝부분+දත්ත)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.අග්_රය=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ඊමේල්(b'terminal\n')
        finally: 자신.닫힘=True

    def සේවාලාභීයා(자신, සේවාලාභීයා, මාර්_ගය):
        සේවාදායකය_අගය=socket.socket(socket.AF_UNIX); සේවාදායකය_අගය.settimeout(10); සේවාලාභීයා.settimeout(10)
        යතුරුපුවරුව_පිවිසුම=යතුරුපුවරුව(자신.ඊමේල්,lambda 한글여부:자신.ඊමේල්(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            සේවාදායකය_අගය.connect(str(මාර්_ගය))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            සේවාලාභීයා.sendall(정확한값(සේවාදායකය_අගය,12))
            판번호=정확한값(සේවාලාභීයා,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            සේවාදායකය_අගය.sendall(판번호)
            개수=정확한값(සේවාදායකය_අගය,1);සේවාලාභීයා.sendall(개수+정확한값(සේවාදායකය_අගය,개수[0]))
            ආරක්ෂණය=정확한값(සේවාලාභීයා,1)
            if ආරක්ෂණය!=b'\x01': raise ValueError('unexpected security type')
            සේවාදායකය_අගය.sendall(ආරක්ෂණය)
            if 판번호==b'RFB 003.008\n':සේවාලාභීයා.sendall(정확한값(සේවාදායකය_අගය,4))
            සේවාදායකය_අගය.sendall(정확한값(සේවාලාභීයා,1))
            초기값=정확한값(සේවාදායකය_අගය,24)
            සේවාලාභීයා.sendall(초기값+정확한값(සේවාදායකය_අගය,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            සේවාලාභීයා.settimeout(None);සේවාදායකය_අගය.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ප්_රවර්ගය_අගය=정확한값(සේවාදායකය_අගය,1)[0]
                        if ප්_රවර්ගය_අගය==0:
                            머리=정확한값(සේවාදායකය_අගය,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 දුරස්ථ_අගය 포인터의 중복을 피한다.
                            සැඟවුණු_අගය=포인터지원
                            if සැඟවුණු_අගය:සේවාලාභීයා.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            සේවාලාභීයා.sendall(bytes([ප්_රවර්ගය_අගය])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(සේවාදායකය_අගය,12);가로,세로,폭,높이,සංකේතනය_අගය=struct.unpack('>HHHHi',사각형)
                                if සංකේතනය_අගය!=0:raise ValueError('unexpected framebuffer encoding: '+str(සංකේතනය_අගය))
                                සේවාලාභීයා.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    දත්ත=정확한값(සේවාදායකය_අගය,min(남음,65536));සේවාලාභීයා.sendall(දත්ත);남음-=len(දත්ත)
                        elif ප්_රවර්ගය_අගය==1:
                            머리=정확한값(සේවාදායකය_අගය,5);개수=struct.unpack('>H',머리[3:])[0]
                            සේවාලාභීයා.sendall(bytes([ප්_රවර්ගය_අගය])+머리+정확한값(සේවාදායකය_අගය,개수*6))
                        elif ප්_රවර්ගය_අගය==2:සේවාලාභීයා.sendall(bytes([ප්_රවර්ගය_අගය]))
                        elif ප්_රවර්ගය_අගය==3:
                            머리=정확한값(සේවාදායකය_අගය,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            සේවාලාභීයා.sendall(bytes([ප්_රවර්ගය_අගය])+머리+정확한값(සේවාදායකය_අගය,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ප්_රවර්ගය_අගය))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:සේවාලාභීයා.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ප්_රවර්ගය_අගය=정확한값(සේවාලාභීයා,1)[0]
                if ප්_රවර්ගය_අගය==4:
                    කඳ_පෙළ=정확한값(සේවාලාභීයා,7); යතුරුපුවරුව_පිවිසුම.누름값(කඳ_පෙළ[0]!=0,struct.unpack('>I',කඳ_පෙළ[3:])[0]); continue
                if ප්_රවර්ගය_අගය==255:
                    කඳ_පෙළ=정확한값(සේවාලාභීයා,11)
                    if කඳ_පෙළ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    යතුරුපුවරුව_පිවිසුම.누름값(struct.unpack('>H',කඳ_පෙළ[1:3])[0]!=0,struct.unpack('>I',කඳ_පෙළ[3:7])[0]); continue
                if ප්_රවර්ගය_අගය==5:
                    කඳ_පෙළ=정확한값(සේවාලාභීයා,5); 단추들,x_ඛණ්ඩාංකය,세로좌표=struct.unpack('>BHH',කඳ_පෙළ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: යතුරුපුවරුව_පිවිසුම.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_ඛණ්ඩාංකය<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.ඊමේල්(bytes([ord('1')+색인]))
                    else: 자신.ඊමේල්(bytes([30,1,단추들,x_ඛණ්ඩාංකය&255,x_ඛණ්ඩාංකය>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if ප්_රවර්ගය_අගය==6:
                    කඳ_පෙළ=정확한값(සේවාලාභීයා,7); දිග_අගය=struct.unpack('>i',කඳ_පෙළ[3:])[0]
                    if abs(දිග_අගය)>65536: raise ValueError('clipboard too large')
                    පෙළ=정확한값(සේවාලාභීයා,abs(දිග_අගය))
                    if දිග_අගය>=0:
                        try: යතුරුපුවරුව_පිවිසුම.පසුරු_පුවරුව_අගය=පෙළ.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: යතුරුපුවරුව_පිවිසුම.පසුරු_පුවරුව_අගය=පෙළ.decode('latin-1').encode('utf-8')
                        යතුරුපුවරුව_පිවිසුම.පසුරු_පුවරුව_අගය=යතුරුපුවරුව_පිවිසුම.පසුරු_පුවරුව_අගය[:65536].decode('utf-8','ignore').encode('utf-8')
                    සේවාදායකය_අගය.sendall(bytes([ප්_රවර්ගය_අගය])+කඳ_පෙළ+පෙළ); continue
                if ප්_රවර්ගය_අගය==0:
                    කඳ_පෙළ=정확한값(සේවාලාභීයා,19)
                    if කඳ_පෙළ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=කඳ_පෙළ[3]//8
                elif ප්_රවර්ගය_අගය==2:
                    කඳ_පෙළ=정확한값(සේවාලාභීයා,3); 항목수=struct.unpack('>H',කඳ_පෙළ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(සේවාලාභීයා,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 පෙරනිමි_අගය Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    කඳ_පෙළ=struct.pack('>BHi',0,1,0)
                elif ප්_රවර්ගය_අගය in (3,150): කඳ_පෙළ=정확한값(සේවාලාභීයා,9)
                elif ප්_රවර්ගය_අගය==248:
                    කඳ_පෙළ=정확한값(සේවාලාභීයා,8)
                    if කඳ_පෙළ[7]>64: raise ValueError('fence too large')
                    කඳ_පෙළ+=정확한값(සේවාලාභීයා,කඳ_පෙළ[7])
                elif ප්_රවර්ගය_අගය==250: කඳ_පෙළ=정확한값(සේවාලාභීයා,3)
                elif ප්_රවර්ගය_අගය==251:
                    කඳ_පෙළ=정확한값(සේවාලාභීයා,7)
                    if කඳ_පෙළ[5]>16: raise ValueError('too many screens')
                    කඳ_පෙළ+=정확한값(සේවාලාභීයා,කඳ_පෙළ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ප්_රවර්ගය_අගය))
                සේවාදායකය_අගය.sendall(bytes([ප්_රවර්ගය_අගය])+කඳ_පෙළ)
        except (OSError,EOFError,ValueError) as දෝෂය:
            if str(දෝෂය): print('VNC client:',දෝෂය,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (සේවාලාභීයා,සේවාදායකය_අගය):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ධාවනය_කරන්න_වැඩතලය(접속번호=5902, ජාලය=False, 파일전송접속번호=2121, 전달규칙들=(), විභේදනය_අගය=(640, 480), අමුත්තා_යොමුව=None, ධාරකය_යොමුව='127.0.0.1'):
    with ExitStack() as සම්පත්, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        ජාලය_පාලම_පිවිසුම = None
        if ජාලය:
            from ජාලය_පාලම import ජාලය_පාලම
            ජාලය_පාලම_පිවිසුම = සම්පත්.enter_context(ජාලය_පාලම(파일전송접속번호, 전달규칙들, අමුත්තා_යොමුව=අමුත්තා_යොමුව, ධාරකය_යොමුව=ධාරකය_යොමුව))
        මාර්_ගය=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if ජාලය_පාලම_පිවිසුම and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ධාරකය==원격화면접속번호 for 통신규약,ධාරකය,_ in ජාලය_පාලම_පිවිසුම.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            සැකසුම=subprocess.Popen(විධානය(විභේදනය_අගය)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(මාර්_ගය)]+(ජාලය_පාලම_පිවිසුම.전달인수() if ජාලය_පාලම_පිවිසුම else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            පාලම=සබඳින්න_වැඩතලය(සැකසුම); පාඨක=threading.Thread(target=පාලම.직렬입출력,daemon=True); පාඨක.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if ජාලය_පාලම_පිවිසුම: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ධාරකය_යොමුව,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while සැකසුම.poll() is None:
                    try: සේවාලාභීයා,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): සේවාලාභීයා.close(); continue
                    if not මාර්_ගය.exists(): සේවාලාභීයා.close(); continue
                    처리작업=threading.Thread(target=පාලම.සේවාලාභීයා,args=(සේවාලාභීයා,මාර්_ගය),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                පාලම.닫힘=True
                if ජාලය_පාලම_පිවිසුම: ජාලය_පාලම_පිවිසුම.විරාම_කරන්න_සිද්ධිය.set()
                if සැකසුම.poll() is None:
                    සැකසුම.terminate()
                    try: සැකසුම.wait(timeout=5)
                    except subprocess.TimeoutExpired: සැකසුම.kill(); සැකසුම.wait()
                පාඨක.join(timeout=2); සැකසුම.stdin.close(); සැකසුම.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if ජාලය_පාලම_පිවිසුම and ජාලය_පාලම_පිවිසුම.දෝෂය: raise RuntimeError('network bridge: '+ජාලය_පාලම_පිවිසුම.දෝෂය)
            return 0 if 가로채기됨 else සැකසුම.returncode


if __name__=='__main__':
    from ක්_රියාත්මක_කරන්න_විධානය import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    විස්තාරකය_ආරා_ව=인수해석기.parse_args()
    if විස්තාරකය_ආරා_ව.forward and not විස්තාරකය_ආරා_ව.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ධාවනය_කරන්න_වැඩතලය(විස්තාරකය_ආරා_ව.port,ජාලය=විස්තාරකය_ආරා_ව.network,파일전송접속번호=විස්තාරකය_ආරා_ව.ftp_port,전달규칙들=විස්තාරකය_ආරා_ව.forward,විභේදනය_අගය=විස්තාරකය_ආරා_ව.resolution))
