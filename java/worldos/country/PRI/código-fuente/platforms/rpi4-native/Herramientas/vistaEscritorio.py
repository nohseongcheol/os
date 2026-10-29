#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, valorTecla 입력은 propio valorNúcleo UART로 전달한다. localhost 전용, 단일 valorControl 클라이언트.
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
from ejecutarComando import comando
from local_input import create


def valorExacto(valorConectorRed, tamaño):
    Datos = bytearray()
    while len(Datos) < tamaño:
        valorFragmento = valorConectorRed.recv(tamaño - len(Datos))
        if not valorFragmento: raise EOFError()
        Datos.extend(valorFragmento)
    return bytes(Datos)


class Teclado:
    def __init__(valorPropio, enviar, cambiadoModo=None):
        valorPropio.bytesTransferencia = enviar; valorPropio.teclaModificador = set(); valorPropio.valorPortapapeles = b''
        valorPropio.ComponedorHangul = create(enviar, Path(__file__).resolve().parents[1]); valorPropio.coreano = False; valorPropio.teclaConmutar = set()
        valorPropio.entradaUnicode = None
        valorPropio.cambiadoModo = cambiadoModo
        if cambiadoModo: cambiadoModo(False)

    def enviar(valorPropio, Datos):
        valorPropio.ComponedorHangul.composiciónConfirmar()
        valorPropio.bytesTransferencia(Datos)

    def modoConmutar(valorPropio):
        valorPropio.ComponedorHangul.composiciónConfirmar(); valorPropio.coreano = not valorPropio.coreano
        if valorPropio.cambiadoModo: valorPropio.cambiadoModo(valorPropio.coreano)

    def valorPulsado(valorPropio, esPulsaciónEnCurso, símboloTecla):
        if símboloTecla in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if esPulsaciónEnCurso: valorPropio.teclaModificador.add(símboloTecla)
            else: valorPropio.teclaModificador.discard(símboloTecla)
            return
        if not esPulsaciónEnCurso:
            valorPropio.teclaConmutar.discard(símboloTecla)
            return
        teclaControl = bool(valorPropio.teclaModificador & {0xffe3, 0xffe4})
        teclaDesplazar = bool(valorPropio.teclaModificador & {0xffe1, 0xffe2})
        if teclaControl and teclaDesplazar and símboloTecla in (ord('u'),ord('U')):
            valorPropio.ComponedorHangul.composiciónConfirmar(); valorPropio.entradaUnicode = ''; return
        if valorPropio.entradaUnicode is not None:
            if símboloTecla in (32,0xff0d):
                try:
                    valor=int(valorPropio.entradaUnicode,16)
                    if 32<=valor<=0x10ffff and not 0xd800<=valor<=0xdfff: valorPropio.enviar(chr(valor).encode('utf-8'))
                except ValueError: pass
                valorPropio.entradaUnicode=None
            elif símboloTecla==0xff1b: valorPropio.entradaUnicode=None
            elif símboloTecla==0xff08: valorPropio.entradaUnicode=valorPropio.entradaUnicode[:-1]
            elif símboloTecla<128 and chr(símboloTecla) in '0123456789abcdefABCDEF' and len(valorPropio.entradaUnicode)<6: valorPropio.entradaUnicode+=chr(símboloTecla)
            return
        if símboloTecla in (0xff31,0xffc6) or símboloTecla==32 and teclaDesplazar and not teclaControl:
            if símboloTecla not in valorPropio.teclaConmutar: valorPropio.modoConmutar()
            valorPropio.teclaConmutar.add(símboloTecla)
            return
        if símboloTecla==0xff08 and valorPropio.coreano and not teclaControl and valorPropio.ComponedorHangul.retroceso(): return
        if teclaControl and teclaDesplazar and símboloTecla in (ord('t'),ord('T')):
            valorPropio.enviar(bytes([30,2,1,0,0,0,0])); return
        if símboloTecla==0xffc3: valorPropio.enviar(bytes([30,2,2,0,0,0,0])); return
        if símboloTecla==0xffc9: valorPropio.enviar(bytes([30,2,3,0,0,0,0])); return
        if teclaControl and teclaDesplazar and símboloTecla in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            valorPropio.enviar(valorPropio.valorPortapapeles); return
        teclaEspecial = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if símboloTecla in teclaEspecial: valorPropio.enviar(teclaEspecial[símboloTecla]); return
        codificaciónEstadoCarácter = símboloTecla & 0xffffff if símboloTecla & 0xff000000 == 0x01000000 else símboloTecla
        if codificaciónEstadoCarácter > 0x10ffff or 0xd800 <= codificaciónEstadoCarácter <= 0xdfff or símboloTecla >= 0xff00 and símboloTecla < 0x1000000: return
        if teclaControl and 0x40 <= codificaciónEstadoCarácter <= 0x7f: valorPropio.enviar(bytes([codificaciónEstadoCarácter & 31])); return
        if codificaciónEstadoCarácter < 32: return
        if valorPropio.coreano and valorPropio.teclaModificador & {0xffea,0xfe03,0xff7e} and not teclaControl and hasattr(valorPropio.ComponedorHangul, 'profile'):
            if valorPropio.ComponedorHangul.teclaAlimentar(chr(codificaciónEstadoCarácter), altgr=True): return
        partePrevio = b'\x1b' if valorPropio.teclaModificador & {0xffe9, 0xffea} else b''
        if valorPropio.coreano and not teclaControl and not partePrevio and 32<=codificaciónEstadoCarácter<127:
            datosCarácter=chr(codificaciónEstadoCarácter).upper() if teclaDesplazar else chr(codificaciónEstadoCarácter)
            if valorPropio.ComponedorHangul.teclaAlimentar(datosCarácter): return
        valorPropio.enviar(partePrevio + chr(codificaciónEstadoCarácter).encode('utf-8'))


class conectarEscritorio:
    def __init__(valorPropio, proceso):
        valorPropio.proceso=proceso; valorPropio.valorCerrojo=threading.Lock(); valorPropio.terminadoPreparación=False; valorPropio.terminal=False; valorPropio.pantallaInicialValor=False; valorPropio.esCerrado=False

    def enviar(valorPropio, Datos):
        if not Datos or valorPropio.esCerrado: return
        with valorPropio.valorCerrojo:
            try: valorPropio.proceso.stdin.write(Datos); valorPropio.proceso.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def entradaSalidaSerie(valorPropio):
        parteTerminación=b''
        try:
            while True:
                Datos=valorPropio.proceso.stdout.read(4096)
                if not Datos: break
                sys.stdout.buffer.write(Datos); sys.stdout.buffer.flush()
                parteTerminación=(parteTerminación+Datos)[-8192:]
                abierto=parteTerminación.rfind(b'TERMINAL READY'); esCerrado=parteTerminación.rfind(b'TERMINAL CLOSED'); pantallaDibujo=parteTerminación.rfind(b'GUI READY:'); tieneSalido=parteTerminación.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(abierto,esCerrado,pantallaDibujo,tieneSalido)>=0:
                    valorPropio.terminal=abierto>max(esCerrado,pantallaDibujo,tieneSalido)
                    valorPropio.pantallaInicialValor=pantallaDibujo>max(abierto,esCerrado,tieneSalido)
                if not valorPropio.terminadoPreparación and b'jkoros-native> ' in parteTerminación:
                    valorPropio.terminadoPreparación=True; valorPropio.enviar(b'terminal\n')
        finally: valorPropio.esCerrado=True

    def cliente(valorPropio, cliente, ruta):
        valorServidor=socket.socket(socket.AF_UNIX); valorServidor.settimeout(10); cliente.settimeout(10)
        entradaElementoTeclado=Teclado(valorPropio.enviar,lambda coreano:valorPropio.enviar(bytes([30,3,int(coreano),0,0,0,0])))
        botonesElementoPrevio=0
        try:
            valorServidor.connect(str(ruta))
            # estadoValorInicialValor 협상은 순서대로 끝낸다. valorDespués Salida 가닥만 클라이언트에 쓴다.
            cliente.sendall(valorExacto(valorServidor,12))
            númeroVersión=valorExacto(cliente,12)
            if númeroVersión not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            valorServidor.sendall(númeroVersión)
            númeroElementosElementoLista=valorExacto(valorServidor,1);cliente.sendall(númeroElementosElementoLista+valorExacto(valorServidor,númeroElementosElementoLista[0]))
            seguridad=valorExacto(cliente,1)
            if seguridad!=b'\x01': raise ValueError('unexpected security type')
            valorServidor.sendall(seguridad)
            if númeroVersión==b'RFB 003.008\n':cliente.sendall(valorExacto(valorServidor,4))
            valorServidor.sendall(valorExacto(cliente,1))
            valorInicialValor=valorExacto(valorServidor,24)
            cliente.sendall(valorInicialValor+valorExacto(valorServidor,struct.unpack('>I',valorInicialValor[20:])[0]))
            bytesPíxel=valorInicialValor[4]//8;admitidoPuntero=False
            cliente.settimeout(None);valorServidor.settimeout(None)
            def salida():
                try:
                    while True:
                        valorCategoría=valorExacto(valorServidor,1)[0]
                        if valorCategoría==0:
                            valorCabecera=valorExacto(valorServidor,3);númeroElementosEntradaElemento=struct.unpack('>H',valorCabecera[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 valorRemoto 포인터의 중복을 피한다.
                            valorOculto=admitidoPuntero
                            if valorOculto:cliente.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            cliente.sendall(bytes([valorCategoría])+valorCabecera)
                            for _ in range(númeroElementosEntradaElemento):
                                rectángulo=valorExacto(valorServidor,12);posiciónHorizontal,posiciónVertical,extensiónRangoAnchura,valorAltura,valorCodificaciónEstado=struct.unpack('>HHHHi',rectángulo)
                                if valorCodificaciónEstado!=0:raise ValueError('unexpected framebuffer encoding: '+str(valorCodificaciónEstado))
                                cliente.sendall(rectángulo)
                                datosRestoDivisión=extensiónRangoAnchura*valorAltura*bytesPíxel
                                while datosRestoDivisión:
                                    Datos=valorExacto(valorServidor,min(datosRestoDivisión,65536));cliente.sendall(Datos);datosRestoDivisión-=len(Datos)
                        elif valorCategoría==1:
                            valorCabecera=valorExacto(valorServidor,5);númeroElementosElementoLista=struct.unpack('>H',valorCabecera[3:])[0]
                            cliente.sendall(bytes([valorCategoría])+valorCabecera+valorExacto(valorServidor,númeroElementosElementoLista*6))
                        elif valorCategoría==2:cliente.sendall(bytes([valorCategoría]))
                        elif valorCategoría==3:
                            valorCabecera=valorExacto(valorServidor,7);númeroElementosElementoLista=struct.unpack('>I',valorCabecera[3:])[0]
                            if númeroElementosElementoLista>1048576:raise ValueError('server clipboard too large')
                            cliente.sendall(bytes([valorCategoría])+valorCabecera+valorExacto(valorServidor,númeroElementosElementoLista))
                        else:raise ValueError('unexpected RFB server message: '+str(valorCategoría))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:cliente.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            tareaFondo=threading.Thread(target=salida,daemon=True);tareaFondo.start()
            while not valorPropio.esCerrado:
                valorCategoría=valorExacto(cliente,1)[0]
                if valorCategoría==4:
                    textoCuerpo=valorExacto(cliente,7); entradaElementoTeclado.valorPulsado(textoCuerpo[0]!=0,struct.unpack('>I',textoCuerpo[3:])[0]); continue
                if valorCategoría==255:
                    textoCuerpo=valorExacto(cliente,11)
                    if textoCuerpo[0]!=0: raise ValueError('unsupported QEMU input extension')
                    entradaElementoTeclado.valorPulsado(struct.unpack('>H',textoCuerpo[1:3])[0]!=0,struct.unpack('>I',textoCuerpo[3:7])[0]); continue
                if valorCategoría==5:
                    textoCuerpo=valorExacto(cliente,5); botones,coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical=struct.unpack('>BHH',textoCuerpo)
                    esPulsado=botones&~botonesElementoPrevio; botonesElementoPrevio=botones
                    if esPulsado: entradaElementoTeclado.ComponedorHangul.composiciónConfirmar()
                    if esPulsado&1 and valorPropio.pantallaInicialValor and 64<=coordenadaCoordenadaHorizontal<576 and 112<=coordenadaCoordenadaVertical<372:
                        índiceBuscar=(coordenadaCoordenadaVertical-112)//52
                        if (coordenadaCoordenadaVertical-112)%52<40 and índiceBuscar<5: valorPropio.enviar(bytes([ord('1')+índiceBuscar]))
                    else: valorPropio.enviar(bytes([30,1,botones,coordenadaCoordenadaHorizontal&255,coordenadaCoordenadaHorizontal>>8,coordenadaCoordenadaVertical&255,coordenadaCoordenadaVertical>>8]))
                    continue
                if valorCategoría==6:
                    textoCuerpo=valorExacto(cliente,7); longitud=struct.unpack('>i',textoCuerpo[3:])[0]
                    if abs(longitud)>65536: raise ValueError('clipboard too large')
                    texto=valorExacto(cliente,abs(longitud))
                    if longitud>=0:
                        try: entradaElementoTeclado.valorPortapapeles=texto.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: entradaElementoTeclado.valorPortapapeles=texto.decode('latin-1').encode('utf-8')
                        entradaElementoTeclado.valorPortapapeles=entradaElementoTeclado.valorPortapapeles[:65536].decode('utf-8','ignore').encode('utf-8')
                    valorServidor.sendall(bytes([valorCategoría])+textoCuerpo+texto); continue
                if valorCategoría==0:
                    textoCuerpo=valorExacto(cliente,19)
                    if textoCuerpo[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    bytesPíxel=textoCuerpo[3]//8
                elif valorCategoría==2:
                    textoCuerpo=valorExacto(cliente,3); númeroElementosEntradaElemento=struct.unpack('>H',textoCuerpo[1:])[0]
                    if númeroElementosEntradaElemento>512: raise ValueError('too many encodings')
                    valoresCodificado=struct.unpack('>'+str(númeroElementosEntradaElemento)+'i',valorExacto(cliente,númeroElementosEntradaElemento*4))
                    admitidoPuntero=-239 in valoresCodificado
                    # 로컬 Pantalla 중계는 valorPredeterminado Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    textoCuerpo=struct.pack('>BHi',0,1,0)
                elif valorCategoría in (3,150): textoCuerpo=valorExacto(cliente,9)
                elif valorCategoría==248:
                    textoCuerpo=valorExacto(cliente,8)
                    if textoCuerpo[7]>64: raise ValueError('fence too large')
                    textoCuerpo+=valorExacto(cliente,textoCuerpo[7])
                elif valorCategoría==250: textoCuerpo=valorExacto(cliente,3)
                elif valorCategoría==251:
                    textoCuerpo=valorExacto(cliente,7)
                    if textoCuerpo[5]>16: raise ValueError('too many screens')
                    textoCuerpo+=valorExacto(cliente,textoCuerpo[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(valorCategoría))
                valorServidor.sendall(bytes([valorCategoría])+textoCuerpo)
        except (OSError,EOFError,ValueError) as error:
            if str(error): print('VNC client:',error,file=sys.stderr,flush=True)
        finally:
            for valorConectorRed in (cliente,valorServidor):
                try: valorConectorRed.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                valorConectorRed.close()


def ponerEnMarchaEscritorio(númeroPuerto=5902, red=False, númeroPuertoTransferenciaArchivo=2121, reglasReenvíoEnCurso=(), valorResolución=(640, 480), direcciónInvitado=None, direcciónAnfitrión='127.0.0.1'):
    with ExitStack() as recursos, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as rutaTrabajoEnCurso:
        entradaElementoPuenteRed = None
        if red:
            from puenteRed import puenteRed
            entradaElementoPuenteRed = recursos.enter_context(puenteRed(númeroPuertoTransferenciaArchivo, reglasReenvíoEnCurso, direcciónInvitado=direcciónInvitado, direcciónAnfitrión=direcciónAnfitrión))
        ruta=Path(rutaTrabajoEnCurso)/'display.sock'
        with socket.socket() as recibirPuerto:
            recibirPuerto.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            recibirPuerto.bind(('127.0.0.1',númeroPuerto)); recibirPuerto.listen(1); recibirPuerto.settimeout(.2)
            puertoVNC=recibirPuerto.getsockname()[1]
            if entradaElementoPuenteRed and (puertoVNC==númeroPuertoTransferenciaArchivo or 50000<=puertoVNC<=50007 or any(ABIRed=='tcp' and Anfitrión==puertoVNC for ABIRed,Anfitrión,_ in entradaElementoPuenteRed.reglasReenvíoEnCurso)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            proceso=subprocess.Popen(comando(valorResolución)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ruta)]+(entradaElementoPuenteRed.argumentoReenviado() if entradaElementoPuenteRed else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            puente=conectarEscritorio(proceso); lector=threading.Thread(target=puente.entradaSalidaSerie,daemon=True); lector.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(recibirPuerto.getsockname()[1]),flush=True)
            if entradaElementoPuenteRed: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(direcciónAnfitrión,númeroPuertoTransferenciaArchivo),flush=True)
            def terminarProceso(númeroSeñal,marcoEjecución): raise KeyboardInterrupt()
            elementoPrevio=signal.signal(signal.SIGTERM,terminarProceso)
            tareaProcesamiento=None; interrumpido=False
            try:
                while proceso.poll() is None:
                    try: cliente,_=recibirPuerto.accept()
                    except socket.timeout: continue
                    if tareaProcesamiento is not None and tareaProcesamiento.is_alive(): cliente.close(); continue
                    if not ruta.exists(): cliente.close(); continue
                    tareaProcesamiento=threading.Thread(target=puente.cliente,args=(cliente,ruta),daemon=True); tareaProcesamiento.start()
            except KeyboardInterrupt: interrumpido=True
            finally:
                puente.esCerrado=True
                if entradaElementoPuenteRed: entradaElementoPuenteRed.eventoPausar.set()
                if proceso.poll() is None:
                    proceso.terminate()
                    try: proceso.wait(timeout=5)
                    except subprocess.TimeoutExpired: proceso.kill(); proceso.wait()
                lector.join(timeout=2); proceso.stdin.close(); proceso.stdout.close(); signal.signal(signal.SIGTERM,elementoPrevio)
            if entradaElementoPuenteRed and entradaElementoPuenteRed.error: raise RuntimeError('network bridge: '+entradaElementoPuenteRed.error)
            return 0 if interrumpido else proceso.returncode


if __name__=='__main__':
    from ejecutarComando import leerResolución
    analizador=argparse.ArgumentParser(description=__doc__); analizador.add_argument('--port',type=int,default=5902)
    analizador.add_argument('--resolution',type=leerResolución,default=(640,480))
    analizador.add_argument('--network',action='store_true'); analizador.add_argument('--ftp-port',type=int,default=2121)
    analizador.add_argument('--forward',action='append',default=[])
    arregloArgumento=analizador.parse_args()
    if arregloArgumento.forward and not arregloArgumento.network: analizador.error('--forward requires --network')
    raise SystemExit(ponerEnMarchaEscritorio(arregloArgumento.port,red=arregloArgumento.network,númeroPuertoTransferenciaArchivo=arregloArgumento.ftp_port,reglasReenvíoEnCurso=arregloArgumento.forward,valorResolución=arregloArgumento.resolution))
