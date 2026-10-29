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
    def __init__(자신, data):
        자신.data = data
        자신.위치 = 0

    def 읽기(자신, urefu_thamani):
        if urefu_thamani < 0 or 자신.위치 + urefu_thamani > len(자신.data):
            raise 컴파일오류('잘린 tabaka_thamani_55654bf1 또는 amri data')
        결과 = 자신.data[자신.위치:자신.위치 + urefu_thamani]
        자신.위치 += urefu_thamani
        return 결과

    def 수(자신, umbiza_thamani):
        return struct.unpack('>' + umbiza_thamani, 자신.읽기(struct.calcsize('>' + umbiza_thamani)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    tungo_thamani = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return tungo_thamani.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class tabaka_thamani_55654bf1:
    def __init__(자신, njia):
        자신.njia = njia
        msomaji_thamani = 자료읽기(njia.read_bytes())
        if msomaji_thamani.수('I') != 0xcafebabe:
            raise 컴파일오류('Java tabaka_thamani_55654bf1 표식이 아님')
        msomaji_thamani.읽기(4)
        개수 = msomaji_thamani.수('H')
        자신.kisobadilika_thamani = [None] * 개수
        kielezo = 1
        while kielezo < 개수:
            종류 = msomaji_thamani.수('B')
            if 종류 == 1:
                thamani = 수정유티에프해독(msomaji_thamani.읽기(msomaji_thamani.수('H')))
            elif 종류 == 3:
                thamani = msomaji_thamani.수('i')
            elif 종류 == 4:
                thamani = msomaji_thamani.읽기(4)
            elif 종류 in (5, 6):
                thamani = msomaji_thamani.읽기(8)
            elif 종류 in (7, 8, 16):
                thamani = msomaji_thamani.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                thamani = (msomaji_thamani.수('H'), msomaji_thamani.수('H'))
            elif 종류 == 15:
                thamani = (msomaji_thamani.수('B'), msomaji_thamani.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 kisobadilika_thamani 종류: {}'.format(종류))
            자신.kisobadilika_thamani[kielezo] = (종류, thamani)
            kielezo += 2 if 종류 in (5, 6) else 1
        자신.fikia_ingizo = msomaji_thamani.수('H')
        자신.Jina = 자신.tabaka_jina(msomaji_thamani.수('H'))
        부모 = msomaji_thamani.수('H')
        if 자신.tabaka_jina(부모) != 'java/lang/Object' or msomaji_thamani.수('H') != 0:
            raise 컴파일오류(자신.Jina + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.uga_thamani = 자신.멤버읽기(msomaji_thamani)
        자신.KITENDAKAZI_thamani = 자신.멤버읽기(msomaji_thamani)
        자신.속성읽기(msomaji_thamani)

    def 문자(자신, kielezo):
        if 자신.kisobadilika_thamani[kielezo][0] != 1:
            raise 컴파일오류('tungo_thamani kisobadilika_thamani umbiza_thamani kosa')
        return 자신.kisobadilika_thamani[kielezo][1]

    def tabaka_jina(자신, kielezo):
        return 자신.문자(자신.kisobadilika_thamani[kielezo][1])

    def Marejeleo(자신, kielezo):
        mmiliki_thamani, jina_umbiza = 자신.kisobadilika_thamani[kielezo][1]
        Jina, umbiza_thamani = 자신.kisobadilika_thamani[jina_umbiza][1]
        return 자신.tabaka_jina(mmiliki_thamani), 자신.문자(Jina), 자신.문자(umbiza_thamani)

    def 속성읽기(자신, msomaji_thamani):
        결과 = {}
        for _ in range(msomaji_thamani.수('H')):
            Jina = 자신.문자(msomaji_thamani.수('H'))
            결과[Jina] = msomaji_thamani.읽기(msomaji_thamani.수('I'))
        return 결과

    def 멤버읽기(자신, msomaji_thamani):
        결과 = []
        for _ in range(msomaji_thamani.수('H')):
            fikia_ingizo = msomaji_thamani.수('H')
            Jina = 자신.문자(msomaji_thamani.수('H'))
            umbiza_thamani = 자신.문자(msomaji_thamani.수('H'))
            결과.append((fikia_ingizo, Jina, umbiza_thamani, 자신.속성읽기(msomaji_thamani)))
        return 결과


def 형식읽기(tungo_thamani):
    결과 = []
    위치 = 0
    while 위치 < len(tungo_thamani):
        for umbiza_thamani in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if tungo_thamani.startswith(umbiza_thamani, 위치):
                결과.append(umbiza_thamani)
                위치 += len(umbiza_thamani)
                break
        else:
            raise 컴파일오류('지원하지 않는 aina_ya_data: ' + tungo_thamani)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('KITENDAKAZI_thamani 서술 umbiza_thamani kosa: ' + 서술)
    return 인수, 반환


def ishara(종류, *부분):
    chanzo = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(chanzo).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 KITENDAKAZI_thamani 서술에 대해서만 허용한다.
def tekeleza_amri(인수=None):
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK chanzo_mti jenga_mfumo')
    kichanganuzi_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    kichanganuzi_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/tabaka_thamani_55654bf1 디렉터리')
    kichanganuzi_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 jenga_mfumo JDK 또는 openjdk-build의 부트 JDK njia')
    kichanganuzi_48ee4b1b.add_argument('--bundle-runtime', help='tekeleza_amri 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    kichanganuzi_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK programu_droo_ya_programu/chanzo_mti 빌드의 C 컴파일러')
    kichanganuzi_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    kichanganuzi_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 jenga_mfumo 작업 수')
    kichanganuzi_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 jenga_mfumo lengo (예: aarch64-linux-gnu)')
    kichanganuzi_48ee4b1b.add_argument('--sysroot', help='교차 jenga_mfumo 대상의 libc/헤더/maktaba 루트')
    kichanganuzi_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 umbiza_thamani')
    kichanganuzi_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=tabaka_thamani_55654bf1.KITENDAKAZI_thamani (자체 스택 ABI)')
    kichanganuzi_48ee4b1b.add_argument('--entry', help='예: 계산.endesha (openjdk-build 이외 대상에서 필수)')
    kichanganuzi_48ee4b1b.add_argument('-o', '--output', required=True, help='tekeleza_amri ELF/.o 출력; openjdk-build는 전용 jenga_mfumo 디렉터리')
    kichanganuzi_48ee4b1b.add_argument('sources', nargs='+')
    parameta_hoja = kichanganuzi_48ee4b1b.parse_args(인수)
    if parameta_hoja.target == 'openjdk-build':
        if len(parameta_hoja.sources) != 1 or not parameta_hoja.java_home or parameta_hoja.entry or parameta_hoja.export or parameta_hoja.classpath or parameta_hoja.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK chanzo_mti 디렉터리 하나와 --java-home 부트 JDK, -o jenga_mfumo 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameta_hoja.sources[0], parameta_hoja.output, parameta_hoja.java_home, parameta_hoja.jobs, parameta_hoja.openjdk_target,
                  parameta_hoja.sysroot, None if parameta_hoja.cc == 'cc' else parameta_hoja.cc, parameta_hoja.cxx, parameta_hoja.configure_arg)
        except BuildError as kosa:
            raise 컴파일오류(str(kosa))
        return
    if not parameta_hoja.entry:
        kichanganuzi_48ee4b1b.error('--entry is required for this target')
    if parameta_hoja.cxx or parameta_hoja.openjdk_target or parameta_hoja.sysroot or parameta_hoja.configure_arg or parameta_hoja.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build lengo 전용')
    if parameta_hoja.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import unda_ingizo
        unda_ingizo(parameta_hoja)
        return
    if parameta_hoja.classpath or parameta_hoja.java_home or parameta_hoja.bundle_runtime or parameta_hoja.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk lengo 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameta_hoja.target, '--entry', parameta_hoja.entry, '-o', parameta_hoja.output]
    for pangia_thamani in parameta_hoja.export: 자바명령.extend(['--export', pangia_thamani])
    subprocess.run(자바명령+parameta_hoja.sources, check=True)
    return


if __name__ == '__main__':
    try:
        tekeleza_amri()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as kosa:
        print('jenga_chanzo kosa: ' + str(kosa), file=sys.stderr)
        sys.exit(1)
