#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Açar_VALUE 입력은 자체 nüvə_VALUE UART로 전달한다. localhost 전용, 단일 nəzarət_VALUE 클라이언트.
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
from icra_etmək_əmr import Əmr
from local_input import create


def EXACT_VALUE(소켓, Böyüklük):
    verilənlər = bytearray()
    while len(verilənlər) < Böyüklük:
        조각 = 소켓.recv(Böyüklük - len(verilənlər))
        if not 조각: raise EOFError()
        verilənlər.extend(조각)
    return bytes(verilənlər)


class klaviatura:
    def __init__(자신, göndərmək, 입력방식알림=None):
        자신.바이트전송 = göndərmək; 자신.dəyişdirici_düymə = set(); 자신.mübadilə_buferi_VALUE = b''
        자신.한글조합기 = create(göndərmək, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Açar = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def göndərmək(자신, verilənlər):
        자신.한글조합기.조합확정()
        자신.바이트전송(verilənlər)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Açar_simvol):
        if Açar_simvol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.dəyişdirici_düymə.add(Açar_simvol)
            else: 자신.dəyişdirici_düymə.discard(Açar_simvol)
            return
        if not 누르는중:
            자신.SWITCH_Açar.discard(Açar_simvol)
            return
        CTRL = bool(자신.dəyişdirici_düymə & {0xffe3, 0xffe4})
        SHIFT_düyməsi = bool(자신.dəyişdirici_düymə & {0xffe1, 0xffe2})
        if CTRL and SHIFT_düyməsi and Açar_simvol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Açar_simvol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.göndərmək(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Açar_simvol==0xff1b: 자신.유니코드입력=None
            elif Açar_simvol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Açar_simvol<128 and chr(Açar_simvol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Açar_simvol)
            return
        if Açar_simvol in (0xff31,0xffc6) or Açar_simvol==32 and SHIFT_düyməsi and not CTRL:
            if Açar_simvol not in 자신.SWITCH_Açar: 자신.SWITCH_MODE()
            자신.SWITCH_Açar.add(Açar_simvol)
            return
        if Açar_simvol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_düyməsi and Açar_simvol in (ord('t'),ord('T')):
            자신.göndərmək(bytes([30,2,1,0,0,0,0])); return
        if Açar_simvol==0xffc3: 자신.göndərmək(bytes([30,2,2,0,0,0,0])); return
        if Açar_simvol==0xffc9: 자신.göndərmək(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_düyməsi and Açar_simvol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.göndərmək(자신.mübadilə_buferi_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Açar_simvol in 특수글쇠: 자신.göndərmək(특수글쇠[Açar_simvol]); return
        simvol_kodlaşdırma = Açar_simvol & 0xffffff if Açar_simvol & 0xff000000 == 0x01000000 else Açar_simvol
        if simvol_kodlaşdırma > 0x10ffff or 0xd800 <= simvol_kodlaşdırma <= 0xdfff or Açar_simvol >= 0xff00 and Açar_simvol < 0x1000000: return
        if CTRL and 0x40 <= simvol_kodlaşdırma <= 0x7f: 자신.göndərmək(bytes([simvol_kodlaşdırma & 31])); return
        if simvol_kodlaşdırma < 32: return
        if 자신.한글여부 and 자신.dəyişdirici_düymə & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.axın_Açar(chr(simvol_kodlaşdırma), altgr=True): return
        앞부분 = b'\x1b' if 자신.dəyişdirici_düymə & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=simvol_kodlaşdırma<127:
            simvol_verilənlər_4d9f8719=chr(simvol_kodlaşdırma).upper() if SHIFT_düyməsi else chr(simvol_kodlaşdırma)
            if 자신.한글조합기.axın_Açar(simvol_verilənlər_4d9f8719): return
        자신.göndərmək(앞부분 + chr(simvol_kodlaşdırma).encode('utf-8'))


class QOŞUN_iş_masası:
    def __init__(자신, Proses):
        자신.Proses=Proses; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def göndərmək(자신, verilənlər):
        if not verilənlər or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Proses.stdin.write(verilənlər); 자신.Proses.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                verilənlər=자신.Proses.stdout.read(4096)
                if not verilənlər: break
                sys.stdout.buffer.write(verilənlər); sys.stdout.buffer.flush()
                끝부분=(끝부분+verilənlər)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.göndərmək(b'terminal\n')
        finally: 자신.닫힘=True

    def müştəri(자신, müştəri, Cığır):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); müştəri.settimeout(10)
        klaviatura_daxiletmə=klaviatura(자신.göndərmək,lambda 한글여부:자신.göndərmək(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(Cığır))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            müştəri.sendall(EXACT_VALUE(server_VALUE,12))
            versiya_nömrəsi=EXACT_VALUE(müştəri,12)
            if versiya_nömrəsi not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(versiya_nömrəsi)
            element_COUNT=EXACT_VALUE(server_VALUE,1);müştəri.sendall(element_COUNT+EXACT_VALUE(server_VALUE,element_COUNT[0]))
            Təhlükəsizlik=EXACT_VALUE(müştəri,1)
            if Təhlükəsizlik!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Təhlükəsizlik)
            if versiya_nömrəsi==b'RFB 003.008\n':müştəri.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(müştəri,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            müştəri.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            müştəri.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        sahə_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if sahə_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);daxiletmə_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 uzaq_VALUE 포인터의 중복을 피한다.
                            gizli_VALUE=포인터지원
                            if gizli_VALUE:müştəri.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            müştəri.sendall(bytes([sahə_VALUE])+머리)
                            for _ in range(daxiletmə_COUNT):
                                사각형=EXACT_VALUE(server_VALUE,12);가로,Şaquli_yerinə_qoymaq,폭,높이,kodlaşdırma_VALUE=struct.unpack('>HHHHi',사각형)
                                if kodlaşdırma_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodlaşdırma_VALUE))
                                müştəri.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    verilənlər=EXACT_VALUE(server_VALUE,min(남음,65536));müştəri.sendall(verilənlər);남음-=len(verilənlər)
                        elif sahə_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);element_COUNT=struct.unpack('>H',머리[3:])[0]
                            müştəri.sendall(bytes([sahə_VALUE])+머리+EXACT_VALUE(server_VALUE,element_COUNT*6))
                        elif sahə_VALUE==2:müştəri.sendall(bytes([sahə_VALUE]))
                        elif sahə_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);element_COUNT=struct.unpack('>I',머리[3:])[0]
                            if element_COUNT>1048576:raise ValueError('server clipboard too large')
                            müştəri.sendall(bytes([sahə_VALUE])+머리+EXACT_VALUE(server_VALUE,element_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(sahə_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:müştəri.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                sahə_VALUE=EXACT_VALUE(müştəri,1)[0]
                if sahə_VALUE==4:
                    əsas_mətn=EXACT_VALUE(müştəri,7); klaviatura_daxiletmə.누름값(əsas_mətn[0]!=0,struct.unpack('>I',əsas_mətn[3:])[0]); continue
                if sahə_VALUE==255:
                    əsas_mətn=EXACT_VALUE(müştəri,11)
                    if əsas_mətn[0]!=0: raise ValueError('unsupported QEMU input extension')
                    klaviatura_daxiletmə.누름값(struct.unpack('>H',əsas_mətn[1:3])[0]!=0,struct.unpack('>I',əsas_mətn[3:7])[0]); continue
                if sahə_VALUE==5:
                    əsas_mətn=EXACT_VALUE(müştəri,5); 단추들,x_koordinatı,Y_koordinat=struct.unpack('>BHH',əsas_mətn)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: klaviatura_daxiletmə.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordinatı<576 and 112<=Y_koordinat<372:
                        LOOKUP_INDEX=(Y_koordinat-112)//52
                        if (Y_koordinat-112)%52<40 and LOOKUP_INDEX<5: 자신.göndərmək(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.göndərmək(bytes([30,1,단추들,x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8]))
                    continue
                if sahə_VALUE==6:
                    əsas_mətn=EXACT_VALUE(müştəri,7); uzunluq_VALUE=struct.unpack('>i',əsas_mətn[3:])[0]
                    if abs(uzunluq_VALUE)>65536: raise ValueError('clipboard too large')
                    Mətn=EXACT_VALUE(müştəri,abs(uzunluq_VALUE))
                    if uzunluq_VALUE>=0:
                        try: klaviatura_daxiletmə.mübadilə_buferi_VALUE=Mətn.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: klaviatura_daxiletmə.mübadilə_buferi_VALUE=Mətn.decode('latin-1').encode('utf-8')
                        klaviatura_daxiletmə.mübadilə_buferi_VALUE=klaviatura_daxiletmə.mübadilə_buferi_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([sahə_VALUE])+əsas_mətn+Mətn); continue
                if sahə_VALUE==0:
                    əsas_mətn=EXACT_VALUE(müştəri,19)
                    if əsas_mətn[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=əsas_mətn[3]//8
                elif sahə_VALUE==2:
                    əsas_mətn=EXACT_VALUE(müştəri,3); daxiletmə_COUNT=struct.unpack('>H',əsas_mətn[1:])[0]
                    if daxiletmə_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(daxiletmə_COUNT)+'i',EXACT_VALUE(müştəri,daxiletmə_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 standart_qiymət Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    əsas_mətn=struct.pack('>BHi',0,1,0)
                elif sahə_VALUE in (3,150): əsas_mətn=EXACT_VALUE(müştəri,9)
                elif sahə_VALUE==248:
                    əsas_mətn=EXACT_VALUE(müştəri,8)
                    if əsas_mətn[7]>64: raise ValueError('fence too large')
                    əsas_mətn+=EXACT_VALUE(müştəri,əsas_mətn[7])
                elif sahə_VALUE==250: əsas_mətn=EXACT_VALUE(müştəri,3)
                elif sahə_VALUE==251:
                    əsas_mətn=EXACT_VALUE(müştəri,7)
                    if əsas_mətn[5]>16: raise ValueError('too many screens')
                    əsas_mətn+=EXACT_VALUE(müştəri,əsas_mətn[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(sahə_VALUE))
                server_VALUE.sendall(bytes([sahə_VALUE])+əsas_mətn)
        except (OSError,EOFError,ValueError) as XƏTA:
            if str(XƏTA): print('VNC client:',XƏTA,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (müştəri,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def icra_iş_masası(접속번호=5902, Şəbəkə=False, 파일전송접속번호=2121, 전달규칙들=(), əksetmə_qabiliyyəti_VALUE=(640, 480), qonaq_ünvan=None, host_ünvan='127.0.0.1'):
    with ExitStack() as Resurslar, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Şəbəkə_körpü_daxiletmə = None
        if Şəbəkə:
            from Şəbəkə_körpü import Şəbəkə_körpü
            Şəbəkə_körpü_daxiletmə = Resurslar.enter_context(Şəbəkə_körpü(파일전송접속번호, 전달규칙들, qonaq_ünvan=qonaq_ünvan, host_ünvan=host_ünvan))
        Cığır=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Şəbəkə_körpü_daxiletmə and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and host==원격화면접속번호 for 통신규약,host,_ in Şəbəkə_körpü_daxiletmə.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proses=subprocess.Popen(Əmr(əksetmə_qabiliyyəti_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Cığır)]+(Şəbəkə_körpü_daxiletmə.전달인수() if Şəbəkə_körpü_daxiletmə else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            körpü=QOŞUN_iş_masası(Proses); oxucu=threading.Thread(target=körpü.직렬입출력,daemon=True); oxucu.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Şəbəkə_körpü_daxiletmə: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(host_ünvan,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Proses.poll() is None:
                    try: müştəri,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): müştəri.close(); continue
                    if not Cığır.exists(): müştəri.close(); continue
                    처리작업=threading.Thread(target=körpü.müştəri,args=(müştəri,Cığır),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                körpü.닫힘=True
                if Şəbəkə_körpü_daxiletmə: Şəbəkə_körpü_daxiletmə.pauza_hadisə.set()
                if Proses.poll() is None:
                    Proses.terminate()
                    try: Proses.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
                oxucu.join(timeout=2); Proses.stdin.close(); Proses.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Şəbəkə_körpü_daxiletmə and Şəbəkə_körpü_daxiletmə.XƏTA: raise RuntimeError('network bridge: '+Şəbəkə_körpü_daxiletmə.XƏTA)
            return 0 if 가로채기됨 else Proses.returncode


if __name__=='__main__':
    from icra_etmək_əmr import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    arqument_ARRAY=parser.parse_args()
    if arqument_ARRAY.forward and not arqument_ARRAY.network: parser.error('--forward requires --network')
    raise SystemExit(icra_iş_masası(arqument_ARRAY.port,Şəbəkə=arqument_ARRAY.network,파일전송접속번호=arqument_ARRAY.ftp_port,전달규칙들=arqument_ARRAY.forward,əksetmə_qabiliyyəti_VALUE=arqument_ARRAY.resolution))
