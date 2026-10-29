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
    def __init__(자신, ডাটা):
        자신.ডাটা = ডাটা
        자신.অৱস্থান = 0

    def পড়া(자신, দৈর্ঘ্য_মান):
        if দৈর্ঘ্য_মান < 0 or 자신.অৱস্থান + দৈর্ঘ্য_মান > len(자신.ডাটা):
            raise 컴파일오류('잘린 শ্ৰেণী_মান 또는 কমান্ড ডাটা')
        পৰিমাপ = 자신.ডাটা[자신.অৱস্থান:자신.অৱস্থান + দৈর্ঘ্য_মান]
        자신.অৱস্থান += দৈর্ঘ্য_মান
        return পৰিমাপ

    def 수(자신, সজ্জা_মান):
        return struct.unpack('>' + সজ্জা_মান, 자신.পড়া(struct.calcsize('>' + সজ্জা_মান)))[0]


def 수정유티에프해독(ডাটা):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ষ্ট্ৰিং_মান = ডাটা.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ষ্ট্ৰিং_মান.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class শ্ৰেণী_মান:
    def __init__(자신, পথ):
        자신.পথ = পথ
        পাঠক_মান = 자료읽기(পথ.read_bytes())
        if পাঠক_মান.수('I') != 0xcafebabe:
            raise 컴파일오류('Java শ্ৰেণী_মান 표식이 아님')
        পাঠক_মান.পড়া(4)
        개수 = পাঠক_মান.수('H')
        자신.ধ্রুৱক_মান = [None] * 개수
        ইনডেক্স = 1
        while ইনডেক্স < 개수:
            종류 = পাঠক_মান.수('B')
            if 종류 == 1:
                মান = 수정유티에프해독(পাঠক_মান.পড়া(পাঠক_মান.수('H')))
            elif 종류 == 3:
                মান = পাঠক_মান.수('i')
            elif 종류 == 4:
                মান = পাঠক_মান.পড়া(4)
            elif 종류 in (5, 6):
                মান = পাঠক_মান.পড়া(8)
            elif 종류 in (7, 8, 16):
                মান = পাঠক_মান.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                মান = (পাঠক_মান.수('H'), পাঠক_মান.수('H'))
            elif 종류 == 15:
                মান = (পাঠক_মান.수('B'), পাঠক_মান.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 ধ্রুৱক_মান 종류: {}'.format(종류))
            자신.ধ্রুৱক_মান[ইনডেক্স] = (종류, মান)
            ইনডেক্স += 2 if 종류 in (5, 6) else 1
        자신.প্ৰৱেশ_কৰক_প্রবিষ্ট = পাঠক_মান.수('H')
        자신.নাম = 자신.শ্ৰেণী_নাম(পাঠক_মান.수('H'))
        부모 = পাঠক_মান.수('H')
        if 자신.শ্ৰেণী_নাম(부모) != 'java/lang/Object' or পাঠক_মান.수('H') != 0:
            raise 컴파일오류(자신.নাম + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ফিল্ড_মান = 자신.멤버읽기(পাঠক_মান)
        자신.ফাংছন_মান = 자신.멤버읽기(পাঠক_মান)
        자신.속성읽기(পাঠক_মান)

    def 문자(자신, ইনডেক্স):
        if 자신.ধ্রুৱক_মান[ইনডেক্স][0] != 1:
            raise 컴파일오류('ষ্ট্ৰিং_মান ধ্রুৱক_মান সজ্জা_মান ত্ৰুটি')
        return 자신.ধ্রুৱক_মান[ইনডেক্স][1]

    def শ্ৰেণী_নাম(자신, ইনডেক্স):
        return 자신.문자(자신.ধ্রুৱক_মান[ইনডেক্স][1])

    def 참조(자신, ইনডেক্স):
        গৰাকী_মান, নাম_সজ্জা = 자신.ধ্রুৱক_মান[ইনডেক্স][1]
        নাম, সজ্জা_মান = 자신.ধ্রুৱক_মান[নাম_সজ্জা][1]
        return 자신.শ্ৰেণী_নাম(গৰাকী_মান), 자신.문자(নাম), 자신.문자(সজ্জা_মান)

    def 속성읽기(자신, পাঠক_মান):
        পৰিমাপ = {}
        for _ in range(পাঠক_মান.수('H')):
            নাম = 자신.문자(পাঠক_মান.수('H'))
            পৰিমাপ[নাম] = পাঠক_মান.পড়া(পাঠক_মান.수('I'))
        return পৰিমাপ

    def 멤버읽기(자신, পাঠক_মান):
        পৰিমাপ = []
        for _ in range(পাঠক_মান.수('H')):
            প্ৰৱেশ_কৰক_প্রবিষ্ট = পাঠক_মান.수('H')
            নাম = 자신.문자(পাঠক_মান.수('H'))
            সজ্জা_মান = 자신.문자(পাঠক_মান.수('H'))
            পৰিমাপ.append((প্ৰৱেশ_কৰক_প্রবিষ্ট, নাম, সজ্জা_মান, 자신.속성읽기(পাঠক_মান)))
        return পৰিমাপ


def 형식읽기(ষ্ট্ৰিং_মান):
    পৰিমাপ = []
    অৱস্থান = 0
    while অৱস্থান < len(ষ্ট্ৰিং_মান):
        for সজ্জা_মান in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ষ্ট্ৰিং_মান.startswith(সজ্জা_মান, অৱস্থান):
                পৰিমাপ.append(সজ্জা_মান)
                অৱস্থান += len(সজ্জা_মান)
                break
        else:
            raise 컴파일오류('지원하지 않는 ডাটা_প্ৰকাৰ: ' + ষ্ট্ৰিং_মান)
    return পৰিমাপ


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('ফাংছন_মান 서술 সজ্জা_মান ত্ৰুটি: ' + 서술)
    return 인수, 반환


def প্ৰতীক(종류, *부분):
    উৎস = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(উৎস).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ফাংছন_মান 서술에 대해서만 허용한다.
def নিষ্পাদন_আদেশ(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK উৎস_ট্ৰি বিল্ড_ছিষ্টেম')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/শ্ৰেণী_মান 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 বিল্ড_ছিষ্টেম JDK 또는 openjdk-build의 부트 JDK পথ')
    해석기.add_argument('--bundle-runtime', help='নিষ্পাদন_আদেশ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK এপ্প্_এপ্প্_ড্ৰৱাৰ/উৎস_ট্ৰি 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 বিল্ড_ছিষ্টেম 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 বিল্ড_ছিষ্টেম লক্ষ্য (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 বিল্ড_ছিষ্টেম 대상의 libc/헤더/লাইব্ৰেৰী 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 সজ্জা_মান')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=শ্ৰেণী_মান.ফাংছন_মান (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.সঞ্চালন (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='নিষ্পাদন_আদেশ ELF/.o নিৰ্গম; openjdk-build는 전용 বিল্ড_ছিষ্টেম 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK উৎস_ট্ৰি 디렉터리 하나와 --java-home 부트 JDK, -o বিল্ড_ছিষ্টেম 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as ত্ৰুটি:
            raise 컴파일오류(str(ত্ৰুটি))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build লক্ষ্য 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ক্ৰিয়েট_প্রবিষ্ট
        ক্ৰিয়েট_প্রবিষ্ট(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk লক্ষ্য 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        নিষ্পাদন_আদেশ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ত্ৰুটি:
        print('বিল্ড_উৎস ত্ৰুটি: ' + str(ত্ৰুটি), file=sys.stderr)
        sys.exit(1)
