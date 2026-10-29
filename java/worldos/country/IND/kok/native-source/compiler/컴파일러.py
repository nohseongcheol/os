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
    def __init__(자신, डेटा):
        자신.डेटा = डेटा
        자신.स्थिती = 0

    def 읽기(자신, लांबाय_मोल):
        if लांबाय_मोल < 0 or 자신.स्थिती + लांबाय_मोल > len(자신.डेटा):
            raise 컴파일오류('잘린 वर्ग_मोल_55654bf1 또는 आदेश डेटा')
        मेजप = 자신.डेटा[자신.स्थिती:자신.स्थिती + लांबाय_मोल]
        자신.स्थिती += लांबाय_मोल
        return मेजप

    def 수(자신, स्वरूप_मोल):
        return struct.unpack('>' + स्वरूप_मोल, 자신.읽기(struct.calcsize('>' + स्वरूप_मोल)))[0]


def 수정유티에프해독(डेटा):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    स्ट्रिंग_मोल = डेटा.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return स्ट्रिंग_मोल.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class वर्ग_मोल_55654bf1:
    def __init__(자신, पाथ):
        자신.पाथ = पाथ
        वाचक_मोल = 자료읽기(पाथ.read_bytes())
        if वाचक_मोल.수('I') != 0xcafebabe:
            raise 컴파일오류('Java वर्ग_मोल_55654bf1 표식이 아님')
        वाचक_मोल.읽기(4)
        आयटम_COUNT = वाचक_मोल.수('H')
        자신.अचल_मोल = [None] * आयटम_COUNT
        INDEX = 1
        while INDEX < आयटम_COUNT:
            종류 = वाचक_मोल.수('B')
            if 종류 == 1:
                मोल = 수정유티에프해독(वाचक_मोल.읽기(वाचक_मोल.수('H')))
            elif 종류 == 3:
                मोल = वाचक_मोल.수('i')
            elif 종류 == 4:
                मोल = वाचक_मोल.읽기(4)
            elif 종류 in (5, 6):
                मोल = वाचक_मोल.읽기(8)
            elif 종류 in (7, 8, 16):
                मोल = वाचक_मोल.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                मोल = (वाचक_मोल.수('H'), वाचक_मोल.수('H'))
            elif 종류 == 15:
                मोल = (वाचक_मोल.수('B'), वाचक_मोल.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 अचल_मोल 종류: {}'.format(종류))
            자신.अचल_मोल[INDEX] = (종류, मोल)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.ऍक्सॅस_प्रवेश = वाचक_मोल.수('H')
        자신.नांव = 자신.वर्ग_नांव(वाचक_मोल.수('H'))
        부모 = वाचक_मोल.수('H')
        if 자신.वर्ग_नांव(부모) != 'java/lang/Object' or वाचक_मोल.수('H') != 0:
            raise 컴파일오류(자신.नांव + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.फिल्ड_मोल = 자신.멤버읽기(वाचक_मोल)
        자신.फंक्शन_मोल = 자신.멤버읽기(वाचक_मोल)
        자신.속성읽기(वाचक_मोल)

    def 문자(자신, INDEX):
        if 자신.अचल_मोल[INDEX][0] != 1:
            raise 컴파일오류('स्ट्रिंग_मोल अचल_मोल स्वरूप_मोल चूक')
        return 자신.अचल_मोल[INDEX][1]

    def वर्ग_नांव(자신, INDEX):
        return 자신.문자(자신.अचल_मोल[INDEX][1])

    def संदर्भ(자신, INDEX):
        धनी_मोल, नांव_स्वरूप = 자신.अचल_मोल[INDEX][1]
        नांव, स्वरूप_मोल = 자신.अचल_मोल[नांव_स्वरूप][1]
        return 자신.वर्ग_नांव(धनी_मोल), 자신.문자(नांव), 자신.문자(स्वरूप_मोल)

    def 속성읽기(자신, वाचक_मोल):
        मेजप = {}
        for _ in range(वाचक_मोल.수('H')):
            नांव = 자신.문자(वाचक_मोल.수('H'))
            मेजप[नांव] = वाचक_मोल.읽기(वाचक_मोल.수('I'))
        return मेजप

    def 멤버읽기(자신, वाचक_मोल):
        मेजप = []
        for _ in range(वाचक_मोल.수('H')):
            ऍक्सॅस_प्रवेश = वाचक_मोल.수('H')
            नांव = 자신.문자(वाचक_मोल.수('H'))
            स्वरूप_मोल = 자신.문자(वाचक_मोल.수('H'))
            मेजप.append((ऍक्सॅस_प्रवेश, नांव, स्वरूप_मोल, 자신.속성읽기(वाचक_मोल)))
        return मेजप


def 형식읽기(स्ट्रिंग_मोल):
    मेजप = []
    स्थिती = 0
    while स्थिती < len(स्ट्रिंग_मोल):
        for स्वरूप_मोल in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if स्ट्रिंग_मोल.startswith(स्वरूप_मोल, स्थिती):
                मेजप.append(स्वरूप_मोल)
                स्थिती += len(स्वरूप_मोल)
                break
        else:
            raise 컴파일오류('지원하지 않는 डेटा_प्रकार: ' + स्ट्रिंग_मोल)
    return मेजप


def 함수형식(서술):
    인수, return_मेजप = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    return_TYPE = 형식읽기(return_मेजप)
    if 'V' in 인수 or len(return_TYPE) != 1:
        raise 컴파일오류('फंक्शन_मोल 서술 स्वरूप_मोल चूक: ' + 서술)
    return 인수, return_मेजप


def चिन्न(종류, *부분):
    स्त्रोत = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(स्त्रोत).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 फंक्शन_मोल 서술에 대해서만 허용한다.
def पाळो_दिवचो_आदेश(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK स्त्रोत_ट्री दाळचे_प्रणाली')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/वर्ग_मोल_55654bf1 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 दाळचे_प्रणाली JDK 또는 openjdk-build의 부트 JDK पाथ')
    해석기.add_argument('--bundle-runtime', help='पाळो_दिवचो_आदेश 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर/स्त्रोत_ट्री 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 दाळचे_प्रणाली 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 दाळचे_प्रणाली लक्ष्य (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 दाळचे_प्रणाली 대상의 libc/헤더/लायब्ररी 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 स्वरूप_मोल')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=वर्ग_मोल_55654bf1.फंक्शन_मोल (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.चलोवप (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='पाळो_दिवचो_आदेश ELF/.o 출력; openjdk-build는 전용 दाळचे_प्रणाली 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK स्त्रोत_ट्री 디렉터리 하나와 --java-home 부트 JDK, -o दाळचे_प्रणाली 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as चूक:
            raise 컴파일오류(str(चूक))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build लक्ष्य 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import निर्माण_करचें_प्रवेश
        निर्माण_करचें_प्रवेश(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk लक्ष्य 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        पाळो_दिवचो_आदेश()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as चूक:
        print('दाळचे_स्त्रोत चूक: ' + str(चूक), file=sys.stderr)
        sys.exit(1)
