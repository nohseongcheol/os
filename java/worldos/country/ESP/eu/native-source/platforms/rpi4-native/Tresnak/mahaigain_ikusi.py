#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, gako_balio 입력은 자체 nukleo_balio UART로 전달한다. localhost 전용, 단일 kontrol_balio 클라이언트.
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
from exekutatu_komando import Komandoa
from local_input import create


def BERDIN_balio(소켓, Tamaina):
    datuak = bytearray()
    while len(datuak) < Tamaina:
        조각 = 소켓.recv(Tamaina - len(datuak))
        if not 조각: raise EOFError()
        datuak.extend(조각)
    return bytes(datuak)


class teklatu:
    def __init__(자신, bidali, 입력방식알림=None):
        자신.바이트전송 = bidali; 자신.tekla_aldatzaile = set(); 자신.arbel_balio = b''
        자신.한글조합기 = create(bidali, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.ALDATU_gako = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def bidali(자신, datuak):
        자신.한글조합기.조합확정()
        자신.바이트전송(datuak)

    def ALDATU_MODA(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, gako_ikur):
        if gako_ikur in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.tekla_aldatzaile.add(gako_ikur)
            else: 자신.tekla_aldatzaile.discard(gako_ikur)
            return
        if not 누르는중:
            자신.ALDATU_gako.discard(gako_ikur)
            return
        KTRL = bool(자신.tekla_aldatzaile & {0xffe3, 0xffe4})
        MAIUS_tekla = bool(자신.tekla_aldatzaile & {0xffe1, 0xffe2})
        if KTRL and MAIUS_tekla and gako_ikur in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if gako_ikur in (32,0xff0d):
                try:
                    balio=int(자신.유니코드입력,16)
                    if 32<=balio<=0x10ffff and not 0xd800<=balio<=0xdfff: 자신.bidali(chr(balio).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif gako_ikur==0xff1b: 자신.유니코드입력=None
            elif gako_ikur==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif gako_ikur<128 and chr(gako_ikur) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(gako_ikur)
            return
        if gako_ikur in (0xff31,0xffc6) or gako_ikur==32 and MAIUS_tekla and not KTRL:
            if gako_ikur not in 자신.ALDATU_gako: 자신.ALDATU_MODA()
            자신.ALDATU_gako.add(gako_ikur)
            return
        if gako_ikur==0xff08 and 자신.한글여부 and not KTRL and 자신.한글조합기.앞글자지우기(): return
        if KTRL and MAIUS_tekla and gako_ikur in (ord('t'),ord('T')):
            자신.bidali(bytes([30,2,1,0,0,0,0])); return
        if gako_ikur==0xffc3: 자신.bidali(bytes([30,2,2,0,0,0,0])); return
        if gako_ikur==0xffc9: 자신.bidali(bytes([30,2,3,0,0,0,0])); return
        if KTRL and MAIUS_tekla and gako_ikur in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.bidali(자신.arbel_balio); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if gako_ikur in 특수글쇠: 자신.bidali(특수글쇠[gako_ikur]); return
        karaktere_kodeketa = gako_ikur & 0xffffff if gako_ikur & 0xff000000 == 0x01000000 else gako_ikur
        if karaktere_kodeketa > 0x10ffff or 0xd800 <= karaktere_kodeketa <= 0xdfff or gako_ikur >= 0xff00 and gako_ikur < 0x1000000: return
        if KTRL and 0x40 <= karaktere_kodeketa <= 0x7f: 자신.bidali(bytes([karaktere_kodeketa & 31])); return
        if karaktere_kodeketa < 32: return
        if 자신.한글여부 and 자신.tekla_aldatzaile & {0xffea,0xfe03,0xff7e} and not KTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.jario_gako(chr(karaktere_kodeketa), altgr=True): return
        앞부분 = b'\x1b' if 자신.tekla_aldatzaile & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not KTRL and not 앞부분 and 32<=karaktere_kodeketa<127:
            karaktere_datuak=chr(karaktere_kodeketa).upper() if MAIUS_tekla else chr(karaktere_kodeketa)
            if 자신.한글조합기.jario_gako(karaktere_datuak): return
        자신.bidali(앞부분 + chr(karaktere_kodeketa).encode('utf-8'))


class KONEKTATU_mahaigain:
    def __init__(자신, Prozesua):
        자신.Prozesua=Prozesua; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terminala=False; 자신.시작화면=False; 자신.닫힘=False

    def bidali(자신, datuak):
        if not datuak or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Prozesua.stdin.write(datuak); 자신.Prozesua.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                datuak=자신.Prozesua.stdout.read(4096)
                if not datuak: break
                sys.stdout.buffer.write(datuak); sys.stdout.buffer.flush()
                끝부분=(끝부분+datuak)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminala=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.bidali(b'terminal\n')
        finally: 자신.닫힘=True

    def bezero(자신, bezero, Bide_izena):
        zerbitzari_balio=socket.socket(socket.AF_UNIX); zerbitzari_balio.settimeout(10); bezero.settimeout(10)
        teklatu_sarrera=teklatu(자신.bidali,lambda 한글여부:자신.bidali(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            zerbitzari_balio.connect(str(Bide_izena))
            # 초기 협상은 순서대로 끝낸다. 이후 Irteera 가닥만 클라이언트에 쓴다.
            bezero.sendall(BERDIN_balio(zerbitzari_balio,12))
            판번호=BERDIN_balio(bezero,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            zerbitzari_balio.sendall(판번호)
            elementu_ZENBATU=BERDIN_balio(zerbitzari_balio,1);bezero.sendall(elementu_ZENBATU+BERDIN_balio(zerbitzari_balio,elementu_ZENBATU[0]))
            segurtasun=BERDIN_balio(bezero,1)
            if segurtasun!=b'\x01': raise ValueError('unexpected security type')
            zerbitzari_balio.sendall(segurtasun)
            if 판번호==b'RFB 003.008\n':bezero.sendall(BERDIN_balio(zerbitzari_balio,4))
            zerbitzari_balio.sendall(BERDIN_balio(bezero,1))
            초기값=BERDIN_balio(zerbitzari_balio,24)
            bezero.sendall(초기값+BERDIN_balio(zerbitzari_balio,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            bezero.settimeout(None);zerbitzari_balio.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        Kategoria_balio=BERDIN_balio(zerbitzari_balio,1)[0]
                        if Kategoria_balio==0:
                            머리=BERDIN_balio(zerbitzari_balio,3);sarrera_ZENBATU=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 urruneko_balio 포인터의 중복을 피한다.
                            Ezkutua_balio=포인터지원
                            if Ezkutua_balio:bezero.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            bezero.sendall(bytes([Kategoria_balio])+머리)
                            for _ in range(sarrera_ZENBATU):
                                사각형=BERDIN_balio(zerbitzari_balio,12);가로,Bertikala_kargu,폭,높이,kodeketa_balio=struct.unpack('>HHHHi',사각형)
                                if kodeketa_balio!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodeketa_balio))
                                bezero.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    datuak=BERDIN_balio(zerbitzari_balio,min(남음,65536));bezero.sendall(datuak);남음-=len(datuak)
                        elif Kategoria_balio==1:
                            머리=BERDIN_balio(zerbitzari_balio,5);elementu_ZENBATU=struct.unpack('>H',머리[3:])[0]
                            bezero.sendall(bytes([Kategoria_balio])+머리+BERDIN_balio(zerbitzari_balio,elementu_ZENBATU*6))
                        elif Kategoria_balio==2:bezero.sendall(bytes([Kategoria_balio]))
                        elif Kategoria_balio==3:
                            머리=BERDIN_balio(zerbitzari_balio,7);elementu_ZENBATU=struct.unpack('>I',머리[3:])[0]
                            if elementu_ZENBATU>1048576:raise ValueError('server clipboard too large')
                            bezero.sendall(bytes([Kategoria_balio])+머리+BERDIN_balio(zerbitzari_balio,elementu_ZENBATU))
                        else:raise ValueError('unexpected RFB server message: '+str(Kategoria_balio))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:bezero.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                Kategoria_balio=BERDIN_balio(bezero,1)[0]
                if Kategoria_balio==4:
                    testu_nagusi=BERDIN_balio(bezero,7); teklatu_sarrera.누름값(testu_nagusi[0]!=0,struct.unpack('>I',testu_nagusi[3:])[0]); continue
                if Kategoria_balio==255:
                    testu_nagusi=BERDIN_balio(bezero,11)
                    if testu_nagusi[0]!=0: raise ValueError('unsupported QEMU input extension')
                    teklatu_sarrera.누름값(struct.unpack('>H',testu_nagusi[1:3])[0]!=0,struct.unpack('>I',testu_nagusi[3:7])[0]); continue
                if Kategoria_balio==5:
                    testu_nagusi=BERDIN_balio(bezero,5); 단추들,X_koordenatu,Y_koordenatu=struct.unpack('>BHH',testu_nagusi)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: teklatu_sarrera.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=X_koordenatu<576 and 112<=Y_koordenatu<372:
                        BEGIRATU_INDIZE=(Y_koordenatu-112)//52
                        if (Y_koordenatu-112)%52<40 and BEGIRATU_INDIZE<5: 자신.bidali(bytes([ord('1')+BEGIRATU_INDIZE]))
                    else: 자신.bidali(bytes([30,1,단추들,X_koordenatu&255,X_koordenatu>>8,Y_koordenatu&255,Y_koordenatu>>8]))
                    continue
                if Kategoria_balio==6:
                    testu_nagusi=BERDIN_balio(bezero,7); luzera_balio=struct.unpack('>i',testu_nagusi[3:])[0]
                    if abs(luzera_balio)>65536: raise ValueError('clipboard too large')
                    Testua=BERDIN_balio(bezero,abs(luzera_balio))
                    if luzera_balio>=0:
                        try: teklatu_sarrera.arbel_balio=Testua.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: teklatu_sarrera.arbel_balio=Testua.decode('latin-1').encode('utf-8')
                        teklatu_sarrera.arbel_balio=teklatu_sarrera.arbel_balio[:65536].decode('utf-8','ignore').encode('utf-8')
                    zerbitzari_balio.sendall(bytes([Kategoria_balio])+testu_nagusi+Testua); continue
                if Kategoria_balio==0:
                    testu_nagusi=BERDIN_balio(bezero,19)
                    if testu_nagusi[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=testu_nagusi[3]//8
                elif Kategoria_balio==2:
                    testu_nagusi=BERDIN_balio(bezero,3); sarrera_ZENBATU=struct.unpack('>H',testu_nagusi[1:])[0]
                    if sarrera_ZENBATU>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(sarrera_ZENBATU)+'i',BERDIN_balio(bezero,sarrera_ZENBATU*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 balio_lehenetsi Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    testu_nagusi=struct.pack('>BHi',0,1,0)
                elif Kategoria_balio in (3,150): testu_nagusi=BERDIN_balio(bezero,9)
                elif Kategoria_balio==248:
                    testu_nagusi=BERDIN_balio(bezero,8)
                    if testu_nagusi[7]>64: raise ValueError('fence too large')
                    testu_nagusi+=BERDIN_balio(bezero,testu_nagusi[7])
                elif Kategoria_balio==250: testu_nagusi=BERDIN_balio(bezero,3)
                elif Kategoria_balio==251:
                    testu_nagusi=BERDIN_balio(bezero,7)
                    if testu_nagusi[5]>16: raise ValueError('too many screens')
                    testu_nagusi+=BERDIN_balio(bezero,testu_nagusi[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(Kategoria_balio))
                zerbitzari_balio.sendall(bytes([Kategoria_balio])+testu_nagusi)
        except (OSError,EOFError,ValueError) as errorea:
            if str(errorea): print('VNC client:',errorea,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (bezero,zerbitzari_balio):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def exekutatu_mahaigain(ataka_zenbaki=5902, sare=False, fitxategi_transferitu_ataka_zenbaki=2121, 전달규칙들=(), bereizmen_balio=(640, 480), gonbidatu_helbide=None, Ostalari_helbide='127.0.0.1'):
    with ExitStack() as Baliabideak, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        sare_zubi_sarrera = None
        if sare:
            from sare_zubi import sare_zubi
            sare_zubi_sarrera = Baliabideak.enter_context(sare_zubi(fitxategi_transferitu_ataka_zenbaki, 전달규칙들, gonbidatu_helbide=gonbidatu_helbide, Ostalari_helbide=Ostalari_helbide))
        Bide_izena=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',ataka_zenbaki)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if sare_zubi_sarrera and (원격화면접속번호==fitxategi_transferitu_ataka_zenbaki or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and Ostalari==원격화면접속번호 for 통신규약,Ostalari,_ in sare_zubi_sarrera.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Prozesua=subprocess.Popen(Komandoa(bereizmen_balio)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Bide_izena)]+(sare_zubi_sarrera.전달인수() if sare_zubi_sarrera else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            zubi=KONEKTATU_mahaigain(Prozesua); irakurle=threading.Thread(target=zubi.직렬입출력,daemon=True); irakurle.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if sare_zubi_sarrera: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(Ostalari_helbide,fitxategi_transferitu_ataka_zenbaki),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            prozesatze_ataza=None; 가로채기됨=False
            try:
                while Prozesua.poll() is None:
                    try: bezero,_=수신창구.accept()
                    except socket.timeout: continue
                    if prozesatze_ataza is not None and prozesatze_ataza.is_alive(): bezero.close(); continue
                    if not Bide_izena.exists(): bezero.close(); continue
                    prozesatze_ataza=threading.Thread(target=zubi.bezero,args=(bezero,Bide_izena),daemon=True); prozesatze_ataza.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                zubi.닫힘=True
                if sare_zubi_sarrera: sare_zubi_sarrera.pausatu_gertaera.set()
                if Prozesua.poll() is None:
                    Prozesua.terminate()
                    try: Prozesua.wait(timeout=5)
                    except subprocess.TimeoutExpired: Prozesua.kill(); Prozesua.wait()
                irakurle.join(timeout=2); Prozesua.stdin.close(); Prozesua.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if sare_zubi_sarrera and sare_zubi_sarrera.errorea: raise RuntimeError('network bridge: '+sare_zubi_sarrera.errorea)
            return 0 if 가로채기됨 else Prozesua.returncode


if __name__=='__main__':
    from exekutatu_komando import 해상도읽기
    analizatzaile=argparse.ArgumentParser(description=__doc__); analizatzaile.add_argument('--port',type=int,default=5902)
    analizatzaile.add_argument('--resolution',type=해상도읽기,default=(640,480))
    analizatzaile.add_argument('--network',action='store_true'); analizatzaile.add_argument('--ftp-port',type=int,default=2121)
    analizatzaile.add_argument('--forward',action='append',default=[])
    arg_matrize=analizatzaile.parse_args()
    if arg_matrize.forward and not arg_matrize.network: analizatzaile.error('--forward requires --network')
    raise SystemExit(exekutatu_mahaigain(arg_matrize.port,sare=arg_matrize.network,fitxategi_transferitu_ataka_zenbaki=arg_matrize.ftp_port,전달규칙들=arg_matrize.forward,bereizmen_balio=arg_matrize.resolution))
