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
    def __init__(자신, მონაცემები):
        자신.მონაცემები = მონაცემები
        자신.პოზიცია = 0

    def კითხვა(자신, სიგრძე_მნიშვნელობა):
        if სიგრძე_მნიშვნელობა < 0 or 자신.პოზიცია + სიგრძე_მნიშვნელობა > len(자신.მონაცემები):
            raise 컴파일오류('잘린 კლასი_მნიშვნელობა 또는 ბრძანება მონაცემები')
        გაზომვა = 자신.მონაცემები[자신.პოზიცია:자신.პოზიცია + სიგრძე_მნიშვნელობა]
        자신.პოზიცია += სიგრძე_მნიშვნელობა
        return გაზომვა

    def 수(자신, ფორმატი_მნიშვნელობა):
        return struct.unpack('>' + ფორმატი_მნიშვნელობა, 자신.კითხვა(struct.calcsize('>' + ფორმატი_მნიშვნელობა)))[0]


def 수정유티에프해독(მონაცემები):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    სტრიქონი_მნიშვნელობა = მონაცემები.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return სტრიქონი_მნიშვნელობა.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class კლასი_მნიშვნელობა:
    def __init__(자신, გეზი):
        자신.გეზი = გეზი
        წამკითხველი_მნიშვნელობა = 자료읽기(გეზი.read_bytes())
        if წამკითხველი_მნიშვნელობა.수('I') != 0xcafebabe:
            raise 컴파일오류('Java კლასი_მნიშვნელობა 표식이 아님')
        წამკითხველი_მნიშვნელობა.კითხვა(4)
        개수 = წამკითხველი_მნიშვნელობა.수('H')
        자신.მუდმივა_მნიშვნელობა = [None] * 개수
        ინდექსი = 1
        while ინდექსი < 개수:
            종류 = წამკითხველი_მნიშვნელობა.수('B')
            if 종류 == 1:
                მნიშვნელობა = 수정유티에프해독(წამკითხველი_მნიშვნელობა.კითხვა(წამკითხველი_მნიშვნელობა.수('H')))
            elif 종류 == 3:
                მნიშვნელობა = წამკითხველი_მნიშვნელობა.수('i')
            elif 종류 == 4:
                მნიშვნელობა = წამკითხველი_მნიშვნელობა.კითხვა(4)
            elif 종류 in (5, 6):
                მნიშვნელობა = წამკითხველი_მნიშვნელობა.კითხვა(8)
            elif 종류 in (7, 8, 16):
                მნიშვნელობა = წამკითხველი_მნიშვნელობა.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                მნიშვნელობა = (წამკითხველი_მნიშვნელობა.수('H'), წამკითხველი_მნიშვნელობა.수('H'))
            elif 종류 == 15:
                მნიშვნელობა = (წამკითხველი_მნიშვნელობა.수('B'), წამკითხველი_მნიშვნელობა.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 მუდმივა_მნიშვნელობა 종류: {}'.format(종류))
            자신.მუდმივა_მნიშვნელობა[ინდექსი] = (종류, მნიშვნელობა)
            ინდექსი += 2 if 종류 in (5, 6) else 1
        자신.წვდომა_შენატანი = წამკითხველი_მნიშვნელობა.수('H')
        자신.სახელი = 자신.კლასი_სახელი(წამკითხველი_მნიშვნელობა.수('H'))
        부모 = წამკითხველი_მნიშვნელობა.수('H')
        if 자신.კლასი_სახელი(부모) != 'java/lang/Object' or წამკითხველი_მნიშვნელობა.수('H') != 0:
            raise 컴파일오류(자신.სახელი + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ველი_მნიშვნელობა = 자신.멤버읽기(წამკითხველი_მნიშვნელობა)
        자신.ფუნქცია_მნიშვნელობა = 자신.멤버읽기(წამკითხველი_მნიშვნელობა)
        자신.속성읽기(წამკითხველი_მნიშვნელობა)

    def 문자(자신, ინდექსი):
        if 자신.მუდმივა_მნიშვნელობა[ინდექსი][0] != 1:
            raise 컴파일오류('სტრიქონი_მნიშვნელობა მუდმივა_მნიშვნელობა ფორმატი_მნიშვნელობა შეცდომა')
        return 자신.მუდმივა_მნიშვნელობა[ინდექსი][1]

    def კლასი_სახელი(자신, ინდექსი):
        return 자신.문자(자신.მუდმივა_მნიშვნელობა[ინდექსი][1])

    def ცნობარები(자신, ინდექსი):
        მფლობელი_მნიშვნელობა, სახელი_ფორმატი = 자신.მუდმივა_მნიშვნელობა[ინდექსი][1]
        სახელი, ფორმატი_მნიშვნელობა = 자신.მუდმივა_მნიშვნელობა[სახელი_ფორმატი][1]
        return 자신.კლასი_სახელი(მფლობელი_მნიშვნელობა), 자신.문자(სახელი), 자신.문자(ფორმატი_მნიშვნელობა)

    def 속성읽기(자신, წამკითხველი_მნიშვნელობა):
        გაზომვა = {}
        for _ in range(წამკითხველი_მნიშვნელობა.수('H')):
            სახელი = 자신.문자(წამკითხველი_მნიშვნელობა.수('H'))
            გაზომვა[სახელი] = წამკითხველი_მნიშვნელობა.კითხვა(წამკითხველი_მნიშვნელობა.수('I'))
        return გაზომვა

    def 멤버읽기(자신, წამკითხველი_მნიშვნელობა):
        გაზომვა = []
        for _ in range(წამკითხველი_მნიშვნელობა.수('H')):
            წვდომა_შენატანი = წამკითხველი_მნიშვნელობა.수('H')
            სახელი = 자신.문자(წამკითხველი_მნიშვნელობა.수('H'))
            ფორმატი_მნიშვნელობა = 자신.문자(წამკითხველი_მნიშვნელობა.수('H'))
            გაზომვა.append((წვდომა_შენატანი, სახელი, ფორმატი_მნიშვნელობა, 자신.속성읽기(წამკითხველი_მნიშვნელობა)))
        return გაზომვა


def 형식읽기(სტრიქონი_მნიშვნელობა):
    გაზომვა = []
    პოზიცია = 0
    while პოზიცია < len(სტრიქონი_მნიშვნელობა):
        for ფორმატი_მნიშვნელობა in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if სტრიქონი_მნიშვნელობა.startswith(ფორმატი_მნიშვნელობა, პოზიცია):
                გაზომვა.append(ფორმატი_მნიშვნელობა)
                პოზიცია += len(ფორმატი_მნიშვნელობა)
                break
        else:
            raise 컴파일오류('지원하지 않는 მონაცემთა_ტიპი: ' + სტრიქონი_მნიშვნელობა)
    return გაზომვა


def 함수형식(서술):
    인수, დაბრუნება_გაზომვა = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    დაბრუნება_აკრეფა = 형식읽기(დაბრუნება_გაზომვა)
    if 'V' in 인수 or len(დაბრუნება_აკრეფა) != 1:
        raise 컴파일오류('ფუნქცია_მნიშვნელობა 서술 ფორმატი_მნიშვნელობა შეცდომა: ' + 서술)
    return 인수, დაბრუნება_გაზომვა


def სიმბოლო(종류, *부분):
    წყარო = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(წყარო).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ფუნქცია_მნიშვნელობა 서술에 대해서만 허용한다.
def შესრულება_ბრძანება(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK წყარო_ხე აწყობა_სისტემა')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/კლასი_მნიშვნელობა 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 აწყობა_სისტემა JDK 또는 openjdk-build의 부트 JDK გეზი')
    해석기.add_argument('--bundle-runtime', help='შესრულება_ბრძანება 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK აპი_გამშვები/წყარო_ხე 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 აწყობა_სისტემა 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 აწყობა_სისტემა მიზანი (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 აწყობა_სისტემა 대상의 libc/헤더/ბიბლიოთეკა 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ფორმატი_მნიშვნელობა')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=კლასი_მნიშვნელობა.ფუნქცია_მნიშვნელობა (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.გაშვება (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='შესრულება_ბრძანება ELF/.o 출력; openjdk-build는 전용 აწყობა_სისტემა 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK წყარო_ხე 디렉터리 하나와 --java-home 부트 JDK, -o აწყობა_სისტემა 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as შეცდომა:
            raise 컴파일오류(str(შეცდომა))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build მიზანი 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import შექმნა_შენატანი
        შექმნა_შენატანი(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk მიზანი 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        შესრულება_ბრძანება()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as შეცდომა:
        print('აწყობა_წყარო შეცდომა: ' + str(შეცდომა), file=sys.stderr)
        sys.exit(1)
