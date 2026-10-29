#!/usr/bin/env python3
"""datosEfectivo QEMU/VNC에서 terminal valorEsquina valorArrastrar·puntero·동적 valorCarácter entradaElementoRanura·valorEditar valorContenidoValor 보존를 검사한다."""
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
from PIL import Image
from vistaEscritorio import valorExacto
from ejecutarComando import raízProyecto


def pruebaRedimensionamientoVentana(valorAnchura, valorAltura, rutaResultado):
    with socket.socket() as valorTemporal:
        valorTemporal.bind(('127.0.0.1', 0)); númeroPuerto = valorTemporal.getsockname()[1]
    textoTamaño = '{}x{}'.format(valorAnchura, valorAltura)
    valorProceso = subprocess.Popen(['python3', str(raízProyecto/'Herramientas/ejecutarComando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(númeroPuerto), '--resolution', textoTamaño], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selector = selectors.DefaultSelector(); Selector.register(valorProceso.stdout, selectors.EVENT_READ)
    registroEntradaDiario = bytearray(); valorRemoto = None; valorTransferencia = None; ocultoPuntero=[False]

    def esperarFin(mostrarValor, ponerEnMarcha=0):
        valorPlazo = time.monotonic() + 60
        while mostrarValor not in registroEntradaDiario[ponerEnMarcha:]:
            if time.monotonic() > valorPlazo or valorProceso.poll() is not None or b'HALTED' in registroEntradaDiario or b'PANIC:' in registroEntradaDiario:
                raise AssertionError(registroEntradaDiario[ponerEnMarcha:].decode('utf-8', 'replace'))
            for evento, _ in Selector.select(.1):
                Datos = evento.fileobj.read(65536)
                if Datos: registroEntradaDiario.extend(Datos)
        return registroEntradaDiario[ponerEnMarcha:].decode('utf-8', 'replace')

    def botónPulsarRatón(símbolo, esPulsado=True): valorRemoto.sendall(struct.pack('>BBHI', 4, int(esPulsado), 0, símbolo))

    def enviarTexto(texto):
        ponerEnMarcha = len(registroEntradaDiario)
        for valorCarácter in texto:
            símbolo = 0xff0d if valorCarácter == '\n' else ord(valorCarácter) if ord(valorCarácter) < 256 else 0x1000000 | ord(valorCarácter)
            botónPulsarRatón(símbolo); botónPulsarRatón(símbolo, False)
        return ponerEnMarcha

    def intérpreteComandos(texto): return esperarFin(b'\r\n__RESIZE_DONE__\r\n', enviarTexto(texto+'; echo __RESIZE_DONE__\n'))

    def enPosiciónPunto(posiciónHorizontal, posiciónVertical, esPulsado): valorRemoto.sendall(struct.pack('>BBHH', 5, esPulsado, posiciónHorizontal, posiciónVertical))

    def valorPulsarRatón(posiciónHorizontal, posiciónVertical): enPosiciónPunto(posiciónHorizontal, posiciónVertical, 1); enPosiciónPunto(posiciónHorizontal, posiciónVertical, 0)

    def imagenMapaBits():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 datosEfectivo 너비를 쓴다.
        valorRemoto.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, valorAnchura, valorAltura))
        Dibujo = Image.new('RGB', (valorAnchura, valorAltura)); valorÁrea = 0
        while True:
            valorClaseTipo = valorExacto(valorRemoto, 1)[0]
            if valorClaseTipo == 2: continue
            if valorClaseTipo == 3:
                longitud = struct.unpack('>I', valorExacto(valorRemoto, 7)[3:])[0]; valorExacto(valorRemoto, longitud); continue
            assert valorClaseTipo == 0, valorClaseTipo
            númeroElementosElementoLista = struct.unpack('>H', valorExacto(valorRemoto, 3)[1:])[0]
            for _ in range(númeroElementosElementoLista):
                posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, longitud, valorCodificaciónEstado = struct.unpack('>HHHHi', valorExacto(valorRemoto, 12))
                if valorCodificaciónEstado == -239:
                    assert extensiónRangoAnchura==0 and longitud==0, 'remote cursor must be hidden'
                    ocultoPuntero[0]=True
                    continue
                assert valorCodificaciónEstado == 0 and posiciónHorizontal+extensiónRangoAnchura <= valorAnchura and posiciónVertical+longitud <= valorAltura
                Dibujo.paste(Image.frombytes('RGB', (extensiónRangoAnchura, longitud), valorExacto(valorRemoto, extensiónRangoAnchura*longitud*4), 'raw', 'BGRX'), (posiciónHorizontal, posiciónVertical))
                valorÁrea += extensiónRangoAnchura*longitud
            if valorÁrea:
                assert valorÁrea == valorAnchura*valorAltura, valorÁrea
                return Dibujo

    def comprobarPíxel(valorCoordenada, valorColor):
        valorPlazo = time.monotonic()+10
        while True:
            Dibujo = imagenMapaBits()
            if Dibujo.getpixel(valorCoordenada) == valorColor: return Dibujo
            if time.monotonic() > valorPlazo: raise AssertionError((valorCoordenada, Dibujo.getpixel(valorCoordenada), valorColor))

    def archivosSubir(nombre, Datos): valorTransferencia.storbinary('STOR '+nombre, io.BytesIO(Datos))

    try:
        esperarFin(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+textoTamaño+' RGB32').encode() in registroEntradaDiario
        print('BOOT:', textoTamaño, flush=True)
        númeroRemoto = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', registroEntradaDiario).group(1))
        valorRemoto = socket.create_connection(('127.0.0.1', númeroRemoto), timeout=20)
        assert valorExacto(valorRemoto, 12) == b'RFB 003.008\n'; valorRemoto.sendall(b'RFB 003.008\n')
        assert 1 in valorExacto(valorRemoto, valorExacto(valorRemoto, 1)[0]); valorRemoto.sendall(b'\x01')
        assert valorExacto(valorRemoto, 4) == b'\0'*4; valorRemoto.sendall(b'\x01')
        estadoValorInicialValor = valorExacto(valorRemoto, 24); assert struct.unpack('>HH', estadoValorInicialValor[:4]) == (valorAnchura, valorAltura)
        valorExacto(valorRemoto, struct.unpack('>I', estadoValorInicialValor[20:])[0])
        valorRemoto.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        valorRemoto.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        comprobarPíxel((valorAnchura-1, valorAltura-1), (24, 32, 48))
        def brevementePausar(valorSegundos=.25):
            terminación=time.monotonic()+valorSegundos
            while time.monotonic()<terminación:
                for evento,_ in Selector.select(.02):
                    Datos=evento.fileobj.read(65536)
                    if Datos:registroEntradaDiario.extend(Datos)
        ventana=[12,48,568,360]
        def verificarTamaño():
            valorColumna,valorFila=(ventana[2]-24)//8,(ventana[3]-56)//16
            texto=intérpreteComandos('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(valorColumna,valorFila) in texto,texto
            # datosEfectivo ventana 테두리: 단지 tamaño valorConsultar 값만 바뀐 것이 아닌지 확인한다.
            enPosiciónPunto(valorAnchura-1,10,0);brevementePausar()
            comprobarPíxel((ventana[0],ventana[1]),(32,80,144))
            Dibujo=comprobarPíxel((ventana[0]+ventana[2]-1,ventana[1]+ventana[3]-1),(39,49,64))
            return Dibujo
        def valorEsquina(direcciónSentido):
            return (ventana[0]+(3 if direcciónSentido in (1,3) else ventana[2]-4),ventana[1]+(3 if direcciónSentido<=2 else ventana[3]-4))
        def arrastrarRedimensionar(direcciónSentido,valorDiferencia,botón=1):
            operandoPrimero,valorTres=valorEsquina(direcciónSentido);enPosiciónPunto(operandoPrimero,valorTres,0);brevementePausar()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            píxelBlancoColor=(operandoPrimero-7 if direcciónSentido in (1,4) else operandoPrimero+7,valorTres-7)
            comprobarPíxel(píxelBlancoColor,(255,255,255))
            enPosiciónPunto(operandoPrimero,valorTres,botón)
            horizontalFin=max(0,min(valorAnchura-1,operandoPrimero+valorDiferencia[0]));verticalFin=max(0,min(valorAltura-1,valorTres+valorDiferencia[1]))
            enPosiciónPunto(horizontalFin,verticalFin,botón);enPosiciónPunto(horizontalFin,verticalFin,0);brevementePausar()
            if botón==1:
                valorIzquierdo,valorExtremoSuperior,extensiónRangoAnchura,longitud=ventana;valorDerecho,valorExtremoInferior=valorIzquierdo+extensiónRangoAnchura,valorExtremoSuperior+longitud
                if direcciónSentido in (1,3):valorIzquierdo=max(0,min(valorDerecho-360,valorIzquierdo+horizontalFin-operandoPrimero))
                else:valorDerecho=max(valorIzquierdo+360,min(valorAnchura,valorDerecho+horizontalFin-operandoPrimero))
                if direcciónSentido<=2:valorExtremoSuperior=max(34,min(valorExtremoInferior-216,valorExtremoSuperior+verticalFin-valorTres))
                else:valorExtremoInferior=max(valorExtremoSuperior+216,min(valorAltura,valorExtremoInferior+verticalFin-valorTres))
                ventana[:]=[valorIzquierdo,valorExtremoSuperior,valorDerecho-valorIzquierdo,valorExtremoInferior-valorExtremoSuperior]
        verificarTamaño();assert ocultoPuntero[0]
        arrastrarRedimensionar(4,(-100,-60),4);verificarTamaño() # derecho 버튼은 크기를 바꾸지 않는다.
        for direcciónSentido,valorDiferencia in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            arrastrarRedimensionar(direcciónSentido,valorDiferencia);verificarTamaño()
        # valorEntrada 중인 긴 textoHangul 명령은 nuevaLínea/posiciónHorizontal 스크롤과 무관하게 그대로 실행된다.
        textoLargo='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        enviarTexto("echo '"+textoLargo+"'");brevementePausar()
        arrastrarRedimensionar(4,(-1000,-1000));assert ventana[2:]==[360,216]
        arrastrarRedimensionar(4,(valorAnchura,valorAltura))
        ponerEnMarcha=enviarTexto('\n');esperarFin(('\r\n'+textoLargo+'\r\n').encode(),ponerEnMarcha);verificarTamaño()
        # vi가 valorEditar 중에 Pantalla 크기를 valorReintentar 읽고, 저장하지 않은 한글도 유지한다.
        intérpreteComandos('ftpd start')
        valorTransferencia=ftplib.FTP();valorTransferencia.encoding='utf-8';valorTransferencia.connect('127.0.0.1',númeroPuerto,timeout=20);valorTransferencia.login()
        esperarFin(b'NORMAL',enviarTexto('vi /크기자료.txt\n'))
        esperarFin(b'INSERT',enviarTexto('i미저장 한글 Datos\n'));brevementePausar()
        arrastrarRedimensionar(4,(-valorAnchura,-valorAltura))
        # ANSI valorFila 이동에 새 valorFila 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ventana[3]-56)//16)).encode() in registroEntradaDiario[-4096:]
        enviarTexto('작은 창에서도 valorContinuación escribir\n');brevementePausar()
        arrastrarRedimensionar(4,(valorAnchura,valorAltura))
        enviarTexto('큰 창에서도 valorContinuación escribir\n');brevementePausar()
        botónPulsarRatón(0xff1b);botónPulsarRatón(0xff1b,False);brevementePausar()
        esperarFin(b'jkoros-native> ',enviarTexto(':wq\n'))
        valorContenidoValor=bytearray();valorTransferencia.retrbinary('RETR 크기자료.txt',valorContenidoValor.extend)
        assert valorContenidoValor=='미저장 한글 Datos\n작은 창에서도 valorContinuación escribir\n큰 창에서도 valorContinuación escribir\n'.encode(),valorContenidoValor
        verificarTamaño().save(str(rutaResultado/(textoTamaño+'-large.png')))
        # 두 번째 창은 valorPredeterminado tamaño, valorReintentar elementoListaPrimero 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ponerEnMarcha=len(registroEntradaDiario);valorPulsarRatón(70,16);esperarFin(b'TERMINAL FOCUS 2',ponerEnMarcha)
        assert 'TERMINAL SIZE 68x19' in intérpreteComandos('terminal size')
        ponerEnMarcha=len(registroEntradaDiario);valorPulsarRatón(180,16);esperarFin(b'TERMINAL FOCUS 1',ponerEnMarcha);verificarTamaño()
        arrastrarRedimensionar(4,(-valorAnchura,-valorAltura));verificarTamaño().save(str(rutaResultado/(textoTamaño+'-small.png')))
        # tamaño cambiarValor valorLadoPosterior X 닫기도 새로운 derecho 가장자리를 사용한다.
        ponerEnMarcha=len(registroEntradaDiario);valorPulsarRatón(ventana[0]+ventana[2]-20,ventana[1]+15);esperarFin(b'TERMINAL FOCUS 2',ponerEnMarcha)
        assert 'RESIZE CLOSED' in intérpreteComandos('echo RESIZE CLOSED')
        print('PASS:',textoTamaño,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if valorTransferencia:valorTransferencia.close()
        if valorRemoto:valorRemoto.close()
        if valorProceso.poll() is None:
            valorProceso.terminate()
            try:valorProceso.wait(timeout=8)
            except subprocess.TimeoutExpired:valorProceso.kill();valorProceso.wait()
        Selector.close();valorProceso.stdout.close();(rutaResultado/(textoTamaño+'.log')).write_bytes(registroEntradaDiario)


def ponerEnMarcha():
    rutaResultado=raízProyecto/'build/verification/resize';rutaResultado.mkdir(parents=True,exist_ok=True)
    registroEntradaDiario={'passed':False,'kernel_sha256':hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for valorAnchura,valorAltura in ((640,480),(1920,1080)):
            pruebaRedimensionamientoVentana(valorAnchura,valorAltura,rutaResultado);registroEntradaDiario['resolutions'].append([valorAnchura,valorAltura])
        registroEntradaDiario.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(rutaResultado/'report.json').write_text(json.dumps(registroEntradaDiario,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ponerEnMarcha()
