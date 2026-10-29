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


class 컴파일오류(Exception):
    pass


class 자료읽기:
    def __init__(자신, datos):
        자신.datos = datos
        자신.Posición = 0

    def Lectura(자신, duración_VALOR):
        if duración_VALOR < 0 or 자신.Posición + duración_VALOR > len(자신.datos):
            raise 컴파일오류('잘린 Clase_VALOR 또는 Orde datos')
        RESULTANTE = 자신.datos[자신.Posición:자신.Posición + duración_VALOR]
        자신.Posición += duración_VALOR
        return RESULTANTE

    def 수(자신, formato_VALOR):
        return struct.unpack('>' + formato_VALOR, 자신.Lectura(struct.calcsize('>' + formato_VALOR)))[0]


def 수정유티에프해독(datos):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    cadea_VALOR = datos.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return cadea_VALOR.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Clase_VALOR:
    def __init__(자신, CAMIÑO):
        자신.CAMIÑO = CAMIÑO
        Lector_VALOR = 자료읽기(CAMIÑO.read_bytes())
        if Lector_VALOR.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Clase_VALOR 표식이 아님')
        Lector_VALOR.Lectura(4)
        elemento_CONTAR = Lector_VALOR.수('H')
        자신.constante_VALOR = [None] * elemento_CONTAR
        ÍNDICE = 1
        while ÍNDICE < elemento_CONTAR:
            종류 = Lector_VALOR.수('B')
            if 종류 == 1:
                VALOR = 수정유티에프해독(Lector_VALOR.Lectura(Lector_VALOR.수('H')))
            elif 종류 == 3:
                VALOR = Lector_VALOR.수('i')
            elif 종류 == 4:
                VALOR = Lector_VALOR.Lectura(4)
            elif 종류 in (5, 6):
                VALOR = Lector_VALOR.Lectura(8)
            elif 종류 in (7, 8, 16):
                VALOR = Lector_VALOR.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALOR = (Lector_VALOR.수('H'), Lector_VALOR.수('H'))
            elif 종류 == 15:
                VALOR = (Lector_VALOR.수('B'), Lector_VALOR.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 constante_VALOR 종류: {}'.format(종류))
            자신.constante_VALOR[ÍNDICE] = (종류, VALOR)
            ÍNDICE += 2 if 종류 in (5, 6) else 1
        자신.acceso_introdución = Lector_VALOR.수('H')
        자신.Nome = 자신.nome_de_clase(Lector_VALOR.수('H'))
        부모 = Lector_VALOR.수('H')
        if 자신.nome_de_clase(부모) != 'java/lang/Object' or Lector_VALOR.수('H') != 0:
            raise 컴파일오류(자신.Nome + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.campo_VALOR = 자신.멤버읽기(Lector_VALOR)
        자신.FUNCIÓN_VALOR = 자신.멤버읽기(Lector_VALOR)
        자신.속성읽기(Lector_VALOR)

    def 문자(자신, ÍNDICE):
        if 자신.constante_VALOR[ÍNDICE][0] != 1:
            raise 컴파일오류('cadea_VALOR constante_VALOR formato_VALOR ERRO')
        return 자신.constante_VALOR[ÍNDICE][1]

    def nome_de_clase(자신, ÍNDICE):
        return 자신.문자(자신.constante_VALOR[ÍNDICE][1])

    def Material_de_referencia(자신, ÍNDICE):
        propietario_VALOR, nome_formato = 자신.constante_VALOR[ÍNDICE][1]
        Nome, formato_VALOR = 자신.constante_VALOR[nome_formato][1]
        return 자신.nome_de_clase(propietario_VALOR), 자신.문자(Nome), 자신.문자(formato_VALOR)

    def 속성읽기(자신, Lector_VALOR):
        RESULTANTE = {}
        for _ in range(Lector_VALOR.수('H')):
            Nome = 자신.문자(Lector_VALOR.수('H'))
            RESULTANTE[Nome] = Lector_VALOR.Lectura(Lector_VALOR.수('I'))
        return RESULTANTE

    def 멤버읽기(자신, Lector_VALOR):
        RESULTANTE = []
        for _ in range(Lector_VALOR.수('H')):
            acceso_introdución = Lector_VALOR.수('H')
            Nome = 자신.문자(Lector_VALOR.수('H'))
            formato_VALOR = 자신.문자(Lector_VALOR.수('H'))
            RESULTANTE.append((acceso_introdución, Nome, formato_VALOR, 자신.속성읽기(Lector_VALOR)))
        return RESULTANTE


def 형식읽기(cadea_VALOR):
    RESULTANTE = []
    Posición = 0
    while Posición < len(cadea_VALOR):
        for formato_VALOR in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if cadea_VALOR.startswith(formato_VALOR, Posición):
                RESULTANTE.append(formato_VALOR)
                Posición += len(formato_VALOR)
                break
        else:
            raise 컴파일오류('지원하지 않는 tipo_de_datos: ' + cadea_VALOR)
    return RESULTANTE


def 함수형식(서술):
    Argumentos, devolver_medida = 서술[1:].split(')')
    Argumentos = 형식읽기(Argumentos)
    devolver_TIPO = 형식읽기(devolver_medida)
    if 'V' in Argumentos or len(devolver_TIPO) != 1:
        raise 컴파일오류('FUNCIÓN_VALOR 서술 formato_VALOR ERRO: ' + 서술)
    return Argumentos, devolver_medida


def símbolo(종류, *부분):
    FONTE = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(FONTE).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCIÓN_VALOR 서술에 대해서만 허용한다.
def executar_comando(Argumentos=None):
    analizador_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK fonte_árbore compilar_sistema')
    analizador_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analizador_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Anexar_introdución JAR/Clase_VALOR 디렉터리')
    analizador_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 compilar_sistema JDK 또는 openjdk-build의 부트 JDK CAMIÑO')
    analizador_48ee4b1b.add_argument('--bundle-runtime', help='executar_comando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analizador_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK apl_iniciador/fonte_árbore 빌드의 C 컴파일러')
    analizador_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    analizador_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 compilar_sistema 작업 수')
    analizador_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 compilar_sistema obxectivo_VALOR (예: aarch64-linux-gnu)')
    analizador_48ee4b1b.add_argument('--sysroot', help='교차 compilar_sistema 대상의 libc/헤더/biblioteca 루트')
    analizador_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formato_VALOR')
    analizador_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Clase_VALOR.FUNCIÓN_VALOR (자체 스택 ABI)')
    analizador_48ee4b1b.add_argument('--entry', help='예: 계산.Executar_2 (openjdk-build 이외 대상에서 필수)')
    analizador_48ee4b1b.add_argument('-o', '--output', required=True, help='executar_comando ELF/.o Saída; openjdk-build는 전용 compilar_sistema 디렉터리')
    analizador_48ee4b1b.add_argument('sources', nargs='+')
    parámetro_argumento = analizador_48ee4b1b.parse_args(Argumentos)
    if parámetro_argumento.target == 'openjdk-build':
        if len(parámetro_argumento.sources) != 1 or not parámetro_argumento.java_home or parámetro_argumento.entry or parámetro_argumento.export or parámetro_argumento.classpath or parámetro_argumento.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK fonte_árbore 디렉터리 하나와 --java-home 부트 JDK, -o compilar_sistema 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parámetro_argumento.sources[0], parámetro_argumento.output, parámetro_argumento.java_home, parámetro_argumento.jobs, parámetro_argumento.openjdk_target,
                  parámetro_argumento.sysroot, None if parámetro_argumento.cc == 'cc' else parámetro_argumento.cc, parámetro_argumento.cxx, parámetro_argumento.configure_arg)
        except BuildError as ERRO:
            raise 컴파일오류(str(ERRO))
        return
    if not parámetro_argumento.entry:
        analizador_48ee4b1b.error('--entry is required for this target')
    if parámetro_argumento.cxx or parámetro_argumento.openjdk_target or parámetro_argumento.sysroot or parámetro_argumento.configure_arg or parámetro_argumento.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build obxectivo_VALOR 전용')
    if parámetro_argumento.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import crear_introdución
        crear_introdución(parámetro_argumento)
        return
    if parámetro_argumento.classpath or parámetro_argumento.java_home or parámetro_argumento.bundle_runtime or parámetro_argumento.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk obxectivo_VALOR 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parámetro_argumento.target, '--entry', parámetro_argumento.entry, '-o', parámetro_argumento.output]
    for Asignar_VALOR in parámetro_argumento.export: 자바명령.extend(['--export', Asignar_VALOR])
    subprocess.run(자바명령+parámetro_argumento.sources, check=True)
    return


if __name__ == '__main__':
    try:
        executar_comando()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ERRO:
        print('compilar_fonte ERRO: ' + str(ERRO), file=sys.stderr)
        sys.exit(1)
