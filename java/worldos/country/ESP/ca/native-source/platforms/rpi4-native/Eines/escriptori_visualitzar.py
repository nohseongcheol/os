#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Clau_VALOR 입력은 propi nucli_VALOR UART로 전달한다. localhost 전용, 단일 control_VALOR 클라이언트.
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
from Executa_ordre import Ordre
from local_input import create


def IGUAL_VALOR(소켓, Mida):
    dades = bytearray()
    while len(dades) < Mida:
        조각 = 소켓.recv(Mida - len(dades))
        if not 조각: raise EOFError()
        dades.extend(조각)
    return bytes(dades)


class teclat:
    def __init__(자신, enviar, 입력방식알림=None):
        자신.바이트전송 = enviar; 자신.tecla_de_modificació = set(); 자신.Porta_retalls_VALOR = b''
        자신.한글조합기 = create(enviar, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.canvi_Clau = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def enviar(자신, dades):
        자신.한글조합기.조합확정()
        자신.바이트전송(dades)

    def canvi_MODA(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Clau_símbol):
        if Clau_símbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.tecla_de_modificació.add(Clau_símbol)
            else: 자신.tecla_de_modificació.discard(Clau_símbol)
            return
        if not 누르는중:
            자신.canvi_Clau.discard(Clau_símbol)
            return
        Control = bool(자신.tecla_de_modificació & {0xffe3, 0xffe4})
        tecla_Maj = bool(자신.tecla_de_modificació & {0xffe1, 0xffe2})
        if Control and tecla_Maj and Clau_símbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Clau_símbol in (32,0xff0d):
                try:
                    VALOR=int(자신.유니코드입력,16)
                    if 32<=VALOR<=0x10ffff and not 0xd800<=VALOR<=0xdfff: 자신.enviar(chr(VALOR).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Clau_símbol==0xff1b: 자신.유니코드입력=None
            elif Clau_símbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Clau_símbol<128 and chr(Clau_símbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Clau_símbol)
            return
        if Clau_símbol in (0xff31,0xffc6) or Clau_símbol==32 and tecla_Maj and not Control:
            if Clau_símbol not in 자신.canvi_Clau: 자신.canvi_MODA()
            자신.canvi_Clau.add(Clau_símbol)
            return
        if Clau_símbol==0xff08 and 자신.한글여부 and not Control and 자신.한글조합기.앞글자지우기(): return
        if Control and tecla_Maj and Clau_símbol in (ord('t'),ord('T')):
            자신.enviar(bytes([30,2,1,0,0,0,0])); return
        if Clau_símbol==0xffc3: 자신.enviar(bytes([30,2,2,0,0,0,0])); return
        if Clau_símbol==0xffc9: 자신.enviar(bytes([30,2,3,0,0,0,0])); return
        if Control and tecla_Maj and Clau_símbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.enviar(자신.Porta_retalls_VALOR); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Clau_símbol in 특수글쇠: 자신.enviar(특수글쇠[Clau_símbol]); return
        caràcter_codificació = Clau_símbol & 0xffffff if Clau_símbol & 0xff000000 == 0x01000000 else Clau_símbol
        if caràcter_codificació > 0x10ffff or 0xd800 <= caràcter_codificació <= 0xdfff or Clau_símbol >= 0xff00 and Clau_símbol < 0x1000000: return
        if Control and 0x40 <= caràcter_codificació <= 0x7f: 자신.enviar(bytes([caràcter_codificació & 31])); return
        if caràcter_codificació < 32: return
        if 자신.한글여부 and 자신.tecla_de_modificació & {0xffea,0xfe03,0xff7e} and not Control and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.font_Clau(chr(caràcter_codificació), altgr=True): return
        앞부분 = b'\x1b' if 자신.tecla_de_modificació & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not Control and not 앞부분 and 32<=caràcter_codificació<127:
            caràcter_dades=chr(caràcter_codificació).upper() if tecla_Maj else chr(caràcter_codificació)
            if 자신.한글조합기.font_Clau(caràcter_dades): return
        자신.enviar(앞부분 + chr(caràcter_codificació).encode('utf-8'))


class CONNECTA_escriptori:
    def __init__(자신, Procés):
        자신.Procés=Procés; 자신.blocar_VALOR=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def enviar(자신, dades):
        if not dades or 자신.닫힘: return
        with 자신.blocar_VALOR:
            try: 자신.Procés.stdin.write(dades); 자신.Procés.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                dades=자신.Procés.stdout.read(4096)
                if not dades: break
                sys.stdout.buffer.write(dades); sys.stdout.buffer.flush()
                끝부분=(끝부분+dades)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.enviar(b'terminal\n')
        finally: 자신.닫힘=True

    def client(자신, client, Camí):
        servidor_VALOR=socket.socket(socket.AF_UNIX); servidor_VALOR.settimeout(10); client.settimeout(10)
        teclat_introducció=teclat(자신.enviar,lambda 한글여부:자신.enviar(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            servidor_VALOR.connect(str(Camí))
            # 초기 협상은 순서대로 끝낸다. 이후 Sortida 가닥만 클라이언트에 쓴다.
            client.sendall(IGUAL_VALOR(servidor_VALOR,12))
            판번호=IGUAL_VALOR(client,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            servidor_VALOR.sendall(판번호)
            element_COMPT=IGUAL_VALOR(servidor_VALOR,1);client.sendall(element_COMPT+IGUAL_VALOR(servidor_VALOR,element_COMPT[0]))
            Seguretat=IGUAL_VALOR(client,1)
            if Seguretat!=b'\x01': raise ValueError('unexpected security type')
            servidor_VALOR.sendall(Seguretat)
            if 판번호==b'RFB 003.008\n':client.sendall(IGUAL_VALOR(servidor_VALOR,4))
            servidor_VALOR.sendall(IGUAL_VALOR(client,1))
            초기값=IGUAL_VALOR(servidor_VALOR,24)
            client.sendall(초기값+IGUAL_VALOR(servidor_VALOR,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            client.settimeout(None);servidor_VALOR.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        Categoria_VALOR=IGUAL_VALOR(servidor_VALOR,1)[0]
                        if Categoria_VALOR==0:
                            머리=IGUAL_VALOR(servidor_VALOR,3);introducció_COMPT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 remot_VALOR 포인터의 중복을 피한다.
                            Amagat_VALOR=포인터지원
                            if Amagat_VALOR:client.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            client.sendall(bytes([Categoria_VALOR])+머리)
                            for _ in range(introducció_COMPT):
                                사각형=IGUAL_VALOR(servidor_VALOR,12);가로,Vertical_càrrec,폭,높이,codificació_VALOR=struct.unpack('>HHHHi',사각형)
                                if codificació_VALOR!=0:raise ValueError('unexpected framebuffer encoding: '+str(codificació_VALOR))
                                client.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    dades=IGUAL_VALOR(servidor_VALOR,min(남음,65536));client.sendall(dades);남음-=len(dades)
                        elif Categoria_VALOR==1:
                            머리=IGUAL_VALOR(servidor_VALOR,5);element_COMPT=struct.unpack('>H',머리[3:])[0]
                            client.sendall(bytes([Categoria_VALOR])+머리+IGUAL_VALOR(servidor_VALOR,element_COMPT*6))
                        elif Categoria_VALOR==2:client.sendall(bytes([Categoria_VALOR]))
                        elif Categoria_VALOR==3:
                            머리=IGUAL_VALOR(servidor_VALOR,7);element_COMPT=struct.unpack('>I',머리[3:])[0]
                            if element_COMPT>1048576:raise ValueError('server clipboard too large')
                            client.sendall(bytes([Categoria_VALOR])+머리+IGUAL_VALOR(servidor_VALOR,element_COMPT))
                        else:raise ValueError('unexpected RFB server message: '+str(Categoria_VALOR))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:client.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                Categoria_VALOR=IGUAL_VALOR(client,1)[0]
                if Categoria_VALOR==4:
                    text_del_cos=IGUAL_VALOR(client,7); teclat_introducció.누름값(text_del_cos[0]!=0,struct.unpack('>I',text_del_cos[3:])[0]); continue
                if Categoria_VALOR==255:
                    text_del_cos=IGUAL_VALOR(client,11)
                    if text_del_cos[0]!=0: raise ValueError('unsupported QEMU input extension')
                    teclat_introducció.누름값(struct.unpack('>H',text_del_cos[1:3])[0]!=0,struct.unpack('>I',text_del_cos[3:7])[0]); continue
                if Categoria_VALOR==5:
                    text_del_cos=IGUAL_VALOR(client,5); 단추들,X_coordenada,Y_coordenada=struct.unpack('>BHH',text_del_cos)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: teclat_introducció.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=X_coordenada<576 and 112<=Y_coordenada<372:
                        Cerca_INDEX=(Y_coordenada-112)//52
                        if (Y_coordenada-112)%52<40 and Cerca_INDEX<5: 자신.enviar(bytes([ord('1')+Cerca_INDEX]))
                    else: 자신.enviar(bytes([30,1,단추들,X_coordenada&255,X_coordenada>>8,Y_coordenada&255,Y_coordenada>>8]))
                    continue
                if Categoria_VALOR==6:
                    text_del_cos=IGUAL_VALOR(client,7); durada_VALOR=struct.unpack('>i',text_del_cos[3:])[0]
                    if abs(durada_VALOR)>65536: raise ValueError('clipboard too large')
                    SMS=IGUAL_VALOR(client,abs(durada_VALOR))
                    if durada_VALOR>=0:
                        try: teclat_introducció.Porta_retalls_VALOR=SMS.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: teclat_introducció.Porta_retalls_VALOR=SMS.decode('latin-1').encode('utf-8')
                        teclat_introducció.Porta_retalls_VALOR=teclat_introducció.Porta_retalls_VALOR[:65536].decode('utf-8','ignore').encode('utf-8')
                    servidor_VALOR.sendall(bytes([Categoria_VALOR])+text_del_cos+SMS); continue
                if Categoria_VALOR==0:
                    text_del_cos=IGUAL_VALOR(client,19)
                    if text_del_cos[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=text_del_cos[3]//8
                elif Categoria_VALOR==2:
                    text_del_cos=IGUAL_VALOR(client,3); introducció_COMPT=struct.unpack('>H',text_del_cos[1:])[0]
                    if introducció_COMPT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(introducció_COMPT)+'i',IGUAL_VALOR(client,introducció_COMPT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 valor_per_defecte Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    text_del_cos=struct.pack('>BHi',0,1,0)
                elif Categoria_VALOR in (3,150): text_del_cos=IGUAL_VALOR(client,9)
                elif Categoria_VALOR==248:
                    text_del_cos=IGUAL_VALOR(client,8)
                    if text_del_cos[7]>64: raise ValueError('fence too large')
                    text_del_cos+=IGUAL_VALOR(client,text_del_cos[7])
                elif Categoria_VALOR==250: text_del_cos=IGUAL_VALOR(client,3)
                elif Categoria_VALOR==251:
                    text_del_cos=IGUAL_VALOR(client,7)
                    if text_del_cos[5]>16: raise ValueError('too many screens')
                    text_del_cos+=IGUAL_VALOR(client,text_del_cos[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(Categoria_VALOR))
                servidor_VALOR.sendall(bytes([Categoria_VALOR])+text_del_cos)
        except (OSError,EOFError,ValueError) as s_ha_produït_un_error:
            if str(s_ha_produït_un_error): print('VNC client:',s_ha_produït_un_error,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (client,servidor_VALOR):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def execució_escriptori(número_de_port=5902, xarxa=False, transferència_de_fitxers_número_de_port=2121, 전달규칙들=(), resolució_VALOR=(640, 480), convidat_ADREÇA=None, allotjar_ADREÇA='127.0.0.1'):
    with ExitStack() as Recursos, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        xarxa_pont_introducció = None
        if xarxa:
            from xarxa_pont import xarxa_pont
            xarxa_pont_introducció = Recursos.enter_context(xarxa_pont(transferència_de_fitxers_número_de_port, 전달규칙들, convidat_ADREÇA=convidat_ADREÇA, allotjar_ADREÇA=allotjar_ADREÇA))
        Camí=Path(작업경로)/'display.sock'
        with socket.socket() as rebre_port:
            rebre_port.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            rebre_port.bind(('127.0.0.1',número_de_port)); rebre_port.listen(1); rebre_port.settimeout(.2)
            원격화면접속번호=rebre_port.getsockname()[1]
            if xarxa_pont_introducció and (원격화면접속번호==transferència_de_fitxers_número_de_port or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and allotjar==원격화면접속번호 for 통신규약,allotjar,_ in xarxa_pont_introducció.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Procés=subprocess.Popen(Ordre(resolució_VALOR)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(Camí)]+(xarxa_pont_introducció.전달인수() if xarxa_pont_introducció else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            pont=CONNECTA_escriptori(Procés); Lector=threading.Thread(target=pont.직렬입출력,daemon=True); Lector.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(rebre_port.getsockname()[1]),flush=True)
            if xarxa_pont_introducció: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(allotjar_ADREÇA,transferència_de_fitxers_número_de_port),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            processament_tasca=None; 가로채기됨=False
            try:
                while Procés.poll() is None:
                    try: client,_=rebre_port.accept()
                    except socket.timeout: continue
                    if processament_tasca is not None and processament_tasca.is_alive(): client.close(); continue
                    if not Camí.exists(): client.close(); continue
                    processament_tasca=threading.Thread(target=pont.client,args=(client,Camí),daemon=True); processament_tasca.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                pont.닫힘=True
                if xarxa_pont_introducció: xarxa_pont_introducció.Pausa_incidència.set()
                if Procés.poll() is None:
                    Procés.terminate()
                    try: Procés.wait(timeout=5)
                    except subprocess.TimeoutExpired: Procés.kill(); Procés.wait()
                Lector.join(timeout=2); Procés.stdin.close(); Procés.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if xarxa_pont_introducció and xarxa_pont_introducció.s_ha_produït_un_error: raise RuntimeError('network bridge: '+xarxa_pont_introducció.s_ha_produït_un_error)
            return 0 if 가로채기됨 else Procés.returncode


if __name__=='__main__':
    from Executa_ordre import tancar_resolució
    analitzador=argparse.ArgumentParser(description=__doc__); analitzador.add_argument('--port',type=int,default=5902)
    analitzador.add_argument('--resolution',type=tancar_resolució,default=(640,480))
    analitzador.add_argument('--network',action='store_true'); analitzador.add_argument('--ftp-port',type=int,default=2121)
    analitzador.add_argument('--forward',action='append',default=[])
    arg_MATRIU=analitzador.parse_args()
    if arg_MATRIU.forward and not arg_MATRIU.network: analitzador.error('--forward requires --network')
    raise SystemExit(execució_escriptori(arg_MATRIU.port,xarxa=arg_MATRIU.network,transferència_de_fitxers_número_de_port=arg_MATRIU.ftp_port,전달규칙들=arg_MATRIU.forward,resolució_VALOR=arg_MATRIU.resolution))
