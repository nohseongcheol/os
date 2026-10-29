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
    def __init__(자신, ma_lumotlar):
        자신.ma_lumotlar = ma_lumotlar
        자신.Holati = 0

    def Oʻqish(자신, uzunlik_VALUE):
        if uzunlik_VALUE < 0 or 자신.Holati + uzunlik_VALUE > len(자신.ma_lumotlar):
            raise 컴파일오류('잘린 Sinf_VALUE 또는 Buyruq ma_lumotlar')
        o_lchov = 자신.ma_lumotlar[자신.Holati:자신.Holati + uzunlik_VALUE]
        자신.Holati += uzunlik_VALUE
        return o_lchov

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.Oʻqish(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(ma_lumotlar):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    satr_VALUE = ma_lumotlar.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return satr_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Sinf_VALUE:
    def __init__(자신, yo_l):
        자신.yo_l = yo_l
        o_quvchi_VALUE = 자료읽기(yo_l.read_bytes())
        if o_quvchi_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Sinf_VALUE 표식이 아님')
        o_quvchi_VALUE.Oʻqish(4)
        element_COUNT = o_quvchi_VALUE.수('H')
        자신.konstanta_VALUE = [None] * element_COUNT
        INDEX = 1
        while INDEX < element_COUNT:
            종류 = o_quvchi_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(o_quvchi_VALUE.Oʻqish(o_quvchi_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = o_quvchi_VALUE.수('i')
            elif 종류 == 4:
                VALUE = o_quvchi_VALUE.Oʻqish(4)
            elif 종류 in (5, 6):
                VALUE = o_quvchi_VALUE.Oʻqish(8)
            elif 종류 in (7, 8, 16):
                VALUE = o_quvchi_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (o_quvchi_VALUE.수('H'), o_quvchi_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (o_quvchi_VALUE.수('B'), o_quvchi_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 konstanta_VALUE 종류: {}'.format(종류))
            자신.konstanta_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.kirish_huquqi_kiritish = o_quvchi_VALUE.수('H')
        자신.Nomi = 자신.Sinf_nom(o_quvchi_VALUE.수('H'))
        부모 = o_quvchi_VALUE.수('H')
        if 자신.Sinf_nom(부모) != 'java/lang/Object' or o_quvchi_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Nomi + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ma_lumotlar_maydoni_VALUE = 자신.멤버읽기(o_quvchi_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(o_quvchi_VALUE)
        자신.속성읽기(o_quvchi_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstanta_VALUE[INDEX][0] != 1:
            raise 컴파일오류('satr_VALUE konstanta_VALUE format_VALUE Xato')
        return 자신.konstanta_VALUE[INDEX][1]

    def Sinf_nom(자신, INDEX):
        return 자신.문자(자신.konstanta_VALUE[INDEX][1])

    def Ma_lumotnomalar(자신, INDEX):
        egasi_VALUE, nom_format = 자신.konstanta_VALUE[INDEX][1]
        Nomi, format_VALUE = 자신.konstanta_VALUE[nom_format][1]
        return 자신.Sinf_nom(egasi_VALUE), 자신.문자(Nomi), 자신.문자(format_VALUE)

    def 속성읽기(자신, o_quvchi_VALUE):
        o_lchov = {}
        for _ in range(o_quvchi_VALUE.수('H')):
            Nomi = 자신.문자(o_quvchi_VALUE.수('H'))
            o_lchov[Nomi] = o_quvchi_VALUE.Oʻqish(o_quvchi_VALUE.수('I'))
        return o_lchov

    def 멤버읽기(자신, o_quvchi_VALUE):
        o_lchov = []
        for _ in range(o_quvchi_VALUE.수('H')):
            kirish_huquqi_kiritish = o_quvchi_VALUE.수('H')
            Nomi = 자신.문자(o_quvchi_VALUE.수('H'))
            format_VALUE = 자신.문자(o_quvchi_VALUE.수('H'))
            o_lchov.append((kirish_huquqi_kiritish, Nomi, format_VALUE, 자신.속성읽기(o_quvchi_VALUE)))
        return o_lchov


def 형식읽기(satr_VALUE):
    o_lchov = []
    Holati = 0
    while Holati < len(satr_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if satr_VALUE.startswith(format_VALUE, Holati):
                o_lchov.append(format_VALUE)
                Holati += len(format_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 ma_lumotlar_turi: ' + satr_VALUE)
    return o_lchov


def 함수형식(서술):
    인수, qaytarish_o_lchov = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    qaytarish_TYPE = 형식읽기(qaytarish_o_lchov)
    if 'V' in 인수 or len(qaytarish_TYPE) != 1:
        raise 컴파일오류('FUNCTION_VALUE 서술 format_VALUE Xato: ' + 서술)
    return 인수, qaytarish_o_lchov


def ramz(종류, *부분):
    manba = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(manba).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def bajarmoq_buyruq(인수=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK manba_daraxt nashr_tizim')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/Sinf_VALUE 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 nashr_tizim JDK 또는 openjdk-build의 부트 JDK yo_l')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='bajarmoq_buyruq 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK ilova_ilovalar_paneli/manba_daraxt 빌드의 C 컴파일러')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 nashr_tizim 작업 수')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 nashr_tizim nishon (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 nashr_tizim 대상의 libc/헤더/kutubxona 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Sinf_VALUE.FUNCTION_VALUE (자체 스택 ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.Bajarish (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='bajarmoq_buyruq ELF/.o 출력; openjdk-build는 전용 nashr_tizim 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    인자 = parser_48ee4b1b.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK manba_daraxt 디렉터리 하나와 --java-home 부트 JDK, -o nashr_tizim 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Xato:
            raise 컴파일오류(str(Xato))
        return
    if not 인자.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build nishon 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Yaratish_kiritish
        Yaratish_kiritish(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk nishon 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for tayinlash_VALUE in 인자.export: 자바명령.extend(['--export', tayinlash_VALUE])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        bajarmoq_buyruq()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Xato:
        print('yig_moq_manba Xato: ' + str(Xato), file=sys.stderr)
        sys.exit(1)
