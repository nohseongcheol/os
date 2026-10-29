#!/usr/bin/env python3
"""datosEfectivo QEMU/VNC에서 Pantalla tamaño·valorFrontera·ventana valorMover·Swing·언어별 그리기를 검사한다."""
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


def PruebaResolución(valorAnchura, valorAltura, rutaResultado):
    with socket.socket() as valorTemporal:
        valorTemporal.bind(('127.0.0.1', 0)); númeroPuerto = valorTemporal.getsockname()[1]
    textoTamaño = '{}x{}'.format(valorAnchura, valorAltura)
    valorProceso = subprocess.Popen(['python3', str(raízProyecto/'Herramientas/ejecutarComando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(númeroPuerto), '--resolution', textoTamaño], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selector = selectors.DefaultSelector(); Selector.register(valorProceso.stdout, selectors.EVENT_READ)
    registroEntradaDiario = bytearray(); valorRemoto = None; valorTransferencia = None

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

    def intérpreteComandos(texto): return esperarFin(b'\r\n__RESOLUTION_DONE__\r\n', enviarTexto(texto+'; echo __RESOLUTION_DONE__\n'))

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
        valorRemoto.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        comprobarPíxel((valorAnchura-1, valorAltura-1), (24, 32, 48))
        # Pantalla derecho 아래까지 이동한다. elementoListaElementoPrevio 640×480 valorFrontera 밖에서 X를 누른다.
        enPosiciónPunto(40, 60, 1); enPosiciónPunto(valorAnchura-568+28, valorAltura-360+12, 1); enPosiciónPunto(valorAnchura-568+28, valorAltura-360+12, 0)
        comprobarPíxel((valorAnchura-568, valorAltura-360), (32, 80, 144))
        ponerEnMarcha = len(registroEntradaDiario); valorPulsarRatón(valorAnchura-20, valorAltura-345); esperarFin(b'TERMINAL FOCUS 1', ponerEnMarcha)
        comprobarPíxel((valorAnchura-568, valorAltura-360), (24, 32, 48))
        ponerEnMarcha = len(registroEntradaDiario); valorPulsarRatón(80, 16); esperarFin(b'TERMINAL FOCUS 1', ponerEnMarcha)
        intérpreteComandos('ftpd start')
        valorTransferencia = ftplib.FTP(); valorTransferencia.encoding = 'utf-8'; valorTransferencia.connect('127.0.0.1', númeroPuerto, timeout=20); valorTransferencia.login()
        # C valorFrontera 검사는 32비트 unsigned valorNegativo convertirValor·recortar 밖·빈 사각형을 포함한다.
        fuente = '''#include <ABIPantalla.h>
#include <ABIArchivo.h>
int main(void) {
    unsigned valorAnchura=anchuraPantalla(), valorAltura=alturaPantalla();
    if(valorAnchura!=WIDTH || valorAltura!=HEIGHT) return 1;
    if(dibujarRectángulo(valorAnchura,valorAltura,0,0,0)) return 2;
    if(dibujarRectángulo(valorAnchura,valorAltura-1,1,1,0)!=-22) return 3;
    if(dibujarRectángulo(valorAnchura-1,valorAltura,1,1,0)!=-22) return 4;
    if(dibujarRectángulo(-1,0,1,1,0)!=-22) return 5;
    if(dibujarRectángulo(0,0,-1,1,0)!=-22) return 6;
    if(dibujarRectángulo(valorAnchura-1,valorAltura-1,1,1,0x332211)) return 7;
    escribirDatosArchivo(1,"C RESOLUTION PASS\\n",18);
    esperarDibujoPara(); return 0;
}
'''.replace('WIDTH', str(valorAnchura)).replace('HEIGHT', str(valorAltura))
        archivosSubir('pruebaPantalla.c', fuente.encode())
        assert 'exit 0' in intérpreteComandos('cc /pruebaPantalla.c -o /pruebaPantalla')
        esperarFin(b'C RESOLUTION PASS', enviarTexto('run /pruebaPantalla\n'))
        comprobarPíxel((valorAnchura-1, valorAltura-1), (17, 34, 51))
        esperarFin(b'jkoros-native> ', enviarTexto('q'))
        fuente = '''from español import tamañoPantalla, dibujarRectángulo, esperarDibujoPara, Salida, ErrorSistema
valorAnchura, valorAltura = tamañoPantalla()
assert (valorAnchura, valorAltura) == (WIDTH, HEIGHT)
try:
    dibujarRectángulo(valorAnchura, valorAltura-1, 1, 1, 0)
    raise AssertionError("boundary")
except ErrorSistema as error:
    assert error.número == 22
dibujarRectángulo(valorAnchura-1, valorAltura-1, 1, 1, 0x665544)
Salida("PYTHON RESOLUTION PASS")
esperarDibujoPara()
'''.replace('WIDTH', str(valorAnchura)).replace('HEIGHT', str(valorAltura))
        archivosSubir('pruebaPantalla.py', fuente.encode())
        esperarFin(b'PYTHON RESOLUTION PASS', enviarTexto('python /pruebaPantalla.py\n'))
        comprobarPíxel((valorAnchura-1, valorAltura-1), (68, 85, 102))
        esperarFin(b'jkoros-native> ', enviarTexto('q'))
        fuente = '''import español.propio.*;
public class PruebaResolución {
    public static void main(String[] argumentos) {
        int valorAnchura=Pantalla.valorAnchura(), valorAltura=Pantalla.valorAltura();
        if (valorAnchura!=WIDTH || valorAltura!=HEIGHT) throw new ExcepciónEstadoValor("tamaño");
        try { Pantalla.rectángulo(valorAnchura,valorAltura-1,1,1,0); throw new ExcepciónEstadoValor("recortar"); }
        catch (ExcepciónArgumentoInválido error) { }
        Pantalla.borrarEntradaElemento(0x302018);
        Pantalla.rectángulo(valorAnchura-1,valorAltura-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        Pantalla.esperarFin();
    }
}
'''.replace('WIDTH', str(valorAnchura)).replace('HEIGHT', str(valorAltura))
        # excepción 처리는 Anfitrión javac 결과를 propio JVM에 올려 검사한다.
        fuenteFrontera = rutaResultado/'해상도경계시험.java'
        fuenteFrontera.write_text(fuente.replace('class PruebaResolución', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(raízProyecto/'dist/jkoros-native-korean.jar'), '-d', str(rutaResultado), str(fuenteFrontera)])
        archivosSubir('해상도경계시험.class', (rutaResultado/'해상도경계시험.class').read_bytes())
        esperarFin(b'JAVA RESOLUTION PASS', enviarTexto('java 해상도경계시험\n'))
        comprobarPíxel((valorAnchura-1, valorAltura-1), (119, 136, 153))
        esperarFin(b'jkoros-native> ', enviarTexto('q'))
        # 게스트 javac의 valorSoporte 문법으로 tamaño valorConsultar·borrarEntradaElemento·다섯 argumentos 그리기를 컴파일한다.
        fuente = '''public class PruebaResolución {
    public static void main(String[] argumentos) {
        int valorAnchura=español.propio.Pantalla.valorAnchura();
        int valorAltura=español.propio.Pantalla.valorAltura();
        if (valorAnchura!=WIDTH || valorAltura!=HEIGHT) return;
        español.propio.Pantalla.borrarEntradaElemento(3153944);
        español.propio.Pantalla.rectángulo(valorAnchura-1,valorAltura-1,1,1,10061943);
        español.propio.Salida.escribirLínea("JAVA RESOLUTION PASS");
        español.propio.Pantalla.esperarFin();
    }
}
'''.replace('WIDTH', str(valorAnchura)).replace('HEIGHT', str(valorAltura))
        archivosSubir('PruebaResolución.java', fuente.encode())
        resultado = intérpreteComandos('javac PruebaResolución.java'); assert 'exit 0' in resultado, resultado
        esperarFin(b'JAVA RESOLUTION PASS', enviarTexto('java PruebaResolución\n'))
        comprobarPíxel((valorAnchura-1, valorAltura-1), (119, 136, 153))
        esperarFin(b'jkoros-native> ', enviarTexto('q'))
        archivosSubir('PruebaSwing.class', (rutaResultado/'PruebaSwing.class').read_bytes())
        esperarFin(b'SWING READY', enviarTexto('java PruebaSwing\n'))
        posiciónHorizontal, posiciónVertical = (valorAnchura-400)//2, (valorAltura-280)//2
        Dibujo = comprobarPíxel((posiciónHorizontal, posiciónVertical), (32, 80, 144))
        Dibujo.save(str(rutaResultado/(textoTamaño+'.png')))
        ponerEnMarcha = len(registroEntradaDiario); valorPulsarRatón(posiciónHorizontal+80, posiciónVertical+155)
        esperarFin('SWING CLICK nombre'.encode(), ponerEnMarcha)
        ponerEnMarcha = len(registroEntradaDiario); valorPulsarRatón(posiciónHorizontal+385, posiciónVertical+15); esperarFin(b'jkoros-native> ', ponerEnMarcha)
        assert 'AFTER_RESOLUTION' in intérpreteComandos('echo AFTER_RESOLUTION')
        print('PASS:', textoTamaño, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if valorTransferencia: valorTransferencia.close()
        if valorRemoto: valorRemoto.close()
        if valorProceso.poll() is None:
            valorProceso.terminate()
            try: valorProceso.wait(timeout=8)
            except subprocess.TimeoutExpired: valorProceso.kill(); valorProceso.wait()
        Selector.close(); valorProceso.stdout.close()
        (rutaResultado/(textoTamaño+'.log')).write_bytes(registroEntradaDiario)


def ponerEnMarcha():
    rutaResultado = raízProyecto/'build/verification/resolution'; rutaResultado.mkdir(parents=True, exist_ok=True)
    registroEntradaDiario = {'passed': False, 'kernel_sha256': hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for valorInválido in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            resultado = subprocess.run(['python3', str(raízProyecto/'Herramientas/ejecutarComando.py'), '--resolution', valorInválido], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert resultado.returncode == 2 and b'--resolution' in resultado.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(rutaResultado), str(raízProyecto/'Pruebas/Java/PruebaSwing.java')])
        for valorAnchura, valorAltura in ((1920,1080), (1280,720), (640,480)):
            PruebaResolución(valorAnchura, valorAltura, rutaResultado); registroEntradaDiario['resolutions'].append([valorAnchura, valorAltura])
        registroEntradaDiario.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (rutaResultado/'report.json').write_text(json.dumps(registroEntradaDiario, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ponerEnMarcha()
