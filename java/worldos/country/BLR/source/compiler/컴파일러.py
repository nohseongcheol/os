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
    def __init__(자신, дадзеныя):
        자신.дадзеныя = дадзеныя
        자신.Пазіцыя = 0

    def Чытанне(자신, даўжыня_значэнне):
        if даўжыня_значэнне < 0 or 자신.Пазіцыя + даўжыня_значэнне > len(자신.дадзеныя):
            raise 컴파일오류('잘린 клас_значэнне 또는 Загад дадзеныя')
        결과 = 자신.дадзеныя[자신.Пазіцыя:자신.Пазіцыя + даўжыня_значэнне]
        자신.Пазіцыя += даўжыня_значэнне
        return 결과

    def 수(자신, фармат_значэнне):
        return struct.unpack('>' + фармат_значэнне, 자신.Чытанне(struct.calcsize('>' + фармат_значэнне)))[0]


def 수정유티에프해독(дадзеныя):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    радок_значэнне = дадзеныя.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return радок_значэнне.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class клас_значэнне:
    def __init__(자신, ШЛЯХ):
        자신.ШЛЯХ = ШЛЯХ
        чытач_значэнне = 자료읽기(ШЛЯХ.read_bytes())
        if чытач_значэнне.수('I') != 0xcafebabe:
            raise 컴파일오류('Java клас_значэнне 표식이 아님')
        чытач_значэнне.Чытанне(4)
        개수 = чытач_значэнне.수('H')
        자신.канстанта_значэнне = [None] * 개수
        індэкс = 1
        while індэкс < 개수:
            종류 = чытач_значэнне.수('B')
            if 종류 == 1:
                значэнне = 수정유티에프해독(чытач_значэнне.Чытанне(чытач_значэнне.수('H')))
            elif 종류 == 3:
                значэнне = чытач_значэнне.수('i')
            elif 종류 == 4:
                значэнне = чытач_значэнне.Чытанне(4)
            elif 종류 in (5, 6):
                значэнне = чытач_значэнне.Чытанне(8)
            elif 종류 in (7, 8, 16):
                значэнне = чытач_значэнне.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                значэнне = (чытач_значэнне.수('H'), чытач_значэнне.수('H'))
            elif 종류 == 15:
                значэнне = (чытач_значэнне.수('B'), чытач_значэнне.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 канстанта_значэнне 종류: {}'.format(종류))
            자신.канстанта_значэнне[індэкс] = (종류, значэнне)
            індэкс += 2 if 종류 in (5, 6) else 1
        자신.доступ_увядзенне = чытач_значэнне.수('H')
        자신.Назва = 자신.клас_імя(чытач_значэнне.수('H'))
        부모 = чытач_значэнне.수('H')
        if 자신.клас_імя(부모) != 'java/lang/Object' or чытач_значэнне.수('H') != 0:
            raise 컴파일오류(자신.Назва + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.поле_значэнне = 자신.멤버읽기(чытач_значэнне)
        자신.функцыя_значэнне = 자신.멤버읽기(чытач_значэнне)
        자신.속성읽기(чытач_значэнне)

    def 문자(자신, індэкс):
        if 자신.канстанта_значэнне[індэкс][0] != 1:
            raise 컴파일오류('радок_значэнне канстанта_значэнне фармат_значэнне ПАМЫЛКА')
        return 자신.канстанта_значэнне[індэкс][1]

    def клас_імя(자신, індэкс):
        return 자신.문자(자신.канстанта_значэнне[індэкс][1])

    def Даведачныя_матэрыялы(자신, індэкс):
        уласнік_значэнне, імя_фармат = 자신.канстанта_значэнне[індэкс][1]
        Назва, фармат_значэнне = 자신.канстанта_значэнне[імя_фармат][1]
        return 자신.клас_імя(уласнік_значэнне), 자신.문자(Назва), 자신.문자(фармат_значэнне)

    def 속성읽기(자신, чытач_значэнне):
        결과 = {}
        for _ in range(чытач_значэнне.수('H')):
            Назва = 자신.문자(чытач_значэнне.수('H'))
            결과[Назва] = чытач_значэнне.Чытанне(чытач_значэнне.수('I'))
        return 결과

    def 멤버읽기(자신, чытач_значэнне):
        결과 = []
        for _ in range(чытач_значэнне.수('H')):
            доступ_увядзенне = чытач_значэнне.수('H')
            Назва = 자신.문자(чытач_значэнне.수('H'))
            фармат_значэнне = 자신.문자(чытач_значэнне.수('H'))
            결과.append((доступ_увядзенне, Назва, фармат_значэнне, 자신.속성읽기(чытач_значэнне)))
        return 결과


def 형식읽기(радок_значэнне):
    결과 = []
    Пазіцыя = 0
    while Пазіцыя < len(радок_значэнне):
        for фармат_значэнне in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if радок_значэнне.startswith(фармат_значэнне, Пазіцыя):
                결과.append(фармат_значэнне)
                Пазіцыя += len(фармат_значэнне)
                break
        else:
            raise 컴파일오류('지원하지 않는 тып_дадзеных: ' + радок_значэнне)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('функцыя_значэнне 서술 фармат_значэнне ПАМЫЛКА: ' + 서술)
    return 인수, 반환


def сімвал(종류, *부분):
    КРЫНІЦА = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(КРЫНІЦА).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 функцыя_значэнне 서술에 대해서만 허용한다.
def выканаць_каманда(인수=None):
    аналізатар_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK крыніца_дрэва зборка_сістэма')
    аналізатар_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    аналізатар_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/клас_значэнне 디렉터리')
    аналізатар_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 зборка_сістэма JDK 또는 openjdk-build의 부트 JDK ШЛЯХ')
    аналізатар_48ee4b1b.add_argument('--bundle-runtime', help='выканаць_каманда 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    аналізатар_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK праграма_выклік_праграм/крыніца_дрэва 빌드의 C 컴파일러')
    аналізатар_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    аналізатар_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 зборка_сістэма 작업 수')
    аналізатар_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 зборка_сістэма мэтавы_паказчык (예: aarch64-linux-gnu)')
    аналізатар_48ee4b1b.add_argument('--sysroot', help='교차 зборка_сістэма 대상의 libc/헤더/бібліятэка 루트')
    аналізатар_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 фармат_значэнне')
    аналізатар_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=клас_значэнне.функцыя_значэнне (자체 스택 ABI)')
    аналізатар_48ee4b1b.add_argument('--entry', help='예: 계산.Выканаць (openjdk-build 이외 대상에서 필수)')
    аналізатар_48ee4b1b.add_argument('-o', '--output', required=True, help='выканаць_каманда ELF/.o Выхад; openjdk-build는 전용 зборка_сістэма 디렉터리')
    аналізатар_48ee4b1b.add_argument('sources', nargs='+')
    параметр_аргумент = аналізатар_48ee4b1b.parse_args(인수)
    if параметр_аргумент.target == 'openjdk-build':
        if len(параметр_аргумент.sources) != 1 or not параметр_аргумент.java_home or параметр_аргумент.entry or параметр_аргумент.export or параметр_аргумент.classpath or параметр_аргумент.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK крыніца_дрэва 디렉터리 하나와 --java-home 부트 JDK, -o зборка_сістэма 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(параметр_аргумент.sources[0], параметр_аргумент.output, параметр_аргумент.java_home, параметр_аргумент.jobs, параметр_аргумент.openjdk_target,
                  параметр_аргумент.sysroot, None if параметр_аргумент.cc == 'cc' else параметр_аргумент.cc, параметр_аргумент.cxx, параметр_аргумент.configure_arg)
        except BuildError as ПАМЫЛКА:
            raise 컴파일오류(str(ПАМЫЛКА))
        return
    if not параметр_аргумент.entry:
        аналізатар_48ee4b1b.error('--entry is required for this target')
    if параметр_аргумент.cxx or параметр_аргумент.openjdk_target or параметр_аргумент.sysroot or параметр_аргумент.configure_arg or параметр_аргумент.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build мэтавы_паказчык 전용')
    if параметр_аргумент.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import стварыць_увядзенне
        стварыць_увядзенне(параметр_аргумент)
        return
    if параметр_аргумент.classpath or параметр_аргумент.java_home or параметр_аргумент.bundle_runtime or параметр_аргумент.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk мэтавы_паказчык 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', параметр_аргумент.target, '--entry', параметр_аргумент.entry, '-o', параметр_аргумент.output]
    for прызначыць_значэнне in параметр_аргумент.export: 자바명령.extend(['--export', прызначыць_значэнне])
    subprocess.run(자바명령+параметр_аргумент.sources, check=True)
    return


if __name__ == '__main__':
    try:
        выканаць_каманда()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ПАМЫЛКА:
        print('будаваць_крыніца ПАМЫЛКА: ' + str(ПАМЫЛКА), file=sys.stderr)
        sys.exit(1)
