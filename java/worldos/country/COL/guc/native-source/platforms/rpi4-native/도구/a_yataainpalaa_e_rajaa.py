#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, ajüttia_ajutuu 입력은 자체 keetnerü_ajutuu UART로 전달한다. localhost 전용, 단일 aa_inmajia_ajutuu 클라이언트.
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
from 실행 import aluwataaya
from local_input import create


def 정확한값(소켓, 크기):
    atijaaya = bytearray()
    while len(atijaaya) < 크기:
        조각 = 소켓.recv(크기 - len(atijaaya))
        if not 조각: raise EOFError()
        atijaaya.extend(조각)
    return bytes(atijaaya)


class ajüttiaapala:
    def __init__(자신, ajütaa, 입력방식알림=None):
        자신.바이트전송 = ajütaa; 자신.ajüttia_a_wanajülü = set(); 자신.Karalo_utapalajana_ajutuu = b''
        자신.한글조합기 = create(ajütaa, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.전환글쇠 = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ajütaa(자신, atijaaya):
        자신.한글조합기.조합확정()
        자신.바이트전송(atijaaya)

    def 전환(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, 글쇠기호):
        if 글쇠기호 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.ajüttia_a_wanajülü.add(글쇠기호)
            else: 자신.ajüttia_a_wanajülü.discard(글쇠기호)
            return
        if not 누르는중:
            자신.전환글쇠.discard(글쇠기호)
            return
        CTRL = bool(자신.ajüttia_a_wanajülü & {0xffe3, 0xffe4})
        ajüttia_MAYÚS = bool(자신.ajüttia_a_wanajülü & {0xffe1, 0xffe2})
        if CTRL and ajüttia_MAYÚS and 글쇠기호 in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if 글쇠기호 in (32,0xff0d):
                try:
                    ajutuu=int(자신.유니코드입력,16)
                    if 32<=ajutuu<=0x10ffff and not 0xd800<=ajutuu<=0xdfff: 자신.ajütaa(chr(ajutuu).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif 글쇠기호==0xff1b: 자신.유니코드입력=None
            elif 글쇠기호==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif 글쇠기호<128 and chr(글쇠기호) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(글쇠기호)
            return
        if 글쇠기호 in (0xff31,0xffc6) or 글쇠기호==32 and ajüttia_MAYÚS and not CTRL:
            if 글쇠기호 not in 자신.전환글쇠: 자신.전환()
            자신.전환글쇠.add(글쇠기호)
            return
        if 글쇠기호==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and ajüttia_MAYÚS and 글쇠기호 in (ord('t'),ord('T')):
            자신.ajütaa(bytes([30,2,1,0,0,0,0])); return
        if 글쇠기호==0xffc3: 자신.ajütaa(bytes([30,2,2,0,0,0,0])); return
        if 글쇠기호==0xffc9: 자신.ajütaa(bytes([30,2,3,0,0,0,0])); return
        if CTRL and ajüttia_MAYÚS and 글쇠기호 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ajütaa(자신.Karalo_utapalajana_ajutuu); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 글쇠기호 in 특수글쇠: 자신.ajütaa(특수글쇠[글쇠기호]); return
        jeerü_atijitaalüjiaa = 글쇠기호 & 0xffffff if 글쇠기호 & 0xff000000 == 0x01000000 else 글쇠기호
        if jeerü_atijitaalüjiaa > 0x10ffff or 0xd800 <= jeerü_atijitaalüjiaa <= 0xdfff or 글쇠기호 >= 0xff00 and 글쇠기호 < 0x1000000: return
        if CTRL and 0x40 <= jeerü_atijitaalüjiaa <= 0x7f: 자신.ajütaa(bytes([jeerü_atijitaalüjiaa & 31])); return
        if jeerü_atijitaalüjiaa < 32: return
        if 자신.한글여부 and 자신.ajüttia_a_wanajülü & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.achikiimüinmaajatü_ajüttia(chr(jeerü_atijitaalüjiaa), altgr=True): return
        앞부분 = b'\x1b' if 자신.ajüttia_a_wanajülü & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=jeerü_atijitaalüjiaa<127:
            jeerü_atijaaya=chr(jeerü_atijitaalüjiaa).upper() if ajüttia_MAYÚS else chr(jeerü_atijitaalüjiaa)
            if 자신.한글조합기.achikiimüinmaajatü_ajüttia(jeerü_atijaaya): return
        자신.ajütaa(앞부분 + chr(jeerü_atijitaalüjiaa).encode('utf-8'))


class a_ataa_a_yataainpalaa:
    def __init__(자신, 실행과정):
        자신.실행과정=실행과정; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def ajütaa(자신, atijaaya):
        if not atijaaya or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.실행과정.stdin.write(atijaaya); 자신.실행과정.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                atijaaya=자신.실행과정.stdout.read(4096)
                if not atijaaya: break
                sys.stdout.buffer.write(atijaaya); sys.stdout.buffer.flush()
                끝부분=(끝부분+atijaaya)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ajütaa(b'terminal\n')
        finally: 자신.닫힘=True

    def matchanta(자신, matchanta, wopu_a_ttaaleemüin):
        서버=socket.socket(socket.AF_UNIX); 서버.settimeout(10); matchanta.settimeout(10)
        ajüttiaapala_ekeroliaa=ajüttiaapala(자신.ajütaa,lambda 한글여부:자신.ajütaa(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            서버.connect(str(wopu_a_ttaaleemüin))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            matchanta.sendall(정확한값(서버,12))
            판번호=정확한값(matchanta,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            서버.sendall(판번호)
            개수=정확한값(서버,1);matchanta.sendall(개수+정확한값(서버,개수[0]))
            apansaajiaa=정확한값(matchanta,1)
            if apansaajiaa!=b'\x01': raise ValueError('unexpected security type')
            서버.sendall(apansaajiaa)
            if 판번호==b'RFB 003.008\n':matchanta.sendall(정확한값(서버,4))
            서버.sendall(정확한값(matchanta,1))
            초기값=정확한값(서버,24)
            matchanta.sendall(초기값+정확한값(서버,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            matchanta.settimeout(None);서버.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        akotchiraayanüliee_ajutuu=정확한값(서버,1)[0]
                        if akotchiraayanüliee_ajutuu==0:
                            머리=정확한값(서버,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 원격 포인터의 중복을 피한다.
                            anujuluushi_ajutuu=포인터지원
                            if anujuluushi_ajutuu:matchanta.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            matchanta.sendall(bytes([akotchiraayanüliee_ajutuu])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(서버,12);가로,세로,폭,높이,atijitaalüjiaa_ajutuu=struct.unpack('>HHHHi',사각형)
                                if atijitaalüjiaa_ajutuu!=0:raise ValueError('unexpected framebuffer encoding: '+str(atijitaalüjiaa_ajutuu))
                                matchanta.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    atijaaya=정확한값(서버,min(남음,65536));matchanta.sendall(atijaaya);남음-=len(atijaaya)
                        elif akotchiraayanüliee_ajutuu==1:
                            머리=정확한값(서버,5);개수=struct.unpack('>H',머리[3:])[0]
                            matchanta.sendall(bytes([akotchiraayanüliee_ajutuu])+머리+정확한값(서버,개수*6))
                        elif akotchiraayanüliee_ajutuu==2:matchanta.sendall(bytes([akotchiraayanüliee_ajutuu]))
                        elif akotchiraayanüliee_ajutuu==3:
                            머리=정확한값(서버,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            matchanta.sendall(bytes([akotchiraayanüliee_ajutuu])+머리+정확한값(서버,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(akotchiraayanüliee_ajutuu))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:matchanta.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                akotchiraayanüliee_ajutuu=정확한값(matchanta,1)[0]
                if akotchiraayanüliee_ajutuu==4:
                    ashajalaa_a_laülaasükalü=정확한값(matchanta,7); ajüttiaapala_ekeroliaa.누름값(ashajalaa_a_laülaasükalü[0]!=0,struct.unpack('>I',ashajalaa_a_laülaasükalü[3:])[0]); continue
                if akotchiraayanüliee_ajutuu==255:
                    ashajalaa_a_laülaasükalü=정확한값(matchanta,11)
                    if ashajalaa_a_laülaasükalü[0]!=0: raise ValueError('unsupported QEMU input extension')
                    ajüttiaapala_ekeroliaa.누름값(struct.unpack('>H',ashajalaa_a_laülaasükalü[1:3])[0]!=0,struct.unpack('>I',ashajalaa_a_laülaasükalü[3:7])[0]); continue
                if akotchiraayanüliee_ajutuu==5:
                    ashajalaa_a_laülaasükalü=정확한값(matchanta,5); 단추들,가로좌표,세로좌표=struct.unpack('>BHH',ashajalaa_a_laülaasükalü)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: ajüttiaapala_ekeroliaa.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=가로좌표<576 and 112<=세로좌표<372:
                        색인=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and 색인<5: 자신.ajütaa(bytes([ord('1')+색인]))
                    else: 자신.ajütaa(bytes([30,1,단추들,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if akotchiraayanüliee_ajutuu==6:
                    ashajalaa_a_laülaasükalü=정확한값(matchanta,7); akaliaa_ajutuu=struct.unpack('>i',ashajalaa_a_laülaasükalü[3:])[0]
                    if abs(akaliaa_ajutuu)>65536: raise ValueError('clipboard too large')
                    글=정확한값(matchanta,abs(akaliaa_ajutuu))
                    if akaliaa_ajutuu>=0:
                        try: ajüttiaapala_ekeroliaa.Karalo_utapalajana_ajutuu=글.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: ajüttiaapala_ekeroliaa.Karalo_utapalajana_ajutuu=글.decode('latin-1').encode('utf-8')
                        ajüttiaapala_ekeroliaa.Karalo_utapalajana_ajutuu=ajüttiaapala_ekeroliaa.Karalo_utapalajana_ajutuu[:65536].decode('utf-8','ignore').encode('utf-8')
                    서버.sendall(bytes([akotchiraayanüliee_ajutuu])+ashajalaa_a_laülaasükalü+글); continue
                if akotchiraayanüliee_ajutuu==0:
                    ashajalaa_a_laülaasükalü=정확한값(matchanta,19)
                    if ashajalaa_a_laülaasükalü[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=ashajalaa_a_laülaasükalü[3]//8
                elif akotchiraayanüliee_ajutuu==2:
                    ashajalaa_a_laülaasükalü=정확한값(matchanta,3); 항목수=struct.unpack('>H',ashajalaa_a_laülaasükalü[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(matchanta,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ajutuu_aneekuushitüjülia Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ashajalaa_a_laülaasükalü=struct.pack('>BHi',0,1,0)
                elif akotchiraayanüliee_ajutuu in (3,150): ashajalaa_a_laülaasükalü=정확한값(matchanta,9)
                elif akotchiraayanüliee_ajutuu==248:
                    ashajalaa_a_laülaasükalü=정확한값(matchanta,8)
                    if ashajalaa_a_laülaasükalü[7]>64: raise ValueError('fence too large')
                    ashajalaa_a_laülaasükalü+=정확한값(matchanta,ashajalaa_a_laülaasükalü[7])
                elif akotchiraayanüliee_ajutuu==250: ashajalaa_a_laülaasükalü=정확한값(matchanta,3)
                elif akotchiraayanüliee_ajutuu==251:
                    ashajalaa_a_laülaasükalü=정확한값(matchanta,7)
                    if ashajalaa_a_laülaasükalü[5]>16: raise ValueError('too many screens')
                    ashajalaa_a_laülaasükalü+=정확한값(matchanta,ashajalaa_a_laülaasükalü[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(akotchiraayanüliee_ajutuu))
                서버.sendall(bytes([akotchiraayanüliee_ajutuu])+ashajalaa_a_laülaasükalü)
        except (OSError,EOFError,ValueError) as ajachitia:
            if str(ajachitia): print('VNC client:',ajachitia,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (matchanta,서버):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def 바탕화면실행(접속번호=5902, kusu=False, 파일전송접속번호=2121, 전달규칙들=(), ja_yashaanaa_ajutuu=(640, 480), 게스트주소=None, epiajatü_ejepüsee='127.0.0.1'):
    with ExitStack() as 자원관리, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if kusu:
            from 통신다리 import 통신다리
            통신다리항목 = 자원관리.enter_context(통신다리(파일전송접속번호, 전달규칙들, 게스트주소=게스트주소, epiajatü_ejepüsee=epiajatü_ejepüsee))
        wopu_a_ttaaleemüin=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and epiajatü==원격화면접속번호 for 통신규약,epiajatü,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            실행과정=subprocess.Popen(aluwataaya(ja_yashaanaa_ajutuu)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(wopu_a_ttaaleemüin)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=a_ataa_a_yataainpalaa(실행과정); aashaje_erülü=threading.Thread(target=연결다리.직렬입출력,daemon=True); aashaje_erülü.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(epiajatü_ejepüsee,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while 실행과정.poll() is None:
                    try: matchanta,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): matchanta.close(); continue
                    if not wopu_a_ttaaleemüin.exists(): matchanta.close(); continue
                    처리작업=threading.Thread(target=연결다리.matchanta,args=(matchanta,wopu_a_ttaaleemüin),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.ata_üle_eraa_kasachiki.set()
                if 실행과정.poll() is None:
                    실행과정.terminate()
                    try: 실행과정.wait(timeout=5)
                    except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait()
                aashaje_erülü.join(timeout=2); 실행과정.stdin.close(); 실행과정.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.ajachitia: raise RuntimeError('network bridge: '+통신다리항목.ajachitia)
            return 0 if 가로채기됨 else 실행과정.returncode


if __name__=='__main__':
    from 실행 import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ajutuu_matüriisü=인수해석기.parse_args()
    if ajutuu_matüriisü.forward and not ajutuu_matüriisü.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(바탕화면실행(ajutuu_matüriisü.port,kusu=ajutuu_matüriisü.network,파일전송접속번호=ajutuu_matüriisü.ftp_port,전달규칙들=ajutuu_matüriisü.forward,ja_yashaanaa_ajutuu=ajutuu_matüriisü.resolution))
