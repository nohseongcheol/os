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
    def __init__(자신, data):
        자신.data = data
        자신.pożizzjoni = 0

    def 읽기(자신, tul_VALUE):
        if tul_VALUE < 0 or 자신.pożizzjoni + tul_VALUE > len(자신.data):
            raise 컴파일오류('잘린 klassi_VALUE 또는 kmand data')
        miżura = 자신.data[자신.pożizzjoni:자신.pożizzjoni + tul_VALUE]
        자신.pożizzjoni += tul_VALUE
        return miżura

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.읽기(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    string_VALUE = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return string_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klassi_VALUE:
    def __init__(자신, mogħdija):
        자신.mogħdija = mogħdija
        Qarrej_VALUE = 자료읽기(mogħdija.read_bytes())
        if Qarrej_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java klassi_VALUE 표식이 아님')
        Qarrej_VALUE.읽기(4)
        element_COUNT = Qarrej_VALUE.수('H')
        자신.valur_fiss_VALUE = [None] * element_COUNT
        INDEX = 1
        while INDEX < element_COUNT:
            종류 = Qarrej_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Qarrej_VALUE.읽기(Qarrej_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Qarrej_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Qarrej_VALUE.읽기(4)
            elif 종류 in (5, 6):
                VALUE = Qarrej_VALUE.읽기(8)
            elif 종류 in (7, 8, 16):
                VALUE = Qarrej_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Qarrej_VALUE.수('H'), Qarrej_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Qarrej_VALUE.수('B'), Qarrej_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 valur_fiss_VALUE 종류: {}'.format(종류))
            자신.valur_fiss_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.aċċess_entrata = Qarrej_VALUE.수('H')
        자신.isem = 자신.klassi_isem(Qarrej_VALUE.수('H'))
        부모 = Qarrej_VALUE.수('H')
        if 자신.klassi_isem(부모) != 'java/lang/Object' or Qarrej_VALUE.수('H') != 0:
            raise 컴파일오류(자신.isem + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.qasam_VALUE = 자신.멤버읽기(Qarrej_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Qarrej_VALUE)
        자신.속성읽기(Qarrej_VALUE)

    def 문자(자신, INDEX):
        if 자신.valur_fiss_VALUE[INDEX][0] != 1:
            raise 컴파일오류('string_VALUE valur_fiss_VALUE format_VALUE żball')
        return 자신.valur_fiss_VALUE[INDEX][1]

    def klassi_isem(자신, INDEX):
        return 자신.문자(자신.valur_fiss_VALUE[INDEX][1])

    def Referenza(자신, INDEX):
        propjetarju_VALUE, isem_format = 자신.valur_fiss_VALUE[INDEX][1]
        isem, format_VALUE = 자신.valur_fiss_VALUE[isem_format][1]
        return 자신.klassi_isem(propjetarju_VALUE), 자신.문자(isem), 자신.문자(format_VALUE)

    def 속성읽기(자신, Qarrej_VALUE):
        miżura = {}
        for _ in range(Qarrej_VALUE.수('H')):
            isem = 자신.문자(Qarrej_VALUE.수('H'))
            miżura[isem] = Qarrej_VALUE.읽기(Qarrej_VALUE.수('I'))
        return miżura

    def 멤버읽기(자신, Qarrej_VALUE):
        miżura = []
        for _ in range(Qarrej_VALUE.수('H')):
            aċċess_entrata = Qarrej_VALUE.수('H')
            isem = 자신.문자(Qarrej_VALUE.수('H'))
            format_VALUE = 자신.문자(Qarrej_VALUE.수('H'))
            miżura.append((aċċess_entrata, isem, format_VALUE, 자신.속성읽기(Qarrej_VALUE)))
        return miżura


def 형식읽기(string_VALUE):
    miżura = []
    pożizzjoni = 0
    while pożizzjoni < len(string_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if string_VALUE.startswith(format_VALUE, pożizzjoni):
                miżura.append(format_VALUE)
                pożizzjoni += len(format_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 tip_ta_data: ' + string_VALUE)
    return miżura


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('FUNCTION_VALUE 서술 format_VALUE żball: ' + 서술)
    return 인수, 반환


def simbolu(종류, *부분):
    sors = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(sors).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def eżegwixxa_kmand(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK sors_siġra bena_sistema')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/klassi_VALUE 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 bena_sistema JDK 또는 openjdk-build의 부트 JDK mogħdija')
    해석기.add_argument('--bundle-runtime', help='eżegwixxa_kmand 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK programm_ġabra_ta_apps/sors_siġra 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 bena_sistema 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 bena_sistema mira (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 bena_sistema 대상의 libc/헤더/librerija 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=klassi_VALUE.FUNCTION_VALUE (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.serje (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='eżegwixxa_kmand ELF/.o 출력; openjdk-build는 전용 bena_sistema 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK sors_siġra 디렉터리 하나와 --java-home 부트 JDK, -o bena_sistema 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as żball:
            raise 컴파일오류(str(żball))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build mira 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ħalaq_entrata
        ħalaq_entrata(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk mira 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for assenja_VALUE in 인자.export: 자바명령.extend(['--export', assenja_VALUE])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        eżegwixxa_kmand()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as żball:
        print('bena_sors żball: ' + str(żball), file=sys.stderr)
        sys.exit(1)
