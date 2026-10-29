#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, key_VALUE 입력은 자체 kernel_VALUE UART로 전달한다. localhost 전용, 단일 control_VALUE 클라이언트.
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
from Mag_execute_utos import utos
from local_input import create


def EXACT_VALUE(소켓, sukat_82232621):
    data = bytearray()
    while len(data) < sukat_82232621:
        조각 = 소켓.recv(sukat_82232621 - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class keyboard:
    def __init__(자신, i_email, 입력방식알림=None):
        자신.바이트전송 = i_email; 자신.pambagong_key = set(); 자신.clipboard_VALUE = b''
        자신.한글조합기 = create(i_email, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_key = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def i_email(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, key_simbolo):
        if key_simbolo in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.pambagong_key.add(key_simbolo)
            else: 자신.pambagong_key.discard(key_simbolo)
            return
        if not 누르는중:
            자신.SWITCH_key.discard(key_simbolo)
            return
        CTRL = bool(자신.pambagong_key & {0xffe3, 0xffe4})
        SHIFT_key = bool(자신.pambagong_key & {0xffe1, 0xffe2})
        if CTRL and SHIFT_key and key_simbolo in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if key_simbolo in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.i_email(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif key_simbolo==0xff1b: 자신.유니코드입력=None
            elif key_simbolo==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif key_simbolo<128 and chr(key_simbolo) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(key_simbolo)
            return
        if key_simbolo in (0xff31,0xffc6) or key_simbolo==32 and SHIFT_key and not CTRL:
            if key_simbolo not in 자신.SWITCH_key: 자신.SWITCH_MODE()
            자신.SWITCH_key.add(key_simbolo)
            return
        if key_simbolo==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_key and key_simbolo in (ord('t'),ord('T')):
            자신.i_email(bytes([30,2,1,0,0,0,0])); return
        if key_simbolo==0xffc3: 자신.i_email(bytes([30,2,2,0,0,0,0])); return
        if key_simbolo==0xffc9: 자신.i_email(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_key and key_simbolo in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.i_email(자신.clipboard_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if key_simbolo in 특수글쇠: 자신.i_email(특수글쇠[key_simbolo]); return
        karakter_pag_encode = key_simbolo & 0xffffff if key_simbolo & 0xff000000 == 0x01000000 else key_simbolo
        if karakter_pag_encode > 0x10ffff or 0xd800 <= karakter_pag_encode <= 0xdfff or key_simbolo >= 0xff00 and key_simbolo < 0x1000000: return
        if CTRL and 0x40 <= karakter_pag_encode <= 0x7f: 자신.i_email(bytes([karakter_pag_encode & 31])); return
        if karakter_pag_encode < 32: return
        if 자신.한글여부 and 자신.pambagong_key & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_key(chr(karakter_pag_encode), altgr=True): return
        앞부분 = b'\x1b' if 자신.pambagong_key & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=karakter_pag_encode<127:
            karakter_data=chr(karakter_pag_encode).upper() if SHIFT_key else chr(karakter_pag_encode)
            if 자신.한글조합기.feed_key(karakter_data): return
        자신.i_email(앞부분 + chr(karakter_pag_encode).encode('utf-8'))


class CONNECT_desktop:
    def __init__(자신, Proseso):
        자신.Proseso=Proseso; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def i_email(자신, data):
        if not data or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Proseso.stdin.write(data); 자신.Proseso.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Proseso.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.i_email(b'terminal\n')
        finally: 자신.닫힘=True

    def client(자신, client, path):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); client.settimeout(10)
        keyboard_pagpasok=keyboard(자신.i_email,lambda 한글여부:자신.i_email(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(path))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            client.sendall(EXACT_VALUE(server_VALUE,12))
            판번호=EXACT_VALUE(client,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(판번호)
            item_COUNT=EXACT_VALUE(server_VALUE,1);client.sendall(item_COUNT+EXACT_VALUE(server_VALUE,item_COUNT[0]))
            Seguridad=EXACT_VALUE(client,1)
            if Seguridad!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Seguridad)
            if 판번호==b'RFB 003.008\n':client.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(client,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            client.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            client.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        kategorya_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if kategorya_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);pagpasok_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 malayuan_VALUE 포인터의 중복을 피한다.
                            nakatago_VALUE=포인터지원
                            if nakatago_VALUE:client.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            client.sendall(bytes([kategorya_VALUE])+머리)
                            for _ in range(pagpasok_COUNT):
                                사각형=EXACT_VALUE(server_VALUE,12);가로,archive_posisyon,폭,높이,pag_encode_VALUE=struct.unpack('>HHHHi',사각형)
                                if pag_encode_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(pag_encode_VALUE))
                                client.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EXACT_VALUE(server_VALUE,min(남음,65536));client.sendall(data);남음-=len(data)
                        elif kategorya_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);item_COUNT=struct.unpack('>H',머리[3:])[0]
                            client.sendall(bytes([kategorya_VALUE])+머리+EXACT_VALUE(server_VALUE,item_COUNT*6))
                        elif kategorya_VALUE==2:client.sendall(bytes([kategorya_VALUE]))
                        elif kategorya_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);item_COUNT=struct.unpack('>I',머리[3:])[0]
                            if item_COUNT>1048576:raise ValueError('server clipboard too large')
                            client.sendall(bytes([kategorya_VALUE])+머리+EXACT_VALUE(server_VALUE,item_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(kategorya_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:client.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                kategorya_VALUE=EXACT_VALUE(client,1)[0]
                if kategorya_VALUE==4:
                    teksto_ng_nilalaman=EXACT_VALUE(client,7); keyboard_pagpasok.누름값(teksto_ng_nilalaman[0]!=0,struct.unpack('>I',teksto_ng_nilalaman[3:])[0]); continue
                if kategorya_VALUE==255:
                    teksto_ng_nilalaman=EXACT_VALUE(client,11)
                    if teksto_ng_nilalaman[0]!=0: raise ValueError('unsupported QEMU input extension')
                    keyboard_pagpasok.누름값(struct.unpack('>H',teksto_ng_nilalaman[1:3])[0]!=0,struct.unpack('>I',teksto_ng_nilalaman[3:7])[0]); continue
                if kategorya_VALUE==5:
                    teksto_ng_nilalaman=EXACT_VALUE(client,5); 단추들,x_coordinate,Y_button_coordinate=struct.unpack('>BHH',teksto_ng_nilalaman)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: keyboard_pagpasok.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_coordinate<576 and 112<=Y_button_coordinate<372:
                        LOOKUP_INDEX=(Y_button_coordinate-112)//52
                        if (Y_button_coordinate-112)%52<40 and LOOKUP_INDEX<5: 자신.i_email(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.i_email(bytes([30,1,단추들,x_coordinate&255,x_coordinate>>8,Y_button_coordinate&255,Y_button_coordinate>>8]))
                    continue
                if kategorya_VALUE==6:
                    teksto_ng_nilalaman=EXACT_VALUE(client,7); haba_VALUE=struct.unpack('>i',teksto_ng_nilalaman[3:])[0]
                    if abs(haba_VALUE)>65536: raise ValueError('clipboard too large')
                    SMS=EXACT_VALUE(client,abs(haba_VALUE))
                    if haba_VALUE>=0:
                        try: keyboard_pagpasok.clipboard_VALUE=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: keyboard_pagpasok.clipboard_VALUE=SMS.decode('latin-1').encode('utf-8')
                        keyboard_pagpasok.clipboard_VALUE=keyboard_pagpasok.clipboard_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([kategorya_VALUE])+teksto_ng_nilalaman+SMS); continue
                if kategorya_VALUE==0:
                    teksto_ng_nilalaman=EXACT_VALUE(client,19)
                    if teksto_ng_nilalaman[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=teksto_ng_nilalaman[3]//8
                elif kategorya_VALUE==2:
                    teksto_ng_nilalaman=EXACT_VALUE(client,3); pagpasok_COUNT=struct.unpack('>H',teksto_ng_nilalaman[1:])[0]
                    if pagpasok_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(pagpasok_COUNT)+'i',EXACT_VALUE(client,pagpasok_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 value_ng_default Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    teksto_ng_nilalaman=struct.pack('>BHi',0,1,0)
                elif kategorya_VALUE in (3,150): teksto_ng_nilalaman=EXACT_VALUE(client,9)
                elif kategorya_VALUE==248:
                    teksto_ng_nilalaman=EXACT_VALUE(client,8)
                    if teksto_ng_nilalaman[7]>64: raise ValueError('fence too large')
                    teksto_ng_nilalaman+=EXACT_VALUE(client,teksto_ng_nilalaman[7])
                elif kategorya_VALUE==250: teksto_ng_nilalaman=EXACT_VALUE(client,3)
                elif kategorya_VALUE==251:
                    teksto_ng_nilalaman=EXACT_VALUE(client,7)
                    if teksto_ng_nilalaman[5]>16: raise ValueError('too many screens')
                    teksto_ng_nilalaman+=EXACT_VALUE(client,teksto_ng_nilalaman[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kategorya_VALUE))
                server_VALUE.sendall(bytes([kategorya_VALUE])+teksto_ng_nilalaman)
        except (OSError,EOFError,ValueError) as error:
            if str(error): print('VNC client:',error,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (client,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def run_desktop(numero_ng_port=5902, Network=False, file_lipat_numero_ng_port=2121, 전달규칙들=(), resolution_VALUE=(640, 480), bisita_email=None, host_email='127.0.0.1'):
    with ExitStack() as Resources, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Network_bridge_pagpasok = None
        if Network:
            from Network_bridge import Network_bridge
            Network_bridge_pagpasok = Resources.enter_context(Network_bridge(file_lipat_numero_ng_port, 전달규칙들, bisita_email=bisita_email, host_email=host_email))
        path=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',numero_ng_port)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Network_bridge_pagpasok and (원격화면접속번호==file_lipat_numero_ng_port or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and host==원격화면접속번호 for 통신규약,host,_ in Network_bridge_pagpasok.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proseso=subprocess.Popen(utos(resolution_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(path)]+(Network_bridge_pagpasok.전달인수() if Network_bridge_pagpasok else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            bridge=CONNECT_desktop(Proseso); Tagabasa=threading.Thread(target=bridge.직렬입출력,daemon=True); Tagabasa.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Network_bridge_pagpasok: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(host_email,file_lipat_numero_ng_port),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Proseso.poll() is None:
                    try: client,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): client.close(); continue
                    if not path.exists(): client.close(); continue
                    처리작업=threading.Thread(target=bridge.client,args=(client,path),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                bridge.닫힘=True
                if Network_bridge_pagpasok: Network_bridge_pagpasok.panadaliang_ihinto_kaganapan.set()
                if Proseso.poll() is None:
                    Proseso.terminate()
                    try: Proseso.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proseso.kill(); Proseso.wait()
                Tagabasa.join(timeout=2); Proseso.stdin.close(); Proseso.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Network_bridge_pagpasok and Network_bridge_pagpasok.error: raise RuntimeError('network bridge: '+Network_bridge_pagpasok.error)
            return 0 if 가로채기됨 else Proseso.returncode


if __name__=='__main__':
    from Mag_execute_utos import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argumento_ARRAY=parser.parse_args()
    if argumento_ARRAY.forward and not argumento_ARRAY.network: parser.error('--forward requires --network')
    raise SystemExit(run_desktop(argumento_ARRAY.port,Network=argumento_ARRAY.network,file_lipat_numero_ng_port=argumento_ARRAY.ftp_port,전달규칙들=argumento_ARRAY.forward,resolution_VALUE=argumento_ARRAY.resolution))
