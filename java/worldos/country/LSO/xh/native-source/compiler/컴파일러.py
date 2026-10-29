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
    def __init__(자신, iingcombolo):
        자신.iingcombolo = iingcombolo
        자신.위치 = 0

    def Funda(자신, ubude_ixabiso):
        if ubude_ixabiso < 0 or 자신.위치 + ubude_ixabiso > len(자신.iingcombolo):
            raise 컴파일오류('잘린 iklasi_ixabiso 또는 Umyalelo iingcombolo')
        결과 = 자신.iingcombolo[자신.위치:자신.위치 + ubude_ixabiso]
        자신.위치 += ubude_ixabiso
        return 결과

    def 수(자신, fomatha_ixabiso):
        return struct.unpack('>' + fomatha_ixabiso, 자신.Funda(struct.calcsize('>' + fomatha_ixabiso)))[0]


def 수정유티에프해독(iingcombolo):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    uluhlu_lweekharektha_ixabiso = iingcombolo.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return uluhlu_lweekharektha_ixabiso.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class iklasi_ixabiso:
    def __init__(자신, INDLELA):
        자신.INDLELA = INDLELA
        Umfundi_ixabiso = 자료읽기(INDLELA.read_bytes())
        if Umfundi_ixabiso.수('I') != 0xcafebabe:
            raise 컴파일오류('Java iklasi_ixabiso 표식이 아님')
        Umfundi_ixabiso.Funda(4)
        개수 = Umfundi_ixabiso.수('H')
        자신.engajikiyo_ixabiso = [None] * 개수
        indeksa = 1
        while indeksa < 개수:
            종류 = Umfundi_ixabiso.수('B')
            if 종류 == 1:
                ixabiso = 수정유티에프해독(Umfundi_ixabiso.Funda(Umfundi_ixabiso.수('H')))
            elif 종류 == 3:
                ixabiso = Umfundi_ixabiso.수('i')
            elif 종류 == 4:
                ixabiso = Umfundi_ixabiso.Funda(4)
            elif 종류 in (5, 6):
                ixabiso = Umfundi_ixabiso.Funda(8)
            elif 종류 in (7, 8, 16):
                ixabiso = Umfundi_ixabiso.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ixabiso = (Umfundi_ixabiso.수('H'), Umfundi_ixabiso.수('H'))
            elif 종류 == 15:
                ixabiso = (Umfundi_ixabiso.수('B'), Umfundi_ixabiso.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 engajikiyo_ixabiso 종류: {}'.format(종류))
            자신.engajikiyo_ixabiso[indeksa] = (종류, ixabiso)
            indeksa += 2 if 종류 in (5, 6) else 1
        자신.fikelela_ufako_nkcukacha = Umfundi_ixabiso.수('H')
        자신.Igama = 자신.iklasi_igama(Umfundi_ixabiso.수('H'))
        부모 = Umfundi_ixabiso.수('H')
        if 자신.iklasi_igama(부모) != 'java/lang/Object' or Umfundi_ixabiso.수('H') != 0:
            raise 컴파일오류(자신.Igama + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ifildi_ixabiso = 자신.멤버읽기(Umfundi_ixabiso)
        자신.INKQUBO_ixabiso = 자신.멤버읽기(Umfundi_ixabiso)
        자신.속성읽기(Umfundi_ixabiso)

    def 문자(자신, indeksa):
        if 자신.engajikiyo_ixabiso[indeksa][0] != 1:
            raise 컴파일오류('uluhlu_lweekharektha_ixabiso engajikiyo_ixabiso fomatha_ixabiso Impazamo')
        return 자신.engajikiyo_ixabiso[indeksa][1]

    def iklasi_igama(자신, indeksa):
        return 자신.문자(자신.engajikiyo_ixabiso[indeksa][1])

    def Isalathiso(자신, indeksa):
        umnini_ixabiso, igama_fomatha = 자신.engajikiyo_ixabiso[indeksa][1]
        Igama, fomatha_ixabiso = 자신.engajikiyo_ixabiso[igama_fomatha][1]
        return 자신.iklasi_igama(umnini_ixabiso), 자신.문자(Igama), 자신.문자(fomatha_ixabiso)

    def 속성읽기(자신, Umfundi_ixabiso):
        결과 = {}
        for _ in range(Umfundi_ixabiso.수('H')):
            Igama = 자신.문자(Umfundi_ixabiso.수('H'))
            결과[Igama] = Umfundi_ixabiso.Funda(Umfundi_ixabiso.수('I'))
        return 결과

    def 멤버읽기(자신, Umfundi_ixabiso):
        결과 = []
        for _ in range(Umfundi_ixabiso.수('H')):
            fikelela_ufako_nkcukacha = Umfundi_ixabiso.수('H')
            Igama = 자신.문자(Umfundi_ixabiso.수('H'))
            fomatha_ixabiso = 자신.문자(Umfundi_ixabiso.수('H'))
            결과.append((fikelela_ufako_nkcukacha, Igama, fomatha_ixabiso, 자신.속성읽기(Umfundi_ixabiso)))
        return 결과


def 형식읽기(uluhlu_lweekharektha_ixabiso):
    결과 = []
    위치 = 0
    while 위치 < len(uluhlu_lweekharektha_ixabiso):
        for fomatha_ixabiso in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if uluhlu_lweekharektha_ixabiso.startswith(fomatha_ixabiso, 위치):
                결과.append(fomatha_ixabiso)
                위치 += len(fomatha_ixabiso)
                break
        else:
            raise 컴파일오류('지원하지 않는 ugcino_lweengcombolo: ' + uluhlu_lweekharektha_ixabiso)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('INKQUBO_ixabiso 서술 fomatha_ixabiso Impazamo: ' + 서술)
    return 인수, 반환


def isimboli(종류, *부분):
    UMTHOMBO = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(UMTHOMBO).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 INKQUBO_ixabiso 서술에 대해서만 허용한다.
def ukwenza_umyalelo(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK umthombo_umthi yakha_inkqubo')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/iklasi_ixabiso 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 yakha_inkqubo JDK 또는 openjdk-build의 부트 JDK INDLELA')
    해석기.add_argument('--bundle-runtime', help='ukwenza_umyalelo 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK inkqubo_idrowa_yosetyenziso/umthombo_umthi 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 yakha_inkqubo 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 yakha_inkqubo ithagethi (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 yakha_inkqubo 대상의 libc/헤더/ilayibhrari 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 fomatha_ixabiso')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=iklasi_ixabiso.INKQUBO_ixabiso (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.Phumeza (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='ukwenza_umyalelo ELF/.o 출력; openjdk-build는 전용 yakha_inkqubo 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK umthombo_umthi 디렉터리 하나와 --java-home 부트 JDK, -o yakha_inkqubo 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as Impazamo:
            raise 컴파일오류(str(Impazamo))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ithagethi 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import yila_ufako_nkcukacha
        yila_ufako_nkcukacha(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ithagethi 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for yabela_ixabiso in 인자.export: 자바명령.extend(['--export', yabela_ixabiso])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ukwenza_umyalelo()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as Impazamo:
        print('yakha_umthombo Impazamo: ' + str(Impazamo), file=sys.stderr)
        sys.exit(1)
