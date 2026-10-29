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
    def __init__(자신, tshedimosetso):
        자신.tshedimosetso = tshedimosetso
        자신.위치 = 0

    def 읽기(자신, boleele_Boleng):
        if boleele_Boleng < 0 or 자신.위치 + boleele_Boleng > len(자신.tshedimosetso):
            raise 컴파일오류('잘린 mofuta_Boleng 또는 Taelo tshedimosetso')
        결과 = 자신.tshedimosetso[자신.위치:자신.위치 + boleele_Boleng]
        자신.위치 += boleele_Boleng
        return 결과

    def 수(자신, fometa_Boleng):
        return struct.unpack('>' + fometa_Boleng, 자신.읽기(struct.calcsize('>' + fometa_Boleng)))[0]


def 수정유티에프해독(tshedimosetso):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    dikwalwa_Boleng = tshedimosetso.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return dikwalwa_Boleng.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class mofuta_Boleng:
    def __init__(자신, tsela):
        자신.tsela = tsela
        mmuisi_Boleng = 자료읽기(tsela.read_bytes())
        if mmuisi_Boleng.수('I') != 0xcafebabe:
            raise 컴파일오류('Java mofuta_Boleng 표식이 아님')
        mmuisi_Boleng.읽기(4)
        개수 = mmuisi_Boleng.수('H')
        자신.tlhomameng_Boleng = [None] * 개수
        tshupane = 1
        while tshupane < 개수:
            종류 = mmuisi_Boleng.수('B')
            if 종류 == 1:
                Boleng = 수정유티에프해독(mmuisi_Boleng.읽기(mmuisi_Boleng.수('H')))
            elif 종류 == 3:
                Boleng = mmuisi_Boleng.수('i')
            elif 종류 == 4:
                Boleng = mmuisi_Boleng.읽기(4)
            elif 종류 in (5, 6):
                Boleng = mmuisi_Boleng.읽기(8)
            elif 종류 in (7, 8, 16):
                Boleng = mmuisi_Boleng.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                Boleng = (mmuisi_Boleng.수('H'), mmuisi_Boleng.수('H'))
            elif 종류 == 15:
                Boleng = (mmuisi_Boleng.수('B'), mmuisi_Boleng.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 tlhomameng_Boleng 종류: {}'.format(종류))
            자신.tlhomameng_Boleng[tshupane] = (종류, Boleng)
            tshupane += 2 if 종류 in (5, 6) else 1
        자신.letlelesega_tsenyo = mmuisi_Boleng.수('H')
        자신.leina = 자신.mofuta_leina(mmuisi_Boleng.수('H'))
        부모 = mmuisi_Boleng.수('H')
        if 자신.mofuta_leina(부모) != 'java/lang/Object' or mmuisi_Boleng.수('H') != 0:
            raise 컴파일오류(자신.leina + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.lefelo_Boleng = 자신.멤버읽기(mmuisi_Boleng)
        자신.TIRISO_Boleng = 자신.멤버읽기(mmuisi_Boleng)
        자신.속성읽기(mmuisi_Boleng)

    def 문자(자신, tshupane):
        if 자신.tlhomameng_Boleng[tshupane][0] != 1:
            raise 컴파일오류('dikwalwa_Boleng tlhomameng_Boleng fometa_Boleng phoso')
        return 자신.tlhomameng_Boleng[tshupane][1]

    def mofuta_leina(자신, tshupane):
        return 자신.문자(자신.tlhomameng_Boleng[tshupane][1])

    def Tshupiso(자신, tshupane):
        mong_Boleng, leina_fometa = 자신.tlhomameng_Boleng[tshupane][1]
        leina, fometa_Boleng = 자신.tlhomameng_Boleng[leina_fometa][1]
        return 자신.mofuta_leina(mong_Boleng), 자신.문자(leina), 자신.문자(fometa_Boleng)

    def 속성읽기(자신, mmuisi_Boleng):
        결과 = {}
        for _ in range(mmuisi_Boleng.수('H')):
            leina = 자신.문자(mmuisi_Boleng.수('H'))
            결과[leina] = mmuisi_Boleng.읽기(mmuisi_Boleng.수('I'))
        return 결과

    def 멤버읽기(자신, mmuisi_Boleng):
        결과 = []
        for _ in range(mmuisi_Boleng.수('H')):
            letlelesega_tsenyo = mmuisi_Boleng.수('H')
            leina = 자신.문자(mmuisi_Boleng.수('H'))
            fometa_Boleng = 자신.문자(mmuisi_Boleng.수('H'))
            결과.append((letlelesega_tsenyo, leina, fometa_Boleng, 자신.속성읽기(mmuisi_Boleng)))
        return 결과


def 형식읽기(dikwalwa_Boleng):
    결과 = []
    위치 = 0
    while 위치 < len(dikwalwa_Boleng):
        for fometa_Boleng in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if dikwalwa_Boleng.startswith(fometa_Boleng, 위치):
                결과.append(fometa_Boleng)
                위치 += len(fometa_Boleng)
                break
        else:
            raise 컴파일오류('지원하지 않는 mofutatshedimosetso: ' + dikwalwa_Boleng)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('TIRISO_Boleng 서술 fometa_Boleng phoso: ' + 서술)
    return 인수, 반환


def letshwao(종류, *부분):
    Motswedi = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Motswedi).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 TIRISO_Boleng 서술에 대해서만 허용한다.
def diragatsa_Taelo(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK Motswedi_sebopego_sa_tshedimosetso aga_tsamaiso')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/mofuta_Boleng 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 aga_tsamaiso JDK 또는 openjdk-build의 부트 JDK tsela')
    해석기.add_argument('--bundle-runtime', help='diragatsa_Taelo 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK Tiriso_llae_ya_sediriso/Motswedi_sebopego_sa_tshedimosetso 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 aga_tsamaiso 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 aga_tsamaiso setotwa (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 aga_tsamaiso 대상의 libc/헤더/laeborari 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 fometa_Boleng')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=mofuta_Boleng.TIRISO_Boleng (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.dirisa (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='diragatsa_Taelo ELF/.o 출력; openjdk-build는 전용 aga_tsamaiso 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK Motswedi_sebopego_sa_tshedimosetso 디렉터리 하나와 --java-home 부트 JDK, -o aga_tsamaiso 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as phoso:
            raise 컴파일오류(str(phoso))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build setotwa 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import tlhama_tsenyo
        tlhama_tsenyo(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk setotwa 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for abela_Boleng in 인자.export: 자바명령.extend(['--export', abela_Boleng])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        diragatsa_Taelo()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as phoso:
        print('aga_Motswedi phoso: ' + str(phoso), file=sys.stderr)
        sys.exit(1)
