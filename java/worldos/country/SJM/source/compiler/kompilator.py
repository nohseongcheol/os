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

    def Les(자신, lengde_VERDI):
        if lengde_VERDI < 0 or 자신.Posisjon + lengde_VERDI > len(자신.data):
            raise 컴파일오류('잘린 time_VERDI 또는 Kommando data')
        KR = 자신.data[자신.Posisjon:자신.Posisjon + lengde_VERDI]
        자신.Posisjon += lengde_VERDI
        return KR

    def nummer(자신, format_VERDI):
        return struct.unpack('>' + format_VERDI, 자신.Les(struct.calcsize('>' + format_VERDI)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    streng_VERDI = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return streng_VERDI.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class time_VERDI:
    def __init__(자신, Sti):
        자신.Sti = Sti
        Leser_VERDI = 자료읽기(Sti.read_bytes())
        if Leser_VERDI.nummer('I') != 0xcafebabe:
            raise 컴파일오류('Java time_VERDI 표식이 아님')
        Leser_VERDI.Les(4)
        vare_ANTALL = Leser_VERDI.nummer('H')
        자신.konstant_VERDI = [None] * vare_ANTALL
        INDEKS = 1
        while INDEKS < vare_ANTALL:
            종류 = Leser_VERDI.nummer('B')
            if 종류 == 1:
                VERDI = 수정유티에프해독(Leser_VERDI.Les(Leser_VERDI.nummer('H')))
            elif 종류 == 3:
                VERDI = Leser_VERDI.nummer('i')
            elif 종류 == 4:
                VERDI = Leser_VERDI.Les(4)
            elif 종류 in (5, 6):
                VERDI = Leser_VERDI.Les(8)
            elif 종류 in (7, 8, 16):
                VERDI = Leser_VERDI.nummer('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VERDI = (Leser_VERDI.nummer('H'), Leser_VERDI.nummer('H'))
            elif 종류 == 15:
                VERDI = (Leser_VERDI.nummer('B'), Leser_VERDI.nummer('H'))
            else:
                raise 컴파일오류('지원하지 않는 konstant_VERDI 종류: {}'.format(종류))
            자신.konstant_VERDI[INDEKS] = (종류, VERDI)
            INDEKS += 2 if 종류 in (5, 6) else 1
        자신.tilgang_oppføring = Leser_VERDI.nummer('H')
        자신.Navn = 자신.klassenavn(Leser_VERDI.nummer('H'))
        overordnet_VERDI_881a8172 = Leser_VERDI.nummer('H')
        if 자신.klassenavn(overordnet_VERDI_881a8172) != 'java/lang/Object' or Leser_VERDI.nummer('H') != 0:
            raise 컴파일오류(자신.Navn + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.feltverdi = 자신.멤버읽기(Leser_VERDI)
        자신.FUNKSJON_VERDI = 자신.멤버읽기(Leser_VERDI)
        자신.속성읽기(Leser_VERDI)

    def 문자(자신, INDEKS):
        if 자신.konstant_VERDI[INDEKS][0] != 1:
            raise 컴파일오류('streng_VERDI konstant_VERDI format_VERDI feil')
        return 자신.konstant_VERDI[INDEKS][1]

    def klassenavn(자신, INDEKS):
        return 자신.문자(자신.konstant_VERDI[INDEKS][1])

    def referere(자신, INDEKS):
        eier_VERDI, navn_format = 자신.konstant_VERDI[INDEKS][1]
        Navn, format_VERDI = 자신.konstant_VERDI[navn_format][1]
        return 자신.klassenavn(eier_VERDI), 자신.문자(Navn), 자신.문자(format_VERDI)

    def 속성읽기(자신, Leser_VERDI):
        KR = {}
        for _ in range(Leser_VERDI.nummer('H')):
            Navn = 자신.문자(Leser_VERDI.nummer('H'))
            KR[Navn] = Leser_VERDI.Les(Leser_VERDI.nummer('I'))
        return KR

    def 멤버읽기(자신, Leser_VERDI):
        KR = []
        for _ in range(Leser_VERDI.nummer('H')):
            tilgang_oppføring = Leser_VERDI.nummer('H')
            Navn = 자신.문자(Leser_VERDI.nummer('H'))
            format_VERDI = 자신.문자(Leser_VERDI.nummer('H'))
            KR.append((tilgang_oppføring, Navn, format_VERDI, 자신.속성읽기(Leser_VERDI)))
        return KR


def 형식읽기(streng_VERDI):
    KR = []
    Posisjon = 0
    while Posisjon < len(streng_VERDI):
        for format_VERDI in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if streng_VERDI.startswith(format_VERDI, Posisjon):
                KR.append(format_VERDI)
                Posisjon += len(format_VERDI)
                break
        else:
            raise 컴파일오류('지원하지 않는 datatype: ' + streng_VERDI)
    return KR


def 함수형식(서술):
    Argumenter, return_KR = 서술[1:].split(')')
    Argumenter = 형식읽기(Argumenter)
    return_Type = 형식읽기(return_KR)
    if 'V' in Argumenter or len(return_Type) != 1:
        raise 컴파일오류('FUNKSJON_VERDI 서술 format_VERDI feil: ' + 서술)
    return Argumenter, return_KR


def symbol(종류, *부분):
    KILDE = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(KILDE).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNKSJON_VERDI 서술에 대해서만 허용한다.
def Utfør_kommando(Argumenter=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='eget Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK kilde_tre bygg_System')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Tilføye_oppføring JAR/time_VERDI 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 bygg_System JDK 또는 openjdk-build의 부트 JDK Sti')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='Utfør_kommando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK app_appskuff/kilde_tre 빌드의 C kompilator')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompilator')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 bygg_System 작업 nummer')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 bygg_System mål (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 bygg_System 대상의 libc/헤더/bibliotek 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VERDI')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=time_VERDI.FUNKSJON_VERDI (eget operand_stakk ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.Kjør_2 (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='Utfør_kommando ELF/.o Utgang; openjdk-build는 전용 bygg_System 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parameter_argument = parser_48ee4b1b.parse_args(Argumenter)
    if parameter_argument.target == 'openjdk-build':
        if len(parameter_argument.sources) != 1 or not parameter_argument.java_home or parameter_argument.entry or parameter_argument.export or parameter_argument.classpath or parameter_argument.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK kilde_tre 디렉터리 하나와 --java-home 부트 JDK, -o bygg_System 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argument.sources[0], parameter_argument.output, parameter_argument.java_home, parameter_argument.jobs, parameter_argument.openjdk_target,
                  parameter_argument.sysroot, None if parameter_argument.cc == 'cc' else parameter_argument.cc, parameter_argument.cxx, parameter_argument.configure_arg)
        except BuildError as feil:
            raise 컴파일오류(str(feil))
        return
    if not parameter_argument.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parameter_argument.cxx or parameter_argument.openjdk_target or parameter_argument.sysroot or parameter_argument.configure_arg or parameter_argument.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build mål 전용')
    if parameter_argument.target == 'openjdk':
        sys.modules.setdefault('kompilator', sys.modules[__name__])
        from kjørbar_fil import åpne_oppføring
        åpne_oppføring(parameter_argument)
        return
    if parameter_argument.classpath or parameter_argument.java_home or parameter_argument.bundle_runtime or parameter_argument.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk mål 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argument.target, '--entry', parameter_argument.entry, '-o', parameter_argument.output]
    for overdra_VERDI in parameter_argument.export: 자바명령.extend(['--export', overdra_VERDI])
    subprocess.run(자바명령+parameter_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Utfør_kommando()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as feil:
        print('kompilere_kilde feil: ' + str(feil), file=sys.stderr)
        sys.exit(1)
