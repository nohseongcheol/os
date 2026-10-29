#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Makulli_Daraja 입력은 자체 Kwara_Daraja UART로 전달한다. localhost 전용, 단일 masarrafa_Daraja 클라이언트.
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
from gudanar_Umarni import Umarni
from local_input import create


def 정확한값(소켓, Girma):
    Tarin_bayani = bytearray()
    while len(Tarin_bayani) < Girma:
        조각 = 소켓.recv(Girma - len(Tarin_bayani))
        if not 조각: raise EOFError()
        Tarin_bayani.extend(조각)
    return bytes(Tarin_bayani)


class kibod:
    def __init__(자신, Aika, 입력방식알림=None):
        자신.바이트전송 = Aika; 자신.Makullin_yin_sauyi = set(); 자신.Allon_zane_Daraja = b''
        자신.한글조합기 = create(Aika, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.Sauya_Makulli = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def Aika(자신, Tarin_bayani):
        자신.한글조합기.조합확정()
        자신.바이트전송(Tarin_bayani)

    def Sauya_yanayin_aiki(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Makulli_alama):
        if Makulli_alama in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.Makullin_yin_sauyi.add(Makulli_alama)
            else: 자신.Makullin_yin_sauyi.discard(Makulli_alama)
            return
        if not 누르는중:
            자신.Sauya_Makulli.discard(Makulli_alama)
            return
        CTRL = bool(자신.Makullin_yin_sauyi & {0xffe3, 0xffe4})
        Makullin_matsawas = bool(자신.Makullin_yin_sauyi & {0xffe1, 0xffe2})
        if CTRL and Makullin_matsawas and Makulli_alama in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Makulli_alama in (32,0xff0d):
                try:
                    Daraja=int(자신.유니코드입력,16)
                    if 32<=Daraja<=0x10ffff and not 0xd800<=Daraja<=0xdfff: 자신.Aika(chr(Daraja).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Makulli_alama==0xff1b: 자신.유니코드입력=None
            elif Makulli_alama==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Makulli_alama<128 and chr(Makulli_alama) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Makulli_alama)
            return
        if Makulli_alama in (0xff31,0xffc6) or Makulli_alama==32 and Makullin_matsawas and not CTRL:
            if Makulli_alama not in 자신.Sauya_Makulli: 자신.Sauya_yanayin_aiki()
            자신.Sauya_Makulli.add(Makulli_alama)
            return
        if Makulli_alama==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and Makullin_matsawas and Makulli_alama in (ord('t'),ord('T')):
            자신.Aika(bytes([30,2,1,0,0,0,0])); return
        if Makulli_alama==0xffc3: 자신.Aika(bytes([30,2,2,0,0,0,0])); return
        if Makulli_alama==0xffc9: 자신.Aika(bytes([30,2,3,0,0,0,0])); return
        if CTRL and Makullin_matsawas and Makulli_alama in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.Aika(자신.Allon_zane_Daraja); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Makulli_alama in 특수글쇠: 자신.Aika(특수글쇠[Makulli_alama]); return
        Harafi_Juyar_da_bayanai_zuwa_lamba = Makulli_alama & 0xffffff if Makulli_alama & 0xff000000 == 0x01000000 else Makulli_alama
        if Harafi_Juyar_da_bayanai_zuwa_lamba > 0x10ffff or 0xd800 <= Harafi_Juyar_da_bayanai_zuwa_lamba <= 0xdfff or Makulli_alama >= 0xff00 and Makulli_alama < 0x1000000: return
        if CTRL and 0x40 <= Harafi_Juyar_da_bayanai_zuwa_lamba <= 0x7f: 자신.Aika(bytes([Harafi_Juyar_da_bayanai_zuwa_lamba & 31])); return
        if Harafi_Juyar_da_bayanai_zuwa_lamba < 32: return
        if 자신.한글여부 and 자신.Makullin_yin_sauyi & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.Hade_haden_yanar_gizo_Makulli(chr(Harafi_Juyar_da_bayanai_zuwa_lamba), altgr=True): return
        앞부분 = b'\x1b' if 자신.Makullin_yin_sauyi & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=Harafi_Juyar_da_bayanai_zuwa_lamba<127:
            Harafi_Tarin_bayani=chr(Harafi_Juyar_da_bayanai_zuwa_lamba).upper() if Makullin_matsawas else chr(Harafi_Juyar_da_bayanai_zuwa_lamba)
            if 자신.한글조합기.Hade_haden_yanar_gizo_Makulli(Harafi_Tarin_bayani): return
        자신.Aika(앞부분 + chr(Harafi_Juyar_da_bayanai_zuwa_lamba).encode('utf-8'))


class HAƊI_destof:
    def __init__(자신, haryar_aikin_na_ura):
        자신.haryar_aikin_na_ura=haryar_aikin_na_ura; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.터미널=False; 자신.시작화면=False; 자신.닫힘=False

    def Aika(자신, Tarin_bayani):
        if not Tarin_bayani or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.haryar_aikin_na_ura.stdin.write(Tarin_bayani); 자신.haryar_aikin_na_ura.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                Tarin_bayani=자신.haryar_aikin_na_ura.stdout.read(4096)
                if not Tarin_bayani: break
                sys.stdout.buffer.write(Tarin_bayani); sys.stdout.buffer.flush()
                끝부분=(끝부분+Tarin_bayani)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.터미널=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.Aika(b'terminal\n')
        finally: 자신.닫힘=True

    def abokin_hulda(자신, abokin_hulda, Hanyar_shiga):
        Saba_Daraja=socket.socket(socket.AF_UNIX); Saba_Daraja.settimeout(10); abokin_hulda.settimeout(10)
        kibod_Mashigar_bayanai=kibod(자신.Aika,lambda 한글여부:자신.Aika(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            Saba_Daraja.connect(str(Hanyar_shiga))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            abokin_hulda.sendall(정확한값(Saba_Daraja,12))
            판번호=정확한값(abokin_hulda,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            Saba_Daraja.sendall(판번호)
            개수=정확한값(Saba_Daraja,1);abokin_hulda.sendall(개수+정확한값(Saba_Daraja,개수[0]))
            Tsaro=정확한값(abokin_hulda,1)
            if Tsaro!=b'\x01': raise ValueError('unexpected security type')
            Saba_Daraja.sendall(Tsaro)
            if 판번호==b'RFB 003.008\n':abokin_hulda.sendall(정확한값(Saba_Daraja,4))
            Saba_Daraja.sendall(정확한값(abokin_hulda,1))
            초기값=정확한값(Saba_Daraja,24)
            abokin_hulda.sendall(초기값+정확한값(Saba_Daraja,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            abokin_hulda.settimeout(None);Saba_Daraja.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ɓangare_Daraja=정확한값(Saba_Daraja,1)[0]
                        if ɓangare_Daraja==0:
                            머리=정확한값(Saba_Daraja,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 na_nesa_Daraja 포인터의 중복을 피한다.
                            ɓoyayye_Daraja=포인터지원
                            if ɓoyayye_Daraja:abokin_hulda.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            abokin_hulda.sendall(bytes([ɓangare_Daraja])+머리)
                            for _ in range(항목수):
                                사각형=정확한값(Saba_Daraja,12);가로,세로,폭,높이,Juyar_da_bayanai_zuwa_lamba_Daraja=struct.unpack('>HHHHi',사각형)
                                if Juyar_da_bayanai_zuwa_lamba_Daraja!=0:raise ValueError('unexpected framebuffer encoding: '+str(Juyar_da_bayanai_zuwa_lamba_Daraja))
                                abokin_hulda.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    Tarin_bayani=정확한값(Saba_Daraja,min(남음,65536));abokin_hulda.sendall(Tarin_bayani);남음-=len(Tarin_bayani)
                        elif ɓangare_Daraja==1:
                            머리=정확한값(Saba_Daraja,5);개수=struct.unpack('>H',머리[3:])[0]
                            abokin_hulda.sendall(bytes([ɓangare_Daraja])+머리+정확한값(Saba_Daraja,개수*6))
                        elif ɓangare_Daraja==2:abokin_hulda.sendall(bytes([ɓangare_Daraja]))
                        elif ɓangare_Daraja==3:
                            머리=정확한값(Saba_Daraja,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            abokin_hulda.sendall(bytes([ɓangare_Daraja])+머리+정확한값(Saba_Daraja,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(ɓangare_Daraja))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:abokin_hulda.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ɓangare_Daraja=정확한값(abokin_hulda,1)[0]
                if ɓangare_Daraja==4:
                    Gundarin_zube=정확한값(abokin_hulda,7); kibod_Mashigar_bayanai.누름값(Gundarin_zube[0]!=0,struct.unpack('>I',Gundarin_zube[3:])[0]); continue
                if ɓangare_Daraja==255:
                    Gundarin_zube=정확한값(abokin_hulda,11)
                    if Gundarin_zube[0]!=0: raise ValueError('unsupported QEMU input extension')
                    kibod_Mashigar_bayanai.누름값(struct.unpack('>H',Gundarin_zube[1:3])[0]!=0,struct.unpack('>I',Gundarin_zube[3:7])[0]); continue
                if ɓangare_Daraja==5:
                    Gundarin_zube=정확한값(abokin_hulda,5); 단추들,gamayyar_x,Maɓallin_Y_Mai_tsarawa=struct.unpack('>BHH',Gundarin_zube)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: kibod_Mashigar_bayanai.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=gamayyar_x<576 and 112<=Maɓallin_Y_Mai_tsarawa<372:
                        색인=(Maɓallin_Y_Mai_tsarawa-112)//52
                        if (Maɓallin_Y_Mai_tsarawa-112)%52<40 and 색인<5: 자신.Aika(bytes([ord('1')+색인]))
                    else: 자신.Aika(bytes([30,1,단추들,gamayyar_x&255,gamayyar_x>>8,Maɓallin_Y_Mai_tsarawa&255,Maɓallin_Y_Mai_tsarawa>>8]))
                    continue
                if ɓangare_Daraja==6:
                    Gundarin_zube=정확한값(abokin_hulda,7); Tsawo_Daraja=struct.unpack('>i',Gundarin_zube[3:])[0]
                    if abs(Tsawo_Daraja)>65536: raise ValueError('clipboard too large')
                    SMS=정확한값(abokin_hulda,abs(Tsawo_Daraja))
                    if Tsawo_Daraja>=0:
                        try: kibod_Mashigar_bayanai.Allon_zane_Daraja=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: kibod_Mashigar_bayanai.Allon_zane_Daraja=SMS.decode('latin-1').encode('utf-8')
                        kibod_Mashigar_bayanai.Allon_zane_Daraja=kibod_Mashigar_bayanai.Allon_zane_Daraja[:65536].decode('utf-8','ignore').encode('utf-8')
                    Saba_Daraja.sendall(bytes([ɓangare_Daraja])+Gundarin_zube+SMS); continue
                if ɓangare_Daraja==0:
                    Gundarin_zube=정확한값(abokin_hulda,19)
                    if Gundarin_zube[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=Gundarin_zube[3]//8
                elif ɓangare_Daraja==2:
                    Gundarin_zube=정확한값(abokin_hulda,3); 항목수=struct.unpack('>H',Gundarin_zube[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(abokin_hulda,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 Tanadaddiyar_daraja Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    Gundarin_zube=struct.pack('>BHi',0,1,0)
                elif ɓangare_Daraja in (3,150): Gundarin_zube=정확한값(abokin_hulda,9)
                elif ɓangare_Daraja==248:
                    Gundarin_zube=정확한값(abokin_hulda,8)
                    if Gundarin_zube[7]>64: raise ValueError('fence too large')
                    Gundarin_zube+=정확한값(abokin_hulda,Gundarin_zube[7])
                elif ɓangare_Daraja==250: Gundarin_zube=정확한값(abokin_hulda,3)
                elif ɓangare_Daraja==251:
                    Gundarin_zube=정확한값(abokin_hulda,7)
                    if Gundarin_zube[5]>16: raise ValueError('too many screens')
                    Gundarin_zube+=정확한값(abokin_hulda,Gundarin_zube[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ɓangare_Daraja))
                Saba_Daraja.sendall(bytes([ɓangare_Daraja])+Gundarin_zube)
        except (OSError,EOFError,ValueError) as Kuskure:
            if str(Kuskure): print('VNC client:',Kuskure,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (abokin_hulda,Saba_Daraja):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def Gudanar_da_destof(lambar_kafa=5902, Hanyar_sadarwa=False, Fayil_Gusar_da_lambar_kafa=2121, 전달규칙들=(), Kyawon_tarkacen_hoto_Daraja=(640, 480), baƙo_imel=None, sauka_imel='127.0.0.1'):
    with ExitStack() as Albarkatu, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if Hanyar_sadarwa:
            from 통신다리 import 통신다리
            통신다리항목 = Albarkatu.enter_context(통신다리(Fayil_Gusar_da_lambar_kafa, 전달규칙들, baƙo_imel=baƙo_imel, sauka_imel=sauka_imel))
        Hanyar_shiga=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',lambar_kafa)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==Fayil_Gusar_da_lambar_kafa or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and sauka==원격화면접속번호 for 통신규약,sauka,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            haryar_aikin_na_ura=subprocess.Popen(Umarni(Kyawon_tarkacen_hoto_Daraja)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Hanyar_shiga)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=HAƊI_destof(haryar_aikin_na_ura); Manazarci=threading.Thread(target=연결다리.직렬입출력,daemon=True); Manazarci.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(sauka_imel,Fayil_Gusar_da_lambar_kafa),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while haryar_aikin_na_ura.poll() is None:
                    try: abokin_hulda,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): abokin_hulda.close(); continue
                    if not Hanyar_shiga.exists(): abokin_hulda.close(); continue
                    처리작업=threading.Thread(target=연결다리.abokin_hulda,args=(abokin_hulda,Hanyar_shiga),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.dakata_Faruwa.set()
                if haryar_aikin_na_ura.poll() is None:
                    haryar_aikin_na_ura.terminate()
                    try: haryar_aikin_na_ura.wait(timeout=5)
                    except subprocess.TimeoutExpired: haryar_aikin_na_ura.kill(); haryar_aikin_na_ura.wait()
                Manazarci.join(timeout=2); haryar_aikin_na_ura.stdin.close(); haryar_aikin_na_ura.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.Kuskure: raise RuntimeError('network bridge: '+통신다리항목.Kuskure)
            return 0 if 가로채기됨 else haryar_aikin_na_ura.returncode


if __name__=='__main__':
    from gudanar_Umarni import 해상도읽기
    tatsar_manhaja=argparse.ArgumentParser(description=__doc__); tatsar_manhaja.add_argument('--port',type=int,default=5902)
    tatsar_manhaja.add_argument('--resolution',type=해상도읽기,default=(640,480))
    tatsar_manhaja.add_argument('--network',action='store_true'); tatsar_manhaja.add_argument('--ftp-port',type=int,default=2121)
    tatsar_manhaja.add_argument('--forward',action='append',default=[])
    Tubalin_aiki_TSARI=tatsar_manhaja.parse_args()
    if Tubalin_aiki_TSARI.forward and not Tubalin_aiki_TSARI.network: tatsar_manhaja.error('--forward requires --network')
    raise SystemExit(Gudanar_da_destof(Tubalin_aiki_TSARI.port,Hanyar_sadarwa=Tubalin_aiki_TSARI.network,Fayil_Gusar_da_lambar_kafa=Tubalin_aiki_TSARI.ftp_port,전달규칙들=Tubalin_aiki_TSARI.forward,Kyawon_tarkacen_hoto_Daraja=Tubalin_aiki_TSARI.resolution))
