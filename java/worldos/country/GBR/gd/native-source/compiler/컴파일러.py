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
    def __init__(자신, dàta):
        자신.dàta = dàta
        자신.suidhich = 0

    def 읽기(자신, faid_VALUE):
        if faid_VALUE < 0 or 자신.suidhich + faid_VALUE > len(자신.dàta):
            raise 컴파일오류('잘린 clas_VALUE 또는 àithne dàta')
        tomhas = 자신.dàta[자신.suidhich:자신.suidhich + faid_VALUE]
        자신.suidhich += faid_VALUE
        return tomhas

    def 수(자신, fòrmat_VALUE):
        return struct.unpack('>' + fòrmat_VALUE, 자신.읽기(struct.calcsize('>' + fòrmat_VALUE)))[0]


def 수정유티에프해독(dàta):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    sreang_VALUE = dàta.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return sreang_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class clas_VALUE:
    def __init__(자신, Slighe):
        자신.Slighe = Slighe
        Leughadair_VALUE = 자료읽기(Slighe.read_bytes())
        if Leughadair_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java clas_VALUE 표식이 아님')
        Leughadair_VALUE.읽기(4)
        nì_COUNT = Leughadair_VALUE.수('H')
        자신.cunbhalachan_VALUE = [None] * nì_COUNT
        INDEX = 1
        while INDEX < nì_COUNT:
            종류 = Leughadair_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Leughadair_VALUE.읽기(Leughadair_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Leughadair_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Leughadair_VALUE.읽기(4)
            elif 종류 in (5, 6):
                VALUE = Leughadair_VALUE.읽기(8)
            elif 종류 in (7, 8, 16):
                VALUE = Leughadair_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Leughadair_VALUE.수('H'), Leughadair_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Leughadair_VALUE.수('B'), Leughadair_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 cunbhalachan_VALUE 종류: {}'.format(종류))
            자신.cunbhalachan_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.inntrigeadh_cur_a_steach = Leughadair_VALUE.수('H')
        자신.Ainm = 자신.clas_ainm(Leughadair_VALUE.수('H'))
        부모 = Leughadair_VALUE.수('H')
        if 자신.clas_ainm(부모) != 'java/lang/Object' or Leughadair_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Ainm + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.raon_VALUE = 자신.멤버읽기(Leughadair_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Leughadair_VALUE)
        자신.속성읽기(Leughadair_VALUE)

    def 문자(자신, INDEX):
        if 자신.cunbhalachan_VALUE[INDEX][0] != 1:
            raise 컴파일오류('sreang_VALUE cunbhalachan_VALUE fòrmat_VALUE Mearachd')
        return 자신.cunbhalachan_VALUE[INDEX][1]

    def clas_ainm(자신, INDEX):
        return 자신.문자(자신.cunbhalachan_VALUE[INDEX][1])

    def fiosrachadh(자신, INDEX):
        sealbhadair_VALUE, ainm_fòrmat = 자신.cunbhalachan_VALUE[INDEX][1]
        Ainm, fòrmat_VALUE = 자신.cunbhalachan_VALUE[ainm_fòrmat][1]
        return 자신.clas_ainm(sealbhadair_VALUE), 자신.문자(Ainm), 자신.문자(fòrmat_VALUE)

    def 속성읽기(자신, Leughadair_VALUE):
        tomhas = {}
        for _ in range(Leughadair_VALUE.수('H')):
            Ainm = 자신.문자(Leughadair_VALUE.수('H'))
            tomhas[Ainm] = Leughadair_VALUE.읽기(Leughadair_VALUE.수('I'))
        return tomhas

    def 멤버읽기(자신, Leughadair_VALUE):
        tomhas = []
        for _ in range(Leughadair_VALUE.수('H')):
            inntrigeadh_cur_a_steach = Leughadair_VALUE.수('H')
            Ainm = 자신.문자(Leughadair_VALUE.수('H'))
            fòrmat_VALUE = 자신.문자(Leughadair_VALUE.수('H'))
            tomhas.append((inntrigeadh_cur_a_steach, Ainm, fòrmat_VALUE, 자신.속성읽기(Leughadair_VALUE)))
        return tomhas


def 형식읽기(sreang_VALUE):
    tomhas = []
    suidhich = 0
    while suidhich < len(sreang_VALUE):
        for fòrmat_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if sreang_VALUE.startswith(fòrmat_VALUE, suidhich):
                tomhas.append(fòrmat_VALUE)
                suidhich += len(fòrmat_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 seòrsa_an_dàta: ' + sreang_VALUE)
    return tomhas


def 함수형식(서술):
    인수, return_tomhas = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    return_TYPE = 형식읽기(return_tomhas)
    if 'V' in 인수 or len(return_TYPE) != 1:
        raise 컴파일오류('FUNCTION_VALUE 서술 fòrmat_VALUE Mearachd: ' + 서술)
    return 인수, return_tomhas


def samhla(종류, *부분):
    tùs = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(tùs).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def gnìomhaich_àithne(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK tùs_craobh tog_siostam')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/clas_VALUE 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 tog_siostam JDK 또는 openjdk-build의 부트 JDK Slighe')
    해석기.add_argument('--bundle-runtime', help='gnìomhaich_àithne 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK ap_drathair_nan_aplacaid/tùs_craobh 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 tog_siostam 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 tog_siostam targaid (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 tog_siostam 대상의 libc/헤더/leabhar_lann 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 fòrmat_VALUE')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=clas_VALUE.FUNCTION_VALUE (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ruith (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='gnìomhaich_àithne ELF/.o 출력; openjdk-build는 전용 tog_siostam 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK tùs_craobh 디렉터리 하나와 --java-home 부트 JDK, -o tog_siostam 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Mearachd:
            raise 컴파일오류(str(Mearachd))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build targaid 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Create_cur_a_steach
        Create_cur_a_steach(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk targaid 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        gnìomhaich_àithne()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Mearachd:
        print('tog_tùs Mearachd: ' + str(Mearachd), file=sys.stderr)
        sys.exit(1)
