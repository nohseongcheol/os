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
    def __init__(자신, տվյալ):
        자신.տվյալ = տվյալ
        자신.Դիրք = 0

    def Ընթերցում(자신, տեւողություն_արժեք):
        if տեւողություն_արժեք < 0 or 자신.Դիրք + տեւողություն_արժեք > len(자신.տվյալ):
            raise 컴파일오류('잘린 դաս_արժեք 또는 Հրահանգ տվյալ')
        չափ = 자신.տվյալ[자신.Դիրք:자신.Դիրք + տեւողություն_արժեք]
        자신.Դիրք += տեւողություն_արժեք
        return չափ

    def 수(자신, ձեւաչափ_արժեք):
        return struct.unpack('>' + ձեւաչափ_արժեք, 자신.Ընթերցում(struct.calcsize('>' + ձեւաչափ_արժեք)))[0]


def 수정유티에프해독(տվյալ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    տող_արժեք_6ca8363c = տվյալ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return տող_արժեք_6ca8363c.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class դաս_արժեք:
    def __init__(자신, Ճանապարհ):
        자신.Ճանապարհ = Ճանապարհ
        Ընթերցիչ_արժեք = 자료읽기(Ճանապարհ.read_bytes())
        if Ընթերցիչ_արժեք.수('I') != 0xcafebabe:
            raise 컴파일오류('Java դաս_արժեք 표식이 아님')
        Ընթերցիչ_արժեք.Ընթերցում(4)
        개수 = Ընթերցիչ_արժեք.수('H')
        자신.հաստատուն_արժեք = [None] * 개수
        դասիչ = 1
        while դասիչ < 개수:
            종류 = Ընթերցիչ_արժեք.수('B')
            if 종류 == 1:
                արժեք = 수정유티에프해독(Ընթերցիչ_արժեք.Ընթերցում(Ընթերցիչ_արժեք.수('H')))
            elif 종류 == 3:
                արժեք = Ընթերցիչ_արժեք.수('i')
            elif 종류 == 4:
                արժեք = Ընթերցիչ_արժեք.Ընթերցում(4)
            elif 종류 in (5, 6):
                արժեք = Ընթերցիչ_արժեք.Ընթերցում(8)
            elif 종류 in (7, 8, 16):
                արժեք = Ընթերցիչ_արժեք.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                արժեք = (Ընթերցիչ_արժեք.수('H'), Ընթերցիչ_արժեք.수('H'))
            elif 종류 == 15:
                արժեք = (Ընթերցիչ_արժեք.수('B'), Ընթերցիչ_արժեք.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 հաստատուն_արժեք 종류: {}'.format(종류))
            자신.հաստատուն_արժեք[դասիչ] = (종류, արժեք)
            դասիչ += 2 if 종류 in (5, 6) else 1
        자신.մատչել_մուտքագրում = Ընթերցիչ_արժեք.수('H')
        자신.Անուն = 자신.դաս_անուն(Ընթերցիչ_արժեք.수('H'))
        부모 = Ընթերցիչ_արժեք.수('H')
        if 자신.դաս_անուն(부모) != 'java/lang/Object' or Ընթերցիչ_արժեք.수('H') != 0:
            raise 컴파일오류(자신.Անուն + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.դաշտ_արժեք = 자신.멤버읽기(Ընթերցիչ_արժեք)
        자신.ՖՈՒՆԿՑԻԱ_արժեք = 자신.멤버읽기(Ընթերցիչ_արժեք)
        자신.속성읽기(Ընթերցիչ_արժեք)

    def 문자(자신, դասիչ):
        if 자신.հաստատուն_արժեք[դասիչ][0] != 1:
            raise 컴파일오류('տող_արժեք_6ca8363c հաստատուն_արժեք ձեւաչափ_արժեք Սխալ')
        return 자신.հաստատուն_արժեք[դասիչ][1]

    def դաս_անուն(자신, դասիչ):
        return 자신.문자(자신.հաստատուն_արժեք[դասիչ][1])

    def Տեղեկատուներ(자신, դասիչ):
        տնօրինող_արժեք, անուն_ձեւաչափ = 자신.հաստատուն_արժեք[դասիչ][1]
        Անուն, ձեւաչափ_արժեք = 자신.հաստատուն_արժեք[անուն_ձեւաչափ][1]
        return 자신.դաս_անուն(տնօրինող_արժեք), 자신.문자(Անուն), 자신.문자(ձեւաչափ_արժեք)

    def 속성읽기(자신, Ընթերցիչ_արժեք):
        չափ = {}
        for _ in range(Ընթերցիչ_արժեք.수('H')):
            Անուն = 자신.문자(Ընթերցիչ_արժեք.수('H'))
            չափ[Անուն] = Ընթերցիչ_արժեք.Ընթերցում(Ընթերցիչ_արժեք.수('I'))
        return չափ

    def 멤버읽기(자신, Ընթերցիչ_արժեք):
        չափ = []
        for _ in range(Ընթերցիչ_արժեք.수('H')):
            մատչել_մուտքագրում = Ընթերցիչ_արժեք.수('H')
            Անուն = 자신.문자(Ընթերցիչ_արժեք.수('H'))
            ձեւաչափ_արժեք = 자신.문자(Ընթերցիչ_արժեք.수('H'))
            չափ.append((մատչել_մուտքագրում, Անուն, ձեւաչափ_արժեք, 자신.속성읽기(Ընթերցիչ_արժեք)))
        return չափ


def 형식읽기(տող_արժեք_6ca8363c):
    չափ = []
    Դիրք = 0
    while Դիրք < len(տող_արժեք_6ca8363c):
        for ձեւաչափ_արժեք in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if տող_արժեք_6ca8363c.startswith(ձեւաչափ_արժեք, Դիրք):
                չափ.append(ձեւաչափ_արժեք)
                Դիրք += len(ձեւաչափ_արժեք)
                break
        else:
            raise 컴파일오류('지원하지 않는 տվյալների_տիպ: ' + տող_արժեք_6ca8363c)
    return չափ


def 함수형식(서술):
    인수, վերադարձնել_չափ = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    վերադարձնել_մուտքագրել = 형식읽기(վերադարձնել_չափ)
    if 'V' in 인수 or len(վերադարձնել_մուտքագրել) != 1:
        raise 컴파일오류('ՖՈՒՆԿՑԻԱ_արժեք 서술 ձեւաչափ_արժեք Սխալ: ' + 서술)
    return 인수, վերադարձնել_չափ


def նշան(종류, *부분):
    ԱՂԲՅՈՒՐ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ԱՂԲՅՈՒՐ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ՖՈՒՆԿՑԻԱ_արժեք 서술에 대해서만 허용한다.
def կատարել_հրաման(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK աղբյուր_ծառ կառուցել_համակարգ')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/դաս_արժեք 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 կառուցել_համակարգ JDK 또는 openjdk-build의 부트 JDK Ճանապարհ')
    해석기.add_argument('--bundle-runtime', help='կատարել_հրաման 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK ծրագիր_թողարկիչ/աղբյուր_ծառ 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 կառուցել_համակարգ 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 կառուցել_համակարգ թիրախ (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 կառուցել_համակարգ 대상의 libc/헤더/դարան 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ձեւաչափ_արժեք')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=դաս_արժեք.ՖՈՒՆԿՑԻԱ_արժեք (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Գործարկել (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='կատարել_հրաման ELF/.o Ելք; openjdk-build는 전용 կառուցել_համակարգ 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK աղբյուր_ծառ 디렉터리 하나와 --java-home 부트 JDK, -o կառուցել_համակարգ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Սխալ:
            raise 컴파일오류(str(Սխալ))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build թիրախ 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Կերտի_ր_մուտքագրում
        Կերտի_ր_մուտքագրում(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk թիրախ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        կատարել_հրաման()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Սխալ:
        print('կառուցել_աղբյուր Սխալ: ' + str(Սխալ), file=sys.stderr)
        sys.exit(1)
