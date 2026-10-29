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
    def __init__(자신, të_dhëna):
        자신.të_dhëna = të_dhëna
        자신.Pozicioni = 0

    def Leximi(자신, gjatësi_VALUE):
        if gjatësi_VALUE < 0 or 자신.Pozicioni + gjatësi_VALUE > len(자신.të_dhëna):
            raise 컴파일오류('잘린 klasë_VALUE 또는 Komanda të_dhëna')
        llogaritje = 자신.të_dhëna[자신.Pozicioni:자신.Pozicioni + gjatësi_VALUE]
        자신.Pozicioni += gjatësi_VALUE
        return llogaritje

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.Leximi(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(të_dhëna):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    varg_VALUE = të_dhëna.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return varg_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klasë_VALUE:
    def __init__(자신, POZICIONI):
        자신.POZICIONI = POZICIONI
        lexues_VALUE = 자료읽기(POZICIONI.read_bytes())
        if lexues_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java klasë_VALUE 표식이 아님')
        lexues_VALUE.Leximi(4)
        njësi_COUNT = lexues_VALUE.수('H')
        자신.konstante_VALUE = [None] * njësi_COUNT
        INDEX = 1
        while INDEX < njësi_COUNT:
            종류 = lexues_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(lexues_VALUE.Leximi(lexues_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = lexues_VALUE.수('i')
            elif 종류 == 4:
                VALUE = lexues_VALUE.Leximi(4)
            elif 종류 in (5, 6):
                VALUE = lexues_VALUE.Leximi(8)
            elif 종류 in (7, 8, 16):
                VALUE = lexues_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (lexues_VALUE.수('H'), lexues_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (lexues_VALUE.수('B'), lexues_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 konstante_VALUE 종류: {}'.format(종류))
            자신.konstante_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.qasem_futje = lexues_VALUE.수('H')
        자신.Emër = 자신.klasë_emër(lexues_VALUE.수('H'))
        부모 = lexues_VALUE.수('H')
        if 자신.klasë_emër(부모) != 'java/lang/Object' or lexues_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Emër + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.fushë_VALUE = 자신.멤버읽기(lexues_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(lexues_VALUE)
        자신.속성읽기(lexues_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstante_VALUE[INDEX][0] != 1:
            raise 컴파일오류('varg_VALUE konstante_VALUE format_VALUE GABIM')
        return 자신.konstante_VALUE[INDEX][1]

    def klasë_emër(자신, INDEX):
        return 자신.문자(자신.konstante_VALUE[INDEX][1])

    def Referencë(자신, INDEX):
        pronari_VALUE, emër_format = 자신.konstante_VALUE[INDEX][1]
        Emër, format_VALUE = 자신.konstante_VALUE[emër_format][1]
        return 자신.klasë_emër(pronari_VALUE), 자신.문자(Emër), 자신.문자(format_VALUE)

    def 속성읽기(자신, lexues_VALUE):
        llogaritje = {}
        for _ in range(lexues_VALUE.수('H')):
            Emër = 자신.문자(lexues_VALUE.수('H'))
            llogaritje[Emër] = lexues_VALUE.Leximi(lexues_VALUE.수('I'))
        return llogaritje

    def 멤버읽기(자신, lexues_VALUE):
        llogaritje = []
        for _ in range(lexues_VALUE.수('H')):
            qasem_futje = lexues_VALUE.수('H')
            Emër = 자신.문자(lexues_VALUE.수('H'))
            format_VALUE = 자신.문자(lexues_VALUE.수('H'))
            llogaritje.append((qasem_futje, Emër, format_VALUE, 자신.속성읽기(lexues_VALUE)))
        return llogaritje


def 형식읽기(varg_VALUE):
    llogaritje = []
    Pozicioni = 0
    while Pozicioni < len(varg_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if varg_VALUE.startswith(format_VALUE, Pozicioni):
                llogaritje.append(format_VALUE)
                Pozicioni += len(format_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 tipi_i_të_dhënave: ' + varg_VALUE)
    return llogaritje


def 함수형식(서술):
    Argumente, Kthe_llogaritje = 서술[1:].split(')')
    Argumente = 형식읽기(Argumente)
    Kthe_TYPE = 형식읽기(Kthe_llogaritje)
    if 'V' in Argumente or len(Kthe_TYPE) != 1:
        raise 컴파일오류('FUNCTION_VALUE 서술 format_VALUE GABIM: ' + 서술)
    return Argumente, Kthe_llogaritje


def simbol(종류, *부분):
    BURIMI = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(BURIMI).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def zbatoj_komandë(Argumente=None):
    analizues_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK burim_degëzim ndërtoj_sistem')
    analizues_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analizues_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/klasë_VALUE 디렉터리')
    analizues_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 ndërtoj_sistem JDK 또는 openjdk-build의 부트 JDK POZICIONI')
    analizues_48ee4b1b.add_argument('--bundle-runtime', help='zbatoj_komandë 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analizues_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK program_hapës/burim_degëzim 빌드의 C 컴파일러')
    analizues_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    analizues_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ndërtoj_sistem 작업 수')
    analizues_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ndërtoj_sistem objektiv (예: aarch64-linux-gnu)')
    analizues_48ee4b1b.add_argument('--sysroot', help='교차 ndërtoj_sistem 대상의 libc/헤더/bibliotekë 루트')
    analizues_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    analizues_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=klasë_VALUE.FUNCTION_VALUE (자체 스택 ABI)')
    analizues_48ee4b1b.add_argument('--entry', help='예: 계산.Ekzekuto (openjdk-build 이외 대상에서 필수)')
    analizues_48ee4b1b.add_argument('-o', '--output', required=True, help='zbatoj_komandë ELF/.o 출력; openjdk-build는 전용 ndërtoj_sistem 디렉터리')
    analizues_48ee4b1b.add_argument('sources', nargs='+')
    parametër_argument = analizues_48ee4b1b.parse_args(Argumente)
    if parametër_argument.target == 'openjdk-build':
        if len(parametër_argument.sources) != 1 or not parametër_argument.java_home or parametër_argument.entry or parametër_argument.export or parametër_argument.classpath or parametër_argument.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK burim_degëzim 디렉터리 하나와 --java-home 부트 JDK, -o ndërtoj_sistem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametër_argument.sources[0], parametër_argument.output, parametër_argument.java_home, parametër_argument.jobs, parametër_argument.openjdk_target,
                  parametër_argument.sysroot, None if parametër_argument.cc == 'cc' else parametër_argument.cc, parametër_argument.cxx, parametër_argument.configure_arg)
        except BuildError as GABIM:
            raise 컴파일오류(str(GABIM))
        return
    if not parametër_argument.entry:
        analizues_48ee4b1b.error('--entry is required for this target')
    if parametër_argument.cxx or parametër_argument.openjdk_target or parametër_argument.sysroot or parametër_argument.configure_arg or parametër_argument.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build objektiv 전용')
    if parametër_argument.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Krijo_futje
        Krijo_futje(parametër_argument)
        return
    if parametër_argument.classpath or parametër_argument.java_home or parametër_argument.bundle_runtime or parametër_argument.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk objektiv 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametër_argument.target, '--entry', parametër_argument.entry, '-o', parametër_argument.output]
    for cakto_VALUE in parametër_argument.export: 자바명령.extend(['--export', cakto_VALUE])
    subprocess.run(자바명령+parametër_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        zbatoj_komandë()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as GABIM:
        print('ndërtoj_burim GABIM: ' + str(GABIM), file=sys.stderr)
        sys.exit(1)
