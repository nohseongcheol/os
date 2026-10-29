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
    def __init__(자신, ᎦᏟᏌᏅᎯ):
        자신.ᎦᏟᏌᏅᎯ = ᎦᏟᏌᏅᎯ
        자신.위치 = 0

    def 읽기(자신, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ):
        if ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ < 0 or 자신.위치 + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ > len(자신.ᎦᏟᏌᏅᎯ):
            raise 컴파일오류('잘린 ᏄᏍᏛᎢ_ᏧᎬᏩᎶᏗᏯ 또는 ᎤᏁᏤᎸᎩ ᎦᏟᏌᏅᎯ')
        결과 = 자신.ᎦᏟᏌᏅᎯ[자신.위치:자신.위치 + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ]
        자신.위치 += ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ
        return 결과

    def 수(자신, ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ):
        return struct.unpack('>' + ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ, 자신.읽기(struct.calcsize('>' + ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ)))[0]


def 수정유티에프해독(ᎦᏟᏌᏅᎯ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ = ᎦᏟᏌᏅᎯ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ᏄᏍᏛᎢ_ᏧᎬᏩᎶᏗᏯ:
    def __init__(자신, ᎠᏍᏓᏩᏛᏍᏗ):
        자신.ᎠᏍᏓᏩᏛᏍᏗ = ᎠᏍᏓᏩᏛᏍᏗ
        ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ = 자료읽기(ᎠᏍᏓᏩᏛᏍᏗ.read_bytes())
        if ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ᏄᏍᏛᎢ_ᏧᎬᏩᎶᏗᏯ 표식이 아님')
        ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.읽기(4)
        개수 = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H')
        자신.상수 = [None] * 개수
        ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 1
        while ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 개수:
            종류 = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('B')
            if 종류 == 1:
                ᏧᎬᏩᎶᏗᏯ = 수정유티에프해독(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.읽기(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H')))
            elif 종류 == 3:
                ᏧᎬᏩᎶᏗᏯ = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('i')
            elif 종류 == 4:
                ᏧᎬᏩᎶᏗᏯ = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.읽기(4)
            elif 종류 in (5, 6):
                ᏧᎬᏩᎶᏗᏯ = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.읽기(8)
            elif 종류 in (7, 8, 16):
                ᏧᎬᏩᎶᏗᏯ = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ᏧᎬᏩᎶᏗᏯ = (ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H'), ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H'))
            elif 종류 == 15:
                ᏧᎬᏩᎶᏗᏯ = (ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('B'), ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 상수 종류: {}'.format(종류))
            자신.상수[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] = (종류, ᏧᎬᏩᎶᏗᏯ)
            ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ += 2 if 종류 in (5, 6) else 1
        자신.ᎬᏴᏍᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H')
        자신.ᏚᏙᎥᎢ = 자신.ᏄᏍᏛᎢ_ᏚᏙᎥᎢ(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H'))
        부모 = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H')
        if 자신.ᏄᏍᏛᎢ_ᏚᏙᎥᎢ(부모) != 'java/lang/Object' or ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H') != 0:
            raise 컴파일오류(자신.ᏚᏙᎥᎢ + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ᏠᎨᏏ_ᏧᎬᏩᎶᏗᏯ = 자신.멤버읽기(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ)
        자신.ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ = 자신.멤버읽기(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ)
        자신.속성읽기(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ)

    def 문자(자신, ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ):
        if 자신.상수[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ][0] != 1:
            raise 컴파일오류('ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ 상수 ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ ᎦᎵᏓᏍᏔᏅ')
        return 자신.상수[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ][1]

    def ᏄᏍᏛᎢ_ᏚᏙᎥᎢ(자신, ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ):
        return 자신.문자(자신.상수[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ][1])

    def 참조(자신, ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ):
        ᎣᏤᎵᎢ_ᏧᎬᏩᎶᏗᏯ, ᏚᏙᎥᎢ_ᏱᎬᏁᎸᎯ = 자신.상수[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ][1]
        ᏚᏙᎥᎢ, ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ = 자신.상수[ᏚᏙᎥᎢ_ᏱᎬᏁᎸᎯ][1]
        return 자신.ᏄᏍᏛᎢ_ᏚᏙᎥᎢ(ᎣᏤᎵᎢ_ᏧᎬᏩᎶᏗᏯ), 자신.문자(ᏚᏙᎥᎢ), 자신.문자(ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ)

    def 속성읽기(자신, ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ):
        결과 = {}
        for _ in range(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H')):
            ᏚᏙᎥᎢ = 자신.문자(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H'))
            결과[ᏚᏙᎥᎢ] = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.읽기(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('I'))
        return 결과

    def 멤버읽기(자신, ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ):
        결과 = []
        for _ in range(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H')):
            ᎬᏴᏍᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ = ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H')
            ᏚᏙᎥᎢ = 자신.문자(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H'))
            ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ = 자신.문자(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ.수('H'))
            결과.append((ᎬᏴᏍᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ, ᏚᏙᎥᎢ, ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ, 자신.속성읽기(ᏗᎪᎵᏰᏍᎩ_ᏧᎬᏩᎶᏗᏯ)))
        return 결과


def 형식읽기(ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ):
    결과 = []
    위치 = 0
    while 위치 < len(ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ):
        for ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ.startswith(ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ, 위치):
                결과.append(ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ)
                위치 += len(ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ)
                break
        else:
            raise 컴파일오류('지원하지 않는 ᎦᏟᏌᏅᎯ_ᎢᏳᏍᏗ: ' + ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ 서술 ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ ᎦᎵᏓᏍᏔᏅ: ' + 서술)
    return 인수, 반환


def 기호(종류, *부분):
    ᎦᏟᏌᏅᎯ_0201f362 = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ᎦᏟᏌᏅᎯ_0201f362).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ 서술에 대해서만 허용한다.
def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ᎦᏟᏌᏅᎯ_ᏡᎬ ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ᏄᏍᏛᎢ_ᏧᎬᏩᎶᏗᏯ 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ JDK 또는 openjdk-build의 부트 JDK ᎠᏍᏓᏩᏛᏍᏗ')
    해석기.add_argument('--bundle-runtime', help='ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK 실행기/ᎦᏟᏌᏅᎯ_ᏡᎬ 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ ᎠᏉᏅᏗᎢ (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 대상의 libc/헤더/ᏧᏂᎪᎵᏰᏗᎢ 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=ᏄᏍᏛᎢ_ᏧᎬᏩᎶᏗᏯ.ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ᎠᎢᏎᏍᏗ (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ ELF/.o 출력; openjdk-build는 전용 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ᎦᏟᏌᏅᎯ_ᏡᎬ 디렉터리 하나와 --java-home 부트 JDK, -o ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as ᎦᎵᏓᏍᏔᏅ:
            raise 컴파일오류(str(ᎦᎵᏓᏍᏔᏅ))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ᎠᏉᏅᏗᎢ 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import 만들기
        만들기(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ᎠᏉᏅᏗᎢ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ᎦᎵᏓᏍᏔᏅ:
        print('ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ ᎦᎵᏓᏍᏔᏅ: ' + str(ᎦᎵᏓᏍᏔᏅ), file=sys.stderr)
        sys.exit(1)
