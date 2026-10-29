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
    def __init__(자신, берилмелер):
        자신.берилмелер = берилмелер
        자신.Турган_жери = 0

    def Окуу(자신, узундук_маани):
        if узундук_маани < 0 or 자신.Турган_жери + узундук_маани > len(자신.берилмелер):
            raise 컴파일오류('잘린 класс_маани 또는 Команда берилмелер')
        결과 = 자신.берилмелер[자신.Турган_жери:자신.Турган_жери + узундук_маани]
        자신.Турган_жери += узундук_маани
        return 결과

    def 수(자신, формат_маани):
        return struct.unpack('>' + формат_маани, 자신.Окуу(struct.calcsize('>' + формат_маани)))[0]


def 수정유티에프해독(берилмелер):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    сап_маани = берилмелер.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return сап_маани.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class класс_маани:
    def __init__(자신, ЖОЛ):
        자신.ЖОЛ = ЖОЛ
        окуучу_маани = 자료읽기(ЖОЛ.read_bytes())
        if окуучу_маани.수('I') != 0xcafebabe:
            raise 컴파일오류('Java класс_маани 표식이 아님')
        окуучу_маани.Окуу(4)
        개수 = окуучу_маани.수('H')
        자신.өзгөрбөс_чоңдук_маани = [None] * 개수
        индекс = 1
        while индекс < 개수:
            종류 = окуучу_маани.수('B')
            if 종류 == 1:
                маани = 수정유티에프해독(окуучу_маани.Окуу(окуучу_маани.수('H')))
            elif 종류 == 3:
                маани = окуучу_маани.수('i')
            elif 종류 == 4:
                маани = окуучу_маани.Окуу(4)
            elif 종류 in (5, 6):
                маани = окуучу_маани.Окуу(8)
            elif 종류 in (7, 8, 16):
                маани = окуучу_маани.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                маани = (окуучу_маани.수('H'), окуучу_маани.수('H'))
            elif 종류 == 15:
                маани = (окуучу_маани.수('B'), окуучу_маани.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 өзгөрбөс_чоңдук_маани 종류: {}'.format(종류))
            자신.өзгөрбөс_чоңдук_маани[индекс] = (종류, маани)
            индекс += 2 if 종류 in (5, 6) else 1
        자신.мүмкүндүк_алуу_киргизме_жазуу = окуучу_маани.수('H')
        자신.Аты = 자신.класс_аты(окуучу_маани.수('H'))
        부모 = окуучу_маани.수('H')
        if 자신.класс_аты(부모) != 'java/lang/Object' or окуучу_маани.수('H') != 0:
            raise 컴파일오류(자신.Аты + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.талаа_маани = 자신.멤버읽기(окуучу_маани)
        자신.функция_маани = 자신.멤버읽기(окуучу_маани)
        자신.속성읽기(окуучу_маани)

    def 문자(자신, индекс):
        if 자신.өзгөрбөс_чоңдук_маани[индекс][0] != 1:
            raise 컴파일오류('сап_маани өзгөрбөс_чоңдук_маани формат_маани Ката')
        return 자신.өзгөрбөс_чоңдук_маани[индекс][1]

    def класс_аты(자신, индекс):
        return 자신.문자(자신.өзгөрбөс_чоңдук_маани[индекс][1])

    def Шилтемелер(자신, индекс):
        ээ_кожоюн_кимдир_бирөөгө_таандык_болуу_маани, аты_формат = 자신.өзгөрбөс_чоңдук_маани[индекс][1]
        Аты, формат_маани = 자신.өзгөрбөс_чоңдук_маани[аты_формат][1]
        return 자신.класс_аты(ээ_кожоюн_кимдир_бирөөгө_таандык_болуу_маани), 자신.문자(Аты), 자신.문자(формат_маани)

    def 속성읽기(자신, окуучу_маани):
        결과 = {}
        for _ in range(окуучу_маани.수('H')):
            Аты = 자신.문자(окуучу_маани.수('H'))
            결과[Аты] = окуучу_маани.Окуу(окуучу_маани.수('I'))
        return 결과

    def 멤버읽기(자신, окуучу_маани):
        결과 = []
        for _ in range(окуучу_маани.수('H')):
            мүмкүндүк_алуу_киргизме_жазуу = окуучу_маани.수('H')
            Аты = 자신.문자(окуучу_маани.수('H'))
            формат_маани = 자신.문자(окуучу_маани.수('H'))
            결과.append((мүмкүндүк_алуу_киргизме_жазуу, Аты, формат_маани, 자신.속성읽기(окуучу_маани)))
        return 결과


def 형식읽기(сап_маани):
    결과 = []
    Турган_жери = 0
    while Турган_жери < len(сап_маани):
        for формат_маани in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if сап_маани.startswith(формат_маани, Турган_жери):
                결과.append(формат_маани)
                Турган_жери += len(формат_маани)
                break
        else:
            raise 컴파일오류('지원하지 않는 берилмелер_тиби: ' + сап_маани)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('функция_маани 서술 формат_маани Ката: ' + 서술)
    return 인수, 반환


def символ(종류, *부분):
    Булак = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Булак).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 функция_маани 서술에 대해서만 허용한다.
def аткаруу_буйрук(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK башат_дарак курам_тутум')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/класс_маани 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 курам_тутум JDK 또는 openjdk-build의 부트 JDK ЖОЛ')
    해석기.add_argument('--bundle-runtime', help='аткаруу_буйрук 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK програм_жаратма_тарткычы/башат_дарак 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 курам_тутум 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 курам_тутум максат (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 курам_тутум 대상의 libc/헤더/жыйнак 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 формат_маани')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=класс_маани.функция_маани (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Жүргүзүү (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='аткаруу_буйрук ELF/.o Чыгыш; openjdk-build는 전용 курам_тутум 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK башат_дарак 디렉터리 하나와 --java-home 부트 JDK, -o курам_тутум 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Ката:
            raise 컴파일오류(str(Ката))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build максат 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import түзүү_киргизме_жазуу
        түзүү_киргизме_жазуу(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk максат 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        аткаруу_буйрук()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Ката:
        print('тургузуу_башат Ката: ' + str(Ката), file=sys.stderr)
        sys.exit(1)
