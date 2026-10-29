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


class kompileringsfel(Exception):
    pass


class läsa_data:
    def __init__(자신, data):
        자신.data = data
        자신.position = 0

    def Läs(자신, längd_värde):
        if längd_värde < 0 or 자신.position + längd_värde > len(자신.data):
            raise kompileringsfel('잘린 Kurs_värde 또는 kommando data')
        RESULTAT = 자신.data[자신.position:자신.position + längd_värde]
        자신.position += längd_värde
        return RESULTAT

    def nummer(자신, format_värde):
        return struct.unpack('>' + format_värde, 자신.Läs(struct.calcsize('>' + format_värde)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    sträng_värde = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return sträng_värde.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Kurs_värde:
    def __init__(자신, sökväg_2):
        자신.sökväg_2 = sökväg_2
        Läsare_värde = läsa_data(sökväg_2.read_bytes())
        if Läsare_värde.nummer('I') != 0xcafebabe:
            raise kompileringsfel('Java Kurs_värde 표식이 아님')
        Läsare_värde.Läs(4)
        objekt_ANTAL = Läsare_värde.nummer('H')
        자신.konstant_värde = [None] * objekt_ANTAL
        INDEX = 1
        while INDEX < objekt_ANTAL:
            variant_värde = Läsare_värde.nummer('B')
            if variant_värde == 1:
                värde = 수정유티에프해독(Läsare_värde.Läs(Läsare_värde.nummer('H')))
            elif variant_värde == 3:
                värde = Läsare_värde.nummer('i')
            elif variant_värde == 4:
                värde = Läsare_värde.Läs(4)
            elif variant_värde in (5, 6):
                värde = Läsare_värde.Läs(8)
            elif variant_värde in (7, 8, 16):
                värde = Läsare_värde.nummer('H')
            elif variant_värde in (9, 10, 11, 12, 18):
                värde = (Läsare_värde.nummer('H'), Läsare_värde.nummer('H'))
            elif variant_värde == 15:
                värde = (Läsare_värde.nummer('B'), Läsare_värde.nummer('H'))
            else:
                raise kompileringsfel('지원하지 않는 konstant_värde variant_värde: {}'.format(variant_värde))
            자신.konstant_värde[INDEX] = (variant_värde, värde)
            INDEX += 2 if variant_värde in (5, 6) else 1
        자신.ansluta_post = Läsare_värde.nummer('H')
        자신.Namn = 자신.klassnamn(Läsare_värde.nummer('H'))
        överordnad_värde = Läsare_värde.nummer('H')
        if 자신.klassnamn(överordnad_värde) != 'java/lang/Object' or Läsare_värde.nummer('H') != 0:
            raise kompileringsfel(자신.Namn + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.fältvärde = 자신.멤버읽기(Läsare_värde)
        자신.FUNKTION_värde = 자신.멤버읽기(Läsare_värde)
        자신.läsa_personlig_information(Läsare_värde)

    def 문자(자신, INDEX):
        if 자신.konstant_värde[INDEX][0] != 1:
            raise kompileringsfel('sträng_värde konstant_värde format_värde fel')
        return 자신.konstant_värde[INDEX][1]

    def klassnamn(자신, INDEX):
        return 자신.문자(자신.konstant_värde[INDEX][1])

    def referens(자신, INDEX):
        ägare_värde, namn_format = 자신.konstant_värde[INDEX][1]
        Namn, format_värde = 자신.konstant_värde[namn_format][1]
        return 자신.klassnamn(ägare_värde), 자신.문자(Namn), 자신.문자(format_värde)

    def läsa_personlig_information(자신, Läsare_värde):
        RESULTAT = {}
        for _ in range(Läsare_värde.nummer('H')):
            Namn = 자신.문자(Läsare_värde.nummer('H'))
            RESULTAT[Namn] = Läsare_värde.Läs(Läsare_värde.nummer('I'))
        return RESULTAT

    def 멤버읽기(자신, Läsare_värde):
        RESULTAT = []
        for _ in range(Läsare_värde.nummer('H')):
            ansluta_post = Läsare_värde.nummer('H')
            Namn = 자신.문자(Läsare_värde.nummer('H'))
            format_värde = 자신.문자(Läsare_värde.nummer('H'))
            RESULTAT.append((ansluta_post, Namn, format_värde, 자신.läsa_personlig_information(Läsare_värde)))
        return RESULTAT


def 형식읽기(sträng_värde):
    RESULTAT = []
    position = 0
    while position < len(sträng_värde):
        for format_värde in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if sträng_värde.startswith(format_värde, position):
                RESULTAT.append(format_värde)
                position += len(format_värde)
                break
        else:
            raise kompileringsfel('지원하지 않는 datatyp: ' + sträng_värde)
    return RESULTAT


def 함수형식(서술):
    argument, Retur_KR = 서술[1:].split(')')
    argument = 형식읽기(argument)
    Retur_Typ = 형식읽기(Retur_KR)
    if 'V' in argument or len(Retur_Typ) != 1:
        raise kompileringsfel('FUNKTION_värde 서술 format_värde fel: ' + 서술)
    return argument, Retur_KR


def symbol(variant_värde, *부분):
    källfil = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(variant_värde, hashlib.sha256(källfil).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNKTION_värde 서술에 대해서만 허용한다.
def köra_kommando(argument=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='eget Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK källa_träd version_System')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Lägga_till_post JAR/Kurs_värde 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 version_System JDK 또는 openjdk-build의 부트 JDK sökväg_2')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='köra_kommando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK app_Startbild/källa_träd 빌드의 C kompilerare')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompilerare')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 version_System 작업 nummer')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 version_System mål (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 version_System 대상의 libc/헤더/bibliotek 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_värde')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Kurs_värde.FUNKTION_värde (eget operand_Stack ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.Kör (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='köra_kommando ELF/.o utmatningsposition; openjdk-build는 전용 version_System 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parameter_argument = parser_48ee4b1b.parse_args(argument)
    if parameter_argument.target == 'openjdk-build':
        if len(parameter_argument.sources) != 1 or not parameter_argument.java_home or parameter_argument.entry or parameter_argument.export or parameter_argument.classpath or parameter_argument.bundle_runtime:
            raise kompileringsfel('openjdk-build: OpenJDK källa_träd 디렉터리 하나와 --java-home 부트 JDK, -o version_System 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argument.sources[0], parameter_argument.output, parameter_argument.java_home, parameter_argument.jobs, parameter_argument.openjdk_target,
                  parameter_argument.sysroot, None if parameter_argument.cc == 'cc' else parameter_argument.cc, parameter_argument.cxx, parameter_argument.configure_arg)
        except BuildError as fel:
            raise kompileringsfel(str(fel))
        return
    if not parameter_argument.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parameter_argument.cxx or parameter_argument.openjdk_target or parameter_argument.sysroot or parameter_argument.configure_arg or parameter_argument.jobs != 2:
        raise kompileringsfel('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build mål 전용')
    if parameter_argument.target == 'openjdk':
        sys.modules.setdefault('kompilerare', sys.modules[__name__])
        from körbar_fil_fil import Skapa_post
        Skapa_post(parameter_argument)
        return
    if parameter_argument.classpath or parameter_argument.java_home or parameter_argument.bundle_runtime or parameter_argument.cc != 'cc':
        raise kompileringsfel('classpath/java-home/bundle-runtime/cc 옵션은 openjdk mål 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argument.target, '--entry', parameter_argument.entry, '-o', parameter_argument.output]
    for Tilldela_värde in parameter_argument.export: 자바명령.extend(['--export', Tilldela_värde])
    subprocess.run(자바명령+parameter_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        köra_kommando()
    except (kompileringsfel, OSError, ValueError, subprocess.CalledProcessError) as fel:
        print('kompilera_källa fel: ' + str(fel), file=sys.stderr)
        sys.exit(1)
