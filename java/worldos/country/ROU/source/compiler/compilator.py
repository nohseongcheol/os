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


class eroare_la_compilare(Exception):
    pass


class 자료읽기:
    def __init__(자신, date):
        자신.date = date
        자신.Poziție = 0

    def Citire(자신, lungime_VALUE):
        if lungime_VALUE < 0 or 자신.Poziție + lungime_VALUE > len(자신.date):
            raise eroare_la_compilare('잘린 Clasă_VALUE 또는 Comandă date')
        KR = 자신.date[자신.Poziție:자신.Poziție + lungime_VALUE]
        자신.Poziție += lungime_VALUE
        return KR

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.Citire(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(date):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    șir_VALUE = date.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return șir_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Clasă_VALUE:
    def __init__(자신, Cale):
        자신.Cale = Cale
        Reader_VALUE = 자료읽기(Cale.read_bytes())
        if Reader_VALUE.수('I') != 0xcafebabe:
            raise eroare_la_compilare('Java Clasă_VALUE 표식이 아님')
        Reader_VALUE.Citire(4)
        element_COUNT = Reader_VALUE.수('H')
        자신.constantă_VALUE = [None] * element_COUNT
        INDEX = 1
        while INDEX < element_COUNT:
            종류 = Reader_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Reader_VALUE.Citire(Reader_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Reader_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Reader_VALUE.Citire(4)
            elif 종류 in (5, 6):
                VALUE = Reader_VALUE.Citire(8)
            elif 종류 in (7, 8, 16):
                VALUE = Reader_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Reader_VALUE.수('H'), Reader_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Reader_VALUE.수('B'), Reader_VALUE.수('H'))
            else:
                raise eroare_la_compilare('지원하지 않는 constantă_VALUE 종류: {}'.format(종류))
            자신.constantă_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.acces_intrare = Reader_VALUE.수('H')
        자신.Nume = 자신.nume_de_clasă(Reader_VALUE.수('H'))
        părinte_VALUE = Reader_VALUE.수('H')
        if 자신.nume_de_clasă(părinte_VALUE) != 'java/lang/Object' or Reader_VALUE.수('H') != 0:
            raise eroare_la_compilare(자신.Nume + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.valoare_câmp = 자신.멤버읽기(Reader_VALUE)
        자신.funcție_VALUE = 자신.멤버읽기(Reader_VALUE)
        자신.속성읽기(Reader_VALUE)

    def 문자(자신, INDEX):
        if 자신.constantă_VALUE[INDEX][0] != 1:
            raise eroare_la_compilare('șir_VALUE constantă_VALUE format_VALUE eroare')
        return 자신.constantă_VALUE[INDEX][1]

    def nume_de_clasă(자신, INDEX):
        return 자신.문자(자신.constantă_VALUE[INDEX][1])

    def referință(자신, INDEX):
        proprietar_VALUE, nume_format = 자신.constantă_VALUE[INDEX][1]
        Nume, format_VALUE = 자신.constantă_VALUE[nume_format][1]
        return 자신.nume_de_clasă(proprietar_VALUE), 자신.문자(Nume), 자신.문자(format_VALUE)

    def 속성읽기(자신, Reader_VALUE):
        KR = {}
        for _ in range(Reader_VALUE.수('H')):
            Nume = 자신.문자(Reader_VALUE.수('H'))
            KR[Nume] = Reader_VALUE.Citire(Reader_VALUE.수('I'))
        return KR

    def 멤버읽기(자신, Reader_VALUE):
        KR = []
        for _ in range(Reader_VALUE.수('H')):
            acces_intrare = Reader_VALUE.수('H')
            Nume = 자신.문자(Reader_VALUE.수('H'))
            format_VALUE = 자신.문자(Reader_VALUE.수('H'))
            KR.append((acces_intrare, Nume, format_VALUE, 자신.속성읽기(Reader_VALUE)))
        return KR


def 형식읽기(șir_VALUE):
    KR = []
    Poziție = 0
    while Poziție < len(șir_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if șir_VALUE.startswith(format_VALUE, Poziție):
                KR.append(format_VALUE)
                Poziție += len(format_VALUE)
                break
        else:
            raise eroare_la_compilare('지원하지 않는 tip_de_date: ' + șir_VALUE)
    return KR


def 함수형식(서술):
    Argumente, restitui_KR = 서술[1:].split(')')
    Argumente = 형식읽기(Argumente)
    restitui_Tip = 형식읽기(restitui_KR)
    if 'V' in Argumente or len(restitui_Tip) != 1:
        raise eroare_la_compilare('funcție_VALUE 서술 format_VALUE eroare: ' + 서술)
    return Argumente, restitui_KR


def simbol(종류, *부분):
    SURSĂ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(SURSĂ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 funcție_VALUE 서술에 대해서만 허용한다.
def executa_comandă(Argumente=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='propriu Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK sursă_arborescență generare_sistem')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 adăuga_intrare JAR/Clasă_VALUE 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 generare_sistem JDK 또는 openjdk-build의 부트 JDK Cale')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='executa_comandă 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK program_ecrane_de_lansare/sursă_arborescență 빌드의 C compilator')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ compilator')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 generare_sistem 작업 수')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 generare_sistem țintă (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 generare_sistem 대상의 libc/헤더/bibliotecă 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Clasă_VALUE.funcție_VALUE (propriu operand_Teanc ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.Pornește (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='executa_comandă ELF/.o Rezultat; openjdk-build는 전용 generare_sistem 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parametru_argument = parser_48ee4b1b.parse_args(Argumente)
    if parametru_argument.target == 'openjdk-build':
        if len(parametru_argument.sources) != 1 or not parametru_argument.java_home or parametru_argument.entry or parametru_argument.export or parametru_argument.classpath or parametru_argument.bundle_runtime:
            raise eroare_la_compilare('openjdk-build: OpenJDK sursă_arborescență 디렉터리 하나와 --java-home 부트 JDK, -o generare_sistem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametru_argument.sources[0], parametru_argument.output, parametru_argument.java_home, parametru_argument.jobs, parametru_argument.openjdk_target,
                  parametru_argument.sysroot, None if parametru_argument.cc == 'cc' else parametru_argument.cc, parametru_argument.cxx, parametru_argument.configure_arg)
        except BuildError as eroare:
            raise eroare_la_compilare(str(eroare))
        return
    if not parametru_argument.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parametru_argument.cxx or parametru_argument.openjdk_target or parametru_argument.sysroot or parametru_argument.configure_arg or parametru_argument.jobs != 2:
        raise eroare_la_compilare('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build țintă 전용')
    if parametru_argument.target == 'openjdk':
        sys.modules.setdefault('compilator', sys.modules[__name__])
        from 실행파일 import crea_intrare
        crea_intrare(parametru_argument)
        return
    if parametru_argument.classpath or parametru_argument.java_home or parametru_argument.bundle_runtime or parametru_argument.cc != 'cc':
        raise eroare_la_compilare('classpath/java-home/bundle-runtime/cc 옵션은 openjdk țintă 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametru_argument.target, '--entry', parametru_argument.entry, '-o', parametru_argument.output]
    for atribui_VALUE in parametru_argument.export: 자바명령.extend(['--export', atribui_VALUE])
    subprocess.run(자바명령+parametru_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        executa_comandă()
    except (eroare_la_compilare, OSError, ValueError, subprocess.CalledProcessError) as eroare:
        print('compilare_sursă eroare: ' + str(eroare), file=sys.stderr)
        sys.exit(1)
