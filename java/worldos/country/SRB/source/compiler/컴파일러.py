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
    def __init__(자신, подаци):
        자신.подаци = подаци
        자신.Положај = 0

    def Чита(자신, дужина_вриједност):
        if дужина_вриједност < 0 or 자신.Положај + дужина_вриједност > len(자신.подаци):
            raise 컴파일오류('잘린 класа_вриједност 또는 Наредба подаци')
        ИСХОД = 자신.подаци[자신.Положај:자신.Положај + дужина_вриједност]
        자신.Положај += дужина_вриједност
        return ИСХОД

    def 수(자신, формат_вриједност):
        return struct.unpack('>' + формат_вриједност, 자신.Чита(struct.calcsize('>' + формат_вриједност)))[0]


def 수정유티에프해독(подаци):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ниска_вриједност = подаци.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ниска_вриједност.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class класа_вриједност:
    def __init__(자신, ПУТАЊА):
        자신.ПУТАЊА = ПУТАЊА
        Читач_вриједност = 자료읽기(ПУТАЊА.read_bytes())
        if Читач_вриједност.수('I') != 0xcafebabe:
            raise 컴파일오류('Java класа_вриједност 표식이 아님')
        Читач_вриједност.Чита(4)
        개수 = Читач_вриједност.수('H')
        자신.константа_вриједност = [None] * 개수
        индекс = 1
        while индекс < 개수:
            종류 = Читач_вриједност.수('B')
            if 종류 == 1:
                вриједност = 수정유티에프해독(Читач_вриједност.Чита(Читач_вриједност.수('H')))
            elif 종류 == 3:
                вриједност = Читач_вриједност.수('i')
            elif 종류 == 4:
                вриједност = Читач_вриједност.Чита(4)
            elif 종류 in (5, 6):
                вриједност = Читач_вриједност.Чита(8)
            elif 종류 in (7, 8, 16):
                вриједност = Читач_вриједност.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                вриједност = (Читач_вриједност.수('H'), Читач_вриједност.수('H'))
            elif 종류 == 15:
                вриједност = (Читач_вриједност.수('B'), Читач_вриједност.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 константа_вриједност 종류: {}'.format(종류))
            자신.константа_вриједност[индекс] = (종류, вриједност)
            индекс += 2 if 종류 in (5, 6) else 1
        자신.приступ_унос = Читач_вриједност.수('H')
        자신.Назив = 자신.име_класе(Читач_вриједност.수('H'))
        родитељ_вриједност = Читач_вриједност.수('H')
        if 자신.име_класе(родитељ_вриједност) != 'java/lang/Object' or Читач_вриједност.수('H') != 0:
            raise 컴파일오류(자신.Назив + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.поље_вриједност = 자신.멤버읽기(Читач_вриједност)
        자신.функција_вриједност = 자신.멤버읽기(Читач_вриједност)
        자신.속성읽기(Читач_вриједност)

    def 문자(자신, индекс):
        if 자신.константа_вриједност[индекс][0] != 1:
            raise 컴파일오류('ниска_вриједност константа_вриједност формат_вриједност ГРЕШКА')
        return 자신.константа_вриједност[индекс][1]

    def име_класе(자신, индекс):
        return 자신.문자(자신.константа_вриједност[индекс][1])

    def Литература(자신, индекс):
        власник_вриједност, име_формат = 자신.константа_вриједност[индекс][1]
        Назив, формат_вриједност = 자신.константа_вриједност[име_формат][1]
        return 자신.име_класе(власник_вриједност), 자신.문자(Назив), 자신.문자(формат_вриједност)

    def 속성읽기(자신, Читач_вриједност):
        ИСХОД = {}
        for _ in range(Читач_вриједност.수('H')):
            Назив = 자신.문자(Читач_вриједност.수('H'))
            ИСХОД[Назив] = Читач_вриједност.Чита(Читач_вриједност.수('I'))
        return ИСХОД

    def 멤버읽기(자신, Читач_вриједност):
        ИСХОД = []
        for _ in range(Читач_вриједност.수('H')):
            приступ_унос = Читач_вриједност.수('H')
            Назив = 자신.문자(Читач_вриједност.수('H'))
            формат_вриједност = 자신.문자(Читач_вриједност.수('H'))
            ИСХОД.append((приступ_унос, Назив, формат_вриједност, 자신.속성읽기(Читач_вриједност)))
        return ИСХОД


def 형식읽기(ниска_вриједност):
    ИСХОД = []
    Положај = 0
    while Положај < len(ниска_вриједност):
        for формат_вриједност in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ниска_вриједност.startswith(формат_вриједност, Положај):
                ИСХОД.append(формат_вриједност)
                Положај += len(формат_вриједност)
                break
        else:
            raise 컴파일오류('지원하지 않는 тип_података: ' + ниска_вриједност)
    return ИСХОД


def 함수형식(서술):
    Аргументи, вратити_мера = 서술[1:].split(')')
    Аргументи = 형식읽기(Аргументи)
    вратити_тип = 형식읽기(вратити_мера)
    if 'V' in Аргументи or len(вратити_тип) != 1:
        raise 컴파일오류('функција_вриједност 서술 формат_вриједност ГРЕШКА: ' + 서술)
    return Аргументи, вратити_мера


def симбол(종류, *부분):
    ИЗВОР = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ИЗВОР).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 функција_вриједност 서술에 대해서만 허용한다.
def Изврши_команда(Аргументи=None):
    анализатор_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK извор_стабло градити_систем')
    анализатор_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    анализатор_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 додати_унос JAR/класа_вриједност 디렉터리')
    анализатор_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 градити_систем JDK 또는 openjdk-build의 부트 JDK ПУТАЊА')
    анализатор_48ee4b1b.add_argument('--bundle-runtime', help='Изврши_команда 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    анализатор_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK програм_покретач/извор_стабло 빌드의 C 컴파일러')
    анализатор_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    анализатор_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 градити_систем 작업 수')
    анализатор_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 градити_систем циљ (예: aarch64-linux-gnu)')
    анализатор_48ee4b1b.add_argument('--sysroot', help='교차 градити_систем 대상의 libc/헤더/библиотека 루트')
    анализатор_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 формат_вриједност')
    анализатор_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=класа_вриједност.функција_вриједност (자체 операнд_комплет ABI)')
    анализатор_48ee4b1b.add_argument('--entry', help='예: 계산.Покрени (openjdk-build 이외 대상에서 필수)')
    анализатор_48ee4b1b.add_argument('-o', '--output', required=True, help='Изврши_команда ELF/.o Излаз; openjdk-build는 전용 градити_систем 디렉터리')
    анализатор_48ee4b1b.add_argument('sources', nargs='+')
    параметар_аргумент = анализатор_48ee4b1b.parse_args(Аргументи)
    if параметар_аргумент.target == 'openjdk-build':
        if len(параметар_аргумент.sources) != 1 or not параметар_аргумент.java_home or параметар_аргумент.entry or параметар_аргумент.export or параметар_аргумент.classpath or параметар_аргумент.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK извор_стабло 디렉터리 하나와 --java-home 부트 JDK, -o градити_систем 디렉터리를 지정하세요')
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
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build циљ 전용')
    if параметар_аргумент.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Направи_унос
        Направи_унос(параметар_аргумент)
        return
    if параметар_аргумент.classpath or параметар_аргумент.java_home or параметар_аргумент.bundle_runtime or параметар_аргумент.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk циљ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', параметар_аргумент.target, '--entry', параметар_аргумент.entry, '-o', параметар_аргумент.output]
    for Додели_вриједност in параметар_аргумент.export: 자바명령.extend(['--export', Додели_вриједност])
    subprocess.run(자바명령+параметар_аргумент.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Изврши_команда()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ГРЕШКА:
        print('направити_извор ГРЕШКА: ' + str(ГРЕШКА), file=sys.stderr)
        sys.exit(1)
