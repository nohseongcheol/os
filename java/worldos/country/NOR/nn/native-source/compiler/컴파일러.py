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
    def __init__(자신, data):
        자신.data = data
        자신.Posisjon = 0

    def Les(자신, lengd_VALUE):
        if lengd_VALUE < 0 or 자신.Posisjon + lengd_VALUE > len(자신.data):
            raise 컴파일오류('잘린 time_VALUE 또는 Kommando data')
        forretningsmål = 자신.data[자신.Posisjon:자신.Posisjon + lengd_VALUE]
        자신.Posisjon += lengd_VALUE
        return forretningsmål

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.Les(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    streng_VALUE = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return streng_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class time_VALUE:
    def __init__(자신, STIGE):
        자신.STIGE = STIGE
        Lesar_VALUE = 자료읽기(STIGE.read_bytes())
        if Lesar_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java time_VALUE 표식이 아님')
        Lesar_VALUE.Les(4)
        vare_COUNT = Lesar_VALUE.수('H')
        자신.konstant_VALUE = [None] * vare_COUNT
        INDEX = 1
        while INDEX < vare_COUNT:
            종류 = Lesar_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Lesar_VALUE.Les(Lesar_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Lesar_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Lesar_VALUE.Les(4)
            elif 종류 in (5, 6):
                VALUE = Lesar_VALUE.Les(8)
            elif 종류 in (7, 8, 16):
                VALUE = Lesar_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Lesar_VALUE.수('H'), Lesar_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Lesar_VALUE.수('B'), Lesar_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 konstant_VALUE 종류: {}'.format(종류))
            자신.konstant_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.tilgang_oppføring = Lesar_VALUE.수('H')
        자신.Namn = 자신.time_namn(Lesar_VALUE.수('H'))
        forelder_VALUE = Lesar_VALUE.수('H')
        if 자신.time_namn(forelder_VALUE) != 'java/lang/Object' or Lesar_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Namn + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.felt_VALUE_0f39cf1c = 자신.멤버읽기(Lesar_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Lesar_VALUE)
        자신.속성읽기(Lesar_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstant_VALUE[INDEX][0] != 1:
            raise 컴파일오류('streng_VALUE konstant_VALUE format_VALUE FEIL')
        return 자신.konstant_VALUE[INDEX][1]

    def time_namn(자신, INDEX):
        return 자신.문자(자신.konstant_VALUE[INDEX][1])

    def Oppslagsverk(자신, INDEX):
        eigar_VALUE, namn_format = 자신.konstant_VALUE[INDEX][1]
        Namn, format_VALUE = 자신.konstant_VALUE[namn_format][1]
        return 자신.time_namn(eigar_VALUE), 자신.문자(Namn), 자신.문자(format_VALUE)

    def 속성읽기(자신, Lesar_VALUE):
        forretningsmål = {}
        for _ in range(Lesar_VALUE.수('H')):
            Namn = 자신.문자(Lesar_VALUE.수('H'))
            forretningsmål[Namn] = Lesar_VALUE.Les(Lesar_VALUE.수('I'))
        return forretningsmål

    def 멤버읽기(자신, Lesar_VALUE):
        forretningsmål = []
        for _ in range(Lesar_VALUE.수('H')):
            tilgang_oppføring = Lesar_VALUE.수('H')
            Namn = 자신.문자(Lesar_VALUE.수('H'))
            format_VALUE = 자신.문자(Lesar_VALUE.수('H'))
            forretningsmål.append((tilgang_oppføring, Namn, format_VALUE, 자신.속성읽기(Lesar_VALUE)))
        return forretningsmål


def 형식읽기(streng_VALUE):
    forretningsmål = []
    Posisjon = 0
    while Posisjon < len(streng_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if streng_VALUE.startswith(format_VALUE, Posisjon):
                forretningsmål.append(format_VALUE)
                Posisjon += len(format_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 datatype: ' + streng_VALUE)
    return forretningsmål


def 함수형식(서술):
    Argument, levere_tilbake_forretningsmål = 서술[1:].split(')')
    Argument = 형식읽기(Argument)
    levere_tilbake_TYPE = 형식읽기(levere_tilbake_forretningsmål)
    if 'V' in Argument or len(levere_tilbake_TYPE) != 1:
        raise 컴파일오류('FUNCTION_VALUE 서술 format_VALUE FEIL: ' + 서술)
    return Argument, levere_tilbake_forretningsmål


def symbol(종류, *부분):
    KJELDE = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(KJELDE).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def Utfør_kommando(Argument=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK kjelde_tre bygg_system')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/time_VALUE 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 bygg_system JDK 또는 openjdk-build의 부트 JDK STIGE')
    해석기.add_argument('--bundle-runtime', help='Utfør_kommando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK app_appskuff/kjelde_tre 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 bygg_system 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 bygg_system mål (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 bygg_system 대상의 libc/헤더/bibliotek 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=time_VALUE.FUNCTION_VALUE (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Køyr_2 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='Utfør_kommando ELF/.o Utdata; openjdk-build는 전용 bygg_system 디렉터리')
    해석기.add_argument('sources', nargs='+')
    parameter_argument = 해석기.parse_args(Argument)
    if parameter_argument.target == 'openjdk-build':
        if len(parameter_argument.sources) != 1 or not parameter_argument.java_home or parameter_argument.entry or parameter_argument.export or parameter_argument.classpath or parameter_argument.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK kjelde_tre 디렉터리 하나와 --java-home 부트 JDK, -o bygg_system 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argument.sources[0], parameter_argument.output, parameter_argument.java_home, parameter_argument.jobs, parameter_argument.openjdk_target,
                  parameter_argument.sysroot, None if parameter_argument.cc == 'cc' else parameter_argument.cc, parameter_argument.cxx, parameter_argument.configure_arg)
        except BuildError as FEIL:
            raise 컴파일오류(str(FEIL))
        return
    if not parameter_argument.entry:
        해석기.error('--entry is required for this target')
    if parameter_argument.cxx or parameter_argument.openjdk_target or parameter_argument.sysroot or parameter_argument.configure_arg or parameter_argument.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build mål 전용')
    if parameter_argument.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Opprett_oppføring
        Opprett_oppføring(parameter_argument)
        return
    if parameter_argument.classpath or parameter_argument.java_home or parameter_argument.bundle_runtime or parameter_argument.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk mål 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argument.target, '--entry', parameter_argument.entry, '-o', parameter_argument.output]
    for Tilordne_VALUE in parameter_argument.export: 자바명령.extend(['--export', Tilordne_VALUE])
    subprocess.run(자바명령+parameter_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Utfør_kommando()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as FEIL:
        print('byggje_kjelde FEIL: ' + str(FEIL), file=sys.stderr)
        sys.exit(1)
