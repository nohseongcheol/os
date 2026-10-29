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


class kompileringsfejl(Exception):
    pass


class 자료읽기:
    def __init__(자신, data):
        자신.data = data
        자신.Placering = 0

    def Læse(자신, varighed_VÆRDI):
        if varighed_VÆRDI < 0 or 자신.Placering + varighed_VÆRDI > len(자신.data):
            raise kompileringsfejl('잘린 Hold_VÆRDI 또는 Kommando data')
        KR = 자신.data[자신.Placering:자신.Placering + varighed_VÆRDI]
        자신.Placering += varighed_VÆRDI
        return KR

    def tal(자신, format_VÆRDI):
        return struct.unpack('>' + format_VÆRDI, 자신.Læse(struct.calcsize('>' + format_VÆRDI)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    streng_VÆRDI = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return streng_VÆRDI.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Hold_VÆRDI:
    def __init__(자신, Sti):
        자신.Sti = Sti
        Læser_VÆRDI = 자료읽기(Sti.read_bytes())
        if Læser_VÆRDI.tal('I') != 0xcafebabe:
            raise kompileringsfejl('Java Hold_VÆRDI 표식이 아님')
        Læser_VÆRDI.Læse(4)
        vare_TÆL = Læser_VÆRDI.tal('H')
        자신.konstant_VÆRDI = [None] * vare_TÆL
        INDEKS = 1
        while INDEKS < vare_TÆL:
            종류 = Læser_VÆRDI.tal('B')
            if 종류 == 1:
                VÆRDI = 수정유티에프해독(Læser_VÆRDI.Læse(Læser_VÆRDI.tal('H')))
            elif 종류 == 3:
                VÆRDI = Læser_VÆRDI.tal('i')
            elif 종류 == 4:
                VÆRDI = Læser_VÆRDI.Læse(4)
            elif 종류 in (5, 6):
                VÆRDI = Læser_VÆRDI.Læse(8)
            elif 종류 in (7, 8, 16):
                VÆRDI = Læser_VÆRDI.tal('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VÆRDI = (Læser_VÆRDI.tal('H'), Læser_VÆRDI.tal('H'))
            elif 종류 == 15:
                VÆRDI = (Læser_VÆRDI.tal('B'), Læser_VÆRDI.tal('H'))
            else:
                raise kompileringsfejl('지원하지 않는 konstant_VÆRDI 종류: {}'.format(종류))
            자신.konstant_VÆRDI[INDEKS] = (종류, VÆRDI)
            INDEKS += 2 if 종류 in (5, 6) else 1
        자신.åbne_post = Læser_VÆRDI.tal('H')
        자신.Navn = 자신.klassenavn(Læser_VÆRDI.tal('H'))
        overordnet_VÆRDI = Læser_VÆRDI.tal('H')
        if 자신.klassenavn(overordnet_VÆRDI) != 'java/lang/Object' or Læser_VÆRDI.tal('H') != 0:
            raise kompileringsfejl(자신.Navn + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.feltværdi = 자신.멤버읽기(Læser_VÆRDI)
        자신.FUNKTION_VÆRDI = 자신.멤버읽기(Læser_VÆRDI)
        자신.속성읽기(Læser_VÆRDI)

    def 문자(자신, INDEKS):
        if 자신.konstant_VÆRDI[INDEKS][0] != 1:
            raise kompileringsfejl('streng_VÆRDI konstant_VÆRDI format_VÆRDI fejl')
        return 자신.konstant_VÆRDI[INDEKS][1]

    def klassenavn(자신, INDEKS):
        return 자신.문자(자신.konstant_VÆRDI[INDEKS][1])

    def referere(자신, INDEKS):
        ejer_VÆRDI, navn_format = 자신.konstant_VÆRDI[INDEKS][1]
        Navn, format_VÆRDI = 자신.konstant_VÆRDI[navn_format][1]
        return 자신.klassenavn(ejer_VÆRDI), 자신.문자(Navn), 자신.문자(format_VÆRDI)

    def 속성읽기(자신, Læser_VÆRDI):
        KR = {}
        for _ in range(Læser_VÆRDI.tal('H')):
            Navn = 자신.문자(Læser_VÆRDI.tal('H'))
            KR[Navn] = Læser_VÆRDI.Læse(Læser_VÆRDI.tal('I'))
        return KR

    def 멤버읽기(자신, Læser_VÆRDI):
        KR = []
        for _ in range(Læser_VÆRDI.tal('H')):
            åbne_post = Læser_VÆRDI.tal('H')
            Navn = 자신.문자(Læser_VÆRDI.tal('H'))
            format_VÆRDI = 자신.문자(Læser_VÆRDI.tal('H'))
            KR.append((åbne_post, Navn, format_VÆRDI, 자신.속성읽기(Læser_VÆRDI)))
        return KR


def 형식읽기(streng_VÆRDI):
    KR = []
    Placering = 0
    while Placering < len(streng_VÆRDI):
        for format_VÆRDI in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if streng_VÆRDI.startswith(format_VÆRDI, Placering):
                KR.append(format_VÆRDI)
                Placering += len(format_VÆRDI)
                break
        else:
            raise kompileringsfejl('지원하지 않는 datatype: ' + streng_VÆRDI)
    return KR


def 함수형식(서술):
    Argumenter, returnere_KR = 서술[1:].split(')')
    Argumenter = 형식읽기(Argumenter)
    returnere_Type = 형식읽기(returnere_KR)
    if 'V' in Argumenter or len(returnere_Type) != 1:
        raise kompileringsfejl('FUNKTION_VÆRDI 서술 format_VÆRDI fejl: ' + 서술)
    return Argumenter, returnere_KR


def symbol(종류, *부분):
    KILDE = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(KILDE).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNKTION_VÆRDI 서술에 대해서만 허용한다.
def Udfør_kommando(Argumenter=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='eget Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK kilde_træ build_System')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 tilføj_post JAR/Hold_VÆRDI 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 build_System JDK 또는 openjdk-build의 부트 JDK Sti')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='Udfør_kommando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK app_Kvikstart/kilde_træ 빌드의 C compiler')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ compiler')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 build_System 작업 tal')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 build_System mål (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 build_System 대상의 libc/헤더/bibliotek 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VÆRDI')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Hold_VÆRDI.FUNKTION_VÆRDI (eget operand_Stak ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.Kør_2 (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='Udfør_kommando ELF/.o Udgang; openjdk-build는 전용 build_System 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parameter_argument = parser_48ee4b1b.parse_args(Argumenter)
    if parameter_argument.target == 'openjdk-build':
        if len(parameter_argument.sources) != 1 or not parameter_argument.java_home or parameter_argument.entry or parameter_argument.export or parameter_argument.classpath or parameter_argument.bundle_runtime:
            raise kompileringsfejl('openjdk-build: OpenJDK kilde_træ 디렉터리 하나와 --java-home 부트 JDK, -o build_System 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argument.sources[0], parameter_argument.output, parameter_argument.java_home, parameter_argument.jobs, parameter_argument.openjdk_target,
                  parameter_argument.sysroot, None if parameter_argument.cc == 'cc' else parameter_argument.cc, parameter_argument.cxx, parameter_argument.configure_arg)
        except BuildError as fejl:
            raise kompileringsfejl(str(fejl))
        return
    if not parameter_argument.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parameter_argument.cxx or parameter_argument.openjdk_target or parameter_argument.sysroot or parameter_argument.configure_arg or parameter_argument.jobs != 2:
        raise kompileringsfejl('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build mål 전용')
    if parameter_argument.target == 'openjdk':
        sys.modules.setdefault('compiler', sys.modules[__name__])
        from eksekverbar_fil import åbne_post_81b8d99b
        åbne_post_81b8d99b(parameter_argument)
        return
    if parameter_argument.classpath or parameter_argument.java_home or parameter_argument.bundle_runtime or parameter_argument.cc != 'cc':
        raise kompileringsfejl('classpath/java-home/bundle-runtime/cc 옵션은 openjdk mål 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argument.target, '--entry', parameter_argument.entry, '-o', parameter_argument.output]
    for Tildel_VÆRDI in parameter_argument.export: 자바명령.extend(['--export', Tildel_VÆRDI])
    subprocess.run(자바명령+parameter_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Udfør_kommando()
    except (kompileringsfejl, OSError, ValueError, subprocess.CalledProcessError) as fejl:
        print('kompilere_kilde fejl: ' + str(fejl), file=sys.stderr)
        sys.exit(1)
