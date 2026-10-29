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
    def __init__(자신, دەیتا):
        자신.دەیتا = دەیتا
        자신.위치 = 0

    def 읽기(자신, درێژی_نرخ):
        if درێژی_نرخ < 0 or 자신.위치 + درێژی_نرخ > len(자신.دەیتا):
            raise 컴파일오류('잘린 کلاس_نرخ 또는 فەرمان دەیتا')
        결과 = 자신.دەیتا[자신.위치:자신.위치 + درێژی_نرخ]
        자신.위치 += درێژی_نرخ
        return 결과

    def 수(자신, بیچم_نرخ):
        return struct.unpack('>' + بیچم_نرخ, 자신.읽기(struct.calcsize('>' + بیچم_نرخ)))[0]


def 수정유티에프해독(دەیتا):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    رست_نرخ = دەیتا.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return رست_نرخ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class کلاس_نرخ:
    def __init__(자신, گوزەر):
        자신.گوزەر = گوزەر
        خوێنەر_نرخ = 자료읽기(گوزەر.read_bytes())
        if خوێنەر_نرخ.수('I') != 0xcafebabe:
            raise 컴파일오류('Java کلاس_نرخ 표식이 아님')
        خوێنەر_نرخ.읽기(4)
        개수 = خوێنەر_نرخ.수('H')
        자신.نەگۆڕ_نرخ = [None] * 개수
        پێرست = 1
        while پێرست < 개수:
            종류 = خوێنەر_نرخ.수('B')
            if 종류 == 1:
                نرخ = 수정유티에프해독(خوێنەر_نرخ.읽기(خوێنەر_نرخ.수('H')))
            elif 종류 == 3:
                نرخ = خوێنەر_نرخ.수('i')
            elif 종류 == 4:
                نرخ = خوێنەر_نرخ.읽기(4)
            elif 종류 in (5, 6):
                نرخ = خوێنەر_نرخ.읽기(8)
            elif 종류 in (7, 8, 16):
                نرخ = خوێنەر_نرخ.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                نرخ = (خوێنەر_نرخ.수('H'), خوێنەر_نرخ.수('H'))
            elif 종류 == 15:
                نرخ = (خوێنەر_نرخ.수('B'), خوێنەر_نرخ.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 نەگۆڕ_نرخ 종류: {}'.format(종류))
            자신.نەگۆڕ_نرخ[پێرست] = (종류, نرخ)
            پێرست += 2 if 종류 in (5, 6) else 1
        자신.دەسگەیشتن_تێنووسین = خوێنەر_نرخ.수('H')
        자신.ناو = 자신.کلاس_ناو(خوێنەر_نرخ.수('H'))
        부모 = خوێنەر_نرخ.수('H')
        if 자신.کلاس_ناو(부모) != 'java/lang/Object' or خوێنەر_نرخ.수('H') != 0:
            raise 컴파일오류(자신.ناو + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.خانە_نرخ = 자신.멤버읽기(خوێنەر_نرخ)
        자신.کردار_نرخ = 자신.멤버읽기(خوێنەر_نرخ)
        자신.속성읽기(خوێنەر_نرخ)

    def 문자(자신, پێرست):
        if 자신.نەگۆڕ_نرخ[پێرست][0] != 1:
            raise 컴파일오류('رست_نرخ نەگۆڕ_نرخ بیچم_نرخ هەڵە')
        return 자신.نەگۆڕ_نرخ[پێرست][1]

    def کلاس_ناو(자신, پێرست):
        return 자신.문자(자신.نەگۆڕ_نرخ[پێرست][1])

    def سەرچاوە(자신, پێرست):
        خاوەن_نرخ, ناو_بیچم = 자신.نەگۆڕ_نرخ[پێرست][1]
        ناو, بیچم_نرخ = 자신.نەگۆڕ_نرخ[ناو_بیچم][1]
        return 자신.کلاس_ناو(خاوەن_نرخ), 자신.문자(ناو), 자신.문자(بیچم_نرخ)

    def 속성읽기(자신, خوێنەر_نرخ):
        결과 = {}
        for _ in range(خوێنەر_نرخ.수('H')):
            ناو = 자신.문자(خوێنەر_نرخ.수('H'))
            결과[ناو] = خوێنەر_نرخ.읽기(خوێنەر_نرخ.수('I'))
        return 결과

    def 멤버읽기(자신, خوێنەر_نرخ):
        결과 = []
        for _ in range(خوێنەر_نرخ.수('H')):
            دەسگەیشتن_تێنووسین = خوێنەر_نرخ.수('H')
            ناو = 자신.문자(خوێنەر_نرخ.수('H'))
            بیچم_نرخ = 자신.문자(خوێنەر_نرخ.수('H'))
            결과.append((دەسگەیشتن_تێنووسین, ناو, بیچم_نرخ, 자신.속성읽기(خوێنەر_نرخ)))
        return 결과


def 형식읽기(رست_نرخ):
    결과 = []
    위치 = 0
    while 위치 < len(رست_نرخ):
        for بیچم_نرخ in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if رست_نرخ.startswith(بیچم_نرخ, 위치):
                결과.append(بیچم_نرخ)
                위치 += len(بیچم_نرخ)
                break
        else:
            raise 컴파일오류('지원하지 않는 جۆری_دەیتا: ' + رست_نرخ)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('کردار_نرخ 서술 بیچم_نرخ هەڵە: ' + 서술)
    return 인수, 반환


def سیمبۆل(종류, *부분):
    ژێدەر = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ژێدەر).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 کردار_نرخ 서술에 대해서만 허용한다.
def جێبەجێکردن_فەرمان(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ژێدەر_دار دروستکراو_سیستم')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/کلاس_نرخ 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 دروستکراو_سیستم JDK 또는 openjdk-build의 부트 JDK گوزەر')
    해석기.add_argument('--bundle-runtime', help='جێبەجێکردن_فەرمان 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK بەرنامە_ئەندامی_ستاف/ژێدەر_دار 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 دروستکراو_سیستم 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 دروستکراو_سیستم مەبەست (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 دروستکراو_سیستم 대상의 libc/헤더/کتێبخانە 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 بیچم_نرخ')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=کلاس_نرخ.کردار_نرخ (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ڕادان (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='جێبەجێکردن_فەرمان ELF/.o 출력; openjdk-build는 전용 دروستکراو_سیستم 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ژێدەر_دار 디렉터리 하나와 --java-home 부트 JDK, -o دروستکراو_سیستم 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as هەڵە:
            raise 컴파일오류(str(هەڵە))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build مەبەست 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import دروستکردن_تێنووسین
        دروستکردن_تێنووسین(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk مەبەست 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        جێبەجێکردن_فەرمان()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as هەڵە:
        print('دروست_کردن_ژێدەر هەڵە: ' + str(هەڵە), file=sys.stderr)
        sys.exit(1)
