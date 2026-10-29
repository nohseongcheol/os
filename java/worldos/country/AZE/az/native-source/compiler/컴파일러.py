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
    def __init__(자신, verilənlər):
        자신.verilənlər = verilənlər
        자신.yerinə_qoymaq = 0

    def Oxuma(자신, uzunluq_VALUE):
        if uzunluq_VALUE < 0 or 자신.yerinə_qoymaq + uzunluq_VALUE > len(자신.verilənlər):
            raise 컴파일오류('잘린 Sinif_VALUE 또는 Əmr verilənlər')
        ölçü = 자신.verilənlər[자신.yerinə_qoymaq:자신.yerinə_qoymaq + uzunluq_VALUE]
        자신.yerinə_qoymaq += uzunluq_VALUE
        return ölçü

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.Oxuma(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(verilənlər):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    sətir_VALUE = verilənlər.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return sətir_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Sinif_VALUE:
    def __init__(자신, Cığır):
        자신.Cığır = Cığır
        oxucu_VALUE = 자료읽기(Cığır.read_bytes())
        if oxucu_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Sinif_VALUE 표식이 아님')
        oxucu_VALUE.Oxuma(4)
        element_COUNT = oxucu_VALUE.수('H')
        자신.sabit_VALUE = [None] * element_COUNT
        INDEX = 1
        while INDEX < element_COUNT:
            종류 = oxucu_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(oxucu_VALUE.Oxuma(oxucu_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = oxucu_VALUE.수('i')
            elif 종류 == 4:
                VALUE = oxucu_VALUE.Oxuma(4)
            elif 종류 in (5, 6):
                VALUE = oxucu_VALUE.Oxuma(8)
            elif 종류 in (7, 8, 16):
                VALUE = oxucu_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (oxucu_VALUE.수('H'), oxucu_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (oxucu_VALUE.수('B'), oxucu_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 sabit_VALUE 종류: {}'.format(종류))
            자신.sabit_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.müraciət_daxiletmə = oxucu_VALUE.수('H')
        자신.Ad = 자신.Sinif_ad(oxucu_VALUE.수('H'))
        부모 = oxucu_VALUE.수('H')
        if 자신.Sinif_ad(부모) != 'java/lang/Object' or oxucu_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Ad + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.sahə_VALUE_0f39cf1c = 자신.멤버읽기(oxucu_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(oxucu_VALUE)
        자신.속성읽기(oxucu_VALUE)

    def 문자(자신, INDEX):
        if 자신.sabit_VALUE[INDEX][0] != 1:
            raise 컴파일오류('sətir_VALUE sabit_VALUE format_VALUE XƏTA')
        return 자신.sabit_VALUE[INDEX][1]

    def Sinif_ad(자신, INDEX):
        return 자신.문자(자신.sabit_VALUE[INDEX][1])

    def İstinad(자신, INDEX):
        sahib_VALUE, ad_format = 자신.sabit_VALUE[INDEX][1]
        Ad, format_VALUE = 자신.sabit_VALUE[ad_format][1]
        return 자신.Sinif_ad(sahib_VALUE), 자신.문자(Ad), 자신.문자(format_VALUE)

    def 속성읽기(자신, oxucu_VALUE):
        ölçü = {}
        for _ in range(oxucu_VALUE.수('H')):
            Ad = 자신.문자(oxucu_VALUE.수('H'))
            ölçü[Ad] = oxucu_VALUE.Oxuma(oxucu_VALUE.수('I'))
        return ölçü

    def 멤버읽기(자신, oxucu_VALUE):
        ölçü = []
        for _ in range(oxucu_VALUE.수('H')):
            müraciət_daxiletmə = oxucu_VALUE.수('H')
            Ad = 자신.문자(oxucu_VALUE.수('H'))
            format_VALUE = 자신.문자(oxucu_VALUE.수('H'))
            ölçü.append((müraciət_daxiletmə, Ad, format_VALUE, 자신.속성읽기(oxucu_VALUE)))
        return ölçü


def 형식읽기(sətir_VALUE):
    ölçü = []
    yerinə_qoymaq = 0
    while yerinə_qoymaq < len(sətir_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if sətir_VALUE.startswith(format_VALUE, yerinə_qoymaq):
                ölçü.append(format_VALUE)
                yerinə_qoymaq += len(format_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 verilənlər_növü: ' + sətir_VALUE)
    return ölçü


def 함수형식(서술):
    인수, geri_qaytarmaq_ölçü = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    geri_qaytarmaq_TYPE = 형식읽기(geri_qaytarmaq_ölçü)
    if 'V' in 인수 or len(geri_qaytarmaq_TYPE) != 1:
        raise 컴파일오류('FUNCTION_VALUE 서술 format_VALUE XƏTA: ' + 서술)
    return 인수, geri_qaytarmaq_ölçü


def simvol(종류, *부분):
    QAYNAQ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(QAYNAQ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def icra_etmək_əmr(인수=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK mənbə_ağac qurmaq_sistem')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/Sinif_VALUE 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 qurmaq_sistem JDK 또는 openjdk-build의 부트 JDK Cığır')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='icra_etmək_əmr 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK proqram_işəsalma/mənbə_ağac 빌드의 C 컴파일러')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 qurmaq_sistem 작업 수')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 qurmaq_sistem hədəf (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 qurmaq_sistem 대상의 libc/헤더/kitabxana 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Sinif_VALUE.FUNCTION_VALUE (자체 스택 ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.İcra_Et (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='icra_etmək_əmr ELF/.o 출력; openjdk-build는 전용 qurmaq_sistem 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    인자 = parser_48ee4b1b.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK mənbə_ağac 디렉터리 하나와 --java-home 부트 JDK, -o qurmaq_sistem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as XƏTA:
            raise 컴파일오류(str(XƏTA))
        return
    if not 인자.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build hədəf 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import yarat_daxiletmə
        yarat_daxiletmə(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk hədəf 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for təyin_et_VALUE in 인자.export: 자바명령.extend(['--export', təyin_et_VALUE])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        icra_etmək_əmr()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as XƏTA:
        print('qurmaq_mənbə XƏTA: ' + str(XƏTA), file=sys.stderr)
        sys.exit(1)
