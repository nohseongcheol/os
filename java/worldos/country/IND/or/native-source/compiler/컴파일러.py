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
    def __init__(자신, ଡାଟା):
        자신.ଡାଟା = ଡାଟା
        자신.ଅବସ୍ଥାନ = 0

    def ପଢନ୍ତୁ(자신, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ):
        if ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ < 0 or 자신.ଅବସ୍ଥାନ + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ > len(자신.ଡାଟା):
            raise 컴파일오류('잘린 ଶ୍ରେଣୀ_ମୂଲ୍ୟ_55654bf1 또는 ନିର୍ଦ୍ଦେଶ ଡାଟା')
        ମାପ = 자신.ଡାଟା[자신.ଅବସ୍ଥାନ:자신.ଅବସ୍ଥାନ + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ]
        자신.ଅବସ୍ଥାନ += ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ
        return ମାପ

    def 수(자신, ଫର୍ମାଟ୍_ମୂଲ୍ୟ):
        return struct.unpack('>' + ଫର୍ମାଟ୍_ମୂଲ୍ୟ, 자신.ପଢନ୍ତୁ(struct.calcsize('>' + ଫର୍ମାଟ୍_ମୂଲ୍ୟ)))[0]


def 수정유티에프해독(ଡାଟା):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ = ଡାଟା.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ଶ୍ରେଣୀ_ମୂଲ୍ୟ_55654bf1:
    def __init__(자신, ପଥ):
        자신.ପଥ = ପଥ
        ପାଠକ_ମୂଲ୍ୟ = 자료읽기(ପଥ.read_bytes())
        if ପାଠକ_ମୂଲ୍ୟ.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ଶ୍ରେଣୀ_ମୂଲ୍ୟ_55654bf1 표식이 아님')
        ପାଠକ_ମୂଲ୍ୟ.ପଢନ୍ତୁ(4)
        개수 = ପାଠକ_ମୂଲ୍ୟ.수('H')
        자신.ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ = [None] * 개수
        ଅନୁକ୍ରମଣିକା = 1
        while ଅନୁକ୍ରମଣିକା < 개수:
            종류 = ପାଠକ_ମୂଲ୍ୟ.수('B')
            if 종류 == 1:
                ମୂଲ୍ୟ = 수정유티에프해독(ପାଠକ_ମୂଲ୍ୟ.ପଢନ୍ତୁ(ପାଠକ_ମୂଲ୍ୟ.수('H')))
            elif 종류 == 3:
                ମୂଲ୍ୟ = ପାଠକ_ମୂଲ୍ୟ.수('i')
            elif 종류 == 4:
                ମୂଲ୍ୟ = ପାଠକ_ମୂଲ୍ୟ.ପଢନ୍ତୁ(4)
            elif 종류 in (5, 6):
                ମୂଲ୍ୟ = ପାଠକ_ମୂଲ୍ୟ.ପଢନ୍ତୁ(8)
            elif 종류 in (7, 8, 16):
                ମୂଲ୍ୟ = ପାଠକ_ମୂଲ୍ୟ.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ମୂଲ୍ୟ = (ପାଠକ_ମୂଲ୍ୟ.수('H'), ପାଠକ_ମୂଲ୍ୟ.수('H'))
            elif 종류 == 15:
                ମୂଲ୍ୟ = (ପାଠକ_ମୂଲ୍ୟ.수('B'), ପାଠକ_ମୂଲ୍ୟ.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ 종류: {}'.format(종류))
            자신.ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ[ଅନୁକ୍ରମଣିକା] = (종류, ମୂଲ୍ୟ)
            ଅନୁକ୍ରମଣିକା += 2 if 종류 in (5, 6) else 1
        자신.ପ୍ରବେଶ_ଏଣ୍ଟ୍ରି = ପାଠକ_ମୂଲ୍ୟ.수('H')
        자신.ନାମ = 자신.ଶ୍ରେଣୀ_ନାମ(ପାଠକ_ମୂଲ୍ୟ.수('H'))
        부모 = ପାଠକ_ମୂଲ୍ୟ.수('H')
        if 자신.ଶ୍ରେଣୀ_ନାମ(부모) != 'java/lang/Object' or ପାଠକ_ମୂଲ୍ୟ.수('H') != 0:
            raise 컴파일오류(자신.ନାମ + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ଫିଲ୍ଡ_ମୂଲ୍ୟ = 자신.멤버읽기(ପାଠକ_ମୂଲ୍ୟ)
        자신.Excel_ଟେବଲ୍_ମୂଲ୍ୟ = 자신.멤버읽기(ପାଠକ_ମୂଲ୍ୟ)
        자신.속성읽기(ପାଠକ_ମୂଲ୍ୟ)

    def 문자(자신, ଅନୁକ୍ରମଣିକା):
        if 자신.ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ[ଅନୁକ୍ରମଣିକା][0] != 1:
            raise 컴파일오류('ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ ଫର୍ମାଟ୍_ମୂଲ୍ୟ ତ୍ରୁଟି')
        return 자신.ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ[ଅନୁକ୍ରମଣିକା][1]

    def ଶ୍ରେଣୀ_ନାମ(자신, ଅନୁକ୍ରମଣିକା):
        return 자신.문자(자신.ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ[ଅନୁକ୍ରମଣିକା][1])

    def ପ୍ରସଙ୍ଗ(자신, ଅନୁକ୍ରମଣିକା):
        ମାଲିକ_ମୂଲ୍ୟ, ନାମ_ଫର୍ମାଟ୍ = 자신.ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ[ଅନୁକ୍ରମଣିକା][1]
        ନାମ, ଫର୍ମାଟ୍_ମୂଲ୍ୟ = 자신.ସ୍ଥିରାଙ୍କ_ମୂଲ୍ୟ[ନାମ_ଫର୍ମାଟ୍][1]
        return 자신.ଶ୍ରେଣୀ_ନାମ(ମାଲିକ_ମୂଲ୍ୟ), 자신.문자(ନାମ), 자신.문자(ଫର୍ମାଟ୍_ମୂଲ୍ୟ)

    def 속성읽기(자신, ପାଠକ_ମୂଲ୍ୟ):
        ମାପ = {}
        for _ in range(ପାଠକ_ମୂଲ୍ୟ.수('H')):
            ନାମ = 자신.문자(ପାଠକ_ମୂଲ୍ୟ.수('H'))
            ମାପ[ନାମ] = ପାଠକ_ମୂଲ୍ୟ.ପଢନ୍ତୁ(ପାଠକ_ମୂଲ୍ୟ.수('I'))
        return ମାପ

    def 멤버읽기(자신, ପାଠକ_ମୂଲ୍ୟ):
        ମାପ = []
        for _ in range(ପାଠକ_ମୂଲ୍ୟ.수('H')):
            ପ୍ରବେଶ_ଏଣ୍ଟ୍ରି = ପାଠକ_ମୂଲ୍ୟ.수('H')
            ନାମ = 자신.문자(ପାଠକ_ମୂଲ୍ୟ.수('H'))
            ଫର୍ମାଟ୍_ମୂଲ୍ୟ = 자신.문자(ପାଠକ_ମୂଲ୍ୟ.수('H'))
            ମାପ.append((ପ୍ରବେଶ_ଏଣ୍ଟ୍ରି, ନାମ, ଫର୍ମାଟ୍_ମୂଲ୍ୟ, 자신.속성읽기(ପାଠକ_ମୂଲ୍ୟ)))
        return ମାପ


def 형식읽기(ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ):
    ମାପ = []
    ଅବସ୍ଥାନ = 0
    while ଅବସ୍ଥାନ < len(ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ):
        for ଫର୍ମାଟ୍_ମୂଲ୍ୟ in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ.startswith(ଫର୍ମାଟ୍_ମୂଲ୍ୟ, ଅବସ୍ଥାନ):
                ମାପ.append(ଫର୍ମାଟ୍_ମୂଲ୍ୟ)
                ଅବସ୍ଥାନ += len(ଫର୍ମାଟ୍_ମୂଲ୍ୟ)
                break
        else:
            raise 컴파일오류('지원하지 않는 ଡାଟା_ପ୍ରକାର: ' + ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ)
    return ମାପ


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('Excel_ଟେବଲ୍_ମୂଲ୍ୟ 서술 ଫର୍ମାଟ୍_ମୂଲ୍ୟ ତ୍ରୁଟି: ' + 서술)
    return 인수, 반환


def ସଙ୍କେତ(종류, *부분):
    ଉତ୍ସ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ଉତ୍ସ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 Excel_ଟେବଲ୍_ମୂଲ୍ୟ 서술에 대해서만 허용한다.
def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ଉତ୍ସ_ବୃକ୍ଷ ବିଲ୍ଡ୍_ସିଷ୍ଟମ')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ଶ୍ରେଣୀ_ମୂଲ୍ୟ_55654bf1 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 ବିଲ୍ଡ୍_ସିଷ୍ଟମ JDK 또는 openjdk-build의 부트 JDK ପଥ')
    해석기.add_argument('--bundle-runtime', help='ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍/ଉତ୍ସ_ବୃକ୍ଷ 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ବିଲ୍ଡ୍_ସିଷ୍ଟମ 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ବିଲ୍ଡ୍_ସିଷ୍ଟମ ଲକ୍ଷ୍ୟସ୍ଥଳ (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 ବିଲ୍ଡ୍_ସିଷ୍ଟମ 대상의 libc/헤더/ଲାଇବ୍ରେରୀ 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ଫର୍ମାଟ୍_ମୂଲ୍ୟ')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=ଶ୍ରେଣୀ_ମୂଲ୍ୟ_55654bf1.Excel_ଟେବଲ୍_ମୂଲ୍ୟ (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ଚଳାନ୍ତୁ (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ ELF/.o ନିର୍ଗମ; openjdk-build는 전용 ବିଲ୍ଡ୍_ସିଷ୍ଟମ 디렉터리')
    해석기.add_argument('sources', nargs='+')
    ପାରାମିଟର୍_ଯୁକ୍ତି = 해석기.parse_args(인수)
    if ପାରାମିଟର୍_ଯୁକ୍ତି.target == 'openjdk-build':
        if len(ପାରାମିଟର୍_ଯୁକ୍ତି.sources) != 1 or not ପାରାମିଟର୍_ଯୁକ୍ତି.java_home or ପାରାମିଟର୍_ଯୁକ୍ତି.entry or ପାରାମିଟର୍_ଯୁକ୍ତି.export or ପାରାମିଟର୍_ଯୁକ୍ତି.classpath or ପାରାମିଟର୍_ଯୁକ୍ତି.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ଉତ୍ସ_ବୃକ୍ଷ 디렉터리 하나와 --java-home 부트 JDK, -o ବିଲ୍ଡ୍_ସିଷ୍ଟମ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(ପାରାମିଟର୍_ଯୁକ୍ତି.sources[0], ପାରାମିଟର୍_ଯୁକ୍ତି.output, ପାରାମିଟର୍_ଯୁକ୍ତି.java_home, ପାରାମିଟର୍_ଯୁକ୍ତି.jobs, ପାରାମିଟର୍_ଯୁକ୍ତି.openjdk_target,
                  ପାରାମିଟର୍_ଯୁକ୍ତି.sysroot, None if ପାରାମିଟର୍_ଯୁକ୍ତି.cc == 'cc' else ପାରାମିଟର୍_ଯୁକ୍ତି.cc, ପାରାମିଟର୍_ଯୁକ୍ତି.cxx, ପାରାମିଟର୍_ଯୁକ୍ତି.configure_arg)
        except BuildError as ତ୍ରୁଟି:
            raise 컴파일오류(str(ତ୍ରୁଟି))
        return
    if not ପାରାମିଟର୍_ଯୁକ୍ତି.entry:
        해석기.error('--entry is required for this target')
    if ପାରାମିଟର୍_ଯୁକ୍ତି.cxx or ପାରାମିଟର୍_ଯୁକ୍ତି.openjdk_target or ପାରାମିଟର୍_ଯୁକ୍ତି.sysroot or ପାରାମିଟର୍_ଯୁକ୍ତି.configure_arg or ପାରାମିଟର୍_ଯୁକ୍ତି.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ଲକ୍ଷ୍ୟସ୍ଥଳ 전용')
    if ପାରାମିଟର୍_ଯୁକ୍ତି.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି
        ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି(ପାରାମିଟର୍_ଯୁକ୍ତି)
        return
    if ପାରାମିଟର୍_ଯୁକ୍ତି.classpath or ପାରାମିଟର୍_ଯୁକ୍ତି.java_home or ପାରାମିଟର୍_ଯୁକ୍ତି.bundle_runtime or ପାରାମିଟର୍_ଯୁକ୍ତି.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ଲକ୍ଷ୍ୟସ୍ଥଳ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', ପାରାମିଟର୍_ଯୁକ୍ତି.target, '--entry', ପାରାମିଟର୍_ଯୁକ୍ତି.entry, '-o', ପାରାମିଟର୍_ଯୁକ୍ତି.output]
    for ନ୍ୟସ୍ତ_କରିବା_ମୂଲ୍ୟ in ପାରାମିଟର୍_ଯୁକ୍ତି.export: 자바명령.extend(['--export', ନ୍ୟସ୍ତ_କରିବା_ମୂଲ୍ୟ])
    subprocess.run(자바명령+ପାରାମିଟର୍_ଯୁକ୍ତି.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ତ୍ରୁଟି:
        print('ସଙ୍କଳନ_ଉତ୍ସ ତ୍ରୁଟି: ' + str(ତ୍ରୁଟି), file=sys.stderr)
        sys.exit(1)
