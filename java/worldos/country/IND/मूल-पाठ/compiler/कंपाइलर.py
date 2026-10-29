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


class संकलन_त्रुटि(Exception):
    pass


class पढें_डेटा:
    def __init__(자신, आँकड़े):
        자신.आँकड़े = आँकड़े
        자신.स्थान = 0

    def पढ़ें(자신, 길이):
        if 길이 < 0 or 자신.स्थान + 길이 > len(자신.आँकड़े):
            raise संकलन_त्रुटि('잘린 कक्षा_मान 또는 आदेश आँकड़े')
        परिणाम = 자신.आँकड़े[자신.स्थान:자신.स्थान + 길이]
        자신.स्थान += 길이
        return परिणाम

    def 수(자신, फॉर्मैट_मान):
        return struct.unpack('>' + फॉर्मैट_मान, 자신.पढ़ें(struct.calcsize('>' + फॉर्मैट_मान)))[0]


def 수정유티에프해독(आँकड़े):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    स्ट्रिंग_मान = आँकड़े.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return स्ट्रिंग_मान.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class कक्षा_मान:
    def __init__(자신, पथ):
        자신.पथ = पथ
        पाठक_मान = पढें_डेटा(पथ.read_bytes())
        if पाठक_मान.수('I') != 0xcafebabe:
            raise संकलन_त्रुटि('Java कक्षा_मान 표식이 아님')
        पाठक_मान.पढ़ें(4)
        개수 = पाठक_मान.수('H')
        자신.अचर_मान = [None] * 개수
        इंडेक्स = 1
        while इंडेक्स < 개수:
            종류 = पाठक_मान.수('B')
            if 종류 == 1:
                मान = 수정유티에프해독(पाठक_मान.पढ़ें(पाठक_मान.수('H')))
            elif 종류 == 3:
                मान = पाठक_मान.수('i')
            elif 종류 == 4:
                मान = पाठक_मान.पढ़ें(4)
            elif 종류 in (5, 6):
                मान = पाठक_मान.पढ़ें(8)
            elif 종류 in (7, 8, 16):
                मान = पाठक_मान.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                मान = (पाठक_मान.수('H'), पाठक_मान.수('H'))
            elif 종류 == 15:
                मान = (पाठक_मान.수('B'), पाठक_मान.수('H'))
            else:
                raise संकलन_त्रुटि('지원하지 않는 अचर_मान 종류: {}'.format(종류))
            자신.अचर_मान[इंडेक्स] = (종류, मान)
            इंडेक्स += 2 if 종류 in (5, 6) else 1
        자신.पहुँच_एन्ट्री = पाठक_मान.수('H')
        자신.नाम = 자신.क्_लास_नाम(पाठक_मान.수('H'))
        पैरेंट_मान = पाठक_मान.수('H')
        if 자신.क्_लास_नाम(पैरेंट_मान) != 'java/lang/Object' or पाठक_मान.수('H') != 0:
            raise संकलन_त्रुटि(자신.नाम + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.फ़ील्ड_मान = 자신.멤버읽기(पाठक_मान)
        자신.फ़ंक्_शन_मान = 자신.멤버읽기(पाठक_मान)
        자신.पढें_विशेषताएँ(पाठक_मान)

    def 문자(자신, इंडेक्स):
        if 자신.अचर_मान[इंडेक्स][0] != 1:
            raise संकलन_त्रुटि('स्ट्रिंग_मान अचर_मान फॉर्मैट_मान त्रुटि')
        return 자신.अचर_मान[इंडेक्स][1]

    def क्_लास_नाम(자신, इंडेक्स):
        return 자신.문자(자신.अचर_मान[इंडेक्स][1])

    def संदर्भ(자신, इंडेक्स):
        स्वामी_मान, नाम_फॉर्मैट = 자신.अचर_मान[इंडेक्स][1]
        नाम, फॉर्मैट_मान = 자신.अचर_मान[नाम_फॉर्मैट][1]
        return 자신.क्_लास_नाम(स्वामी_मान), 자신.문자(नाम), 자신.문자(फॉर्मैट_मान)

    def पढें_विशेषताएँ(자신, पाठक_मान):
        परिणाम = {}
        for _ in range(पाठक_मान.수('H')):
            नाम = 자신.문자(पाठक_मान.수('H'))
            परिणाम[नाम] = पाठक_मान.पढ़ें(पाठक_मान.수('I'))
        return परिणाम

    def 멤버읽기(자신, पाठक_मान):
        परिणाम = []
        for _ in range(पाठक_मान.수('H')):
            पहुँच_एन्ट्री = पाठक_मान.수('H')
            नाम = 자신.문자(पाठक_मान.수('H'))
            फॉर्मैट_मान = 자신.문자(पाठक_मान.수('H'))
            परिणाम.append((पहुँच_एन्ट्री, नाम, फॉर्मैट_मान, 자신.पढें_विशेषताएँ(पाठक_मान)))
        return परिणाम


def 형식읽기(स्ट्रिंग_मान):
    परिणाम = []
    स्थान = 0
    while स्थान < len(स्ट्रिंग_मान):
        for फॉर्मैट_मान in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if स्ट्रिंग_मान.startswith(फॉर्मैट_मान, स्थान):
                परिणाम.append(फॉर्मैट_मान)
                स्थान += len(फॉर्मैट_मान)
                break
        else:
            raise संकलन_त्रुटि('지원하지 않는 डेटा_प्रकार: ' + स्ट्रिंग_मान)
    return परिणाम


def 함수형식(서술):
    तर्क, वापस_करें_परिणाम = 서술[1:].split(')')
    तर्क = 형식읽기(तर्क)
    वापस_करें_लिखें = 형식읽기(वापस_करें_परिणाम)
    if 'V' in तर्क or len(वापस_करें_लिखें) != 1:
        raise संकलन_त्रुटि('फ़ंक्_शन_मान 서술 फॉर्मैट_मान त्रुटि: ' + 서술)
    return तर्क, वापस_करें_परिणाम


def प्रतीक(종류, *부분):
    स्रोत = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(स्रोत).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 फ़ंक्_शन_मान 서술에 대해서만 허용한다.
def निष्पादित_करें_आदेश(तर्क=None):
    पार्सर_48ee4b1b = argparse.ArgumentParser(description='निज Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK स्रोत_ट्री बिल्ड_सिस्टम')
    पार्सर_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    पार्सर_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 जोड़ें_एन्ट्री JAR/कक्षा_मान 디렉터리')
    पार्सर_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 बिल्ड_सिस्टम JDK 또는 openjdk-build의 부트 JDK पथ')
    पार्सर_48ee4b1b.add_argument('--bundle-runtime', help='निष्पादित_करें_आदेश 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    पार्सर_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK ऐप_लॉन्चर/स्रोत_ट्री 빌드의 C कंपाइलर')
    पार्सर_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ कंपाइलर')
    पार्सर_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 बिल्ड_सिस्टम 작업 수')
    पार्सर_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 बिल्ड_सिस्टम लक्ष्य (예: aarch64-linux-gnu)')
    पार्सर_48ee4b1b.add_argument('--sysroot', help='교차 बिल्ड_सिस्टम 대상의 libc/헤더/लाइब्रेरी 루트')
    पार्सर_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 फॉर्मैट_मान')
    पार्सर_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=कक्षा_मान.फ़ंक्_शन_मान (निज ऑपरेंड_स्टैक ABI)')
    पार्सर_48ee4b1b.add_argument('--entry', help='예: 계산.चलाएँ (openjdk-build 이외 대상에서 필수)')
    पार्सर_48ee4b1b.add_argument('-o', '--output', required=True, help='निष्पादित_करें_आदेश ELF/.o निर्गम; openjdk-build는 전용 बिल्ड_सिस्टम 디렉터리')
    पार्सर_48ee4b1b.add_argument('sources', nargs='+')
    पैरामीटर_तर्क = पार्सर_48ee4b1b.parse_args(तर्क)
    if पैरामीटर_तर्क.target == 'openjdk-build':
        if len(पैरामीटर_तर्क.sources) != 1 or not पैरामीटर_तर्क.java_home or पैरामीटर_तर्क.entry or पैरामीटर_तर्क.export or पैरामीटर_तर्क.classpath or पैरामीटर_तर्क.bundle_runtime:
            raise संकलन_त्रुटि('openjdk-build: OpenJDK स्रोत_ट्री 디렉터리 하나와 --java-home 부트 JDK, -o बिल्ड_सिस्टम 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(पैरामीटर_तर्क.sources[0], पैरामीटर_तर्क.output, पैरामीटर_तर्क.java_home, पैरामीटर_तर्क.jobs, पैरामीटर_तर्क.openjdk_target,
                  पैरामीटर_तर्क.sysroot, None if पैरामीटर_तर्क.cc == 'cc' else पैरामीटर_तर्क.cc, पैरामीटर_तर्क.cxx, पैरामीटर_तर्क.configure_arg)
        except BuildError as त्रुटि:
            raise संकलन_त्रुटि(str(त्रुटि))
        return
    if not पैरामीटर_तर्क.entry:
        पार्सर_48ee4b1b.error('--entry is required for this target')
    if पैरामीटर_तर्क.cxx or पैरामीटर_तर्क.openjdk_target or पैरामीटर_तर्क.sysroot or पैरामीटर_तर्क.configure_arg or पैरामीटर_तर्क.jobs != 2:
        raise संकलन_त्रुटि('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build लक्ष्य 전용')
    if पैरामीटर_तर्क.target == 'openjdk':
        sys.modules.setdefault('कंपाइलर', sys.modules[__name__])
        from निष्पादन_योग्य_फ़ाइल import बनाएँ_एन्ट्री
        बनाएँ_एन्ट्री(पैरामीटर_तर्क)
        return
    if पैरामीटर_तर्क.classpath or पैरामीटर_तर्क.java_home or पैरामीटर_तर्क.bundle_runtime or पैरामीटर_तर्क.cc != 'cc':
        raise संकलन_त्रुटि('classpath/java-home/bundle-runtime/cc 옵션은 openjdk लक्ष्य 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', पैरामीटर_तर्क.target, '--entry', पैरामीटर_तर्क.entry, '-o', पैरामीटर_तर्क.output]
    for असाइन_करें_मान in पैरामीटर_तर्क.export: 자바명령.extend(['--export', असाइन_करें_मान])
    subprocess.run(자바명령+पैरामीटर_तर्क.sources, check=True)
    return


if __name__ == '__main__':
    try:
        निष्पादित_करें_आदेश()
    except (संकलन_त्रुटि, OSError, ValueError, subprocess.CalledProcessError) as त्रुटि:
        print('कंपाइल_स्रोत त्रुटि: ' + str(त्रुटि), file=sys.stderr)
        sys.exit(1)
