#!/usr/bin/env python3
"""datosEfectivo RFB 클라이언트로 QEMU 창의 한글/valorTecla/클립보드/마우스와 Pantalla 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from vistaEscritorio import valorExacto
from ejecutarComando import raízProyecto


def ponerEnMarcha():
    salida=raízProyecto/'build/verification/desktop'; salida.mkdir(parents=True,exist_ok=True)
    proceso=subprocess.Popen(['python3',str(raízProyecto/'Herramientas/vistaEscritorio.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    monitorEstadoDisponibilidad=selectors.DefaultSelector(); monitorEstadoDisponibilidad.register(proceso.stdout,selectors.EVENT_READ)
    transcripción=bytearray(); informeValidación={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest()}
    def hasta(marcador,ponerEnMarcha=0):
        tiempoPlazo=time.monotonic()+45
        while marcador not in transcripción[ponerEnMarcha:]:
            if time.monotonic()>tiempoPlazo or proceso.poll() is not None: raise AssertionError(transcripción[ponerEnMarcha:].decode('utf-8','replace'))
            for valorPulsado,_ in monitorEstadoDisponibilidad.select(.1):
                Datos=valorPulsado.fileobj.read(4096)
                if Datos: transcripción.extend(Datos)
        return bytes(transcripción[ponerEnMarcha:])
    try:
        hasta(b'TERMINAL READY')
        númeroPuerto=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcripción).group(1))
        with socket.create_connection(('127.0.0.1',númeroPuerto),timeout=10) as cliente:
            assert valorExacto(cliente,12)==b'RFB 003.008\n'; cliente.sendall(b'RFB 003.008\n')
            assert 1 in valorExacto(cliente,valorExacto(cliente,1)[0]); cliente.sendall(b'\x01'); assert valorExacto(cliente,4)==b'\0'*4
            cliente.sendall(b'\x01'); valorInicialValor=valorExacto(cliente,24); assert struct.unpack('>HH',valorInicialValor[:4])==(640,480); valorExacto(cliente,struct.unpack('>I',valorInicialValor[20:])[0])
            cliente.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            cliente.sendall(struct.pack('>BBHi',2,0,1,0))
            def valorPulsado(valorSímbolo,esPulsaciónEnCurso=True): cliente.sendall(struct.pack('>BBHI',4,int(esPulsaciónEnCurso),0,valorSímbolo))
            def carácterIngresado(texto):
                for datosCarácter in texto:
                    símbolo=0xff0d if datosCarácter=='\n' else ord(datosCarácter) if ord(datosCarácter)<256 else 0x01000000|ord(datosCarácter)
                    valorPulsado(símbolo); valorPulsado(símbolo,False)
            def teclaPulsar(valorSímbolo): valorPulsado(valorSímbolo); valorPulsado(valorSímbolo,False)
            # Start with English keys only, as delivered without a host IME.
            valorDesfase=len(transcripción); carácterIngresado('echo '); teclaPulsar(0xffc6)
            carácterIngresado('dkssudgktpdy gksrmf'); teclaPulsar(0xffc6); carácterIngresado('\n')
            hasta('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('echo ')
            valorPulsado(0xffe1); teclaPulsar(32); valorPulsado(0xffe1,False)
            carácterIngresado('dlfr'); teclaPulsar(0xff08); teclaPulsar(0xff08); carácterIngresado('fr')
            teclaPulsar(0xff31); carácterIngresado(' EN\n')
            hasta('\r\n읽 EN\r\njkoros-native> '.encode(),valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('echo '); teclaPulsar(0xff31)
            carácterIngresado('rhk rkqtk RkRnd'); teclaPulsar(0xff31); carácterIngresado('\n')
            hasta('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),valorDesfase)
            # The same composition edits UTF-8 text in the native vi editor.
            valorDesfase=len(transcripción); carácterIngresado('vi entradaHangul.txt\n'); hasta(b'NORMAL',valorDesfase)
            carácterIngresado('i'); teclaPulsar(0xffc6); carácterIngresado('gksrmf dlfr'); teclaPulsar(0xffc6)
            teclaPulsar(0xff1b); carácterIngresado(':wq\n'); hasta(b'jkoros-native> ',valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('cat entradaHangul.txt\n')
            hasta('한글 읽'.encode(),valorDesfase); hasta(b'jkoros-native> ',valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('help ko\n')
            hasta('한/operandoCero valorTecla, Shift+Space 또는 F9'.encode(),valorDesfase); hasta(b'jkoros-native> ',valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('clear\necho "VNC 한글 valorEntrada 😀"\n'); hasta('VNC 한글 valorEntrada 😀\r\n'.encode(),valorDesfase)
            valorDesfase=len(transcripción); valorPulsado(0xffe3); valorPulsado(ord('u')); valorPulsado(ord('u'),False); valorPulsado(0xffe3,False); carácterIngresado('echo CONTROL_OK\n'); hasta(b'\r\nCONTROL_OK\r\n',valorDesfase)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            valorPortapapeles='echo "valorPegar esTerminado"\n'.encode(); valorDesfase=len(transcripción)
            cliente.sendall(struct.pack('>B3xI',6,len(valorPortapapeles))+valorPortapapeles)
            for evento,_ in monitorEstadoDisponibilidad.select(.15):
                bloqueDatos=evento.fileobj.read(4096)
                if bloqueDatos: transcripción.extend(bloqueDatos)
            assert 'valorPegar esTerminado'.encode() not in transcripción[valorDesfase:]
            valorPulsado(0xffe3); valorPulsado(0xffe1); valorPulsado(ord('v')); valorPulsado(ord('v'),False); valorPulsado(0xffe1,False); valorPulsado(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            hasta('\r\n붙여넣기 esTerminado\r\njkoros-native> '.encode(),valorDesfase)
            cliente.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            colorRGB=bytearray(640*480*3); entradasVisto=False
            while not entradasVisto:
                textoNotificación=valorExacto(cliente,1)[0]
                if textoNotificación==2: continue
                if textoNotificación==3:
                    tamaño=struct.unpack('>I',valorExacto(cliente,7)[3:])[0]; valorExacto(cliente,tamaño); continue
                assert textoNotificación==0,textoNotificación
                listaRectángulos=struct.unpack('>H',valorExacto(cliente,3)[1:])[0]
                for _ in range(listaRectángulos):
                    coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,valorAnchuraSolicitado,valorAlturaSolicitado,juegoCaracteres=struct.unpack('>HHHHi',valorExacto(cliente,12)); assert juegoCaracteres==0,juegoCaracteres
                    listaPíxeles=valorExacto(cliente,valorAnchuraSolicitado*valorAlturaSolicitado*4)
                    for ordinalInterior in range(valorAlturaSolicitado):
                        for índiceOrdinal in range(valorAnchuraSolicitado):
                            direcciónOriginal=(ordinalInterior*valorAnchuraSolicitado+índiceOrdinal)*4; direcciónDestino=((coordenadaCoordenadaVertical+ordinalInterior)*640+coordenadaCoordenadaHorizontal+índiceOrdinal)*3
                            colorRGB[direcciónDestino:direcciónDestino+3]=bytes((listaPíxeles[direcciónOriginal+2],listaPíxeles[direcciónOriginal+1],listaPíxeles[direcciónOriginal]))
                    entradasVisto=True
            assert colorRGB[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (salida/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+colorRGB)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(colorRGB)).save(str(salida/'vnc-terminal.png'))
            valorDesfase=len(transcripción)
            valorPulsado(0xffe3); valorPulsado(0xffe1); valorPulsado(ord('t')); valorPulsado(ord('t'),False); valorPulsado(0xffe1,False); valorPulsado(0xffe3,False)
            hasta(b'TERMINAL FOCUS 2',valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('echo SECOND_VNC_WINDOW\n'); hasta(b'\r\nSECOND_VNC_WINDOW\r\n',valorDesfase)
            valorDesfase=len(transcripción); cliente.sendall(struct.pack('>BBHH',5,1,576,81)); cliente.sendall(struct.pack('>BBHH',5,0,576,81)); hasta(b'TERMINAL FOCUS 1',valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('python -c \'print("x"*9000)\'\n'); hasta(b'\r\njkoros-native> ',valorDesfase)
            assert len(transcripción)-valorDesfase>8192,'exercise output longer than bridge status buffer'
            valorDesfase=len(transcripción); cliente.sendall(struct.pack('>BBHH',5,1,560,63)); cliente.sendall(struct.pack('>BBHH',5,0,560,63)); hasta(b'TERMINAL FOCUS 1',valorDesfase)
            valorDesfase=len(transcripción); cliente.sendall(struct.pack('>BBHH',5,1,80,16)); cliente.sendall(struct.pack('>BBHH',5,0,80,16)); hasta(b'TERMINAL FOCUS 1',valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('echo REOPENED_VNC_WINDOW\n'); hasta(b'\r\nREOPENED_VNC_WINDOW\r\n',valorDesfase)
            valorDesfase=len(transcripción); carácterIngresado('gui\n'); hasta(b'GUI READY:',valorDesfase)
            valorDesfase=len(transcripción); cliente.sendall(struct.pack('>BBHH',5,1,80,332)); cliente.sendall(struct.pack('>BBHH',5,0,80,332)); hasta(b'TERMINAL READY',valorDesfase)
            informeValidación.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if proceso.poll() is None:
            proceso.terminate()
            try: proceso.wait(timeout=8)
            except subprocess.TimeoutExpired: proceso.kill(); proceso.wait()
        monitorEstadoDisponibilidad.close(); proceso.stdout.close()
        (salida/'serial.log').write_bytes(transcripción)
        (salida/'report.json').write_text(json.dumps(informeValidación,indent=2)+'\n')


if __name__=='__main__': ponerEnMarcha()
