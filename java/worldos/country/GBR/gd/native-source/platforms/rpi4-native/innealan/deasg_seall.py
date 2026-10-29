#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Iuchair_VALUE 입력은 자체 eitean_VALUE UART로 전달한다. localhost 전용, 단일 smachd_VALUE 클라이언트.
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
from gnìomhaich_àithne import àithne
from local_input import create


def EXACT_VALUE(소켓, atharraich_am_meud):
    dàta = bytearray()
    while len(dàta) < atharraich_am_meud:
        조각 = 소켓.recv(atharraich_am_meud - len(dàta))
        if not 조각: raise EOFError()
        dàta.extend(조각)
    return bytes(dàta)


class meur_chlàr:
    def __init__(자신, cuir, 입력방식알림=None):
        자신.바이트전송 = cuir; 자신.iuchair_atharrachaidh = set(); 자신.bòrd_stòraidh_VALUE = b''
        자신.한글조합기 = create(cuir, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Iuchair = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def cuir(자신, dàta):
        자신.한글조합기.조합확정()
        자신.바이트전송(dàta)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Iuchair_samhla):
        if Iuchair_samhla in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.iuchair_atharrachaidh.add(Iuchair_samhla)
            else: 자신.iuchair_atharrachaidh.discard(Iuchair_samhla)
            return
        if not 누르는중:
            자신.SWITCH_Iuchair.discard(Iuchair_samhla)
            return
        CTRL = bool(자신.iuchair_atharrachaidh & {0xffe3, 0xffe4})
        iuchair_SHIFT = bool(자신.iuchair_atharrachaidh & {0xffe1, 0xffe2})
        if CTRL and iuchair_SHIFT and Iuchair_samhla in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Iuchair_samhla in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.cuir(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Iuchair_samhla==0xff1b: 자신.유니코드입력=None
            elif Iuchair_samhla==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Iuchair_samhla<128 and chr(Iuchair_samhla) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Iuchair_samhla)
            return
        if Iuchair_samhla in (0xff31,0xffc6) or Iuchair_samhla==32 and iuchair_SHIFT and not CTRL:
            if Iuchair_samhla not in 자신.SWITCH_Iuchair: 자신.SWITCH_MODE()
            자신.SWITCH_Iuchair.add(Iuchair_samhla)
            return
        if Iuchair_samhla==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and iuchair_SHIFT and Iuchair_samhla in (ord('t'),ord('T')):
            자신.cuir(bytes([30,2,1,0,0,0,0])); return
        if Iuchair_samhla==0xffc3: 자신.cuir(bytes([30,2,2,0,0,0,0])); return
        if Iuchair_samhla==0xffc9: 자신.cuir(bytes([30,2,3,0,0,0,0])); return
        if CTRL and iuchair_SHIFT and Iuchair_samhla in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.cuir(자신.bòrd_stòraidh_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Iuchair_samhla in 특수글쇠: 자신.cuir(특수글쇠[Iuchair_samhla]); return
        caractar_còdachadh = Iuchair_samhla & 0xffffff if Iuchair_samhla & 0xff000000 == 0x01000000 else Iuchair_samhla
        if caractar_còdachadh > 0x10ffff or 0xd800 <= caractar_còdachadh <= 0xdfff or Iuchair_samhla >= 0xff00 and Iuchair_samhla < 0x1000000: return
        if CTRL and 0x40 <= caractar_còdachadh <= 0x7f: 자신.cuir(bytes([caractar_còdachadh & 31])); return
        if caractar_còdachadh < 32: return
        if 자신.한글여부 and 자신.iuchair_atharrachaidh & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.inbhir_Iuchair(chr(caractar_còdachadh), altgr=True): return
        앞부분 = b'\x1b' if 자신.iuchair_atharrachaidh & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=caractar_còdachadh<127:
            caractar_dàta=chr(caractar_còdachadh).upper() if iuchair_SHIFT else chr(caractar_còdachadh)
            if 자신.한글조합기.inbhir_Iuchair(caractar_dàta): return
        자신.cuir(앞부분 + chr(caractar_còdachadh).encode('utf-8'))


class CONNECT_deasg:
    def __init__(자신, Pròiseas):
        자신.Pròiseas=Pròiseas; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.tèirmineal=False; 자신.시작화면=False; 자신.닫힘=False

    def cuir(자신, dàta):
        if not dàta or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Pròiseas.stdin.write(dàta); 자신.Pròiseas.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                dàta=자신.Pròiseas.stdout.read(4096)
                if not dàta: break
                sys.stdout.buffer.write(dàta); sys.stdout.buffer.flush()
                끝부분=(끝부분+dàta)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.tèirmineal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.cuir(b'terminal\n')
        finally: 자신.닫힘=True

    def cliant(자신, cliant, Slighe):
        frithealaiche_VALUE=socket.socket(socket.AF_UNIX); frithealaiche_VALUE.settimeout(10); cliant.settimeout(10)
        meur_chlàr_cur_a_steach=meur_chlàr(자신.cuir,lambda 한글여부:자신.cuir(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            frithealaiche_VALUE.connect(str(Slighe))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            cliant.sendall(EXACT_VALUE(frithealaiche_VALUE,12))
            판번호=EXACT_VALUE(cliant,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            frithealaiche_VALUE.sendall(판번호)
            nì_COUNT=EXACT_VALUE(frithealaiche_VALUE,1);cliant.sendall(nì_COUNT+EXACT_VALUE(frithealaiche_VALUE,nì_COUNT[0]))
            tèarainteachd=EXACT_VALUE(cliant,1)
            if tèarainteachd!=b'\x01': raise ValueError('unexpected security type')
            frithealaiche_VALUE.sendall(tèarainteachd)
            if 판번호==b'RFB 003.008\n':cliant.sendall(EXACT_VALUE(frithealaiche_VALUE,4))
            frithealaiche_VALUE.sendall(EXACT_VALUE(cliant,1))
            초기값=EXACT_VALUE(frithealaiche_VALUE,24)
            cliant.sendall(초기값+EXACT_VALUE(frithealaiche_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            cliant.settimeout(None);frithealaiche_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        roinn_seòrsa_VALUE=EXACT_VALUE(frithealaiche_VALUE,1)[0]
                        if roinn_seòrsa_VALUE==0:
                            머리=EXACT_VALUE(frithealaiche_VALUE,3);cur_a_steach_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 cian_VALUE 포인터의 중복을 피한다.
                            falaichte_VALUE=포인터지원
                            if falaichte_VALUE:cliant.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            cliant.sendall(bytes([roinn_seòrsa_VALUE])+머리)
                            for _ in range(cur_a_steach_COUNT):
                                사각형=EXACT_VALUE(frithealaiche_VALUE,12);가로,inghearach_suidhich,폭,높이,còdachadh_VALUE=struct.unpack('>HHHHi',사각형)
                                if còdachadh_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(còdachadh_VALUE))
                                cliant.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    dàta=EXACT_VALUE(frithealaiche_VALUE,min(남음,65536));cliant.sendall(dàta);남음-=len(dàta)
                        elif roinn_seòrsa_VALUE==1:
                            머리=EXACT_VALUE(frithealaiche_VALUE,5);nì_COUNT=struct.unpack('>H',머리[3:])[0]
                            cliant.sendall(bytes([roinn_seòrsa_VALUE])+머리+EXACT_VALUE(frithealaiche_VALUE,nì_COUNT*6))
                        elif roinn_seòrsa_VALUE==2:cliant.sendall(bytes([roinn_seòrsa_VALUE]))
                        elif roinn_seòrsa_VALUE==3:
                            머리=EXACT_VALUE(frithealaiche_VALUE,7);nì_COUNT=struct.unpack('>I',머리[3:])[0]
                            if nì_COUNT>1048576:raise ValueError('server clipboard too large')
                            cliant.sendall(bytes([roinn_seòrsa_VALUE])+머리+EXACT_VALUE(frithealaiche_VALUE,nì_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(roinn_seòrsa_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:cliant.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                roinn_seòrsa_VALUE=EXACT_VALUE(cliant,1)[0]
                if roinn_seòrsa_VALUE==4:
                    bodhaig_an_teacsa=EXACT_VALUE(cliant,7); meur_chlàr_cur_a_steach.누름값(bodhaig_an_teacsa[0]!=0,struct.unpack('>I',bodhaig_an_teacsa[3:])[0]); continue
                if roinn_seòrsa_VALUE==255:
                    bodhaig_an_teacsa=EXACT_VALUE(cliant,11)
                    if bodhaig_an_teacsa[0]!=0: raise ValueError('unsupported QEMU input extension')
                    meur_chlàr_cur_a_steach.누름값(struct.unpack('>H',bodhaig_an_teacsa[1:3])[0]!=0,struct.unpack('>I',bodhaig_an_teacsa[3:7])[0]); continue
                if roinn_seòrsa_VALUE==5:
                    bodhaig_an_teacsa=EXACT_VALUE(cliant,5); 단추들,co_chomharra_x,세로좌표=struct.unpack('>BHH',bodhaig_an_teacsa)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: meur_chlàr_cur_a_steach.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=co_chomharra_x<576 and 112<=세로좌표<372:
                        LOOKUP_INDEX=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and LOOKUP_INDEX<5: 자신.cuir(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.cuir(bytes([30,1,단추들,co_chomharra_x&255,co_chomharra_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if roinn_seòrsa_VALUE==6:
                    bodhaig_an_teacsa=EXACT_VALUE(cliant,7); faid_VALUE=struct.unpack('>i',bodhaig_an_teacsa[3:])[0]
                    if abs(faid_VALUE)>65536: raise ValueError('clipboard too large')
                    SMS=EXACT_VALUE(cliant,abs(faid_VALUE))
                    if faid_VALUE>=0:
                        try: meur_chlàr_cur_a_steach.bòrd_stòraidh_VALUE=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: meur_chlàr_cur_a_steach.bòrd_stòraidh_VALUE=SMS.decode('latin-1').encode('utf-8')
                        meur_chlàr_cur_a_steach.bòrd_stòraidh_VALUE=meur_chlàr_cur_a_steach.bòrd_stòraidh_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    frithealaiche_VALUE.sendall(bytes([roinn_seòrsa_VALUE])+bodhaig_an_teacsa+SMS); continue
                if roinn_seòrsa_VALUE==0:
                    bodhaig_an_teacsa=EXACT_VALUE(cliant,19)
                    if bodhaig_an_teacsa[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=bodhaig_an_teacsa[3]//8
                elif roinn_seòrsa_VALUE==2:
                    bodhaig_an_teacsa=EXACT_VALUE(cliant,3); cur_a_steach_COUNT=struct.unpack('>H',bodhaig_an_teacsa[1:])[0]
                    if cur_a_steach_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(cur_a_steach_COUNT)+'i',EXACT_VALUE(cliant,cur_a_steach_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 luach_bunaiteach Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    bodhaig_an_teacsa=struct.pack('>BHi',0,1,0)
                elif roinn_seòrsa_VALUE in (3,150): bodhaig_an_teacsa=EXACT_VALUE(cliant,9)
                elif roinn_seòrsa_VALUE==248:
                    bodhaig_an_teacsa=EXACT_VALUE(cliant,8)
                    if bodhaig_an_teacsa[7]>64: raise ValueError('fence too large')
                    bodhaig_an_teacsa+=EXACT_VALUE(cliant,bodhaig_an_teacsa[7])
                elif roinn_seòrsa_VALUE==250: bodhaig_an_teacsa=EXACT_VALUE(cliant,3)
                elif roinn_seòrsa_VALUE==251:
                    bodhaig_an_teacsa=EXACT_VALUE(cliant,7)
                    if bodhaig_an_teacsa[5]>16: raise ValueError('too many screens')
                    bodhaig_an_teacsa+=EXACT_VALUE(cliant,bodhaig_an_teacsa[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(roinn_seòrsa_VALUE))
                frithealaiche_VALUE.sendall(bytes([roinn_seòrsa_VALUE])+bodhaig_an_teacsa)
        except (OSError,EOFError,ValueError) as Mearachd:
            if str(Mearachd): print('VNC client:',Mearachd,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (cliant,frithealaiche_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ruith_deasg(접속번호=5902, lìonra=False, 파일전송접속번호=2121, 전달규칙들=(), dùmhlachd_bhreacaidh_VALUE=(640, 480), aoigh_ADDRESS=None, òstair_ADDRESS='127.0.0.1'):
    with ExitStack() as Goireasan, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        lìonra_drochaid_cur_a_steach = None
        if lìonra:
            from lìonra_drochaid import lìonra_drochaid
            lìonra_drochaid_cur_a_steach = Goireasan.enter_context(lìonra_drochaid(파일전송접속번호, 전달규칙들, aoigh_ADDRESS=aoigh_ADDRESS, òstair_ADDRESS=òstair_ADDRESS))
        Slighe=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if lìonra_drochaid_cur_a_steach and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and òstair==원격화면접속번호 for 통신규약,òstair,_ in lìonra_drochaid_cur_a_steach.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Pròiseas=subprocess.Popen(àithne(dùmhlachd_bhreacaidh_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Slighe)]+(lìonra_drochaid_cur_a_steach.전달인수() if lìonra_drochaid_cur_a_steach else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            drochaid=CONNECT_deasg(Pròiseas); Leughadair=threading.Thread(target=drochaid.직렬입출력,daemon=True); Leughadair.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if lìonra_drochaid_cur_a_steach: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(òstair_ADDRESS,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Pròiseas.poll() is None:
                    try: cliant,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): cliant.close(); continue
                    if not Slighe.exists(): cliant.close(); continue
                    처리작업=threading.Thread(target=drochaid.cliant,args=(cliant,Slighe),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                drochaid.닫힘=True
                if lìonra_drochaid_cur_a_steach: lìonra_drochaid_cur_a_steach.cuir_na_stad_tachartas.set()
                if Pròiseas.poll() is None:
                    Pròiseas.terminate()
                    try: Pròiseas.wait(timeout=5)
                    except subprocess.TimeoutExpired: Pròiseas.kill(); Pròiseas.wait()
                Leughadair.join(timeout=2); Pròiseas.stdin.close(); Pròiseas.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if lìonra_drochaid_cur_a_steach and lìonra_drochaid_cur_a_steach.Mearachd: raise RuntimeError('network bridge: '+lìonra_drochaid_cur_a_steach.Mearachd)
            return 0 if 가로채기됨 else Pròiseas.returncode


if __name__=='__main__':
    from gnìomhaich_àithne import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    argamaid_ARRAY=인수해석기.parse_args()
    if argamaid_ARRAY.forward and not argamaid_ARRAY.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(ruith_deasg(argamaid_ARRAY.port,lìonra=argamaid_ARRAY.network,파일전송접속번호=argamaid_ARRAY.ftp_port,전달규칙들=argamaid_ARRAY.forward,dùmhlachd_bhreacaidh_VALUE=argamaid_ARRAY.resolution))
