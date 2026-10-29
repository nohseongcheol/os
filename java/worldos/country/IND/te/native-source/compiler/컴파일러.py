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
    def __init__(자신, డేటా):
        자신.డేటా = డేటా
        자신.స్థానము = 0

    def చదువు(자신, పొడవు_మూల్యం):
        if పొడవు_మూల్యం < 0 or 자신.స్థానము + పొడవు_మూల్యం > len(자신.డేటా):
            raise 컴파일오류('잘린 తరగతి_మూల్యం 또는 ఆదేశము డేటా')
        ప్రమాణం = 자신.డేటా[자신.స్థానము:자신.స్థానము + పొడవు_మూల్యం]
        자신.స్థానము += పొడవు_మూల్యం
        return ప్రమాణం

    def 수(자신, ఆకృతి_మూల్యం):
        return struct.unpack('>' + ఆకృతి_మూల్యం, 자신.చదువు(struct.calcsize('>' + ఆకృతి_మూల్యం)))[0]


def 수정유티에프해독(డేటా):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    అక్షరసరం_మూల్యం = డేటా.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return అక్షరసరం_మూల్యం.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class తరగతి_మూల్యం:
    def __init__(자신, పాత్):
        자신.పాత్ = పాత్
        రీడర్_మూల్యం = 자료읽기(పాత్.read_bytes())
        if రీడర్_మూల్యం.수('I') != 0xcafebabe:
            raise 컴파일오류('Java తరగతి_మూల్యం 표식이 아님')
        రీడర్_మూల్యం.చదువు(4)
        개수 = రీడర్_మూల్యం.수('H')
        자신.స్థిర_మూల్యం = [None] * 개수
        సూచీ = 1
        while సూచీ < 개수:
            종류 = రీడర్_మూల్యం.수('B')
            if 종류 == 1:
                మూల్యం = 수정유티에프해독(రీడర్_మూల్యం.చదువు(రీడర్_మూల్యం.수('H')))
            elif 종류 == 3:
                మూల్యం = రీడర్_మూల్యం.수('i')
            elif 종류 == 4:
                మూల్యం = రీడర్_మూల్యం.చదువు(4)
            elif 종류 in (5, 6):
                మూల్యం = రీడర్_మూల్యం.చదువు(8)
            elif 종류 in (7, 8, 16):
                మూల్యం = రీడర్_మూల్యం.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                మూల్యం = (రీడర్_మూల్యం.수('H'), రీడర్_మూల్యం.수('H'))
            elif 종류 == 15:
                మూల్యం = (రీడర్_మూల్యం.수('B'), రీడర్_మూల్యం.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 స్థిర_మూల్యం 종류: {}'.format(종류))
            자신.స్థిర_మూల్యం[సూచీ] = (종류, మూల్యం)
            సూచీ += 2 if 종류 in (5, 6) else 1
        자신.ప్రాప్తి_ప్రవేశం = రీడర్_మూల్యం.수('H')
        자신.పేరు = 자신.తరగతి_పేరు(రీడర్_మూల్యం.수('H'))
        부모 = రీడర్_మూల్యం.수('H')
        if 자신.తరగతి_పేరు(부모) != 'java/lang/Object' or రీడర్_మూల్యం.수('H') != 0:
            raise 컴파일오류(자신.పేరు + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ఫీల్డ్_మూల్యం = 자신.멤버읽기(రీడర్_మూల్యం)
        자신.కార్యం_మూల్యం = 자신.멤버읽기(రీడర్_మూల్యం)
        자신.속성읽기(రీడర్_మూల్యం)

    def 문자(자신, సూచీ):
        if 자신.స్థిర_మూల్యం[సూచీ][0] != 1:
            raise 컴파일오류('అక్షరసరం_మూల్యం స్థిర_మూల్యం ఆకృతి_మూల్యం దోషం')
        return 자신.స్థిర_మూల్యం[సూచీ][1]

    def తరగతి_పేరు(자신, సూచీ):
        return 자신.문자(자신.స్థిర_మూల్యం[సూచీ][1])

    def సూచన(자신, సూచీ):
        యజమాని_మూల్యం, పేరు_ఆకృతి = 자신.స్థిర_మూల్యం[సూచీ][1]
        పేరు, ఆకృతి_మూల్యం = 자신.స్థిర_మూల్యం[పేరు_ఆకృతి][1]
        return 자신.తరగతి_పేరు(యజమాని_మూల్యం), 자신.문자(పేరు), 자신.문자(ఆకృతి_మూల్యం)

    def 속성읽기(자신, రీడర్_మూల్యం):
        ప్రమాణం = {}
        for _ in range(రీడర్_మూల్యం.수('H')):
            పేరు = 자신.문자(రీడర్_మూల్యం.수('H'))
            ప్రమాణం[పేరు] = రీడర్_మూల్యం.చదువు(రీడర్_మూల్యం.수('I'))
        return ప్రమాణం

    def 멤버읽기(자신, రీడర్_మూల్యం):
        ప్రమాణం = []
        for _ in range(రీడర్_మూల్యం.수('H')):
            ప్రాప్తి_ప్రవేశం = రీడర్_మూల్యం.수('H')
            పేరు = 자신.문자(రీడర్_మూల్యం.수('H'))
            ఆకృతి_మూల్యం = 자신.문자(రీడర్_మూల్యం.수('H'))
            ప్రమాణం.append((ప్రాప్తి_ప్రవేశం, పేరు, ఆకృతి_మూల్యం, 자신.속성읽기(రీడర్_మూల్యం)))
        return ప్రమాణం


def 형식읽기(అక్షరసరం_మూల్యం):
    ప్రమాణం = []
    స్థానము = 0
    while స్థానము < len(అక్షరసరం_మూల్యం):
        for ఆకృతి_మూల్యం in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if అక్షరసరం_మూల్యం.startswith(ఆకృతి_మూల్యం, స్థానము):
                ప్రమాణం.append(ఆకృతి_మూల్యం)
                స్థానము += len(ఆకృతి_మూల్యం)
                break
        else:
            raise 컴파일오류('지원하지 않는 డేటా_రకం: ' + అక్షరసరం_మూల్యం)
    return ప్రమాణం


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('కార్యం_మూల్యం 서술 ఆకృతి_మూల్యం దోషం: ' + 서술)
    return 인수, 반환


def చిహ్నం(종류, *부분):
    వనరు = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(వనరు).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 కార్యం_మూల్యం 서술에 대해서만 허용한다.
def అమలు_చేయి_ఆదేశం(인수=None):
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK మూలం_వృక్షాకృతి బిల్డ్_సిస్టం')
    పార్సర్_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    పార్సర్_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/తరగతి_మూల్యం 디렉터리')
    పార్సర్_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 బిల్డ్_సిస్టం JDK 또는 openjdk-build의 부트 JDK పాత్')
    పార్సర్_48ee4b1b.add_argument('--bundle-runtime', help='అమలు_చేయి_ఆదేశం 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    పార్సర్_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK అనువర్తనం_లాంచర్/మూలం_వృక్షాకృతి 빌드의 C 컴파일러')
    పార్సర్_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    పార్సర్_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 బిల్డ్_సిస్టం 작업 수')
    పార్సర్_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 బిల్డ్_సిస్టం లక్ష్యం (예: aarch64-linux-gnu)')
    పార్సర్_48ee4b1b.add_argument('--sysroot', help='교차 బిల్డ్_సిస్టం 대상의 libc/헤더/లైబ్రరీ 루트')
    పార్సర్_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ఆకృతి_మూల్యం')
    పార్సర్_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=తరగతి_మూల్యం.కార్యం_మూల్యం (자체 스택 ABI)')
    పార్సర్_48ee4b1b.add_argument('--entry', help='예: 계산.నడుపుము (openjdk-build 이외 대상에서 필수)')
    పార్సర్_48ee4b1b.add_argument('-o', '--output', required=True, help='అమలు_చేయి_ఆదేశం ELF/.o అవుట్పుట్; openjdk-build는 전용 బిల్డ్_సిస్టం 디렉터리')
    పార్సర్_48ee4b1b.add_argument('sources', nargs='+')
    పారామీటర్_కారకం = పార్సర్_48ee4b1b.parse_args(인수)
    if పారామీటర్_కారకం.target == 'openjdk-build':
        if len(పారామీటర్_కారకం.sources) != 1 or not పారామీటర్_కారకం.java_home or పారామీటర్_కారకం.entry or పారామీటర్_కారకం.export or పారామీటర్_కారకం.classpath or పారామీటర్_కారకం.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK మూలం_వృక్షాకృతి 디렉터리 하나와 --java-home 부트 JDK, -o బిల్డ్_సిస్టం 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(పారామీటర్_కారకం.sources[0], పారామీటర్_కారకం.output, పారామీటర్_కారకం.java_home, పారామీటర్_కారకం.jobs, పారామీటర్_కారకం.openjdk_target,
                  పారామీటర్_కారకం.sysroot, None if పారామీటర్_కారకం.cc == 'cc' else పారామీటర్_కారకం.cc, పారామీటర్_కారకం.cxx, పారామీటర్_కారకం.configure_arg)
        except BuildError as దోషం:
            raise 컴파일오류(str(దోషం))
        return
    if not పారామీటర్_కారకం.entry:
        పార్సర్_48ee4b1b.error('--entry is required for this target')
    if పారామీటర్_కారకం.cxx or పారామీటర్_కారకం.openjdk_target or పారామీటర్_కారకం.sysroot or పారామీటర్_కారకం.configure_arg or పారామీటర్_కారకం.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build లక్ష్యం 전용')
    if పారామీటర్_కారకం.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import క్రియేట్_ప్రవేశం
        క్రియేట్_ప్రవేశం(పారామీటర్_కారకం)
        return
    if పారామీటర్_కారకం.classpath or పారామీటర్_కారకం.java_home or పారామీటర్_కారకం.bundle_runtime or పారామీటర్_కారకం.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk లక్ష్యం 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', పారామీటర్_కారకం.target, '--entry', పారామీటర్_కారకం.entry, '-o', పారామీటర్_కారకం.output]
    for కేటాయించు_మూల్యం in పారామీటర్_కారకం.export: 자바명령.extend(['--export', కేటాయించు_మూల్యం])
    subprocess.run(자바명령+పారామీటర్_కారకం.sources, check=True)
    return


if __name__ == '__main__':
    try:
        అమలు_చేయి_ఆదేశం()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as దోషం:
        print('నిర్మించు_మూలం దోషం: ' + str(దోషం), file=sys.stderr)
        sys.exit(1)
