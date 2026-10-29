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


class помилка_компіляції(Exception):
    pass


class 자료읽기:
    def __init__(자신, дані):
        자신.дані = дані
        자신.позиція = 0

    def Читання(자신, 길이):
        if 길이 < 0 or 자신.позиція + 길이 > len(자신.дані):
            raise помилка_компіляції('잘린 Клас_значення 또는 команда дані')
        результат = 자신.дані[자신.позиція:자신.позиція + 길이]
        자신.позиція += 길이
        return результат

    def 수(자신, формат_значення):
        return struct.unpack('>' + формат_значення, 자신.Читання(struct.calcsize('>' + формат_значення)))[0]


def 수정유티에프해독(дані):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    рядок_значення = дані.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return рядок_значення.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Клас_значення:
    def __init__(자신, шлях):
        자신.шлях = шлях
        читач_значення = 자료읽기(шлях.read_bytes())
        if читач_значення.수('I') != 0xcafebabe:
            raise помилка_компіляції('Java Клас_значення 표식이 아님')
        читач_значення.Читання(4)
        개수 = читач_значення.수('H')
        자신.константа_значення = [None] * 개수
        індекс = 1
        while індекс < 개수:
            종류 = читач_значення.수('B')
            if 종류 == 1:
                значення = 수정유티에프해독(читач_значення.Читання(читач_значення.수('H')))
            elif 종류 == 3:
                значення = читач_значення.수('i')
            elif 종류 == 4:
                значення = читач_значення.Читання(4)
            elif 종류 in (5, 6):
                значення = читач_значення.Читання(8)
            elif 종류 in (7, 8, 16):
                значення = читач_значення.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                значення = (читач_значення.수('H'), читач_значення.수('H'))
            elif 종류 == 15:
                значення = (читач_значення.수('B'), читач_значення.수('H'))
            else:
                raise помилка_компіляції('지원하지 않는 константа_значення 종류: {}'.format(종류))
            자신.константа_значення[індекс] = (종류, значення)
            індекс += 2 if 종류 in (5, 6) else 1
        자신.доступ_запис = читач_значення.수('H')
        자신.Назва = 자신.ім_я_класу(читач_значення.수('H'))
        батьківський_значення = читач_значення.수('H')
        if 자신.ім_я_класу(батьківський_значення) != 'java/lang/Object' or читач_значення.수('H') != 0:
            raise помилка_компіляції(자신.Назва + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.значення_поля = 자신.멤버읽기(читач_значення)
        자신.функція_значення = 자신.멤버읽기(читач_значення)
        자신.속성읽기(читач_значення)

    def 문자(자신, індекс):
        if 자신.константа_значення[індекс][0] != 1:
            raise помилка_компіляції('рядок_значення константа_значення формат_значення ПОМИЛКА')
        return 자신.константа_значення[індекс][1]

    def ім_я_класу(자신, індекс):
        return 자신.문자(자신.константа_значення[індекс][1])

    def довідка(자신, індекс):
        власник_значення, ім_я_формат = 자신.константа_значення[індекс][1]
        Назва, формат_значення = 자신.константа_значення[ім_я_формат][1]
        return 자신.ім_я_класу(власник_значення), 자신.문자(Назва), 자신.문자(формат_значення)

    def 속성읽기(자신, читач_значення):
        результат = {}
        for _ in range(читач_значення.수('H')):
            Назва = 자신.문자(читач_значення.수('H'))
            результат[Назва] = читач_значення.Читання(читач_значення.수('I'))
        return результат

    def 멤버읽기(자신, читач_значення):
        результат = []
        for _ in range(читач_значення.수('H')):
            доступ_запис = читач_значення.수('H')
            Назва = 자신.문자(читач_значення.수('H'))
            формат_значення = 자신.문자(читач_значення.수('H'))
            результат.append((доступ_запис, Назва, формат_значення, 자신.속성읽기(читач_значення)))
        return результат


def 형식읽기(рядок_значення):
    результат = []
    позиція = 0
    while позиція < len(рядок_значення):
        for формат_значення in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if рядок_значення.startswith(формат_значення, позиція):
                результат.append(формат_значення)
                позиція += len(формат_значення)
                break
        else:
            raise помилка_компіляції('지원하지 않는 тип_даних: ' + рядок_значення)
    return результат


def 함수형식(서술):
    аргументи, повернути_КР = 서술[1:].split(')')
    аргументи = 형식읽기(аргументи)
    повернути_Тип = 형식읽기(повернути_КР)
    if 'V' in аргументи or len(повернути_Тип) != 1:
        raise помилка_компіляції('функція_значення 서술 формат_значення ПОМИЛКА: ' + 서술)
    return аргументи, повернути_КР


def символ(종류, *부분):
    вихіднийКод = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(вихіднийКод).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 функція_значення 서술에 대해서만 허용한다.
def Виконати_команда(аргументи=None):
    аналізатор_48ee4b1b = argparse.ArgumentParser(description='своє Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK джерело_дерево збирання')
    аналізатор_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    аналізатор_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 додавати_запис JAR/Клас_значення 디렉터리')
    аналізатор_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 збирання JDK 또는 openjdk-build의 부트 JDK шлях')
    аналізатор_48ee4b1b.add_argument('--bundle-runtime', help='Виконати_команда 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    аналізатор_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK програма_запускач/джерело_дерево 빌드의 C компілятор')
    аналізатор_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ компілятор')
    аналізатор_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 збирання 작업 수')
    аналізатор_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 збирання мета (예: aarch64-linux-gnu)')
    аналізатор_48ee4b1b.add_argument('--sysroot', help='교차 збирання 대상의 libc/헤더/бібліотека 루트')
    аналізатор_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 формат_значення')
    аналізатор_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Клас_значення.функція_значення (своє операнд_Стіс ABI)')
    аналізатор_48ee4b1b.add_argument('--entry', help='예: 계산.запустити (openjdk-build 이외 대상에서 필수)')
    аналізатор_48ee4b1b.add_argument('-o', '--output', required=True, help='Виконати_команда ELF/.o Вивід; openjdk-build는 전용 збирання 디렉터리')
    аналізатор_48ee4b1b.add_argument('sources', nargs='+')
    параметр_аргумент = аналізатор_48ee4b1b.parse_args(аргументи)
    if параметр_аргумент.target == 'openjdk-build':
        if len(параметр_аргумент.sources) != 1 or not параметр_аргумент.java_home or параметр_аргумент.entry or параметр_аргумент.export or параметр_аргумент.classpath or параметр_аргумент.bundle_runtime:
            raise помилка_компіляції('openjdk-build: OpenJDK джерело_дерево 디렉터리 하나와 --java-home 부트 JDK, -o збирання 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(параметр_аргумент.sources[0], параметр_аргумент.output, параметр_аргумент.java_home, параметр_аргумент.jobs, параметр_аргумент.openjdk_target,
                  параметр_аргумент.sysroot, None if параметр_аргумент.cc == 'cc' else параметр_аргумент.cc, параметр_аргумент.cxx, параметр_аргумент.configure_arg)
        except BuildError as ПОМИЛКА:
            raise помилка_компіляції(str(ПОМИЛКА))
        return
    if not параметр_аргумент.entry:
        аналізатор_48ee4b1b.error('--entry is required for this target')
    if параметр_аргумент.cxx or параметр_аргумент.openjdk_target or параметр_аргумент.sysroot or параметр_аргумент.configure_arg or параметр_аргумент.jobs != 2:
        raise помилка_компіляції('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build мета 전용')
    if параметр_аргумент.target == 'openjdk':
        sys.modules.setdefault('компілятор', sys.modules[__name__])
        from 실행파일 import Створення_запис
        Створення_запис(параметр_аргумент)
        return
    if параметр_аргумент.classpath or параметр_аргумент.java_home or параметр_аргумент.bundle_runtime or параметр_аргумент.cc != 'cc':
        raise помилка_компіляції('classpath/java-home/bundle-runtime/cc 옵션은 openjdk мета 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', параметр_аргумент.target, '--entry', параметр_аргумент.entry, '-o', параметр_аргумент.output]
    for Призначити_значення in параметр_аргумент.export: 자바명령.extend(['--export', Призначити_значення])
    subprocess.run(자바명령+параметр_аргумент.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Виконати_команда()
    except (помилка_компіляції, OSError, ValueError, subprocess.CalledProcessError) as ПОМИЛКА:
        print('компілювати_джерело ПОМИЛКА: ' + str(ПОМИЛКА), file=sys.stderr)
        sys.exit(1)
