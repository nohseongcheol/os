#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from vistaEscritorio import valorExacto
from ServidorEcoEjemplo import ServidoresRepetirEntrada
from ejecutarComando import raízProyecto


def pruebaLengua(Lengua,entradaElementoServidorRepetirEntrada,datosResultado):
    with socket.socket() as temporal:
        temporal.bind(('127.0.0.1',0));númeroPuertoTransferenciaArchivo=temporal.getsockname()[1]
    proceso=subprocess.Popen(['python3',str(raízProyecto/'Herramientas/ejecutarComando.py'),'--desktop','--network','--port','0','--ftp-port',str(númeroPuertoTransferenciaArchivo)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selector=selectors.DefaultSelector();selector.register(proceso.stdout,selectors.EVENT_READ)
    transcripción=bytearray();cliente=None;conexiónTransferenciaArchivo=None
    def recibirMensaje(marcador,ponerEnMarcha=0):
        desfaseFin=time.monotonic()+60
        while marcador not in transcripción[ponerEnMarcha:]:
            if time.monotonic()>desfaseFin or proceso.poll() is not None:raise AssertionError(transcripción[ponerEnMarcha:].decode('utf-8','replace'))
            for valorPulsado,_ in selector.select(.1):
                Datos=valorPulsado.fileobj.read(65536)
                if Datos:transcripción.extend(Datos)
        return transcripción[ponerEnMarcha:].decode('utf-8','replace').replace('\r\n','\n')
    def valorPulsado(valorSímbolo,esPulsaciónEnCurso=True):cliente.sendall(struct.pack('>BBHI',4,int(esPulsaciónEnCurso),0,valorSímbolo))
    def iniciarDesfase(línea):
        ponerEnMarcha=len(transcripción)
        for códigoCarácter in línea+'\n':
            valorSímbolo=0xff0d if códigoCarácter=='\n' else ord(códigoCarácter) if ord(códigoCarácter)<256 else 0x1000000|ord(códigoCarácter)
            valorPulsado(valorSímbolo);valorPulsado(valorSímbolo,False)
        return ponerEnMarcha
    def intérpreteComandos(línea):return recibirMensaje(b'jkoros-native> ',iniciarDesfase(línea))
    def ejecutarComando(línea,esperado):
        texto=intérpreteComandos(línea);assert esperado in texto and 'exit 0' in texto,(línea,texto)
        return texto
    def listaPíxeles():
        cliente.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        colorRGB=bytearray(640*480*3)
        while True:
            valorCategoría=valorExacto(cliente,1)[0]
            if valorCategoría==2:continue
            if valorCategoría==3:
                númeroElementosElementoLista=struct.unpack('>I',valorExacto(cliente,7)[3:])[0];valorExacto(cliente,númeroElementosElementoLista);continue
            assert valorCategoría==0,valorCategoría
            númeroElementosEntradaElemento=struct.unpack('>H',valorExacto(cliente,3)[1:])[0]
            for _ in range(númeroElementosEntradaElemento):
                coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,valorAnchuraSolicitado,valorAlturaSolicitado,juegoCaracteres=struct.unpack('>HHHHi',valorExacto(cliente,12));assert juegoCaracteres==0,juegoCaracteres
                Datos=valorExacto(cliente,valorAnchuraSolicitado*valorAlturaSolicitado*4)
                for posiciónFila in range(valorAlturaSolicitado):
                    for posiciónColumna in range(valorAnchuraSolicitado):
                        datosOriginal=(posiciónFila*valorAnchuraSolicitado+posiciónColumna)*4;valorObjetivo=((coordenadaCoordenadaVertical+posiciónFila)*640+coordenadaCoordenadaHorizontal+posiciónColumna)*3
                        colorRGB[valorObjetivo:valorObjetivo+3]=bytes((Datos[datosOriginal+2],Datos[datosOriginal+1],Datos[datosOriginal]))
            if númeroElementosEntradaElemento:return colorRGB
    try:
        recibirMensaje(b'TERMINAL READY');recibirMensaje(b'jkoros-native> ',transcripción.rfind(b'TERMINAL READY'))
        númeroPuerto=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcripción).group(1))
        cliente=socket.create_connection(('127.0.0.1',númeroPuerto),timeout=10)
        assert valorExacto(cliente,12)==b'RFB 003.008\n';cliente.sendall(b'RFB 003.008\n')
        assert 1 in valorExacto(cliente,valorExacto(cliente,1)[0]);cliente.sendall(b'\x01');assert valorExacto(cliente,4)==b'\0'*4
        cliente.sendall(b'\x01');valorInicialValor=valorExacto(cliente,24);valorExacto(cliente,struct.unpack('>I',valorInicialValor[20:])[0])
        cliente.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        cliente.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in intérpreteComandos('ftpd start')
        conexiónTransferenciaArchivo=ftplib.FTP();conexiónTransferenciaArchivo.encoding='utf-8';conexiónTransferenciaArchivo.connect('127.0.0.1',númeroPuertoTransferenciaArchivo,timeout=20);conexiónTransferenciaArchivo.login()
        datosCargaÚtil=('GUI와 FTP 동시 valorUsar '+Lengua+' 😀\n').encode()
        conexiónTransferenciaArchivo.storbinary('STOR 함께.txt',io.BytesIO(datosCargaÚtil))
        assert datosCargaÚtil.decode().strip() in intérpreteComandos('cat /함께.txt')
        númeroElementosRecibido=bytearray();conexiónTransferenciaArchivo.retrbinary('RETR 함께.txt',númeroElementosRecibido.extend);assert númeroElementosRecibido==datosCargaÚtil;conexiónTransferenciaArchivo.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        enviarLista=intérpreteComandos('ls /example')
        assert all(nombre in enviarLista for nombre in ('java/','c/','python/','README.md')),enviarLista
        if Lengua=='java':
            manifiestoPaquete=json.loads((raízProyecto/'build/examples/manifest.json').read_text())
            for ruta,puntoEntradaElemento in manifiestoPaquete.items():
                intérpreteComandos('cp '+ruta+' /example-check.bin')
                valorContenidoValor=bytearray();conexiónTransferenciaArchivo.retrbinary('RETR example-check.bin',valorContenidoValor.extend)
                assert len(valorContenidoValor)==puntoEntradaElemento['bytes'] and hashlib.sha256(valorContenidoValor).hexdigest()==puntoEntradaElemento['sha256'],ruta
            conexiónTransferenciaArchivo.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binario=bytes(range(256))*64
            conexiónTransferenciaArchivo.storbinary('STOR boundary.bin',io.BytesIO(binario))
            valorContenidoValor=bytearray();conexiónTransferenciaArchivo.retrbinary('RETR boundary.bin',valorContenidoValor.extend)
            assert valorContenidoValor==binario and 'boundary.bin' in conexiónTransferenciaArchivo.nlst()
            intérpreteComandos('cp /boundary.bin /boundary-copy.bin')
            valorContenidoValor=bytearray();conexiónTransferenciaArchivo.retrbinary('RETR boundary-copy.bin',valorContenidoValor.extend)
            assert valorContenidoValor==binario
            conexiónTransferenciaArchivo.delete('boundary.bin');conexiónTransferenciaArchivo.delete('boundary-copy.bin')
        assert 'EjemploSalida' in intérpreteComandos('ls /example/'+Lengua)
        intérpreteComandos('cd /example/'+Lengua)
        tablaNombre={'java':'JAVA','c':'C','python':'PYTHON'}[Lengua]
        archivoEsperado=tablaNombre+' Archivo: 한글 Datos 😀\n'
        if Lengua=='java':
            ejecutarComando('javac EjemploSalida.java','Compiled:');ejecutarComando('java EjemploSalida','JAVA Salida: 안녕하세요 😀')
            ejecutarComando('javac EjemploArchivo.java','Compiled:');ejecutarComando('java EjemploArchivo',archivoEsperado)
            ejecutarComando('java EjemploRed {} {}'.format(entradaElementoServidorRepetirEntrada.puertoTCP,entradaElementoServidorRepetirEntrada.puertoUDP),'JAVA 네트워크 verificar: TCP UDP 한글')
            comandoGráficos='java EjemploDibujo'
        elif Lengua=='c':
            for nombre,valorReenviado,esperado in [('Salida','', 'C Salida: 안녕하세요 😀'),('Archivo','',archivoEsperado),
                    ('네트워크',' '+str(entradaElementoServidorRepetirEntrada.puertoUDP),'C 네트워크 verificar: UDP 한글')]:
                ejecutarComando('cc '+nombre+'Ejemplos.c -o ejecutarComando','Compiled native ARM64 ELF:')
                ejecutarComando('./ejecutarComando'+valorReenviado,esperado)
            ejecutarComando('cc EjemploDibujo.c -o ejecutarComando','Compiled native ARM64 ELF:');comandoGráficos='./ejecutarComando'
        else:
            for nombre,valorReenviado,esperado in [('Salida','','PYTHON Salida: 안녕하세요 😀'),('Archivo','',archivoEsperado),
                    ('네트워크',' '+str(entradaElementoServidorRepetirEntrada.puertoUDP),'PYTHON 네트워크 verificar: UDP 한글')]:
                ejecutarComando('python '+nombre+'Ejemplos.py'+valorReenviado,esperado)
            comandoGráficos='python EjemploDibujo.py'
        iniciarDibujo=iniciarDesfase(comandoGráficos)
        texto=recibirMensaje('그림을 확인한 valorLadoPosterior Enter를 누르세요.\r\n'.encode(),iniciarDibujo)
        assert tablaNombre+' 그래픽: 빨강 초록 파랑' in texto and 'exit 0' not in texto,texto
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        conexiónTransferenciaArchivo.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        númeroElementosRecibido=bytearray();conexiónTransferenciaArchivo.retrbinary('RETR 도중.txt',númeroElementosRecibido.extend);assert númeroElementosRecibido==b'FTP DURING GRAPHICS';conexiónTransferenciaArchivo.delete('도중.txt')
        colorRGB=listaPíxeles()
        for coordenadaCoordenadaVertical,colorPíxel in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            valorDesfase=(coordenadaCoordenadaVertical*640+610)*3;assert tuple(colorRGB[valorDesfase:valorDesfase+3])==colorPíxel,(Lengua,coordenadaCoordenadaVertical,tuple(colorRGB[valorDesfase:valorDesfase+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(colorRGB)).save(str(datosResultado/(Lengua+'-graphics.png')))
        valorPulsado(0xff0d);valorPulsado(0xff0d,False)
        assert 'exit 0' in recibirMensaje(b'jkoros-native> ',iniciarDibujo)
        if Lengua=='java':
            iniciarVentana=iniciarDesfase('java EjemploVentana')
            recibirMensaje('GUI Ejemplos preparar: EjemploVentana'.encode(),iniciarVentana)
            def valorPulsarRatón(posiciónHorizontal,posiciónVertical):
                for botón in (1,0):cliente.sendall(struct.pack('>BBHH',5,botón,posiciónHorizontal,posiciónVertical))
            time.sleep(.3)
            imagenElementoPrevio=Image.frombytes('RGB',(640,480),bytes(listaPíxeles()))
            valorPulsarRatón(160,196)
            for _ in range(2):valorPulsado(0xff08);valorPulsado(0xff08,False)
            for valorCarácter in '한글':valorPulsado(0x1000000|ord(valorCarácter));valorPulsado(0x1000000|ord(valorCarácter),False)
            for númeroElementosRepetición in (1,2):
                ponerEnMarcha=len(transcripción);valorPulsarRatón(180,242)
                recibirMensaje(('GUI Saludo: 안녕하세요, 한글님! ('+str(númeroElementosRepetición)+')').encode(),ponerEnMarcha)
            time.sleep(.3)
            dibujoVentana=Image.frombytes('RGB',(640,480),bytes(listaPíxeles()))
            assert imagenElementoPrevio.crop((110,272,530,300)).tobytes()!=dibujoVentana.crop((110,272,530,300)).tobytes()
            dibujoVentana.save(str(datosResultado/'java-swing.png'))
            ponerEnMarcha=len(transcripción);valorPulsarRatón(535,105)
            assert 'exit 0' in recibirMensaje(b'jkoros-native> ',ponerEnMarcha)
        # Download the guest-created bytes through FTP in the same GUI VM.
        nombreEntradaElementoArchivo={'java':'java.txt','c':'c.txt','python':'python.txt'}[Lengua]
        intérpreteComandos('cp '+nombreEntradaElementoArchivo+' /validar.txt')
        númeroElementosRecibido=bytearray();conexiónTransferenciaArchivo.retrbinary('RETR validar.txt',númeroElementosRecibido.extend);assert númeroElementosRecibido==archivoEsperado.encode()
        intérpreteComandos('echo preserved > EjemploSalida.'+('py' if Lengua=='python' else Lengua))
        assert 'EXAMPLES READY' in intérpreteComandos('example '+Lengua)
        assert '\npreserved\n' in intérpreteComandos('cat EjemploSalida.'+('py' if Lengua=='python' else Lengua))
        assert '한/operandoCero valorTecla, Shift+Space 또는 F9' in intérpreteComandos('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in intérpreteComandos('echo GUI NETWORK TOGETHER')
        conexiónTransferenciaArchivo.quit();conexiónTransferenciaArchivo=None;assert 'FTP stopped' in intérpreteComandos('ftpd stop')
        print('PASS '+Lengua+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if conexiónTransferenciaArchivo:
            try:conexiónTransferenciaArchivo.close()
            except OSError:pass
        if cliente:cliente.close()
        proceso.terminate()
        try:proceso.wait(timeout=8)
        except subprocess.TimeoutExpired:proceso.kill();proceso.wait()
        selector.close();proceso.stdout.close();(datosResultado/(Lengua+'-serial.log')).write_bytes(transcripción)


def ponerEnMarcha():
    datosResultado=raízProyecto/'build/verification/examples';datosResultado.mkdir(parents=True,exist_ok=True)
    informeValidación={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with ServidoresRepetirEntrada() as entradaElementoServidorRepetirEntrada:
            for Lengua in ('java','c','python'):
                pruebaLengua(Lengua,entradaElementoServidorRepetirEntrada,datosResultado);informeValidación['languages'].append(Lengua)
            esperado=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert entradaElementoServidorRepetirEntrada.tieneRecibido==[(valorCategoría,Datos.encode()) for valorCategoría,Datos in esperado],entradaElementoServidorRepetirEntrada.tieneRecibido
            informeValidación['host_network_payloads']=[{'protocol':valorCategoría,'text':Datos.decode()} for valorCategoría,Datos in entradaElementoServidorRepetirEntrada.tieneRecibido]
        informeValidación.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(datosResultado/'report.json').write_text(json.dumps(informeValidación,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ponerEnMarcha()
