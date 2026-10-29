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
    def __init__(자신, titiqqat):
        자신.titiqqat = titiqqat
        자신.위치 = 0

    def 읽기(자신, takininga_atuutilik):
        if takininga_atuutilik < 0 or 자신.위치 + takininga_atuutilik > len(자신.titiqqat):
            raise 컴파일오류('잘린 naliannuungavik_atuutilik 또는 piqujijjut titiqqat')
        결과 = 자신.titiqqat[자신.위치:자신.위치 + takininga_atuutilik]
        자신.위치 += takininga_atuutilik
        return 결과

    def 수(자신, aaqqisurli_atuutilik):
        return struct.unpack('>' + aaqqisurli_atuutilik, 자신.읽기(struct.calcsize('>' + aaqqisurli_atuutilik)))[0]


def 수정유티에프해독(titiqqat):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    qimiaq_atuutilik = titiqqat.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return qimiaq_atuutilik.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class naliannuungavik_atuutilik:
    def __init__(자신, aqqut):
        자신.aqqut = aqqut
        Uqalimaarut_atuutilik = 자료읽기(aqqut.read_bytes())
        if Uqalimaarut_atuutilik.수('I') != 0xcafebabe:
            raise 컴파일오류('Java naliannuungavik_atuutilik 표식이 아님')
        Uqalimaarut_atuutilik.읽기(4)
        개수 = Uqalimaarut_atuutilik.수('H')
        자신.surragunnangittuq_atuutilik = [None] * 개수
        nalunaiqsimavik = 1
        while nalunaiqsimavik < 개수:
            종류 = Uqalimaarut_atuutilik.수('B')
            if 종류 == 1:
                atuutilik = 수정유티에프해독(Uqalimaarut_atuutilik.읽기(Uqalimaarut_atuutilik.수('H')))
            elif 종류 == 3:
                atuutilik = Uqalimaarut_atuutilik.수('i')
            elif 종류 == 4:
                atuutilik = Uqalimaarut_atuutilik.읽기(4)
            elif 종류 in (5, 6):
                atuutilik = Uqalimaarut_atuutilik.읽기(8)
            elif 종류 in (7, 8, 16):
                atuutilik = Uqalimaarut_atuutilik.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                atuutilik = (Uqalimaarut_atuutilik.수('H'), Uqalimaarut_atuutilik.수('H'))
            elif 종류 == 15:
                atuutilik = (Uqalimaarut_atuutilik.수('B'), Uqalimaarut_atuutilik.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 surragunnangittuq_atuutilik 종류: {}'.format(종류))
            자신.surragunnangittuq_atuutilik[nalunaiqsimavik] = (종류, atuutilik)
            nalunaiqsimavik += 2 if 종류 in (5, 6) else 1
        자신.pili_Iliniku = Uqalimaarut_atuutilik.수('H')
        자신.atiq = 자신.naliannuungavik_atiq(Uqalimaarut_atuutilik.수('H'))
        부모 = Uqalimaarut_atuutilik.수('H')
        if 자신.naliannuungavik_atiq(부모) != 'java/lang/Object' or Uqalimaarut_atuutilik.수('H') != 0:
            raise 컴파일오류(자신.atiq + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.kisumuungavik_atuutilik = 자신.멤버읽기(Uqalimaarut_atuutilik)
        자신.sugiakkannirut_atuutilik = 자신.멤버읽기(Uqalimaarut_atuutilik)
        자신.속성읽기(Uqalimaarut_atuutilik)

    def 문자(자신, nalunaiqsimavik):
        if 자신.surragunnangittuq_atuutilik[nalunaiqsimavik][0] != 1:
            raise 컴파일오류('qimiaq_atuutilik surragunnangittuq_atuutilik aaqqisurli_atuutilik tammarniq')
        return 자신.surragunnangittuq_atuutilik[nalunaiqsimavik][1]

    def naliannuungavik_atiq(자신, nalunaiqsimavik):
        return 자신.문자(자신.surragunnangittuq_atuutilik[nalunaiqsimavik][1])

    def 참조(자신, nalunaiqsimavik):
        소유, atiq_aaqqisurli = 자신.surragunnangittuq_atuutilik[nalunaiqsimavik][1]
        atiq, aaqqisurli_atuutilik = 자신.surragunnangittuq_atuutilik[atiq_aaqqisurli][1]
        return 자신.naliannuungavik_atiq(소유), 자신.문자(atiq), 자신.문자(aaqqisurli_atuutilik)

    def 속성읽기(자신, Uqalimaarut_atuutilik):
        결과 = {}
        for _ in range(Uqalimaarut_atuutilik.수('H')):
            atiq = 자신.문자(Uqalimaarut_atuutilik.수('H'))
            결과[atiq] = Uqalimaarut_atuutilik.읽기(Uqalimaarut_atuutilik.수('I'))
        return 결과

    def 멤버읽기(자신, Uqalimaarut_atuutilik):
        결과 = []
        for _ in range(Uqalimaarut_atuutilik.수('H')):
            pili_Iliniku = Uqalimaarut_atuutilik.수('H')
            atiq = 자신.문자(Uqalimaarut_atuutilik.수('H'))
            aaqqisurli_atuutilik = 자신.문자(Uqalimaarut_atuutilik.수('H'))
            결과.append((pili_Iliniku, atiq, aaqqisurli_atuutilik, 자신.속성읽기(Uqalimaarut_atuutilik)))
        return 결과


def 형식읽기(qimiaq_atuutilik):
    결과 = []
    위치 = 0
    while 위치 < len(qimiaq_atuutilik):
        for aaqqisurli_atuutilik in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if qimiaq_atuutilik.startswith(aaqqisurli_atuutilik, 위치):
                결과.append(aaqqisurli_atuutilik)
                위치 += len(aaqqisurli_atuutilik)
                break
        else:
            raise 컴파일오류('지원하지 않는 titiqqat_qanuittut: ' + qimiaq_atuutilik)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('sugiakkannirut_atuutilik 서술 aaqqisurli_atuutilik tammarniq: ' + 서술)
    return 인수, 반환


def 기호(종류, *부분):
    pivviujuq = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(pivviujuq).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 sugiakkannirut_atuutilik 서술에 대해서만 허용한다.
def 실행(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK pivviujuq_attavigiit sanali_qarasaujaq')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/naliannuungavik_atuutilik 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 sanali_qarasaujaq JDK 또는 openjdk-build의 부트 JDK aqqut')
    해석기.add_argument('--bundle-runtime', help='실행 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK 실행기/pivviujuq_attavigiit 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 sanali_qarasaujaq 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 sanali_qarasaujaq turaagaq (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 sanali_qarasaujaq 대상의 libc/헤더/tukisiurvik 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 aaqqisurli_atuutilik')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=naliannuungavik_atuutilik.sugiakkannirut_atuutilik (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.시작 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='실행 ELF/.o 출력; openjdk-build는 전용 sanali_qarasaujaq 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK pivviujuq_attavigiit 디렉터리 하나와 --java-home 부트 JDK, -o sanali_qarasaujaq 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as tammarniq:
            raise 컴파일오류(str(tammarniq))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build turaagaq 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import 만들기
        만들기(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk turaagaq 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        실행()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as tammarniq:
        print('sanali_pivviujuq tammarniq: ' + str(tammarniq), file=sys.stderr)
        sys.exit(1)
