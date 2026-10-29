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
    def __init__(자신, datuak):
        자신.datuak = datuak
        자신.Posizioa = 0

    def Irakurri(자신, luzera_balio):
        if luzera_balio < 0 or 자신.Posizioa + luzera_balio > len(자신.datuak):
            raise 컴파일오류('잘린 Gela_balio 또는 Komandoa datuak')
        EMAITZA = 자신.datuak[자신.Posizioa:자신.Posizioa + luzera_balio]
        자신.Posizioa += luzera_balio
        return EMAITZA

    def 수(자신, formatu_balio):
        return struct.unpack('>' + formatu_balio, 자신.Irakurri(struct.calcsize('>' + formatu_balio)))[0]


def 수정유티에프해독(datuak):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    kate_balio = datuak.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return kate_balio.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Gela_balio:
    def __init__(자신, Bide_izena):
        자신.Bide_izena = Bide_izena
        irakurle_balio = 자료읽기(Bide_izena.read_bytes())
        if irakurle_balio.수('I') != 0xcafebabe:
            raise 컴파일오류('Java Gela_balio 표식이 아님')
        irakurle_balio.Irakurri(4)
        elementu_ZENBATU = irakurle_balio.수('H')
        자신.konstante_balio = [None] * elementu_ZENBATU
        INDIZE = 1
        while INDIZE < elementu_ZENBATU:
            종류 = irakurle_balio.수('B')
            if 종류 == 1:
                balio = 수정유티에프해독(irakurle_balio.Irakurri(irakurle_balio.수('H')))
            elif 종류 == 3:
                balio = irakurle_balio.수('i')
            elif 종류 == 4:
                balio = irakurle_balio.Irakurri(4)
            elif 종류 in (5, 6):
                balio = irakurle_balio.Irakurri(8)
            elif 종류 in (7, 8, 16):
                balio = irakurle_balio.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                balio = (irakurle_balio.수('H'), irakurle_balio.수('H'))
            elif 종류 == 15:
                balio = (irakurle_balio.수('B'), irakurle_balio.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 konstante_balio 종류: {}'.format(종류))
            자신.konstante_balio[INDIZE] = (종류, balio)
            INDIZE += 2 if 종류 in (5, 6) else 1
        자신.atzitu_sarrera = irakurle_balio.수('H')
        자신.Izena = 자신.klasearen_izen(irakurle_balio.수('H'))
        부모 = irakurle_balio.수('H')
        if 자신.klasearen_izen(부모) != 'java/lang/Object' or irakurle_balio.수('H') != 0:
            raise 컴파일오류(자신.Izena + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.eremu_balio = 자신.멤버읽기(irakurle_balio)
        자신.FUNTZIOA_balio = 자신.멤버읽기(irakurle_balio)
        자신.속성읽기(irakurle_balio)

    def 문자(자신, INDIZE):
        if 자신.konstante_balio[INDIZE][0] != 1:
            raise 컴파일오류('kate_balio konstante_balio formatu_balio errorea')
        return 자신.konstante_balio[INDIZE][1]

    def klasearen_izen(자신, INDIZE):
        return 자신.문자(자신.konstante_balio[INDIZE][1])

    def Erreferentzia_materiala(자신, INDIZE):
        jabe_balio, izen_formatu = 자신.konstante_balio[INDIZE][1]
        Izena, formatu_balio = 자신.konstante_balio[izen_formatu][1]
        return 자신.klasearen_izen(jabe_balio), 자신.문자(Izena), 자신.문자(formatu_balio)

    def 속성읽기(자신, irakurle_balio):
        EMAITZA = {}
        for _ in range(irakurle_balio.수('H')):
            Izena = 자신.문자(irakurle_balio.수('H'))
            EMAITZA[Izena] = irakurle_balio.Irakurri(irakurle_balio.수('I'))
        return EMAITZA

    def 멤버읽기(자신, irakurle_balio):
        EMAITZA = []
        for _ in range(irakurle_balio.수('H')):
            atzitu_sarrera = irakurle_balio.수('H')
            Izena = 자신.문자(irakurle_balio.수('H'))
            formatu_balio = 자신.문자(irakurle_balio.수('H'))
            EMAITZA.append((atzitu_sarrera, Izena, formatu_balio, 자신.속성읽기(irakurle_balio)))
        return EMAITZA


def 형식읽기(kate_balio):
    EMAITZA = []
    Posizioa = 0
    while Posizioa < len(kate_balio):
        for formatu_balio in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if kate_balio.startswith(formatu_balio, Posizioa):
                EMAITZA.append(formatu_balio)
                Posizioa += len(formatu_balio)
                break
        else:
            raise 컴파일오류('지원하지 않는 datu_mota: ' + kate_balio)
    return EMAITZA


def 함수형식(서술):
    Argumentuak, itzuli_neurria = 서술[1:].split(')')
    Argumentuak = 형식읽기(Argumentuak)
    itzuli_MOTA = 형식읽기(itzuli_neurria)
    if 'V' in Argumentuak or len(itzuli_MOTA) != 1:
        raise 컴파일오류('FUNTZIOA_balio 서술 formatu_balio errorea: ' + 서술)
    return Argumentuak, itzuli_neurria


def ikur(종류, *부분):
    ITURBURUA = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ITURBURUA).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNTZIOA_balio 서술에 대해서만 허용한다.
def exekutatu_komando(Argumentuak=None):
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK iturburu_zuhaitz eraiki_sistema')
    analizatzaile_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analizatzaile_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Erantsi_sarrera JAR/Gela_balio 디렉터리')
    analizatzaile_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 eraiki_sistema JDK 또는 openjdk-build의 부트 JDK Bide_izena')
    analizatzaile_48ee4b1b.add_argument('--bundle-runtime', help='exekutatu_komando 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analizatzaile_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK aplik_abiarazle/iturburu_zuhaitz 빌드의 C 컴파일러')
    analizatzaile_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    analizatzaile_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 eraiki_sistema 작업 수')
    analizatzaile_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 eraiki_sistema helburu_balio (예: aarch64-linux-gnu)')
    analizatzaile_48ee4b1b.add_argument('--sysroot', help='교차 eraiki_sistema 대상의 libc/헤더/liburutegi 루트')
    analizatzaile_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formatu_balio')
    analizatzaile_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Gela_balio.FUNTZIOA_balio (자체 스택 ABI)')
    analizatzaile_48ee4b1b.add_argument('--entry', help='예: 계산.Exekutatu_2 (openjdk-build 이외 대상에서 필수)')
    analizatzaile_48ee4b1b.add_argument('-o', '--output', required=True, help='exekutatu_komando ELF/.o Irteera; openjdk-build는 전용 eraiki_sistema 디렉터리')
    analizatzaile_48ee4b1b.add_argument('sources', nargs='+')
    parametro_arg = analizatzaile_48ee4b1b.parse_args(Argumentuak)
    if parametro_arg.target == 'openjdk-build':
        if len(parametro_arg.sources) != 1 or not parametro_arg.java_home or parametro_arg.entry or parametro_arg.export or parametro_arg.classpath or parametro_arg.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK iturburu_zuhaitz 디렉터리 하나와 --java-home 부트 JDK, -o eraiki_sistema 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametro_arg.sources[0], parametro_arg.output, parametro_arg.java_home, parametro_arg.jobs, parametro_arg.openjdk_target,
                  parametro_arg.sysroot, None if parametro_arg.cc == 'cc' else parametro_arg.cc, parametro_arg.cxx, parametro_arg.configure_arg)
        except BuildError as errorea:
            raise 컴파일오류(str(errorea))
        return
    if not parametro_arg.entry:
        analizatzaile_48ee4b1b.error('--entry is required for this target')
    if parametro_arg.cxx or parametro_arg.openjdk_target or parametro_arg.sysroot or parametro_arg.configure_arg or parametro_arg.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build helburu_balio 전용')
    if parametro_arg.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import sortu_sarrera
        sortu_sarrera(parametro_arg)
        return
    if parametro_arg.classpath or parametro_arg.java_home or parametro_arg.bundle_runtime or parametro_arg.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk helburu_balio 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametro_arg.target, '--entry', parametro_arg.entry, '-o', parametro_arg.output]
    for Esleitu_balio in parametro_arg.export: 자바명령.extend(['--export', Esleitu_balio])
    subprocess.run(자바명령+parametro_arg.sources, check=True)
    return


if __name__ == '__main__':
    try:
        exekutatu_komando()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as errorea:
        print('eraiki_iturburu errorea: ' + str(errorea), file=sys.stderr)
        sys.exit(1)
