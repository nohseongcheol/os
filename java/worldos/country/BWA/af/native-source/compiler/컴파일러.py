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
        자신.Posisie = 0

    def Lees(자신, lengte_VALUE):
        if lengte_VALUE < 0 or 자신.Posisie + lengte_VALUE > len(자신.data):
            raise 컴파일오류('잘린 Klas_VALUE 또는 Opdrag data')
        maatreël = 자신.data[자신.Posisie:자신.Posisie + lengte_VALUE]
        자신.Posisie += lengte_VALUE
        return maatreël

    def 수(자신, formaat_VALUE):
        return struct.unpack('>' + formaat_VALUE, 자신.Lees(struct.calcsize('>' + formaat_VALUE)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    string_VALUE = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return string_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Klas_VALUE:
    def __init__(자신, Pad):
        자신.Pad = Pad
        Leser_VALUE = 자료읽기(Pad.read_bytes())
        if Leser_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Klas_VALUE 표식이 아님')
        Leser_VALUE.Lees(4)
        item_COUNT = Leser_VALUE.수('H')
        자신.konstante_VALUE = [None] * item_COUNT
        INDEX = 1
        while INDEX < item_COUNT:
            종류 = Leser_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Leser_VALUE.Lees(Leser_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Leser_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Leser_VALUE.Lees(4)
            elif 종류 in (5, 6):
                VALUE = Leser_VALUE.Lees(8)
            elif 종류 in (7, 8, 16):
                VALUE = Leser_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Leser_VALUE.수('H'), Leser_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Leser_VALUE.수('B'), Leser_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 konstante_VALUE 종류: {}'.format(종류))
            자신.konstante_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.toegang_inskrywing = Leser_VALUE.수('H')
        자신.Naam = 자신.Klas_naam(Leser_VALUE.수('H'))
        부모 = Leser_VALUE.수('H')
        if 자신.Klas_naam(부모) != 'java/lang/Object' or Leser_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Naam + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.veld_VALUE = 자신.멤버읽기(Leser_VALUE)
        자신.funksie_VALUE = 자신.멤버읽기(Leser_VALUE)
        자신.속성읽기(Leser_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstante_VALUE[INDEX][0] != 1:
            raise 컴파일오류('string_VALUE konstante_VALUE formaat_VALUE Fout')
        return 자신.konstante_VALUE[INDEX][1]

    def Klas_naam(자신, INDEX):
        return 자신.문자(자신.konstante_VALUE[INDEX][1])

    def Naslaan(자신, INDEX):
        eienaar_VALUE, naam_formaat = 자신.konstante_VALUE[INDEX][1]
        Naam, formaat_VALUE = 자신.konstante_VALUE[naam_formaat][1]
        return 자신.Klas_naam(eienaar_VALUE), 자신.문자(Naam), 자신.문자(formaat_VALUE)

    def 속성읽기(자신, Leser_VALUE):
        maatreël = {}
        for _ in range(Leser_VALUE.수('H')):
            Naam = 자신.문자(Leser_VALUE.수('H'))
            maatreël[Naam] = Leser_VALUE.Lees(Leser_VALUE.수('I'))
        return maatreël

    def 멤버읽기(자신, Leser_VALUE):
        maatreël = []
        for _ in range(Leser_VALUE.수('H')):
            toegang_inskrywing = Leser_VALUE.수('H')
            Naam = 자신.문자(Leser_VALUE.수('H'))
            formaat_VALUE = 자신.문자(Leser_VALUE.수('H'))
            maatreël.append((toegang_inskrywing, Naam, formaat_VALUE, 자신.속성읽기(Leser_VALUE)))
        return maatreël


def 형식읽기(string_VALUE):
    maatreël = []
    Posisie = 0
    while Posisie < len(string_VALUE):
        for formaat_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if string_VALUE.startswith(formaat_VALUE, Posisie):
                maatreël.append(formaat_VALUE)
                Posisie += len(formaat_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 datatipe: ' + string_VALUE)
    return maatreël


def 함수형식(서술):
    인수, teruggee_maatreël = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    teruggee_TYPE = 형식읽기(teruggee_maatreël)
    if 'V' in 인수 or len(teruggee_TYPE) != 1:
        raise 컴파일오류('funksie_VALUE 서술 formaat_VALUE Fout: ' + 서술)
    return 인수, teruggee_maatreël


def simbool(종류, *부분):
    Bron = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Bron).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 funksie_VALUE 서술에 대해서만 허용한다.
def uitvoer_bevel(인수=None):
    ontleder_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK bron_boom bou_stelsel')
    ontleder_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    ontleder_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/Klas_VALUE 디렉터리')
    ontleder_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 bou_stelsel JDK 또는 openjdk-build의 부트 JDK Pad')
    ontleder_48ee4b1b.add_argument('--bundle-runtime', help='uitvoer_bevel 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    ontleder_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK program_oopmaker/bron_boom 빌드의 C 컴파일러')
    ontleder_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    ontleder_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 bou_stelsel 작업 수')
    ontleder_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 bou_stelsel teiken (예: aarch64-linux-gnu)')
    ontleder_48ee4b1b.add_argument('--sysroot', help='교차 bou_stelsel 대상의 libc/헤더/biblioteek 루트')
    ontleder_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formaat_VALUE')
    ontleder_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Klas_VALUE.funksie_VALUE (자체 스택 ABI)')
    ontleder_48ee4b1b.add_argument('--entry', help='예: 계산.Loop (openjdk-build 이외 대상에서 필수)')
    ontleder_48ee4b1b.add_argument('-o', '--output', required=True, help='uitvoer_bevel ELF/.o Afvoer; openjdk-build는 전용 bou_stelsel 디렉터리')
    ontleder_48ee4b1b.add_argument('sources', nargs='+')
    인자 = ontleder_48ee4b1b.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK bron_boom 디렉터리 하나와 --java-home 부트 JDK, -o bou_stelsel 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Fout:
            raise 컴파일오류(str(Fout))
        return
    if not 인자.entry:
        ontleder_48ee4b1b.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build teiken 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Skep_inskrywing
        Skep_inskrywing(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk teiken 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for toeken_VALUE in 인자.export: 자바명령.extend(['--export', toeken_VALUE])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        uitvoer_bevel()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Fout:
        print('bou_bron Fout: ' + str(Fout), file=sys.stderr)
        sys.exit(1)
