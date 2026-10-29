#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, tasto_VALORE 입력은 nativo kernel_VALORE UART로 전달한다. localhost 전용, 단일 controllo_VALORE 클라이언트.
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
from Esegui_comando import comando
from local_input import create


def IDENTICO_VALORE(socket_VALORE, Dimensione):
    dati = bytearray()
    while len(dati) < Dimensione:
        blocco_VALORE_652d4b53 = socket_VALORE.recv(Dimensione - len(dati))
        if not blocco_VALORE_652d4b53: raise EOFError()
        dati.extend(blocco_VALORE_652d4b53)
    return bytes(dati)


class tastiera:
    def __init__(자신, inviare, 입력방식알림=None):
        자신.바이트전송 = inviare; 자신.tasto_di_modifica = set(); 자신.Appunti_VALORE = b''
        자신.한글조합기 = create(inviare, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_tasto = set()
        자신.UNICODE_input = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def inviare(자신, dati):
        자신.한글조합기.commit_composizione()
        자신.바이트전송(dati)

    def SWITCH_MODA(자신):
        자신.한글조합기.commit_composizione(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, tasto_simbolo):
        if tasto_simbolo in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.tasto_di_modifica.add(tasto_simbolo)
            else: 자신.tasto_di_modifica.discard(tasto_simbolo)
            return
        if not 누르는중:
            자신.SWITCH_tasto.discard(tasto_simbolo)
            return
        CTRL = bool(자신.tasto_di_modifica & {0xffe3, 0xffe4})
        tasto_MAIUSC = bool(자신.tasto_di_modifica & {0xffe1, 0xffe2})
        if CTRL and tasto_MAIUSC and tasto_simbolo in (ord('u'),ord('U')):
            자신.한글조합기.commit_composizione(); 자신.UNICODE_input = ''; return
        if 자신.UNICODE_input is not None:
            if tasto_simbolo in (32,0xff0d):
                try:
                    VALORE=int(자신.UNICODE_input,16)
                    if 32<=VALORE<=0x10ffff and not 0xd800<=VALORE<=0xdfff: 자신.inviare(chr(VALORE).encode('utf-8'))
                except ValueError: pass
                자신.UNICODE_input=None
            elif tasto_simbolo==0xff1b: 자신.UNICODE_input=None
            elif tasto_simbolo==0xff08: 자신.UNICODE_input=자신.UNICODE_input[:-1]
            elif tasto_simbolo<128 and chr(tasto_simbolo) in '0123456789abcdefABCDEF' and len(자신.UNICODE_input)<6: 자신.UNICODE_input+=chr(tasto_simbolo)
            return
        if tasto_simbolo in (0xff31,0xffc6) or tasto_simbolo==32 and tasto_MAIUSC and not CTRL:
            if tasto_simbolo not in 자신.SWITCH_tasto: 자신.SWITCH_MODA()
            자신.SWITCH_tasto.add(tasto_simbolo)
            return
        if tasto_simbolo==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and tasto_MAIUSC and tasto_simbolo in (ord('t'),ord('T')):
            자신.inviare(bytes([30,2,1,0,0,0,0])); return
        if tasto_simbolo==0xffc3: 자신.inviare(bytes([30,2,2,0,0,0,0])); return
        if tasto_simbolo==0xffc9: 자신.inviare(bytes([30,2,3,0,0,0,0])); return
        if CTRL and tasto_MAIUSC and tasto_simbolo in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.inviare(자신.Appunti_VALORE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if tasto_simbolo in 특수글쇠: 자신.inviare(특수글쇠[tasto_simbolo]); return
        codifica_dei_caratteri = tasto_simbolo & 0xffffff if tasto_simbolo & 0xff000000 == 0x01000000 else tasto_simbolo
        if codifica_dei_caratteri > 0x10ffff or 0xd800 <= codifica_dei_caratteri <= 0xdfff or tasto_simbolo >= 0xff00 and tasto_simbolo < 0x1000000: return
        if CTRL and 0x40 <= codifica_dei_caratteri <= 0x7f: 자신.inviare(bytes([codifica_dei_caratteri & 31])); return
        if codifica_dei_caratteri < 32: return
        if 자신.한글여부 and 자신.tasto_di_modifica & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_tasto(chr(codifica_dei_caratteri), altgr=True): return
        interlinea_parte = b'\x1b' if 자신.tasto_di_modifica & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not interlinea_parte and 32<=codifica_dei_caratteri<127:
            dati_di_tipo_carattere=chr(codifica_dei_caratteri).upper() if tasto_MAIUSC else chr(codifica_dei_caratteri)
            if 자신.한글조합기.feed_tasto(dati_di_tipo_carattere): return
        자신.inviare(interlinea_parte + chr(codifica_dei_caratteri).encode('utf-8'))


class CONNETTI_PC:
    def __init__(자신, Processi):
        자신.Processi=Processi; 자신.blocco_VALORE_978a15a5=threading.Lock(); 자신.준비완료=False; 자신.terminale=False; 자신.시작화면=False; 자신.reparto_IT_chiusa=False

    def inviare(자신, dati):
        if not dati or 자신.reparto_IT_chiusa: return
        with 자신.blocco_VALORE_978a15a5:
            try: 자신.Processi.stdin.write(dati); 자신.Processi.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                dati=자신.Processi.stdout.read(4096)
                if not dati: break
                sys.stdout.buffer.write(dati); sys.stdout.buffer.flush()
                끝부분=(끝부분+dati)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); reparto_IT_chiusa=끝부분.rfind(b'TERMINAL CLOSED'); disegno_schermata=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,reparto_IT_chiusa,disegno_schermata,종료됨)>=0:
                    자신.terminale=열림>max(reparto_IT_chiusa,disegno_schermata,종료됨)
                    자신.시작화면=disegno_schermata>max(열림,reparto_IT_chiusa,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.inviare(b'terminal\n')
        finally: 자신.reparto_IT_chiusa=True

    def client(자신, client, percorso):
        server_VALORE=socket.socket(socket.AF_UNIX); server_VALORE.settimeout(10); client.settimeout(10)
        tastiera_voce=tastiera(자신.inviare,lambda 한글여부:자신.inviare(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALORE.connect(str(percorso))
            # stato_iniziale 협상은 순서대로 끝낸다. 이후 uscitaTesto 가닥만 클라이언트에 쓴다.
            client.sendall(IDENTICO_VALORE(server_VALORE,12))
            numero_di_versione=IDENTICO_VALORE(client,12)
            if numero_di_versione not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALORE.sendall(numero_di_versione)
            articolo_CONTA_NUMERI=IDENTICO_VALORE(server_VALORE,1);client.sendall(articolo_CONTA_NUMERI+IDENTICO_VALORE(server_VALORE,articolo_CONTA_NUMERI[0]))
            Sicurezza=IDENTICO_VALORE(client,1)
            if Sicurezza!=b'\x01': raise ValueError('unexpected security type')
            server_VALORE.sendall(Sicurezza)
            if numero_di_versione==b'RFB 003.008\n':client.sendall(IDENTICO_VALORE(server_VALORE,4))
            server_VALORE.sendall(IDENTICO_VALORE(client,1))
            초기값=IDENTICO_VALORE(server_VALORE,24)
            client.sendall(초기값+IDENTICO_VALORE(server_VALORE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            client.settimeout(None);server_VALORE.settimeout(None)
            def output():
                try:
                    while True:
                        Valore_categoria=IDENTICO_VALORE(server_VALORE,1)[0]
                        if Valore_categoria==0:
                            intestazione_VALORE=IDENTICO_VALORE(server_VALORE,3);voce_CONTA_NUMERI=struct.unpack('>H',intestazione_VALORE[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 remoto_VALORE 포인터의 중복을 피한다.
                            Nascosta_VALORE=포인터지원
                            if Nascosta_VALORE:client.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            client.sendall(bytes([Valore_categoria])+intestazione_VALORE)
                            for _ in range(voce_CONTA_NUMERI):
                                rettangolo=IDENTICO_VALORE(server_VALORE,12);가로,Verticale_funzione,폭,altezza_VALORE,Codifica_VALORE=struct.unpack('>HHHHi',rettangolo)
                                if Codifica_VALORE!=0:raise ValueError('unexpected framebuffer encoding: '+str(Codifica_VALORE))
                                client.sendall(rettangolo)
                                남음=폭*altezza_VALORE*화소바이트
                                while 남음:
                                    dati=IDENTICO_VALORE(server_VALORE,min(남음,65536));client.sendall(dati);남음-=len(dati)
                        elif Valore_categoria==1:
                            intestazione_VALORE=IDENTICO_VALORE(server_VALORE,5);articolo_CONTA_NUMERI=struct.unpack('>H',intestazione_VALORE[3:])[0]
                            client.sendall(bytes([Valore_categoria])+intestazione_VALORE+IDENTICO_VALORE(server_VALORE,articolo_CONTA_NUMERI*6))
                        elif Valore_categoria==2:client.sendall(bytes([Valore_categoria]))
                        elif Valore_categoria==3:
                            intestazione_VALORE=IDENTICO_VALORE(server_VALORE,7);articolo_CONTA_NUMERI=struct.unpack('>I',intestazione_VALORE[3:])[0]
                            if articolo_CONTA_NUMERI>1048576:raise ValueError('server clipboard too large')
                            client.sendall(bytes([Valore_categoria])+intestazione_VALORE+IDENTICO_VALORE(server_VALORE,articolo_CONTA_NUMERI))
                        else:raise ValueError('unexpected RFB server message: '+str(Valore_categoria))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:client.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            esecutoreAsincrono=threading.Thread(target=output,daemon=True);esecutoreAsincrono.start()
            while not 자신.reparto_IT_chiusa:
                Valore_categoria=IDENTICO_VALORE(client,1)[0]
                if Valore_categoria==4:
                    corpo_del_testo=IDENTICO_VALORE(client,7); tastiera_voce.누름값(corpo_del_testo[0]!=0,struct.unpack('>I',corpo_del_testo[3:])[0]); continue
                if Valore_categoria==255:
                    corpo_del_testo=IDENTICO_VALORE(client,11)
                    if corpo_del_testo[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastiera_voce.누름값(struct.unpack('>H',corpo_del_testo[1:3])[0]!=0,struct.unpack('>I',corpo_del_testo[3:7])[0]); continue
                if Valore_categoria==5:
                    corpo_del_testo=IDENTICO_VALORE(client,5); 단추들,coordinata_x,Y_coordinata=struct.unpack('>BHH',corpo_del_testo)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tastiera_voce.한글조합기.commit_composizione()
                    if 눌림&1 and 자신.시작화면 and 64<=coordinata_x<576 and 112<=Y_coordinata<372:
                        CERCA_INDICE=(Y_coordinata-112)//52
                        if (Y_coordinata-112)%52<40 and CERCA_INDICE<5: 자신.inviare(bytes([ord('1')+CERCA_INDICE]))
                    else: 자신.inviare(bytes([30,1,단추들,coordinata_x&255,coordinata_x>>8,Y_coordinata&255,Y_coordinata>>8]))
                    continue
                if Valore_categoria==6:
                    corpo_del_testo=IDENTICO_VALORE(client,7); durata_VALORE=struct.unpack('>i',corpo_del_testo[3:])[0]
                    if abs(durata_VALORE)>65536: raise ValueError('clipboard too large')
                    testo=IDENTICO_VALORE(client,abs(durata_VALORE))
                    if durata_VALORE>=0:
                        try: tastiera_voce.Appunti_VALORE=testo.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastiera_voce.Appunti_VALORE=testo.decode('latin-1').encode('utf-8')
                        tastiera_voce.Appunti_VALORE=tastiera_voce.Appunti_VALORE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALORE.sendall(bytes([Valore_categoria])+corpo_del_testo+testo); continue
                if Valore_categoria==0:
                    corpo_del_testo=IDENTICO_VALORE(client,19)
                    if corpo_del_testo[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=corpo_del_testo[3]//8
                elif Valore_categoria==2:
                    corpo_del_testo=IDENTICO_VALORE(client,3); voce_CONTA_NUMERI=struct.unpack('>H',corpo_del_testo[1:])[0]
                    if voce_CONTA_NUMERI>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(voce_CONTA_NUMERI)+'i',IDENTICO_VALORE(client,voce_CONTA_NUMERI*4))
                    포인터지원=-239 in 부호들
                    # 로컬 schermata 중계는 valore_predefinito Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    corpo_del_testo=struct.pack('>BHi',0,1,0)
                elif Valore_categoria in (3,150): corpo_del_testo=IDENTICO_VALORE(client,9)
                elif Valore_categoria==248:
                    corpo_del_testo=IDENTICO_VALORE(client,8)
                    if corpo_del_testo[7]>64: raise ValueError('fence too large')
                    corpo_del_testo+=IDENTICO_VALORE(client,corpo_del_testo[7])
                elif Valore_categoria==250: corpo_del_testo=IDENTICO_VALORE(client,3)
                elif Valore_categoria==251:
                    corpo_del_testo=IDENTICO_VALORE(client,7)
                    if corpo_del_testo[5]>16: raise ValueError('too many screens')
                    corpo_del_testo+=IDENTICO_VALORE(client,corpo_del_testo[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(Valore_categoria))
                server_VALORE.sendall(bytes([Valore_categoria])+corpo_del_testo)
        except (OSError,EOFError,ValueError) as errore:
            if str(errore): print('VNC client:',errore,file=sys.stderr,flush=True)
        finally:
            for socket_VALORE in (client,server_VALORE):
                try: socket_VALORE.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                socket_VALORE.close()


def eseguire_PC(numero_di_porta=5902, rete=False, trasferimento_di_file_numero_di_porta=2121, 전달규칙들=(), risoluzione_VALORE=(640, 480), guest_e_mail=None, ID_host='127.0.0.1'):
    with ExitStack() as Risorse, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        bridge_voce = None
        if rete:
            from bridge_3de4fe3a import bridge_3de4fe3a
            bridge_voce = Risorse.enter_context(bridge_3de4fe3a(trasferimento_di_file_numero_di_porta, 전달규칙들, guest_e_mail=guest_e_mail, ID_host=ID_host))
        percorso=Path(작업경로)/'display.sock'
        with socket.socket() as porta_di_ricezione:
            porta_di_ricezione.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            porta_di_ricezione.bind(('127.0.0.1',numero_di_porta)); porta_di_ricezione.listen(1); porta_di_ricezione.settimeout(.2)
            원격화면접속번호=porta_di_ricezione.getsockname()[1]
            if bridge_voce and (원격화면접속번호==trasferimento_di_file_numero_di_porta or 50000<=원격화면접속번호<=50007 or any(rete_ABI=='tcp' and host==원격화면접속번호 for rete_ABI,host,_ in bridge_voce.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Processi=subprocess.Popen(comando(risoluzione_VALORE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(percorso)]+(bridge_voce.전달인수() if bridge_voce else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            bridge=CONNETTI_PC(Processi); Lettore=threading.Thread(target=bridge.직렬입출력,daemon=True); Lettore.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(porta_di_ricezione.getsockname()[1]),flush=True)
            if bridge_voce: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ID_host,trasferimento_di_file_numero_di_porta),flush=True)
            def terminare(segnale_numero,esecuzione_frame): raise KeyboardInterrupt()
            Indietro=signal.signal(signal.SIGTERM,terminare)
            elaborazione_task=None; 가로채기됨=False
            try:
                while Processi.poll() is None:
                    try: client,_=porta_di_ricezione.accept()
                    except socket.timeout: continue
                    if elaborazione_task is not None and elaborazione_task.is_alive(): client.close(); continue
                    if not percorso.exists(): client.close(); continue
                    elaborazione_task=threading.Thread(target=bridge.client,args=(client,percorso),daemon=True); elaborazione_task.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                bridge.reparto_IT_chiusa=True
                if bridge_voce: bridge_voce.Pause_evento.set()
                if Processi.poll() is None:
                    Processi.terminate()
                    try: Processi.wait(timeout=5)
                    except subprocess.TimeoutExpired: Processi.kill(); Processi.wait()
                Lettore.join(timeout=2); Processi.stdin.close(); Processi.stdout.close(); signal.signal(signal.SIGTERM,Indietro)
            if bridge_voce and bridge_voce.errore: raise RuntimeError('network bridge: '+bridge_voce.errore)
            return 0 if 가로채기됨 else Processi.returncode


if __name__=='__main__':
    from Esegui_comando import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    argomento_array=parser.parse_args()
    if argomento_array.forward and not argomento_array.network: parser.error('--forward requires --network')
    raise SystemExit(eseguire_PC(argomento_array.port,rete=argomento_array.network,trasferimento_di_file_numero_di_porta=argomento_array.ftp_port,전달규칙들=argomento_array.forward,risoluzione_VALORE=argomento_array.resolution))
