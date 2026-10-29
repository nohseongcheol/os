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
    def __init__(자신, Daten):
        자신.Daten = Daten
        자신.positionéieren = 0

    def 읽기(자신, Längt_VALUE):
        if Längt_VALUE < 0 or 자신.positionéieren + Längt_VALUE > len(자신.Daten):
            raise 컴파일오류('잘린 Klass_VALUE 또는 Befeel Daten')
        Mooss = 자신.Daten[자신.positionéieren:자신.positionéieren + Längt_VALUE]
        자신.positionéieren += Längt_VALUE
        return Mooss

    def 수(자신, Format_VALUE):
        return struct.unpack('>' + Format_VALUE, 자신.읽기(struct.calcsize('>' + Format_VALUE)))[0]


def 수정유티에프해독(Daten):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    Zeechefolleg_VALUE = Daten.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return Zeechefolleg_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Klass_VALUE:
    def __init__(자신, Wee):
        자신.Wee = Wee
        Lieser_VALUE = 자료읽기(Wee.read_bytes())
        if Lieser_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Klass_VALUE 표식이 아님')
        Lieser_VALUE.읽기(4)
        Element_COUNT = Lieser_VALUE.수('H')
        자신.Konstant_VALUE = [None] * Element_COUNT
        INDEX = 1
        while INDEX < Element_COUNT:
            종류 = Lieser_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Lieser_VALUE.읽기(Lieser_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Lieser_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Lieser_VALUE.읽기(4)
            elif 종류 in (5, 6):
                VALUE = Lieser_VALUE.읽기(8)
            elif 종류 in (7, 8, 16):
                VALUE = Lieser_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Lieser_VALUE.수('H'), Lieser_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Lieser_VALUE.수('B'), Lieser_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 Konstant_VALUE 종류: {}'.format(종류))
            자신.Konstant_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.Zougrëff_Agab = Lieser_VALUE.수('H')
        자신.Numm = 자신.Klass_Numm(Lieser_VALUE.수('H'))
        부모 = Lieser_VALUE.수('H')
        if 자신.Klass_Numm(부모) != 'java/lang/Object' or Lieser_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Numm + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.Feld_VALUE = 자신.멤버읽기(Lieser_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Lieser_VALUE)
        자신.속성읽기(Lieser_VALUE)

    def 문자(자신, INDEX):
        if 자신.Konstant_VALUE[INDEX][0] != 1:
            raise 컴파일오류('Zeechefolleg_VALUE Konstant_VALUE Format_VALUE Feeler')
        return 자신.Konstant_VALUE[INDEX][1]

    def Klass_Numm(자신, INDEX):
        return 자신.문자(자신.Konstant_VALUE[INDEX][1])

    def Referenzen(자신, INDEX):
        Besëtzer_VALUE, Numm_Format = 자신.Konstant_VALUE[INDEX][1]
        Numm, Format_VALUE = 자신.Konstant_VALUE[Numm_Format][1]
        return 자신.Klass_Numm(Besëtzer_VALUE), 자신.문자(Numm), 자신.문자(Format_VALUE)

    def 속성읽기(자신, Lieser_VALUE):
        Mooss = {}
        for _ in range(Lieser_VALUE.수('H')):
            Numm = 자신.문자(Lieser_VALUE.수('H'))
            Mooss[Numm] = Lieser_VALUE.읽기(Lieser_VALUE.수('I'))
        return Mooss

    def 멤버읽기(자신, Lieser_VALUE):
        Mooss = []
        for _ in range(Lieser_VALUE.수('H')):
            Zougrëff_Agab = Lieser_VALUE.수('H')
            Numm = 자신.문자(Lieser_VALUE.수('H'))
            Format_VALUE = 자신.문자(Lieser_VALUE.수('H'))
            Mooss.append((Zougrëff_Agab, Numm, Format_VALUE, 자신.속성읽기(Lieser_VALUE)))
        return Mooss


def 형식읽기(Zeechefolleg_VALUE):
    Mooss = []
    positionéieren = 0
    while positionéieren < len(Zeechefolleg_VALUE):
        for Format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if Zeechefolleg_VALUE.startswith(Format_VALUE, positionéieren):
                Mooss.append(Format_VALUE)
                positionéieren += len(Format_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 Datentyp: ' + Zeechefolleg_VALUE)
    return Mooss


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('FUNCTION_VALUE 서술 Format_VALUE Feeler: ' + 서술)
    return 인수, 반환


def Symbol(종류, *부분):
    Quell = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Quell).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def ausféieren_Befeel(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK Quell_Bamstruktur Build_System')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/Klass_VALUE 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 Build_System JDK 또는 openjdk-build의 부트 JDK Wee')
    해석기.add_argument('--bundle-runtime', help='ausféieren_Befeel 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK App_App_Beräich/Quell_Bamstruktur 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 Build_System 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 Build_System Zil (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 Build_System 대상의 libc/헤더/Bibliothéik 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 Format_VALUE')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=Klass_VALUE.FUNCTION_VALUE (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Laf (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ausféieren_Befeel ELF/.o 출력; openjdk-build는 전용 Build_System 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK Quell_Bamstruktur 디렉터리 하나와 --java-home 부트 JDK, -o Build_System 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Feeler:
            raise 컴파일오류(str(Feeler))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build Zil 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Create_Agab
        Create_Agab(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk Zil 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ausféieren_Befeel()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Feeler:
        print('erstellen_Quell Feeler: ' + str(Feeler), file=sys.stderr)
        sys.exit(1)
