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


class ошибка_компиляции(Exception):
    pass


class чтение_данные:
    def __init__(자신, данные):
        자신.данные = данные
        자신.позиция = 0

    def Чтение(자신, длина_ЗНАЧЕН):
        if длина_ЗНАЧЕН < 0 or 자신.позиция + длина_ЗНАЧЕН > len(자신.данные):
            raise ошибка_компиляции('잘린 Класс_ЗНАЧЕН 또는 команда данные')
        результат = 자신.данные[자신.позиция:자신.позиция + длина_ЗНАЧЕН]
        자신.позиция += длина_ЗНАЧЕН
        return результат

    def 수(자신, формат_ЗНАЧЕН):
        return struct.unpack('>' + формат_ЗНАЧЕН, 자신.Чтение(struct.calcsize('>' + формат_ЗНАЧЕН)))[0]


def 수정유티에프해독(данные):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    строка_ЗНАЧЕН = данные.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return строка_ЗНАЧЕН.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Класс_ЗНАЧЕН:
    def __init__(자신, путь):
        자신.путь = путь
        Ридер_ЗНАЧЕН = чтение_данные(путь.read_bytes())
        if Ридер_ЗНАЧЕН.수('I') != 0xcafebabe:
            raise ошибка_компиляции('Java Класс_ЗНАЧЕН 표식이 아님')
        Ридер_ЗНАЧЕН.Чтение(4)
        товар_СЧЁТ = Ридер_ЗНАЧЕН.수('H')
        자신.константа_ЗНАЧЕН = [None] * товар_СЧЁТ
        ИНДЕКС = 1
        while ИНДЕКС < товар_СЧЁТ:
            Вид_ЗНАЧЕН = Ридер_ЗНАЧЕН.수('B')
            if Вид_ЗНАЧЕН == 1:
                ЗНАЧЕН = 수정유티에프해독(Ридер_ЗНАЧЕН.Чтение(Ридер_ЗНАЧЕН.수('H')))
            elif Вид_ЗНАЧЕН == 3:
                ЗНАЧЕН = Ридер_ЗНАЧЕН.수('i')
            elif Вид_ЗНАЧЕН == 4:
                ЗНАЧЕН = Ридер_ЗНАЧЕН.Чтение(4)
            elif Вид_ЗНАЧЕН in (5, 6):
                ЗНАЧЕН = Ридер_ЗНАЧЕН.Чтение(8)
            elif Вид_ЗНАЧЕН in (7, 8, 16):
                ЗНАЧЕН = Ридер_ЗНАЧЕН.수('H')
            elif Вид_ЗНАЧЕН in (9, 10, 11, 12, 18):
                ЗНАЧЕН = (Ридер_ЗНАЧЕН.수('H'), Ридер_ЗНАЧЕН.수('H'))
            elif Вид_ЗНАЧЕН == 15:
                ЗНАЧЕН = (Ридер_ЗНАЧЕН.수('B'), Ридер_ЗНАЧЕН.수('H'))
            else:
                raise ошибка_компиляции('지원하지 않는 константа_ЗНАЧЕН Вид_ЗНАЧЕН: {}'.format(Вид_ЗНАЧЕН))
            자신.константа_ЗНАЧЕН[ИНДЕКС] = (Вид_ЗНАЧЕН, ЗНАЧЕН)
            ИНДЕКС += 2 if Вид_ЗНАЧЕН in (5, 6) else 1
        자신.доступ_ввод = Ридер_ЗНАЧЕН.수('H')
        자신.Название = 자신.имя_класса(Ридер_ЗНАЧЕН.수('H'))
        родительский_ЗНАЧЕН = Ридер_ЗНАЧЕН.수('H')
        if 자신.имя_класса(родительский_ЗНАЧЕН) != 'java/lang/Object' or Ридер_ЗНАЧЕН.수('H') != 0:
            raise ошибка_компиляции(자신.Название + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.значение_поля = 자신.멤버읽기(Ридер_ЗНАЧЕН)
        자신.ФУНКЦИЯ_ЗНАЧЕН = 자신.멤버읽기(Ридер_ЗНАЧЕН)
        자신.чтение_атрибуты(Ридер_ЗНАЧЕН)

    def 문자(자신, ИНДЕКС):
        if 자신.константа_ЗНАЧЕН[ИНДЕКС][0] != 1:
            raise ошибка_компиляции('строка_ЗНАЧЕН константа_ЗНАЧЕН формат_ЗНАЧЕН ошибка')
        return 자신.константа_ЗНАЧЕН[ИНДЕКС][1]

    def имя_класса(자신, ИНДЕКС):
        return 자신.문자(자신.константа_ЗНАЧЕН[ИНДЕКС][1])

    def ссылка(자신, ИНДЕКС):
        владелец_ЗНАЧЕН, имя_формат = 자신.константа_ЗНАЧЕН[ИНДЕКС][1]
        Название, формат_ЗНАЧЕН = 자신.константа_ЗНАЧЕН[имя_формат][1]
        return 자신.имя_класса(владелец_ЗНАЧЕН), 자신.문자(Название), 자신.문자(формат_ЗНАЧЕН)

    def чтение_атрибуты(자신, Ридер_ЗНАЧЕН):
        результат = {}
        for _ in range(Ридер_ЗНАЧЕН.수('H')):
            Название = 자신.문자(Ридер_ЗНАЧЕН.수('H'))
            результат[Название] = Ридер_ЗНАЧЕН.Чтение(Ридер_ЗНАЧЕН.수('I'))
        return результат

    def 멤버읽기(자신, Ридер_ЗНАЧЕН):
        результат = []
        for _ in range(Ридер_ЗНАЧЕН.수('H')):
            доступ_ввод = Ридер_ЗНАЧЕН.수('H')
            Название = 자신.문자(Ридер_ЗНАЧЕН.수('H'))
            формат_ЗНАЧЕН = 자신.문자(Ридер_ЗНАЧЕН.수('H'))
            результат.append((доступ_ввод, Название, формат_ЗНАЧЕН, 자신.чтение_атрибуты(Ридер_ЗНАЧЕН)))
        return результат


def 형식읽기(строка_ЗНАЧЕН):
    результат = []
    позиция = 0
    while позиция < len(строка_ЗНАЧЕН):
        for формат_ЗНАЧЕН in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if строка_ЗНАЧЕН.startswith(формат_ЗНАЧЕН, позиция):
                результат.append(формат_ЗНАЧЕН)
                позиция += len(формат_ЗНАЧЕН)
                break
        else:
            raise ошибка_компиляции('지원하지 않는 тип_данных: ' + строка_ЗНАЧЕН)
    return результат


def метод_дескриптор(описание_ЗНАЧЕН):
    аргументы, Возврат_KR = описание_ЗНАЧЕН[1:].split(')')
    аргументы = 형식읽기(аргументы)
    тип_возвращаемого_значения = 형식읽기(Возврат_KR)
    if 'V' in аргументы or len(тип_возвращаемого_значения) != 1:
        raise ошибка_компиляции('ФУНКЦИЯ_ЗНАЧЕН описание_ЗНАЧЕН формат_ЗНАЧЕН ошибка: ' + описание_ЗНАЧЕН)
    return аргументы, Возврат_KR


def символ(Вид_ЗНАЧЕН, *부분):
    исходныйКод = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(Вид_ЗНАЧЕН, hashlib.sha256(исходныйКод).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ФУНКЦИЯ_ЗНАЧЕН 서술에 대해서만 허용한다.
def 실행(аргументы=None):
    анализатор_48ee4b1b = argparse.ArgumentParser(description='свой Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK источник_дерево сборка')
    анализатор_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    анализатор_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 добавить_ввод JAR/Класс_ЗНАЧЕН 디렉터리')
    анализатор_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 сборка JDK 또는 openjdk-build의 부트 JDK путь')
    анализатор_48ee4b1b.add_argument('--bundle-runtime', help='실행 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    анализатор_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK программа_Launcher/источник_дерево 빌드의 C компилятор')
    анализатор_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ компилятор')
    анализатор_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 сборка 작업 수')
    анализатор_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 сборка целевое_значение (예: aarch64-linux-gnu)')
    анализатор_48ee4b1b.add_argument('--sysroot', help='교차 сборка 대상의 libc/헤더/библиотека 루트')
    анализатор_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 формат_ЗНАЧЕН')
    анализатор_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Класс_ЗНАЧЕН.ФУНКЦИЯ_ЗНАЧЕН (свой операнд_стек ABI)')
    анализатор_48ee4b1b.add_argument('--entry', help='예: 계산.запустить (openjdk-build 이외 대상에서 필수)')
    анализатор_48ee4b1b.add_argument('-o', '--output', required=True, help='실행 ELF/.o текстовыйВывод; openjdk-build는 전용 сборка 디렉터리')
    анализатор_48ee4b1b.add_argument('sources', nargs='+')
    параметр_аргумент = анализатор_48ee4b1b.parse_args(аргументы)
    if параметр_аргумент.target == 'openjdk-build':
        if len(параметр_аргумент.sources) != 1 or not параметр_аргумент.java_home or параметр_аргумент.entry or параметр_аргумент.export or параметр_аргумент.classpath or параметр_аргумент.bundle_runtime:
            raise ошибка_компиляции('openjdk-build: OpenJDK источник_дерево 디렉터리 하나와 --java-home 부트 JDK, -o сборка 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(параметр_аргумент.sources[0], параметр_аргумент.output, параметр_аргумент.java_home, параметр_аргумент.jobs, параметр_аргумент.openjdk_target,
                  параметр_аргумент.sysroot, None if параметр_аргумент.cc == 'cc' else параметр_аргумент.cc, параметр_аргумент.cxx, параметр_аргумент.configure_arg)
        except BuildError as ошибка:
            raise ошибка_компиляции(str(ошибка))
        return
    if not параметр_аргумент.entry:
        анализатор_48ee4b1b.error('--entry is required for this target')
    if параметр_аргумент.cxx or параметр_аргумент.openjdk_target or параметр_аргумент.sysroot or параметр_аргумент.configure_arg or параметр_аргумент.jobs != 2:
        raise ошибка_компиляции('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build целевое_значение 전용')
    if параметр_аргумент.target == 'openjdk':
        sys.modules.setdefault('компилятор', sys.modules[__name__])
        from исполняемый_файл import Create_ввод
        Create_ввод(параметр_аргумент)
        return
    if параметр_аргумент.classpath or параметр_аргумент.java_home or параметр_аргумент.bundle_runtime or параметр_аргумент.cc != 'cc':
        raise ошибка_компиляции('classpath/java-home/bundle-runtime/cc 옵션은 openjdk целевое_значение 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', параметр_аргумент.target, '--entry', параметр_аргумент.entry, '-o', параметр_аргумент.output]
    for Назначить_ЗНАЧЕН in параметр_аргумент.export: 자바명령.extend(['--export', Назначить_ЗНАЧЕН])
    subprocess.run(자바명령+параметр_аргумент.sources, check=True)
    return


if __name__ == '__main__':
    try:
        실행()
    except (ошибка_компиляции, OSError, ValueError, subprocess.CalledProcessError) as ошибка:
        print('компилировать_источник ошибка: ' + str(ошибка), file=sys.stderr)
        sys.exit(1)
