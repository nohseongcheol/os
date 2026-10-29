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
    def __init__(자신, datà):
        자신.datà = datà
        자신.위치 = 0

    def Wepụta_ọzi(자신, ogologo_valuu):
        if ogologo_valuu < 0 or 자신.위치 + ogologo_valuu > len(자신.datà):
            raise 컴파일오류('잘린 klaàsị_valuu 또는 Ntiiwu datà')
        결과 = 자신.datà[자신.위치:자신.위치 + ogologo_valuu]
        자신.위치 += ogologo_valuu
        return 결과

    def 수(자신, hàzie_valuu):
        return struct.unpack('>' + hàzie_valuu, 자신.Wepụta_ọzi(struct.calcsize('>' + hàzie_valuu)))[0]


def 수정유티에프해독(datà):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ùsòròokwū_valuu = datà.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ùsòròokwū_valuu.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klaàsị_valuu:
    def __init__(자신, ụzọ_ozi):
        자신.ụzọ_ozi = ụzọ_ozi
        Ọgụụ_valuu = 자료읽기(ụzọ_ozi.read_bytes())
        if Ọgụụ_valuu.수('I') != 0xcafebabe:
            raise 컴파일오류('Java klaàsị_valuu 표식이 아님')
        Ọgụụ_valuu.Wepụta_ọzi(4)
        개수 = Ọgụụ_valuu.수('H')
        자신.ihendịgide_valuu = [None] * 개수
        indèks = 1
        while indèks < 개수:
            종류 = Ọgụụ_valuu.수('B')
            if 종류 == 1:
                valuu = 수정유티에프해독(Ọgụụ_valuu.Wepụta_ọzi(Ọgụụ_valuu.수('H')))
            elif 종류 == 3:
                valuu = Ọgụụ_valuu.수('i')
            elif 종류 == 4:
                valuu = Ọgụụ_valuu.Wepụta_ọzi(4)
            elif 종류 in (5, 6):
                valuu = Ọgụụ_valuu.Wepụta_ọzi(8)
            elif 종류 in (7, 8, 16):
                valuu = Ọgụụ_valuu.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                valuu = (Ọgụụ_valuu.수('H'), Ọgụụ_valuu.수('H'))
            elif 종류 == 15:
                valuu = (Ọgụụ_valuu.수('B'), Ọgụụ_valuu.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 ihendịgide_valuu 종류: {}'.format(종류))
            자신.ihendịgide_valuu[indèks] = (종류, valuu)
            indèks += 2 if 종류 in (5, 6) else 1
        자신.òhèrè_ndebà = Ọgụụ_valuu.수('H')
        자신.Aha = 자신.klaàsị_akara_ahà(Ọgụụ_valuu.수('H'))
        부모 = Ọgụụ_valuu.수('H')
        if 자신.klaàsị_akara_ahà(부모) != 'java/lang/Object' or Ọgụụ_valuu.수('H') != 0:
            raise 컴파일오류(자신.Aha + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.fild_valuu = 자신.멤버읽기(Ọgụụ_valuu)
        자신.ọrụ_valuu = 자신.멤버읽기(Ọgụụ_valuu)
        자신.속성읽기(Ọgụụ_valuu)

    def 문자(자신, indèks):
        if 자신.ihendịgide_valuu[indèks][0] != 1:
            raise 컴파일오류('ùsòròokwū_valuu ihendịgide_valuu hàzie_valuu mmejọ')
        return 자신.ihendịgide_valuu[indèks][1]

    def klaàsị_akara_ahà(자신, indèks):
        return 자신.문자(자신.ihendịgide_valuu[indèks][1])

    def Nrụtụ_aka(자신, indèks):
        nwe_valuu, akara_ahà_hàzie = 자신.ihendịgide_valuu[indèks][1]
        Aha, hàzie_valuu = 자신.ihendịgide_valuu[akara_ahà_hàzie][1]
        return 자신.klaàsị_akara_ahà(nwe_valuu), 자신.문자(Aha), 자신.문자(hàzie_valuu)

    def 속성읽기(자신, Ọgụụ_valuu):
        결과 = {}
        for _ in range(Ọgụụ_valuu.수('H')):
            Aha = 자신.문자(Ọgụụ_valuu.수('H'))
            결과[Aha] = Ọgụụ_valuu.Wepụta_ọzi(Ọgụụ_valuu.수('I'))
        return 결과

    def 멤버읽기(자신, Ọgụụ_valuu):
        결과 = []
        for _ in range(Ọgụụ_valuu.수('H')):
            òhèrè_ndebà = Ọgụụ_valuu.수('H')
            Aha = 자신.문자(Ọgụụ_valuu.수('H'))
            hàzie_valuu = 자신.문자(Ọgụụ_valuu.수('H'))
            결과.append((òhèrè_ndebà, Aha, hàzie_valuu, 자신.속성읽기(Ọgụụ_valuu)))
        return 결과


def 형식읽기(ùsòròokwū_valuu):
    결과 = []
    위치 = 0
    while 위치 < len(ùsòròokwū_valuu):
        for hàzie_valuu in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ùsòròokwū_valuu.startswith(hàzie_valuu, 위치):
                결과.append(hàzie_valuu)
                위치 += len(hàzie_valuu)
                break
        else:
            raise 컴파일오류('지원하지 않는 ụdịrị_datà: ' + ùsòròokwū_valuu)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('ọrụ_valuu 서술 hàzie_valuu mmejọ: ' + 서술)
    return 인수, 반환


def adimara(종류, *부분):
    ebensìbịa = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ebensìbịa).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ọrụ_valuu 서술에 대해서만 허용한다.
def mee_nnyemiwu(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ebensìbịa_èsèrèsè_osisi wue_sistèm')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/klaàsị_valuu 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 wue_sistèm JDK 또는 openjdk-build의 부트 JDK ụzọ_ozi')
    해석기.add_argument('--bundle-runtime', help='mee_nnyemiwu 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK app_ihengosi_ndi_app/ebensìbịa_èsèrèsè_osisi 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 wue_sistèm 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 wue_sistèm ebenlereanya (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 wue_sistèm 대상의 libc/헤더/ọbaakwụkwọ 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 hàzie_valuu')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=klaàsị_valuu.ọrụ_valuu (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Bido (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='mee_nnyemiwu ELF/.o 출력; openjdk-build는 전용 wue_sistèm 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ebensìbịa_èsèrèsè_osisi 디렉터리 하나와 --java-home 부트 JDK, -o wue_sistèm 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as mmejọ:
            raise 컴파일오류(str(mmejọ))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ebenlereanya 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import mepụta_ndebà
        mepụta_ndebà(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ebenlereanya 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        mee_nnyemiwu()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as mmejọ:
        print('wue_ebensìbịa mmejọ: ' + str(mmejọ), file=sys.stderr)
        sys.exit(1)
