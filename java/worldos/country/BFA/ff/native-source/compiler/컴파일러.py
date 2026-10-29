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
    def __init__(자신, keɓe):
        자신.keɓe = keɓe
        자신.위치 = 0

    def 읽기(자신, njuuteendi_njaru):
        if njuuteendi_njaru < 0 or 자신.위치 + njuuteendi_njaru > len(자신.keɓe):
            raise 컴파일오류('잘린 fedde_njaru 또는 ginol keɓe')
        결과 = 자신.keɓe[자신.위치:자신.위치 + njuuteendi_njaru]
        자신.위치 += njuuteendi_njaru
        return 결과

    def 수(자신, formaa_njaru):
        return struct.unpack('>' + formaa_njaru, 자신.읽기(struct.calcsize('>' + formaa_njaru)))[0]


def 수정유티에프해독(keɓe):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ɓoggol_njaru = keɓe.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ɓoggol_njaru.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class fedde_njaru:
    def __init__(자신, laawol):
        자신.laawol = laawol
        Tarirgal_njaru = 자료읽기(laawol.read_bytes())
        if Tarirgal_njaru.수('I') != 0xcafebabe:
            raise 컴파일오류('Java fedde_njaru 표식이 아님')
        Tarirgal_njaru.읽기(4)
        개수 = Tarirgal_njaru.수('H')
        자신.상수 = [None] * 개수
        joopirdu = 1
        while joopirdu < 개수:
            종류 = Tarirgal_njaru.수('B')
            if 종류 == 1:
                njaru = 수정유티에프해독(Tarirgal_njaru.읽기(Tarirgal_njaru.수('H')))
            elif 종류 == 3:
                njaru = Tarirgal_njaru.수('i')
            elif 종류 == 4:
                njaru = Tarirgal_njaru.읽기(4)
            elif 종류 in (5, 6):
                njaru = Tarirgal_njaru.읽기(8)
            elif 종류 in (7, 8, 16):
                njaru = Tarirgal_njaru.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                njaru = (Tarirgal_njaru.수('H'), Tarirgal_njaru.수('H'))
            elif 종류 == 15:
                njaru = (Tarirgal_njaru.수('B'), Tarirgal_njaru.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 상수 종류: {}'.format(종류))
            자신.상수[joopirdu] = (종류, njaru)
            joopirdu += 2 if 종류 in (5, 6) else 1
        자신.naatde_naatnugol = Tarirgal_njaru.수('H')
        자신.innde = 자신.fedde_innde(Tarirgal_njaru.수('H'))
        부모 = Tarirgal_njaru.수('H')
        if 자신.fedde_innde(부모) != 'java/lang/Object' or Tarirgal_njaru.수('H') != 0:
            raise 컴파일오류(자신.innde + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.suudu_njaru = 자신.멤버읽기(Tarirgal_njaru)
        자신.juɓɓol_njaru = 자신.멤버읽기(Tarirgal_njaru)
        자신.속성읽기(Tarirgal_njaru)

    def 문자(자신, joopirdu):
        if 자신.상수[joopirdu][0] != 1:
            raise 컴파일오류('ɓoggol_njaru 상수 formaa_njaru juumre')
        return 자신.상수[joopirdu][1]

    def fedde_innde(자신, joopirdu):
        return 자신.문자(자신.상수[joopirdu][1])

    def 참조(자신, joopirdu):
        소유, innde_formaa = 자신.상수[joopirdu][1]
        innde, formaa_njaru = 자신.상수[innde_formaa][1]
        return 자신.fedde_innde(소유), 자신.문자(innde), 자신.문자(formaa_njaru)

    def 속성읽기(자신, Tarirgal_njaru):
        결과 = {}
        for _ in range(Tarirgal_njaru.수('H')):
            innde = 자신.문자(Tarirgal_njaru.수('H'))
            결과[innde] = Tarirgal_njaru.읽기(Tarirgal_njaru.수('I'))
        return 결과

    def 멤버읽기(자신, Tarirgal_njaru):
        결과 = []
        for _ in range(Tarirgal_njaru.수('H')):
            naatde_naatnugol = Tarirgal_njaru.수('H')
            innde = 자신.문자(Tarirgal_njaru.수('H'))
            formaa_njaru = 자신.문자(Tarirgal_njaru.수('H'))
            결과.append((naatde_naatnugol, innde, formaa_njaru, 자신.속성읽기(Tarirgal_njaru)))
        return 결과


def 형식읽기(ɓoggol_njaru):
    결과 = []
    위치 = 0
    while 위치 < len(ɓoggol_njaru):
        for formaa_njaru in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ɓoggol_njaru.startswith(formaa_njaru, 위치):
                결과.append(formaa_njaru)
                위치 += len(formaa_njaru)
                break
        else:
            raise 컴파일오류('지원하지 않는 fannu_keɓe: ' + ɓoggol_njaru)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('juɓɓol_njaru 서술 formaa_njaru juumre: ' + 서술)
    return 인수, 반환


def 기호(종류, *부분):
    sewnde = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(sewnde).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 juɓɓol_njaru 서술에 대해서만 허용한다.
def 실행(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK sewnde_lekki tafde_yuɓɓo')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/fedde_njaru 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 tafde_yuɓɓo JDK 또는 openjdk-build의 부트 JDK laawol')
    해석기.add_argument('--bundle-runtime', help='실행 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK 실행기/sewnde_lekki 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 tafde_yuɓɓo 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 tafde_yuɓɓo faandaare (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 tafde_yuɓɓo 대상의 libc/헤더/defterdu 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formaa_njaru')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=fedde_njaru.juɓɓol_njaru (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.huutoraade (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='실행 ELF/.o 출력; openjdk-build는 전용 tafde_yuɓɓo 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK sewnde_lekki 디렉터리 하나와 --java-home 부트 JDK, -o tafde_yuɓɓo 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as juumre:
            raise 컴파일오류(str(juumre))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build faandaare 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import 만들기
        만들기(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk faandaare 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        실행()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as juumre:
        print('tafde_sewnde juumre: ' + str(juumre), file=sys.stderr)
        sys.exit(1)
