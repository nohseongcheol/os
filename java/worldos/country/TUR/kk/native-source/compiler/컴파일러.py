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


class құрастыру_қатесі(Exception):
    pass


class 자료읽기:
    def __init__(자신, деректер):
        자신.деректер = деректер
        자신.Орны = 0

    def Оқу(자신, ұзындық_мән):
        if ұзындық_мән < 0 or 자신.Орны + ұзындық_мән > len(자신.деректер):
            raise құрастыру_қатесі('잘린 оқу_мән 또는 Команда деректер')
        НӘТИЖЕ = 자신.деректер[자신.Орны:자신.Орны + ұзындық_мән]
        자신.Орны += ұзындық_мән
        return НӘТИЖЕ

    def 수(자신, пішім_мән):
        return struct.unpack('>' + пішім_мән, 자신.Оқу(struct.calcsize('>' + пішім_мән)))[0]


def 수정유티에프해독(деректер):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    жол_мән_6ca8363c = деректер.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return жол_мән_6ca8363c.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class оқу_мән:
    def __init__(자신, Жол_2):
        자신.Жол_2 = Жол_2
        оқушы_мән = 자료읽기(Жол_2.read_bytes())
        if оқушы_мән.수('I') != 0xcafebabe:
            raise құрастыру_қатесі('Java оқу_мән 표식이 아님')
        оқушы_мән.Оқу(4)
        개수 = оқушы_мән.수('H')
        자신.тұрақты_мән_мән = [None] * 개수
        индекс = 1
        while индекс < 개수:
            종류 = оқушы_мән.수('B')
            if 종류 == 1:
                мән = 수정유티에프해독(оқушы_мән.Оқу(оқушы_мән.수('H')))
            elif 종류 == 3:
                мән = оқушы_мән.수('i')
            elif 종류 == 4:
                мән = оқушы_мән.Оқу(4)
            elif 종류 in (5, 6):
                мән = оқушы_мән.Оқу(8)
            elif 종류 in (7, 8, 16):
                мән = оқушы_мән.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                мән = (оқушы_мән.수('H'), оқушы_мән.수('H'))
            elif 종류 == 15:
                мән = (оқушы_мән.수('B'), оқушы_мән.수('H'))
            else:
                raise құрастыру_қатесі('지원하지 않는 тұрақты_мән_мән 종류: {}'.format(종류))
            자신.тұрақты_мән_мән[индекс] = (종류, мән)
            индекс += 2 if 종류 in (5, 6) else 1
        자신.қатынас_енгізу = оқушы_мән.수('H')
        자신.Аты = 자신.Класс_атауы(оқушы_мән.수('H'))
        басты_мән = оқушы_мән.수('H')
        if 자신.Класс_атауы(басты_мән) != 'java/lang/Object' or оқушы_мән.수('H') != 0:
            raise құрастыру_қатесі(자신.Аты + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.өріс_мәні = 자신.멤버읽기(оқушы_мән)
        자신.функция_мән = 자신.멤버읽기(оқушы_мән)
        자신.속성읽기(оқушы_мән)

    def 문자(자신, индекс):
        if 자신.тұрақты_мән_мән[индекс][0] != 1:
            raise құрастыру_қатесі('жол_мән_6ca8363c тұрақты_мән_мән пішім_мән Қате')
        return 자신.тұрақты_мән_мән[индекс][1]

    def Класс_атауы(자신, индекс):
        return 자신.문자(자신.тұрақты_мән_мән[индекс][1])

    def Анықтамалық(자신, индекс):
        ие_мән, аты_пішім = 자신.тұрақты_мән_мән[индекс][1]
        Аты, пішім_мән = 자신.тұрақты_мән_мән[аты_пішім][1]
        return 자신.Класс_атауы(ие_мән), 자신.문자(Аты), 자신.문자(пішім_мән)

    def 속성읽기(자신, оқушы_мән):
        НӘТИЖЕ = {}
        for _ in range(оқушы_мән.수('H')):
            Аты = 자신.문자(оқушы_мән.수('H'))
            НӘТИЖЕ[Аты] = оқушы_мән.Оқу(оқушы_мән.수('I'))
        return НӘТИЖЕ

    def 멤버읽기(자신, оқушы_мән):
        НӘТИЖЕ = []
        for _ in range(оқушы_мән.수('H')):
            қатынас_енгізу = оқушы_мән.수('H')
            Аты = 자신.문자(оқушы_мән.수('H'))
            пішім_мән = 자신.문자(оқушы_мән.수('H'))
            НӘТИЖЕ.append((қатынас_енгізу, Аты, пішім_мән, 자신.속성읽기(оқушы_мән)))
        return НӘТИЖЕ


def 형식읽기(жол_мән_6ca8363c):
    НӘТИЖЕ = []
    Орны = 0
    while Орны < len(жол_мән_6ca8363c):
        for пішім_мән in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if жол_мән_6ca8363c.startswith(пішім_мән, Орны):
                НӘТИЖЕ.append(пішім_мән)
                Орны += len(пішім_мән)
                break
        else:
            raise құрастыру_қатесі('지원하지 않는 деректер_түрі: ' + жол_мән_6ca8363c)
    return НӘТИЖЕ


def 함수형식(서술):
    Аргументтер, қайтару_өлшем = 서술[1:].split(')')
    Аргументтер = 형식읽기(Аргументтер)
    қайтару_Түрі = 형식읽기(қайтару_өлшем)
    if 'V' in Аргументтер or len(қайтару_Түрі) != 1:
        raise құрастыру_қатесі('функция_мән 서술 пішім_мән Қате: ' + 서술)
    return Аргументтер, қайтару_өлшем


def символ(종류, *부분):
    Неден = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Неден).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 функция_мән 서술에 대해서만 허용한다.
def орындау_пәрмен(Аргументтер=None):
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK көз_дарақ құрастыру_жүйе')
    талдау_құралы_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    талдау_құралы_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 қосу_енгізу JAR/оқу_мән 디렉터리')
    талдау_құралы_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 құрастыру_жүйе JDK 또는 openjdk-build의 부트 JDK Жол_2')
    талдау_құралы_48ee4b1b.add_argument('--bundle-runtime', help='орындау_пәрмен 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    талдау_құралы_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK бағдарлама_іске_қосу_құралы/көз_дарақ 빌드의 C 컴파일러')
    талдау_құралы_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    талдау_құралы_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 құрастыру_жүйе 작업 수')
    талдау_құралы_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 құрастыру_жүйе мақсатты_мән (예: aarch64-linux-gnu)')
    талдау_құралы_48ee4b1b.add_argument('--sysroot', help='교차 құрастыру_жүйе 대상의 libc/헤더/кітапхана 루트')
    талдау_құралы_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 пішім_мән')
    талдау_құралы_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=оқу_мән.функция_мән (자체 операнд_Бума ABI)')
    талдау_құралы_48ee4b1b.add_argument('--entry', help='예: 계산.Орындау_2 (openjdk-build 이외 대상에서 필수)')
    талдау_құралы_48ee4b1b.add_argument('-o', '--output', required=True, help='орындау_пәрмен ELF/.o Шығысы; openjdk-build는 전용 құрастыру_жүйе 디렉터리')
    талдау_құралы_48ee4b1b.add_argument('sources', nargs='+')
    параметр_аргумент = талдау_құралы_48ee4b1b.parse_args(Аргументтер)
    if параметр_аргумент.target == 'openjdk-build':
        if len(параметр_аргумент.sources) != 1 or not параметр_аргумент.java_home or параметр_аргумент.entry or параметр_аргумент.export or параметр_аргумент.classpath or параметр_аргумент.bundle_runtime:
            raise құрастыру_қатесі('openjdk-build: OpenJDK көз_дарақ 디렉터리 하나와 --java-home 부트 JDK, -o құрастыру_жүйе 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(параметр_аргумент.sources[0], параметр_аргумент.output, параметр_аргумент.java_home, параметр_аргумент.jobs, параметр_аргумент.openjdk_target,
                  параметр_аргумент.sysroot, None if параметр_аргумент.cc == 'cc' else параметр_аргумент.cc, параметр_аргумент.cxx, параметр_аргумент.configure_arg)
        except BuildError as Қате:
            raise құрастыру_қатесі(str(Қате))
        return
    if not параметр_аргумент.entry:
        талдау_құралы_48ee4b1b.error('--entry is required for this target')
    if параметр_аргумент.cxx or параметр_аргумент.openjdk_target or параметр_аргумент.sysroot or параметр_аргумент.configure_arg or параметр_аргумент.jobs != 2:
        raise құрастыру_қатесі('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build мақсатты_мән 전용')
    if параметр_аргумент.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import жасау_енгізу
        жасау_енгізу(параметр_аргумент)
        return
    if параметр_аргумент.classpath or параметр_аргумент.java_home or параметр_аргумент.bundle_runtime or параметр_аргумент.cc != 'cc':
        raise құрастыру_қатесі('classpath/java-home/bundle-runtime/cc 옵션은 openjdk мақсатты_мән 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', параметр_аргумент.target, '--entry', параметр_аргумент.entry, '-o', параметр_аргумент.output]
    for белгілеу_мән in параметр_аргумент.export: 자바명령.extend(['--export', белгілеу_мән])
    subprocess.run(자바명령+параметр_аргумент.sources, check=True)
    return


if __name__ == '__main__':
    try:
        орындау_пәрмен()
    except (құрастыру_қатесі, OSError, ValueError, subprocess.CalledProcessError) as Қате:
        print('құрастыру_көз Қате: ' + str(Қате), file=sys.stderr)
        sys.exit(1)
