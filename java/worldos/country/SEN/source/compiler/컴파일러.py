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
    def __init__(자신, mbir):
        자신.mbir = mbir
        자신.위치 = 0

    def 읽기(자신, diir_xëyma):
        if diir_xëyma < 0 or 자신.위치 + diir_xëyma > len(자신.mbir):
            raise 컴파일오류('잘린 maas_xëyma 또는 ndigel mbir')
        결과 = 자신.mbir[자신.위치:자신.위치 + diir_xëyma]
        자신.위치 += diir_xëyma
        return 결과

    def 수(자신, dayo_xëyma):
        return struct.unpack('>' + dayo_xëyma, 자신.읽기(struct.calcsize('>' + dayo_xëyma)))[0]


def 수정유티에프해독(mbir):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    araf_yu_bennoo_xëyma = mbir.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return araf_yu_bennoo_xëyma.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class maas_xëyma:
    def __init__(자신, Yoonu_jëmale):
        자신.Yoonu_jëmale = Yoonu_jëmale
        jangkat_xëyma = 자료읽기(Yoonu_jëmale.read_bytes())
        if jangkat_xëyma.수('I') != 0xcafebabe:
            raise 컴파일오류('Java maas_xëyma 표식이 아님')
        jangkat_xëyma.읽기(4)
        개수 = jangkat_xëyma.수('H')
        자신.Lees_dul_soppi_xëyma = [None] * 개수
        àlluwa_tur = 1
        while àlluwa_tur < 개수:
            종류 = jangkat_xëyma.수('B')
            if 종류 == 1:
                xëyma = 수정유티에프해독(jangkat_xëyma.읽기(jangkat_xëyma.수('H')))
            elif 종류 == 3:
                xëyma = jangkat_xëyma.수('i')
            elif 종류 == 4:
                xëyma = jangkat_xëyma.읽기(4)
            elif 종류 in (5, 6):
                xëyma = jangkat_xëyma.읽기(8)
            elif 종류 in (7, 8, 16):
                xëyma = jangkat_xëyma.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                xëyma = (jangkat_xëyma.수('H'), jangkat_xëyma.수('H'))
            elif 종류 == 15:
                xëyma = (jangkat_xëyma.수('B'), jangkat_xëyma.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 Lees_dul_soppi_xëyma 종류: {}'.format(종류))
            자신.Lees_dul_soppi_xëyma[àlluwa_tur] = (종류, xëyma)
            àlluwa_tur += 2 if 종류 in (5, 6) else 1
        자신.jot_dugal_xabaar = jangkat_xëyma.수('H')
        자신.tur_253d1510 = 자신.maas_tur(jangkat_xëyma.수('H'))
        부모 = jangkat_xëyma.수('H')
        if 자신.maas_tur(부모) != 'java/lang/Object' or jangkat_xëyma.수('H') != 0:
            raise 컴파일오류(자신.tur_253d1510 + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.barabu_denc_ab_joxe_xëyma = 자신.멤버읽기(jangkat_xëyma)
        자신.liëey_xëyma = 자신.멤버읽기(jangkat_xëyma)
        자신.속성읽기(jangkat_xëyma)

    def 문자(자신, àlluwa_tur):
        if 자신.Lees_dul_soppi_xëyma[àlluwa_tur][0] != 1:
            raise 컴파일오류('araf_yu_bennoo_xëyma Lees_dul_soppi_xëyma dayo_xëyma njumte')
        return 자신.Lees_dul_soppi_xëyma[àlluwa_tur][1]

    def maas_tur(자신, àlluwa_tur):
        return 자신.문자(자신.Lees_dul_soppi_xëyma[àlluwa_tur][1])

    def Royukaay(자신, àlluwa_tur):
        boroom_xëyma, tur_dayo = 자신.Lees_dul_soppi_xëyma[àlluwa_tur][1]
        tur_253d1510, dayo_xëyma = 자신.Lees_dul_soppi_xëyma[tur_dayo][1]
        return 자신.maas_tur(boroom_xëyma), 자신.문자(tur_253d1510), 자신.문자(dayo_xëyma)

    def 속성읽기(자신, jangkat_xëyma):
        결과 = {}
        for _ in range(jangkat_xëyma.수('H')):
            tur_253d1510 = 자신.문자(jangkat_xëyma.수('H'))
            결과[tur_253d1510] = jangkat_xëyma.읽기(jangkat_xëyma.수('I'))
        return 결과

    def 멤버읽기(자신, jangkat_xëyma):
        결과 = []
        for _ in range(jangkat_xëyma.수('H')):
            jot_dugal_xabaar = jangkat_xëyma.수('H')
            tur_253d1510 = 자신.문자(jangkat_xëyma.수('H'))
            dayo_xëyma = 자신.문자(jangkat_xëyma.수('H'))
            결과.append((jot_dugal_xabaar, tur_253d1510, dayo_xëyma, 자신.속성읽기(jangkat_xëyma)))
        return 결과


def 형식읽기(araf_yu_bennoo_xëyma):
    결과 = []
    위치 = 0
    while 위치 < len(araf_yu_bennoo_xëyma):
        for dayo_xëyma in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if araf_yu_bennoo_xëyma.startswith(dayo_xëyma, 위치):
                결과.append(dayo_xëyma)
                위치 += len(dayo_xëyma)
                break
        else:
            raise 컴파일오류('지원하지 않는 xéeti_mbir: ' + araf_yu_bennoo_xëyma)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('liëey_xëyma 서술 dayo_xëyma njumte: ' + 서술)
    return 인수, 반환


def sembóol(종류, *부분):
    Cosaan = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(Cosaan).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 liëey_xëyma 서술에 대해서만 허용한다.
def def_ndigel(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK Cosaan_tëralinuy_pàcc tabax_kureel')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/maas_xëyma 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 tabax_kureel JDK 또는 openjdk-build의 부트 JDK Yoonu_jëmale')
    해석기.add_argument('--bundle-runtime', help='def_ndigel 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK jëfekaay_armuwaaru_jëfekaay/Cosaan_tëralinuy_pàcc 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 tabax_kureel 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 tabax_kureel luñu_name (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 tabax_kureel 대상의 libc/헤더/daaray_téere 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 dayo_xëyma')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=maas_xëyma.liëey_xëyma (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.daw (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='def_ndigel ELF/.o 출력; openjdk-build는 전용 tabax_kureel 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK Cosaan_tëralinuy_pàcc 디렉터리 하나와 --java-home 부트 JDK, -o tabax_kureel 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as njumte:
            raise 컴파일오류(str(njumte))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build luñu_name 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import sos_dugal_xabaar
        sos_dugal_xabaar(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk luñu_name 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        def_ndigel()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as njumte:
        print('tabax_Cosaan njumte: ' + str(njumte), file=sys.stderr)
        sys.exit(1)
