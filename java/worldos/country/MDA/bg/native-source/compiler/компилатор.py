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


class грешка_при_компилиране(Exception):
    pass


class 자료읽기:
    def __init__(자신, данни):
        자신.данни = данни
        자신.Позиция = 0

    def Четене(자신, 길이):
        if 길이 < 0 or 자신.Позиция + 길이 > len(자신.данни):
            raise грешка_при_компилиране('잘린 Клас_стойност 또는 Команда данни')
        РЕЗУЛТАТ = 자신.данни[자신.Позиция:자신.Позиция + 길이]
        자신.Позиция += 길이
        return РЕЗУЛТАТ

    def 수(자신, формат_стойност):
        return struct.unpack('>' + формат_стойност, 자신.Четене(struct.calcsize('>' + формат_стойност)))[0]


def 수정유티에프해독(данни):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    низ_стойност = данни.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return низ_стойност.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Клас_стойност:
    def __init__(자신, ПЪТ):
        자신.ПЪТ = ПЪТ
        читател_стойност = 자료읽기(ПЪТ.read_bytes())
        if читател_стойност.수('I') != 0xcafebabe:
            raise грешка_при_компилиране('Java Клас_стойност 표식이 아님')
        читател_стойност.Четене(4)
        개수 = читател_стойност.수('H')
        자신.константа_стойност = [None] * 개수
        индекс = 1
        while индекс < 개수:
            종류 = читател_стойност.수('B')
            if 종류 == 1:
                стойност = 수정유티에프해독(читател_стойност.Четене(читател_стойност.수('H')))
            elif 종류 == 3:
                стойност = читател_стойност.수('i')
            elif 종류 == 4:
                стойност = читател_стойност.Четене(4)
            elif 종류 in (5, 6):
                стойност = читател_стойност.Четене(8)
            elif 종류 in (7, 8, 16):
                стойност = читател_стойност.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                стойност = (читател_стойност.수('H'), читател_стойност.수('H'))
            elif 종류 == 15:
                стойност = (читател_стойност.수('B'), читател_стойност.수('H'))
            else:
                raise грешка_при_компилиране('지원하지 않는 константа_стойност 종류: {}'.format(종류))
            자신.константа_стойност[индекс] = (종류, стойност)
            индекс += 2 if 종류 in (5, 6) else 1
        자신.достъп_запис = читател_стойност.수('H')
        자신.Име = 자신.име_на_клас(читател_стойност.수('H'))
        родител_стойност = читател_стойност.수('H')
        if 자신.име_на_клас(родител_стойност) != 'java/lang/Object' or читател_стойност.수('H') != 0:
            raise грешка_при_компилиране(자신.Име + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.стойност_на_поле = 자신.멤버읽기(читател_стойност)
        자신.функция_стойност = 자신.멤버읽기(читател_стойност)
        자신.속성읽기(читател_стойност)

    def 문자(자신, индекс):
        if 자신.константа_стойност[индекс][0] != 1:
            raise грешка_при_компилиране('низ_стойност константа_стойност формат_стойност ГРЕШКА')
        return 자신.константа_стойност[индекс][1]

    def име_на_клас(자신, индекс):
        return 자신.문자(자신.константа_стойност[индекс][1])

    def препратка(자신, индекс):
        собственик_стойност, препратка_към_клетка_формат = 자신.константа_стойност[индекс][1]
        Име, формат_стойност = 자신.константа_стойност[препратка_към_клетка_формат][1]
        return 자신.име_на_клас(собственик_стойност), 자신.문자(Име), 자신.문자(формат_стойност)

    def 속성읽기(자신, читател_стойност):
        РЕЗУЛТАТ = {}
        for _ in range(читател_стойност.수('H')):
            Име = 자신.문자(читател_стойност.수('H'))
            РЕЗУЛТАТ[Име] = читател_стойност.Четене(читател_стойност.수('I'))
        return РЕЗУЛТАТ

    def 멤버읽기(자신, читател_стойност):
        РЕЗУЛТАТ = []
        for _ in range(читател_стойност.수('H')):
            достъп_запис = читател_стойност.수('H')
            Име = 자신.문자(читател_стойност.수('H'))
            формат_стойност = 자신.문자(читател_стойност.수('H'))
            РЕЗУЛТАТ.append((достъп_запис, Име, формат_стойност, 자신.속성읽기(читател_стойност)))
        return РЕЗУЛТАТ


def 형식읽기(низ_стойност):
    РЕЗУЛТАТ = []
    Позиция = 0
    while Позиция < len(низ_стойност):
        for формат_стойност in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if низ_стойност.startswith(формат_стойност, Позиция):
                РЕЗУЛТАТ.append(формат_стойност)
                Позиция += len(формат_стойност)
                break
        else:
            raise грешка_при_компилиране('지원하지 않는 тип_на_данните: ' + низ_стойност)
    return РЕЗУЛТАТ


def 함수형식(서술):
    Параметри, връщам_мярка = 서술[1:].split(')')
    Параметри = 형식읽기(Параметри)
    връщам_Тип = 형식읽기(връщам_мярка)
    if 'V' in Параметри or len(връщам_Тип) != 1:
        raise грешка_при_компилиране('функция_стойност 서술 формат_стойност ГРЕШКА: ' + 서술)
    return Параметри, връщам_мярка


def символ(종류, *부분):
    ИЗТОЧНИК = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ИЗТОЧНИК).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 функция_стойност 서술에 대해서만 허용한다.
def изпълнявам_команда(Параметри=None):
    анализатор_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK източник_дърво компилация_система')
    анализатор_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    анализатор_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 добавям_запис JAR/Клас_стойност 디렉터리')
    анализатор_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 компилация_система JDK 또는 openjdk-build의 부트 JDK ПЪТ')
    анализатор_48ee4b1b.add_argument('--bundle-runtime', help='изпълнявам_команда 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    анализатор_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK програма_програма_за_стартиране/източник_дърво 빌드의 C компилатор')
    анализатор_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ компилатор')
    анализатор_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 компилация_система 작업 수')
    анализатор_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 компилация_система цел (예: aarch64-linux-gnu)')
    анализатор_48ee4b1b.add_argument('--sysroot', help='교차 компилация_система 대상의 libc/헤더/библиотека 루트')
    анализатор_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 формат_стойност')
    анализатор_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Клас_стойност.функция_стойност (자체 операнд_стек ABI)')
    анализатор_48ee4b1b.add_argument('--entry', help='예: 계산.Стартиране (openjdk-build 이외 대상에서 필수)')
    анализатор_48ee4b1b.add_argument('-o', '--output', required=True, help='изпълнявам_команда ELF/.o Изход; openjdk-build는 전용 компилация_система 디렉터리')
    анализатор_48ee4b1b.add_argument('sources', nargs='+')
    параметър_аргумент = анализатор_48ee4b1b.parse_args(Параметри)
    if параметър_аргумент.target == 'openjdk-build':
        if len(параметър_аргумент.sources) != 1 or not параметър_аргумент.java_home or параметър_аргумент.entry or параметър_аргумент.export or параметър_аргумент.classpath or параметър_аргумент.bundle_runtime:
            raise грешка_при_компилиране('openjdk-build: OpenJDK източник_дърво 디렉터리 하나와 --java-home 부트 JDK, -o компилация_система 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(параметър_аргумент.sources[0], параметър_аргумент.output, параметър_аргумент.java_home, параметър_аргумент.jobs, параметър_аргумент.openjdk_target,
                  параметър_аргумент.sysroot, None if параметър_аргумент.cc == 'cc' else параметър_аргумент.cc, параметър_аргумент.cxx, параметър_аргумент.configure_arg)
        except BuildError as ГРЕШКА:
            raise грешка_при_компилиране(str(ГРЕШКА))
        return
    if not параметър_аргумент.entry:
        анализатор_48ee4b1b.error('--entry is required for this target')
    if параметър_аргумент.cxx or параметър_аргумент.openjdk_target or параметър_аргумент.sysroot or параметър_аргумент.configure_arg or параметър_аргумент.jobs != 2:
        raise грешка_при_компилиране('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build цел 전용')
    if параметър_аргумент.target == 'openjdk':
        sys.modules.setdefault('компилатор', sys.modules[__name__])
        from 실행파일 import Създаване_запис
        Създаване_запис(параметър_аргумент)
        return
    if параметър_аргумент.classpath or параметър_аргумент.java_home or параметър_аргумент.bundle_runtime or параметър_аргумент.cc != 'cc':
        raise грешка_при_компилиране('classpath/java-home/bundle-runtime/cc 옵션은 openjdk цел 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', параметър_аргумент.target, '--entry', параметър_аргумент.entry, '-o', параметър_аргумент.output]
    for Възложи_стойност in параметър_аргумент.export: 자바명령.extend(['--export', Възложи_стойност])
    subprocess.run(자바명령+параметър_аргумент.sources, check=True)
    return


if __name__ == '__main__':
    try:
        изпълнявам_команда()
    except (грешка_при_компилиране, OSError, ValueError, subprocess.CalledProcessError) as ГРЕШКА:
        print('компилирам_източник ГРЕШКА: ' + str(ГРЕШКА), file=sys.stderr)
        sys.exit(1)
