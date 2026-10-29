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
    def __init__(자신, podaci):
        자신.podaci = podaci
        자신.Pozicija = 0

    def Čitaj(자신, dužina_VALUE):
        if dužina_VALUE < 0 or 자신.Pozicija + dužina_VALUE > len(자신.podaci):
            raise 컴파일오류('잘린 klasa_VALUE 또는 Naredba podaci')
        mjera = 자신.podaci[자신.Pozicija:자신.Pozicija + dužina_VALUE]
        자신.Pozicija += dužina_VALUE
        return mjera

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.Čitaj(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(podaci):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    string_VALUE = podaci.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return string_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klasa_VALUE:
    def __init__(자신, Putanja):
        자신.Putanja = Putanja
        Čitač_VALUE = 자료읽기(Putanja.read_bytes())
        if Čitač_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java klasa_VALUE 표식이 아님')
        Čitač_VALUE.Čitaj(4)
        stavka_COUNT = Čitač_VALUE.수('H')
        자신.konstanta_VALUE = [None] * stavka_COUNT
        INDEX = 1
        while INDEX < stavka_COUNT:
            종류 = Čitač_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Čitač_VALUE.Čitaj(Čitač_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Čitač_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Čitač_VALUE.Čitaj(4)
            elif 종류 in (5, 6):
                VALUE = Čitač_VALUE.Čitaj(8)
            elif 종류 in (7, 8, 16):
                VALUE = Čitač_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Čitač_VALUE.수('H'), Čitač_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Čitač_VALUE.수('B'), Čitač_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 konstanta_VALUE 종류: {}'.format(종류))
            자신.konstanta_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.pristup_unos = Čitač_VALUE.수('H')
        자신.Naziv = 자신.naziv_klase(Čitač_VALUE.수('H'))
        roditelj_VALUE = Čitač_VALUE.수('H')
        if 자신.naziv_klase(roditelj_VALUE) != 'java/lang/Object' or Čitač_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Naziv + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.polje_VALUE = 자신.멤버읽기(Čitač_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Čitač_VALUE)
        자신.속성읽기(Čitač_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstanta_VALUE[INDEX][0] != 1:
            raise 컴파일오류('string_VALUE konstanta_VALUE format_VALUE GRESKA')
        return 자신.konstanta_VALUE[INDEX][1]

    def naziv_klase(자신, INDEX):
        return 자신.문자(자신.konstanta_VALUE[INDEX][1])

    def Reference(자신, INDEX):
        vlasnik_VALUE, naziv_format = 자신.konstanta_VALUE[INDEX][1]
        Naziv, format_VALUE = 자신.konstanta_VALUE[naziv_format][1]
        return 자신.naziv_klase(vlasnik_VALUE), 자신.문자(Naziv), 자신.문자(format_VALUE)

    def 속성읽기(자신, Čitač_VALUE):
        mjera = {}
        for _ in range(Čitač_VALUE.수('H')):
            Naziv = 자신.문자(Čitač_VALUE.수('H'))
            mjera[Naziv] = Čitač_VALUE.Čitaj(Čitač_VALUE.수('I'))
        return mjera

    def 멤버읽기(자신, Čitač_VALUE):
        mjera = []
        for _ in range(Čitač_VALUE.수('H')):
            pristup_unos = Čitač_VALUE.수('H')
            Naziv = 자신.문자(Čitač_VALUE.수('H'))
            format_VALUE = 자신.문자(Čitač_VALUE.수('H'))
            mjera.append((pristup_unos, Naziv, format_VALUE, 자신.속성읽기(Čitač_VALUE)))
        return mjera


def 형식읽기(string_VALUE):
    mjera = []
    Pozicija = 0
    while Pozicija < len(string_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if string_VALUE.startswith(format_VALUE, Pozicija):
                mjera.append(format_VALUE)
                Pozicija += len(format_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 vrsta_podataka: ' + string_VALUE)
    return mjera


def 함수형식(서술):
    Argumenti, vratiti_mjera = 서술[1:].split(')')
    Argumenti = 형식읽기(Argumenti)
    vratiti_TYPE = 형식읽기(vratiti_mjera)
    if 'V' in Argumenti or len(vratiti_TYPE) != 1:
        raise 컴파일오류('FUNCTION_VALUE 서술 format_VALUE GRESKA: ' + 서술)
    return Argumenti, vratiti_mjera


def simbol(종류, *부분):
    IZVOR = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(IZVOR).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def Izvrši_komanda(Argumenti=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK izvor_stablo verzija_sistem')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/klasa_VALUE 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 verzija_sistem JDK 또는 openjdk-build의 부트 JDK Putanja')
    해석기.add_argument('--bundle-runtime', help='Izvrši_komanda 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK program_pokretač/izvor_stablo 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 verzija_sistem 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 verzija_sistem cilj (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 verzija_sistem 대상의 libc/헤더/biblioteka 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=klasa_VALUE.FUNCTION_VALUE (자체 operand_snop ABI)')
    해석기.add_argument('--entry', help='예: 계산.Pokreni (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='Izvrši_komanda ELF/.o Ispis; openjdk-build는 전용 verzija_sistem 디렉터리')
    해석기.add_argument('sources', nargs='+')
    parametar_argument = 해석기.parse_args(Argumenti)
    if parametar_argument.target == 'openjdk-build':
        if len(parametar_argument.sources) != 1 or not parametar_argument.java_home or parametar_argument.entry or parametar_argument.export or parametar_argument.classpath or parametar_argument.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK izvor_stablo 디렉터리 하나와 --java-home 부트 JDK, -o verzija_sistem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametar_argument.sources[0], parametar_argument.output, parametar_argument.java_home, parametar_argument.jobs, parametar_argument.openjdk_target,
                  parametar_argument.sysroot, None if parametar_argument.cc == 'cc' else parametar_argument.cc, parametar_argument.cxx, parametar_argument.configure_arg)
        except BuildError as GRESKA:
            raise 컴파일오류(str(GRESKA))
        return
    if not parametar_argument.entry:
        해석기.error('--entry is required for this target')
    if parametar_argument.cxx or parametar_argument.openjdk_target or parametar_argument.sysroot or parametar_argument.configure_arg or parametar_argument.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build cilj 전용')
    if parametar_argument.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Create_unos
        Create_unos(parametar_argument)
        return
    if parametar_argument.classpath or parametar_argument.java_home or parametar_argument.bundle_runtime or parametar_argument.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk cilj 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametar_argument.target, '--entry', parametar_argument.entry, '-o', parametar_argument.output]
    for dodijeliti_VALUE in parametar_argument.export: 자바명령.extend(['--export', dodijeliti_VALUE])
    subprocess.run(자바명령+parametar_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Izvrši_komanda()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as GRESKA:
        print('napraviti_izvor GRESKA: ' + str(GRESKA), file=sys.stderr)
        sys.exit(1)
