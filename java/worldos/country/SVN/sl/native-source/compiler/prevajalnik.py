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


class napaka_pri_prevajanju(Exception):
    pass


class 자료읽기:
    def __init__(자신, podatki):
        자신.podatki = podatki
        자신.Položaj = 0

    def Branje(자신, 길이):
        if 길이 < 0 or 자신.Položaj + 길이 > len(자신.podatki):
            raise napaka_pri_prevajanju('잘린 Razred_VALUE 또는 Ukaz podatki')
        REZULTAT = 자신.podatki[자신.Položaj:자신.Položaj + 길이]
        자신.Položaj += 길이
        return REZULTAT

    def 수(자신, oblika_VALUE):
        return struct.unpack('>' + oblika_VALUE, 자신.Branje(struct.calcsize('>' + oblika_VALUE)))[0]


def 수정유티에프해독(podatki):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    niz_VALUE = podatki.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return niz_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Razred_VALUE:
    def __init__(자신, POT):
        자신.POT = POT
        bralec_VALUE = 자료읽기(POT.read_bytes())
        if bralec_VALUE.수('I') != 0xcafebabe:
            raise napaka_pri_prevajanju('Java Razred_VALUE 표식이 아님')
        bralec_VALUE.Branje(4)
        element_COUNT = bralec_VALUE.수('H')
        자신.konstanta_VALUE = [None] * element_COUNT
        INDEX = 1
        while INDEX < element_COUNT:
            종류 = bralec_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(bralec_VALUE.Branje(bralec_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = bralec_VALUE.수('i')
            elif 종류 == 4:
                VALUE = bralec_VALUE.Branje(4)
            elif 종류 in (5, 6):
                VALUE = bralec_VALUE.Branje(8)
            elif 종류 in (7, 8, 16):
                VALUE = bralec_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (bralec_VALUE.수('H'), bralec_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (bralec_VALUE.수('B'), bralec_VALUE.수('H'))
            else:
                raise napaka_pri_prevajanju('지원하지 않는 konstanta_VALUE 종류: {}'.format(종류))
            자신.konstanta_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.dostop_vnos = bralec_VALUE.수('H')
        자신.Ime = 자신.ime_razreda(bralec_VALUE.수('H'))
        nadrejen_VALUE = bralec_VALUE.수('H')
        if 자신.ime_razreda(nadrejen_VALUE) != 'java/lang/Object' or bralec_VALUE.수('H') != 0:
            raise napaka_pri_prevajanju(자신.Ime + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.polje_VALUE = 자신.멤버읽기(bralec_VALUE)
        자신.FUNCTION_VALUE = 자신.멤버읽기(bralec_VALUE)
        자신.속성읽기(bralec_VALUE)

    def 문자(자신, INDEX):
        if 자신.konstanta_VALUE[INDEX][0] != 1:
            raise napaka_pri_prevajanju('niz_VALUE konstanta_VALUE oblika_VALUE NAPAKA')
        return 자신.konstanta_VALUE[INDEX][1]

    def ime_razreda(자신, INDEX):
        return 자신.문자(자신.konstanta_VALUE[INDEX][1])

    def Gradiva(자신, INDEX):
        lastnik_VALUE, ime_oblika = 자신.konstanta_VALUE[INDEX][1]
        Ime, oblika_VALUE = 자신.konstanta_VALUE[ime_oblika][1]
        return 자신.ime_razreda(lastnik_VALUE), 자신.문자(Ime), 자신.문자(oblika_VALUE)

    def 속성읽기(자신, bralec_VALUE):
        REZULTAT = {}
        for _ in range(bralec_VALUE.수('H')):
            Ime = 자신.문자(bralec_VALUE.수('H'))
            REZULTAT[Ime] = bralec_VALUE.Branje(bralec_VALUE.수('I'))
        return REZULTAT

    def 멤버읽기(자신, bralec_VALUE):
        REZULTAT = []
        for _ in range(bralec_VALUE.수('H')):
            dostop_vnos = bralec_VALUE.수('H')
            Ime = 자신.문자(bralec_VALUE.수('H'))
            oblika_VALUE = 자신.문자(bralec_VALUE.수('H'))
            REZULTAT.append((dostop_vnos, Ime, oblika_VALUE, 자신.속성읽기(bralec_VALUE)))
        return REZULTAT


def 형식읽기(niz_VALUE):
    REZULTAT = []
    Položaj = 0
    while Položaj < len(niz_VALUE):
        for oblika_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if niz_VALUE.startswith(oblika_VALUE, Položaj):
                REZULTAT.append(oblika_VALUE)
                Položaj += len(oblika_VALUE)
                break
        else:
            raise napaka_pri_prevajanju('지원하지 않는 vrsta_podatkov: ' + niz_VALUE)
    return REZULTAT


def 함수형식(서술):
    Argumenti, vrni_KR = 서술[1:].split(')')
    Argumenti = 형식읽기(Argumenti)
    vrni_Tip = 형식읽기(vrni_KR)
    if 'V' in Argumenti or len(vrni_Tip) != 1:
        raise napaka_pri_prevajanju('FUNCTION_VALUE 서술 oblika_VALUE NAPAKA: ' + 서술)
    return Argumenti, vrni_KR


def simbol(종류, *부분):
    VIR = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(VIR).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNCTION_VALUE 서술에 대해서만 허용한다.
def Izvedi_ukaz(Argumenti=None):
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description='lastno Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK vir_drevo graditev_sistem')
    razčlenjevalnik_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    razčlenjevalnik_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 dodati_vnos JAR/Razred_VALUE 디렉터리')
    razčlenjevalnik_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 graditev_sistem JDK 또는 openjdk-build의 부트 JDK POT')
    razčlenjevalnik_48ee4b1b.add_argument('--bundle-runtime', help='Izvedi_ukaz 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    razčlenjevalnik_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK aplikacija_zaganjalnik/vir_drevo 빌드의 C prevajalnik')
    razčlenjevalnik_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ prevajalnik')
    razčlenjevalnik_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 graditev_sistem 작업 수')
    razčlenjevalnik_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 graditev_sistem tarča (예: aarch64-linux-gnu)')
    razčlenjevalnik_48ee4b1b.add_argument('--sysroot', help='교차 graditev_sistem 대상의 libc/헤더/knjižnica 루트')
    razčlenjevalnik_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 oblika_VALUE')
    razčlenjevalnik_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Razred_VALUE.FUNCTION_VALUE (lastno operand_Sklad ABI)')
    razčlenjevalnik_48ee4b1b.add_argument('--entry', help='예: 계산.Zaženi (openjdk-build 이외 대상에서 필수)')
    razčlenjevalnik_48ee4b1b.add_argument('-o', '--output', required=True, help='Izvedi_ukaz ELF/.o Izpis; openjdk-build는 전용 graditev_sistem 디렉터리')
    razčlenjevalnik_48ee4b1b.add_argument('sources', nargs='+')
    parameter_argument = razčlenjevalnik_48ee4b1b.parse_args(Argumenti)
    if parameter_argument.target == 'openjdk-build':
        if len(parameter_argument.sources) != 1 or not parameter_argument.java_home or parameter_argument.entry or parameter_argument.export or parameter_argument.classpath or parameter_argument.bundle_runtime:
            raise napaka_pri_prevajanju('openjdk-build: OpenJDK vir_drevo 디렉터리 하나와 --java-home 부트 JDK, -o graditev_sistem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argument.sources[0], parameter_argument.output, parameter_argument.java_home, parameter_argument.jobs, parameter_argument.openjdk_target,
                  parameter_argument.sysroot, None if parameter_argument.cc == 'cc' else parameter_argument.cc, parameter_argument.cxx, parameter_argument.configure_arg)
        except BuildError as NAPAKA:
            raise napaka_pri_prevajanju(str(NAPAKA))
        return
    if not parameter_argument.entry:
        razčlenjevalnik_48ee4b1b.error('--entry is required for this target')
    if parameter_argument.cxx or parameter_argument.openjdk_target or parameter_argument.sysroot or parameter_argument.configure_arg or parameter_argument.jobs != 2:
        raise napaka_pri_prevajanju('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build tarča 전용')
    if parameter_argument.target == 'openjdk':
        sys.modules.setdefault('prevajalnik', sys.modules[__name__])
        from 실행파일 import Ustvari_vnos
        Ustvari_vnos(parameter_argument)
        return
    if parameter_argument.classpath or parameter_argument.java_home or parameter_argument.bundle_runtime or parameter_argument.cc != 'cc':
        raise napaka_pri_prevajanju('classpath/java-home/bundle-runtime/cc 옵션은 openjdk tarča 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argument.target, '--entry', parameter_argument.entry, '-o', parameter_argument.output]
    for Dodeli_VALUE in parameter_argument.export: 자바명령.extend(['--export', Dodeli_VALUE])
    subprocess.run(자바명령+parameter_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Izvedi_ukaz()
    except (napaka_pri_prevajanju, OSError, ValueError, subprocess.CalledProcessError) as NAPAKA:
        print('prevajati_vir NAPAKA: ' + str(NAPAKA), file=sys.stderr)
        sys.exit(1)
