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
    def __init__(자신, ទិន្នន័យ):
        자신.ទិន្នន័យ = ទិន្នន័យ
        자신.កំណត់ទីតាំង = 0

    def អាន(자신, ប្រវែង_តំលៃ):
        if ប្រវែង_តំលៃ < 0 or 자신.កំណត់ទីតាំង + ប្រវែង_តំលៃ > len(자신.ទិន្នន័យ):
            raise 컴파일오류('잘린 ថ្នាក់_តំលៃ 또는 ពាក្យ_បញ្ជា ទិន្នន័យ')
        ការវាស់វែង = 자신.ទិន្នន័យ[자신.កំណត់ទីតាំង:자신.កំណត់ទីតាំង + ប្រវែង_តំលៃ]
        자신.កំណត់ទីតាំង += ប្រវែង_តំលៃ
        return ការវាស់វែង

    def 수(자신, ទំរង់_តំលៃ):
        return struct.unpack('>' + ទំរង់_តំលៃ, 자신.អាន(struct.calcsize('>' + ទំរង់_តំលៃ)))[0]


def 수정유티에프해독(ទិន្នន័យ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    សំនុំអក្សរ_តំលៃ = ទិន្នន័យ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return សំនុំអក្សរ_តំលៃ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ថ្នាក់_តំលៃ:
    def __init__(자신, ផ្លូវ):
        자신.ផ្លូវ = ផ្លូវ
        អ្នកអាន_តំលៃ = 자료읽기(ផ្លូវ.read_bytes())
        if អ្នកអាន_តំលៃ.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ថ្នាក់_តំលៃ 표식이 아님')
        អ្នកអាន_តំលៃ.អាន(4)
        개수 = អ្នកអាន_តំលៃ.수('H')
        자신.តំលៃថេរ_តំលៃ = [None] * 개수
        សន្ទស្សន៏ = 1
        while សន្ទស្សន៏ < 개수:
            종류 = អ្នកអាន_តំលៃ.수('B')
            if 종류 == 1:
                តំលៃ = 수정유티에프해독(អ្នកអាន_តំលៃ.អាន(អ្នកអាន_តំលៃ.수('H')))
            elif 종류 == 3:
                តំលៃ = អ្នកអាន_តំលៃ.수('i')
            elif 종류 == 4:
                តំលៃ = អ្នកអាន_តំលៃ.អាន(4)
            elif 종류 in (5, 6):
                តំលៃ = អ្នកអាន_តំលៃ.អាន(8)
            elif 종류 in (7, 8, 16):
                តំលៃ = អ្នកអាន_តំលៃ.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                តំលៃ = (អ្នកអាន_តំលៃ.수('H'), អ្នកអាន_តំលៃ.수('H'))
            elif 종류 == 15:
                តំលៃ = (អ្នកអាន_តំលៃ.수('B'), អ្នកអាន_តំលៃ.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 តំលៃថេរ_តំលៃ 종류: {}'.format(종류))
            자신.តំលៃថេរ_តំលៃ[សន្ទស្សន៏] = (종류, តំលៃ)
            សន្ទស្សន៏ += 2 if 종류 in (5, 6) else 1
        자신.ការចូលប្រើ_ការបញ្ចូល = អ្នកអាន_តំលៃ.수('H')
        자신.ឈ្មោះ = 자신.ថ្នាក់_ឈ្មោះ(អ្នកអាន_តំលៃ.수('H'))
        부모 = អ្នកអាន_តំលៃ.수('H')
        if 자신.ថ្នាក់_ឈ្មោះ(부모) != 'java/lang/Object' or អ្នកអាន_តំលៃ.수('H') != 0:
            raise 컴파일오류(자신.ឈ្មោះ + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.កន្លែង_បញ្ចូល_តំលៃ = 자신.멤버읽기(អ្នកអាន_តំលៃ)
        자신.អនុគមន៍_តំលៃ = 자신.멤버읽기(អ្នកអាន_តំលៃ)
        자신.속성읽기(អ្នកអាន_តំលៃ)

    def 문자(자신, សន្ទស្សន៏):
        if 자신.តំលៃថេរ_តំលៃ[សន្ទស្សន៏][0] != 1:
            raise 컴파일오류('សំនុំអក្សរ_តំលៃ តំលៃថេរ_តំលៃ ទំរង់_តំលៃ កំហុស')
        return 자신.តំលៃថេរ_តំលៃ[សន្ទស្សន៏][1]

    def ថ្នាក់_ឈ្មោះ(자신, សន្ទស្សន៏):
        return 자신.문자(자신.តំលៃថេរ_តំលៃ[សន្ទស្សន៏][1])

    def យោង(자신, សន្ទស្សន៏):
        ម្ចាស់_តំលៃ, ឈ្មោះ_ទំរង់ = 자신.តំលៃថេរ_តំលៃ[សន្ទស្សន៏][1]
        ឈ្មោះ, ទំរង់_តំលៃ = 자신.តំលៃថេរ_តំលៃ[ឈ្មោះ_ទំរង់][1]
        return 자신.ថ្នាក់_ឈ្មោះ(ម្ចាស់_តំលៃ), 자신.문자(ឈ្មោះ), 자신.문자(ទំរង់_តំលៃ)

    def 속성읽기(자신, អ្នកអាន_តំលៃ):
        ការវាស់វែង = {}
        for _ in range(អ្នកអាន_តំលៃ.수('H')):
            ឈ្មោះ = 자신.문자(អ្នកអាន_តំលៃ.수('H'))
            ការវាស់វែង[ឈ្មោះ] = អ្នកអាន_តំលៃ.អាន(អ្នកអាន_តំលៃ.수('I'))
        return ការវាស់វែង

    def 멤버읽기(자신, អ្នកអាន_តំលៃ):
        ការវាស់វែង = []
        for _ in range(អ្នកអាន_តំលៃ.수('H')):
            ការចូលប្រើ_ការបញ្ចូល = អ្នកអាន_តំលៃ.수('H')
            ឈ្មោះ = 자신.문자(អ្នកអាន_តំលៃ.수('H'))
            ទំរង់_តំលៃ = 자신.문자(អ្នកអាន_តំលៃ.수('H'))
            ការវាស់វែង.append((ការចូលប្រើ_ការបញ្ចូល, ឈ្មោះ, ទំរង់_តំលៃ, 자신.속성읽기(អ្នកអាន_តំលៃ)))
        return ការវាស់វែង


def 형식읽기(សំនុំអក្សរ_តំលៃ):
    ការវាស់វែង = []
    កំណត់ទីតាំង = 0
    while កំណត់ទីតាំង < len(សំនុំអក្សរ_តំលៃ):
        for ទំរង់_តំលៃ in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if សំនុំអក្សរ_តំលៃ.startswith(ទំរង់_តំលៃ, កំណត់ទីតាំង):
                ការវាស់វែង.append(ទំរង់_តំលៃ)
                កំណត់ទីតាំង += len(ទំរង់_តំលៃ)
                break
        else:
            raise 컴파일오류('지원하지 않는 ប្រភេទទិន្នន័យ: ' + សំនុំអក្សរ_តំលៃ)
    return ការវាស់វែង


def 함수형식(서술):
    អាគុយម៉ង់, 반환 = 서술[1:].split(')')
    អាគុយម៉ង់ = 형식읽기(អាគុយម៉ង់)
    반환형 = 형식읽기(반환)
    if 'V' in អាគុយម៉ង់ or len(반환형) != 1:
        raise 컴파일오류('អនុគមន៍_តំលៃ 서술 ទំរង់_តំលៃ កំហុស: ' + 서술)
    return អាគុយម៉ង់, 반환


def និមិត្ត_សញ្ញា(종류, *부분):
    ប្រភព = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ប្រភព).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 អនុគមន៍_តំលៃ 서술에 대해서만 허용한다.
def អនុវត្ត_ពាក្យបញ្ជា(អាគុយម៉ង់=None):
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ប្រភព_មែកធាង ចងក្រង_ប្រព័ន្ធ')
    មុខងារ_ញែក_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    មុខងារ_ញែក_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ថ្នាក់_តំលៃ 디렉터리')
    មុខងារ_ញែក_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 ចងក្រង_ប្រព័ន្ធ JDK 또는 openjdk-build의 부트 JDK ផ្លូវ')
    មុខងារ_ញែក_48ee4b1b.add_argument('--bundle-runtime', help='អនុវត្ត_ពាក្យបញ្ជា 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    មុខងារ_ញែក_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK កម្មវិធី_ថត_កម្មវិធី/ប្រភព_មែកធាង 빌드의 C 컴파일러')
    មុខងារ_ញែក_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    មុខងារ_ញែក_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ចងក្រង_ប្រព័ន្ធ 작업 수')
    មុខងារ_ញែក_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ចងក្រង_ប្រព័ន្ធ គោលដៅ (예: aarch64-linux-gnu)')
    មុខងារ_ញែក_48ee4b1b.add_argument('--sysroot', help='교차 ចងក្រង_ប្រព័ន្ធ 대상의 libc/헤더/បណ្ណាល័យ 루트')
    មុខងារ_ញែក_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ទំរង់_តំលៃ')
    មុខងារ_ញែក_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=ថ្នាក់_តំលៃ.អនុគមន៍_តំលៃ (자체 스택 ABI)')
    មុខងារ_ញែក_48ee4b1b.add_argument('--entry', help='예: 계산.រត់ (openjdk-build 이외 대상에서 필수)')
    មុខងារ_ញែក_48ee4b1b.add_argument('-o', '--output', required=True, help='អនុវត្ត_ពាក្យបញ្ជា ELF/.o លទ្ធផល; openjdk-build는 전용 ចងក្រង_ប្រព័ន្ធ 디렉터리')
    មុខងារ_ញែក_48ee4b1b.add_argument('sources', nargs='+')
    ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args(អាគុយម៉ង់)
    if ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.target == 'openjdk-build':
        if len(ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.sources) != 1 or not ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.java_home or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.entry or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.export or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.classpath or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ប្រភព_មែកធាង 디렉터리 하나와 --java-home 부트 JDK, -o ចងក្រង_ប្រព័ន្ធ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.sources[0], ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.output, ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.java_home, ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.jobs, ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.openjdk_target,
                  ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.sysroot, None if ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.cc == 'cc' else ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.cc, ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.cxx, ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.configure_arg)
        except BuildError as កំហុស:
            raise 컴파일오류(str(កំហុស))
        return
    if not ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.entry:
        មុខងារ_ញែក_48ee4b1b.error('--entry is required for this target')
    if ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.cxx or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.openjdk_target or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.sysroot or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.configure_arg or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build គោលដៅ 전용')
    if ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import បង្កើត_ការបញ្ចូល
        បង្កើត_ការបញ្ចូល(ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់)
        return
    if ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.classpath or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.java_home or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.bundle_runtime or ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk គោលដៅ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.target, '--entry', ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.entry, '-o', ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.output]
    for កំណត់_តំលៃ in ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.export: 자바명령.extend(['--export', កំណត់_តំលៃ])
    subprocess.run(자바명령+ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.sources, check=True)
    return


if __name__ == '__main__':
    try:
        អនុវត្ត_ពាក្យបញ្ជា()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as កំហុស:
        print('ចងក្រង_ប្រភព កំហុស: ' + str(កំហុស), file=sys.stderr)
        sys.exit(1)
