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
    def __init__(자신, ડેટા):
        자신.ડેટા = ડેટા
        자신.સ્થાન = 0

    def વાંચો(자신, લંબાઈ_મૂલ્ય):
        if લંબાઈ_મૂલ્ય < 0 or 자신.સ્થાન + લંબાઈ_મૂલ્ય > len(자신.ડેટા):
            raise 컴파일오류('잘린 વર્ગ_મૂલ્ય 또는 આદેશ ડેટા')
        પરિમાણ = 자신.ડેટા[자신.સ્થાન:자신.સ્થાન + લંબાઈ_મૂલ્ય]
        자신.સ્થાન += લંબાઈ_મૂલ્ય
        return પરિમાણ

    def 수(자신, સ્વરૂપ_મૂલ્ય):
        return struct.unpack('>' + સ્વરૂપ_મૂલ્ય, 자신.વાંચો(struct.calcsize('>' + સ્વરૂપ_મૂલ્ય)))[0]


def 수정유티에프해독(ડેટા):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    સ્ટ્રિંગ_મૂલ્ય = ડેટા.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return સ્ટ્રિંગ_મૂલ્ય.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class વર્ગ_મૂલ્ય:
    def __init__(자신, પથ):
        자신.પથ = પથ
        રીડર_મૂલ્ય = 자료읽기(પથ.read_bytes())
        if રીડર_મૂલ્ય.수('I') != 0xcafebabe:
            raise 컴파일오류('Java વર્ગ_મૂલ્ય 표식이 아님')
        રીડર_મૂલ્ય.વાંચો(4)
        개수 = રીડર_મૂલ્ય.수('H')
        자신.અચલ_મૂલ્ય = [None] * 개수
        અનુક્રમણિકા = 1
        while અનુક્રમણિકા < 개수:
            종류 = રીડર_મૂલ્ય.수('B')
            if 종류 == 1:
                મૂલ્ય = 수정유티에프해독(રીડર_મૂલ્ય.વાંચો(રીડર_મૂલ્ય.수('H')))
            elif 종류 == 3:
                મૂલ્ય = રીડર_મૂલ્ય.수('i')
            elif 종류 == 4:
                મૂલ્ય = રીડર_મૂલ્ય.વાંચો(4)
            elif 종류 in (5, 6):
                મૂલ્ય = રીડર_મૂલ્ય.વાંચો(8)
            elif 종류 in (7, 8, 16):
                મૂલ્ય = રીડર_મૂલ્ય.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                મૂલ્ય = (રીડર_મૂલ્ય.수('H'), રીડર_મૂલ્ય.수('H'))
            elif 종류 == 15:
                મૂલ્ય = (રીડર_મૂલ્ય.수('B'), રીડર_મૂલ્ય.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 અચલ_મૂલ્ય 종류: {}'.format(종류))
            자신.અચલ_મૂલ્ય[અનુક્રમણિકા] = (종류, મૂલ્ય)
            અનુક્રમણિકા += 2 if 종류 in (5, 6) else 1
        자신.ઍક્સેસ_પ્રવેશ = રીડર_મૂલ્ય.수('H')
        자신.નામ = 자신.વર્ગ_નામ(રીડર_મૂલ્ય.수('H'))
        부모 = રીડર_મૂલ્ય.수('H')
        if 자신.વર્ગ_નામ(부모) != 'java/lang/Object' or રીડર_મૂલ્ય.수('H') != 0:
            raise 컴파일오류(자신.નામ + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ફીલ્ડ_મૂલ્ય = 자신.멤버읽기(રીડર_મૂલ્ય)
        자신.ફંક્શંસ_મૂલ્ય = 자신.멤버읽기(રીડર_મૂલ્ય)
        자신.속성읽기(રીડર_મૂલ્ય)

    def 문자(자신, અનુક્રમણિકા):
        if 자신.અચલ_મૂલ્ય[અનુક્રમણિકા][0] != 1:
            raise 컴파일오류('સ્ટ્રિંગ_મૂલ્ય અચલ_મૂલ્ય સ્વરૂપ_મૂલ્ય ભૂલ')
        return 자신.અચલ_મૂલ્ય[અનુક્રમણિકા][1]

    def વર્ગ_નામ(자신, અનુક્રમણિકા):
        return 자신.문자(자신.અચલ_મૂલ્ય[અનુક્રમણિકા][1])

    def સંદર્ભ(자신, અનુક્રમણિકા):
        સ્વામી_મૂલ્ય, નામ_સ્વરૂપ = 자신.અચલ_મૂલ્ય[અનુક્રમણિકા][1]
        નામ, સ્વરૂપ_મૂલ્ય = 자신.અચલ_મૂલ્ય[નામ_સ્વરૂપ][1]
        return 자신.વર્ગ_નામ(સ્વામી_મૂલ્ય), 자신.문자(નામ), 자신.문자(સ્વરૂપ_મૂલ્ય)

    def 속성읽기(자신, રીડર_મૂલ્ય):
        પરિમાણ = {}
        for _ in range(રીડર_મૂલ્ય.수('H')):
            નામ = 자신.문자(રીડર_મૂલ્ય.수('H'))
            પરિમાણ[નામ] = રીડર_મૂલ્ય.વાંચો(રીડર_મૂલ્ય.수('I'))
        return પરિમાણ

    def 멤버읽기(자신, રીડર_મૂલ્ય):
        પરિમાણ = []
        for _ in range(રીડર_મૂલ્ય.수('H')):
            ઍક્સેસ_પ્રવેશ = રીડર_મૂલ્ય.수('H')
            નામ = 자신.문자(રીડર_મૂલ્ય.수('H'))
            સ્વરૂપ_મૂલ્ય = 자신.문자(રીડર_મૂલ્ય.수('H'))
            પરિમાણ.append((ઍક્સેસ_પ્રવેશ, નામ, સ્વરૂપ_મૂલ્ય, 자신.속성읽기(રીડર_મૂલ્ય)))
        return પરિમાણ


def 형식읽기(સ્ટ્રિંગ_મૂલ્ય):
    પરિમાણ = []
    સ્થાન = 0
    while સ્થાન < len(સ્ટ્રિંગ_મૂલ્ય):
        for સ્વરૂપ_મૂલ્ય in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if સ્ટ્રિંગ_મૂલ્ય.startswith(સ્વરૂપ_મૂલ્ય, સ્થાન):
                પરિમાણ.append(સ્વરૂપ_મૂલ્ય)
                સ્થાન += len(સ્વરૂપ_મૂલ્ય)
                break
        else:
            raise 컴파일오류('지원하지 않는 ડેટા_પ્રકાર: ' + સ્ટ્રિંગ_મૂલ્ય)
    return પરિમાણ


def 함수형식(서술):
    દલીલો, 반환 = 서술[1:].split(')')
    દલીલો = 형식읽기(દલીલો)
    반환형 = 형식읽기(반환)
    if 'V' in દલીલો or len(반환형) != 1:
        raise 컴파일오류('ફંક્શંસ_મૂલ્ય 서술 સ્વરૂપ_મૂલ્ય ભૂલ: ' + 서술)
    return દલીલો, 반환


def પ્રતીક(종류, *부분):
    સ્રોત = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(સ્રોત).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ફંક્શંસ_મૂલ્ય 서술에 대해서만 허용한다.
def અમલ_કરો_આદેશ(દલીલો=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK સ્રોત_ટ્રી બિલ્ડ_સિસ્ટમ')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/વર્ગ_મૂલ્ય 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 બિલ્ડ_સિસ્ટમ JDK 또는 openjdk-build의 부트 JDK પથ')
    해석기.add_argument('--bundle-runtime', help='અમલ_કરો_આદેશ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK એપ્લિકેશન_લૉન્ચર/સ્રોત_ટ્રી 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 બિલ્ડ_સિસ્ટમ 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 બિલ્ડ_સિસ્ટમ લક્ષ્ય (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 બિલ્ડ_સિસ્ટમ 대상의 libc/헤더/લાઇબ્રેરી 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 સ્વરૂપ_મૂલ્ય')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=વર્ગ_મૂલ્ય.ફંક્શંસ_મૂલ્ય (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ચલાવો_2 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='અમલ_કરો_આદેશ ELF/.o આઉટપુટ; openjdk-build는 전용 બિલ્ડ_સિસ્ટમ 디렉터리')
    해석기.add_argument('sources', nargs='+')
    પેરામીટર_દલીલ = 해석기.parse_args(દલીલો)
    if પેરામીટર_દલીલ.target == 'openjdk-build':
        if len(પેરામીટર_દલીલ.sources) != 1 or not પેરામીટર_દલીલ.java_home or પેરામીટર_દલીલ.entry or પેરામીટર_દલીલ.export or પેરામીટર_દલીલ.classpath or પેરામીટર_દલીલ.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK સ્રોત_ટ્રી 디렉터리 하나와 --java-home 부트 JDK, -o બિલ્ડ_સિસ્ટમ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(પેરામીટર_દલીલ.sources[0], પેરામીટર_દલીલ.output, પેરામીટર_દલીલ.java_home, પેરામીટર_દલીલ.jobs, પેરામીટર_દલીલ.openjdk_target,
                  પેરામીટર_દલીલ.sysroot, None if પેરામીટર_દલીલ.cc == 'cc' else પેરામીટર_દલીલ.cc, પેરામીટર_દલીલ.cxx, પેરામીટર_દલીલ.configure_arg)
        except BuildError as ભૂલ:
            raise 컴파일오류(str(ભૂલ))
        return
    if not પેરામીટર_દલીલ.entry:
        해석기.error('--entry is required for this target')
    if પેરામીટર_દલીલ.cxx or પેરામીટર_દલીલ.openjdk_target or પેરામીટર_દલીલ.sysroot or પેરામીટર_દલીલ.configure_arg or પેરામીટર_દલીલ.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build લક્ષ્ય 전용')
    if પેરામીટર_દલીલ.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import બનાવો_પ્રવેશ
        બનાવો_પ્રવેશ(પેરામીટર_દલીલ)
        return
    if પેરામીટર_દલીલ.classpath or પેરામીટર_દલીલ.java_home or પેરામીટર_દલીલ.bundle_runtime or પેરામીટર_દલીલ.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk લક્ષ્ય 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', પેરામીટર_દલીલ.target, '--entry', પેરામીટર_દલીલ.entry, '-o', પેરામીટર_દલીલ.output]
    for 지정 in પેરામીટર_દલીલ.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+પેરામીટર_દલીલ.sources, check=True)
    return


if __name__ == '__main__':
    try:
        અમલ_કરો_આદેશ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ભૂલ:
        print('બિલ્ડ_કરો_સ્રોત ભૂલ: ' + str(ભૂલ), file=sys.stderr)
        sys.exit(1)
