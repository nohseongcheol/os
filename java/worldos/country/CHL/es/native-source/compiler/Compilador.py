#!/usr/bin/env python3
"""제한형 Java의 검증된 javac 바이트코드를 x86 ELF32 네이티브 코드로 변환한다."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import struct
import subprocess
import sys
import tempfile


class ErrorCompilación(Exception):
    pass


class leerDatos:
    def __init__(valorPropio, Datos):
        valorPropio.Datos = Datos
        valorPropio.posición = 0

    def leer(valorPropio, longitud):
        if longitud < 0 or valorPropio.posición + longitud > len(valorPropio.Datos):
            raise ErrorCompilación('valorRecortado valorClase 또는 comando Datos')
        resultado = valorPropio.Datos[valorPropio.posición:valorPropio.posición + longitud]
        valorPropio.posición += longitud
        return resultado

    def númeroValor(valorPropio, valorFormato):
        return struct.unpack('>' + valorFormato, valorPropio.leer(struct.calcsize('>' + valorFormato)))[0]


def decodificar8UTFModificado(Datos):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    Cadena = Datos.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return Cadena.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class valorClase:
    def __init__(valorPropio, ruta):
        valorPropio.ruta = ruta
        valorLector = leerDatos(ruta.read_bytes())
        if valorLector.númeroValor('I') != 0xcafebabe:
            raise ErrorCompilación('Java valorClase 표식이 아님')
        valorLector.leer(4)
        númeroElementosElementoLista = valorLector.númeroValor('H')
        valorPropio.valorConstante = [None] * númeroElementosElementoLista
        número = 1
        while número < númeroElementosElementoLista:
            valorClaseTipo = valorLector.númeroValor('B')
            if valorClaseTipo == 1:
                valor = decodificar8UTFModificado(valorLector.leer(valorLector.númeroValor('H')))
            elif valorClaseTipo == 3:
                valor = valorLector.númeroValor('i')
            elif valorClaseTipo == 4:
                valor = valorLector.leer(4)
            elif valorClaseTipo in (5, 6):
                valor = valorLector.leer(8)
            elif valorClaseTipo in (7, 8, 16):
                valor = valorLector.númeroValor('H')
            elif valorClaseTipo in (9, 10, 11, 12, 18):
                valor = (valorLector.númeroValor('H'), valorLector.númeroValor('H'))
            elif valorClaseTipo == 15:
                valor = (valorLector.númeroValor('B'), valorLector.númeroValor('H'))
            else:
                raise ErrorCompilación('지원하지 않는 valorConstante valorClaseTipo: {}'.format(valorClaseTipo))
            valorPropio.valorConstante[número] = (valorClaseTipo, valor)
            número += 2 if valorClaseTipo in (5, 6) else 1
        valorPropio.entradaElementoAcceso = valorLector.númeroValor('H')
        valorPropio.nombre = valorPropio.nombreClase(valorLector.númeroValor('H'))
        valorPadre = valorLector.númeroValor('H')
        if valorPropio.nombreClase(valorPadre) != 'java/lang/Object' or valorLector.númeroValor('H') != 0:
            raise ErrorCompilación(valorPropio.nombre + ': 상속 및 인터페이스는 아직 지원하지 않음')
        valorPropio.valorCampo = valorPropio.leerMiembros(valorLector)
        valorPropio.Función = valorPropio.leerMiembros(valorLector)
        valorPropio.leerAtributos(valorLector)

    def Caracteres(valorPropio, número):
        if valorPropio.valorConstante[número][0] != 1:
            raise ErrorCompilación('Cadena valorConstante valorFormato error')
        return valorPropio.valorConstante[número][1]

    def nombreClase(valorPropio, número):
        return valorPropio.Caracteres(valorPropio.valorConstante[número][1])

    def referencia(valorPropio, número):
        valorPropietario, formatoNombre = valorPropio.valorConstante[número][1]
        nombre, valorFormato = valorPropio.valorConstante[formatoNombre][1]
        return valorPropio.nombreClase(valorPropietario), valorPropio.Caracteres(nombre), valorPropio.Caracteres(valorFormato)

    def leerAtributos(valorPropio, valorLector):
        resultado = {}
        for _ in range(valorLector.númeroValor('H')):
            nombre = valorPropio.Caracteres(valorLector.númeroValor('H'))
            resultado[nombre] = valorLector.leer(valorLector.númeroValor('I'))
        return resultado

    def leerMiembros(valorPropio, valorLector):
        resultado = []
        for _ in range(valorLector.númeroValor('H')):
            entradaElementoAcceso = valorLector.númeroValor('H')
            nombre = valorPropio.Caracteres(valorLector.númeroValor('H'))
            valorFormato = valorPropio.Caracteres(valorLector.númeroValor('H'))
            resultado.append((entradaElementoAcceso, nombre, valorFormato, valorPropio.leerAtributos(valorLector)))
        return resultado


def analizarTipos(Cadena):
    resultado = []
    posición = 0
    while posición < len(Cadena):
        for valorFormato in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if Cadena.startswith(valorFormato, posición):
                resultado.append(valorFormato)
                posición += len(valorFormato)
                break
        else:
            raise ErrorCompilación('지원하지 않는 tipoDatos: ' + Cadena)
    return resultado


def DescriptorMétodo(valorDescripción):
    argumentos, resultadoRetornar = valorDescripción[1:].split(')')
    argumentos = analizarTipos(argumentos)
    tipoRetornar = analizarTipos(resultadoRetornar)
    if 'V' in argumentos or len(tipoRetornar) != 1:
        raise ErrorCompilación('Función valorDescripción valorFormato error: ' + valorDescripción)
    return argumentos, resultadoRetornar


def símbolo(valorClaseTipo, *valorSubparte):
    fuente = '\x00'.join(valorSubparte).encode('utf-8')
    return 'j_{}_{}'.format(valorClaseTipo, hashlib.sha256(fuente).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 Función 서술에 대해서만 허용한다.
def ejecutarComando(argumentos=None):
    Analizador = argparse.ArgumentParser(description='propio Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK árbolFuente construirSistema')
    Analizador.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    Analizador.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 añadirFinalEntradaElemento JAR/valorClase 디렉터리')
    Analizador.add_argument('--java-home', help='openjdk 앱의 construirSistema JDK 또는 openjdk-build의 부트 JDK ruta')
    Analizador.add_argument('--bundle-runtime', help='ejecutarComando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    Analizador.add_argument('--cc', default='cc', help='OpenJDK LanzadorPrograma/árbolFuente 빌드의 C Compilador')
    Analizador.add_argument('--cxx', help='openjdk-build의 C++ Compilador')
    Analizador.add_argument('--jobs', type=int, default=2, help='openjdk-build의 construirSistema Tarea númeroValor')
    Analizador.add_argument('--openjdk-target', help='공식 OpenJDK 교차 construirSistema valorObjetivo (예: aarch64-linux-gnu)')
    Analizador.add_argument('--sysroot', help='교차 construirSistema 대상의 libc/헤더/biblioteca 루트')
    Analizador.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 valorFormato')
    Analizador.add_argument('--export', action='append', default=[], help='외부기호=valorClase.Función (propio pilaOperando ABI)')
    Analizador.add_argument('--entry', help='예: resultadoCálculo.ponerEnMarcha (openjdk-build 이외 대상에서 esRequerido)')
    Analizador.add_argument('-o', '--output', required=True, help='ejecutarComando ELF/.o Salida; openjdk-build는 전용 construirSistema 디렉터리')
    Analizador.add_argument('sources', nargs='+')
    argumentoParámetro = Analizador.parse_args(argumentos)
    if argumentoParámetro.target == 'openjdk-build':
        if len(argumentoParámetro.sources) != 1 or not argumentoParámetro.java_home or argumentoParámetro.entry or argumentoParámetro.export or argumentoParámetro.classpath or argumentoParámetro.bundle_runtime:
            raise ErrorCompilación('openjdk-build: OpenJDK árbolFuente 디렉터리 하나와 --java-home 부트 JDK, -o construirSistema 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(argumentoParámetro.sources[0], argumentoParámetro.output, argumentoParámetro.java_home, argumentoParámetro.jobs, argumentoParámetro.openjdk_target,
                  argumentoParámetro.sysroot, None if argumentoParámetro.cc == 'cc' else argumentoParámetro.cc, argumentoParámetro.cxx, argumentoParámetro.configure_arg)
        except BuildError as error:
            raise ErrorCompilación(str(error))
        return
    if not argumentoParámetro.entry:
        Analizador.error('--entry is required for this target')
    if argumentoParámetro.cxx or argumentoParámetro.openjdk_target or argumentoParámetro.sysroot or argumentoParámetro.configure_arg or argumentoParámetro.jobs != 2:
        raise ErrorCompilación('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build valorObjetivo 전용')
    if argumentoParámetro.target == 'openjdk':
        sys.modules.setdefault('Compilador', sys.modules[__name__])
        from archivoCódigoEjecutable import crearEntradaElemento
        crearEntradaElemento(argumentoParámetro)
        return
    if argumentoParámetro.classpath or argumentoParámetro.java_home or argumentoParámetro.bundle_runtime or argumentoParámetro.cc != 'cc':
        raise ErrorCompilación('classpath/java-home/bundle-runtime/cc 옵션은 openjdk valorObjetivo 전용')
    comandoJava = ['sh', str(Path(__file__).resolve().parent/'tiempoDeAnticipado.sh'),
                '--target', argumentoParámetro.target, '--entry', argumentoParámetro.entry, '-o', argumentoParámetro.output]
    for valorAsignar in argumentoParámetro.export: comandoJava.extend(['--export', valorAsignar])
    subprocess.run(comandoJava+argumentoParámetro.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ejecutarComando()
    except (ErrorCompilación, OSError, ValueError, subprocess.CalledProcessError) as error:
        print('compilarFuente error: ' + str(error), file=sys.stderr)
        sys.exit(1)
