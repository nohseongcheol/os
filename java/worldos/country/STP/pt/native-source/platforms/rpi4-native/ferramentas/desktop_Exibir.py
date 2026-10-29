#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Chave_VALOR 입력은 nativo kernel_VALOR UART로 전달한다. localhost 전용, 단일 visual_VALOR 클라이언트.
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
from Executar_comando import comando
from local_input import create


def EXATO_VALOR(soquete_VALOR, Tamanho):
    dados = bytearray()
    while len(dados) < Tamanho:
        fragmento_VALOR = soquete_VALOR.recv(Tamanho - len(dados))
        if not fragmento_VALOR: raise EOFError()
        dados.extend(fragmento_VALOR)
    return bytes(dados)


class teclado:
    def __init__(자신, enviar, 입력방식알림=None):
        자신.바이트전송 = enviar; 자신.tecla_modificadora = set(); 자신.área_de_transferência_VALOR = b''
        자신.한글조합기 = create(enviar, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.mudar_Chave = set()
        자신.UNICODE_entrada = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def enviar(자신, dados):
        자신.한글조합기.commit_composição()
        자신.바이트전송(dados)

    def mudar_MODO(자신):
        자신.한글조합기.commit_composição(); 자신.한글여부 = not 자신.한글여부
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
        tecla_SHIFT = bool(자신.tecla_modificadora & {0xffe1, 0xffe2})
        if CTRL and tecla_SHIFT and Chave_símbolo in (ord('u'),ord('U')):
            자신.한글조합기.commit_composição(); 자신.UNICODE_entrada = ''; return
        if 자신.UNICODE_entrada is not None:
            if Chave_símbolo in (32,0xff0d):
                try:
                    VALOR=int(자신.UNICODE_entrada,16)
                    if 32<=VALOR<=0x10ffff and not 0xd800<=VALOR<=0xdfff: 자신.enviar(chr(VALOR).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_entrada=None
            elif Chave_símbolo==0xff1b: 자신.UNICODE_entrada=None
            elif Chave_símbolo==0xff08: 자신.UNICODE_entrada=자신.UNICODE_entrada[:-1]
            elif Chave_símbolo<128 and chr(Chave_símbolo) in '0123456789abcdefABCDEF' and len(자신.UNICODE_entrada)<6: 자신.UNICODE_entrada+=chr(Chave_símbolo)
            return
        if Chave_símbolo in (0xff31,0xffc6) or Chave_símbolo==32 and tecla_SHIFT and not CTRL:
            if Chave_símbolo not in 자신.mudar_Chave: 자신.mudar_MODO()
            자신.mudar_Chave.add(Chave_símbolo)
            return
        if Chave_símbolo==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and tecla_SHIFT and Chave_símbolo in (ord('t'),ord('T')):
            자신.enviar(bytes([30,2,1,0,0,0,0])); return
        if Chave_símbolo==0xffc3: 자신.enviar(bytes([30,2,2,0,0,0,0])); return
        if Chave_símbolo==0xffc9: 자신.enviar(bytes([30,2,3,0,0,0,0])); return
        if CTRL and tecla_SHIFT and Chave_símbolo in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.enviar(자신.área_de_transferência_VALOR); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Chave_símbolo in 특수글쇠: 자신.enviar(특수글쇠[Chave_símbolo]); return
        codificação_de_caracteres = Chave_símbolo & 0xffffff if Chave_símbolo & 0xff000000 == 0x01000000 else Chave_símbolo
        if codificação_de_caracteres > 0x10ffff or 0xd800 <= codificação_de_caracteres <= 0xdfff or Chave_símbolo >= 0xff00 and Chave_símbolo < 0x1000000: return
        if CTRL and 0x40 <= codificação_de_caracteres <= 0x7f: 자신.enviar(bytes([codificação_de_caracteres & 31])); return
        if codificação_de_caracteres < 32: return
        if 자신.한글여부 and 자신.tecla_modificadora & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_Chave(chr(codificação_de_caracteres), altgr=True): return
        entrelinhamento_bloco = b'\x1b' if 자신.tecla_modificadora & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not entrelinhamento_bloco and 32<=codificação_de_caracteres<127:
            dados_de_caractere=chr(codificação_de_caracteres).upper() if tecla_SHIFT else chr(codificação_de_caracteres)
            if 자신.한글조합기.feed_Chave(dados_de_caractere): return
        자신.enviar(entrelinhamento_bloco + chr(codificação_de_caracteres).encode('utf-8'))


class Conexão_desktop:
    def __init__(자신, Processo):
        자신.Processo=Processo; 자신.bloquear_VALOR=threading.Lock(); 자신.준비완료=False; 자신.terminal=False; 자신.시작화면=False; 자신.TI_fechado=False

    def enviar(자신, dados):
        if not dados or 자신.TI_fechado: return
        with 자신.bloquear_VALOR:
            try: 자신.Processo.stdin.write(dados); 자신.Processo.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                dados=자신.Processo.stdout.read(4096)
                if not dados: break
                sys.stdout.buffer.write(dados); sys.stdout.buffer.flush()
                끝부분=(끝부분+dados)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); TI_fechado=끝부분.rfind(b'TERMINAL CLOSED'); desenho_tela=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,TI_fechado,desenho_tela,종료됨)>=0:
                    자신.terminal=열림>max(TI_fechado,desenho_tela,종료됨)
                    자신.시작화면=desenho_tela>max(열림,TI_fechado,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.enviar(b'terminal\n')
        finally: 자신.TI_fechado=True

    def cliente(자신, cliente, caminho):
        servidor_VALOR=socket.socket(socket.AF_UNIX); servidor_VALOR.settimeout(10); cliente.settimeout(10)
        teclado_entrada=teclado(자신.enviar,lambda 한글여부:자신.enviar(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            servidor_VALOR.connect(str(caminho))
            # estado_inicial 협상은 순서대로 끝낸다. 이후 saídaTexto 가닥만 클라이언트에 쓴다.
            cliente.sendall(EXATO_VALOR(servidor_VALOR,12))
            número_de_versão=EXATO_VALOR(cliente,12)
            if número_de_versão not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            servidor_VALOR.sendall(número_de_versão)
            item_CONT_NÚM=EXATO_VALOR(servidor_VALOR,1);cliente.sendall(item_CONT_NÚM+EXATO_VALOR(servidor_VALOR,item_CONT_NÚM[0]))
            Segurança=EXATO_VALOR(cliente,1)
            if Segurança!=b'\x01': raise ValueError('unexpected security type')
            servidor_VALOR.sendall(Segurança)
            if número_de_versão==b'RFB 003.008\n':cliente.sendall(EXATO_VALOR(servidor_VALOR,4))
            servidor_VALOR.sendall(EXATO_VALOR(cliente,1))
            초기값=EXATO_VALOR(servidor_VALOR,24)
            cliente.sendall(초기값+EXATO_VALOR(servidor_VALOR,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            cliente.settimeout(None);servidor_VALOR.settimeout(None)
            def saída():
                try:
                    while True:
                        área_VALOR=EXATO_VALOR(servidor_VALOR,1)[0]
                        if área_VALOR==0:
                            HEAD_VALOR=EXATO_VALOR(servidor_VALOR,3);entrada_CONT_NÚM_8f7753a1=struct.unpack('>H',HEAD_VALOR[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 remoto_VALOR 포인터의 중복을 피한다.
                            Oculta_VALOR=포인터지원
                            if Oculta_VALOR:cliente.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            cliente.sendall(bytes([área_VALOR])+HEAD_VALOR)
                            for _ in range(entrada_CONT_NÚM_8f7753a1):
                                retângulo=EXATO_VALOR(servidor_VALOR,12);가로,Vertical_cargo,폭,altura_VALOR,Codificação_VALOR=struct.unpack('>HHHHi',retângulo)
                                if Codificação_VALOR!=0:raise ValueError('unexpected framebuffer encoding: '+str(Codificação_VALOR))
                                cliente.sendall(retângulo)
                                남음=폭*altura_VALOR*화소바이트
                                while 남음:
                                    dados=EXATO_VALOR(servidor_VALOR,min(남음,65536));cliente.sendall(dados);남음-=len(dados)
                        elif área_VALOR==1:
                            HEAD_VALOR=EXATO_VALOR(servidor_VALOR,5);item_CONT_NÚM=struct.unpack('>H',HEAD_VALOR[3:])[0]
                            cliente.sendall(bytes([área_VALOR])+HEAD_VALOR+EXATO_VALOR(servidor_VALOR,item_CONT_NÚM*6))
                        elif área_VALOR==2:cliente.sendall(bytes([área_VALOR]))
                        elif área_VALOR==3:
                            HEAD_VALOR=EXATO_VALOR(servidor_VALOR,7);item_CONT_NÚM=struct.unpack('>I',HEAD_VALOR[3:])[0]
                            if item_CONT_NÚM>1048576:raise ValueError('server clipboard too large')
                            cliente.sendall(bytes([área_VALOR])+HEAD_VALOR+EXATO_VALOR(servidor_VALOR,item_CONT_NÚM))
                        else:raise ValueError('unexpected RFB server message: '+str(área_VALOR))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:cliente.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            tarefaSegundoPlano=threading.Thread(target=saída,daemon=True);tarefaSegundoPlano.start()
            while not 자신.TI_fechado:
                área_VALOR=EXATO_VALOR(cliente,1)[0]
                if área_VALOR==4:
                    corpo_de_texto=EXATO_VALOR(cliente,7); teclado_entrada.누름값(corpo_de_texto[0]!=0,struct.unpack('>I',corpo_de_texto[3:])[0]); continue
                if área_VALOR==255:
                    corpo_de_texto=EXATO_VALOR(cliente,11)
                    if corpo_de_texto[0]!=0: raise ValueError('unsupported QEMU input extension')
                    teclado_entrada.누름값(struct.unpack('>H',corpo_de_texto[1:3])[0]!=0,struct.unpack('>I',corpo_de_texto[3:7])[0]); continue
                if área_VALOR==5:
                    corpo_de_texto=EXATO_VALOR(cliente,5); 단추들,coordenada_X,Y_coordenada=struct.unpack('>BHH',corpo_de_texto)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: teclado_entrada.한글조합기.commit_composição()
                    if 눌림&1 and 자신.시작화면 and 64<=coordenada_X<576 and 112<=Y_coordenada<372:
                        PROC_ÍNDICE=(Y_coordenada-112)//52
                        if (Y_coordenada-112)%52<40 and PROC_ÍNDICE<5: 자신.enviar(bytes([ord('1')+PROC_ÍNDICE]))
                    else: 자신.enviar(bytes([30,1,단추들,coordenada_X&255,coordenada_X>>8,Y_coordenada&255,Y_coordenada>>8]))
                    continue
                if área_VALOR==6:
                    corpo_de_texto=EXATO_VALOR(cliente,7); duração_VALOR=struct.unpack('>i',corpo_de_texto[3:])[0]
                    if abs(duração_VALOR)>65536: raise ValueError('clipboard too large')
                    texto=EXATO_VALOR(cliente,abs(duração_VALOR))
                    if duração_VALOR>=0:
                        try: teclado_entrada.área_de_transferência_VALOR=texto.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: teclado_entrada.área_de_transferência_VALOR=texto.decode('latin-1').encode('utf-8')
                        teclado_entrada.área_de_transferência_VALOR=teclado_entrada.área_de_transferência_VALOR[:65536].decode('utf-8','ignore').encode('utf-8')
                    servidor_VALOR.sendall(bytes([área_VALOR])+corpo_de_texto+texto); continue
                if área_VALOR==0:
                    corpo_de_texto=EXATO_VALOR(cliente,19)
                    if corpo_de_texto[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=corpo_de_texto[3]//8
                elif área_VALOR==2:
                    corpo_de_texto=EXATO_VALOR(cliente,3); entrada_CONT_NÚM_8f7753a1=struct.unpack('>H',corpo_de_texto[1:])[0]
                    if entrada_CONT_NÚM_8f7753a1>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(entrada_CONT_NÚM_8f7753a1)+'i',EXATO_VALOR(cliente,entrada_CONT_NÚM_8f7753a1*4))
                    포인터지원=-239 in 부호들
                    # 로컬 tela 중계는 valor_padrão Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    corpo_de_texto=struct.pack('>BHi',0,1,0)
                elif área_VALOR in (3,150): corpo_de_texto=EXATO_VALOR(cliente,9)
                elif área_VALOR==248:
                    corpo_de_texto=EXATO_VALOR(cliente,8)
                    if corpo_de_texto[7]>64: raise ValueError('fence too large')
                    corpo_de_texto+=EXATO_VALOR(cliente,corpo_de_texto[7])
                elif área_VALOR==250: corpo_de_texto=EXATO_VALOR(cliente,3)
                elif área_VALOR==251:
                    corpo_de_texto=EXATO_VALOR(cliente,7)
                    if corpo_de_texto[5]>16: raise ValueError('too many screens')
                    corpo_de_texto+=EXATO_VALOR(cliente,corpo_de_texto[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(área_VALOR))
                servidor_VALOR.sendall(bytes([área_VALOR])+corpo_de_texto)
        except (OSError,EOFError,ValueError) as erro:
            if str(erro): print('VNC client:',erro,file=sys.stderr,flush=True)
        finally:
            for soquete_VALOR in (cliente,servidor_VALOR):
                try: soquete_VALOR.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                soquete_VALOR.close()


def executar_desktop(número_da_porta=5902, rede=False, transferência_de_arquivo_número_da_porta=2121, 전달규칙들=(), resolução_VALOR=(640, 480), convidado_email=None, ID_do_host='127.0.0.1'):
    with ExitStack() as Recursos, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        ponte_entrada = None
        if rede:
            from ponte_3de4fe3a import ponte_3de4fe3a
            ponte_entrada = Recursos.enter_context(ponte_3de4fe3a(transferência_de_arquivo_número_da_porta, 전달규칙들, convidado_email=convidado_email, ID_do_host=ID_do_host))
        caminho=Path(작업경로)/'display.sock'
        with socket.socket() as porta_de_recepção:
            porta_de_recepção.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            porta_de_recepção.bind(('127.0.0.1',número_da_porta)); porta_de_recepção.listen(1); porta_de_recepção.settimeout(.2)
            원격화면접속번호=porta_de_recepção.getsockname()[1]
            if ponte_entrada and (원격화면접속번호==transferência_de_arquivo_número_da_porta or 50000<=원격화면접속번호<=50007 or any(rede_ABI=='tcp' and host==원격화면접속번호 for rede_ABI,host,_ in ponte_entrada.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Processo=subprocess.Popen(comando(resolução_VALOR)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(caminho)]+(ponte_entrada.전달인수() if ponte_entrada else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            ponte=Conexão_desktop(Processo); Leitor=threading.Thread(target=ponte.직렬입출력,daemon=True); Leitor.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(porta_de_recepção.getsockname()[1]),flush=True)
            if ponte_entrada: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ID_do_host,transferência_de_arquivo_número_da_porta),flush=True)
            def terminar(sinal_número,execução_quadro): raise KeyboardInterrupt()
            Anterior=signal.signal(signal.SIGTERM,terminar)
            processamento_Tarefa=None; 가로채기됨=False
            try:
                while Processo.poll() is None:
                    try: cliente,_=porta_de_recepção.accept()
                    except socket.timeout: continue
                    if processamento_Tarefa is not None and processamento_Tarefa.is_alive(): cliente.close(); continue
                    if not caminho.exists(): cliente.close(); continue
                    processamento_Tarefa=threading.Thread(target=ponte.cliente,args=(cliente,caminho),daemon=True); processamento_Tarefa.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                ponte.TI_fechado=True
                if ponte_entrada: ponte_entrada.Pausar_Evento.set()
                if Processo.poll() is None:
                    Processo.terminate()
                    try: Processo.wait(timeout=5)
                    except subprocess.TimeoutExpired: Processo.kill(); Processo.wait()
                Leitor.join(timeout=2); Processo.stdin.close(); Processo.stdout.close(); signal.signal(signal.SIGTERM,Anterior)
            if ponte_entrada and ponte_entrada.erro: raise RuntimeError('network bridge: '+ponte_entrada.erro)
            return 0 if 가로채기됨 else Processo.returncode


if __name__=='__main__':
    from Executar_comando import leitura_resolução
    analisador=argparse.ArgumentParser(description=__doc__); analisador.add_argument('--port',type=int,default=5902)
    analisador.add_argument('--resolution',type=leitura_resolução,default=(640,480))
    analisador.add_argument('--network',action='store_true'); analisador.add_argument('--ftp-port',type=int,default=2121)
    analisador.add_argument('--forward',action='append',default=[])
    argumento_MATRIZ=analisador.parse_args()
    if argumento_MATRIZ.forward and not argumento_MATRIZ.network: analisador.error('--forward requires --network')
    raise SystemExit(executar_desktop(argumento_MATRIZ.port,rede=argumento_MATRIZ.network,transferência_de_arquivo_número_da_porta=argumento_MATRIZ.ftp_port,전달규칙들=argumento_MATRIZ.forward,resolução_VALOR=argumento_MATRIZ.resolution))
