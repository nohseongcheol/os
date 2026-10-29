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
    def __init__(자신, иттилоот):
        자신.иттилоот = иттилоот
        자신.위치 = 0

    def Хондан(자신, дарозӣ_қимат):
        if дарозӣ_қимат < 0 or 자신.위치 + дарозӣ_қимат > len(자신.иттилоот):
            raise 컴파일오류('잘린 синф_қимат 또는 фармон иттилоот')
        결과 = 자신.иттилоот[자신.위치:자신.위치 + дарозӣ_қимат]
        자신.위치 += дарозӣ_қимат
        return 결과

    def 수(자신, формат_қимат):
        return struct.unpack('>' + формат_қимат, 자신.Хондан(struct.calcsize('>' + формат_қимат)))[0]


def 수정유티에프해독(иттилоот):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    сатр_қимат_6ca8363c = иттилоот.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return сатр_қимат_6ca8363c.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class синф_қимат:
    def __init__(자신, масир):
        자신.масир = масир
        Хонанда_қимат = 자료읽기(масир.read_bytes())
        if Хонанда_қимат.수('I') != 0xcafebabe:
            raise 컴파일오류('Java синф_қимат 표식이 아님')
        Хонанда_қимат.Хондан(4)
        개수 = Хонанда_қимат.수('H')
        자신.доимӣ_қимат = [None] * 개수
        индекс = 1
        while индекс < 개수:
            종류 = Хонанда_қимат.수('B')
            if 종류 == 1:
                қимат = 수정유티에프해독(Хонанда_қимат.Хондан(Хонанда_қимат.수('H')))
            elif 종류 == 3:
                қимат = Хонанда_қимат.수('i')
            elif 종류 == 4:
                қимат = Хонанда_қимат.Хондан(4)
            elif 종류 in (5, 6):
                қимат = Хонанда_қимат.Хондан(8)
            elif 종류 in (7, 8, 16):
                қимат = Хонанда_қимат.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                қимат = (Хонанда_қимат.수('H'), Хонанда_қимат.수('H'))
            elif 종류 == 15:
                қимат = (Хонанда_қимат.수('B'), Хонанда_қимат.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 доимӣ_қимат 종류: {}'.format(종류))
            자신.доимӣ_қимат[индекс] = (종류, қимат)
            индекс += 2 if 종류 in (5, 6) else 1
        자신.дастрасӣ_ворида = Хонанда_қимат.수('H')
        자신.Ном = 자신.синф_ном(Хонанда_қимат.수('H'))
        부모 = Хонанда_қимат.수('H')
        if 자신.синф_ном(부모) != 'java/lang/Object' or Хонанда_қимат.수('H') != 0:
            raise 컴파일오류(자신.Ном + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.майдон_қимат = 자신.멤버읽기(Хонанда_қимат)
        자신.функсия_қимат = 자신.멤버읽기(Хонанда_қимат)
        자신.속성읽기(Хонанда_қимат)

    def 문자(자신, индекс):
        if 자신.доимӣ_қимат[индекс][0] != 1:
            raise 컴파일오류('сатр_қимат_6ca8363c доимӣ_қимат формат_қимат Хато')
        return 자신.доимӣ_қимат[индекс][1]

    def синф_ном(자신, индекс):
        return 자신.문자(자신.доимӣ_қимат[индекс][1])

    def Маълумотнома(자신, индекс):
        молик_қимат, ном_формат = 자신.доимӣ_қимат[индекс][1]
        Ном, формат_қимат = 자신.доимӣ_қимат[ном_формат][1]
        return 자신.синф_ном(молик_қимат), 자신.문자(Ном), 자신.문자(формат_қимат)

    def 속성읽기(자신, Хонанда_қимат):
        결과 = {}
        for _ in range(Хонанда_қимат.수('H')):
            Ном = 자신.문자(Хонанда_қимат.수('H'))
            결과[Ном] = Хонанда_қимат.Хондан(Хонанда_қимат.수('I'))
        return 결과

    def 멤버읽기(자신, Хонанда_қимат):
        결과 = []
        for _ in range(Хонанда_қимат.수('H')):
            дастрасӣ_ворида = Хонанда_қимат.수('H')
            Ном = 자신.문자(Хонанда_қимат.수('H'))
            формат_қимат = 자신.문자(Хонанда_қимат.수('H'))
            결과.append((дастрасӣ_ворида, Ном, формат_қимат, 자신.속성읽기(Хонанда_қимат)))
        return 결과


def 형식읽기(сатр_қимат_6ca8363c):
    결과 = []
    위치 = 0
    while 위치 < len(сатр_қимат_6ca8363c):
        for формат_қимат in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if сатр_қимат_6ca8363c.startswith(формат_қимат, 위치):
                결과.append(формат_қимат)
                위치 += len(формат_қимат)
                break
        else:
            raise 컴파일오류('지원하지 않는 намуди_маълумот: ' + сатр_қимат_6ca8363c)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('функсия_қимат 서술 формат_қимат Хато: ' + 서술)
    return 인수, 반환


def аломат(종류, *부분):
    манбаъ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(манбаъ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 функсия_қимат 서술에 대해서만 허용한다.
def иҷро_кардан_фармон(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK манбаъ_дарахт сохт_система')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/синф_қимат 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 сохт_система JDK 또는 openjdk-build의 부트 JDK масир')
    해석기.add_argument('--bundle-runtime', help='иҷро_кардан_фармон 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK барнома_панели_барномаҳо/манбаъ_дарахт 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 сохт_система 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 сохт_система ҳадаф (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 сохт_система 대상의 libc/헤더/китобхона 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 формат_қимат')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=синф_қимат.функсия_қимат (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.порча (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='иҷро_кардан_фармон ELF/.o 출력; openjdk-build는 전용 сохт_система 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK манбаъ_дарахт 디렉터리 하나와 --java-home 부트 JDK, -o сохт_система 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Хато:
            raise 컴파일오류(str(Хато))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ҳадаф 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import эҷод_кардан_ворида
        эҷод_кардан_ворида(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ҳадаф 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        иҷро_кардан_фармон()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Хато:
        print('сохтан_манбаъ Хато: ' + str(Хато), file=sys.stderr)
        sys.exit(1)
