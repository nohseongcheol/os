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
    def __init__(자신, 자료):
        자신.자료 = 자료
        자신.위치 = 0

    def 읽기(자신, 길이):
        if 길이 < 0 or 자신.위치 + 길이 > len(자신.자료):
            raise 컴파일오류('잘린 클래스 또는 명령 자료')
        결과 = 자신.자료[자신.위치:자신.위치 + 길이]
        자신.위치 += 길이
        return 결과

    def 수(자신, 형식):
        return struct.unpack('>' + 형식, 자신.읽기(struct.calcsize('>' + 형식)))[0]


def 수정유티에프해독(자료):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    문자열 = 자료.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return 문자열.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class 클래스:
    def __init__(자신, 경로):
        자신.경로 = 경로
        읽개 = 자료읽기(경로.read_bytes())
        if 읽개.수('I') != 0xcafebabe:
            raise 컴파일오류('Java 클래스 표식이 아님')
        읽개.읽기(4)
        개수 = 읽개.수('H')
        자신.상수 = [None] * 개수
        번호 = 1
        while 번호 < 개수:
            종류 = 읽개.수('B')
            if 종류 == 1:
                값 = 수정유티에프해독(읽개.읽기(읽개.수('H')))
            elif 종류 == 3:
                값 = 읽개.수('i')
            elif 종류 == 4:
                값 = 읽개.읽기(4)
            elif 종류 in (5, 6):
                값 = 읽개.읽기(8)
            elif 종류 in (7, 8, 16):
                값 = 읽개.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                값 = (읽개.수('H'), 읽개.수('H'))
            elif 종류 == 15:
                값 = (읽개.수('B'), 읽개.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 상수 종류: {}'.format(종류))
            자신.상수[번호] = (종류, 값)
            번호 += 2 if 종류 in (5, 6) else 1
        자신.접근 = 읽개.수('H')
        자신.Nòm = 자신.클래스명(읽개.수('H'))
        부모 = 읽개.수('H')
        if 자신.클래스명(부모) != 'java/lang/Object' or 읽개.수('H') != 0:
            raise 컴파일오류(자신.Nòm + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.필드 = 자신.멤버읽기(읽개)
        자신.함수 = 자신.멤버읽기(읽개)
        자신.속성읽기(읽개)

    def 문자(자신, 번호):
        if 자신.상수[번호][0] != 1:
            raise 컴파일오류('문자열 상수 형식 Eror')
        return 자신.상수[번호][1]

    def 클래스명(자신, 번호):
        return 자신.문자(자신.상수[번호][1])

    def 참조(자신, 번호):
        소유, 이름형식 = 자신.상수[번호][1]
        Nòm, 형식 = 자신.상수[이름형식][1]
        return 자신.클래스명(소유), 자신.문자(Nòm), 자신.문자(형식)

    def 속성읽기(자신, 읽개):
        결과 = {}
        for _ in range(읽개.수('H')):
            Nòm = 자신.문자(읽개.수('H'))
            결과[Nòm] = 읽개.읽기(읽개.수('I'))
        return 결과

    def 멤버읽기(자신, 읽개):
        결과 = []
        for _ in range(읽개.수('H')):
            접근 = 읽개.수('H')
            Nòm = 자신.문자(읽개.수('H'))
            형식 = 자신.문자(읽개.수('H'))
            결과.append((접근, Nòm, 형식, 자신.속성읽기(읽개)))
        return 결과


def 형식읽기(문자열):
    결과 = []
    위치 = 0
    while 위치 < len(문자열):
        for 형식 in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if 문자열.startswith(형식, 위치):
                결과.append(형식)
                위치 += len(형식)
                break
        else:
            raise 컴파일오류('지원하지 않는 자료형: ' + 문자열)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('함수 서술 형식 Eror: ' + 서술)
    return 인수, 반환


def 기호(종류, *부분):
    원문 = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(원문).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 함수 서술에 대해서만 허용한다.
def 실행(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK 소스 빌드')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/클래스 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 빌드 JDK 또는 openjdk-build의 부트 JDK 경로')
    해석기.add_argument('--bundle-runtime', help='실행 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK 실행기/소스 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 빌드 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 빌드 대상 (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 빌드 대상의 libc/헤더/라이브러리 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 형식')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=클래스.함수 (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.시작 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='실행 ELF/.o 출력; openjdk-build는 전용 빌드 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK 소스 디렉터리 하나와 --java-home 부트 JDK, -o 빌드 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Eror:
            raise 컴파일오류(str(Eror))
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
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Eror:
        print('컴파일 Eror: ' + str(Eror), file=sys.stderr)
        sys.exit(1)
