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
    def __init__(자신, ውሂብ):
        자신.ውሂብ = ውሂብ
        자신.አካባቢ = 0

    def ማንበቢያ(자신, ርዝመት_እሴት):
        if ርዝመት_እሴት < 0 or 자신.አካባቢ + ርዝመት_እሴት > len(자신.ውሂብ):
            raise 컴파일오류('잘린 መደብ_እሴት 또는 ትእዛዝ ውሂብ')
        ልኬት = 자신.ውሂብ[자신.አካባቢ:자신.አካባቢ + ርዝመት_እሴት]
        자신.አካባቢ += ርዝመት_እሴት
        return ልኬት

    def 수(자신, ቅርጸት_እሴት):
        return struct.unpack('>' + ቅርጸት_እሴት, 자신.ማንበቢያ(struct.calcsize('>' + ቅርጸት_እሴት)))[0]


def 수정유티에프해독(ውሂብ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ኅብረቁምፊ_እሴት = ውሂብ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ኅብረቁምፊ_እሴት.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class መደብ_እሴት:
    def __init__(자신, መተላለፊያ):
        자신.መተላለፊያ = መተላለፊያ
        አንባቢ_እሴት = 자료읽기(መተላለፊያ.read_bytes())
        if አንባቢ_እሴት.수('I') != 0xcafebabe:
            raise 컴파일오류('Java መደብ_እሴት 표식이 아님')
        አንባቢ_እሴት.ማንበቢያ(4)
        개수 = አንባቢ_እሴት.수('H')
        자신.ቋሚ_እሴት = [None] * 개수
        መረጃ_ጠቆመ = 1
        while መረጃ_ጠቆመ < 개수:
            종류 = አንባቢ_እሴት.수('B')
            if 종류 == 1:
                እሴት = 수정유티에프해독(አንባቢ_እሴት.ማንበቢያ(አንባቢ_እሴት.수('H')))
            elif 종류 == 3:
                እሴት = አንባቢ_እሴት.수('i')
            elif 종류 == 4:
                እሴት = አንባቢ_እሴት.ማንበቢያ(4)
            elif 종류 in (5, 6):
                እሴት = አንባቢ_እሴት.ማንበቢያ(8)
            elif 종류 in (7, 8, 16):
                እሴት = አንባቢ_እሴት.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                እሴት = (አንባቢ_እሴት.수('H'), አንባቢ_እሴት.수('H'))
            elif 종류 == 15:
                እሴት = (አንባቢ_እሴት.수('B'), አንባቢ_እሴት.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 ቋሚ_እሴት 종류: {}'.format(종류))
            자신.ቋሚ_እሴት[መረጃ_ጠቆመ] = (종류, እሴት)
            መረጃ_ጠቆመ += 2 if 종류 in (5, 6) else 1
        자신.መዳረሻ_ምዝግብ = አንባቢ_እሴት.수('H')
        자신.ስም = 자신.መደብ_ስም(አንባቢ_እሴት.수('H'))
        부모 = አንባቢ_እሴት.수('H')
        if 자신.መደብ_ስም(부모) != 'java/lang/Object' or አንባቢ_እሴት.수('H') != 0:
            raise 컴파일오류(자신.ስም + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.መስክ_እሴት = 자신.멤버읽기(አንባቢ_እሴት)
        자신.ተግባር_እሴት = 자신.멤버읽기(አንባቢ_እሴት)
        자신.속성읽기(አንባቢ_እሴት)

    def 문자(자신, መረጃ_ጠቆመ):
        if 자신.ቋሚ_እሴት[መረጃ_ጠቆመ][0] != 1:
            raise 컴파일오류('ኅብረቁምፊ_እሴት ቋሚ_እሴት ቅርጸት_እሴት ስህተት')
        return 자신.ቋሚ_እሴት[መረጃ_ጠቆመ][1]

    def መደብ_ስም(자신, መረጃ_ጠቆመ):
        return 자신.문자(자신.ቋሚ_እሴት[መረጃ_ጠቆመ][1])

    def ማጣቀሻ(자신, መረጃ_ጠቆመ):
        ባለቤት_እሴት, ስም_ቅርጸት = 자신.ቋሚ_እሴት[መረጃ_ጠቆመ][1]
        ስም, ቅርጸት_እሴት = 자신.ቋሚ_እሴት[ስም_ቅርጸት][1]
        return 자신.መደብ_ስም(ባለቤት_እሴት), 자신.문자(ስም), 자신.문자(ቅርጸት_እሴት)

    def 속성읽기(자신, አንባቢ_እሴት):
        ልኬት = {}
        for _ in range(አንባቢ_እሴት.수('H')):
            ስም = 자신.문자(አንባቢ_እሴት.수('H'))
            ልኬት[ስም] = አንባቢ_እሴት.ማንበቢያ(አንባቢ_እሴት.수('I'))
        return ልኬት

    def 멤버읽기(자신, አንባቢ_እሴት):
        ልኬት = []
        for _ in range(አንባቢ_እሴት.수('H')):
            መዳረሻ_ምዝግብ = አንባቢ_እሴት.수('H')
            ስም = 자신.문자(አንባቢ_እሴት.수('H'))
            ቅርጸት_እሴት = 자신.문자(አንባቢ_እሴት.수('H'))
            ልኬት.append((መዳረሻ_ምዝግብ, ስም, ቅርጸት_እሴት, 자신.속성읽기(አንባቢ_እሴት)))
        return ልኬት


def 형식읽기(ኅብረቁምፊ_እሴት):
    ልኬት = []
    አካባቢ = 0
    while አካባቢ < len(ኅብረቁምፊ_እሴት):
        for ቅርጸት_እሴት in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ኅብረቁምፊ_እሴት.startswith(ቅርጸት_እሴት, አካባቢ):
                ልኬት.append(ቅርጸት_እሴት)
                አካባቢ += len(ቅርጸት_እሴት)
                break
        else:
            raise 컴파일오류('지원하지 않는 የውሂብ_ዓይነት: ' + ኅብረቁምፊ_እሴት)
    return ልኬት


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('ተግባር_እሴት 서술 ቅርጸት_እሴት ስህተት: ' + 서술)
    return 인수, 반환


def ምልክት_ad6f1a96(종류, *부분):
    ምንጭ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ምንጭ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ተግባር_እሴት 서술에 대해서만 허용한다.
def ፈጽም_ትእዛዝ(인수=None):
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ምንጭ_ዛፍ ግንብ_ስርዓት')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/መደብ_እሴት 디렉터리')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 ግንብ_ስርዓት JDK 또는 openjdk-build의 부트 JDK መተላለፊያ')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--bundle-runtime', help='ፈጽም_ትእዛዝ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK ፕሮግራም_የመተግበሪያ_መሳቢያ/ምንጭ_ዛፍ 빌드의 C 컴파일러')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ግንብ_ስርዓት 작업 수')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ግንብ_ስርዓት ዓላማ (예: aarch64-linux-gnu)')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--sysroot', help='교차 ግንብ_ስርዓት 대상의 libc/헤더/ማከማቻ_ስፍራ 루트')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ቅርጸት_እሴት')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=መደብ_እሴት.ተግባር_እሴት (자체 스택 ABI)')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--entry', help='예: 계산.ማስኬጃ (openjdk-build 이외 대상에서 필수)')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('-o', '--output', required=True, help='ፈጽም_ትእዛዝ ELF/.o ውጤት; openjdk-build는 전용 ግንብ_ስርዓት 디렉터리')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('sources', nargs='+')
    ግቤት_ነጋሪ_እሴት = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args(인수)
    if ግቤት_ነጋሪ_እሴት.target == 'openjdk-build':
        if len(ግቤት_ነጋሪ_እሴት.sources) != 1 or not ግቤት_ነጋሪ_እሴት.java_home or ግቤት_ነጋሪ_እሴት.entry or ግቤት_ነጋሪ_እሴት.export or ግቤት_ነጋሪ_እሴት.classpath or ግቤት_ነጋሪ_እሴት.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ምንጭ_ዛፍ 디렉터리 하나와 --java-home 부트 JDK, -o ግንብ_ስርዓት 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(ግቤት_ነጋሪ_እሴት.sources[0], ግቤት_ነጋሪ_እሴት.output, ግቤት_ነጋሪ_እሴት.java_home, ግቤት_ነጋሪ_እሴት.jobs, ግቤት_ነጋሪ_እሴት.openjdk_target,
                  ግቤት_ነጋሪ_እሴት.sysroot, None if ግቤት_ነጋሪ_እሴት.cc == 'cc' else ግቤት_ነጋሪ_እሴት.cc, ግቤት_ነጋሪ_እሴት.cxx, ግቤት_ነጋሪ_እሴት.configure_arg)
        except BuildError as ስህተት:
            raise 컴파일오류(str(ስህተት))
        return
    if not ግቤት_ነጋሪ_እሴት.entry:
        አግልሎ_ማስቀመጥ_48ee4b1b.error('--entry is required for this target')
    if ግቤት_ነጋሪ_እሴት.cxx or ግቤት_ነጋሪ_እሴት.openjdk_target or ግቤት_ነጋሪ_እሴት.sysroot or ግቤት_ነጋሪ_እሴት.configure_arg or ግቤት_ነጋሪ_እሴት.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ዓላማ 전용')
    if ግቤት_ነጋሪ_እሴት.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ፍጠር_ምዝግብ
        ፍጠር_ምዝግብ(ግቤት_ነጋሪ_እሴት)
        return
    if ግቤት_ነጋሪ_እሴት.classpath or ግቤት_ነጋሪ_እሴት.java_home or ግቤት_ነጋሪ_እሴት.bundle_runtime or ግቤት_ነጋሪ_እሴት.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ዓላማ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', ግቤት_ነጋሪ_እሴት.target, '--entry', ግቤት_ነጋሪ_እሴት.entry, '-o', ግቤት_ነጋሪ_እሴት.output]
    for 지정 in ግቤት_ነጋሪ_እሴት.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+ግቤት_ነጋሪ_እሴት.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ፈጽም_ትእዛዝ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ስህተት:
        print('መገንባት_ምንጭ ስህተት: ' + str(ስህተት), file=sys.stderr)
        sys.exit(1)
