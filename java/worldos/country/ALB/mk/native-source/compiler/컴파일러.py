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
    def __init__(자신, податоци):
        자신.податоци = податоци
        자신.Позиција = 0

    def Читај(자신, должина_VALUE):
        if должина_VALUE < 0 or 자신.Позиција + должина_VALUE > len(자신.податоци):
            raise 컴파일오류('잘린 класа_VALUE 또는 Команда податоци')
        мерка = 자신.податоци[자신.Позиција:자신.Позиција + должина_VALUE]
        자신.Позиција += должина_VALUE
        return мерка

    def 수(자신, формат_VALUE):
        return struct.unpack('>' + формат_VALUE, 자신.Читај(struct.calcsize('>' + формат_VALUE)))[0]


def 수정유티에프해독(податоци):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    низа_VALUE_6ca8363c = податоци.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return низа_VALUE_6ca8363c.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class класа_VALUE:
    def __init__(자신, ПАТЕКА):
        자신.ПАТЕКА = ПАТЕКА
        Читач_VALUE = 자료읽기(ПАТЕКА.read_bytes())
        if Читач_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java класа_VALUE 표식이 아님')
        Читач_VALUE.Читај(4)
        ставка_COUNT = Читач_VALUE.수('H')
        자신.константа_VALUE = [None] * ставка_COUNT
        INDEX = 1
        while INDEX < ставка_COUNT:
            종류 = Читач_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Читач_VALUE.Читај(Читач_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Читач_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Читач_VALUE.Читај(4)
            elif 종류 in (5, 6):
                VALUE = Читач_VALUE.Читај(8)
            elif 종류 in (7, 8, 16):
                VALUE = Читач_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Читач_VALUE.수('H'), Читач_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Читач_VALUE.수('B'), Читач_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 константа_VALUE 종류: {}'.format(종류))
            자신.константа_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.пристап_внес = Читач_VALUE.수('H')
        자신.Име = 자신.класа_име(Читач_VALUE.수('H'))
        부모 = Читач_VALUE.수('H')
        if 자신.класа_име(부모) != 'java/lang/Object' or Читач_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Име + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.поле_VALUE = 자신.멤버읽기(Читач_VALUE)
        자신.ФУНКЦИЈА_VALUE = 자신.멤버읽기(Читач_VALUE)
        자신.속성읽기(Читач_VALUE)

    def 문자(자신, INDEX):
        if 자신.константа_VALUE[INDEX][0] != 1:
            raise 컴파일오류('низа_VALUE_6ca8363c константа_VALUE формат_VALUE ГРЕШКА')
        return 자신.константа_VALUE[INDEX][1]

    def класа_име(자신, INDEX):
        return 자신.문자(자신.константа_VALUE[INDEX][1])

    def Референци(자신, INDEX):
        сопственик_VALUE, име_формат = 자신.константа_VALUE[INDEX][1]
        Име, формат_VALUE = 자신.константа_VALUE[име_формат][1]
        return 자신.класа_име(сопственик_VALUE), 자신.문자(Име), 자신.문자(формат_VALUE)

    def 속성읽기(자신, Читач_VALUE):
        мерка = {}
        for _ in range(Читач_VALUE.수('H')):
            Име = 자신.문자(Читач_VALUE.수('H'))
            мерка[Име] = Читач_VALUE.Читај(Читач_VALUE.수('I'))
        return мерка

    def 멤버읽기(자신, Читач_VALUE):
        мерка = []
        for _ in range(Читач_VALUE.수('H')):
            пристап_внес = Читач_VALUE.수('H')
            Име = 자신.문자(Читач_VALUE.수('H'))
            формат_VALUE = 자신.문자(Читач_VALUE.수('H'))
            мерка.append((пристап_внес, Име, формат_VALUE, 자신.속성읽기(Читач_VALUE)))
        return мерка


def 형식읽기(низа_VALUE_6ca8363c):
    мерка = []
    Позиција = 0
    while Позиција < len(низа_VALUE_6ca8363c):
        for формат_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if низа_VALUE_6ca8363c.startswith(формат_VALUE, Позиција):
                мерка.append(формат_VALUE)
                Позиција += len(формат_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 тип_податоци: ' + низа_VALUE_6ca8363c)
    return мерка


def 함수형식(서술):
    Аргументи, 반환 = 서술[1:].split(')')
    Аргументи = 형식읽기(Аргументи)
    반환형 = 형식읽기(반환)
    if 'V' in Аргументи or len(반환형) != 1:
        raise 컴파일오류('ФУНКЦИЈА_VALUE 서술 формат_VALUE ГРЕШКА: ' + 서술)
    return Аргументи, 반환


def симбол(종류, *부분):
    ИЗВОР = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ИЗВОР).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ФУНКЦИЈА_VALUE 서술에 대해서만 허용한다.
def Изврши_наредба(Аргументи=None):
    анализатор_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK извор_дрво верзија_систем')
    анализатор_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    анализатор_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/класа_VALUE 디렉터리')
    анализатор_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 верзија_систем JDK 또는 openjdk-build의 부트 JDK ПАТЕКА')
    анализатор_48ee4b1b.add_argument('--bundle-runtime', help='Изврши_наредба 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    анализатор_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK програма_стартувач/извор_дрво 빌드의 C 컴파일러')
    анализатор_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    анализатор_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 верзија_систем 작업 수')
    анализатор_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 верзија_систем цел (예: aarch64-linux-gnu)')
    анализатор_48ee4b1b.add_argument('--sysroot', help='교차 верзија_систем 대상의 libc/헤더/библиотека 루트')
    анализатор_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 формат_VALUE')
    анализатор_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=класа_VALUE.ФУНКЦИЈА_VALUE (자체 스택 ABI)')
    анализатор_48ee4b1b.add_argument('--entry', help='예: 계산.Изврши_2 (openjdk-build 이외 대상에서 필수)')
    анализатор_48ee4b1b.add_argument('-o', '--output', required=True, help='Изврши_наредба ELF/.o 출력; openjdk-build는 전용 верзија_систем 디렉터리')
    анализатор_48ee4b1b.add_argument('sources', nargs='+')
    параметар_аргумент = анализатор_48ee4b1b.parse_args(Аргументи)
    if параметар_аргумент.target == 'openjdk-build':
        if len(параметар_аргумент.sources) != 1 or not параметар_аргумент.java_home or параметар_аргумент.entry or параметар_аргумент.export or параметар_аргумент.classpath or параметар_аргумент.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK извор_дрво 디렉터리 하나와 --java-home 부트 JDK, -o верзија_систем 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(параметар_аргумент.sources[0], параметар_аргумент.output, параметар_аргумент.java_home, параметар_аргумент.jobs, параметар_аргумент.openjdk_target,
                  параметар_аргумент.sysroot, None if параметар_аргумент.cc == 'cc' else параметар_аргумент.cc, параметар_аргумент.cxx, параметар_аргумент.configure_arg)
        except BuildError as ГРЕШКА:
            raise 컴파일오류(str(ГРЕШКА))
        return
    if not параметар_аргумент.entry:
        анализатор_48ee4b1b.error('--entry is required for this target')
    if параметар_аргумент.cxx or параметар_аргумент.openjdk_target or параметар_аргумент.sysroot or параметар_аргумент.configure_arg or параметар_аргумент.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build цел 전용')
    if параметар_аргумент.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Create_внес
        Create_внес(параметар_аргумент)
        return
    if параметар_аргумент.classpath or параметар_аргумент.java_home or параметар_аргумент.bundle_runtime or параметар_аргумент.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk цел 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', параметар_аргумент.target, '--entry', параметар_аргумент.entry, '-o', параметар_аргумент.output]
    for доделува_VALUE in параметар_аргумент.export: 자바명령.extend(['--export', доделува_VALUE])
    subprocess.run(자바명령+параметар_аргумент.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Изврши_наредба()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ГРЕШКА:
        print('изгради_извор ГРЕШКА: ' + str(ГРЕШКА), file=sys.stderr)
        sys.exit(1)
