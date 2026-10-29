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


class compilatiefout(Exception):
    pass


class 자료읽기:
    def __init__(자신, gegevens):
        자신.gegevens = gegevens
        자신.positie = 0

    def Lezen(자신, tijdsduur_WAARDE):
        if tijdsduur_WAARDE < 0 or 자신.positie + tijdsduur_WAARDE > len(자신.gegevens):
            raise compilatiefout('잘린 les_WAARDE 또는 opdracht gegevens')
        resultaat = 자신.gegevens[자신.positie:자신.positie + tijdsduur_WAARDE]
        자신.positie += tijdsduur_WAARDE
        return resultaat

    def nummer(자신, opmaak_WAARDE):
        return struct.unpack('>' + opmaak_WAARDE, 자신.Lezen(struct.calcsize('>' + opmaak_WAARDE)))[0]


def 수정유티에프해독(gegevens):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    tekenreeks_WAARDE = gegevens.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return tekenreeks_WAARDE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class les_WAARDE:
    def __init__(자신, pad):
        자신.pad = pad
        Lezer_WAARDE = 자료읽기(pad.read_bytes())
        if Lezer_WAARDE.nummer('I') != 0xcafebabe:
            raise compilatiefout('Java les_WAARDE 표식이 아님')
        Lezer_WAARDE.Lezen(4)
        item_AANTAL = Lezer_WAARDE.nummer('H')
        자신.constante_WAARDE = [None] * item_AANTAL
        INDEX = 1
        while INDEX < item_AANTAL:
            soort_WAARDE = Lezer_WAARDE.nummer('B')
            if soort_WAARDE == 1:
                WAARDE = 수정유티에프해독(Lezer_WAARDE.Lezen(Lezer_WAARDE.nummer('H')))
            elif soort_WAARDE == 3:
                WAARDE = Lezer_WAARDE.nummer('i')
            elif soort_WAARDE == 4:
                WAARDE = Lezer_WAARDE.Lezen(4)
            elif soort_WAARDE in (5, 6):
                WAARDE = Lezer_WAARDE.Lezen(8)
            elif soort_WAARDE in (7, 8, 16):
                WAARDE = Lezer_WAARDE.nummer('H')
            elif soort_WAARDE in (9, 10, 11, 12, 18):
                WAARDE = (Lezer_WAARDE.nummer('H'), Lezer_WAARDE.nummer('H'))
            elif soort_WAARDE == 15:
                WAARDE = (Lezer_WAARDE.nummer('B'), Lezer_WAARDE.nummer('H'))
            else:
                raise compilatiefout('지원하지 않는 constante_WAARDE soort_WAARDE: {}'.format(soort_WAARDE))
            자신.constante_WAARDE[INDEX] = (soort_WAARDE, WAARDE)
            INDEX += 2 if soort_WAARDE in (5, 6) else 1
        자신.toegang_invoer = Lezer_WAARDE.nummer('H')
        자신.Naam = 자신.klassenaam(Lezer_WAARDE.nummer('H'))
        bovenliggend_WAARDE = Lezer_WAARDE.nummer('H')
        if 자신.klassenaam(bovenliggend_WAARDE) != 'java/lang/Object' or Lezer_WAARDE.nummer('H') != 0:
            raise compilatiefout(자신.Naam + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.veldwaarde = 자신.멤버읽기(Lezer_WAARDE)
        자신.FUNCTIE_WAARDE = 자신.멤버읽기(Lezer_WAARDE)
        자신.속성읽기(Lezer_WAARDE)

    def 문자(자신, INDEX):
        if 자신.constante_WAARDE[INDEX][0] != 1:
            raise compilatiefout('tekenreeks_WAARDE constante_WAARDE opmaak_WAARDE fout')
        return 자신.constante_WAARDE[INDEX][1]

    def klassenaam(자신, INDEX):
        return 자신.문자(자신.constante_WAARDE[INDEX][1])

    def verwijzen(자신, INDEX):
        eigenaar_WAARDE, naam_opmaak = 자신.constante_WAARDE[INDEX][1]
        Naam, opmaak_WAARDE = 자신.constante_WAARDE[naam_opmaak][1]
        return 자신.klassenaam(eigenaar_WAARDE), 자신.문자(Naam), 자신.문자(opmaak_WAARDE)

    def 속성읽기(자신, Lezer_WAARDE):
        resultaat = {}
        for _ in range(Lezer_WAARDE.nummer('H')):
            Naam = 자신.문자(Lezer_WAARDE.nummer('H'))
            resultaat[Naam] = Lezer_WAARDE.Lezen(Lezer_WAARDE.nummer('I'))
        return resultaat

    def 멤버읽기(자신, Lezer_WAARDE):
        resultaat = []
        for _ in range(Lezer_WAARDE.nummer('H')):
            toegang_invoer = Lezer_WAARDE.nummer('H')
            Naam = 자신.문자(Lezer_WAARDE.nummer('H'))
            opmaak_WAARDE = 자신.문자(Lezer_WAARDE.nummer('H'))
            resultaat.append((toegang_invoer, Naam, opmaak_WAARDE, 자신.속성읽기(Lezer_WAARDE)))
        return resultaat


def 형식읽기(tekenreeks_WAARDE):
    resultaat = []
    positie = 0
    while positie < len(tekenreeks_WAARDE):
        for opmaak_WAARDE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if tekenreeks_WAARDE.startswith(opmaak_WAARDE, positie):
                resultaat.append(opmaak_WAARDE)
                positie += len(opmaak_WAARDE)
                break
        else:
            raise compilatiefout('지원하지 않는 gegevenstype: ' + tekenreeks_WAARDE)
    return resultaat


def 함수형식(서술):
    argumenten, Retour_HR = 서술[1:].split(')')
    argumenten = 형식읽기(argumenten)
    Retour_TYPE = 형식읽기(Retour_HR)
    if 'V' in argumenten or len(Retour_TYPE) != 1:
        raise compilatiefout('FUNCTIE_WAARDE 서술 opmaak_WAARDE fout: ' + 서술)
    return argumenten, Retour_HR


def symbool(soort_WAARDE, *부분):
    broncode = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(soort_WAARDE, hashlib.sha256(broncode).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTIE_WAARDE 서술에 대해서만 허용한다.
def Uitvoeren_opdracht(argumenten=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='Eigen Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK bron_structuur bouwen')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 toevoegen_invoer JAR/les_WAARDE 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 bouwen JDK 또는 openjdk-build의 부트 JDK pad')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='Uitvoeren_opdracht 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK app_app_lade/bron_structuur 빌드의 C compiler')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ compiler')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 bouwen 작업 nummer')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 bouwen doel (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 bouwen 대상의 libc/헤더/bibliotheek 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 opmaak_WAARDE')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=les_WAARDE.FUNCTIE_WAARDE (Eigen operand_stack ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.starten (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='Uitvoeren_opdracht ELF/.o tekstuitvoer; openjdk-build는 전용 bouwen 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parameter_argument = parser_48ee4b1b.parse_args(argumenten)
    if parameter_argument.target == 'openjdk-build':
        if len(parameter_argument.sources) != 1 or not parameter_argument.java_home or parameter_argument.entry or parameter_argument.export or parameter_argument.classpath or parameter_argument.bundle_runtime:
            raise compilatiefout('openjdk-build: OpenJDK bron_structuur 디렉터리 하나와 --java-home 부트 JDK, -o bouwen 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argument.sources[0], parameter_argument.output, parameter_argument.java_home, parameter_argument.jobs, parameter_argument.openjdk_target,
                  parameter_argument.sysroot, None if parameter_argument.cc == 'cc' else parameter_argument.cc, parameter_argument.cxx, parameter_argument.configure_arg)
        except BuildError as fout:
            raise compilatiefout(str(fout))
        return
    if not parameter_argument.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parameter_argument.cxx or parameter_argument.openjdk_target or parameter_argument.sysroot or parameter_argument.configure_arg or parameter_argument.jobs != 2:
        raise compilatiefout('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build doel 전용')
    if parameter_argument.target == 'openjdk':
        sys.modules.setdefault('compiler', sys.modules[__name__])
        from uitvoerbaar_bestand import maken_invoer
        maken_invoer(parameter_argument)
        return
    if parameter_argument.classpath or parameter_argument.java_home or parameter_argument.bundle_runtime or parameter_argument.cc != 'cc':
        raise compilatiefout('classpath/java-home/bundle-runtime/cc 옵션은 openjdk doel 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argument.target, '--entry', parameter_argument.entry, '-o', parameter_argument.output]
    for Toewijzen_WAARDE in parameter_argument.export: 자바명령.extend(['--export', Toewijzen_WAARDE])
    subprocess.run(자바명령+parameter_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Uitvoeren_opdracht()
    except (compilatiefout, OSError, ValueError, subprocess.CalledProcessError) as fout:
        print('compileren_bron fout: ' + str(fout), file=sys.stderr)
        sys.exit(1)
