#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, калид_қимат 입력은 자체 ҳаста_қимат UART로 전달한다. localhost 전용, 단일 идоракунӣ_қимат 클라이언트.
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
from иҷро_кардан_фармон import фармон
from local_input import create


def 정확한값(소켓, андоза_кардан):
    иттилоот = bytearray()
    while len(иттилоот) < андоза_кардан:
        조각 = 소켓.recv(андоза_кардан - len(иттилоот))
        if not 조각: raise EOFError()
        иттилоот.extend(조각)
    return bytes(иттилоот)


class клавиатура:
    def __init__(자신, фиристодан, 입력방식알림=None):
        자신.바이트전송 = фиристодан; 자신.тугмаи_виростор = set(); 자신.ҳофизаи_муваққатӣ_қимат = b''
        자신.한글조합기 = create(фиристодан, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.қатъу_васл_кардан_калид = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def фиристодан(자신, иттилоот):
        자신.한글조합기.조합확정()
        자신.바이트전송(иттилоот)

    def қатъу_васл_кардан_ҳолат(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, калид_аломат):
        if калид_аломат in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.тугмаи_виростор.add(калид_аломат)
            else: 자신.тугмаи_виростор.discard(калид_аломат)
            return
        if not 누르는중:
            자신.қатъу_васл_кардан_калид.discard(калид_аломат)
            return
        идоракунӣ_калид = bool(자신.тугмаи_виростор & {0xffe3, 0xffe4})
        тугмаи_SHIFT = bool(자신.тугмаи_виростор & {0xffe1, 0xffe2})
        if идоракунӣ_калид and тугмаи_SHIFT and калид_аломат in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if калид_аломат in (32,0xff0d):
                try:
                    қимат=int(자신.유니코드입력,16)
                    if 32<=қимат<=0x10ffff and not 0xd800<=қимат<=0xdfff: 자신.фиристодан(chr(қимат).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif калид_аломат==0xff1b: 자신.유니코드입력=None
            elif калид_аломат==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif калид_аломат<128 and chr(калид_аломат) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(калид_аломат)
            return
        if калид_аломат in (0xff31,0xffc6) or калид_аломат==32 and тугмаи_SHIFT and not идоракунӣ_калид:
            if калид_аломат not in 자신.қатъу_васл_кардан_калид: 자신.қатъу_васл_кардан_ҳолат()
            자신.қатъу_васл_кардан_калид.add(калид_аломат)
            return
        if калид_аломат==0xff08 and 자신.한글여부 and not идоракунӣ_калид and 자신.한글조합기.앞글자지우기(): return
        if идоракунӣ_калид and тугмаи_SHIFT and калид_аломат in (ord('t'),ord('T')):
            자신.фиристодан(bytes([30,2,1,0,0,0,0])); return
        if калид_аломат==0xffc3: 자신.фиристодан(bytes([30,2,2,0,0,0,0])); return
        if калид_аломат==0xffc9: 자신.фиристодан(bytes([30,2,3,0,0,0,0])); return
        if идоракунӣ_калид and тугмаи_SHIFT and калид_аломат in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.фиристодан(자신.ҳофизаи_муваққатӣ_қимат); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if калид_аломат in 특수글쇠: 자신.фиристодан(특수글쇠[калид_аломат]); return
        аломат_рамзгузорӣ = калид_аломат & 0xffffff if калид_аломат & 0xff000000 == 0x01000000 else калид_аломат
        if аломат_рамзгузорӣ > 0x10ffff or 0xd800 <= аломат_рамзгузорӣ <= 0xdfff or калид_аломат >= 0xff00 and калид_аломат < 0x1000000: return
        if идоракунӣ_калид and 0x40 <= аломат_рамзгузорӣ <= 0x7f: 자신.фиристодан(bytes([аломат_рамзгузорӣ & 31])); return
        if аломат_рамзгузорӣ < 32: return
        if 자신.한글여부 and 자신.тугмаи_виростор & {0xffea,0xfe03,0xff7e} and not идоракунӣ_калид and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.веб_канал_калид(chr(аломат_рамзгузорӣ), altgr=True): return
        앞부분 = b'\x1b' if 자신.тугмаи_виростор & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not идоракунӣ_калид and not 앞부분 and 32<=аломат_рамзгузорӣ<127:
            аломат_иттилоот_4d9f8719=chr(аломат_рамзгузорӣ).upper() if тугмаи_SHIFT else chr(аломат_рамзгузорӣ)
            if 자신.한글조합기.веб_канал_калид(аломат_иттилоот_4d9f8719): return
        자신.фиристодан(앞부분 + chr(аломат_рамзгузорӣ).encode('utf-8'))


class ПАЙВАСТ_мизи_корӣ:
    def __init__(자신, Раванд):
        자신.Раванд=Раванд; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def фиристодан(자신, иттилоот):
        if not иттилоот or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Раванд.stdin.write(иттилоот); 자신.Раванд.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                иттилоот=자신.Раванд.stdout.read(4096)
                if not иттилоот: break
                sys.stdout.buffer.write(иттилоот); sys.stdout.buffer.flush()
                끝부분=(끝부분+иттилоот)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.фиристодан(b'terminal\n')
        finally: 자신.닫힘=True

    def муштарӣ(자신, муштарӣ, масир):
        сервер_қимат=socket.socket(socket.AF_UNIX); сервер_қимат.settimeout(10); муштарӣ.settimeout(10)
        клавиатура_ворида=клавиатура(자신.фиристодан,lambda 한글여부:자신.фиристодан(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            сервер_қимат.connect(str(масир))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            муштарӣ.sendall(정확한값(сервер_қимат,12))
            판번호=정확한값(муштарӣ,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            сервер_қимат.sendall(판번호)
            개수=정확한값(сервер_қимат,1);муштарӣ.sendall(개수+정확한값(сервер_қимат,개수[0]))
            Амният=정확한값(муштарӣ,1)
            if Амният!=b'\x01': raise ValueError('unexpected security type')
            сервер_қимат.sendall(Амният)
            if 판번호==b'RFB 003.008\n':муштарӣ.sendall(정확한값(сервер_қимат,4))
            сервер_қимат.sendall(정확한값(муштарӣ,1))
            초기값=정확한값(сервер_қимат,24)
            муштарӣ.sendall(초기값+정확한값(сервер_қимат,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            муштарӣ.settimeout(None);сервер_қимат.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        категория_қимат=정확한값(сервер_қимат,1)[0]
                        if категория_қимат==0:
                            머리=정확한값(сервер_қимат,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 дурдаст_қимат 포인터의 중복을 피한다.
                            ноаён_қимат=포인터지원
                            if ноаён_қимат:муштарӣ.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            муштарӣ.sendall(bytes([категория_қимат])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(сервер_қимат,12);가로,세로,폭,높이,рамзгузорӣ_қимат=struct.unpack('>HHHHi',사각형)
                                if рамзгузорӣ_қимат!=0:raise ValueError('unexpected framebuffer encoding: '+str(рамзгузорӣ_қимат))
                                муштарӣ.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    иттилоот=정확한값(сервер_қимат,min(남음,65536));муштарӣ.sendall(иттилоот);남음-=len(иттилоот)
                        elif категория_қимат==1:
                            머리=정확한값(сервер_қимат,5);개수=struct.unpack('>H',머리[3:])[0]
                            муштарӣ.sendall(bytes([категория_қимат])+머리+정확한값(сервер_қимат,개수*6))
                        elif категория_қимат==2:муштарӣ.sendall(bytes([категория_қимат]))
                        elif категория_қимат==3:
                            머리=정확한값(сервер_қимат,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            муштарӣ.sendall(bytes([категория_қимат])+머리+정확한값(сервер_қимат,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(категория_қимат))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:муштарӣ.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                категория_қимат=정확한값(муштарӣ,1)[0]
                if категория_қимат==4:
                    матни_асосӣ=정확한값(муштарӣ,7); клавиатура_ворида.누름값(матни_асосӣ[0]!=0,struct.unpack('>I',матни_асосӣ[3:])[0]); continue
                if категория_қимат==255:
                    матни_асосӣ=정확한값(муштарӣ,11)
                    if матни_асосӣ[0]!=0: raise ValueError('unsupported QEMU input extension')
                    клавиатура_ворида.누름값(struct.unpack('>H',матни_асосӣ[1:3])[0]!=0,struct.unpack('>I',матни_асосӣ[3:7])[0]); continue
                if категория_қимат==5:
                    матни_асосӣ=정확한값(муштарӣ,5); 단추들,координатаи_х,세로좌표=struct.unpack('>BHH',матни_асосӣ)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: клавиатура_ворида.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=координатаи_х<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.фиристодан(bytes([ord('1')+색인]))
                    else: 자신.фиристодан(bytes([30,1,단추들,координатаи_х&255,координатаи_х>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if категория_қимат==6:
                    матни_асосӣ=정확한값(муштарӣ,7); дарозӣ_қимат=struct.unpack('>i',матни_асосӣ[3:])[0]
                    if abs(дарозӣ_қимат)>65536: raise ValueError('clipboard too large')
                    Матн=정확한값(муштарӣ,abs(дарозӣ_қимат))
                    if дарозӣ_қимат>=0:
                        try: клавиатура_ворида.ҳофизаи_муваққатӣ_қимат=Матн.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: клавиатура_ворида.ҳофизаи_муваққатӣ_қимат=Матн.decode('latin-1').encode('utf-8')
                        клавиатура_ворида.ҳофизаи_муваққатӣ_қимат=клавиатура_ворида.ҳофизаи_муваққатӣ_қимат[:65536].decode('utf-8','ignore').encode('utf-8')
                    сервер_қимат.sendall(bytes([категория_қимат])+матни_асосӣ+Матн); continue
                if категория_қимат==0:
                    матни_асосӣ=정확한값(муштарӣ,19)
                    if матни_асосӣ[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=матни_асосӣ[3]//8
                elif категория_қимат==2:
                    матни_асосӣ=정확한값(муштарӣ,3); 항목수=struct.unpack('>H',матни_асосӣ[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(муштарӣ,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 қимати_пешфарз Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    матни_асосӣ=struct.pack('>BHi',0,1,0)
                elif категория_қимат in (3,150): матни_асосӣ=정확한값(муштарӣ,9)
                elif категория_қимат==248:
                    матни_асосӣ=정확한값(муштарӣ,8)
                    if матни_асосӣ[7]>64: raise ValueError('fence too large')
                    матни_асосӣ+=정확한값(муштарӣ,матни_асосӣ[7])
                elif категория_қимат==250: матни_асосӣ=정확한값(муштарӣ,3)
                elif категория_қимат==251:
                    матни_асосӣ=정확한값(муштарӣ,7)
                    if матни_асосӣ[5]>16: raise ValueError('too many screens')
                    матни_асосӣ+=정확한값(муштарӣ,матни_асосӣ[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(категория_қимат))
                сервер_қимат.sendall(bytes([категория_қимат])+матни_асосӣ)
        except (OSError,EOFError,ValueError) as Хато:
            if str(Хато): print('VNC client:',Хато,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (муштарӣ,сервер_қимат):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def порча_мизи_корӣ(접속번호=5902, Шабака=False, 파일전송접속번호=2121, 전달규칙들=(), возеҳӣ_қимат=(640, 480), меҳмон_суроға=None, мизбон_суроға='127.0.0.1'):
    with ExitStack() as Захираҳо, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Шабака_кӯпрук_ворида = None
        if Шабака:
            from Шабака_кӯпрук import Шабака_кӯпрук
            Шабака_кӯпрук_ворида = Захираҳо.enter_context(Шабака_кӯпрук(파일전송접속번호, 전달규칙들, меҳмон_суроға=меҳмон_суроға, мизбон_суроға=мизбон_суроға))
        масир=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Шабака_кӯпрук_ворида and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and мизбон==원격화면접속번호 for 통신규약,мизбон,_ in Шабака_кӯпрук_ворида.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Раванд=subprocess.Popen(фармон(возеҳӣ_қимат)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(масир)]+(Шабака_кӯпрук_ворида.전달인수() if Шабака_кӯпрук_ворида else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            кӯпрук=ПАЙВАСТ_мизи_корӣ(Раванд); Хонанда=threading.Thread(target=кӯпрук.직렬입출력,daemon=True); Хонанда.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Шабака_кӯпрук_ворида: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(мизбон_суроға,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Раванд.poll() is None:
                    try: муштарӣ,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): муштарӣ.close(); continue
                    if not масир.exists(): муштарӣ.close(); continue
                    처리작업=threading.Thread(target=кӯпрук.муштарӣ,args=(муштарӣ,масир),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                кӯпрук.닫힘=True
                if Шабака_кӯпрук_ворида: Шабака_кӯпрук_ворида.таваққуф_кардан_рӯйдод.set()
                if Раванд.poll() is None:
                    Раванд.terminate()
                    try: Раванд.wait(timeout=5)
                    except subprocess.TimeoutExpired: Раванд.kill(); Раванд.wait()
                Хонанда.join(timeout=2); Раванд.stdin.close(); Раванд.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Шабака_кӯпрук_ворида and Шабака_кӯпрук_ворида.Хато: raise RuntimeError('network bridge: '+Шабака_кӯпрук_ворида.Хато)
            return 0 if 가로채기됨 else Раванд.returncode


if __name__=='__main__':
    from иҷро_кардан_фармон import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    аргумент_қатор=인수해석기.parse_args()
    if аргумент_қатор.forward and not аргумент_қатор.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(порча_мизи_корӣ(аргумент_қатор.port,Шабака=аргумент_қатор.network,파일전송접속번호=аргумент_қатор.ftp_port,전달규칙들=аргумент_қатор.forward,возеҳӣ_қимат=аргумент_қатор.resolution))
