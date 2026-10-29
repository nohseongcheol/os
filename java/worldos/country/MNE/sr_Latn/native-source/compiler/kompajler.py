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


class greška_u_kompajliranju(Exception):
    pass


class 자료읽기:
    def __init__(자신, podaci):
        자신.podaci = podaci
        자신.pozicija = 0

    def 읽기(자신, 길이):
        if 길이 < 0 or 자신.pozicija + 길이 > len(자신.podaci):
            raise greška_u_kompajliranju('잘린 Razred_VALUE 또는 komanda podaci')
        KR = 자신.podaci[자신.pozicija:자신.pozicija + 길이]
        자신.pozicija += 길이
        return KR

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.읽기(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(podaci):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    niska_VALUE = podaci.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return niska_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Razred_VALUE:
    def __init__(자신, putanja):
        자신.putanja = putanja
        Čitač_VALUE = 자료읽기(putanja.read_bytes())
        if Čitač_VALUE.수('I') != 0xcafebabe:
            raise greška_u_kompajliranju('Java Razred_VALUE 표식이 아님')
        Čitač_VALUE.읽기(4)
        stavka_COUNT = Čitač_VALUE.수('H')
        자신.konstanta_VALUE = [None] * stavka_COUNT
        INDEX = 1
        while INDEX < stavka_COUNT:
            종류 = Čitač_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Čitač_VALUE.읽기(Čitač_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Čitač_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Čitač_VALUE.읽기(4)
            elif 종류 in (5, 6):
                VALUE = Čitač_VALUE.읽기(8)
            elif 종류 in (7, 8, 16):
                VALUE = Čitač_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Čitač_VALUE.수('H'), Čitač_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Čitač_VALUE.수('B'), Čitač_VALUE.수('H'))
            else:
                raise greška_u_kompajliranju('지원하지 않는 konstanta_VALUE 종류: {}'.format(종류))
            자신.konstanta_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.pristup_stavka = Čitač_VALUE.수('H')
        자신.ime = 자신.ime_klase(Čitač_VALUE.수('H'))
        nadređen_VALUE = Čitač_VALUE.수('H')
        if 자신.ime_klase(nadređen_VALUE) != 'java/lang/Object' or Čitač_VALUE.수('H') != 0:
            raise greška_u_kompajliranju(자신.ime + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.vrednost_polja = 자신.멤버읽기(Čitač_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Čitač_VALUE)
        자신.속성읽기(Čitač_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstanta_VALUE[INDEX][0] != 1:
            raise greška_u_kompajliranju('niska_VALUE konstanta_VALUE format_VALUE greška')
        return 자신.konstanta_VALUE[INDEX][1]

    def ime_klase(자신, INDEX):
        return 자신.문자(자신.konstanta_VALUE[INDEX][1])

    def referenca(자신, INDEX):
        vlasnik_VALUE, ime_format = 자신.konstanta_VALUE[INDEX][1]
        ime, format_VALUE = 자신.konstanta_VALUE[ime_format][1]
        return 자신.ime_klase(vlasnik_VALUE), 자신.문자(ime), 자신.문자(format_VALUE)

    def 속성읽기(자신, Čitač_VALUE):
        KR = {}
        for _ in range(Čitač_VALUE.수('H')):
            ime = 자신.문자(Čitač_VALUE.수('H'))
            KR[ime] = Čitač_VALUE.읽기(Čitač_VALUE.수('I'))
        return KR

    def 멤버읽기(자신, Čitač_VALUE):
        KR = []
        for _ in range(Čitač_VALUE.수('H')):
            pristup_stavka = Čitač_VALUE.수('H')
            ime = 자신.문자(Čitač_VALUE.수('H'))
            format_VALUE = 자신.문자(Čitač_VALUE.수('H'))
            KR.append((pristup_stavka, ime, format_VALUE, 자신.속성읽기(Čitač_VALUE)))
        return KR


def 형식읽기(niska_VALUE):
    KR = []
    pozicija = 0
    while pozicija < len(niska_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if niska_VALUE.startswith(format_VALUE, pozicija):
                KR.append(format_VALUE)
                pozicija += len(format_VALUE)
                break
        else:
            raise greška_u_kompajliranju('지원하지 않는 tip_podataka: ' + niska_VALUE)
    return KR


def 함수형식(서술):
    인수, vratiti_KR = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    vratiti_tip = 형식읽기(vratiti_KR)
    if 'V' in 인수 or len(vratiti_tip) != 1:
        raise greška_u_kompajliranju('FUNCTION_VALUE 서술 format_VALUE greška: ' + 서술)
    return 인수, vratiti_KR


def simbol(종류, *부분):
    izvor = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(izvor).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def Izvrši_komanda(인수=None):
    analizator_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK izvor_stablo verzija_sistem')
    analizator_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analizator_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 dodati_stavka JAR/Razred_VALUE 디렉터리')
    analizator_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 verzija_sistem JDK 또는 openjdk-build의 부트 JDK putanja')
    analizator_48ee4b1b.add_argument('--bundle-runtime', help='Izvrši_komanda 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analizator_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK program_pokretač/izvor_stablo 빌드의 C kompajler')
    analizator_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompajler')
    analizator_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 verzija_sistem 작업 수')
    analizator_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 verzija_sistem cilj (예: aarch64-linux-gnu)')
    analizator_48ee4b1b.add_argument('--sysroot', help='교차 verzija_sistem 대상의 libc/헤더/biblioteka 루트')
    analizator_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    analizator_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Razred_VALUE.FUNCTION_VALUE (자체 operand_stek ABI)')
    analizator_48ee4b1b.add_argument('--entry', help='예: 계산.koristiti (openjdk-build 이외 대상에서 필수)')
    analizator_48ee4b1b.add_argument('-o', '--output', required=True, help='Izvrši_komanda ELF/.o 출력; openjdk-build는 전용 verzija_sistem 디렉터리')
    analizator_48ee4b1b.add_argument('sources', nargs='+')
    parametar_argument = analizator_48ee4b1b.parse_args(인수)
    if parametar_argument.target == 'openjdk-build':
        if len(parametar_argument.sources) != 1 or not parametar_argument.java_home or parametar_argument.entry or parametar_argument.export or parametar_argument.classpath or parametar_argument.bundle_runtime:
            raise greška_u_kompajliranju('openjdk-build: OpenJDK izvor_stablo 디렉터리 하나와 --java-home 부트 JDK, -o verzija_sistem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametar_argument.sources[0], parametar_argument.output, parametar_argument.java_home, parametar_argument.jobs, parametar_argument.openjdk_target,
                  parametar_argument.sysroot, None if parametar_argument.cc == 'cc' else parametar_argument.cc, parametar_argument.cxx, parametar_argument.configure_arg)
        except BuildError as greška:
            raise greška_u_kompajliranju(str(greška))
        return
    if not parametar_argument.entry:
        analizator_48ee4b1b.error('--entry is required for this target')
    if parametar_argument.cxx or parametar_argument.openjdk_target or parametar_argument.sysroot or parametar_argument.configure_arg or parametar_argument.jobs != 2:
        raise greška_u_kompajliranju('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build cilj 전용')
    if parametar_argument.target == 'openjdk':
        sys.modules.setdefault('kompajler', sys.modules[__name__])
        from 실행파일 import Create_stavka
        Create_stavka(parametar_argument)
        return
    if parametar_argument.classpath or parametar_argument.java_home or parametar_argument.bundle_runtime or parametar_argument.cc != 'cc':
        raise greška_u_kompajliranju('classpath/java-home/bundle-runtime/cc 옵션은 openjdk cilj 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametar_argument.target, '--entry', parametar_argument.entry, '-o', parametar_argument.output]
    for Dodeli_VALUE in parametar_argument.export: 자바명령.extend(['--export', Dodeli_VALUE])
    subprocess.run(자바명령+parametar_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Izvrši_komanda()
    except (greška_u_kompajliranju, OSError, ValueError, subprocess.CalledProcessError) as greška:
        print('kompajlirati_izvor greška: ' + str(greška), file=sys.stderr)
        sys.exit(1)
