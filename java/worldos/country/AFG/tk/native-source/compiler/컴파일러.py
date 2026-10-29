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
    def __init__(자신, maglumat):
        자신.maglumat = maglumat
        자신.위치 = 0

    def Oka(자신, dowamlylyk_baha):
        if dowamlylyk_baha < 0 or 자신.위치 + dowamlylyk_baha > len(자신.maglumat):
            raise 컴파일오류('잘린 klas_baha 또는 buýruk maglumat')
        결과 = 자신.maglumat[자신.위치:자신.위치 + dowamlylyk_baha]
        자신.위치 += dowamlylyk_baha
        return 결과

    def 수(자신, format_baha):
        return struct.unpack('>' + format_baha, 자신.Oka(struct.calcsize('>' + format_baha)))[0]


def 수정유티에프해독(maglumat):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    setir_baha_6ca8363c = maglumat.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return setir_baha_6ca8363c.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klas_baha:
    def __init__(자신, Ýol):
        자신.Ýol = Ýol
        okyjy_baha = 자료읽기(Ýol.read_bytes())
        if okyjy_baha.수('I') != 0xcafebabe:
            raise 컴파일오류('Java klas_baha 표식이 아님')
        okyjy_baha.Oka(4)
        개수 = okyjy_baha.수('H')
        자신.hemişelik_baha = [None] * 개수
        indeks = 1
        while indeks < 개수:
            종류 = okyjy_baha.수('B')
            if 종류 == 1:
                baha = 수정유티에프해독(okyjy_baha.Oka(okyjy_baha.수('H')))
            elif 종류 == 3:
                baha = okyjy_baha.수('i')
            elif 종류 == 4:
                baha = okyjy_baha.Oka(4)
            elif 종류 in (5, 6):
                baha = okyjy_baha.Oka(8)
            elif 종류 in (7, 8, 16):
                baha = okyjy_baha.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                baha = (okyjy_baha.수('H'), okyjy_baha.수('H'))
            elif 종류 == 15:
                baha = (okyjy_baha.수('B'), okyjy_baha.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 hemişelik_baha 종류: {}'.format(종류))
            자신.hemişelik_baha[indeks] = (종류, baha)
            indeks += 2 if 종류 in (5, 6) else 1
        자신.ygtyýarlylyk_girizmeklik = okyjy_baha.수('H')
        자신.Ad = 자신.klas_at(okyjy_baha.수('H'))
        부모 = okyjy_baha.수('H')
        if 자신.klas_at(부모) != 'java/lang/Object' or okyjy_baha.수('H') != 0:
            raise 컴파일오류(자신.Ad + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.meýdan_baha = 자신.멤버읽기(okyjy_baha)
        자신.FUNCTION_baha = 자신.멤버읽기(okyjy_baha)
        자신.속성읽기(okyjy_baha)

    def 문자(자신, indeks):
        if 자신.hemişelik_baha[indeks][0] != 1:
            raise 컴파일오류('setir_baha_6ca8363c hemişelik_baha format_baha Hata')
        return 자신.hemişelik_baha[indeks][1]

    def klas_at(자신, indeks):
        return 자신.문자(자신.hemişelik_baha[indeks][1])

    def Salgylanma(자신, indeks):
        eýe_baha, at_format = 자신.hemişelik_baha[indeks][1]
        Ad, format_baha = 자신.hemişelik_baha[at_format][1]
        return 자신.klas_at(eýe_baha), 자신.문자(Ad), 자신.문자(format_baha)

    def 속성읽기(자신, okyjy_baha):
        결과 = {}
        for _ in range(okyjy_baha.수('H')):
            Ad = 자신.문자(okyjy_baha.수('H'))
            결과[Ad] = okyjy_baha.Oka(okyjy_baha.수('I'))
        return 결과

    def 멤버읽기(자신, okyjy_baha):
        결과 = []
        for _ in range(okyjy_baha.수('H')):
            ygtyýarlylyk_girizmeklik = okyjy_baha.수('H')
            Ad = 자신.문자(okyjy_baha.수('H'))
            format_baha = 자신.문자(okyjy_baha.수('H'))
            결과.append((ygtyýarlylyk_girizmeklik, Ad, format_baha, 자신.속성읽기(okyjy_baha)))
        return 결과


def 형식읽기(setir_baha_6ca8363c):
    결과 = []
    위치 = 0
    while 위치 < len(setir_baha_6ca8363c):
        for format_baha in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if setir_baha_6ca8363c.startswith(format_baha, 위치):
                결과.append(format_baha)
                위치 += len(format_baha)
                break
        else:
            raise 컴파일오류('지원하지 않는 maglumatlaryň_görnüşi: ' + setir_baha_6ca8363c)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('FUNCTION_baha 서술 format_baha Hata: ' + 서술)
    return 인수, 반환


def nyşan(종류, *부분):
    Çeşme = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Çeşme).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_baha 서술에 대해서만 허용한다.
def ýerine_ýetir_buýruk(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK gor_agaç düz_ulgam')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/klas_baha 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 düz_ulgam JDK 또는 openjdk-build의 부트 JDK Ýol')
    해석기.add_argument('--bundle-runtime', help='ýerine_ýetir_buýruk 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK programma_programma_paneli/gor_agaç 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 düz_ulgam 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 düz_ulgam niýet (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 düz_ulgam 대상의 libc/헤더/Kitaphana 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_baha')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=klas_baha.FUNCTION_baha (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Bitir (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ýerine_ýetir_buýruk ELF/.o 출력; openjdk-build는 전용 düz_ulgam 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK gor_agaç 디렉터리 하나와 --java-home 부트 JDK, -o düz_ulgam 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Hata:
            raise 컴파일오류(str(Hata))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build niýet 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import döretmek_girizmeklik
        döretmek_girizmeklik(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk niýet 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ýerine_ýetir_buýruk()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Hata:
        print('düz_gor Hata: ' + str(Hata), file=sys.stderr)
        sys.exit(1)
