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
    def __init__(자신, දත්ත):
        자신.දත්ත = දත්ත
        자신.පිහිටීම = 0

    def කියවීම(자신, දිග_අගය):
        if දිග_අගය < 0 or 자신.පිහිටීම + දිග_අගය > len(자신.දත්ත):
            raise 컴파일오류('잘린 පන්තිය_අගය 또는 විධානය දත්ත')
        결과 = 자신.දත්ත[자신.පිහිටීම:자신.පිහිටීම + දිග_අගය]
        자신.පිහිටීම += දිග_අගය
        return 결과

    def 수(자신, හැඩතලය_අගය):
        return struct.unpack('>' + හැඩතලය_අගය, 자신.කියවීම(struct.calcsize('>' + හැඩතලය_අගය)))[0]


def 수정유티에프해독(දත්ත):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    අනුලකුණු_වැල_අගය = දත්ත.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return අනුලකුණු_වැල_අගය.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class පන්තිය_අගය:
    def __init__(자신, මාර්_ගය):
        자신.මාර්_ගය = මාර්_ගය
        පාඨක_අගය = 자료읽기(මාර්_ගය.read_bytes())
        if පාඨක_අගය.수('I') != 0xcafebabe:
            raise 컴파일오류('Java පන්තිය_අගය 표식이 아님')
        පාඨක_අගය.කියවීම(4)
        개수 = පාඨක_අගය.수('H')
        자신.නියතය_අගය = [None] * 개수
        සූචිය = 1
        while සූචිය < 개수:
            종류 = පාඨක_අගය.수('B')
            if 종류 == 1:
                අගය = 수정유티에프해독(පාඨක_අගය.කියවීම(පාඨක_අගය.수('H')))
            elif 종류 == 3:
                අගය = පාඨක_අගය.수('i')
            elif 종류 == 4:
                අගය = පාඨක_අගය.කියවීම(4)
            elif 종류 in (5, 6):
                අගය = පාඨක_අගය.කියවීම(8)
            elif 종류 in (7, 8, 16):
                අගය = පාඨක_අගය.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                අගය = (පාඨක_අගය.수('H'), පාඨක_අගය.수('H'))
            elif 종류 == 15:
                අගය = (පාඨක_අගය.수('B'), පාඨක_අගය.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 නියතය_අගය 종류: {}'.format(종류))
            자신.නියතය_අගය[සූචිය] = (종류, අගය)
            සූචිය += 2 if 종류 in (5, 6) else 1
        자신.ප්_රවේශය_පිවිසුම = පාඨක_අගය.수('H')
        자신.නම = 자신.පන්තිය_නම(පාඨක_අගය.수('H'))
        부모 = පාඨක_අගය.수('H')
        if 자신.පන්තිය_නම(부모) != 'java/lang/Object' or පාඨක_අගය.수('H') != 0:
            raise 컴파일오류(자신.නම + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ක්_ෂේත්_රය_අගය = 자신.멤버읽기(පාඨක_අගය)
        자신.ශ්_රිතය_අගය = 자신.멤버읽기(පාඨක_අගය)
        자신.속성읽기(පාඨක_අගය)

    def 문자(자신, සූචිය):
        if 자신.නියතය_අගය[සූචිය][0] != 1:
            raise 컴파일오류('අනුලකුණු_වැල_අගය නියතය_අගය හැඩතලය_අගය දෝෂය')
        return 자신.නියතය_අගය[සූචිය][1]

    def පන්තිය_නම(자신, සූචිය):
        return 자신.문자(자신.නියතය_අගය[සූචිය][1])

    def පරිශීලනය(자신, සූචිය):
        හිමිකරු_අගය, නම_හැඩතලය = 자신.නියතය_අගය[සූචිය][1]
        නම, හැඩතලය_අගය = 자신.නියතය_අගය[නම_හැඩතලය][1]
        return 자신.පන්තිය_නම(හිමිකරු_අගය), 자신.문자(නම), 자신.문자(හැඩතලය_අගය)

    def 속성읽기(자신, පාඨක_අගය):
        결과 = {}
        for _ in range(පාඨක_අගය.수('H')):
            නම = 자신.문자(පාඨක_අගය.수('H'))
            결과[නම] = පාඨක_අගය.කියවීම(පාඨක_අගය.수('I'))
        return 결과

    def 멤버읽기(자신, පාඨක_අගය):
        결과 = []
        for _ in range(පාඨක_අගය.수('H')):
            ප්_රවේශය_පිවිසුම = පාඨක_අගය.수('H')
            නම = 자신.문자(පාඨක_අගය.수('H'))
            හැඩතලය_අගය = 자신.문자(පාඨක_අගය.수('H'))
            결과.append((ප්_රවේශය_පිවිසුම, නම, හැඩතලය_අගය, 자신.속성읽기(පාඨක_අගය)))
        return 결과


def 형식읽기(අනුලකුණු_වැල_අගය):
    결과 = []
    පිහිටීම = 0
    while පිහිටීම < len(අනුලකුණු_වැල_අගය):
        for හැඩතලය_අගය in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if අනුලකුණු_වැල_අගය.startswith(හැඩතලය_අගය, පිහිටීම):
                결과.append(හැඩතලය_අගය)
                පිහිටීම += len(හැඩතලය_අගය)
                break
        else:
            raise 컴파일오류('지원하지 않는 දත්ත_වර්ගය: ' + අනුලකුණු_වැල_අගය)
    return 결과


def 함수형식(서술):
    විස්තාරක, 반환 = 서술[1:].split(')')
    විස්තාරක = 형식읽기(විස්තාරක)
    반환형 = 형식읽기(반환)
    if 'V' in විස්තාරක or len(반환형) != 1:
        raise 컴파일오류('ශ්_රිතය_අගය 서술 හැඩතලය_අගය දෝෂය: ' + 서술)
    return විස්තාරක, 반환


def සංකේතය(종류, *부분):
    මූලය = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(මූලය).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ශ්_රිතය_අගය 서술에 대해서만 허용한다.
def ක්_රියාත්මක_කරන්න_විධානය(විස්තාරක=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK මූලය_රුක තැනුම_පද්ධතිය')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/පන්තිය_අගය 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 තැනුම_පද්ධතිය JDK 또는 openjdk-build의 부트 JDK මාර්_ගය')
    해석기.add_argument('--bundle-runtime', help='ක්_රියාත්මක_කරන්න_විධානය 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK යෙදු_යෙදුම්_ලාච්චුව/මූලය_රුක 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 තැනුම_පද්ධතිය 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 තැනුම_පද්ධතිය ඉලක්කය (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 තැනුම_පද්ධතිය 대상의 libc/헤더/ලේඛාගාරය 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 හැඩතලය_අගය')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=පන්තිය_අගය.ශ්_රිතය_අගය (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.ක්_රියාත්මක_කරන්න_2 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ක්_රියාත්මක_කරන්න_විධානය ELF/.o 출력; openjdk-build는 전용 තැනුම_පද්ධතිය 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(විස්තාරක)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK මූලය_රුක 디렉터리 하나와 --java-home 부트 JDK, -o තැනුම_පද්ධතිය 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as දෝෂය:
            raise 컴파일오류(str(දෝෂය))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ඉලක්කය 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import සාදන්න_පිවිසුම
        සාදන්න_පිවිසුම(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ඉලක්කය 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ක්_රියාත්මක_කරන්න_විධානය()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as දෝෂය:
        print('සාදන්න_මූලය දෝෂය: ' + str(දෝෂය), file=sys.stderr)
        sys.exit(1)
