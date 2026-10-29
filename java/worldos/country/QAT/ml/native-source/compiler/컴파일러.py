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
    def __init__(자신, ഡാറ്റാ):
        자신.ഡാറ്റാ = ഡാറ്റാ
        자신.സ്ഥാനം = 0

    def വായന(자신, ദൈര്_ഘ്യം_മൂല്യം):
        if ദൈര്_ഘ്യം_മൂല്യം < 0 or 자신.സ്ഥാനം + ദൈര്_ഘ്യം_മൂല്യം > len(자신.ഡാറ്റാ):
            raise 컴파일오류('잘린 ക്ലാസ്_മൂല്യം 또는 ആജ്ഞ ഡാറ്റാ')
        അളവ് = 자신.ഡാറ്റാ[자신.സ്ഥാനം:자신.സ്ഥാനം + ദൈര്_ഘ്യം_മൂല്യം]
        자신.സ്ഥാനം += ദൈര്_ഘ്യം_മൂല്യം
        return അളവ്

    def 수(자신, ఫార్మాట్_മൂല്യം):
        return struct.unpack('>' + ఫార్మాట్_മൂല്യം, 자신.വായന(struct.calcsize('>' + ఫార్మాట్_മൂല്യം)))[0]


def 수정유티에프해독(ഡാറ്റാ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    സ്ട്രിംഗ്_മൂല്യം = ഡാറ്റാ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return സ്ട്രിംഗ്_മൂല്യം.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ക്ലാസ്_മൂല്യം:
    def __init__(자신, വഴി):
        자신.വഴി = വഴി
        റീഡര്_മൂല്യം = 자료읽기(വഴി.read_bytes())
        if റീഡര്_മൂല്യം.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ക്ലാസ്_മൂല്യം 표식이 아님')
        റീഡര്_മൂല്യം.വായന(4)
        개수 = റീഡര്_മൂല്യം.수('H')
        자신.സ്ഥിരം_മൂല്യം = [None] * 개수
        സൂചിക = 1
        while സൂചിക < 개수:
            종류 = റീഡര്_മൂല്യം.수('B')
            if 종류 == 1:
                മൂല്യം = 수정유티에프해독(റീഡര്_മൂല്യം.വായന(റീഡര്_മൂല്യം.수('H')))
            elif 종류 == 3:
                മൂല്യം = റീഡര്_മൂല്യം.수('i')
            elif 종류 == 4:
                മൂല്യം = റീഡര്_മൂല്യം.വായന(4)
            elif 종류 in (5, 6):
                മൂല്യം = റീഡര്_മൂല്യം.വായന(8)
            elif 종류 in (7, 8, 16):
                മൂല്യം = റീഡര്_മൂല്യം.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                മൂല്യം = (റീഡര്_മൂല്യം.수('H'), റീഡര്_മൂല്യം.수('H'))
            elif 종류 == 15:
                മൂല്യം = (റീഡര്_മൂല്യം.수('B'), റീഡര്_മൂല്യം.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 സ്ഥിരം_മൂല്യം 종류: {}'.format(종류))
            자신.സ്ഥിരം_മൂല്യം[സൂചിക] = (종류, മൂല്യം)
            സൂചിക += 2 if 종류 in (5, 6) else 1
        자신.ആക്സസ്_എന്_ട്രി = റീഡര്_മൂല്യം.수('H')
        자신.പേരു് = 자신.ക്ലാസ്_നാ_മം(റീഡര്_മൂല്യം.수('H'))
        부모 = റീഡര്_മൂല്യം.수('H')
        if 자신.ക്ലാസ്_നാ_മം(부모) != 'java/lang/Object' or റീഡര്_മൂല്യം.수('H') != 0:
            raise 컴파일오류(자신.പേരു് + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.മണ്ഡലം_മൂല്യം = 자신.멤버읽기(റീഡര്_മൂല്യം)
        자신.കാര്യപ്രവര്_ത്തനം_മൂല്യം = 자신.멤버읽기(റീഡര്_മൂല്യം)
        자신.속성읽기(റീഡര്_മൂല്യം)

    def 문자(자신, സൂചിക):
        if 자신.സ്ഥിരം_മൂല്യം[സൂചിക][0] != 1:
            raise 컴파일오류('സ്ട്രിംഗ്_മൂല്യം സ്ഥിരം_മൂല്യം ఫార్మాట్_മൂല്യം പിശക്')
        return 자신.സ്ഥിരം_മൂല്യം[സൂചിക][1]

    def ക്ലാസ്_നാ_മം(자신, സൂചിക):
        return 자신.문자(자신.സ്ഥിരം_മൂല്യം[സൂചിക][1])

    def റഫറൻസ്(자신, സൂചിക):
        ഉടമ_മൂല്യം, നാ_മം_ఫార్మాట్ = 자신.സ്ഥിരം_മൂല്യം[സൂചിക][1]
        പേരു്, ఫార్మాట్_മൂല്യം = 자신.സ്ഥിരം_മൂല്യം[നാ_മം_ఫార్మాట్][1]
        return 자신.ക്ലാസ്_നാ_മം(ഉടമ_മൂല്യം), 자신.문자(പേരു്), 자신.문자(ఫార్మాట్_മൂല്യം)

    def 속성읽기(자신, റീഡര്_മൂല്യം):
        അളവ് = {}
        for _ in range(റീഡര്_മൂല്യം.수('H')):
            പേരു് = 자신.문자(റീഡര്_മൂല്യം.수('H'))
            അളവ്[പേരു്] = റീഡര്_മൂല്യം.വായന(റീഡര്_മൂല്യം.수('I'))
        return അളവ്

    def 멤버읽기(자신, റീഡര്_മൂല്യം):
        അളവ് = []
        for _ in range(റീഡര്_മൂല്യം.수('H')):
            ആക്സസ്_എന്_ട്രി = റീഡര്_മൂല്യം.수('H')
            പേരു് = 자신.문자(റീഡര്_മൂല്യം.수('H'))
            ఫార్మాట్_മൂല്യം = 자신.문자(റീഡര്_മൂല്യം.수('H'))
            അളവ്.append((ആക്സസ്_എന്_ട്രി, പേരു്, ఫార్మాట్_മൂല്യം, 자신.속성읽기(റീഡര്_മൂല്യം)))
        return അളവ്


def 형식읽기(സ്ട്രിംഗ്_മൂല്യം):
    അളവ് = []
    സ്ഥാനം = 0
    while സ്ഥാനം < len(സ്ട്രിംഗ്_മൂല്യം):
        for ఫార్మాట్_മൂല്യം in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if സ്ട്രിംഗ്_മൂല്യം.startswith(ఫార్మాట్_മൂല്യം, സ്ഥാനം):
                അളവ്.append(ఫార్మాట్_മൂല്യം)
                സ്ഥാനം += len(ఫార్మాట్_മൂല്യം)
                break
        else:
            raise 컴파일오류('지원하지 않는 ഡാറ്റാ_തരം: ' + സ്ട്രിംഗ്_മൂല്യം)
    return അളവ്


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('കാര്യപ്രവര്_ത്തനം_മൂല്യം 서술 ఫార్మాట్_മൂല്യം പിശക്: ' + 서술)
    return 인수, 반환


def nbsp_ചിഹ്നം(종류, *부분):
    ഉറവിടം = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ഉറവിടം).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 കാര്യപ്രവര്_ത്തനം_മൂല്യം 서술에 대해서만 허용한다.
def നടപ്പാക്കുക_കമാന്_ഡ്(인수=None):
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ഉറവിടം_ശാഖി ബിൽഡ്_సిస్టమ్')
    പാഴ്_സർ_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    പാഴ്_സർ_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ക്ലാസ്_മൂല്യം 디렉터리')
    പാഴ്_സർ_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 ബിൽഡ്_సిస్టమ్ JDK 또는 openjdk-build의 부트 JDK വഴി')
    പാഴ്_സർ_48ee4b1b.add_argument('--bundle-runtime', help='നടപ്പാക്കുക_കമാന്_ഡ് 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    പാഴ്_സർ_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ/ഉറവിടം_ശാഖി 빌드의 C 컴파일러')
    പാഴ്_സർ_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    പാഴ്_സർ_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ബിൽഡ്_సిస్టమ్ 작업 수')
    പാഴ്_സർ_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ബിൽഡ്_సిస్టమ్ ലക്_ഷ്യം (예: aarch64-linux-gnu)')
    പാഴ്_സർ_48ee4b1b.add_argument('--sysroot', help='교차 ബിൽഡ്_సిస్టమ్ 대상의 libc/헤더/లైబ్రరీ 루트')
    പാഴ്_സർ_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ఫార్మాట్_മൂല്യം')
    പാഴ്_സർ_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=ക്ലാസ്_മൂല്യം.കാര്യപ്രവര്_ത്തനം_മൂല്യം (자체 스택 ABI)')
    പാഴ്_സർ_48ee4b1b.add_argument('--entry', help='예: 계산.നടപ്പിലാക്കുക (openjdk-build 이외 대상에서 필수)')
    പാഴ്_സർ_48ee4b1b.add_argument('-o', '--output', required=True, help='നടപ്പാക്കുക_കമാന്_ഡ് ELF/.o ഫലം; openjdk-build는 전용 ബിൽഡ്_సిస్టమ్ 디렉터리')
    പാഴ്_സർ_48ee4b1b.add_argument('sources', nargs='+')
    പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ് = പാഴ്_സർ_48ee4b1b.parse_args(인수)
    if പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.target == 'openjdk-build':
        if len(പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.sources) != 1 or not പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.java_home or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.entry or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.export or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.classpath or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ഉറവിടം_ശാഖി 디렉터리 하나와 --java-home 부트 JDK, -o ബിൽഡ്_సిస్టమ్ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.sources[0], പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.output, പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.java_home, പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.jobs, പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.openjdk_target,
                  പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.sysroot, None if പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.cc == 'cc' else പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.cc, പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.cxx, പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.configure_arg)
        except BuildError as പിശക്:
            raise 컴파일오류(str(പിശക്))
        return
    if not പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.entry:
        പാഴ്_സർ_48ee4b1b.error('--entry is required for this target')
    if പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.cxx or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.openjdk_target or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.sysroot or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.configure_arg or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ലക്_ഷ്യം 전용')
    if പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from നിര്_വ്വഹണക്ഷമമായ_ഫയല് import സൃഷ്_ടിക്കുക_എന്_ട്രി
        സൃഷ്_ടിക്കുക_എന്_ട്രി(പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്)
        return
    if പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.classpath or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.java_home or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.bundle_runtime or പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ലക്_ഷ്യം 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.target, '--entry', പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.entry, '-o', പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.output]
    for അസൈൻ_ചെയ്യുക_മൂല്യം in പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.export: 자바명령.extend(['--export', അസൈൻ_ചെയ്യുക_മൂല്യം])
    subprocess.run(자바명령+പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.sources, check=True)
    return


if __name__ == '__main__':
    try:
        നടപ്പാക്കുക_കമാന്_ഡ്()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as പിശക്:
        print('കംപൈല്_ചെയ്യുക_ഉറവിടം പിശക്: ' + str(പിശക്), file=sys.stderr)
        sys.exit(1)
