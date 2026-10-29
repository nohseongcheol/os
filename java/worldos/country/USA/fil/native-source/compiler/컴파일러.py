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
        자신.posisyon = 0

    def 읽기(자신, haba_VALUE):
        if haba_VALUE < 0 or 자신.posisyon + haba_VALUE > len(자신.data):
            raise 컴파일오류('잘린 kategorya_VALUE_55654bf1 또는 utos data')
        sukat = 자신.data[자신.posisyon:자신.posisyon + haba_VALUE]
        자신.posisyon += haba_VALUE
        return sukat

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.읽기(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    string_VALUE = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return string_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class kategorya_VALUE_55654bf1:
    def __init__(자신, path):
        자신.path = path
        Tagabasa_VALUE = 자료읽기(path.read_bytes())
        if Tagabasa_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java kategorya_VALUE_55654bf1 표식이 아님')
        Tagabasa_VALUE.읽기(4)
        item_COUNT = Tagabasa_VALUE.수('H')
        자신.constant_VALUE = [None] * item_COUNT
        INDEX = 1
        while INDEX < item_COUNT:
            종류 = Tagabasa_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Tagabasa_VALUE.읽기(Tagabasa_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Tagabasa_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Tagabasa_VALUE.읽기(4)
            elif 종류 in (5, 6):
                VALUE = Tagabasa_VALUE.읽기(8)
            elif 종류 in (7, 8, 16):
                VALUE = Tagabasa_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Tagabasa_VALUE.수('H'), Tagabasa_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Tagabasa_VALUE.수('B'), Tagabasa_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 constant_VALUE 종류: {}'.format(종류))
            자신.constant_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.access_pagpasok = Tagabasa_VALUE.수('H')
        자신.pangalan = 자신.kategorya_pangalan(Tagabasa_VALUE.수('H'))
        부모 = Tagabasa_VALUE.수('H')
        if 자신.kategorya_pangalan(부모) != 'java/lang/Object' or Tagabasa_VALUE.수('H') != 0:
            raise 컴파일오류(자신.pangalan + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.field_VALUE = 자신.멤버읽기(Tagabasa_VALUE)
        자신.pormula_VALUE = 자신.멤버읽기(Tagabasa_VALUE)
        자신.속성읽기(Tagabasa_VALUE)

    def 문자(자신, INDEX):
        if 자신.constant_VALUE[INDEX][0] != 1:
            raise 컴파일오류('string_VALUE constant_VALUE format_VALUE error')
        return 자신.constant_VALUE[INDEX][1]

    def kategorya_pangalan(자신, INDEX):
        return 자신.문자(자신.constant_VALUE[INDEX][1])

    def Sanggunian(자신, INDEX):
        may_ari_VALUE, pangalan_format = 자신.constant_VALUE[INDEX][1]
        pangalan, format_VALUE = 자신.constant_VALUE[pangalan_format][1]
        return 자신.kategorya_pangalan(may_ari_VALUE), 자신.문자(pangalan), 자신.문자(format_VALUE)

    def 속성읽기(자신, Tagabasa_VALUE):
        sukat = {}
        for _ in range(Tagabasa_VALUE.수('H')):
            pangalan = 자신.문자(Tagabasa_VALUE.수('H'))
            sukat[pangalan] = Tagabasa_VALUE.읽기(Tagabasa_VALUE.수('I'))
        return sukat

    def 멤버읽기(자신, Tagabasa_VALUE):
        sukat = []
        for _ in range(Tagabasa_VALUE.수('H')):
            access_pagpasok = Tagabasa_VALUE.수('H')
            pangalan = 자신.문자(Tagabasa_VALUE.수('H'))
            format_VALUE = 자신.문자(Tagabasa_VALUE.수('H'))
            sukat.append((access_pagpasok, pangalan, format_VALUE, 자신.속성읽기(Tagabasa_VALUE)))
        return sukat


def 형식읽기(string_VALUE):
    sukat = []
    posisyon = 0
    while posisyon < len(string_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if string_VALUE.startswith(format_VALUE, posisyon):
                sukat.append(format_VALUE)
                posisyon += len(format_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 uri_ng_data: ' + string_VALUE)
    return sukat


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('pormula_VALUE 서술 format_VALUE error: ' + 서술)
    return 인수, 반환


def simbolo(종류, *부분):
    pinagmulan = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(pinagmulan).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 pormula_VALUE 서술에 대해서만 허용한다.
def Mag_execute_utos(인수=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK pinagmulan_balangkas build_system')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/kategorya_VALUE_55654bf1 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 build_system JDK 또는 openjdk-build의 부트 JDK path')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='Mag_execute_utos 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK app_launcher/pinagmulan_balangkas 빌드의 C 컴파일러')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 build_system 작업 수')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 build_system layunin (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 build_system 대상의 libc/헤더/library 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=kategorya_VALUE_55654bf1.pormula_VALUE (자체 스택 ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.run (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='Mag_execute_utos ELF/.o 출력; openjdk-build는 전용 build_system 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parameter_argumento = parser_48ee4b1b.parse_args(인수)
    if parameter_argumento.target == 'openjdk-build':
        if len(parameter_argumento.sources) != 1 or not parameter_argumento.java_home or parameter_argumento.entry or parameter_argumento.export or parameter_argumento.classpath or parameter_argumento.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK pinagmulan_balangkas 디렉터리 하나와 --java-home 부트 JDK, -o build_system 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argumento.sources[0], parameter_argumento.output, parameter_argumento.java_home, parameter_argumento.jobs, parameter_argumento.openjdk_target,
                  parameter_argumento.sysroot, None if parameter_argumento.cc == 'cc' else parameter_argumento.cc, parameter_argumento.cxx, parameter_argumento.configure_arg)
        except BuildError as error:
            raise 컴파일오류(str(error))
        return
    if not parameter_argumento.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parameter_argumento.cxx or parameter_argumento.openjdk_target or parameter_argumento.sysroot or parameter_argumento.configure_arg or parameter_argumento.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build layunin 전용')
    if parameter_argumento.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Create_pagpasok
        Create_pagpasok(parameter_argumento)
        return
    if parameter_argumento.classpath or parameter_argumento.java_home or parameter_argumento.bundle_runtime or parameter_argumento.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk layunin 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argumento.target, '--entry', parameter_argumento.entry, '-o', parameter_argumento.output]
    for italaga_VALUE in parameter_argumento.export: 자바명령.extend(['--export', italaga_VALUE])
    subprocess.run(자바명령+parameter_argumento.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Mag_execute_utos()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as error:
        print('bumuo_pinagmulan error: ' + str(error), file=sys.stderr)
        sys.exit(1)
