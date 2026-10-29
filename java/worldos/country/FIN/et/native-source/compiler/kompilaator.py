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


class kompileerimistõrge(Exception):
    pass


class 자료읽기:
    def __init__(자신, andmed):
        자신.andmed = andmed
        자신.Asukoht = 0

    def Lugemine(자신, 길이):
        if 길이 < 0 or 자신.Asukoht + 길이 > len(자신.andmed):
            raise kompileerimistõrge('잘린 tund_VALUE 또는 Käsk andmed')
        TULEMUS = 자신.andmed[자신.Asukoht:자신.Asukoht + 길이]
        자신.Asukoht += 길이
        return TULEMUS

    def number(자신, vorming_VALUE):
        return struct.unpack('>' + vorming_VALUE, 자신.Lugemine(struct.calcsize('>' + vorming_VALUE)))[0]


def 수정유티에프해독(andmed):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    string_VALUE = andmed.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return string_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class tund_VALUE:
    def __init__(자신, RADA):
        자신.RADA = RADA
        Reader_VALUE = 자료읽기(RADA.read_bytes())
        if Reader_VALUE.number('I') != 0xcafebabe:
            raise kompileerimistõrge('Java tund_VALUE 표식이 아님')
        Reader_VALUE.Lugemine(4)
        kaup_COUNT = Reader_VALUE.number('H')
        자신.konstant_VALUE = [None] * kaup_COUNT
        INDEX = 1
        while INDEX < kaup_COUNT:
            종류 = Reader_VALUE.number('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Reader_VALUE.Lugemine(Reader_VALUE.number('H')))
            elif 종류 == 3:
                VALUE = Reader_VALUE.number('i')
            elif 종류 == 4:
                VALUE = Reader_VALUE.Lugemine(4)
            elif 종류 in (5, 6):
                VALUE = Reader_VALUE.Lugemine(8)
            elif 종류 in (7, 8, 16):
                VALUE = Reader_VALUE.number('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Reader_VALUE.number('H'), Reader_VALUE.number('H'))
            elif 종류 == 15:
                VALUE = (Reader_VALUE.number('B'), Reader_VALUE.number('H'))
            else:
                raise kompileerimistõrge('지원하지 않는 konstant_VALUE 종류: {}'.format(종류))
            자신.konstant_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.pöördus_kirje = Reader_VALUE.number('H')
        자신.Nimi_2 = 자신.klassinimi(Reader_VALUE.number('H'))
        ema_VALUE = Reader_VALUE.number('H')
        if 자신.klassinimi(ema_VALUE) != 'java/lang/Object' or Reader_VALUE.number('H') != 0:
            raise kompileerimistõrge(자신.Nimi_2 + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.väljaväärtus = 자신.멤버읽기(Reader_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(Reader_VALUE)
        자신.속성읽기(Reader_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstant_VALUE[INDEX][0] != 1:
            raise kompileerimistõrge('string_VALUE konstant_VALUE vorming_VALUE VIGA')
        return 자신.konstant_VALUE[INDEX][1]

    def klassinimi(자신, INDEX):
        return 자신.문자(자신.konstant_VALUE[INDEX][1])

    def viide(자신, INDEX):
        omanik_VALUE, nimetus_vorming = 자신.konstant_VALUE[INDEX][1]
        Nimi_2, vorming_VALUE = 자신.konstant_VALUE[nimetus_vorming][1]
        return 자신.klassinimi(omanik_VALUE), 자신.문자(Nimi_2), 자신.문자(vorming_VALUE)

    def 속성읽기(자신, Reader_VALUE):
        TULEMUS = {}
        for _ in range(Reader_VALUE.number('H')):
            Nimi_2 = 자신.문자(Reader_VALUE.number('H'))
            TULEMUS[Nimi_2] = Reader_VALUE.Lugemine(Reader_VALUE.number('I'))
        return TULEMUS

    def 멤버읽기(자신, Reader_VALUE):
        TULEMUS = []
        for _ in range(Reader_VALUE.number('H')):
            pöördus_kirje = Reader_VALUE.number('H')
            Nimi_2 = 자신.문자(Reader_VALUE.number('H'))
            vorming_VALUE = 자신.문자(Reader_VALUE.number('H'))
            TULEMUS.append((pöördus_kirje, Nimi_2, vorming_VALUE, 자신.속성읽기(Reader_VALUE)))
        return TULEMUS


def 형식읽기(string_VALUE):
    TULEMUS = []
    Asukoht = 0
    while Asukoht < len(string_VALUE):
        for vorming_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if string_VALUE.startswith(vorming_VALUE, Asukoht):
                TULEMUS.append(vorming_VALUE)
                Asukoht += len(vorming_VALUE)
                break
        else:
            raise kompileerimistõrge('지원하지 않는 andmetüüp: ' + string_VALUE)
    return TULEMUS


def 함수형식(서술):
    Argumendid, tagasi_saatma_näitaja = 서술[1:].split(')')
    Argumendid = 형식읽기(Argumendid)
    tagasi_saatma_TYPE = 형식읽기(tagasi_saatma_näitaja)
    if 'V' in Argumendid or len(tagasi_saatma_TYPE) != 1:
        raise kompileerimistõrge('FUNCTION_VALUE 서술 vorming_VALUE VIGA: ' + 서술)
    return Argumendid, tagasi_saatma_näitaja


def sümbol(종류, *부분):
    ALLIKAS = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ALLIKAS).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def Täida_käsk(Argumendid=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='oma Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK lähe_puu järk_süsteem')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Lisa_kirje JAR/tund_VALUE 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 järk_süsteem JDK 또는 openjdk-build의 부트 JDK RADA')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='Täida_käsk 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK programm_käiviti/lähe_puu 빌드의 C kompilaator')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompilaator')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 järk_süsteem 작업 number')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 järk_süsteem siht (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 järk_süsteem 대상의 libc/헤더/teek 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 vorming_VALUE')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=tund_VALUE.FUNCTION_VALUE (oma operand_Virn ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.Käivita_2 (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='Täida_käsk ELF/.o Väljund; openjdk-build는 전용 järk_süsteem 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parameeter_argument = parser_48ee4b1b.parse_args(Argumendid)
    if parameeter_argument.target == 'openjdk-build':
        if len(parameeter_argument.sources) != 1 or not parameeter_argument.java_home or parameeter_argument.entry or parameeter_argument.export or parameeter_argument.classpath or parameeter_argument.bundle_runtime:
            raise kompileerimistõrge('openjdk-build: OpenJDK lähe_puu 디렉터리 하나와 --java-home 부트 JDK, -o järk_süsteem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameeter_argument.sources[0], parameeter_argument.output, parameeter_argument.java_home, parameeter_argument.jobs, parameeter_argument.openjdk_target,
                  parameeter_argument.sysroot, None if parameeter_argument.cc == 'cc' else parameeter_argument.cc, parameeter_argument.cxx, parameeter_argument.configure_arg)
        except BuildError as VIGA:
            raise kompileerimistõrge(str(VIGA))
        return
    if not parameeter_argument.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parameeter_argument.cxx or parameeter_argument.openjdk_target or parameeter_argument.sysroot or parameeter_argument.configure_arg or parameeter_argument.jobs != 2:
        raise kompileerimistõrge('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build siht 전용')
    if parameeter_argument.target == 'openjdk':
        sys.modules.setdefault('kompilaator', sys.modules[__name__])
        from 실행파일 import avama_kirje
        avama_kirje(parameeter_argument)
        return
    if parameeter_argument.classpath or parameeter_argument.java_home or parameeter_argument.bundle_runtime or parameeter_argument.cc != 'cc':
        raise kompileerimistõrge('classpath/java-home/bundle-runtime/cc 옵션은 openjdk siht 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameeter_argument.target, '--entry', parameeter_argument.entry, '-o', parameeter_argument.output]
    for Määra_VALUE in parameeter_argument.export: 자바명령.extend(['--export', Määra_VALUE])
    subprocess.run(자바명령+parameeter_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Täida_käsk()
    except (kompileerimistõrge, OSError, ValueError, subprocess.CalledProcessError) as VIGA:
        print('kompileerima_lähe VIGA: ' + str(VIGA), file=sys.stderr)
        sys.exit(1)
