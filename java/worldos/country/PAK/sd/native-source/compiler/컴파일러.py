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
    def __init__(자신, ڪوائف):
        자신.ڪوائف = ڪوائف
        자신.위치 = 0

    def 읽기(자신, لمبائي_قدر):
        if لمبائي_قدر < 0 or 자신.위치 + لمبائي_قدر > len(자신.ڪوائف):
            raise 컴파일오류('잘린 درجو_قدر 또는 حڪم ڪوائف')
        결과 = 자신.ڪوائف[자신.위치:자신.위치 + لمبائي_قدر]
        자신.위치 += لمبائي_قدر
        return 결과

    def 수(자신, وضع_قدر):
        return struct.unpack('>' + وضع_قدر, 자신.읽기(struct.calcsize('>' + وضع_قدر)))[0]


def 수정유티에프해독(ڪوائف):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    اسٽرنگ_قدر = ڪوائف.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return اسٽرنگ_قدر.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class درجو_قدر:
    def __init__(자신, راههه):
        자신.راههه = راههه
        ريڊر_قدر = 자료읽기(راههه.read_bytes())
        if ريڊر_قدر.수('I') != 0xcafebabe:
            raise 컴파일오류('Java درجو_قدر 표식이 아님')
        ريڊر_قدر.읽기(4)
        개수 = ريڊر_قدر.수('H')
        자신.لاڳاتار_جزو_قدر = [None] * 개수
        ابتدائي = 1
        while ابتدائي < 개수:
            종류 = ريڊر_قدر.수('B')
            if 종류 == 1:
                قدر = 수정유티에프해독(ريڊر_قدر.읽기(ريڊر_قدر.수('H')))
            elif 종류 == 3:
                قدر = ريڊر_قدر.수('i')
            elif 종류 == 4:
                قدر = ريڊر_قدر.읽기(4)
            elif 종류 in (5, 6):
                قدر = ريڊر_قدر.읽기(8)
            elif 종류 in (7, 8, 16):
                قدر = ريڊر_قدر.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                قدر = (ريڊر_قدر.수('H'), ريڊر_قدر.수('H'))
            elif 종류 == 15:
                قدر = (ريڊر_قدر.수('B'), ريڊر_قدر.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 لاڳاتار_جزو_قدر 종류: {}'.format(종류))
            자신.لاڳاتار_جزو_قدر[ابتدائي] = (종류, قدر)
            ابتدائي += 2 if 종류 in (5, 6) else 1
        자신.پهچ_داخلا = ريڊر_قدر.수('H')
        자신.نالو = 자신.درجو_نالو(ريڊر_قدر.수('H'))
        부모 = ريڊر_قدر.수('H')
        if 자신.درجو_نالو(부모) != 'java/lang/Object' or ريڊر_قدر.수('H') != 0:
            raise 컴파일오류(자신.نالو + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.قطعه_قدر = 자신.멤버읽기(ريڊر_قدر)
        자신.فعل_قدر = 자신.멤버읽기(ريڊر_قدر)
        자신.속성읽기(ريڊر_قدر)

    def 문자(자신, ابتدائي):
        if 자신.لاڳاتار_جزو_قدر[ابتدائي][0] != 1:
            raise 컴파일오류('اسٽرنگ_قدر لاڳاتار_جزو_قدر وضع_قدر نقص')
        return 자신.لاڳاتار_جزو_قدر[ابتدائي][1]

    def درجو_نالو(자신, ابتدائي):
        return 자신.문자(자신.لاڳاتار_جزو_قدر[ابتدائي][1])

    def حوالو(자신, ابتدائي):
        مالڪ_قدر, نالو_وضع = 자신.لاڳاتار_جزو_قدر[ابتدائي][1]
        نالو, وضع_قدر = 자신.لاڳاتار_جزو_قدر[نالو_وضع][1]
        return 자신.درجو_نالو(مالڪ_قدر), 자신.문자(نالو), 자신.문자(وضع_قدر)

    def 속성읽기(자신, ريڊر_قدر):
        결과 = {}
        for _ in range(ريڊر_قدر.수('H')):
            نالو = 자신.문자(ريڊر_قدر.수('H'))
            결과[نالو] = ريڊر_قدر.읽기(ريڊر_قدر.수('I'))
        return 결과

    def 멤버읽기(자신, ريڊر_قدر):
        결과 = []
        for _ in range(ريڊر_قدر.수('H')):
            پهچ_داخلا = ريڊر_قدر.수('H')
            نالو = 자신.문자(ريڊر_قدر.수('H'))
            وضع_قدر = 자신.문자(ريڊر_قدر.수('H'))
            결과.append((پهچ_داخلا, نالو, وضع_قدر, 자신.속성읽기(ريڊر_قدر)))
        return 결과


def 형식읽기(اسٽرنگ_قدر):
    결과 = []
    위치 = 0
    while 위치 < len(اسٽرنگ_قدر):
        for وضع_قدر in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if اسٽرنگ_قدر.startswith(وضع_قدر, 위치):
                결과.append(وضع_قدر)
                위치 += len(وضع_قدر)
                break
        else:
            raise 컴파일오류('지원하지 않는 ڊيٽا_قسم: ' + اسٽرنگ_قدر)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('فعل_قدر 서술 وضع_قدر نقص: ' + 서술)
    return 인수, 반환


def نشاني(종류, *부분):
    ماخذ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ماخذ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 فعل_قدر 서술에 대해서만 허용한다.
def تعميل_ڪرڻ_حڪم(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ماخذ_شجرو گڏ_ڪريو_سسٽم')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/درجو_قدر 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 گڏ_ڪريو_سسٽم JDK 또는 openjdk-build의 부트 JDK راههه')
    해석기.add_argument('--bundle-runtime', help='تعميل_ڪرڻ_حڪم 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK ائپ_ائپ_ڊرائر/ماخذ_شجرو 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 گڏ_ڪريو_سسٽم 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 گڏ_ڪريو_سسٽم هدف (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 گڏ_ڪريو_سسٽم 대상의 libc/헤더/لائبريري 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 وضع_قدر')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=درجو_قدر.فعل_قدر (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.هلائڻ (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='تعميل_ڪرڻ_حڪم ELF/.o 출력; openjdk-build는 전용 گڏ_ڪريو_سسٽم 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ماخذ_شجرو 디렉터리 하나와 --java-home 부트 JDK, -o گڏ_ڪريو_سسٽم 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as نقص:
            raise 컴파일오류(str(نقص))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build هدف 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ٺاھيو_داخلا
        ٺاھيو_داخلا(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk هدف 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        تعميل_ڪرڻ_حڪم()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as نقص:
        print('گڏ_ڪريو_ماخذ نقص: ' + str(نقص), file=sys.stderr)
        sys.exit(1)
