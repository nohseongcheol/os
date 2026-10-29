#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Chave_VALOR 입력은 자체 kernel_VALOR UART로 전달한다. localhost 전용, 단일 control_VALOR 클라이언트.
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
from executar_comando import Orde
from local_input import create


def EXACTO_VALOR(소켓, Tamaño):
    datos = bytearray()
    while len(datos) < Tamaño:
        조각 = 소켓.recv(Tamaño - len(datos))
        if not 조각: raise EOFError()
        datos.extend(조각)
    return bytes(datos)


class teclado:
    def __init__(자신, enviar, 입력방식알림=None):
        자신.바이트전송 = enviar; 자신.tecla_modificadora = set(); 자신.portapapeis_VALOR = b''
        자신.한글조합기 = create(enviar, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.mudar_Chave = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def enviar(자신, datos):
        자신.한글조합기.조합확정()
        자신.바이트전송(datos)

    def mudar_MODO(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Chave_símbolo):
        if Chave_símbolo in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.tecla_modificadora.add(Chave_símbolo)
            else: 자신.tecla_modificadora.discard(Chave_símbolo)
            return
        if not 누르는중:
            자신.mudar_Chave.discard(Chave_símbolo)
            return
        CTRL = bool(자신.tecla_modificadora & {0xffe3, 0xffe4})
        tecla_MAIÚS = bool(자신.tecla_modificadora & {0xffe1, 0xffe2})
        if CTRL and tecla_MAIÚS and Chave_símbolo in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Chave_símbolo in (32,0xff0d):
                try:
                    VALOR=int(자신.유니코드입력,16)
                    if 32<=VALOR<=0x10ffff and not 0xd800<=VALOR<=0xdfff: 자신.enviar(chr(VALOR).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Chave_símbolo==0xff1b: 자신.유니코드입력=None
            elif Chave_símbolo==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Chave_símbolo<128 and chr(Chave_símbolo) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Chave_símbolo)
            return
        if Chave_símbolo in (0xff31,0xffc6) or Chave_símbolo==32 and tecla_MAIÚS and not CTRL:
            if Chave_símbolo not in 자신.mudar_Chave: 자신.mudar_MODO()
            자신.mudar_Chave.add(Chave_símbolo)
            return
        if Chave_símbolo==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and tecla_MAIÚS and Chave_símbolo in (ord('t'),ord('T')):
            자신.enviar(bytes([30,2,1,0,0,0,0])); return
        if Chave_símbolo==0xffc3: 자신.enviar(bytes([30,2,2,0,0,0,0])); return
        if Chave_símbolo==0xffc9: 자신.enviar(bytes([30,2,3,0,0,0,0])); return
        if CTRL and tecla_MAIÚS and Chave_símbolo in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.enviar(자신.portapapeis_VALOR); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Chave_símbolo in 특수글쇠: 자신.enviar(특수글쇠[Chave_símbolo]); return
        carácter_codificación = Chave_símbolo & 0xffffff if Chave_símbolo & 0xff000000 == 0x01000000 else Chave_símbolo
        if carácter_codificación > 0x10ffff or 0xd800 <= carácter_codificación <= 0xdfff or Chave_símbolo >= 0xff00 and Chave_símbolo < 0x1000000: return
        if CTRL and 0x40 <= carácter_codificación <= 0x7f: 자신.enviar(bytes([carácter_codificación & 31])); return
        if carácter_codificación < 32: return
        if 자신.한글여부 and 자신.tecla_modificadora & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.fonte_Chave(chr(carácter_codificación), altgr=True): return
        앞부분 = b'\x1b' if 자신.tecla_modificadora & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=carácter_codificación<127:
            carácter_datos=chr(carácter_codificación).upper() if tecla_MAIÚS else chr(carácter_codificación)
            if 자신.한글조합기.fonte_Chave(carácter_datos): return
        자신.enviar(앞부분 + chr(carácter_codificación).encode('utf-8'))


class CONECTAR_escritorio:
    def __init__(자신, Proceso):
        자신.Proceso=Proceso; 자신.bloquear_VALOR=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def enviar(자신, datos):
        if not datos or 자신.닫힘: return
        with 자신.bloquear_VALOR:
            try: 자신.Proceso.stdin.write(datos); 자신.Proceso.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                datos=자신.Proceso.stdout.read(4096)
                if not datos: break
                sys.stdout.buffer.write(datos); sys.stdout.buffer.flush()
                끝부분=(끝부분+datos)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.enviar(b'terminal\n')
        finally: 자신.닫힘=True

    def cliente(자신, cliente, CAMIÑO):
        servidor_VALOR=socket.socket(socket.AF_UNIX); servidor_VALOR.settimeout(10); cliente.settimeout(10)
        teclado_introdución=teclado(자신.enviar,lambda 한글여부:자신.enviar(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            servidor_VALOR.connect(str(CAMIÑO))
            # 초기 협상은 순서대로 끝낸다. 이후 Saída 가닥만 클라이언트에 쓴다.
            cliente.sendall(EXACTO_VALOR(servidor_VALOR,12))
            판번호=EXACTO_VALOR(cliente,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            servidor_VALOR.sendall(판번호)
            elemento_CONTAR=EXACTO_VALOR(servidor_VALOR,1);cliente.sendall(elemento_CONTAR+EXACTO_VALOR(servidor_VALOR,elemento_CONTAR[0]))
            Seguranza=EXACTO_VALOR(cliente,1)
            if Seguranza!=b'\x01': raise ValueError('unexpected security type')
            servidor_VALOR.sendall(Seguranza)
            if 판번호==b'RFB 003.008\n':cliente.sendall(EXACTO_VALOR(servidor_VALOR,4))
            servidor_VALOR.sendall(EXACTO_VALOR(cliente,1))
            초기값=EXACTO_VALOR(servidor_VALOR,24)
            cliente.sendall(초기값+EXACTO_VALOR(servidor_VALOR,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            cliente.settimeout(None);servidor_VALOR.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        Categoría_VALOR=EXACTO_VALOR(servidor_VALOR,1)[0]
                        if Categoría_VALOR==0:
                            머리=EXACTO_VALOR(servidor_VALOR,3);introdución_CONTAR=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 remoto_VALOR 포인터의 중복을 피한다.
                            Oculto_VALOR=포인터지원
                            if Oculto_VALOR:cliente.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            cliente.sendall(bytes([Categoría_VALOR])+머리)
                            for _ in range(introdución_CONTAR):
                                사각형=EXACTO_VALOR(servidor_VALOR,12);가로,Vertical_cargo,폭,높이,codificación_VALOR=struct.unpack('>HHHHi',사각형)
                                if codificación_VALOR!=0:raise ValueError('unexpected framebuffer encoding: '+str(codificación_VALOR))
                                cliente.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    datos=EXACTO_VALOR(servidor_VALOR,min(남음,65536));cliente.sendall(datos);남음-=len(datos)
                        elif Categoría_VALOR==1:
                            머리=EXACTO_VALOR(servidor_VALOR,5);elemento_CONTAR=struct.unpack('>H',머리[3:])[0]
                            cliente.sendall(bytes([Categoría_VALOR])+머리+EXACTO_VALOR(servidor_VALOR,elemento_CONTAR*6))
                        elif Categoría_VALOR==2:cliente.sendall(bytes([Categoría_VALOR]))
                        elif Categoría_VALOR==3:
                            머리=EXACTO_VALOR(servidor_VALOR,7);elemento_CONTAR=struct.unpack('>I',머리[3:])[0]
                            if elemento_CONTAR>1048576:raise ValueError('server clipboard too large')
                            cliente.sendall(bytes([Categoría_VALOR])+머리+EXACTO_VALOR(servidor_VALOR,elemento_CONTAR))
                        else:raise ValueError('unexpected RFB server message: '+str(Categoría_VALOR))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:cliente.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                Categoría_VALOR=EXACTO_VALOR(cliente,1)[0]
                if Categoría_VALOR==4:
                    corpo_do_texto=EXACTO_VALOR(cliente,7); teclado_introdución.누름값(corpo_do_texto[0]!=0,struct.unpack('>I',corpo_do_texto[3:])[0]); continue
                if Categoría_VALOR==255:
                    corpo_do_texto=EXACTO_VALOR(cliente,11)
                    if corpo_do_texto[0]!=0: raise ValueError('unsupported QEMU input extension')
                    teclado_introdución.누름값(struct.unpack('>H',corpo_do_texto[1:3])[0]!=0,struct.unpack('>I',corpo_do_texto[3:7])[0]); continue
                if Categoría_VALOR==5:
                    corpo_do_texto=EXACTO_VALOR(cliente,5); 단추들,X_coordenada,Y_coordenada=struct.unpack('>BHH',corpo_do_texto)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: teclado_introdución.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=X_coordenada<576 and 112<=Y_coordenada<372:
                        Busca_ÍNDICE=(Y_coordenada-112)//52
                        if (Y_coordenada-112)%52<40 and Busca_ÍNDICE<5: 자신.enviar(bytes([ord('1')+Busca_ÍNDICE]))
                    else: 자신.enviar(bytes([30,1,단추들,X_coordenada&255,X_coordenada>>8,Y_coordenada&255,Y_coordenada>>8]))
                    continue
                if Categoría_VALOR==6:
                    corpo_do_texto=EXACTO_VALOR(cliente,7); duración_VALOR=struct.unpack('>i',corpo_do_texto[3:])[0]
                    if abs(duración_VALOR)>65536: raise ValueError('clipboard too large')
                    Texto=EXACTO_VALOR(cliente,abs(duración_VALOR))
                    if duración_VALOR>=0:
                        try: teclado_introdución.portapapeis_VALOR=Texto.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: teclado_introdución.portapapeis_VALOR=Texto.decode('latin-1').encode('utf-8')
                        teclado_introdución.portapapeis_VALOR=teclado_introdución.portapapeis_VALOR[:65536].decode('utf-8','ignore').encode('utf-8')
                    servidor_VALOR.sendall(bytes([Categoría_VALOR])+corpo_do_texto+Texto); continue
                if Categoría_VALOR==0:
                    corpo_do_texto=EXACTO_VALOR(cliente,19)
                    if corpo_do_texto[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=corpo_do_texto[3]//8
                elif Categoría_VALOR==2:
                    corpo_do_texto=EXACTO_VALOR(cliente,3); introdución_CONTAR=struct.unpack('>H',corpo_do_texto[1:])[0]
                    if introdución_CONTAR>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(introdución_CONTAR)+'i',EXACTO_VALOR(cliente,introdución_CONTAR*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 valor_predefinido Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    corpo_do_texto=struct.pack('>BHi',0,1,0)
                elif Categoría_VALOR in (3,150): corpo_do_texto=EXACTO_VALOR(cliente,9)
                elif Categoría_VALOR==248:
                    corpo_do_texto=EXACTO_VALOR(cliente,8)
                    if corpo_do_texto[7]>64: raise ValueError('fence too large')
                    corpo_do_texto+=EXACTO_VALOR(cliente,corpo_do_texto[7])
                elif Categoría_VALOR==250: corpo_do_texto=EXACTO_VALOR(cliente,3)
                elif Categoría_VALOR==251:
                    corpo_do_texto=EXACTO_VALOR(cliente,7)
                    if corpo_do_texto[5]>16: raise ValueError('too many screens')
                    corpo_do_texto+=EXACTO_VALOR(cliente,corpo_do_texto[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(Categoría_VALOR))
                servidor_VALOR.sendall(bytes([Categoría_VALOR])+corpo_do_texto)
        except (OSError,EOFError,ValueError) as ERRO:
            if str(ERRO): print('VNC client:',ERRO,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (cliente,servidor_VALOR):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def executar_escritorio(número_do_porto=5902, Rede=False, transferencia_de_ficheiros_número_do_porto=2121, 전달규칙들=(), resolución_VALOR=(640, 480), convidado_ENDEREZO=None, hospedar_ENDEREZO='127.0.0.1'):
    with ExitStack() as Recursos, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Rede_ponte_introdución = None
        if Rede:
            from Rede_ponte import Rede_ponte
            Rede_ponte_introdución = Recursos.enter_context(Rede_ponte(transferencia_de_ficheiros_número_do_porto, 전달규칙들, convidado_ENDEREZO=convidado_ENDEREZO, hospedar_ENDEREZO=hospedar_ENDEREZO))
        CAMIÑO=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',número_do_porto)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Rede_ponte_introdución and (원격화면접속번호==transferencia_de_ficheiros_número_do_porto or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and hospedar==원격화면접속번호 for 통신규약,hospedar,_ in Rede_ponte_introdución.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proceso=subprocess.Popen(Orde(resolución_VALOR)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(CAMIÑO)]+(Rede_ponte_introdución.전달인수() if Rede_ponte_introdución else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ponte=CONECTAR_escritorio(Proceso); Lector=threading.Thread(target=ponte.직렬입출력,daemon=True); Lector.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Rede_ponte_introdución: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(hospedar_ENDEREZO,transferencia_de_ficheiros_número_do_porto),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            procesamento_tarefa=None; 가로채기됨=False
            try:
                while Proceso.poll() is None:
                    try: cliente,_=수신창구.accept()
                    except socket.timeout: continue
                    if procesamento_tarefa is not None and procesamento_tarefa.is_alive(): cliente.close(); continue
                    if not CAMIÑO.exists(): cliente.close(); continue
                    procesamento_tarefa=threading.Thread(target=ponte.cliente,args=(cliente,CAMIÑO),daemon=True); procesamento_tarefa.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ponte.닫힘=True
                if Rede_ponte_introdución: Rede_ponte_introdución.Pausa_evento.set()
                if Proceso.poll() is None:
                    Proceso.terminate()
                    try: Proceso.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proceso.kill(); Proceso.wait()
                Lector.join(timeout=2); Proceso.stdin.close(); Proceso.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Rede_ponte_introdución and Rede_ponte_introdución.ERRO: raise RuntimeError('network bridge: '+Rede_ponte_introdución.ERRO)
            return 0 if 가로채기됨 else Proceso.returncode


if __name__=='__main__':
    from executar_comando import 해상도읽기
    analizador=argparse.ArgumentParser(description=__doc__); analizador.add_argument('--port',type=int,default=5902)
    analizador.add_argument('--resolution',type=해상도읽기,default=(640,480))
    analizador.add_argument('--network',action='store_true'); analizador.add_argument('--ftp-port',type=int,default=2121)
    analizador.add_argument('--forward',action='append',default=[])
    argumento_MATRIZ=analizador.parse_args()
    if argumento_MATRIZ.forward and not argumento_MATRIZ.network: analizador.error('--forward requires --network')
    raise SystemExit(executar_escritorio(argumento_MATRIZ.port,Rede=argumento_MATRIZ.network,transferencia_de_ficheiros_número_do_porto=argumento_MATRIZ.ftp_port,전달규칙들=argumento_MATRIZ.forward,resolución_VALOR=argumento_MATRIZ.resolution))
