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


class kompilēšanas_kļūda(Exception):
    pass


class 자료읽기:
    def __init__(자신, dati):
        자신.dati = dati
        자신.Novietojums = 0

    def Lasīt(자신, 길이):
        if 길이 < 0 or 자신.Novietojums + 길이 > len(자신.dati):
            raise kompilēšanas_kļūda('잘린 klase_VALUE 또는 Komanda dati')
        mērs = 자신.dati[자신.Novietojums:자신.Novietojums + 길이]
        자신.Novietojums += 길이
        return mērs

    def numurs(자신, formāts_VALUE):
        return struct.unpack('>' + formāts_VALUE, 자신.Lasīt(struct.calcsize('>' + formāts_VALUE)))[0]


def 수정유티에프해독(dati):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    virkne_VALUE = dati.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return virkne_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klase_VALUE:
    def __init__(자신, CEĻŠ):
        자신.CEĻŠ = CEĻŠ
        Lasītājs_VALUE = 자료읽기(CEĻŠ.read_bytes())
        if Lasītājs_VALUE.numurs('I') != 0xcafebabe:
            raise kompilēšanas_kļūda('Java klase_VALUE 표식이 아님')
        Lasītājs_VALUE.Lasīt(4)
        krājums_COUNT = Lasītājs_VALUE.numurs('H')
        자신.konstante_VALUE = [None] * krājums_COUNT
        INDEX = 1
        while INDEX < krājums_COUNT:
            종류 = Lasītājs_VALUE.numurs('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Lasītājs_VALUE.Lasīt(Lasītājs_VALUE.numurs('H')))
            elif 종류 == 3:
                VALUE = Lasītājs_VALUE.numurs('i')
            elif 종류 == 4:
                VALUE = Lasītājs_VALUE.Lasīt(4)
            elif 종류 in (5, 6):
                VALUE = Lasītājs_VALUE.Lasīt(8)
            elif 종류 in (7, 8, 16):
                VALUE = Lasītājs_VALUE.numurs('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Lasītājs_VALUE.numurs('H'), Lasītājs_VALUE.numurs('H'))
            elif 종류 == 15:
                VALUE = (Lasītājs_VALUE.numurs('B'), Lasītājs_VALUE.numurs('H'))
            else:
                raise kompilēšanas_kļūda('지원하지 않는 konstante_VALUE 종류: {}'.format(종류))
            자신.konstante_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.piekļūt_ievade = Lasītājs_VALUE.numurs('H')
        자신.Nosaukums = 자신.klases_nosaukums(Lasītājs_VALUE.numurs('H'))
        vecākobjekts_VALUE = Lasītājs_VALUE.numurs('H')
        if 자신.klases_nosaukums(vecākobjekts_VALUE) != 'java/lang/Object' or Lasītājs_VALUE.numurs('H') != 0:
            raise kompilēšanas_kļūda(자신.Nosaukums + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.lauka_vērtība = 자신.멤버읽기(Lasītājs_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Lasītājs_VALUE)
        자신.속성읽기(Lasītājs_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstante_VALUE[INDEX][0] != 1:
            raise kompilēšanas_kļūda('virkne_VALUE konstante_VALUE formāts_VALUE Kļūda')
        return 자신.konstante_VALUE[INDEX][1]

    def klases_nosaukums(자신, INDEX):
        return 자신.문자(자신.konstante_VALUE[INDEX][1])

    def Uzziņas(자신, INDEX):
        īpašnieks_VALUE, nosaukums_formāts = 자신.konstante_VALUE[INDEX][1]
        Nosaukums, formāts_VALUE = 자신.konstante_VALUE[nosaukums_formāts][1]
        return 자신.klases_nosaukums(īpašnieks_VALUE), 자신.문자(Nosaukums), 자신.문자(formāts_VALUE)

    def 속성읽기(자신, Lasītājs_VALUE):
        mērs = {}
        for _ in range(Lasītājs_VALUE.numurs('H')):
            Nosaukums = 자신.문자(Lasītājs_VALUE.numurs('H'))
            mērs[Nosaukums] = Lasītājs_VALUE.Lasīt(Lasītājs_VALUE.numurs('I'))
        return mērs

    def 멤버읽기(자신, Lasītājs_VALUE):
        mērs = []
        for _ in range(Lasītājs_VALUE.numurs('H')):
            piekļūt_ievade = Lasītājs_VALUE.numurs('H')
            Nosaukums = 자신.문자(Lasītājs_VALUE.numurs('H'))
            formāts_VALUE = 자신.문자(Lasītājs_VALUE.numurs('H'))
            mērs.append((piekļūt_ievade, Nosaukums, formāts_VALUE, 자신.속성읽기(Lasītājs_VALUE)))
        return mērs


def 형식읽기(virkne_VALUE):
    mērs = []
    Novietojums = 0
    while Novietojums < len(virkne_VALUE):
        for formāts_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if virkne_VALUE.startswith(formāts_VALUE, Novietojums):
                mērs.append(formāts_VALUE)
                Novietojums += len(formāts_VALUE)
                break
        else:
            raise kompilēšanas_kļūda('지원하지 않는 datu_tips: ' + virkne_VALUE)
    return mērs


def 함수형식(서술):
    Parametri, atdot_mērs = 서술[1:].split(')')
    Parametri = 형식읽기(Parametri)
    atdot_TYPE = 형식읽기(atdot_mērs)
    if 'V' in Parametri or len(atdot_TYPE) != 1:
        raise kompilēšanas_kļūda('FUNCTION_VALUE 서술 formāts_VALUE Kļūda: ' + 서술)
    return Parametri, atdot_mērs


def simbols(종류, *부분):
    AVOTS = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(AVOTS).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def Izpildīt_komanda(Parametri=None):
    parsētājs_48ee4b1b = argparse.ArgumentParser(description='savs Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK avots_koks būvējums_sistēma')
    parsētājs_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parsētājs_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Pievienot_ievade JAR/klase_VALUE 디렉터리')
    parsētājs_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 būvējums_sistēma JDK 또는 openjdk-build의 부트 JDK CEĻŠ')
    parsētājs_48ee4b1b.add_argument('--bundle-runtime', help='Izpildīt_komanda 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parsētājs_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK programma_palaidējs/avots_koks 빌드의 C kompilators')
    parsētājs_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompilators')
    parsētājs_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 būvējums_sistēma 작업 numurs')
    parsētājs_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 būvējums_sistēma mērķis (예: aarch64-linux-gnu)')
    parsētājs_48ee4b1b.add_argument('--sysroot', help='교차 būvējums_sistēma 대상의 libc/헤더/bibliotēka 루트')
    parsētājs_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formāts_VALUE')
    parsētājs_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=klase_VALUE.FUNCTION_VALUE (savs operands_kopa ABI)')
    parsētājs_48ee4b1b.add_argument('--entry', help='예: 계산.Palaist (openjdk-build 이외 대상에서 필수)')
    parsētājs_48ee4b1b.add_argument('-o', '--output', required=True, help='Izpildīt_komanda ELF/.o Izvade; openjdk-build는 전용 būvējums_sistēma 디렉터리')
    parsētājs_48ee4b1b.add_argument('sources', nargs='+')
    parametrs_arg = parsētājs_48ee4b1b.parse_args(Parametri)
    if parametrs_arg.target == 'openjdk-build':
        if len(parametrs_arg.sources) != 1 or not parametrs_arg.java_home or parametrs_arg.entry or parametrs_arg.export or parametrs_arg.classpath or parametrs_arg.bundle_runtime:
            raise kompilēšanas_kļūda('openjdk-build: OpenJDK avots_koks 디렉터리 하나와 --java-home 부트 JDK, -o būvējums_sistēma 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametrs_arg.sources[0], parametrs_arg.output, parametrs_arg.java_home, parametrs_arg.jobs, parametrs_arg.openjdk_target,
                  parametrs_arg.sysroot, None if parametrs_arg.cc == 'cc' else parametrs_arg.cc, parametrs_arg.cxx, parametrs_arg.configure_arg)
        except BuildError as Kļūda:
            raise kompilēšanas_kļūda(str(Kļūda))
        return
    if not parametrs_arg.entry:
        parsētājs_48ee4b1b.error('--entry is required for this target')
    if parametrs_arg.cxx or parametrs_arg.openjdk_target or parametrs_arg.sysroot or parametrs_arg.configure_arg or parametrs_arg.jobs != 2:
        raise kompilēšanas_kļūda('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build mērķis 전용')
    if parametrs_arg.target == 'openjdk':
        sys.modules.setdefault('kompilators', sys.modules[__name__])
        from izpildāms_fails import atvērt_ievade
        atvērt_ievade(parametrs_arg)
        return
    if parametrs_arg.classpath or parametrs_arg.java_home or parametrs_arg.bundle_runtime or parametrs_arg.cc != 'cc':
        raise kompilēšanas_kļūda('classpath/java-home/bundle-runtime/cc 옵션은 openjdk mērķis 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametrs_arg.target, '--entry', parametrs_arg.entry, '-o', parametrs_arg.output]
    for nodot_VALUE in parametrs_arg.export: 자바명령.extend(['--export', nodot_VALUE])
    subprocess.run(자바명령+parametrs_arg.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Izpildīt_komanda()
    except (kompilēšanas_kļūda, OSError, ValueError, subprocess.CalledProcessError) as Kļūda:
        print('kompilēt_avots Kļūda: ' + str(Kļūda), file=sys.stderr)
        sys.exit(1)
