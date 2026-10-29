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
    def __init__(자신, мәгълүмат):
        자신.мәгълүмат = мәгълүмат
        자신.урнаштыру = 0

    def 읽기(자신, озынлык_VALUE):
        if озынлык_VALUE < 0 or 자신.урнаштыру + озынлык_VALUE > len(자신.мәгълүмат):
            raise 컴파일오류('잘린 класс_VALUE 또는 команда мәгълүмат')
        үлчәм = 자신.мәгълүмат[자신.урнаштыру:자신.урнаштыру + озынлык_VALUE]
        자신.урнаштыру += озынлык_VALUE
        return үлчәм

    def 수(자신, формат_VALUE):
        return struct.unpack('>' + формат_VALUE, 자신.읽기(struct.calcsize('>' + формат_VALUE)))[0]


def 수정유티에프해독(мәгълүмат):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    юл_VALUE_6ca8363c = мәгълүмат.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return юл_VALUE_6ca8363c.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class класс_VALUE:
    def __init__(자신, Yul):
        자신.Yul = Yul
        укучы_VALUE = 자료읽기(Yul.read_bytes())
        if укучы_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java класс_VALUE 표식이 아님')
        укучы_VALUE.읽기(4)
        элемент_COUNT = укучы_VALUE.수('H')
        자신.константа_VALUE = [None] * элемент_COUNT
        INDEX = 1
        while INDEX < элемент_COUNT:
            종류 = укучы_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(укучы_VALUE.읽기(укучы_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = укучы_VALUE.수('i')
            elif 종류 == 4:
                VALUE = укучы_VALUE.읽기(4)
            elif 종류 in (5, 6):
                VALUE = укучы_VALUE.읽기(8)
            elif 종류 in (7, 8, 16):
                VALUE = укучы_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (укучы_VALUE.수('H'), укучы_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (укучы_VALUE.수('B'), укучы_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 константа_VALUE 종류: {}'.format(종류))
            자신.константа_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.керү_кертү = укучы_VALUE.수('H')
        자신.исем = 자신.класс_исем(укучы_VALUE.수('H'))
        부모 = укучы_VALUE.수('H')
        if 자신.класс_исем(부모) != 'java/lang/Object' or укучы_VALUE.수('H') != 0:
            raise 컴파일오류(자신.исем + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.кыр_VALUE = 자신.멤버읽기(укучы_VALUE)
        자신.ФУНКЦИЯ_VALUE = 자신.멤버읽기(укучы_VALUE)
        자신.속성읽기(укучы_VALUE)

    def 문자(자신, INDEX):
        if 자신.константа_VALUE[INDEX][0] != 1:
            raise 컴파일오류('юл_VALUE_6ca8363c константа_VALUE формат_VALUE Хата')
        return 자신.константа_VALUE[INDEX][1]

    def класс_исем(자신, INDEX):
        return 자신.문자(자신.константа_VALUE[INDEX][1])

    def Белешмәлекләр(자신, INDEX):
        биләүче_VALUE, исем_формат = 자신.константа_VALUE[INDEX][1]
        исем, формат_VALUE = 자신.константа_VALUE[исем_формат][1]
        return 자신.класс_исем(биләүче_VALUE), 자신.문자(исем), 자신.문자(формат_VALUE)

    def 속성읽기(자신, укучы_VALUE):
        үлчәм = {}
        for _ in range(укучы_VALUE.수('H')):
            исем = 자신.문자(укучы_VALUE.수('H'))
            үлчәм[исем] = укучы_VALUE.읽기(укучы_VALUE.수('I'))
        return үлчәм

    def 멤버읽기(자신, укучы_VALUE):
        үлчәм = []
        for _ in range(укучы_VALUE.수('H')):
            керү_кертү = укучы_VALUE.수('H')
            исем = 자신.문자(укучы_VALUE.수('H'))
            формат_VALUE = 자신.문자(укучы_VALUE.수('H'))
            үлчәм.append((керү_кертү, исем, формат_VALUE, 자신.속성읽기(укучы_VALUE)))
        return үлчәм


def 형식읽기(юл_VALUE_6ca8363c):
    үлчәм = []
    урнаштыру = 0
    while урнаштыру < len(юл_VALUE_6ca8363c):
        for формат_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if юл_VALUE_6ca8363c.startswith(формат_VALUE, урнаштыру):
                үлчәм.append(формат_VALUE)
                урнаштыру += len(формат_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 мәгълүмат_төре: ' + юл_VALUE_6ca8363c)
    return үлчәм


def 함수형식(서술):
    인수, кайтару_үлчәм = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    кайтару_TYPE = 형식읽기(кайтару_үлчәм)
    if 'V' in 인수 or len(кайтару_TYPE) != 1:
        raise 컴파일오류('ФУНКЦИЯ_VALUE 서술 формат_VALUE Хата: ' + 서술)
    return 인수, кайтару_үлчәм


def символ(종류, *부분):
    чыганак = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(чыганак).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ФУНКЦИЯ_VALUE 서술에 대해서만 허용한다.
def үтәргә_команда(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK чыганак_агач төзү_система')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/класс_VALUE 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 төзү_система JDK 또는 openjdk-build의 부트 JDK Yul')
    해석기.add_argument('--bundle-runtime', help='үтәргә_команда 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK кушымта_хезмәткәр/чыганак_агач 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 төзү_система 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 төзү_система максат_кыйммәт (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 төзү_система 대상의 libc/헤더/библиотека 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 формат_VALUE')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=класс_VALUE.ФУНКЦИЯ_VALUE (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.эшләтү (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='үтәргә_команда ELF/.o 출력; openjdk-build는 전용 төзү_система 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK чыганак_агач 디렉터리 하나와 --java-home 부트 JDK, -o төзү_система 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Хата:
            raise 컴파일오류(str(Хата))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build максат_кыйммәт 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Төзү_кертү
        Төзү_кертү(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk максат_кыйммәт 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        үтәргә_команда()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Хата:
        print('төзү_чыганак Хата: ' + str(Хата), file=sys.stderr)
        sys.exit(1)
