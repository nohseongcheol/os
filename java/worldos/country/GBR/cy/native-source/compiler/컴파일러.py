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
        자신.safle = 0

    def Darllen(자신, hyd_VALUE):
        if hyd_VALUE < 0 or 자신.safle + hyd_VALUE > len(자신.data):
            raise 컴파일오류('잘린 Dosbarth_VALUE 또는 Gorchymyn data')
        mesur = 자신.data[자신.safle:자신.safle + hyd_VALUE]
        자신.safle += hyd_VALUE
        return mesur

    def 수(자신, fformat_VALUE):
        return struct.unpack('>' + fformat_VALUE, 자신.Darllen(struct.calcsize('>' + fformat_VALUE)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    testun_VALUE = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return testun_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Dosbarth_VALUE:
    def __init__(자신, LLWYBR):
        자신.LLWYBR = LLWYBR
        darllenwr_VALUE = 자료읽기(LLWYBR.read_bytes())
        if darllenwr_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Dosbarth_VALUE 표식이 아님')
        darllenwr_VALUE.Darllen(4)
        eitem_COUNT = darllenwr_VALUE.수('H')
        자신.cysonyn_VALUE = [None] * eitem_COUNT
        INDEX = 1
        while INDEX < eitem_COUNT:
            종류 = darllenwr_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(darllenwr_VALUE.Darllen(darllenwr_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = darllenwr_VALUE.수('i')
            elif 종류 == 4:
                VALUE = darllenwr_VALUE.Darllen(4)
            elif 종류 in (5, 6):
                VALUE = darllenwr_VALUE.Darllen(8)
            elif 종류 in (7, 8, 16):
                VALUE = darllenwr_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (darllenwr_VALUE.수('H'), darllenwr_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (darllenwr_VALUE.수('B'), darllenwr_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 cysonyn_VALUE 종류: {}'.format(종류))
            자신.cysonyn_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.mynediad_cofnod = darllenwr_VALUE.수('H')
        자신.Enw = 자신.Dosbarth_enw(darllenwr_VALUE.수('H'))
        부모 = darllenwr_VALUE.수('H')
        if 자신.Dosbarth_enw(부모) != 'java/lang/Object' or darllenwr_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Enw + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.maes_VALUE = 자신.멤버읽기(darllenwr_VALUE)
        자신.SWYDDOGAETH_VALUE = 자신.멤버읽기(darllenwr_VALUE)
        자신.속성읽기(darllenwr_VALUE)

    def 문자(자신, INDEX):
        if 자신.cysonyn_VALUE[INDEX][0] != 1:
            raise 컴파일오류('testun_VALUE cysonyn_VALUE fformat_VALUE Gwall')
        return 자신.cysonyn_VALUE[INDEX][1]

    def Dosbarth_enw(자신, INDEX):
        return 자신.문자(자신.cysonyn_VALUE[INDEX][1])

    def cyfeiriad(자신, INDEX):
        perchennog_VALUE, enw_fformat = 자신.cysonyn_VALUE[INDEX][1]
        Enw, fformat_VALUE = 자신.cysonyn_VALUE[enw_fformat][1]
        return 자신.Dosbarth_enw(perchennog_VALUE), 자신.문자(Enw), 자신.문자(fformat_VALUE)

    def 속성읽기(자신, darllenwr_VALUE):
        mesur = {}
        for _ in range(darllenwr_VALUE.수('H')):
            Enw = 자신.문자(darllenwr_VALUE.수('H'))
            mesur[Enw] = darllenwr_VALUE.Darllen(darllenwr_VALUE.수('I'))
        return mesur

    def 멤버읽기(자신, darllenwr_VALUE):
        mesur = []
        for _ in range(darllenwr_VALUE.수('H')):
            mynediad_cofnod = darllenwr_VALUE.수('H')
            Enw = 자신.문자(darllenwr_VALUE.수('H'))
            fformat_VALUE = 자신.문자(darllenwr_VALUE.수('H'))
            mesur.append((mynediad_cofnod, Enw, fformat_VALUE, 자신.속성읽기(darllenwr_VALUE)))
        return mesur


def 형식읽기(testun_VALUE):
    mesur = []
    safle = 0
    while safle < len(testun_VALUE):
        for fformat_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if testun_VALUE.startswith(fformat_VALUE, safle):
                mesur.append(fformat_VALUE)
                safle += len(fformat_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 math_data: ' + testun_VALUE)
    return mesur


def 함수형식(서술):
    인수, return_mesur = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    return_TYPE = 형식읽기(return_mesur)
    if 'V' in 인수 or len(return_TYPE) != 1:
        raise 컴파일오류('SWYDDOGAETH_VALUE 서술 fformat_VALUE Gwall: ' + 서술)
    return 인수, return_mesur


def symbol(종류, *부분):
    FFYNHONNELL = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(FFYNHONNELL).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 SWYDDOGAETH_VALUE 서술에 대해서만 허용한다.
def Gweithredu_gorchymyn(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ffynhonnell_coeden llunio_system')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/Dosbarth_VALUE 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 llunio_system JDK 또는 openjdk-build의 부트 JDK LLWYBR')
    해석기.add_argument('--bundle-runtime', help='Gweithredu_gorchymyn 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK Rhaglen_lansiwr/ffynhonnell_coeden 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 llunio_system 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 llunio_system targed (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 llunio_system 대상의 libc/헤더/llyfrgell 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 fformat_VALUE')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=Dosbarth_VALUE.SWYDDOGAETH_VALUE (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Gweithredu_2 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='Gweithredu_gorchymyn ELF/.o Allbwn; openjdk-build는 전용 llunio_system 디렉터리')
    해석기.add_argument('sources', nargs='+')
    paramedr_arg = 해석기.parse_args(인수)
    if paramedr_arg.target == 'openjdk-build':
        if len(paramedr_arg.sources) != 1 or not paramedr_arg.java_home or paramedr_arg.entry or paramedr_arg.export or paramedr_arg.classpath or paramedr_arg.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ffynhonnell_coeden 디렉터리 하나와 --java-home 부트 JDK, -o llunio_system 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(paramedr_arg.sources[0], paramedr_arg.output, paramedr_arg.java_home, paramedr_arg.jobs, paramedr_arg.openjdk_target,
                  paramedr_arg.sysroot, None if paramedr_arg.cc == 'cc' else paramedr_arg.cc, paramedr_arg.cxx, paramedr_arg.configure_arg)
        except BuildError as Gwall:
            raise 컴파일오류(str(Gwall))
        return
    if not paramedr_arg.entry:
        해석기.error('--entry is required for this target')
    if paramedr_arg.cxx or paramedr_arg.openjdk_target or paramedr_arg.sysroot or paramedr_arg.configure_arg or paramedr_arg.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build targed 전용')
    if paramedr_arg.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Creu_cofnod
        Creu_cofnod(paramedr_arg)
        return
    if paramedr_arg.classpath or paramedr_arg.java_home or paramedr_arg.bundle_runtime or paramedr_arg.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk targed 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', paramedr_arg.target, '--entry', paramedr_arg.entry, '-o', paramedr_arg.output]
    for 지정 in paramedr_arg.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+paramedr_arg.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Gweithredu_gorchymyn()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Gwall:
        print('llunio_ffynhonnell Gwall: ' + str(Gwall), file=sys.stderr)
        sys.exit(1)
