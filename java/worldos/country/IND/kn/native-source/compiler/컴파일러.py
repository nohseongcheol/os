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
    def __init__(자신, ಡೇಟಾ):
        자신.ಡೇಟಾ = ಡೇಟಾ
        자신.ಸ್ಥಾನ = 0

    def ಓದು(자신, ಉದ್ದ_ಮೌಲ್ಯ):
        if ಉದ್ದ_ಮೌಲ್ಯ < 0 or 자신.ಸ್ಥಾನ + ಉದ್ದ_ಮೌಲ್ಯ > len(자신.ಡೇಟಾ):
            raise 컴파일오류('잘린 ವರ್ಗ_ಮೌಲ್ಯ_55654bf1 또는 ಆಜ್ಞೆ ಡೇಟಾ')
        ಮಾಪನ = 자신.ಡೇಟಾ[자신.ಸ್ಥಾನ:자신.ಸ್ಥಾನ + ಉದ್ದ_ಮೌಲ್ಯ]
        자신.ಸ್ಥಾನ += ಉದ್ದ_ಮೌಲ್ಯ
        return ಮಾಪನ

    def 수(자신, ಸ್ವರೂಪ_ಮೌಲ್ಯ):
        return struct.unpack('>' + ಸ್ವರೂಪ_ಮೌಲ್ಯ, 자신.ಓದು(struct.calcsize('>' + ಸ್ವರೂಪ_ಮೌಲ್ಯ)))[0]


def 수정유티에프해독(ಡೇಟಾ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ = ಡೇಟಾ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ವರ್ಗ_ಮೌಲ್ಯ_55654bf1:
    def __init__(자신, ಮಾರ್ಗ):
        자신.ಮಾರ್ಗ = ಮಾರ್ಗ
        ಓದುಗ_ಮೌಲ್ಯ = 자료읽기(ಮಾರ್ಗ.read_bytes())
        if ಓದುಗ_ಮೌಲ್ಯ.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ವರ್ಗ_ಮೌಲ್ಯ_55654bf1 표식이 아님')
        ಓದುಗ_ಮೌಲ್ಯ.ಓದು(4)
        개수 = ಓದುಗ_ಮೌಲ್ಯ.수('H')
        자신.ಸ್ಧಿರ_ಮೌಲ್ಯ = [None] * 개수
        ಪದಸೂಚಿ = 1
        while ಪದಸೂಚಿ < 개수:
            종류 = ಓದುಗ_ಮೌಲ್ಯ.수('B')
            if 종류 == 1:
                ಮೌಲ್ಯ = 수정유티에프해독(ಓದುಗ_ಮೌಲ್ಯ.ಓದು(ಓದುಗ_ಮೌಲ್ಯ.수('H')))
            elif 종류 == 3:
                ಮೌಲ್ಯ = ಓದುಗ_ಮೌಲ್ಯ.수('i')
            elif 종류 == 4:
                ಮೌಲ್ಯ = ಓದುಗ_ಮೌಲ್ಯ.ಓದು(4)
            elif 종류 in (5, 6):
                ಮೌಲ್ಯ = ಓದುಗ_ಮೌಲ್ಯ.ಓದು(8)
            elif 종류 in (7, 8, 16):
                ಮೌಲ್ಯ = ಓದುಗ_ಮೌಲ್ಯ.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ಮೌಲ್ಯ = (ಓದುಗ_ಮೌಲ್ಯ.수('H'), ಓದುಗ_ಮೌಲ್ಯ.수('H'))
            elif 종류 == 15:
                ಮೌಲ್ಯ = (ಓದುಗ_ಮೌಲ್ಯ.수('B'), ಓದುಗ_ಮೌಲ್ಯ.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 ಸ್ಧಿರ_ಮೌಲ್ಯ 종류: {}'.format(종류))
            자신.ಸ್ಧಿರ_ಮೌಲ್ಯ[ಪದಸೂಚಿ] = (종류, ಮೌಲ್ಯ)
            ಪದಸೂಚಿ += 2 if 종류 in (5, 6) else 1
        자신.ಪ್ರವೇಶ_ನಮೂದು = ಓದುಗ_ಮೌಲ್ಯ.수('H')
        자신.ಹೆಸರು = 자신.ವರ್ಗ_ಹೆಸರು(ಓದುಗ_ಮೌಲ್ಯ.수('H'))
        부모 = ಓದುಗ_ಮೌಲ್ಯ.수('H')
        if 자신.ವರ್ಗ_ಹೆಸರು(부모) != 'java/lang/Object' or ಓದುಗ_ಮೌಲ್ಯ.수('H') != 0:
            raise 컴파일오류(자신.ಹೆಸರು + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ಕ್ಷೇತ್ರ_ಮೌಲ್ಯ = 자신.멤버읽기(ಓದುಗ_ಮೌಲ್ಯ)
        자신.ಕಾರ್ಯ_ಮೌಲ್ಯ = 자신.멤버읽기(ಓದುಗ_ಮೌಲ್ಯ)
        자신.속성읽기(ಓದುಗ_ಮೌಲ್ಯ)

    def 문자(자신, ಪದಸೂಚಿ):
        if 자신.ಸ್ಧಿರ_ಮೌಲ್ಯ[ಪದಸೂಚಿ][0] != 1:
            raise 컴파일오류('ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ ಸ್ಧಿರ_ಮೌಲ್ಯ ಸ್ವರೂಪ_ಮೌಲ್ಯ ದೋಷ')
        return 자신.ಸ್ಧಿರ_ಮೌಲ್ಯ[ಪದಸೂಚಿ][1]

    def ವರ್ಗ_ಹೆಸರು(자신, ಪದಸೂಚಿ):
        return 자신.문자(자신.ಸ್ಧಿರ_ಮೌಲ್ಯ[ಪದಸೂಚಿ][1])

    def ಉಲ್ಲೇಖ(자신, ಪದಸೂಚಿ):
        ಮಾಲೀಕ_ಮೌಲ್ಯ, ಹೆಸರು_ಸ್ವರೂಪ = 자신.ಸ್ಧಿರ_ಮೌಲ್ಯ[ಪದಸೂಚಿ][1]
        ಹೆಸರು, ಸ್ವರೂಪ_ಮೌಲ್ಯ = 자신.ಸ್ಧಿರ_ಮೌಲ್ಯ[ಹೆಸರು_ಸ್ವರೂಪ][1]
        return 자신.ವರ್ಗ_ಹೆಸರು(ಮಾಲೀಕ_ಮೌಲ್ಯ), 자신.문자(ಹೆಸರು), 자신.문자(ಸ್ವರೂಪ_ಮೌಲ್ಯ)

    def 속성읽기(자신, ಓದುಗ_ಮೌಲ್ಯ):
        ಮಾಪನ = {}
        for _ in range(ಓದುಗ_ಮೌಲ್ಯ.수('H')):
            ಹೆಸರು = 자신.문자(ಓದುಗ_ಮೌಲ್ಯ.수('H'))
            ಮಾಪನ[ಹೆಸರು] = ಓದುಗ_ಮೌಲ್ಯ.ಓದು(ಓದುಗ_ಮೌಲ್ಯ.수('I'))
        return ಮಾಪನ

    def 멤버읽기(자신, ಓದುಗ_ಮೌಲ್ಯ):
        ಮಾಪನ = []
        for _ in range(ಓದುಗ_ಮೌಲ್ಯ.수('H')):
            ಪ್ರವೇಶ_ನಮೂದು = ಓದುಗ_ಮೌಲ್ಯ.수('H')
            ಹೆಸರು = 자신.문자(ಓದುಗ_ಮೌಲ್ಯ.수('H'))
            ಸ್ವರೂಪ_ಮೌಲ್ಯ = 자신.문자(ಓದುಗ_ಮೌಲ್ಯ.수('H'))
            ಮಾಪನ.append((ಪ್ರವೇಶ_ನಮೂದು, ಹೆಸರು, ಸ್ವರೂಪ_ಮೌಲ್ಯ, 자신.속성읽기(ಓದುಗ_ಮೌಲ್ಯ)))
        return ಮಾಪನ


def 형식읽기(ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ):
    ಮಾಪನ = []
    ಸ್ಥಾನ = 0
    while ಸ್ಥಾನ < len(ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ):
        for ಸ್ವರೂಪ_ಮೌಲ್ಯ in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ.startswith(ಸ್ವರೂಪ_ಮೌಲ್ಯ, ಸ್ಥಾನ):
                ಮಾಪನ.append(ಸ್ವರೂಪ_ಮೌಲ್ಯ)
                ಸ್ಥಾನ += len(ಸ್ವರೂಪ_ಮೌಲ್ಯ)
                break
        else:
            raise 컴파일오류('지원하지 않는 ಡೇಟಾ_ಪ್ರಕಾರ: ' + ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ)
    return ಮಾಪನ


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('ಕಾರ್ಯ_ಮೌಲ್ಯ 서술 ಸ್ವರೂಪ_ಮೌಲ್ಯ ದೋಷ: ' + 서술)
    return 인수, 반환


def ಚಿಹ್ನೆ(종류, *부분):
    ಮೂಲ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ಮೂಲ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ಕಾರ್ಯ_ಮೌಲ್ಯ 서술에 대해서만 허용한다.
def ಪೂರೈಸು_ಆದೇಶ(인수=None):
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ಮೂಲ_ವೃಕ್ಷ ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ವರ್ಗ_ಮೌಲ್ಯ_55654bf1 디렉터리')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ JDK 또는 openjdk-build의 부트 JDK ಮಾರ್ಗ')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--bundle-runtime', help='ಪೂರೈಸು_ಆದೇಶ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK ಅಪ್ಲಿ_ಲಾಂಚರ್/ಮೂಲ_ವೃಕ್ಷ 빌드의 C 컴파일러')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ 작업 수')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ ಲಕ್ಷ್ಯ (예: aarch64-linux-gnu)')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--sysroot', help='교차 ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ 대상의 libc/헤더/ಲೈಬ್ರರಿ 루트')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ಸ್ವರೂಪ_ಮೌಲ್ಯ')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=ವರ್ಗ_ಮೌಲ್ಯ_55654bf1.ಕಾರ್ಯ_ಮೌಲ್ಯ (자체 스택 ABI)')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--entry', help='예: 계산.ಚಲಾಯಿಸು_2 (openjdk-build 이외 대상에서 필수)')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('-o', '--output', required=True, help='ಪೂರೈಸು_ಆದೇಶ ELF/.o ಔಟ್_ಪುಟ್; openjdk-build는 전용 ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ 디렉터리')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('sources', nargs='+')
    ಪ್ಯಾರಾಮೀಟರ್_ವಾದ = ಪಾರ್ಸರ್_48ee4b1b.parse_args(인수)
    if ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.target == 'openjdk-build':
        if len(ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.sources) != 1 or not ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.java_home or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.entry or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.export or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.classpath or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ಮೂಲ_ವೃಕ್ಷ 디렉터리 하나와 --java-home 부트 JDK, -o ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.sources[0], ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.output, ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.java_home, ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.jobs, ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.openjdk_target,
                  ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.sysroot, None if ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.cc == 'cc' else ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.cc, ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.cxx, ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.configure_arg)
        except BuildError as ದೋಷ:
            raise 컴파일오류(str(ದೋಷ))
        return
    if not ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.entry:
        ಪಾರ್ಸರ್_48ee4b1b.error('--entry is required for this target')
    if ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.cxx or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.openjdk_target or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.sysroot or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.configure_arg or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ಲಕ್ಷ್ಯ 전용')
    if ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ರಚಿಸು_ನಮೂದು
        ರಚಿಸು_ನಮೂದು(ಪ್ಯಾರಾಮೀಟರ್_ವಾದ)
        return
    if ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.classpath or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.java_home or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.bundle_runtime or ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ಲಕ್ಷ್ಯ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.target, '--entry', ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.entry, '-o', ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.output]
    for ನಿಯೋಜಿಸು_ಮೌಲ್ಯ in ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.export: 자바명령.extend(['--export', ನಿಯೋಜಿಸು_ಮೌಲ್ಯ])
    subprocess.run(자바명령+ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ಪೂರೈಸು_ಆದೇಶ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ದೋಷ:
        print('ಸಂಕಲಿಸು_ಮೂಲ ದೋಷ: ' + str(ದೋಷ), file=sys.stderr)
        sys.exit(1)
