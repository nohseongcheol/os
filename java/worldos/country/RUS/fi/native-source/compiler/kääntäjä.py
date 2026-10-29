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


class lukea_data:
    def __init__(자신, data):
        자신.data = data
        자신.paikka = 0

    def Luku(자신, kesto_ARVO):
        if kesto_ARVO < 0 or 자신.paikka + kesto_ARVO > len(자신.data):
            raise 컴파일오류('잘린 Luokka_ARVO 또는 komento data')
        TULOS = 자신.data[자신.paikka:자신.paikka + kesto_ARVO]
        자신.paikka += kesto_ARVO
        return TULOS

    def numero(자신, muoto_ARVO):
        return struct.unpack('>' + muoto_ARVO, 자신.Luku(struct.calcsize('>' + muoto_ARVO)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    merkkijono_ARVO = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return merkkijono_ARVO.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Luokka_ARVO:
    def __init__(자신, polku_2):
        자신.polku_2 = polku_2
        Lukija_ARVO = lukea_data(polku_2.read_bytes())
        if Lukija_ARVO.numero('I') != 0xcafebabe:
            raise 컴파일오류('Java Luokka_ARVO 표식이 아님')
        Lukija_ARVO.Luku(4)
        kohde_LASKE = Lukija_ARVO.numero('H')
        자신.vakio_ARVO = [None] * kohde_LASKE
        INDEKSI = 1
        while INDEKSI < kohde_LASKE:
            종류 = Lukija_ARVO.numero('B')
            if 종류 == 1:
                ARVO = 수정유티에프해독(Lukija_ARVO.Luku(Lukija_ARVO.numero('H')))
            elif 종류 == 3:
                ARVO = Lukija_ARVO.numero('i')
            elif 종류 == 4:
                ARVO = Lukija_ARVO.Luku(4)
            elif 종류 in (5, 6):
                ARVO = Lukija_ARVO.Luku(8)
            elif 종류 in (7, 8, 16):
                ARVO = Lukija_ARVO.numero('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ARVO = (Lukija_ARVO.numero('H'), Lukija_ARVO.numero('H'))
            elif 종류 == 15:
                ARVO = (Lukija_ARVO.numero('B'), Lukija_ARVO.numero('H'))
            else:
                raise 컴파일오류('지원하지 않는 vakio_ARVO 종류: {}'.format(종류))
            자신.vakio_ARVO[INDEKSI] = (종류, ARVO)
            INDEKSI += 2 if 종류 in (5, 6) else 1
        자신.pääsy_merkintä_68aed533 = Lukija_ARVO.numero('H')
        자신.Nimi = 자신.luokan_nimi(Lukija_ARVO.numero('H'))
        pää_ARVO = Lukija_ARVO.numero('H')
        if 자신.luokan_nimi(pää_ARVO) != 'java/lang/Object' or Lukija_ARVO.numero('H') != 0:
            raise 컴파일오류(자신.Nimi + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.kentän_arvo = 자신.멤버읽기(Lukija_ARVO)
        자신.funktio_ARVO = 자신.멤버읽기(Lukija_ARVO)
        자신.lukea_määritteet(Lukija_ARVO)

    def 문자(자신, INDEKSI):
        if 자신.vakio_ARVO[INDEKSI][0] != 1:
            raise 컴파일오류('merkkijono_ARVO vakio_ARVO muoto_ARVO VIRHE')
        return 자신.vakio_ARVO[INDEKSI][1]

    def luokan_nimi(자신, INDEKSI):
        return 자신.문자(자신.vakio_ARVO[INDEKSI][1])

    def viite(자신, INDEKSI):
        omistaja_ARVO, nimi_muoto = 자신.vakio_ARVO[INDEKSI][1]
        Nimi, muoto_ARVO = 자신.vakio_ARVO[nimi_muoto][1]
        return 자신.luokan_nimi(omistaja_ARVO), 자신.문자(Nimi), 자신.문자(muoto_ARVO)

    def lukea_määritteet(자신, Lukija_ARVO):
        TULOS = {}
        for _ in range(Lukija_ARVO.numero('H')):
            Nimi = 자신.문자(Lukija_ARVO.numero('H'))
            TULOS[Nimi] = Lukija_ARVO.Luku(Lukija_ARVO.numero('I'))
        return TULOS

    def 멤버읽기(자신, Lukija_ARVO):
        TULOS = []
        for _ in range(Lukija_ARVO.numero('H')):
            pääsy_merkintä_68aed533 = Lukija_ARVO.numero('H')
            Nimi = 자신.문자(Lukija_ARVO.numero('H'))
            muoto_ARVO = 자신.문자(Lukija_ARVO.numero('H'))
            TULOS.append((pääsy_merkintä_68aed533, Nimi, muoto_ARVO, 자신.lukea_määritteet(Lukija_ARVO)))
        return TULOS


def 형식읽기(merkkijono_ARVO):
    TULOS = []
    paikka = 0
    while paikka < len(merkkijono_ARVO):
        for muoto_ARVO in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if merkkijono_ARVO.startswith(muoto_ARVO, paikka):
                TULOS.append(muoto_ARVO)
                paikka += len(muoto_ARVO)
                break
        else:
            raise 컴파일오류('지원하지 않는 tietotyyppi: ' + merkkijono_ARVO)
    return TULOS


def 함수형식(서술):
    argumentit, palauttaa_KR = 서술[1:].split(')')
    argumentit = 형식읽기(argumentit)
    palauttaa_TYYPPI = 형식읽기(palauttaa_KR)
    if 'V' in argumentit or len(palauttaa_TYYPPI) != 1:
        raise 컴파일오류('funktio_ARVO 서술 muoto_ARVO VIRHE: ' + 서술)
    return argumentit, palauttaa_KR


def symboli(종류, *부분):
    lähdetiedosto = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(lähdetiedosto).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 funktio_ARVO 서술에 대해서만 허용한다.
def Suorita_komento(argumentit=None):
    jäsennin_48ee4b1b = argparse.ArgumentParser(description='oma Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK lähde_puu kääntää_Järjestelmä')
    jäsennin_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    jäsennin_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 liitä_merkintä JAR/Luokka_ARVO 디렉터리')
    jäsennin_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 kääntää_Järjestelmä JDK 또는 openjdk-build의 부트 JDK polku_2')
    jäsennin_48ee4b1b.add_argument('--bundle-runtime', help='Suorita_komento 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    jäsennin_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK ohjelma_sovellusvalikko/lähde_puu 빌드의 C kääntäjä')
    jäsennin_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kääntäjä')
    jäsennin_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 kääntää_Järjestelmä 작업 numero')
    jäsennin_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 kääntää_Järjestelmä tavoite (예: aarch64-linux-gnu)')
    jäsennin_48ee4b1b.add_argument('--sysroot', help='교차 kääntää_Järjestelmä 대상의 libc/헤더/kirjasto 루트')
    jäsennin_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 muoto_ARVO')
    jäsennin_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Luokka_ARVO.funktio_ARVO (oma operandi_Pino ABI)')
    jäsennin_48ee4b1b.add_argument('--entry', help='예: 계산.Suorita_2 (openjdk-build 이외 대상에서 필수)')
    jäsennin_48ee4b1b.add_argument('-o', '--output', required=True, help='Suorita_komento ELF/.o tulostuspaikka; openjdk-build는 전용 kääntää_Järjestelmä 디렉터리')
    jäsennin_48ee4b1b.add_argument('sources', nargs='+')
    parametri_argumentti = jäsennin_48ee4b1b.parse_args(argumentit)
    if parametri_argumentti.target == 'openjdk-build':
        if len(parametri_argumentti.sources) != 1 or not parametri_argumentti.java_home or parametri_argumentti.entry or parametri_argumentti.export or parametri_argumentti.classpath or parametri_argumentti.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK lähde_puu 디렉터리 하나와 --java-home 부트 JDK, -o kääntää_Järjestelmä 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametri_argumentti.sources[0], parametri_argumentti.output, parametri_argumentti.java_home, parametri_argumentti.jobs, parametri_argumentti.openjdk_target,
                  parametri_argumentti.sysroot, None if parametri_argumentti.cc == 'cc' else parametri_argumentti.cc, parametri_argumentti.cxx, parametri_argumentti.configure_arg)
        except BuildError as VIRHE:
            raise 컴파일오류(str(VIRHE))
        return
    if not parametri_argumentti.entry:
        jäsennin_48ee4b1b.error('--entry is required for this target')
    if parametri_argumentti.cxx or parametri_argumentti.openjdk_target or parametri_argumentti.sysroot or parametri_argumentti.configure_arg or parametri_argumentti.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build tavoite 전용')
    if parametri_argumentti.target == 'openjdk':
        sys.modules.setdefault('kääntäjä', sys.modules[__name__])
        from suoritettava_tiedosto import Luo_merkintä
        Luo_merkintä(parametri_argumentti)
        return
    if parametri_argumentti.classpath or parametri_argumentti.java_home or parametri_argumentti.bundle_runtime or parametri_argumentti.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk tavoite 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametri_argumentti.target, '--entry', parametri_argumentti.entry, '-o', parametri_argumentti.output]
    for Määritä_ARVO in parametri_argumentti.export: 자바명령.extend(['--export', Määritä_ARVO])
    subprocess.run(자바명령+parametri_argumentti.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Suorita_komento()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as VIRHE:
        print('kääntää_lähde VIRHE: ' + str(VIRHE), file=sys.stderr)
        sys.exit(1)
