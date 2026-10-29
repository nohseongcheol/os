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
    def __init__(자신, தரவு):
        자신.தரவு = தரவு
        자신.இடம் = 0

    def படி(자신, நீளம்_மதிப்பு):
        if நீளம்_மதிப்பு < 0 or 자신.இடம் + நீளம்_மதிப்பு > len(자신.தரவு):
            raise 컴파일오류('잘린 பிரிவு_மதிப்பு_55654bf1 또는 கட்டளை தரவு')
        அளவிடக்கூடியது = 자신.தரவு[자신.இடம்:자신.இடம் + நீளம்_மதிப்பு]
        자신.இடம் += நீளம்_மதிப்பு
        return அளவிடக்கூடியது

    def 수(자신, வடிவமை_மதிப்பு):
        return struct.unpack('>' + வடிவமை_மதிப்பு, 자신.படி(struct.calcsize('>' + வடிவமை_மதிப்பு)))[0]


def 수정유티에프해독(தரவு):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    சரம்_மதிப்பு = தரவு.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return சரம்_மதிப்பு.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class பிரிவு_மதிப்பு_55654bf1:
    def __init__(자신, பாதை_2):
        자신.பாதை_2 = பாதை_2
        படிப்பவர்_மதிப்பு = 자료읽기(பாதை_2.read_bytes())
        if படிப்பவர்_மதிப்பு.수('I') != 0xcafebabe:
            raise 컴파일오류('Java பிரிவு_மதிப்பு_55654bf1 표식이 아님')
        படிப்பவர்_மதிப்பு.படி(4)
        개수 = படிப்பவர்_மதிப்பு.수('H')
        자신.மாறிலி_மதிப்பு = [None] * 개수
        அடைவு = 1
        while அடைவு < 개수:
            종류 = படிப்பவர்_மதிப்பு.수('B')
            if 종류 == 1:
                மதிப்பு = 수정유티에프해독(படிப்பவர்_மதிப்பு.படி(படிப்பவர்_மதிப்பு.수('H')))
            elif 종류 == 3:
                மதிப்பு = படிப்பவர்_மதிப்பு.수('i')
            elif 종류 == 4:
                மதிப்பு = படிப்பவர்_மதிப்பு.படி(4)
            elif 종류 in (5, 6):
                மதிப்பு = படிப்பவர்_மதிப்பு.படி(8)
            elif 종류 in (7, 8, 16):
                மதிப்பு = படிப்பவர்_மதிப்பு.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                மதிப்பு = (படிப்பவர்_மதிப்பு.수('H'), படிப்பவர்_மதிப்பு.수('H'))
            elif 종류 == 15:
                மதிப்பு = (படிப்பவர்_மதிப்பு.수('B'), படிப்பவர்_மதிப்பு.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 மாறிலி_மதிப்பு 종류: {}'.format(종류))
            자신.மாறிலி_மதிப்பு[அடைவு] = (종류, மதிப்பு)
            அடைவு += 2 if 종류 in (5, 6) else 1
        자신.அணுகு_உள்ளீடு = படிப்பவர்_மதிப்பு.수('H')
        자신.பெயர் = 자신.பிரிவு_பெயர்(படிப்பவர்_மதிப்பு.수('H'))
        부모 = படிப்பவர்_மதிப்பு.수('H')
        if 자신.பிரிவு_பெயர்(부모) != 'java/lang/Object' or படிப்பவர்_மதிப்பு.수('H') != 0:
            raise 컴파일오류(자신.பெயர் + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.புலம்_மதிப்பு = 자신.멤버읽기(படிப்பவர்_மதிப்பு)
        자신.செயல்பாடு_மதிப்பு = 자신.멤버읽기(படிப்பவர்_மதிப்பு)
        자신.속성읽기(படிப்பவர்_மதிப்பு)

    def 문자(자신, அடைவு):
        if 자신.மாறிலி_மதிப்பு[அடைவு][0] != 1:
            raise 컴파일오류('சரம்_மதிப்பு மாறிலி_மதிப்பு வடிவமை_மதிப்பு பிழை')
        return 자신.மாறிலி_மதிப்பு[அடைவு][1]

    def பிரிவு_பெயர்(자신, அடைவு):
        return 자신.문자(자신.மாறிலி_மதிப்பு[அடைவு][1])

    def மேற்கோள்(자신, அடைவு):
        உரிமையாளர்_மதிப்பு, பெயர்_வடிவமை = 자신.மாறிலி_மதிப்பு[அடைவு][1]
        பெயர், வடிவமை_மதிப்பு = 자신.மாறிலி_மதிப்பு[பெயர்_வடிவமை][1]
        return 자신.பிரிவு_பெயர்(உரிமையாளர்_மதிப்பு), 자신.문자(பெயர்), 자신.문자(வடிவமை_மதிப்பு)

    def 속성읽기(자신, படிப்பவர்_மதிப்பு):
        அளவிடக்கூடியது = {}
        for _ in range(படிப்பவர்_மதிப்பு.수('H')):
            பெயர் = 자신.문자(படிப்பவர்_மதிப்பு.수('H'))
            அளவிடக்கூடியது[பெயர்] = படிப்பவர்_மதிப்பு.படி(படிப்பவர்_மதிப்பு.수('I'))
        return அளவிடக்கூடியது

    def 멤버읽기(자신, படிப்பவர்_மதிப்பு):
        அளவிடக்கூடியது = []
        for _ in range(படிப்பவர்_மதிப்பு.수('H')):
            அணுகு_உள்ளீடு = படிப்பவர்_மதிப்பு.수('H')
            பெயர் = 자신.문자(படிப்பவர்_மதிப்பு.수('H'))
            வடிவமை_மதிப்பு = 자신.문자(படிப்பவர்_மதிப்பு.수('H'))
            அளவிடக்கூடியது.append((அணுகு_உள்ளீடு, பெயர், வடிவமை_மதிப்பு, 자신.속성읽기(படிப்பவர்_மதிப்பு)))
        return அளவிடக்கூடியது


def 형식읽기(சரம்_மதிப்பு):
    அளவிடக்கூடியது = []
    இடம் = 0
    while இடம் < len(சரம்_மதிப்பு):
        for வடிவமை_மதிப்பு in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if சரம்_மதிப்பு.startswith(வடிவமை_மதிப்பு, இடம்):
                அளவிடக்கூடியது.append(வடிவமை_மதிப்பு)
                இடம் += len(வடிவமை_மதிப்பு)
                break
        else:
            raise 컴파일오류('지원하지 않는 தரவு_வகை: ' + சரம்_மதிப்பு)
    return அளவிடக்கூடியது


def 함수형식(서술):
    செயலுருபுகள், 반환 = 서술[1:].split(')')
    செயலுருபுகள் = 형식읽기(செயலுருபுகள்)
    반환형 = 형식읽기(반환)
    if 'V' in செயலுருபுகள் or len(반환형) != 1:
        raise 컴파일오류('செயல்பாடு_மதிப்பு 서술 வடிவமை_மதிப்பு பிழை: ' + 서술)
    return செயலுருபுகள், 반환


def சின்னம்(종류, *부분):
    மூலக்_கோப்பு = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(மூலக்_கோப்பு).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 செயல்பாடு_மதிப்பு 서술에 대해서만 허용한다.
def இயக்கு_கட்டளை(செயலுருபுகள்=None):
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK மூலம்_மரம் தொகு_முறைமை')
    பார்சர்_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    பார்சர்_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/பிரிவு_மதிப்பு_55654bf1 디렉터리')
    பார்சர்_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 தொகு_முறைமை JDK 또는 openjdk-build의 부트 JDK பாதை_2')
    பார்சர்_48ee4b1b.add_argument('--bundle-runtime', help='இயக்கு_கட்டளை 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    பார்சர்_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK நிரல்_துவக்குநர்/மூலம்_மரம் 빌드의 C 컴파일러')
    பார்சர்_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    பார்சர்_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 தொகு_முறைமை 작업 수')
    பார்சர்_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 தொகு_முறைமை இலக்கு (예: aarch64-linux-gnu)')
    பார்சர்_48ee4b1b.add_argument('--sysroot', help='교차 தொகு_முறைமை 대상의 libc/헤더/நூலகம் 루트')
    பார்சர்_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 வடிவமை_மதிப்பு')
    பார்சர்_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=பிரிவு_மதிப்பு_55654bf1.செயல்பாடு_மதிப்பு (자체 스택 ABI)')
    பார்சர்_48ee4b1b.add_argument('--entry', help='예: 계산.செயல்படுத்துக (openjdk-build 이외 대상에서 필수)')
    பார்சர்_48ee4b1b.add_argument('-o', '--output', required=True, help='இயக்கு_கட்டளை ELF/.o வெளியீட்டு_இடம்; openjdk-build는 전용 தொகு_முறைமை 디렉터리')
    பார்சர்_48ee4b1b.add_argument('sources', nargs='+')
    அளவுரு_மதிப்புரு = பார்சர்_48ee4b1b.parse_args(செயலுருபுகள்)
    if அளவுரு_மதிப்புரு.target == 'openjdk-build':
        if len(அளவுரு_மதிப்புரு.sources) != 1 or not அளவுரு_மதிப்புரு.java_home or அளவுரு_மதிப்புரு.entry or அளவுரு_மதிப்புரு.export or அளவுரு_மதிப்புரு.classpath or அளவுரு_மதிப்புரு.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK மூலம்_மரம் 디렉터리 하나와 --java-home 부트 JDK, -o தொகு_முறைமை 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(அளவுரு_மதிப்புரு.sources[0], அளவுரு_மதிப்புரு.output, அளவுரு_மதிப்புரு.java_home, அளவுரு_மதிப்புரு.jobs, அளவுரு_மதிப்புரு.openjdk_target,
                  அளவுரு_மதிப்புரு.sysroot, None if அளவுரு_மதிப்புரு.cc == 'cc' else அளவுரு_மதிப்புரு.cc, அளவுரு_மதிப்புரு.cxx, அளவுரு_மதிப்புரு.configure_arg)
        except BuildError as பிழை:
            raise 컴파일오류(str(பிழை))
        return
    if not அளவுரு_மதிப்புரு.entry:
        பார்சர்_48ee4b1b.error('--entry is required for this target')
    if அளவுரு_மதிப்புரு.cxx or அளவுரு_மதிப்புரு.openjdk_target or அளவுரு_மதிப்புரு.sysroot or அளவுரு_மதிப்புரு.configure_arg or அளவுரு_மதிப்புரு.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build இலக்கு 전용')
    if அளவுரு_மதிப்புரு.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from செயல்படுத்தக்கூடிய_கோப்பு import உருவாக்கு_உள்ளீடு
        உருவாக்கு_உள்ளீடு(அளவுரு_மதிப்புரு)
        return
    if அளவுரு_மதிப்புரு.classpath or அளவுரு_மதிப்புரு.java_home or அளவுரு_மதிப்புரு.bundle_runtime or அளவுரு_மதிப்புரு.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk இலக்கு 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', அளவுரு_மதிப்புரு.target, '--entry', அளவுரு_மதிப்புரு.entry, '-o', அளவுரு_மதிப்புரு.output]
    for ஒதுக்கு_மதிப்பு in அளவுரு_மதிப்புரு.export: 자바명령.extend(['--export', ஒதுக்கு_மதிப்பு])
    subprocess.run(자바명령+அளவுரு_மதிப்புரு.sources, check=True)
    return


if __name__ == '__main__':
    try:
        இயக்கு_கட்டளை()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as பிழை:
        print('தொகு_மூலம் பிழை: ' + str(பிழை), file=sys.stderr)
        sys.exit(1)
