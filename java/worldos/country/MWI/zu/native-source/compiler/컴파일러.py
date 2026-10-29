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
    def __init__(자신, imininingwane):
        자신.imininingwane = imininingwane
        자신.위치 = 0

    def Funda(자신, ubude_inani):
        if ubude_inani < 0 or 자신.위치 + ubude_inani > len(자신.imininingwane):
            raise 컴파일오류('잘린 uhlobo_inani 또는 Umlayelo imininingwane')
        결과 = 자신.imininingwane[자신.위치:자신.위치 + ubude_inani]
        자신.위치 += ubude_inani
        return 결과

    def 수(자신, misa_inani):
        return struct.unpack('>' + misa_inani, 자신.Funda(struct.calcsize('>' + misa_inani)))[0]


def 수정유티에프해독(imininingwane):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    uchunge_inani = imininingwane.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return uchunge_inani.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class uhlobo_inani:
    def __init__(자신, Indlela_2):
        자신.Indlela_2 = Indlela_2
        umfundi_inani = 자료읽기(Indlela_2.read_bytes())
        if umfundi_inani.수('I') != 0xcafebabe:
            raise 컴파일오류('Java uhlobo_inani 표식이 아님')
        umfundi_inani.Funda(4)
        개수 = umfundi_inani.수('H')
        자신.okungaguquki_inani = [None] * 개수
        thola_inkomba = 1
        while thola_inkomba < 개수:
            종류 = umfundi_inani.수('B')
            if 종류 == 1:
                inani = 수정유티에프해독(umfundi_inani.Funda(umfundi_inani.수('H')))
            elif 종류 == 3:
                inani = umfundi_inani.수('i')
            elif 종류 == 4:
                inani = umfundi_inani.Funda(4)
            elif 종류 in (5, 6):
                inani = umfundi_inani.Funda(8)
            elif 종류 in (7, 8, 16):
                inani = umfundi_inani.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                inani = (umfundi_inani.수('H'), umfundi_inani.수('H'))
            elif 종류 == 15:
                inani = (umfundi_inani.수('B'), umfundi_inani.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 okungaguquki_inani 종류: {}'.format(종류))
            자신.okungaguquki_inani[thola_inkomba] = (종류, inani)
            thola_inkomba += 2 if 종류 in (5, 6) else 1
        자신.ungeno_okufakwayo = umfundi_inani.수('H')
        자신.Igama = 자신.uhlobo_igama(umfundi_inani.수('H'))
        부모 = umfundi_inani.수('H')
        if 자신.uhlobo_igama(부모) != 'java/lang/Object' or umfundi_inani.수('H') != 0:
            raise 컴파일오류(자신.Igama + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.inkundla_indawana_inani = 자신.멤버읽기(umfundi_inani)
        자신.umsebenzi_inani = 자신.멤버읽기(umfundi_inani)
        자신.속성읽기(umfundi_inani)

    def 문자(자신, thola_inkomba):
        if 자신.okungaguquki_inani[thola_inkomba][0] != 1:
            raise 컴파일오류('uchunge_inani okungaguquki_inani misa_inani Iphutha')
        return 자신.okungaguquki_inani[thola_inkomba][1]

    def uhlobo_igama(자신, thola_inkomba):
        return 자신.문자(자신.okungaguquki_inani[thola_inkomba][1])

    def Ireferensi(자신, thola_inkomba):
        umnikazi_inani, igama_misa = 자신.okungaguquki_inani[thola_inkomba][1]
        Igama, misa_inani = 자신.okungaguquki_inani[igama_misa][1]
        return 자신.uhlobo_igama(umnikazi_inani), 자신.문자(Igama), 자신.문자(misa_inani)

    def 속성읽기(자신, umfundi_inani):
        결과 = {}
        for _ in range(umfundi_inani.수('H')):
            Igama = 자신.문자(umfundi_inani.수('H'))
            결과[Igama] = umfundi_inani.Funda(umfundi_inani.수('I'))
        return 결과

    def 멤버읽기(자신, umfundi_inani):
        결과 = []
        for _ in range(umfundi_inani.수('H')):
            ungeno_okufakwayo = umfundi_inani.수('H')
            Igama = 자신.문자(umfundi_inani.수('H'))
            misa_inani = 자신.문자(umfundi_inani.수('H'))
            결과.append((ungeno_okufakwayo, Igama, misa_inani, 자신.속성읽기(umfundi_inani)))
        return 결과


def 형식읽기(uchunge_inani):
    결과 = []
    위치 = 0
    while 위치 < len(uchunge_inani):
        for misa_inani in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if uchunge_inani.startswith(misa_inani, 위치):
                결과.append(misa_inani)
                위치 += len(misa_inani)
                break
        else:
            raise 컴파일오류('지원하지 않는 uhlobo_lwemininingwane: ' + uchunge_inani)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('umsebenzi_inani 서술 misa_inani Iphutha: ' + 서술)
    return 인수, 반환


def uphawu_ad6f1a96(종류, *부분):
    umthombo = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(umthombo).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 umsebenzi_inani 서술에 대해서만 허용한다.
def yenza_umyalo(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK umthombo_isihlahla akha_isistimu')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/uhlobo_inani 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 akha_isistimu JDK 또는 openjdk-build의 부트 JDK Indlela_2')
    해석기.add_argument('--bundle-runtime', help='yenza_umyalo 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK i_app_ikhabethe_le_app/umthombo_isihlahla 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 akha_isistimu 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 akha_isistimu impokophelo (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 akha_isistimu 대상의 libc/헤더/umtapo 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 misa_inani')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=uhlobo_inani.umsebenzi_inani (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Sebenzisa (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='yenza_umyalo ELF/.o 출력; openjdk-build는 전용 akha_isistimu 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK umthombo_isihlahla 디렉터리 하나와 --java-home 부트 JDK, -o akha_isistimu 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Iphutha:
            raise 컴파일오류(str(Iphutha))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build impokophelo 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import yakha_okufakwayo
        yakha_okufakwayo(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk impokophelo 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for yabela_inani in 인자.export: 자바명령.extend(['--export', yabela_inani])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        yenza_umyalo()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Iphutha:
        print('akha_umthombo Iphutha: ' + str(Iphutha), file=sys.stderr)
        sys.exit(1)
