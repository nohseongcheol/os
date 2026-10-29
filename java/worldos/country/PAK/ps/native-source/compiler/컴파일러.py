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
    def __init__(자신, اومتوک):
        자신.اومتوک = اومتوک
        자신.ځای = 0

    def لوستل(자신, اوږدوالى_ارزښت):
        if اوږدوالى_ارزښت < 0 or 자신.ځای + اوږدوالى_ارزښت > len(자신.اومتوک):
            raise 컴파일오류('잘린 پاړکى_ارزښت 또는 بولۍ اومتوک')
        결과 = 자신.اومتوک[자신.ځای:자신.ځای + اوږدوالى_ارزښت]
        자신.ځای += اوږدوالى_ارزښت
        return 결과

    def 수(자신, بڼه_ارزښت):
        return struct.unpack('>' + بڼه_ارزښت, 자신.لوستل(struct.calcsize('>' + بڼه_ارزښت)))[0]


def 수정유티에프해독(اومتوک):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    مزى_ارزښت_6ca8363c = اومتوک.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return مزى_ارزښت_6ca8363c.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class پاړکى_ارزښت:
    def __init__(자신, يونلور):
        자신.يونلور = يونلور
        لوستونکی_ارزښت = 자료읽기(يونلور.read_bytes())
        if لوستونکی_ارزښت.수('I') != 0xcafebabe:
            raise 컴파일오류('Java پاړکى_ارزښت 표식이 아님')
        لوستونکی_ارزښت.لوستل(4)
        개수 = لوستونکی_ارزښت.수('H')
        자신.درېدلى_ارزښت = [None] * 개수
        لړیال = 1
        while لړیال < 개수:
            종류 = لوستونکی_ارزښت.수('B')
            if 종류 == 1:
                ارزښت = 수정유티에프해독(لوستونکی_ارزښت.لوستل(لوستونکی_ارزښت.수('H')))
            elif 종류 == 3:
                ارزښت = لوستونکی_ارزښت.수('i')
            elif 종류 == 4:
                ارزښت = لوستونکی_ارزښت.لوستل(4)
            elif 종류 in (5, 6):
                ارزښت = لوستونکی_ارزښت.لوستل(8)
            elif 종류 in (7, 8, 16):
                ارزښت = لوستونکی_ارزښت.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ارزښت = (لوستونکی_ارزښت.수('H'), لوستونکی_ارزښت.수('H'))
            elif 종류 == 15:
                ارزښت = (لوستونکی_ارزښت.수('B'), لوستونکی_ارزښت.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 درېدلى_ارزښت 종류: {}'.format(종류))
            자신.درېدلى_ارزښت[لړیال] = (종류, ارزښت)
            لړیال += 2 if 종류 in (5, 6) else 1
        자신.رسى_ننوت = لوستونکی_ارزښت.수('H')
        자신.نوم = 자신.클래스명(لوستونکی_ارزښت.수('H'))
        부모 = لوستونکی_ارزښت.수('H')
        if 자신.클래스명(부모) != 'java/lang/Object' or لوستونکی_ارزښت.수('H') != 0:
            raise 컴파일오류(자신.نوم + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ډګر_ارزښت = 자신.멤버읽기(لوستونکی_ارزښت)
        자신.함수 = 자신.멤버읽기(لوستونکی_ارزښت)
        자신.속성읽기(لوستونکی_ارزښت)

    def 문자(자신, لړیال):
        if 자신.درېدلى_ارزښت[لړیال][0] != 1:
            raise 컴파일오류('مزى_ارزښت_6ca8363c درېدلى_ارزښت بڼه_ارزښت تېروتنه')
        return 자신.درېدلى_ارزښت[لړیال][1]

    def 클래스명(자신, لړیال):
        return 자신.문자(자신.درېدلى_ارزښت[لړیال][1])

    def 참조(자신, لړیال):
        소유, 이름형식 = 자신.درېدلى_ارزښت[لړیال][1]
        نوم, بڼه_ارزښت = 자신.درېدلى_ارزښت[이름형식][1]
        return 자신.클래스명(소유), 자신.문자(نوم), 자신.문자(بڼه_ارزښت)

    def 속성읽기(자신, لوستونکی_ارزښت):
        결과 = {}
        for _ in range(لوستونکی_ارزښت.수('H')):
            نوم = 자신.문자(لوستونکی_ارزښت.수('H'))
            결과[نوم] = لوستونکی_ارزښت.لوستل(لوستونکی_ارزښت.수('I'))
        return 결과

    def 멤버읽기(자신, لوستونکی_ارزښت):
        결과 = []
        for _ in range(لوستونکی_ارزښت.수('H')):
            رسى_ننوت = لوستونکی_ارزښت.수('H')
            نوم = 자신.문자(لوستونکی_ارزښت.수('H'))
            بڼه_ارزښت = 자신.문자(لوستونکی_ارزښت.수('H'))
            결과.append((رسى_ننوت, نوم, بڼه_ارزښت, 자신.속성읽기(لوستونکی_ارزښت)))
        return 결과


def 형식읽기(مزى_ارزښت_6ca8363c):
    결과 = []
    ځای = 0
    while ځای < len(مزى_ارزښت_6ca8363c):
        for بڼه_ارزښت in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if مزى_ارزښت_6ca8363c.startswith(بڼه_ارزښت, ځای):
                결과.append(بڼه_ارزښت)
                ځای += len(بڼه_ارزښت)
                break
        else:
            raise 컴파일오류('지원하지 않는 اومتوک_ډول: ' + مزى_ارزښت_6ca8363c)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('함수 서술 بڼه_ارزښت تېروتنه: ' + 서술)
    return 인수, 반환


def 기호(종류, *부분):
    سرچينه = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(سرچينه).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 함수 서술에 대해서만 허용한다.
def 실행(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK سرچینه_ونه جوړول_غونډال')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/پاړکى_ارزښت 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 جوړول_غونډال JDK 또는 openjdk-build의 부트 JDK يونلور')
    해석기.add_argument('--bundle-runtime', help='실행 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK 실행기/سرچینه_ونه 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 جوړول_غونډال 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 جوړول_غونډال 대상 (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 جوړول_غونډال 대상의 libc/헤더/کتابتون 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 بڼه_ارزښت')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=پاړکى_ارزښت.함수 (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ځغلول (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='실행 ELF/.o 출력; openjdk-build는 전용 جوړول_غونډال 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK سرچینه_ونه 디렉터리 하나와 --java-home 부트 JDK, -o جوړول_غونډال 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as تېروتنه:
            raise 컴파일오류(str(تېروتنه))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build 대상 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import 만들기
        만들기(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk 대상 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        실행()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as تېروتنه:
        print('جوړول_سرچینه تېروتنه: ' + str(تېروتنه), file=sys.stderr)
        sys.exit(1)
