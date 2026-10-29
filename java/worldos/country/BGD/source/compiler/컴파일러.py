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
        자신.অবস্থান = 0

    def পড়া(자신, দৈর্ঘ্য_মান):
        if দৈর্ঘ্য_মান < 0 or 자신.অবস্থান + দৈর্ঘ্য_মান > len(자신.ডাটা):
            raise 컴파일오류('잘린 শ্রেণী_মান 또는 আদেশ ডাটা')
        পরিমাপ = 자신.ডাটা[자신.অবস্থান:자신.অবস্থান + দৈর্ঘ্য_মান]
        자신.অবস্থান += দৈর্ঘ্য_মান
        return পরিমাপ

    def 수(자신, বিন্যাস_মান):
        return struct.unpack('>' + বিন্যাস_মান, 자신.পড়া(struct.calcsize('>' + বিন্যাস_মান)))[0]


def 수정유티에프해독(ডাটা):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    স্ট্রিং_মান = ডাটা.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return স্ট্রিং_মান.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class শ্রেণী_মান:
    def __init__(자신, পথ_2):
        자신.পথ_2 = পথ_2
        পাঠক_মান = 자료읽기(পথ_2.read_bytes())
        if পাঠক_মান.수('I') != 0xcafebabe:
            raise 컴파일오류('Java শ্রেণী_মান 표식이 아님')
        পাঠক_মান.পড়া(4)
        개수 = পাঠক_মান.수('H')
        자신.ধ্রুবক_মান = [None] * 개수
        সূচি = 1
        while সূচি < 개수:
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
                raise 컴파일오류('지원하지 않는 ধ্রুবক_মান 종류: {}'.format(종류))
            자신.ধ্রুবক_মান[সূচি] = (종류, মান)
            সূচি += 2 if 종류 in (5, 6) else 1
        자신.অ্যাক্সেস_ভুক্তি = পাঠক_মান.수('H')
        자신.নাম = 자신.শ্রেণী_নাম(পাঠক_মান.수('H'))
        부모 = পাঠক_মান.수('H')
        if 자신.শ্রেণী_নাম(부모) != 'java/lang/Object' or পাঠক_মান.수('H') != 0:
            raise 컴파일오류(자신.নাম + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ক্ষেত্র_মান = 자신.멤버읽기(পাঠক_মান)
        자신.ফাংশন_মান = 자신.멤버읽기(পাঠক_মান)
        자신.속성읽기(পাঠক_মান)

    def 문자(자신, সূচি):
        if 자신.ধ্রুবক_মান[সূচি][0] != 1:
            raise 컴파일오류('স্ট্রিং_মান ধ্রুবক_মান বিন্যাস_মান ত্রুটি')
        return 자신.ধ্রুবক_মান[সূচি][1]

    def শ্রেণী_নাম(자신, সূচি):
        return 자신.문자(자신.ধ্রুবক_মান[সূচি][1])

    def প্রসঙ্গ(자신, সূচি):
        মালিক_মান, নাম_বিন্যাস = 자신.ধ্রুবক_মান[সূচি][1]
        নাম, বিন্যাস_মান = 자신.ধ্রুবক_মান[নাম_বিন্যাস][1]
        return 자신.শ্রেণী_নাম(মালিক_মান), 자신.문자(নাম), 자신.문자(বিন্যাস_মান)

    def 속성읽기(자신, পাঠক_মান):
        পরিমাপ = {}
        for _ in range(পাঠক_মান.수('H')):
            নাম = 자신.문자(পাঠক_মান.수('H'))
            পরিমাপ[নাম] = পাঠক_মান.পড়া(পাঠক_মান.수('I'))
        return পরিমাপ

    def 멤버읽기(자신, পাঠক_মান):
        পরিমাপ = []
        for _ in range(পাঠক_মান.수('H')):
            অ্যাক্সেস_ভুক্তি = পাঠক_মান.수('H')
            নাম = 자신.문자(পাঠক_মান.수('H'))
            বিন্যাস_মান = 자신.문자(পাঠক_মান.수('H'))
            পরিমাপ.append((অ্যাক্সেস_ভুক্তি, নাম, বিন্যাস_মান, 자신.속성읽기(পাঠক_মান)))
        return পরিমাপ


def 형식읽기(স্ট্রিং_মান):
    পরিমাপ = []
    অবস্থান = 0
    while অবস্থান < len(স্ট্রিং_মান):
        for বিন্যাস_মান in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if স্ট্রিং_মান.startswith(বিন্যাস_মান, অবস্থান):
                পরিমাপ.append(বিন্যাস_মান)
                অবস্থান += len(বিন্যাস_মান)
                break
        else:
            raise 컴파일오류('지원하지 않는 ডেটা_ধরণ: ' + স্ট্রিং_মান)
    return পরিমাপ


def 함수형식(서술):
    আর্গুমেন্ট_তালিকা, 반환 = 서술[1:].split(')')
    আর্গুমেন্ট_তালিকা = 형식읽기(আর্গুমেন্ট_তালিকা)
    반환형 = 형식읽기(반환)
    if 'V' in আর্গুমেন্ট_তালিকা or len(반환형) != 1:
        raise 컴파일오류('ফাংশন_মান 서술 বিন্যাস_মান ত্রুটি: ' + 서술)
    return আর্গুমেন্ট_তালিকা, 반환


def প্রতীক(종류, *부분):
    উৎস_নথি = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(উৎস_নথি).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ফাংশন_মান 서술에 대해서만 허용한다.
def কার্যকর_করুন_আদেশ(আর্গুমেন্ট_তালিকা=None):
    পার্সার_48ee4b1b = argparse.ArgumentParser(description='নিজ Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK উত্স_ট্রী গঠন_সিস্টেম')
    পার্সার_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    পার্সার_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/শ্রেণী_মান 디렉터리')
    পার্সার_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 গঠন_সিস্টেম JDK 또는 openjdk-build의 부트 JDK পথ_2')
    পার্সার_48ee4b1b.add_argument('--bundle-runtime', help='কার্যকর_করুন_আদেশ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    পার্সার_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK অ্যাপ_অ্যাপ_লঞ্চার/উত্স_ট্রী 빌드의 C 컴파일러')
    পার্সার_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    পার্সার_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 গঠন_সিস্টেম 작업 수')
    পার্সার_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 গঠন_সিস্টেম লক্ষ্য (예: aarch64-linux-gnu)')
    পার্সার_48ee4b1b.add_argument('--sysroot', help='교차 গঠন_সিস্টেম 대상의 libc/헤더/লাইব্রেরি 루트')
    পার্সার_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 বিন্যাস_মান')
    পার্সার_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=শ্রেণী_মান.ফাংশন_মান (নিজ 스택 ABI)')
    পার্সার_48ee4b1b.add_argument('--entry', help='예: 계산.চালনা (openjdk-build 이외 대상에서 필수)')
    পার্সার_48ee4b1b.add_argument('-o', '--output', required=True, help='কার্যকর_করুন_আদেশ ELF/.o নির্গম; openjdk-build는 전용 গঠন_সিস্টেম 디렉터리')
    পার্সার_48ee4b1b.add_argument('sources', nargs='+')
    প্যারামিটার_যুক্তি = পার্সার_48ee4b1b.parse_args(আর্গুমেন্ট_তালিকা)
    if প্যারামিটার_যুক্তি.target == 'openjdk-build':
        if len(প্যারামিটার_যুক্তি.sources) != 1 or not প্যারামিটার_যুক্তি.java_home or প্যারামিটার_যুক্তি.entry or প্যারামিটার_যুক্তি.export or প্যারামিটার_যুক্তি.classpath or প্যারামিটার_যুক্তি.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK উত্স_ট্রী 디렉터리 하나와 --java-home 부트 JDK, -o গঠন_সিস্টেম 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(প্যারামিটার_যুক্তি.sources[0], প্যারামিটার_যুক্তি.output, প্যারামিটার_যুক্তি.java_home, প্যারামিটার_যুক্তি.jobs, প্যারামিটার_যুক্তি.openjdk_target,
                  প্যারামিটার_যুক্তি.sysroot, None if প্যারামিটার_যুক্তি.cc == 'cc' else প্যারামিটার_যুক্তি.cc, প্যারামিটার_যুক্তি.cxx, প্যারামিটার_যুক্তি.configure_arg)
        except BuildError as ত্রুটি:
            raise 컴파일오류(str(ত্রুটি))
        return
    if not প্যারামিটার_যুক্তি.entry:
        পার্সার_48ee4b1b.error('--entry is required for this target')
    if প্যারামিটার_যুক্তি.cxx or প্যারামিটার_যুক্তি.openjdk_target or প্যারামিটার_যুক্তি.sysroot or প্যারামিটার_যুক্তি.configure_arg or প্যারামিটার_যুক্তি.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build লক্ষ্য 전용')
    if প্যারামিটার_যুক্তি.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ক্রিয়েট_ভুক্তি
        ক্রিয়েট_ভুক্তি(প্যারামিটার_যুক্তি)
        return
    if প্যারামিটার_যুক্তি.classpath or প্যারামিটার_যুক্তি.java_home or প্যারামিটার_যুক্তি.bundle_runtime or প্যারামিটার_যুক্তি.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk লক্ষ্য 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', প্যারামিটার_যুক্তি.target, '--entry', প্যারামিটার_যুক্তি.entry, '-o', প্যারামিটার_যুক্তি.output]
    for নিয়োগ_করুন_মান in প্যারামিটার_যুক্তি.export: 자바명령.extend(['--export', নিয়োগ_করুন_মান])
    subprocess.run(자바명령+প্যারামিটার_যুক্তি.sources, check=True)
    return


if __name__ == '__main__':
    try:
        কার্যকর_করুন_আদেশ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ত্রুটি:
        print('গঠন_উত্স ত্রুটি: ' + str(ত্রুটি), file=sys.stderr)
        sys.exit(1)
