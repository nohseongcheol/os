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
    def __init__(자신, ਸਮੱਗਰੀ):
        자신.ਸਮੱਗਰੀ = ਸਮੱਗਰੀ
        자신.ਸਥਿਤੀ = 0

    def ਪੜ੍ਹਨ(자신, ਲੰਬਾਈ_ਕੀਮਤ):
        if ਲੰਬਾਈ_ਕੀਮਤ < 0 or 자신.ਸਥਿਤੀ + ਲੰਬਾਈ_ਕੀਮਤ > len(자신.ਸਮੱਗਰੀ):
            raise 컴파일오류('잘린 ਸ੍ਰੇਣੀ_ਕੀਮਤ 또는 ਕਮਾਂਡ ਸਮੱਗਰੀ')
        ਮਾਪ = 자신.ਸਮੱਗਰੀ[자신.ਸਥਿਤੀ:자신.ਸਥਿਤੀ + ਲੰਬਾਈ_ਕੀਮਤ]
        자신.ਸਥਿਤੀ += ਲੰਬਾਈ_ਕੀਮਤ
        return ਮਾਪ

    def 수(자신, ਸਰੂਪ_ਕੀਮਤ):
        return struct.unpack('>' + ਸਰੂਪ_ਕੀਮਤ, 자신.ਪੜ੍ਹਨ(struct.calcsize('>' + ਸਰੂਪ_ਕੀਮਤ)))[0]


def 수정유티에프해독(ਸਮੱਗਰੀ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ = ਸਮੱਗਰੀ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ਸ੍ਰੇਣੀ_ਕੀਮਤ:
    def __init__(자신, ਮਾਰਗ):
        자신.ਮਾਰਗ = ਮਾਰਗ
        ਪਾਠਕ_ਕੀਮਤ = 자료읽기(ਮਾਰਗ.read_bytes())
        if ਪਾਠਕ_ਕੀਮਤ.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ਸ੍ਰੇਣੀ_ਕੀਮਤ 표식이 아님')
        ਪਾਠਕ_ਕੀਮਤ.ਪੜ੍ਹਨ(4)
        개수 = ਪਾਠਕ_ਕੀਮਤ.수('H')
        자신.ਸਥਿਰ_ਕੀਮਤ = [None] * 개수
        ਅਨੁਕ੍ਰਮਣਿਕਾ = 1
        while ਅਨੁਕ੍ਰਮਣਿਕਾ < 개수:
            종류 = ਪਾਠਕ_ਕੀਮਤ.수('B')
            if 종류 == 1:
                ਕੀਮਤ = 수정유티에프해독(ਪਾਠਕ_ਕੀਮਤ.ਪੜ੍ਹਨ(ਪਾਠਕ_ਕੀਮਤ.수('H')))
            elif 종류 == 3:
                ਕੀਮਤ = ਪਾਠਕ_ਕੀਮਤ.수('i')
            elif 종류 == 4:
                ਕੀਮਤ = ਪਾਠਕ_ਕੀਮਤ.ਪੜ੍ਹਨ(4)
            elif 종류 in (5, 6):
                ਕੀਮਤ = ਪਾਠਕ_ਕੀਮਤ.ਪੜ੍ਹਨ(8)
            elif 종류 in (7, 8, 16):
                ਕੀਮਤ = ਪਾਠਕ_ਕੀਮਤ.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ਕੀਮਤ = (ਪਾਠਕ_ਕੀਮਤ.수('H'), ਪਾਠਕ_ਕੀਮਤ.수('H'))
            elif 종류 == 15:
                ਕੀਮਤ = (ਪਾਠਕ_ਕੀਮਤ.수('B'), ਪਾਠਕ_ਕੀਮਤ.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 ਸਥਿਰ_ਕੀਮਤ 종류: {}'.format(종류))
            자신.ਸਥਿਰ_ਕੀਮਤ[ਅਨੁਕ੍ਰਮਣਿਕਾ] = (종류, ਕੀਮਤ)
            ਅਨੁਕ੍ਰਮਣਿਕਾ += 2 if 종류 in (5, 6) else 1
        자신.ਐਕਸੈਸ_ਦਾਖਲਾ = ਪਾਠਕ_ਕੀਮਤ.수('H')
        자신.ਨਾਂ = 자신.ਸ੍ਰੇਣੀ_ਨਾਮ(ਪਾਠਕ_ਕੀਮਤ.수('H'))
        부모 = ਪਾਠਕ_ਕੀਮਤ.수('H')
        if 자신.ਸ੍ਰੇਣੀ_ਨਾਮ(부모) != 'java/lang/Object' or ਪਾਠਕ_ਕੀਮਤ.수('H') != 0:
            raise 컴파일오류(자신.ਨਾਂ + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ਫਿਲਡ_ਕੀਮਤ = 자신.멤버읽기(ਪਾਠਕ_ਕੀਮਤ)
        자신.ਫੰਗਸ਼ਨ_ਕੀਮਤ = 자신.멤버읽기(ਪਾਠਕ_ਕੀਮਤ)
        자신.속성읽기(ਪਾਠਕ_ਕੀਮਤ)

    def 문자(자신, ਅਨੁਕ੍ਰਮਣਿਕਾ):
        if 자신.ਸਥਿਰ_ਕੀਮਤ[ਅਨੁਕ੍ਰਮਣਿਕਾ][0] != 1:
            raise 컴파일오류('ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ ਸਥਿਰ_ਕੀਮਤ ਸਰੂਪ_ਕੀਮਤ ਗਲਤੀ')
        return 자신.ਸਥਿਰ_ਕੀਮਤ[ਅਨੁਕ੍ਰਮਣਿਕਾ][1]

    def ਸ੍ਰੇਣੀ_ਨਾਮ(자신, ਅਨੁਕ੍ਰਮਣਿਕਾ):
        return 자신.문자(자신.ਸਥਿਰ_ਕੀਮਤ[ਅਨੁਕ੍ਰਮਣਿਕਾ][1])

    def ਸੰਦਰਭ(자신, ਅਨੁਕ੍ਰਮਣਿਕਾ):
        ਮਾਲਕ_ਕੀਮਤ, ਨਾਮ_ਸਰੂਪ = 자신.ਸਥਿਰ_ਕੀਮਤ[ਅਨੁਕ੍ਰਮਣਿਕਾ][1]
        ਨਾਂ, ਸਰੂਪ_ਕੀਮਤ = 자신.ਸਥਿਰ_ਕੀਮਤ[ਨਾਮ_ਸਰੂਪ][1]
        return 자신.ਸ੍ਰੇਣੀ_ਨਾਮ(ਮਾਲਕ_ਕੀਮਤ), 자신.문자(ਨਾਂ), 자신.문자(ਸਰੂਪ_ਕੀਮਤ)

    def 속성읽기(자신, ਪਾਠਕ_ਕੀਮਤ):
        ਮਾਪ = {}
        for _ in range(ਪਾਠਕ_ਕੀਮਤ.수('H')):
            ਨਾਂ = 자신.문자(ਪਾਠਕ_ਕੀਮਤ.수('H'))
            ਮਾਪ[ਨਾਂ] = ਪਾਠਕ_ਕੀਮਤ.ਪੜ੍ਹਨ(ਪਾਠਕ_ਕੀਮਤ.수('I'))
        return ਮਾਪ

    def 멤버읽기(자신, ਪਾਠਕ_ਕੀਮਤ):
        ਮਾਪ = []
        for _ in range(ਪਾਠਕ_ਕੀਮਤ.수('H')):
            ਐਕਸੈਸ_ਦਾਖਲਾ = ਪਾਠਕ_ਕੀਮਤ.수('H')
            ਨਾਂ = 자신.문자(ਪਾਠਕ_ਕੀਮਤ.수('H'))
            ਸਰੂਪ_ਕੀਮਤ = 자신.문자(ਪਾਠਕ_ਕੀਮਤ.수('H'))
            ਮਾਪ.append((ਐਕਸੈਸ_ਦਾਖਲਾ, ਨਾਂ, ਸਰੂਪ_ਕੀਮਤ, 자신.속성읽기(ਪਾਠਕ_ਕੀਮਤ)))
        return ਮਾਪ


def 형식읽기(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ):
    ਮਾਪ = []
    ਸਥਿਤੀ = 0
    while ਸਥਿਤੀ < len(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ):
        for ਸਰੂਪ_ਕੀਮਤ in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ.startswith(ਸਰੂਪ_ਕੀਮਤ, ਸਥਿਤੀ):
                ਮਾਪ.append(ਸਰੂਪ_ਕੀਮਤ)
                ਸਥਿਤੀ += len(ਸਰੂਪ_ਕੀਮਤ)
                break
        else:
            raise 컴파일오류('지원하지 않는 ਡੇਟਾ_ਕਿਸਮ: ' + ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ)
    return ਮਾਪ


def 함수형식(서술):
    ਆਰਗੂਮੈਂਟ, 반환 = 서술[1:].split(')')
    ਆਰਗੂਮੈਂਟ = 형식읽기(ਆਰਗੂਮੈਂਟ)
    반환형 = 형식읽기(반환)
    if 'V' in ਆਰਗੂਮੈਂਟ or len(반환형) != 1:
        raise 컴파일오류('ਫੰਗਸ਼ਨ_ਕੀਮਤ 서술 ਸਰੂਪ_ਕੀਮਤ ਗਲਤੀ: ' + 서술)
    return ਆਰਗੂਮੈਂਟ, 반환


def ਪ੍ਰਤੀਕ(종류, *부분):
    ਸਰੋਤ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ਸਰੋਤ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ਫੰਗਸ਼ਨ_ਕੀਮਤ 서술에 대해서만 허용한다.
def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਆਰਗੂਮੈਂਟ=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ਸਰੋਤ_ਟ੍ਰੀ ਬਿਲਡ_ਪਰਬੰਧ')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ਸ੍ਰੇਣੀ_ਕੀਮਤ 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 ਬਿਲਡ_ਪਰਬੰਧ JDK 또는 openjdk-build의 부트 JDK ਮਾਰਗ')
    해석기.add_argument('--bundle-runtime', help='ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ/ਸਰੋਤ_ਟ੍ਰੀ 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ਬਿਲਡ_ਪਰਬੰਧ 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ਬਿਲਡ_ਪਰਬੰਧ ਟੀਚਾ (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 ਬਿਲਡ_ਪਰਬੰਧ 대상의 libc/헤더/ਪੁਸਤਕਾਲਾ 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ਸਰੂਪ_ਕੀਮਤ')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=ਸ੍ਰੇਣੀ_ਕੀਮਤ.ਫੰਗਸ਼ਨ_ਕੀਮਤ (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ਚਲਾਓ_2 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ ELF/.o ਆਉਟਪੁੱਟ; openjdk-build는 전용 ਬਿਲਡ_ਪਰਬੰਧ 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(ਆਰਗੂਮੈਂਟ)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ਸਰੋਤ_ਟ੍ਰੀ 디렉터리 하나와 --java-home 부트 JDK, -o ਬਿਲਡ_ਪਰਬੰਧ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as ਗਲਤੀ:
            raise 컴파일오류(str(ਗਲਤੀ))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ਟੀਚਾ 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ਬਣਾਓ_ਦਾਖਲਾ
        ਬਣਾਓ_ਦਾਖਲਾ(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ਟੀਚਾ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for ਅਸਾਈਨ_ਕਰੋ_ਕੀਮਤ in 인자.export: 자바명령.extend(['--export', ਅਸਾਈਨ_ਕਰੋ_ਕੀਮਤ])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ਗਲਤੀ:
        print('ਬਣਾਊਣਾ_ਸਰੋਤ ਗਲਤੀ: ' + str(ਗਲਤੀ), file=sys.stderr)
        sys.exit(1)
