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


class błąd_kompilacji(Exception):
    pass


class 자료읽기:
    def __init__(자신, dane):
        자신.dane = dane
        자신.pozycja = 0

    def Odczyt(자신, długość_WARTOŚĆ):
        if długość_WARTOŚĆ < 0 or 자신.pozycja + długość_WARTOŚĆ > len(자신.dane):
            raise błąd_kompilacji('잘린 Klasa_WARTOŚĆ 또는 polecenie dane')
        WYNIK = 자신.dane[자신.pozycja:자신.pozycja + długość_WARTOŚĆ]
        자신.pozycja += długość_WARTOŚĆ
        return WYNIK

    def identyfikator(자신, format_WARTOŚĆ):
        return struct.unpack('>' + format_WARTOŚĆ, 자신.Odczyt(struct.calcsize('>' + format_WARTOŚĆ)))[0]


def 수정유티에프해독(dane):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ciąg_WARTOŚĆ = dane.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ciąg_WARTOŚĆ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Klasa_WARTOŚĆ:
    def __init__(자신, ścieżka_2):
        자신.ścieżka_2 = ścieżka_2
        Czytnik_WARTOŚĆ = 자료읽기(ścieżka_2.read_bytes())
        if Czytnik_WARTOŚĆ.identyfikator('I') != 0xcafebabe:
            raise błąd_kompilacji('Java Klasa_WARTOŚĆ 표식이 아님')
        Czytnik_WARTOŚĆ.Odczyt(4)
        towar_ILE_LICZB = Czytnik_WARTOŚĆ.identyfikator('H')
        자신.stała_WARTOŚĆ = [None] * towar_ILE_LICZB
        INDEKS = 1
        while INDEKS < towar_ILE_LICZB:
            Rodzaj_WARTOŚĆ = Czytnik_WARTOŚĆ.identyfikator('B')
            if Rodzaj_WARTOŚĆ == 1:
                WARTOŚĆ = 수정유티에프해독(Czytnik_WARTOŚĆ.Odczyt(Czytnik_WARTOŚĆ.identyfikator('H')))
            elif Rodzaj_WARTOŚĆ == 3:
                WARTOŚĆ = Czytnik_WARTOŚĆ.identyfikator('i')
            elif Rodzaj_WARTOŚĆ == 4:
                WARTOŚĆ = Czytnik_WARTOŚĆ.Odczyt(4)
            elif Rodzaj_WARTOŚĆ in (5, 6):
                WARTOŚĆ = Czytnik_WARTOŚĆ.Odczyt(8)
            elif Rodzaj_WARTOŚĆ in (7, 8, 16):
                WARTOŚĆ = Czytnik_WARTOŚĆ.identyfikator('H')
            elif Rodzaj_WARTOŚĆ in (9, 10, 11, 12, 18):
                WARTOŚĆ = (Czytnik_WARTOŚĆ.identyfikator('H'), Czytnik_WARTOŚĆ.identyfikator('H'))
            elif Rodzaj_WARTOŚĆ == 15:
                WARTOŚĆ = (Czytnik_WARTOŚĆ.identyfikator('B'), Czytnik_WARTOŚĆ.identyfikator('H'))
            else:
                raise błąd_kompilacji('지원하지 않는 stała_WARTOŚĆ Rodzaj_WARTOŚĆ: {}'.format(Rodzaj_WARTOŚĆ))
            자신.stała_WARTOŚĆ[INDEKS] = (Rodzaj_WARTOŚĆ, WARTOŚĆ)
            INDEKS += 2 if Rodzaj_WARTOŚĆ in (5, 6) else 1
        자신.dostęp_wpis = Czytnik_WARTOŚĆ.identyfikator('H')
        자신.Nazwa = 자신.nazwa_klasy(Czytnik_WARTOŚĆ.identyfikator('H'))
        nadrzędny_WARTOŚĆ = Czytnik_WARTOŚĆ.identyfikator('H')
        if 자신.nazwa_klasy(nadrzędny_WARTOŚĆ) != 'java/lang/Object' or Czytnik_WARTOŚĆ.identyfikator('H') != 0:
            raise błąd_kompilacji(자신.Nazwa + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.wartość_pola = 자신.멤버읽기(Czytnik_WARTOŚĆ)
        자신.FUNKCJA_WARTOŚĆ = 자신.멤버읽기(Czytnik_WARTOŚĆ)
        자신.속성읽기(Czytnik_WARTOŚĆ)

    def 문자(자신, INDEKS):
        if 자신.stała_WARTOŚĆ[INDEKS][0] != 1:
            raise błąd_kompilacji('ciąg_WARTOŚĆ stała_WARTOŚĆ format_WARTOŚĆ błąd')
        return 자신.stała_WARTOŚĆ[INDEKS][1]

    def nazwa_klasy(자신, INDEKS):
        return 자신.문자(자신.stała_WARTOŚĆ[INDEKS][1])

    def odwołanie(자신, INDEKS):
        właściciel_WARTOŚĆ, nazwa_format = 자신.stała_WARTOŚĆ[INDEKS][1]
        Nazwa, format_WARTOŚĆ = 자신.stała_WARTOŚĆ[nazwa_format][1]
        return 자신.nazwa_klasy(właściciel_WARTOŚĆ), 자신.문자(Nazwa), 자신.문자(format_WARTOŚĆ)

    def 속성읽기(자신, Czytnik_WARTOŚĆ):
        WYNIK = {}
        for _ in range(Czytnik_WARTOŚĆ.identyfikator('H')):
            Nazwa = 자신.문자(Czytnik_WARTOŚĆ.identyfikator('H'))
            WYNIK[Nazwa] = Czytnik_WARTOŚĆ.Odczyt(Czytnik_WARTOŚĆ.identyfikator('I'))
        return WYNIK

    def 멤버읽기(자신, Czytnik_WARTOŚĆ):
        WYNIK = []
        for _ in range(Czytnik_WARTOŚĆ.identyfikator('H')):
            dostęp_wpis = Czytnik_WARTOŚĆ.identyfikator('H')
            Nazwa = 자신.문자(Czytnik_WARTOŚĆ.identyfikator('H'))
            format_WARTOŚĆ = 자신.문자(Czytnik_WARTOŚĆ.identyfikator('H'))
            WYNIK.append((dostęp_wpis, Nazwa, format_WARTOŚĆ, 자신.속성읽기(Czytnik_WARTOŚĆ)))
        return WYNIK


def 형식읽기(ciąg_WARTOŚĆ):
    WYNIK = []
    pozycja = 0
    while pozycja < len(ciąg_WARTOŚĆ):
        for format_WARTOŚĆ in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ciąg_WARTOŚĆ.startswith(format_WARTOŚĆ, pozycja):
                WYNIK.append(format_WARTOŚĆ)
                pozycja += len(format_WARTOŚĆ)
                break
        else:
            raise błąd_kompilacji('지원하지 않는 typ_danych: ' + ciąg_WARTOŚĆ)
    return WYNIK


def metoda_deskryptor(서술):
    argumenty, Zwrot_KR = 서술[1:].split(')')
    argumenty = 형식읽기(argumenty)
    zwracany_typ = 형식읽기(Zwrot_KR)
    if 'V' in argumenty or len(zwracany_typ) != 1:
        raise błąd_kompilacji('FUNKCJA_WARTOŚĆ 서술 format_WARTOŚĆ błąd: ' + 서술)
    return argumenty, Zwrot_KR


def symbol(Rodzaj_WARTOŚĆ, *부분):
    plik_źródłowy = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(Rodzaj_WARTOŚĆ, hashlib.sha256(plik_źródłowy).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 FUNKCJA_WARTOŚĆ 서술에 대해서만 허용한다.
def Wykonaj_polecenie(argumenty=None):
    parser_48ee4b1b = argparse.ArgumentParser(description='własny Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK źródło_drzewo BLD_System')
    parser_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    parser_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 dołączać_wpis JAR/Klasa_WARTOŚĆ 디렉터리')
    parser_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 BLD_System JDK 또는 openjdk-build의 부트 JDK ścieżka_2')
    parser_48ee4b1b.add_argument('--bundle-runtime', help='Wykonaj_polecenie 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    parser_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK program_Launcher/źródło_drzewo 빌드의 C kompilator')
    parser_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ kompilator')
    parser_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 BLD_System 작업 identyfikator')
    parser_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 BLD_System wartość_docelowa (예: aarch64-linux-gnu)')
    parser_48ee4b1b.add_argument('--sysroot', help='교차 BLD_System 대상의 libc/헤더/biblioteka 루트')
    parser_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_WARTOŚĆ')
    parser_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Klasa_WARTOŚĆ.FUNKCJA_WARTOŚĆ (własny operand_Stos ABI)')
    parser_48ee4b1b.add_argument('--entry', help='예: 계산.Uruchom_2 (openjdk-build 이외 대상에서 필수)')
    parser_48ee4b1b.add_argument('-o', '--output', required=True, help='Wykonaj_polecenie ELF/.o pozycja_wyjścia; openjdk-build는 전용 BLD_System 디렉터리')
    parser_48ee4b1b.add_argument('sources', nargs='+')
    parametr_argument = parser_48ee4b1b.parse_args(argumenty)
    if parametr_argument.target == 'openjdk-build':
        if len(parametr_argument.sources) != 1 or not parametr_argument.java_home or parametr_argument.entry or parametr_argument.export or parametr_argument.classpath or parametr_argument.bundle_runtime:
            raise błąd_kompilacji('openjdk-build: OpenJDK źródło_drzewo 디렉터리 하나와 --java-home 부트 JDK, -o BLD_System 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametr_argument.sources[0], parametr_argument.output, parametr_argument.java_home, parametr_argument.jobs, parametr_argument.openjdk_target,
                  parametr_argument.sysroot, None if parametr_argument.cc == 'cc' else parametr_argument.cc, parametr_argument.cxx, parametr_argument.configure_arg)
        except BuildError as błąd:
            raise błąd_kompilacji(str(błąd))
        return
    if not parametr_argument.entry:
        parser_48ee4b1b.error('--entry is required for this target')
    if parametr_argument.cxx or parametr_argument.openjdk_target or parametr_argument.sysroot or parametr_argument.configure_arg or parametr_argument.jobs != 2:
        raise błąd_kompilacji('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build wartość_docelowa 전용')
    if parametr_argument.target == 'openjdk':
        sys.modules.setdefault('kompilator', sys.modules[__name__])
        from plik_wykonywalny import Twórca_wpis
        Twórca_wpis(parametr_argument)
        return
    if parametr_argument.classpath or parametr_argument.java_home or parametr_argument.bundle_runtime or parametr_argument.cc != 'cc':
        raise błąd_kompilacji('classpath/java-home/bundle-runtime/cc 옵션은 openjdk wartość_docelowa 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametr_argument.target, '--entry', parametr_argument.entry, '-o', parametr_argument.output]
    for Przypisz_WARTOŚĆ in parametr_argument.export: 자바명령.extend(['--export', Przypisz_WARTOŚĆ])
    subprocess.run(자바명령+parametr_argument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        Wykonaj_polecenie()
    except (błąd_kompilacji, OSError, ValueError, subprocess.CalledProcessError) as błąd:
        print('kompilować_źródło błąd: ' + str(błąd), file=sys.stderr)
        sys.exit(1)
