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
    def __init__(자신, sonraí):
        자신.sonraí = sonraí
        자신.suíomh = 0

    def Léigh(자신, fad_VALUE):
        if fad_VALUE < 0 or 자신.suíomh + fad_VALUE > len(자신.sonraí):
            raise 컴파일오류('잘린 aicme_VALUE 또는 Ordú sonraí')
        tomhas = 자신.sonraí[자신.suíomh:자신.suíomh + fad_VALUE]
        자신.suíomh += fad_VALUE
        return tomhas

    def 수(자신, formáid_VALUE):
        return struct.unpack('>' + formáid_VALUE, 자신.Léigh(struct.calcsize('>' + formáid_VALUE)))[0]


def 수정유티에프해독(sonraí):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    teaghrán_VALUE = sonraí.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return teaghrán_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class aicme_VALUE:
    def __init__(자신, CONAIR):
        자신.CONAIR = CONAIR
        Léitheoir_VALUE = 자료읽기(CONAIR.read_bytes())
        if Léitheoir_VALUE.수('I') != 0xcafebabe:
            raise 컴파일오류('Java aicme_VALUE 표식이 아님')
        Léitheoir_VALUE.Léigh(4)
        mír_COUNT = Léitheoir_VALUE.수('H')
        자신.tairiseach_VALUE = [None] * mír_COUNT
        INDEX = 1
        while INDEX < mír_COUNT:
            종류 = Léitheoir_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Léitheoir_VALUE.Léigh(Léitheoir_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Léitheoir_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Léitheoir_VALUE.Léigh(4)
            elif 종류 in (5, 6):
                VALUE = Léitheoir_VALUE.Léigh(8)
            elif 종류 in (7, 8, 16):
                VALUE = Léitheoir_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Léitheoir_VALUE.수('H'), Léitheoir_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Léitheoir_VALUE.수('B'), Léitheoir_VALUE.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 tairiseach_VALUE 종류: {}'.format(종류))
            자신.tairiseach_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.rochtain_iontráil = Léitheoir_VALUE.수('H')
        자신.Ainm = 자신.aicme_ainm(Léitheoir_VALUE.수('H'))
        부모 = Léitheoir_VALUE.수('H')
        if 자신.aicme_ainm(부모) != 'java/lang/Object' or Léitheoir_VALUE.수('H') != 0:
            raise 컴파일오류(자신.Ainm + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.réimse_VALUE = 자신.멤버읽기(Léitheoir_VALUE)
        자신.feidhm_VALUE = 자신.멤버읽기(Léitheoir_VALUE)
        자신.속성읽기(Léitheoir_VALUE)

    def 문자(자신, INDEX):
        if 자신.tairiseach_VALUE[INDEX][0] != 1:
            raise 컴파일오류('teaghrán_VALUE tairiseach_VALUE formáid_VALUE ERREÁID')
        return 자신.tairiseach_VALUE[INDEX][1]

    def aicme_ainm(자신, INDEX):
        return 자신.문자(자신.tairiseach_VALUE[INDEX][1])

    def Leabhair_thagartha(자신, INDEX):
        úinéir_VALUE, ainm_formáid = 자신.tairiseach_VALUE[INDEX][1]
        Ainm, formáid_VALUE = 자신.tairiseach_VALUE[ainm_formáid][1]
        return 자신.aicme_ainm(úinéir_VALUE), 자신.문자(Ainm), 자신.문자(formáid_VALUE)

    def 속성읽기(자신, Léitheoir_VALUE):
        tomhas = {}
        for _ in range(Léitheoir_VALUE.수('H')):
            Ainm = 자신.문자(Léitheoir_VALUE.수('H'))
            tomhas[Ainm] = Léitheoir_VALUE.Léigh(Léitheoir_VALUE.수('I'))
        return tomhas

    def 멤버읽기(자신, Léitheoir_VALUE):
        tomhas = []
        for _ in range(Léitheoir_VALUE.수('H')):
            rochtain_iontráil = Léitheoir_VALUE.수('H')
            Ainm = 자신.문자(Léitheoir_VALUE.수('H'))
            formáid_VALUE = 자신.문자(Léitheoir_VALUE.수('H'))
            tomhas.append((rochtain_iontráil, Ainm, formáid_VALUE, 자신.속성읽기(Léitheoir_VALUE)))
        return tomhas


def 형식읽기(teaghrán_VALUE):
    tomhas = []
    suíomh = 0
    while suíomh < len(teaghrán_VALUE):
        for formáid_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if teaghrán_VALUE.startswith(formáid_VALUE, suíomh):
                tomhas.append(formáid_VALUE)
                suíomh += len(formáid_VALUE)
                break
        else:
            raise 컴파일오류('지원하지 않는 cineál_sonraí: ' + teaghrán_VALUE)
    return tomhas


def 함수형식(서술):
    Argóintí, return_tomhas = 서술[1:].split(')')
    Argóintí = 형식읽기(Argóintí)
    return_TYPE = 형식읽기(return_tomhas)
    if 'V' in Argóintí or len(return_TYPE) != 1:
        raise 컴파일오류('feidhm_VALUE 서술 formáid_VALUE ERREÁID: ' + 서술)
    return Argóintí, return_tomhas


def siombail(종류, *부분):
    FOINSE = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(FOINSE).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 feidhm_VALUE 서술에 대해서만 허용한다.
def Rith_ordú(Argóintí=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK foinse_crann tóg_córas')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/aicme_VALUE 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 tóg_córas JDK 또는 openjdk-build의 부트 JDK CONAIR')
    해석기.add_argument('--bundle-runtime', help='Rith_ordú 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK clár_tarraiceán_feidhmchlár/foinse_crann 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 tóg_córas 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 tóg_córas sprioc (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 tóg_córas 대상의 libc/헤더/leabharlann 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formáid_VALUE')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=aicme_VALUE.feidhm_VALUE (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Rith_2 (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='Rith_ordú ELF/.o Aschur; openjdk-build는 전용 tóg_córas 디렉터리')
    해석기.add_argument('sources', nargs='+')
    paraiméadar_argóint = 해석기.parse_args(Argóintí)
    if paraiméadar_argóint.target == 'openjdk-build':
        if len(paraiméadar_argóint.sources) != 1 or not paraiméadar_argóint.java_home or paraiméadar_argóint.entry or paraiméadar_argóint.export or paraiméadar_argóint.classpath or paraiméadar_argóint.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK foinse_crann 디렉터리 하나와 --java-home 부트 JDK, -o tóg_córas 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(paraiméadar_argóint.sources[0], paraiméadar_argóint.output, paraiméadar_argóint.java_home, paraiméadar_argóint.jobs, paraiméadar_argóint.openjdk_target,
                  paraiméadar_argóint.sysroot, None if paraiméadar_argóint.cc == 'cc' else paraiméadar_argóint.cc, paraiméadar_argóint.cxx, paraiméadar_argóint.configure_arg)
        except BuildError as ERREÁID:
            raise 컴파일오류(str(ERREÁID))
        return
    if not paraiméadar_argóint.entry:
        해석기.error('--entry is required for this target')
    if paraiméadar_argóint.cxx or paraiméadar_argóint.openjdk_target or paraiméadar_argóint.sysroot or paraiméadar_argóint.configure_arg or paraiméadar_argóint.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build sprioc 전용')
    if paraiméadar_argóint.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import Create_iontráil
        Create_iontráil(paraiméadar_argóint)
        return
    if paraiméadar_argóint.classpath or paraiméadar_argóint.java_home or paraiméadar_argóint.bundle_runtime or paraiméadar_argóint.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk sprioc 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', paraiméadar_argóint.target, '--entry', paraiméadar_argóint.entry, '-o', paraiméadar_argóint.output]
    for 지정 in paraiméadar_argóint.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+paraiméadar_argóint.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Rith_ordú()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ERREÁID:
        print('tóg_foinse ERREÁID: ' + str(ERREÁID), file=sys.stderr)
        sys.exit(1)
