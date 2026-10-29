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
    def __init__(자신, atijaaya):
        자신.atijaaya = atijaaya
        자신.위치 = 0

    def 읽기(자신, akaliaa_ajutuu):
        if akaliaa_ajutuu < 0 or 자신.위치 + akaliaa_ajutuu > len(자신.atijaaya):
            raise 컴파일오류('잘린 akotchijuushi_ajutuu_55654bf1 또는 aluwataaya atijaaya')
        결과 = 자신.atijaaya[자신.위치:자신.위치 + akaliaa_ajutuu]
        자신.위치 += akaliaa_ajutuu
        return 결과

    def 수(자신, akua_ipaa_ajutuu):
        return struct.unpack('>' + akua_ipaa_ajutuu, 자신.읽기(struct.calcsize('>' + akua_ipaa_ajutuu)))[0]


def 수정유티에프해독(atijaaya):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    kaleena_ajutuu = atijaaya.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return kaleena_ajutuu.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class akotchijuushi_ajutuu_55654bf1:
    def __init__(자신, wopu_a_ttaaleemüin):
        자신.wopu_a_ttaaleemüin = wopu_a_ttaaleemüin
        aashaje_erülü_ajutuu = 자료읽기(wopu_a_ttaaleemüin.read_bytes())
        if aashaje_erülü_ajutuu.수('I') != 0xcafebabe:
            raise 컴파일오류('Java akotchijuushi_ajutuu_55654bf1 표식이 아님')
        aashaje_erülü_ajutuu.읽기(4)
        개수 = aashaje_erülü_ajutuu.수('H')
        자신.waneepiajutu_ajutuu = [None] * 개수
        ee_iyatialujuna = 1
        while ee_iyatialujuna < 개수:
            종류 = aashaje_erülü_ajutuu.수('B')
            if 종류 == 1:
                ajutuu = 수정유티에프해독(aashaje_erülü_ajutuu.읽기(aashaje_erülü_ajutuu.수('H')))
            elif 종류 == 3:
                ajutuu = aashaje_erülü_ajutuu.수('i')
            elif 종류 == 4:
                ajutuu = aashaje_erülü_ajutuu.읽기(4)
            elif 종류 in (5, 6):
                ajutuu = aashaje_erülü_ajutuu.읽기(8)
            elif 종류 in (7, 8, 16):
                ajutuu = aashaje_erülü_ajutuu.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ajutuu = (aashaje_erülü_ajutuu.수('H'), aashaje_erülü_ajutuu.수('H'))
            elif 종류 == 15:
                ajutuu = (aashaje_erülü_ajutuu.수('B'), aashaje_erülü_ajutuu.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 waneepiajutu_ajutuu 종류: {}'.format(종류))
            자신.waneepiajutu_ajutuu[ee_iyatialujuna] = (종류, ajutuu)
            ee_iyatialujuna += 2 if 종류 in (5, 6) else 1
        자신.a_ttaaya_ekeroliaa = aashaje_erülü_ajutuu.수('H')
        자신.이름 = 자신.클래스명(aashaje_erülü_ajutuu.수('H'))
        부모 = aashaje_erülü_ajutuu.수('H')
        if 자신.클래스명(부모) != 'java/lang/Object' or aashaje_erülü_ajutuu.수('H') != 0:
            raise 컴파일오류(자신.이름 + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.apülajanaa_ajutuu = 자신.멤버읽기(aashaje_erülü_ajutuu)
        자신.함수 = 자신.멤버읽기(aashaje_erülü_ajutuu)
        자신.속성읽기(aashaje_erülü_ajutuu)

    def 문자(자신, ee_iyatialujuna):
        if 자신.waneepiajutu_ajutuu[ee_iyatialujuna][0] != 1:
            raise 컴파일오류('kaleena_ajutuu waneepiajutu_ajutuu akua_ipaa_ajutuu ajachitia')
        return 자신.waneepiajutu_ajutuu[ee_iyatialujuna][1]

    def 클래스명(자신, ee_iyatialujuna):
        return 자신.문자(자신.waneepiajutu_ajutuu[ee_iyatialujuna][1])

    def 참조(자신, ee_iyatialujuna):
        소유, 이름형식 = 자신.waneepiajutu_ajutuu[ee_iyatialujuna][1]
        이름, akua_ipaa_ajutuu = 자신.waneepiajutu_ajutuu[이름형식][1]
        return 자신.클래스명(소유), 자신.문자(이름), 자신.문자(akua_ipaa_ajutuu)

    def 속성읽기(자신, aashaje_erülü_ajutuu):
        결과 = {}
        for _ in range(aashaje_erülü_ajutuu.수('H')):
            이름 = 자신.문자(aashaje_erülü_ajutuu.수('H'))
            결과[이름] = aashaje_erülü_ajutuu.읽기(aashaje_erülü_ajutuu.수('I'))
        return 결과

    def 멤버읽기(자신, aashaje_erülü_ajutuu):
        결과 = []
        for _ in range(aashaje_erülü_ajutuu.수('H')):
            a_ttaaya_ekeroliaa = aashaje_erülü_ajutuu.수('H')
            이름 = 자신.문자(aashaje_erülü_ajutuu.수('H'))
            akua_ipaa_ajutuu = 자신.문자(aashaje_erülü_ajutuu.수('H'))
            결과.append((a_ttaaya_ekeroliaa, 이름, akua_ipaa_ajutuu, 자신.속성읽기(aashaje_erülü_ajutuu)))
        return 결과


def 형식읽기(kaleena_ajutuu):
    결과 = []
    위치 = 0
    while 위치 < len(kaleena_ajutuu):
        for akua_ipaa_ajutuu in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if kaleena_ajutuu.startswith(akua_ipaa_ajutuu, 위치):
                결과.append(akua_ipaa_ajutuu)
                위치 += len(akua_ipaa_ajutuu)
                break
        else:
            raise 컴파일오류('지원하지 않는 atijaayakua_ipa: ' + kaleena_ajutuu)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('함수 서술 akua_ipaa_ajutuu ajachitia: ' + 서술)
    return 인수, 반환


def 기호(종류, *부분):
    eejeejetülein = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(eejeejetülein).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 함수 서술에 대해서만 허용한다.
def 실행(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK eejeejetülein_wunu_ulia akompiraajaa_a_yatawaajiraaya')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/akotchijuushi_ajutuu_55654bf1 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 akompiraajaa_a_yatawaajiraaya JDK 또는 openjdk-build의 부트 JDK wopu_a_ttaaleemüin')
    해석기.add_argument('--bundle-runtime', help='실행 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK 실행기/eejeejetülein_wunu_ulia 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 akompiraajaa_a_yatawaajiraaya 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 akompiraajaa_a_yatawaajiraaya 대상 (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 akompiraajaa_a_yatawaajiraaya 대상의 libc/헤더/anaajaalee 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 akua_ipaa_ajutuu')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=akotchijuushi_ajutuu_55654bf1.함수 (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.시작 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='실행 ELF/.o 출력; openjdk-build는 전용 akompiraajaa_a_yatawaajiraaya 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK eejeejetülein_wunu_ulia 디렉터리 하나와 --java-home 부트 JDK, -o akompiraajaa_a_yatawaajiraaya 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as ajachitia:
            raise 컴파일오류(str(ajachitia))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build 대상 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import 만들기
        만들기(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk 대상 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        실행()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ajachitia:
        print('akompiraajaa_eejeejetülein ajachitia: ' + str(ajachitia), file=sys.stderr)
        sys.exit(1)
