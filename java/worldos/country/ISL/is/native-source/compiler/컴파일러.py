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
    def __init__(자신, gögn):
        자신.gögn = gögn
        자신.Staðsetning = 0

    def Lestur(자신, lengd_VALUE):
        if lengd_VALUE < 0 or 자신.Staðsetning + lengd_VALUE > len(자신.gögn):
            raise 컴파일오류('잘린 klasi_VALUE 또는 Skipun gögn')
        NIÐURSTAÐA = 자신.gögn[자신.Staðsetning:자신.Staðsetning + lengd_VALUE]
        자신.Staðsetning += lengd_VALUE
        return NIÐURSTAÐA

    def númer(자신, snið_VALUE):
        return struct.unpack('>' + snið_VALUE, 자신.Lestur(struct.calcsize('>' + snið_VALUE)))[0]


def 수정유티에프해독(gögn):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    strengur_VALUE = gögn.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return strengur_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klasi_VALUE:
    def __init__(자신, SLÓÐ):
        자신.SLÓÐ = SLÓÐ
        Lesari_VALUE = 자료읽기(SLÓÐ.read_bytes())
        if Lesari_VALUE.númer('I') != 0xcafebabe:
            raise 컴파일오류('Java klasi_VALUE 표식이 아님')
        Lesari_VALUE.Lestur(4)
        vara_COUNT = Lesari_VALUE.númer('H')
        자신.fasti_VALUE = [None] * vara_COUNT
        INDEX = 1
        while INDEX < vara_COUNT:
            종류 = Lesari_VALUE.númer('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Lesari_VALUE.Lestur(Lesari_VALUE.númer('H')))
            elif 종류 == 3:
                VALUE = Lesari_VALUE.númer('i')
            elif 종류 == 4:
                VALUE = Lesari_VALUE.Lestur(4)
            elif 종류 in (5, 6):
                VALUE = Lesari_VALUE.Lestur(8)
            elif 종류 in (7, 8, 16):
                VALUE = Lesari_VALUE.númer('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Lesari_VALUE.númer('H'), Lesari_VALUE.númer('H'))
            elif 종류 == 15:
                VALUE = (Lesari_VALUE.númer('B'), Lesari_VALUE.númer('H'))
            else:
                raise 컴파일오류('지원하지 않는 fasti_VALUE 종류: {}'.format(종류))
            자신.fasti_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.aðgangur_færsla = Lesari_VALUE.númer('H')
        자신.Heiti = 자신.klasi_heiti(Lesari_VALUE.númer('H'))
        yfireining_VALUE = Lesari_VALUE.númer('H')
        if 자신.klasi_heiti(yfireining_VALUE) != 'java/lang/Object' or Lesari_VALUE.númer('H') != 0:
            raise 컴파일오류(자신.Heiti + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.reitur_VALUE = 자신.멤버읽기(Lesari_VALUE)
        자신.fall_VALUE = 자신.멤버읽기(Lesari_VALUE)
        자신.속성읽기(Lesari_VALUE)

    def 문자(자신, INDEX):
        if 자신.fasti_VALUE[INDEX][0] != 1:
            raise 컴파일오류('strengur_VALUE fasti_VALUE snið_VALUE Villa')
        return 자신.fasti_VALUE[INDEX][1]

    def klasi_heiti(자신, INDEX):
        return 자신.문자(자신.fasti_VALUE[INDEX][1])

    def tilvísun(자신, INDEX):
        eigandi_VALUE, heiti_snið = 자신.fasti_VALUE[INDEX][1]
        Heiti, snið_VALUE = 자신.fasti_VALUE[heiti_snið][1]
        return 자신.klasi_heiti(eigandi_VALUE), 자신.문자(Heiti), 자신.문자(snið_VALUE)

    def 속성읽기(자신, Lesari_VALUE):
        NIÐURSTAÐA = {}
        for _ in range(Lesari_VALUE.númer('H')):
            Heiti = 자신.문자(Lesari_VALUE.númer('H'))
            NIÐURSTAÐA[Heiti] = Lesari_VALUE.Lestur(Lesari_VALUE.númer('I'))
        return NIÐURSTAÐA

    def 멤버읽기(자신, Lesari_VALUE):
        NIÐURSTAÐA = []
        for _ in range(Lesari_VALUE.númer('H')):
            aðgangur_færsla = Lesari_VALUE.númer('H')
            Heiti = 자신.문자(Lesari_VALUE.númer('H'))
            snið_VALUE = 자신.문자(Lesari_VALUE.númer('H'))
            NIÐURSTAÐA.append((aðgangur_færsla, Heiti, snið_VALUE, 자신.속성읽기(Lesari_VALUE)))
        return NIÐURSTAÐA


def 형식읽기(strengur_VALUE):
    NIÐURSTAÐA = []
    Staðsetning = 0
    while Staðsetning < len(strengur_VALUE):
        for snið_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if strengur_VALUE.startswith(snið_VALUE, Staðsetning):
                NIÐURSTAÐA.append(snið_VALUE)
                Staðsetning += len(snið_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 gagnagerð: ' + strengur_VALUE)
    return NIÐURSTAÐA


def 함수형식(서술):
    Viðföng, skila_mæld_stærð = 서술[1:].split(')')
    Viðföng = 형식읽기(Viðföng)
    skila_TYPE = 형식읽기(skila_mæld_stærð)
    if 'V' in Viðföng or len(skila_TYPE) != 1:
        raise 컴파일오류('fall_VALUE 서술 snið_VALUE Villa: ' + 서술)
    return Viðföng, skila_mæld_stærð


def tákn(종류, *부분):
    Uppruni = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Uppruni).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 fall_VALUE 서술에 대해서만 허용한다.
def keyra_skipun(Viðföng=None):
    þáttari_48ee4b1b = argparse.ArgumentParser(description='eigin Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK uppruni_tré smíð_kerfi')
    þáttari_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    þáttari_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/klasi_VALUE 디렉터리')
    þáttari_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 smíð_kerfi JDK 또는 openjdk-build의 부트 JDK SLÓÐ')
    þáttari_48ee4b1b.add_argument('--bundle-runtime', help='keyra_skipun 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    þáttari_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK forrit_ræsir/uppruni_tré 빌드의 C 컴파일러')
    þáttari_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    þáttari_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 smíð_kerfi 작업 númer')
    þáttari_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 smíð_kerfi markmið (예: aarch64-linux-gnu)')
    þáttari_48ee4b1b.add_argument('--sysroot', help='교차 smíð_kerfi 대상의 libc/헤더/safn 루트')
    þáttari_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 snið_VALUE')
    þáttari_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=klasi_VALUE.fall_VALUE (eigin 스택 ABI)')
    þáttari_48ee4b1b.add_argument('--entry', help='예: 계산.Keyra_2 (openjdk-build 이외 대상에서 필수)')
    þáttari_48ee4b1b.add_argument('-o', '--output', required=True, help='keyra_skipun ELF/.o úttak; openjdk-build는 전용 smíð_kerfi 디렉터리')
    þáttari_48ee4b1b.add_argument('sources', nargs='+')
    færibreyta_frumbreyta = þáttari_48ee4b1b.parse_args(Viðföng)
    if færibreyta_frumbreyta.target == 'openjdk-build':
        if len(færibreyta_frumbreyta.sources) != 1 or not færibreyta_frumbreyta.java_home or færibreyta_frumbreyta.entry or færibreyta_frumbreyta.export or færibreyta_frumbreyta.classpath or færibreyta_frumbreyta.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK uppruni_tré 디렉터리 하나와 --java-home 부트 JDK, -o smíð_kerfi 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(færibreyta_frumbreyta.sources[0], færibreyta_frumbreyta.output, færibreyta_frumbreyta.java_home, færibreyta_frumbreyta.jobs, færibreyta_frumbreyta.openjdk_target,
                  færibreyta_frumbreyta.sysroot, None if færibreyta_frumbreyta.cc == 'cc' else færibreyta_frumbreyta.cc, færibreyta_frumbreyta.cxx, færibreyta_frumbreyta.configure_arg)
        except BuildError as Villa:
            raise 컴파일오류(str(Villa))
        return
    if not færibreyta_frumbreyta.entry:
        þáttari_48ee4b1b.error('--entry is required for this target')
    if færibreyta_frumbreyta.cxx or færibreyta_frumbreyta.openjdk_target or færibreyta_frumbreyta.sysroot or færibreyta_frumbreyta.configure_arg or færibreyta_frumbreyta.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build markmið 전용')
    if færibreyta_frumbreyta.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import stofna_færsla
        stofna_færsla(færibreyta_frumbreyta)
        return
    if færibreyta_frumbreyta.classpath or færibreyta_frumbreyta.java_home or færibreyta_frumbreyta.bundle_runtime or færibreyta_frumbreyta.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk markmið 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', færibreyta_frumbreyta.target, '--entry', færibreyta_frumbreyta.entry, '-o', færibreyta_frumbreyta.output]
    for úthluta_VALUE in færibreyta_frumbreyta.export: 자바명령.extend(['--export', úthluta_VALUE])
    subprocess.run(자바명령+færibreyta_frumbreyta.sources, check=True)
    return


if __name__ == '__main__':
    try:
        keyra_skipun()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Villa:
        print('þýða_uppruni Villa: ' + str(Villa), file=sys.stderr)
        sys.exit(1)
