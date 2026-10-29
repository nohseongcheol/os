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


class chyba_kompilace(Exception):
    pass


class 자료읽기:
    def __init__(자신, data):
        자신.data = data
        자신.pozice = 0

    def Čtení(자신, délka_HODNOTA):
        if délka_HODNOTA < 0 or 자신.pozice + délka_HODNOTA > len(자신.data):
            raise chyba_kompilace('잘린 Třída_HODNOTA 또는 příkaz data')
        VÝSLEDEK = 자신.data[자신.pozice:자신.pozice + délka_HODNOTA]
        자신.pozice += délka_HODNOTA
        return VÝSLEDEK

    def číslo(자신, formát_HODNOTA):
        return struct.unpack('>' + formát_HODNOTA, 자신.Čtení(struct.calcsize('>' + formát_HODNOTA)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    řetězec_HODNOTA = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return řetězec_HODNOTA.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Třída_HODNOTA:
    def __init__(자신, cesta_2):
        자신.cesta_2 = cesta_2
        Čtenář_HODNOTA = 자료읽기(cesta_2.read_bytes())
        if Čtenář_HODNOTA.číslo('I') != 0xcafebabe:
            raise chyba_kompilace('Java Třída_HODNOTA 표식이 아님')
        Čtenář_HODNOTA.Čtení(4)
        zboží_POČET = Čtenář_HODNOTA.číslo('H')
        자신.konstanta_HODNOTA = [None] * zboží_POČET
        INDEX = 1
        while INDEX < zboží_POČET:
            Druh_HODNOTA = Čtenář_HODNOTA.číslo('B')
            if Druh_HODNOTA == 1:
                HODNOTA = 수정유티에프해독(Čtenář_HODNOTA.Čtení(Čtenář_HODNOTA.číslo('H')))
            elif Druh_HODNOTA == 3:
                HODNOTA = Čtenář_HODNOTA.číslo('i')
            elif Druh_HODNOTA == 4:
                HODNOTA = Čtenář_HODNOTA.Čtení(4)
            elif Druh_HODNOTA in (5, 6):
                HODNOTA = Čtenář_HODNOTA.Čtení(8)
            elif Druh_HODNOTA in (7, 8, 16):
                HODNOTA = Čtenář_HODNOTA.číslo('H')
            elif Druh_HODNOTA in (9, 10, 11, 12, 18):
                HODNOTA = (Čtenář_HODNOTA.číslo('H'), Čtenář_HODNOTA.číslo('H'))
            elif Druh_HODNOTA == 15:
                HODNOTA = (Čtenář_HODNOTA.číslo('B'), Čtenář_HODNOTA.číslo('H'))
            else:
                raise chyba_kompilace('지원하지 않는 konstanta_HODNOTA Druh_HODNOTA: {}'.format(Druh_HODNOTA))
            자신.konstanta_HODNOTA[INDEX] = (Druh_HODNOTA, HODNOTA)
            INDEX += 2 if Druh_HODNOTA in (5, 6) else 1
        자신.přístup_položka = Čtenář_HODNOTA.číslo('H')
        자신.Název = 자신.název_třídy(Čtenář_HODNOTA.číslo('H'))
        nadřazený_HODNOTA = Čtenář_HODNOTA.číslo('H')
        if 자신.název_třídy(nadřazený_HODNOTA) != 'java/lang/Object' or Čtenář_HODNOTA.číslo('H') != 0:
            raise chyba_kompilace(자신.Název + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.hodnota_pole = 자신.멤버읽기(Čtenář_HODNOTA)
        자신.funkce_HODNOTA = 자신.멤버읽기(Čtenář_HODNOTA)
        자신.속성읽기(Čtenář_HODNOTA)

    def 문자(자신, INDEX):
        if 자신.konstanta_HODNOTA[INDEX][0] != 1:
            raise chyba_kompilace('řetězec_HODNOTA konstanta_HODNOTA formát_HODNOTA chyba')
        return 자신.konstanta_HODNOTA[INDEX][1]

    def název_třídy(자신, INDEX):
        return 자신.문자(자신.konstanta_HODNOTA[INDEX][1])

    def odkaz(자신, INDEX):
        vlastník_HODNOTA, název_formát = 자신.konstanta_HODNOTA[INDEX][1]
        Název, formát_HODNOTA = 자신.konstanta_HODNOTA[název_formát][1]
        return 자신.název_třídy(vlastník_HODNOTA), 자신.문자(Název), 자신.문자(formát_HODNOTA)

    def 속성읽기(자신, Čtenář_HODNOTA):
        VÝSLEDEK = {}
        for _ in range(Čtenář_HODNOTA.číslo('H')):
            Název = 자신.문자(Čtenář_HODNOTA.číslo('H'))
            VÝSLEDEK[Název] = Čtenář_HODNOTA.Čtení(Čtenář_HODNOTA.číslo('I'))
        return VÝSLEDEK

    def 멤버읽기(자신, Čtenář_HODNOTA):
        VÝSLEDEK = []
        for _ in range(Čtenář_HODNOTA.číslo('H')):
            přístup_položka = Čtenář_HODNOTA.číslo('H')
            Název = 자신.문자(Čtenář_HODNOTA.číslo('H'))
            formát_HODNOTA = 자신.문자(Čtenář_HODNOTA.číslo('H'))
            VÝSLEDEK.append((přístup_položka, Název, formát_HODNOTA, 자신.속성읽기(Čtenář_HODNOTA)))
        return VÝSLEDEK


def 형식읽기(řetězec_HODNOTA):
    VÝSLEDEK = []
    pozice = 0
    while pozice < len(řetězec_HODNOTA):
        for formát_HODNOTA in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if řetězec_HODNOTA.startswith(formát_HODNOTA, pozice):
                VÝSLEDEK.append(formát_HODNOTA)
                pozice += len(formát_HODNOTA)
                break
        else:
            raise chyba_kompilace('지원하지 않는 datový_typ: ' + řetězec_HODNOTA)
    return VÝSLEDEK


def metoda_popisovač(서술):
    argumenty, Vratka_KV = 서술[1:].split(')')
    argumenty = 형식읽기(argumenty)
    návratový_typ = 형식읽기(Vratka_KV)
    if 'V' in argumenty or len(návratový_typ) != 1:
        raise chyba_kompilace('funkce_HODNOTA 서술 formát_HODNOTA chyba: ' + 서술)
    return argumenty, Vratka_KV


def symbol(Druh_HODNOTA, *부분):
    zdrojový_soubor = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(Druh_HODNOTA, hashlib.sha256(zdrojový_soubor).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 funkce_HODNOTA 서술에 대해서만 허용한다.
def Provést_příkaz(argumenty=None):
    analyzátor_48ee4b1b = argparse.ArgumentParser(description='vlastní Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK zdroj_strom BLD_Systém')
    analyzátor_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    analyzátor_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Připojit_položka JAR/Třída_HODNOTA 디렉터리')
    analyzátor_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 BLD_Systém JDK 또는 openjdk-build의 부트 JDK cesta_2')
    analyzátor_48ee4b1b.add_argument('--bundle-runtime', help='Provést_příkaz 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    analyzátor_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK program_Launcher/zdroj_strom 빌드의 C kompilátor')
    analyzátor_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompilátor')
    analyzátor_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 BLD_Systém 작업 číslo')
    analyzátor_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 BLD_Systém cílová_úroveň (예: aarch64-linux-gnu)')
    analyzátor_48ee4b1b.add_argument('--sysroot', help='교차 BLD_Systém 대상의 libc/헤더/knihovna 루트')
    analyzátor_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formát_HODNOTA')
    analyzátor_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Třída_HODNOTA.funkce_HODNOTA (vlastní operand_Štos ABI)')
    analyzátor_48ee4b1b.add_argument('--entry', help='예: 계산.Spustit_2 (openjdk-build 이외 대상에서 필수)')
    analyzátor_48ee4b1b.add_argument('-o', '--output', required=True, help='Provést_příkaz ELF/.o výstupní_pozice; openjdk-build는 전용 BLD_Systém 디렉터리')
    analyzátor_48ee4b1b.add_argument('sources', nargs='+')
    parametr_argument = analyzátor_48ee4b1b.parse_args(argumenty)
    if parametr_argument.target == 'openjdk-build':
        if len(parametr_argument.sources) != 1 or not parametr_argument.java_home or parametr_argument.entry or parametr_argument.export or parametr_argument.classpath or parametr_argument.bundle_runtime:
            raise chyba_kompilace('openjdk-build: OpenJDK zdroj_strom 디렉터리 하나와 --java-home 부트 JDK, -o BLD_Systém 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametr_argument.sources[0], parametr_argument.output, parametr_argument.java_home, parametr_argument.jobs, parametr_argument.openjdk_target,
                  parametr_argument.sysroot, None if parametr_argument.cc == 'cc' else parametr_argument.cc, parametr_argument.cxx, parametr_argument.configure_arg)
        except BuildError as chyba:
            raise chyba_kompilace(str(chyba))
        return
    if not parametr_argument.entry:
        analyzátor_48ee4b1b.error('--entry is required for this target')
    if parametr_argument.cxx or parametr_argument.openjdk_target or parametr_argument.sysroot or parametr_argument.configure_arg or parametr_argument.jobs != 2:
        raise chyba_kompilace('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build cílová_úroveň 전용')
    if parametr_argument.target == 'openjdk':
        sys.modules.setdefault('kompilátor', sys.modules[__name__])
        from spustitelný_soubor import Create_položka
        Create_položka(parametr_argument)
        return
    if parametr_argument.classpath or parametr_argument.java_home or parametr_argument.bundle_runtime or parametr_argument.cc != 'cc':
        raise chyba_kompilace('classpath/java-home/bundle-runtime/cc 옵션은 openjdk cílová_úroveň 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametr_argument.target, '--entry', parametr_argument.entry, '-o', parametr_argument.output]
    for Přiřadit_HODNOTA in parametr_argument.export: 자바명령.extend(['--export', Přiřadit_HODNOTA])
    subprocess.run(자바명령+parametr_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Provést_příkaz()
    except (chyba_kompilace, OSError, ValueError, subprocess.CalledProcessError) as chyba:
        print('kompilovat_zdroj chyba: ' + str(chyba), file=sys.stderr)
        sys.exit(1)
