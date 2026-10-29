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
    def __init__(자신, लगत):
        자신.लगत = लगत
        자신.स्थिति = 0

    def पढनुहोस्(자신, लम्बाइ_मान):
        if लम्बाइ_मान < 0 or 자신.स्थिति + लम्बाइ_मान > len(자신.लगत):
            raise 컴파일오류('잘린 वर्ग_मान 또는 आदेश लगत')
        मापन = 자신.लगत[자신.स्थिति:자신.स्थिति + लम्बाइ_मान]
        자신.स्थिति += लम्बाइ_मान
        return मापन

    def 수(자신, ढाँचा_मान):
        return struct.unpack('>' + ढाँचा_मान, 자신.पढनुहोस्(struct.calcsize('>' + ढाँचा_मान)))[0]


def 수정유티에프해독(लगत):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    स्ट्रिङ_मान = लगत.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return स्ट्रिङ_मान.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class वर्ग_मान:
    def __init__(자신, मार्ग):
        자신.मार्ग = मार्ग
        पाठक_मान = 자료읽기(मार्ग.read_bytes())
        if पाठक_मान.수('I') != 0xcafebabe:
            raise 컴파일오류('Java वर्ग_मान 표식이 아님')
        पाठक_मान.पढनुहोस्(4)
        개수 = पाठक_मान.수('H')
        자신.अचल_मान = [None] * 개수
        अनुक्रमणिका = 1
        while अनुक्रमणिका < 개수:
            종류 = पाठक_मान.수('B')
            if 종류 == 1:
                मान = 수정유티에프해독(पाठक_मान.पढनुहोस्(पाठक_मान.수('H')))
            elif 종류 == 3:
                मान = पाठक_मान.수('i')
            elif 종류 == 4:
                मान = पाठक_मान.पढनुहोस्(4)
            elif 종류 in (5, 6):
                मान = पाठक_मान.पढनुहोस्(8)
            elif 종류 in (7, 8, 16):
                मान = पाठक_मान.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                मान = (पाठक_मान.수('H'), पाठक_मान.수('H'))
            elif 종류 == 15:
                मान = (पाठक_मान.수('B'), पाठक_मान.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 अचल_मान 종류: {}'.format(종류))
            자신.अचल_मान[अनुक्रमणिका] = (종류, मान)
            अनुक्रमणिका += 2 if 종류 in (5, 6) else 1
        자신.पहुँच_प्रविष्टि = पाठक_मान.수('H')
        자신.नाम = 자신.वर्ग_नाम(पाठक_मान.수('H'))
        부모 = पाठक_मान.수('H')
        if 자신.वर्ग_नाम(부모) != 'java/lang/Object' or पाठक_मान.수('H') != 0:
            raise 컴파일오류(자신.नाम + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.फाँट_मान = 자신.멤버읽기(पाठक_मान)
        자신.प्रकार्य_मान = 자신.멤버읽기(पाठक_मान)
        자신.속성읽기(पाठक_मान)

    def 문자(자신, अनुक्रमणिका):
        if 자신.अचल_मान[अनुक्रमणिका][0] != 1:
            raise 컴파일오류('स्ट्रिङ_मान अचल_मान ढाँचा_मान त्रुटि')
        return 자신.अचल_मान[अनुक्रमणिका][1]

    def वर्ग_नाम(자신, अनुक्रमणिका):
        return 자신.문자(자신.अचल_मान[अनुक्रमणिका][1])

    def निर्देश(자신, अनुक्रमणिका):
        मालिक_मान, नाम_ढाँचा = 자신.अचल_मान[अनुक्रमणिका][1]
        नाम, ढाँचा_मान = 자신.अचल_मान[नाम_ढाँचा][1]
        return 자신.वर्ग_नाम(मालिक_मान), 자신.문자(नाम), 자신.문자(ढाँचा_मान)

    def 속성읽기(자신, पाठक_मान):
        मापन = {}
        for _ in range(पाठक_मान.수('H')):
            नाम = 자신.문자(पाठक_मान.수('H'))
            मापन[नाम] = पाठक_मान.पढनुहोस्(पाठक_मान.수('I'))
        return मापन

    def 멤버읽기(자신, पाठक_मान):
        मापन = []
        for _ in range(पाठक_मान.수('H')):
            पहुँच_प्रविष्टि = पाठक_मान.수('H')
            नाम = 자신.문자(पाठक_मान.수('H'))
            ढाँचा_मान = 자신.문자(पाठक_मान.수('H'))
            मापन.append((पहुँच_प्रविष्टि, नाम, ढाँचा_मान, 자신.속성읽기(पाठक_मान)))
        return मापन


def 형식읽기(स्ट्रिङ_मान):
    मापन = []
    स्थिति = 0
    while स्थिति < len(स्ट्रिङ_मान):
        for ढाँचा_मान in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if स्ट्रिङ_मान.startswith(ढाँचा_मान, स्थिति):
                मापन.append(ढाँचा_मान)
                स्थिति += len(ढाँचा_मान)
                break
        else:
            raise 컴파일오류('지원하지 않는 लगत_प्रकार: ' + स्ट्रिङ_मान)
    return मापन


def 함수형식(서술):
    तर्क, 반환 = 서술[1:].split(')')
    तर्क = 형식읽기(तर्क)
    반환형 = 형식읽기(반환)
    if 'V' in तर्क or len(반환형) != 1:
        raise 컴파일오류('प्रकार्य_मान 서술 ढाँचा_मान त्रुटि: ' + 서술)
    return तर्क, 반환


def चिन्ह(종류, *부분):
    स्रोत = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(स्रोत).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 प्रकार्य_मान 서술에 대해서만 허용한다.
def कार्यान्वयन_गर्नुहोस्_आदेश(तर्क=None):
    해석기 = argparse.ArgumentParser(description='निज Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK स्रोत_वृक्ष बनाउनुहोस्_प्रणाली')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/वर्ग_मान 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 बनाउनुहोस्_प्रणाली JDK 또는 openjdk-build의 부트 JDK मार्ग')
    해석기.add_argument('--bundle-runtime', help='कार्यान्वयन_गर्नुहोस्_आदेश 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK अनुप्रयोग_कर्मचारी_अगुवा/स्रोत_वृक्ष 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 बनाउनुहोस्_प्रणाली 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 बनाउनुहोस्_प्रणाली लक्ष्य (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 बनाउनुहोस्_प्रणाली 대상의 libc/헤더/पुस्तकालय 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ढाँचा_मान')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=वर्ग_मान.प्रकार्य_मान (निज 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.चलाउनुहोस् (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='कार्यान्वयन_गर्नुहोस्_आदेश ELF/.o 출력; openjdk-build는 전용 बनाउनुहोस्_प्रणाली 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(तर्क)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK स्रोत_वृक्ष 디렉터리 하나와 --java-home 부트 JDK, -o बनाउनुहोस्_प्रणाली 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as त्रुटि:
            raise 컴파일오류(str(त्रुटि))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build लक्ष्य 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import सिर्जना_प्रविष्टि
        सिर्जना_प्रविष्टि(인자)
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
        कार्यान्वयन_गर्नुहोस्_आदेश()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as त्रुटि:
        print('बनाउनुहोस्_स्रोत त्रुटि: ' + str(त्रुटि), file=sys.stderr)
        sys.exit(1)
