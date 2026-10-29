#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ачкыч_маани 입력은 자체 өзөк_маани UART로 전달한다. localhost 전용, 단일 башкаруу_маани 클라이언트.
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
from аткаруу_буйрук import Команда
from local_input import create


def 정확한값(소켓, Өлчөмү):
    берилмелер = bytearray()
    while len(берилмелер) < Өлчөмү:
        조각 = 소켓.recv(Өлчөмү - len(берилмелер))
        if not 조각: raise EOFError()
        берилмелер.extend(조각)
    return bytes(берилмелер)


class баскычтоп:
    def __init__(자신, жөнөтүү, 입력방식알림=None):
        자신.바이트전송 = жөнөтүү; 자신.өзгөрткүч_баскыч = set(); 자신.алмашуу_буфери_маани = b''
        자신.한글조합기 = create(жөнөтүү, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.котормо_ачкыч = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def жөнөтүү(자신, берилмелер):
        자신.한글조합기.조합확정()
        자신.바이트전송(берилмелер)

    def котормо_режим(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, ачкыч_символ):
        if ачкыч_символ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.өзгөрткүч_баскыч.add(ачкыч_символ)
            else: 자신.өзгөрткүч_баскыч.discard(ачкыч_символ)
            return
        if not 누르는중:
            자신.котормо_ачкыч.discard(ачкыч_символ)
            return
        CTRL_баскычы = bool(자신.өзгөрткүч_баскыч & {0xffe3, 0xffe4})
        SHIFT_баскычы = bool(자신.өзгөрткүч_баскыч & {0xffe1, 0xffe2})
        if CTRL_баскычы and SHIFT_баскычы and ачкыч_символ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if ачкыч_символ in (32,0xff0d):
                try:
                    маани=int(자신.유니코드입력,16)
                    if 32<=маани<=0x10ffff and not 0xd800<=маани<=0xdfff: 자신.жөнөтүү(chr(маани).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif ачкыч_символ==0xff1b: 자신.유니코드입력=None
            elif ачкыч_символ==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif ачкыч_символ<128 and chr(ачкыч_символ) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(ачкыч_символ)
            return
        if ачкыч_символ in (0xff31,0xffc6) or ачкыч_символ==32 and SHIFT_баскычы and not CTRL_баскычы:
            if ачкыч_символ not in 자신.котормо_ачкыч: 자신.котормо_режим()
            자신.котормо_ачкыч.add(ачкыч_символ)
            return
        if ачкыч_символ==0xff08 and 자신.한글여부 and not CTRL_баскычы and 자신.한글조합기.앞글자지우기(): return
        if CTRL_баскычы and SHIFT_баскычы and ачкыч_символ in (ord('t'),ord('T')):
            자신.жөнөтүү(bytes([30,2,1,0,0,0,0])); return
        if ачкыч_символ==0xffc3: 자신.жөнөтүү(bytes([30,2,2,0,0,0,0])); return
        if ачкыч_символ==0xffc9: 자신.жөнөтүү(bytes([30,2,3,0,0,0,0])); return
        if CTRL_баскычы and SHIFT_баскычы and ачкыч_символ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.жөнөтүү(자신.алмашуу_буфери_маани); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if ачкыч_символ in 특수글쇠: 자신.жөнөтүү(특수글쇠[ачкыч_символ]); return
        символ_коддоо = ачкыч_символ & 0xffffff if ачкыч_символ & 0xff000000 == 0x01000000 else ачкыч_символ
        if символ_коддоо > 0x10ffff or 0xd800 <= символ_коддоо <= 0xdfff or ачкыч_символ >= 0xff00 and ачкыч_символ < 0x1000000: return
        if CTRL_баскычы and 0x40 <= символ_коддоо <= 0x7f: 자신.жөнөтүү(bytes([символ_коддоо & 31])); return
        if символ_коддоо < 32: return
        if 자신.한글여부 and 자신.өзгөрткүч_баскыч & {0xffea,0xfe03,0xff7e} and not CTRL_баскычы and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.канал_ачкыч(chr(символ_коддоо), altgr=True): return
        앞부분 = b'\x1b' if 자신.өзгөрткүч_баскыч & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL_баскычы and not 앞부분 and 32<=символ_коддоо<127:
            символ_берилмелер_4d9f8719=chr(символ_коддоо).upper() if SHIFT_баскычы else chr(символ_коддоо)
            if 자신.한글조합기.канал_ачкыч(символ_берилмелер_4d9f8719): return
        자신.жөнөтүү(앞부분 + chr(символ_коддоо).encode('utf-8'))


class ТУТАШУУ_иш_такта:
    def __init__(자신, Процесси):
        자신.Процесси=Процесси; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Терминал=False; 자신.시작화면=False; 자신.닫힘=False

    def жөнөтүү(자신, берилмелер):
        if not берилмелер or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Процесси.stdin.write(берилмелер); 자신.Процесси.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                берилмелер=자신.Процесси.stdout.read(4096)
                if not берилмелер: break
                sys.stdout.buffer.write(берилмелер); sys.stdout.buffer.flush()
                끝부분=(끝부분+берилмелер)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Терминал=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.жөнөтүү(b'terminal\n')
        finally: 자신.닫힘=True

    def керектөөчү(자신, керектөөчү, ЖОЛ):
        сервер_маани=socket.socket(socket.AF_UNIX); сервер_маани.settimeout(10); керектөөчү.settimeout(10)
        баскычтоп_киргизме_жазуу=баскычтоп(자신.жөнөтүү,lambda 한글여부:자신.жөнөтүү(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_маани.connect(str(ЖОЛ))
            # 초기 협상은 순서대로 끝낸다. 이후 Чыгыш 가닥만 클라이언트에 쓴다.
            керектөөчү.sendall(정확한값(сервер_маани,12))
            판번호=정확한값(керектөөчү,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_маани.sendall(판번호)
            개수=정확한값(сервер_маани,1);керектөөчү.sendall(개수+정확한값(сервер_маани,개수[0]))
            Коопсуздук=정확한값(керектөөчү,1)
            if Коопсуздук!=b'\x01': raise ValueError('unexpected security type')
            сервер_маани.sendall(Коопсуздук)
            if 판번호==b'RFB 003.008\n':керектөөчү.sendall(정확한값(сервер_маани,4))
            сервер_маани.sendall(정확한값(керектөөчү,1))
            초기값=정확한값(сервер_маани,24)
            керектөөчү.sendall(초기값+정확한값(сервер_маани,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            керектөөчү.settimeout(None);сервер_маани.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        категория_маани=정확한값(сервер_маани,1)[0]
                        if категория_маани==0:
                            머리=정확한값(сервер_маани,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 алыскы_маани 포인터의 중복을 피한다.
                            жашырылган_маани=포인터지원
                            if жашырылган_маани:керектөөчү.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            керектөөчү.sendall(bytes([категория_маани])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(сервер_маани,12);가로,세로,폭,높이,коддоо_маани=struct.unpack('>HHHHi',사각형)
                                if коддоо_маани!=0:raise ValueError('unexpected framebuffer encoding: '+str(коддоо_маани))
                                керектөөчү.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    берилмелер=정확한값(сервер_маани,min(남음,65536));керектөөчү.sendall(берилмелер);남음-=len(берилмелер)
                        elif категория_маани==1:
                            머리=정확한값(сервер_маани,5);개수=struct.unpack('>H',머리[3:])[0]
                            керектөөчү.sendall(bytes([категория_маани])+머리+정확한값(сервер_маани,개수*6))
                        elif категория_маани==2:керектөөчү.sendall(bytes([категория_маани]))
                        elif категория_маани==3:
                            머리=정확한값(сервер_маани,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            керектөөчү.sendall(bytes([категория_маани])+머리+정확한값(сервер_маани,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(категория_маани))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:керектөөчү.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                категория_маани=정확한값(керектөөчү,1)[0]
                if категория_маани==4:
                    негизги_текст=정확한값(керектөөчү,7); баскычтоп_киргизме_жазуу.누름값(негизги_текст[0]!=0,struct.unpack('>I',негизги_текст[3:])[0]); continue
                if категория_маани==255:
                    негизги_текст=정확한값(керектөөчү,11)
                    if негизги_текст[0]!=0: raise ValueError('unsupported QEMU input extension')
                    баскычтоп_киргизме_жазуу.누름값(struct.unpack('>H',негизги_текст[1:3])[0]!=0,struct.unpack('>I',негизги_текст[3:7])[0]); continue
                if категория_маани==5:
                    негизги_текст=정확한값(керектөөчү,5); 단추들,x_координата,세로좌표=struct.unpack('>BHH',негизги_текст)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: баскычтоп_киргизме_жазуу.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_координата<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.жөнөтүү(bytes([ord('1')+색인]))
                    else: 자신.жөнөтүү(bytes([30,1,단추들,x_координата&255,x_координата>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if категория_маани==6:
                    негизги_текст=정확한값(керектөөчү,7); узундук_маани=struct.unpack('>i',негизги_текст[3:])[0]
                    if abs(узундук_маани)>65536: raise ValueError('clipboard too large')
                    Текст=정확한값(керектөөчү,abs(узундук_маани))
                    if узундук_маани>=0:
                        try: баскычтоп_киргизме_жазуу.алмашуу_буфери_маани=Текст.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: баскычтоп_киргизме_жазуу.алмашуу_буфери_маани=Текст.decode('latin-1').encode('utf-8')
                        баскычтоп_киргизме_жазуу.алмашуу_буфери_маани=баскычтоп_киргизме_жазуу.алмашуу_буфери_маани[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_маани.sendall(bytes([категория_маани])+негизги_текст+Текст); continue
                if категория_маани==0:
                    негизги_текст=정확한값(керектөөчү,19)
                    if негизги_текст[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=негизги_текст[3]//8
                elif категория_маани==2:
                    негизги_текст=정확한값(керектөөчү,3); 항목수=struct.unpack('>H',негизги_текст[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(керектөөчү,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 жарыяланбаган_маани Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    негизги_текст=struct.pack('>BHi',0,1,0)
                elif категория_маани in (3,150): негизги_текст=정확한값(керектөөчү,9)
                elif категория_маани==248:
                    негизги_текст=정확한값(керектөөчү,8)
                    if негизги_текст[7]>64: raise ValueError('fence too large')
                    негизги_текст+=정확한값(керектөөчү,негизги_текст[7])
                elif категория_маани==250: негизги_текст=정확한값(керектөөчү,3)
                elif категория_маани==251:
                    негизги_текст=정확한값(керектөөчү,7)
                    if негизги_текст[5]>16: raise ValueError('too many screens')
                    негизги_текст+=정확한값(керектөөчү,негизги_текст[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(категория_маани))
                сервер_маани.sendall(bytes([категория_маани])+негизги_текст)
        except (OSError,EOFError,ValueError) as Ката:
            if str(Ката): print('VNC client:',Ката,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (керектөөчү,сервер_маани):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def топтом_иш_такта(접속번호=5902, Желе=False, 파일전송접속번호=2121, 전달규칙들=(), чечим_маани=(640, 480), 게스트주소=None, кабылдоо_дарек='127.0.0.1'):
    with ExitStack() as Ресурстар, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if Желе:
            from 통신다리 import 통신다리
            통신다리항목 = Ресурстар.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, кабылдоо_дарек=кабылдоо_дарек))
        ЖОЛ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and кабылдоо==원격화면접속번호 for 통신규약,кабылдоо,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Процесси=subprocess.Popen(Команда(чечим_маани)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ЖОЛ)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=ТУТАШУУ_иш_такта(Процесси); окуучу=threading.Thread(target=연결다리.직렬입출력,daemon=True); окуучу.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(кабылдоо_дарек,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Процесси.poll() is None:
                    try: керектөөчү,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): керектөөчү.close(); continue
                    if not ЖОЛ.exists(): керектөөчү.close(); continue
                    처리작업=threading.Thread(target=연결다리.керектөөчү,args=(керектөөчү,ЖОЛ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.пауза_окуя.set()
                if Процесси.poll() is None:
                    Процесси.terminate()
                    try: Процесси.wait(timeout=5)
                    except subprocess.TimeoutExpired: Процесси.kill(); Процесси.wait()
                окуучу.join(timeout=2); Процесси.stdin.close(); Процесси.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.Ката: raise RuntimeError('network bridge: '+통신다리항목.Ката)
            return 0 if 가로채기됨 else Процесси.returncode


if __name__=='__main__':
    from аткаруу_буйрук import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    аргумент_МАССИВ=인수해석기.parse_args()
    if аргумент_МАССИВ.forward and not аргумент_МАССИВ.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(топтом_иш_такта(аргумент_МАССИВ.port,Желе=аргумент_МАССИВ.network,파일전송접속번호=аргумент_МАССИВ.ftp_port,전달규칙들=аргумент_МАССИВ.forward,чечим_маани=аргумент_МАССИВ.resolution))
