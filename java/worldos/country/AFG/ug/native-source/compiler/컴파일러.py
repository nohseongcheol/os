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
    def __init__(자신, مەلۇمات):
        자신.مەلۇمات = مەلۇمات
        자신.ئورۇن = 0

    def ئوقۇ(자신, ئۇزۇنلۇق_قىممىتى):
        if ئۇزۇنلۇق_قىممىتى < 0 or 자신.ئورۇن + ئۇزۇنلۇق_قىممىتى > len(자신.مەلۇمات):
            raise 컴파일오류('잘린 تۈركۈم_قىممىتى 또는 بۇيرۇق مەلۇمات')
        ئۆلچەم = 자신.مەلۇمات[자신.ئورۇن:자신.ئورۇن + ئۇزۇنلۇق_قىممىتى]
        자신.ئورۇن += ئۇزۇنلۇق_قىممىتى
        return ئۆلچەم

    def 수(자신, فورمات_قىممىتى):
        return struct.unpack('>' + فورمات_قىممىتى, 자신.ئوقۇ(struct.calcsize('>' + فورمات_قىممىتى)))[0]


def 수정유티에프해독(مەلۇمات):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ھەرپ_تىزمىسى_قىممىتى = مەلۇمات.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ھەرپ_تىزمىسى_قىممىتى.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class تۈركۈم_قىممىتى:
    def __init__(자신, يول):
        자신.يول = يول
        ئوقۇغۇچ_قىممىتى = 자료읽기(يول.read_bytes())
        if ئوقۇغۇچ_قىممىتى.수('I') != 0xcafebabe:
            raise 컴파일오류('Java تۈركۈم_قىممىتى 표식이 아님')
        ئوقۇغۇچ_قىممىتى.ئوقۇ(4)
        개수 = ئوقۇغۇچ_قىممىتى.수('H')
        자신.تۇراقلىق_مىقدار_قىممىتى = [None] * 개수
        ئىندېكس = 1
        while ئىندېكس < 개수:
            종류 = ئوقۇغۇچ_قىممىتى.수('B')
            if 종류 == 1:
                قىممىتى = 수정유티에프해독(ئوقۇغۇچ_قىممىتى.ئوقۇ(ئوقۇغۇچ_قىممىتى.수('H')))
            elif 종류 == 3:
                قىممىتى = ئوقۇغۇچ_قىممىتى.수('i')
            elif 종류 == 4:
                قىممىتى = ئوقۇغۇچ_قىممىتى.ئوقۇ(4)
            elif 종류 in (5, 6):
                قىممىتى = ئوقۇغۇچ_قىممىتى.ئوقۇ(8)
            elif 종류 in (7, 8, 16):
                قىممىتى = ئوقۇغۇچ_قىممىتى.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                قىممىتى = (ئوقۇغۇچ_قىممىتى.수('H'), ئوقۇغۇچ_قىممىتى.수('H'))
            elif 종류 == 15:
                قىممىتى = (ئوقۇغۇچ_قىممىتى.수('B'), ئوقۇغۇچ_قىممىتى.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 تۇراقلىق_مىقدار_قىممىتى 종류: {}'.format(종류))
            자신.تۇراقلىق_مىقدار_قىممىتى[ئىندېكس] = (종류, قىممىتى)
            ئىندېكس += 2 if 종류 in (5, 6) else 1
        자신.زىيارەت_كىرگۈزۈش = ئوقۇغۇچ_قىممىتى.수('H')
        자신.ئاتى = 자신.تۈركۈم_نامى(ئوقۇغۇچ_قىممىتى.수('H'))
        부모 = ئوقۇغۇچ_قىممىتى.수('H')
        if 자신.تۈركۈم_نامى(부모) != 'java/lang/Object' or ئوقۇغۇچ_قىممىتى.수('H') != 0:
            raise 컴파일오류(자신.ئاتى + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.بۆلەك_قىممىتى_0f39cf1c = 자신.멤버읽기(ئوقۇغۇچ_قىممىتى)
        자신.فۇنكسىيە_قىممىتى = 자신.멤버읽기(ئوقۇغۇچ_قىممىتى)
        자신.속성읽기(ئوقۇغۇچ_قىممىتى)

    def 문자(자신, ئىندېكس):
        if 자신.تۇراقلىق_مىقدار_قىممىتى[ئىندېكس][0] != 1:
            raise 컴파일오류('ھەرپ_تىزمىسى_قىممىتى تۇراقلىق_مىقدار_قىممىتى فورمات_قىممىتى خاتالىق')
        return 자신.تۇراقلىق_مىقدار_قىممىتى[ئىندېكس][1]

    def تۈركۈم_نامى(자신, ئىندېكس):
        return 자신.문자(자신.تۇراقلىق_مىقدار_قىممىتى[ئىندېكس][1])

    def پايدىلانما(자신, ئىندېكس):
        ئىگە_قىممىتى, نامى_فورمات = 자신.تۇراقلىق_مىقدار_قىممىتى[ئىندېكس][1]
        ئاتى, فورمات_قىممىتى = 자신.تۇراقلىق_مىقدار_قىممىتى[نامى_فورمات][1]
        return 자신.تۈركۈم_نامى(ئىگە_قىممىتى), 자신.문자(ئاتى), 자신.문자(فورمات_قىممىتى)

    def 속성읽기(자신, ئوقۇغۇچ_قىممىتى):
        ئۆلچەم = {}
        for _ in range(ئوقۇغۇچ_قىممىتى.수('H')):
            ئاتى = 자신.문자(ئوقۇغۇچ_قىممىتى.수('H'))
            ئۆلچەم[ئاتى] = ئوقۇغۇچ_قىممىتى.ئوقۇ(ئوقۇغۇچ_قىممىتى.수('I'))
        return ئۆلچەم

    def 멤버읽기(자신, ئوقۇغۇچ_قىممىتى):
        ئۆلچەم = []
        for _ in range(ئوقۇغۇچ_قىممىتى.수('H')):
            زىيارەت_كىرگۈزۈش = ئوقۇغۇچ_قىممىتى.수('H')
            ئاتى = 자신.문자(ئوقۇغۇچ_قىممىتى.수('H'))
            فورمات_قىممىتى = 자신.문자(ئوقۇغۇچ_قىممىتى.수('H'))
            ئۆلچەم.append((زىيارەت_كىرگۈزۈش, ئاتى, فورمات_قىممىتى, 자신.속성읽기(ئوقۇغۇچ_قىممىتى)))
        return ئۆلچەم


def 형식읽기(ھەرپ_تىزمىسى_قىممىتى):
    ئۆلچەم = []
    ئورۇن = 0
    while ئورۇن < len(ھەرپ_تىزمىسى_قىممىتى):
        for فورمات_قىممىتى in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ھەرپ_تىزمىسى_قىممىتى.startswith(فورمات_قىممىتى, ئورۇن):
                ئۆلچەم.append(فورمات_قىممىتى)
                ئورۇن += len(فورمات_قىممىتى)
                break
        else:
            raise 컴파일오류('지원하지 않는 مەلۇمات_تىپى: ' + ھەرپ_تىزمىسى_قىممىتى)
    return ئۆلچەم


def 함수형식(서술):
    ئۆزگەرگۈچىلەر, قايتۇرۇپ_بېرىش_ئۆلچەم = 서술[1:].split(')')
    ئۆزگەرگۈچىلەر = 형식읽기(ئۆزگەرگۈچىلەر)
    قايتۇرۇپ_بېرىش_تىپ = 형식읽기(قايتۇرۇپ_بېرىش_ئۆلچەم)
    if 'V' in ئۆزگەرگۈچىلەر or len(قايتۇرۇپ_بېرىش_تىپ) != 1:
        raise 컴파일오류('فۇنكسىيە_قىممىتى 서술 فورمات_قىممىتى خاتالىق: ' + 서술)
    return ئۆزگەرگۈچىلەر, قايتۇرۇپ_بېرىش_ئۆلچەم


def بەلگە(종류, *부분):
    مەنبە = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(مەنبە).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 فۇنكسىيە_قىممىتى 서술에 대해서만 허용한다.
def ئىجرا_قىلىش_بۇيرۇق(ئۆزگەرگۈچىلەر=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK مەنبە_دەرەخ نۇسخا_سىستېما')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/تۈركۈم_قىممىتى 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 نۇسخا_سىستېما JDK 또는 openjdk-build의 부트 JDK يول')
    해석기.add_argument('--bundle-runtime', help='ئىجرا_قىلىش_بۇيرۇق 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK ئەپ_خادىم/مەنبە_دەرەخ 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 نۇسخا_سىستېما 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 نۇسخا_سىستېما نىشان (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 نۇسخا_سىستېما 대상의 libc/헤더/ئامبار 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 فورمات_قىممىتى')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=تۈركۈم_قىممىتى.فۇنكسىيە_قىممىتى (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ئىجرا_قىل_2 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ئىجرا_قىلىش_بۇيرۇق ELF/.o چىقار; openjdk-build는 전용 نۇسخا_سىستېما 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(ئۆزگەرگۈچىلەر)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK مەنبە_دەرەخ 디렉터리 하나와 --java-home 부트 JDK, -o نۇسخا_سىستېما 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as خاتالىق:
            raise 컴파일오류(str(خاتالىق))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build نىشان 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import قۇرۇش_كىرگۈزۈش
        قۇرۇش_كىرگۈزۈش(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk نىشان 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ئىجرا_قىلىش_بۇيرۇق()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as خاتالىق:
        print('قۇرماق_مەنبە خاتالىق: ' + str(خاتالىق), file=sys.stderr)
        sys.exit(1)
