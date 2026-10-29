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


class chyba_pri_kompilácii(Exception):
    pass


class 자료읽기:
    def __init__(자신, údaje):
        자신.údaje = údaje
        자신.Pozícia = 0

    def Čítanie(자신, dĺžka_VALUE):
        if dĺžka_VALUE < 0 or 자신.Pozícia + dĺžka_VALUE > len(자신.údaje):
            raise chyba_pri_kompilácii('잘린 lekcia_VALUE 또는 Príkaz údaje')
        KR = 자신.údaje[자신.Pozícia:자신.Pozícia + dĺžka_VALUE]
        자신.Pozícia += dĺžka_VALUE
        return KR

    def 수(자신, formát_VALUE):
        return struct.unpack('>' + formát_VALUE, 자신.Čítanie(struct.calcsize('>' + formát_VALUE)))[0]


def 수정유티에프해독(údaje):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    reťazec_VALUE = údaje.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return reťazec_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class lekcia_VALUE:
    def __init__(자신, Cesta):
        자신.Cesta = Cesta
        Čítačka_VALUE = 자료읽기(Cesta.read_bytes())
        if Čítačka_VALUE.수('I') != 0xcafebabe:
            raise chyba_pri_kompilácii('Java lekcia_VALUE 표식이 아님')
        Čítačka_VALUE.Čítanie(4)
        položka_COUNT = Čítačka_VALUE.수('H')
        자신.konštanta_VALUE = [None] * položka_COUNT
        INDEX = 1
        while INDEX < položka_COUNT:
            종류 = Čítačka_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Čítačka_VALUE.Čítanie(Čítačka_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Čítačka_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Čítačka_VALUE.Čítanie(4)
            elif 종류 in (5, 6):
                VALUE = Čítačka_VALUE.Čítanie(8)
            elif 종류 in (7, 8, 16):
                VALUE = Čítačka_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Čítačka_VALUE.수('H'), Čítačka_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Čítačka_VALUE.수('B'), Čítačka_VALUE.수('H'))
            else:
                raise chyba_pri_kompilácii('지원하지 않는 konštanta_VALUE 종류: {}'.format(종류))
            자신.konštanta_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.prístup_položka = Čítačka_VALUE.수('H')
        자신.Názov = 자신.názov_triedy(Čítačka_VALUE.수('H'))
        nadradený_VALUE = Čítačka_VALUE.수('H')
        if 자신.názov_triedy(nadradený_VALUE) != 'java/lang/Object' or Čítačka_VALUE.수('H') != 0:
            raise chyba_pri_kompilácii(자신.Názov + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.hodnota_poľa = 자신.멤버읽기(Čítačka_VALUE)
        자신.funkcia_VALUE = 자신.멤버읽기(Čítačka_VALUE)
        자신.속성읽기(Čítačka_VALUE)

    def 문자(자신, INDEX):
        if 자신.konštanta_VALUE[INDEX][0] != 1:
            raise chyba_pri_kompilácii('reťazec_VALUE konštanta_VALUE formát_VALUE chyba')
        return 자신.konštanta_VALUE[INDEX][1]

    def názov_triedy(자신, INDEX):
        return 자신.문자(자신.konštanta_VALUE[INDEX][1])

    def zdroj(자신, INDEX):
        vlastník_VALUE, názov_formát = 자신.konštanta_VALUE[INDEX][1]
        Názov, formát_VALUE = 자신.konštanta_VALUE[názov_formát][1]
        return 자신.názov_triedy(vlastník_VALUE), 자신.문자(Názov), 자신.문자(formát_VALUE)

    def 속성읽기(자신, Čítačka_VALUE):
        KR = {}
        for _ in range(Čítačka_VALUE.수('H')):
            Názov = 자신.문자(Čítačka_VALUE.수('H'))
            KR[Názov] = Čítačka_VALUE.Čítanie(Čítačka_VALUE.수('I'))
        return KR

    def 멤버읽기(자신, Čítačka_VALUE):
        KR = []
        for _ in range(Čítačka_VALUE.수('H')):
            prístup_položka = Čítačka_VALUE.수('H')
            Názov = 자신.문자(Čítačka_VALUE.수('H'))
            formát_VALUE = 자신.문자(Čítačka_VALUE.수('H'))
            KR.append((prístup_položka, Názov, formát_VALUE, 자신.속성읽기(Čítačka_VALUE)))
        return KR


def 형식읽기(reťazec_VALUE):
    KR = []
    Pozícia = 0
    while Pozícia < len(reťazec_VALUE):
        for formát_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if reťazec_VALUE.startswith(formát_VALUE, Pozícia):
                KR.append(formát_VALUE)
                Pozícia += len(formát_VALUE)
                break
        else:
            raise chyba_pri_kompilácii('지원하지 않는 typ_údajov: ' + reťazec_VALUE)
    return KR


def 함수형식(서술):
    Argumenty, vrátiť_KR = 서술[1:].split(')')
    Argumenty = 형식읽기(Argumenty)
    vrátiť_Typ = 형식읽기(vrátiť_KR)
    if 'V' in Argumenty or len(vrátiť_Typ) != 1:
        raise chyba_pri_kompilácii('funkcia_VALUE 서술 formát_VALUE chyba: ' + 서술)
    return Argumenty, vrátiť_KR


def symbol(종류, *부분):
    ZDROJ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ZDROJ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 funkcia_VALUE 서술에 대해서만 허용한다.
def Vykonať_príkaz(Argumenty=None):
    analyzátor_48ee4b1b = argparse.ArgumentParser(description='vlastné Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK zdroj_strom zostava_systém')
    analyzátor_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analyzátor_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Pripojiť_položka JAR/lekcia_VALUE 디렉터리')
    analyzátor_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 zostava_systém JDK 또는 openjdk-build의 부트 JDK Cesta')
    analyzátor_48ee4b1b.add_argument('--bundle-runtime', help='Vykonať_príkaz 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analyzátor_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK program_spúšťač/zdroj_strom 빌드의 C kompilátor')
    analyzátor_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompilátor')
    analyzátor_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 zostava_systém 작업 수')
    analyzátor_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 zostava_systém cieľová_hodnota (예: aarch64-linux-gnu)')
    analyzátor_48ee4b1b.add_argument('--sysroot', help='교차 zostava_systém 대상의 libc/헤더/knižnica 루트')
    analyzátor_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formát_VALUE')
    analyzátor_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=lekcia_VALUE.funkcia_VALUE (vlastné operand_Vrstvy ABI)')
    analyzátor_48ee4b1b.add_argument('--entry', help='예: 계산.Spustiť_2 (openjdk-build 이외 대상에서 필수)')
    analyzátor_48ee4b1b.add_argument('-o', '--output', required=True, help='Vykonať_príkaz ELF/.o Výstup; openjdk-build는 전용 zostava_systém 디렉터리')
    analyzátor_48ee4b1b.add_argument('sources', nargs='+')
    parameter_argument = analyzátor_48ee4b1b.parse_args(Argumenty)
    if parameter_argument.target == 'openjdk-build':
        if len(parameter_argument.sources) != 1 or not parameter_argument.java_home or parameter_argument.entry or parameter_argument.export or parameter_argument.classpath or parameter_argument.bundle_runtime:
            raise chyba_pri_kompilácii('openjdk-build: OpenJDK zdroj_strom 디렉터리 하나와 --java-home 부트 JDK, -o zostava_systém 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argument.sources[0], parameter_argument.output, parameter_argument.java_home, parameter_argument.jobs, parameter_argument.openjdk_target,
                  parameter_argument.sysroot, None if parameter_argument.cc == 'cc' else parameter_argument.cc, parameter_argument.cxx, parameter_argument.configure_arg)
        except BuildError as chyba:
            raise chyba_pri_kompilácii(str(chyba))
        return
    if not parameter_argument.entry:
        analyzátor_48ee4b1b.error('--entry is required for this target')
    if parameter_argument.cxx or parameter_argument.openjdk_target or parameter_argument.sysroot or parameter_argument.configure_arg or parameter_argument.jobs != 2:
        raise chyba_pri_kompilácii('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build cieľová_hodnota 전용')
    if parameter_argument.target == 'openjdk':
        sys.modules.setdefault('kompilátor', sys.modules[__name__])
        from spustiteľný_súbor import Create_položka
        Create_položka(parameter_argument)
        return
    if parameter_argument.classpath or parameter_argument.java_home or parameter_argument.bundle_runtime or parameter_argument.cc != 'cc':
        raise chyba_pri_kompilácii('classpath/java-home/bundle-runtime/cc 옵션은 openjdk cieľová_hodnota 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argument.target, '--entry', parameter_argument.entry, '-o', parameter_argument.output]
    for Priradiť_VALUE in parameter_argument.export: 자바명령.extend(['--export', Priradiť_VALUE])
    subprocess.run(자바명령+parameter_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Vykonať_príkaz()
    except (chyba_pri_kompilácii, OSError, ValueError, subprocess.CalledProcessError) as chyba:
        print('kompilovať_zdroj chyba: ' + str(chyba), file=sys.stderr)
        sys.exit(1)
