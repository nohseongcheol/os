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
    def __init__(자신, raraunga):
        자신.raraunga = raraunga
        자신.tūranga = 0

    def Pānuitia(자신, roa_uara):
        if roa_uara < 0 or 자신.tūranga + roa_uara > len(자신.raraunga):
            raise 컴파일오류('잘린 tauaha_uara 또는 tono raraunga')
        mēhua = 자신.raraunga[자신.tūranga:자신.tūranga + roa_uara]
        자신.tūranga += roa_uara
        return mēhua

    def 수(자신, hōputu_uara):
        return struct.unpack('>' + hōputu_uara, 자신.Pānuitia(struct.calcsize('>' + hōputu_uara)))[0]


def 수정유티에프해독(raraunga):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    aho_uara = raraunga.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return aho_uara.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class tauaha_uara:
    def __init__(자신, ara):
        자신.ara = ara
        Pūpānui_uara = 자료읽기(ara.read_bytes())
        if Pūpānui_uara.수('I') != 0xcafebabe:
            raise 컴파일오류('Java tauaha_uara 표식이 아님')
        Pūpānui_uara.Pānuitia(4)
        tuemi_COUNT = Pūpānui_uara.수('H')
        자신.taimau_uara = [None] * tuemi_COUNT
        INDEX = 1
        while INDEX < tuemi_COUNT:
            종류 = Pūpānui_uara.수('B')
            if 종류 == 1:
                uara = 수정유티에프해독(Pūpānui_uara.Pānuitia(Pūpānui_uara.수('H')))
            elif 종류 == 3:
                uara = Pūpānui_uara.수('i')
            elif 종류 == 4:
                uara = Pūpānui_uara.Pānuitia(4)
            elif 종류 in (5, 6):
                uara = Pūpānui_uara.Pānuitia(8)
            elif 종류 in (7, 8, 16):
                uara = Pūpānui_uara.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                uara = (Pūpānui_uara.수('H'), Pūpānui_uara.수('H'))
            elif 종류 == 15:
                uara = (Pūpānui_uara.수('B'), Pūpānui_uara.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 taimau_uara 종류: {}'.format(종류))
            자신.taimau_uara[INDEX] = (종류, uara)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.uru_tāurunga = Pūpānui_uara.수('H')
        자신.Ingoa = 자신.tauaha_ingoa(Pūpānui_uara.수('H'))
        부모 = Pūpānui_uara.수('H')
        if 자신.tauaha_ingoa(부모) != 'java/lang/Object' or Pūpānui_uara.수('H') != 0:
            raise 컴파일오류(자신.Ingoa + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.āpure_uara = 자신.멤버읽기(Pūpānui_uara)
        자신.TAUMAHI_uara = 자신.멤버읽기(Pūpānui_uara)
        자신.속성읽기(Pūpānui_uara)

    def 문자(자신, INDEX):
        if 자신.taimau_uara[INDEX][0] != 1:
            raise 컴파일오류('aho_uara taimau_uara hōputu_uara Pōhēhē')
        return 자신.taimau_uara[INDEX][1]

    def tauaha_ingoa(자신, INDEX):
        return 자신.문자(자신.taimau_uara[INDEX][1])

    def Pūranga_kōrero(자신, INDEX):
        kaipupuri_uara, ingoa_hōputu = 자신.taimau_uara[INDEX][1]
        Ingoa, hōputu_uara = 자신.taimau_uara[ingoa_hōputu][1]
        return 자신.tauaha_ingoa(kaipupuri_uara), 자신.문자(Ingoa), 자신.문자(hōputu_uara)

    def 속성읽기(자신, Pūpānui_uara):
        mēhua = {}
        for _ in range(Pūpānui_uara.수('H')):
            Ingoa = 자신.문자(Pūpānui_uara.수('H'))
            mēhua[Ingoa] = Pūpānui_uara.Pānuitia(Pūpānui_uara.수('I'))
        return mēhua

    def 멤버읽기(자신, Pūpānui_uara):
        mēhua = []
        for _ in range(Pūpānui_uara.수('H')):
            uru_tāurunga = Pūpānui_uara.수('H')
            Ingoa = 자신.문자(Pūpānui_uara.수('H'))
            hōputu_uara = 자신.문자(Pūpānui_uara.수('H'))
            mēhua.append((uru_tāurunga, Ingoa, hōputu_uara, 자신.속성읽기(Pūpānui_uara)))
        return mēhua


def 형식읽기(aho_uara):
    mēhua = []
    tūranga = 0
    while tūranga < len(aho_uara):
        for hōputu_uara in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if aho_uara.startswith(hōputu_uara, tūranga):
                mēhua.append(hōputu_uara)
                tūranga += len(hōputu_uara)
                break
        else:
            raise 컴파일오류('지원하지 않는 momo_raraunga: ' + aho_uara)
    return mēhua


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('TAUMAHI_uara 서술 hōputu_uara Pōhēhē: ' + 서술)
    return 인수, 반환


def tohu(종류, *부분):
    pūtake = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(pūtake).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 TAUMAHI_uara 서술에 대해서만 허용한다.
def kawe_tono(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK pūtake_rākau hanga_pūnaha')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/tauaha_uara 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 hanga_pūnaha JDK 또는 openjdk-build의 부트 JDK ara')
    해석기.add_argument('--bundle-runtime', help='kawe_tono 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK kaupapa_pūwhiri_taupānga/pūtake_rākau 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 hanga_pūnaha 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 hanga_pūnaha ūnga (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 hanga_pūnaha 대상의 libc/헤더/puna 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 hōputu_uara')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=tauaha_uara.TAUMAHI_uara (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.whakahaere (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='kawe_tono ELF/.o 출력; openjdk-build는 전용 hanga_pūnaha 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK pūtake_rākau 디렉터리 하나와 --java-home 부트 JDK, -o hanga_pūnaha 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Pōhēhē:
            raise 컴파일오류(str(Pōhēhē))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ūnga 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Waihanga_tāurunga
        Waihanga_tāurunga(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ūnga 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for tautapa_uara in 인자.export: 자바명령.extend(['--export', tautapa_uara])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        kawe_tono()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Pōhēhē:
        print('hanga_pūtake Pōhēhē: ' + str(Pōhēhē), file=sys.stderr)
        sys.exit(1)
