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
    def __init__(자신, ሓበሬታ):
        자신.ሓበሬታ = ሓበሬታ
        자신.위치 = 0

    def 읽기(자신, ንውሓት_ዋጋ):
        if ንውሓት_ዋጋ < 0 or 자신.위치 + ንውሓት_ዋጋ > len(자신.ሓበሬታ):
            raise 컴파일오류('잘린 ክፍሊ_ዋጋ 또는 ትእዛዝ ሓበሬታ')
        결과 = 자신.ሓበሬታ[자신.위치:자신.위치 + ንውሓት_ዋጋ]
        자신.위치 += ንውሓት_ዋጋ
        return 결과

    def 수(자신, ቅረጽ_ዋጋ):
        return struct.unpack('>' + ቅረጽ_ዋጋ, 자신.읽기(struct.calcsize('>' + ቅረጽ_ዋጋ)))[0]


def 수정유티에프해독(ሓበሬታ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ሕብረ_ቁምፊ_ዋጋ = ሓበሬታ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ሕብረ_ቁምፊ_ዋጋ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ክፍሊ_ዋጋ:
    def __init__(자신, መገዲ):
        자신.መገዲ = መገዲ
        ኣንባቢ_ዋጋ = 자료읽기(መገዲ.read_bytes())
        if ኣንባቢ_ዋጋ.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ክፍሊ_ዋጋ 표식이 아님')
        ኣንባቢ_ዋጋ.읽기(4)
        개수 = ኣንባቢ_ዋጋ.수('H')
        자신.መረራኽቦ_ዋጋ = [None] * 개수
        መሐበሪ = 1
        while መሐበሪ < 개수:
            종류 = ኣንባቢ_ዋጋ.수('B')
            if 종류 == 1:
                ዋጋ = 수정유티에프해독(ኣንባቢ_ዋጋ.읽기(ኣንባቢ_ዋጋ.수('H')))
            elif 종류 == 3:
                ዋጋ = ኣንባቢ_ዋጋ.수('i')
            elif 종류 == 4:
                ዋጋ = ኣንባቢ_ዋጋ.읽기(4)
            elif 종류 in (5, 6):
                ዋጋ = ኣንባቢ_ዋጋ.읽기(8)
            elif 종류 in (7, 8, 16):
                ዋጋ = ኣንባቢ_ዋጋ.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ዋጋ = (ኣንባቢ_ዋጋ.수('H'), ኣንባቢ_ዋጋ.수('H'))
            elif 종류 == 15:
                ዋጋ = (ኣንባቢ_ዋጋ.수('B'), ኣንባቢ_ዋጋ.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 መረራኽቦ_ዋጋ 종류: {}'.format(종류))
            자신.መረራኽቦ_ዋጋ[መሐበሪ] = (종류, ዋጋ)
            መሐበሪ += 2 if 종류 in (5, 6) else 1
        자신.ፍቓድ_ምእታው = ኣንባቢ_ዋጋ.수('H')
        자신.ሽም = 자신.ክፍሊ_ሽም(ኣንባቢ_ዋጋ.수('H'))
        부모 = ኣንባቢ_ዋጋ.수('H')
        if 자신.ክፍሊ_ሽም(부모) != 'java/lang/Object' or ኣንባቢ_ዋጋ.수('H') != 0:
            raise 컴파일오류(자신.ሽም + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ሜዳ_ዋጋ = 자신.멤버읽기(ኣንባቢ_ዋጋ)
        자신.ተግባር_ዋጋ = 자신.멤버읽기(ኣንባቢ_ዋጋ)
        자신.속성읽기(ኣንባቢ_ዋጋ)

    def 문자(자신, መሐበሪ):
        if 자신.መረራኽቦ_ዋጋ[መሐበሪ][0] != 1:
            raise 컴파일오류('ሕብረ_ቁምፊ_ዋጋ መረራኽቦ_ዋጋ ቅረጽ_ዋጋ ጌጋ')
        return 자신.መረራኽቦ_ዋጋ[መሐበሪ][1]

    def ክፍሊ_ሽም(자신, መሐበሪ):
        return 자신.문자(자신.መረራኽቦ_ዋጋ[መሐበሪ][1])

    def መወከሲ(자신, መሐበሪ):
        ወናኒ_ዋጋ, ሽም_ቅረጽ = 자신.መረራኽቦ_ዋጋ[መሐበሪ][1]
        ሽም, ቅረጽ_ዋጋ = 자신.መረራኽቦ_ዋጋ[ሽም_ቅረጽ][1]
        return 자신.ክፍሊ_ሽም(ወናኒ_ዋጋ), 자신.문자(ሽም), 자신.문자(ቅረጽ_ዋጋ)

    def 속성읽기(자신, ኣንባቢ_ዋጋ):
        결과 = {}
        for _ in range(ኣንባቢ_ዋጋ.수('H')):
            ሽም = 자신.문자(ኣንባቢ_ዋጋ.수('H'))
            결과[ሽም] = ኣንባቢ_ዋጋ.읽기(ኣንባቢ_ዋጋ.수('I'))
        return 결과

    def 멤버읽기(자신, ኣንባቢ_ዋጋ):
        결과 = []
        for _ in range(ኣንባቢ_ዋጋ.수('H')):
            ፍቓድ_ምእታው = ኣንባቢ_ዋጋ.수('H')
            ሽም = 자신.문자(ኣንባቢ_ዋጋ.수('H'))
            ቅረጽ_ዋጋ = 자신.문자(ኣንባቢ_ዋጋ.수('H'))
            결과.append((ፍቓድ_ምእታው, ሽም, ቅረጽ_ዋጋ, 자신.속성읽기(ኣንባቢ_ዋጋ)))
        return 결과


def 형식읽기(ሕብረ_ቁምፊ_ዋጋ):
    결과 = []
    위치 = 0
    while 위치 < len(ሕብረ_ቁምፊ_ዋጋ):
        for ቅረጽ_ዋጋ in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ሕብረ_ቁምፊ_ዋጋ.startswith(ቅረጽ_ዋጋ, 위치):
                결과.append(ቅረጽ_ዋጋ)
                위치 += len(ቅረጽ_ዋጋ)
                break
        else:
            raise 컴파일오류('지원하지 않는 ናይ_ሓበሬታ_ዓይነት: ' + ሕብረ_ቁምፊ_ዋጋ)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('ተግባር_ዋጋ 서술 ቅረጽ_ዋጋ ጌጋ: ' + 서술)
    return 인수, 반환


def ምልክት(종류, *부분):
    ምንጪ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ምንጪ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ተግባር_ዋጋ 서술에 대해서만 허용한다.
def ተግብር_ትእዛዝ(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ምንጪ_ገረብ ህነጽ_ስርዓት')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ክፍሊ_ዋጋ 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 ህነጽ_ስርዓት JDK 또는 openjdk-build의 부트 JDK መገዲ')
    해석기.add_argument('--bundle-runtime', help='ተግብር_ትእዛዝ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK መተግበሪ_ተመዛዚ_መተግበሪ/ምንጪ_ገረብ 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ህነጽ_ስርዓት 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ህነጽ_ስርዓት ዕላማ (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 ህነጽ_ስርዓት 대상의 libc/헤더/ቤት_ንባብ 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ቅረጽ_ዋጋ')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=ክፍሊ_ዋጋ.ተግባር_ዋጋ (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ኣኺድ (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ተግብር_ትእዛዝ ELF/.o 출력; openjdk-build는 전용 ህነጽ_ስርዓት 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ምንጪ_ገረብ 디렉터리 하나와 --java-home 부트 JDK, -o ህነጽ_ስርዓት 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as ጌጋ:
            raise 컴파일오류(str(ጌጋ))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ዕላማ 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ፍጠር_ምእታው
        ፍጠር_ምእታው(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ዕላማ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ተግብር_ትእዛዝ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ጌጋ:
        print('ህነጽ_ምንጪ ጌጋ: ' + str(ጌጋ), file=sys.stderr)
        sys.exit(1)
