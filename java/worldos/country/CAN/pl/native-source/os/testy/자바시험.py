#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Wykonaj_polecenie, awaria_WARTOŚĆ/zasób_WARTOŚĆ granica_WARTOŚĆ testy."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import time
from test_użytkownik_sieć import maszyna_wirtualna, pozycja


def Edytuj_WARTOŚĆ(maszyna, Nazwa, treść_WARTOŚĆ_cb0f2404, Store_WARTOŚĆ=True):
    Uruchom_2 = len(maszyna.LOG_zapis)
    maszyna.직렬.sendall(('edit ' + Nazwa + '\n').encode())
    maszyna.stan_oczekiwania('...> ', Uruchom_2)
    for wiersz_wejścia in treść_WARTOŚĆ_cb0f2404.splitlines():
        assert len(wiersz_wejścia) <= 128
        Uruchom_2 = len(maszyna.LOG_zapis)
        maszyna.직렬.sendall((wiersz_wejścia + '\n').encode())
        maszyna.stan_oczekiwania('...> ', Uruchom_2)
    Uruchom_2 = len(maszyna.LOG_zapis)
    maszyna.직렬.sendall(b'.save\n' if Store_WARTOŚĆ else b'.cancel\n')
    WYNIK = maszyna.stan_oczekiwania('jkoros> ', Uruchom_2)
    assert ('Saved:' if Store_WARTOŚĆ else 'Cancelled; original preserved') in WYNIK, WYNIK


def Plik_ADRES():
    WYNIK = subprocess.check_output(['nm', '-n', str(pozycja / 'build/kernel.elf')], universal_newlines=True)
    for wiersz_wejścia in WYNIK.splitlines():
        if wiersz_wejścia.endswith(' ram_files'):
            return int(wiersz_wejścia.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gość_Plik(maszyna, gniazdo_WARTOŚĆ_ff41a4f1, Rozmiar, ścieżka_2):
    # testy VM의 메모리에서 rzeczywisty_dane 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    Adres = Plik_ADRES() + gniazdo_WARTOŚĆ_ff41a4f1 * 16384
    maszyna.monitor_WARTOŚĆ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(Adres, Rozmiar, ścieżka_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ścieżka_2.exists() and ścieżka_2.stat().st_size == Rozmiar:
            return ścieżka_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def przebieg_testu(Rodzaj_WARTOŚĆ):
    maszyna = maszyna_wirtualna(pozycja / ('build/kernel.elf' if Rodzaj_WARTOŚĆ == 'elf' else 'build/kernel.iso'), Rodzaj_WARTOŚĆ, sieć_WARTOŚĆ=False)
    WYNIK = {}
    try:
        maszyna.polecenie('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        maszyna.polecenie('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        maszyna.polecenie('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        maszyna.polecenie('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        maszyna.polecenie('java Missing', ['cannot read class: -2', 'Exit: 1'])
        maszyna.polecenie('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        maszyna.polecenie('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        treść_WARTOŚĆ_cb0f2404 = '''public class Calc {
 public static int fact(int n) {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
 }
 public static boolean check(int n) { return n == 7; }
 public static void main(String[] args) {
  int n = Integer.parseInt(args[0]);
  System.out.println(fact(n));
  int sum = 0;
  for (int i = 1; i <= n; i++) { sum = sum + i; }
  while (n > 0) { n--; }
  System.out.println(sum);
  System.out.println(n);
  System.out.println(check(7) && false || true);
  System.out.println(false && 1 / 0 == 0);
  System.out.println(true || 1 / 0 == 0);
  System.out.println(-2147483648 / -1);
  System.out.println(args[1]);
  System.out.println(args[1].length());
  System.out.println(args.length);
  String label = "sum=";
  label += sum;
  System.out.println(label);
  System.out.println(12 + "x" + false);
  System.out.println("logic=" + (true && check(7)));
  char letter = 'a';
  letter++;
  System.out.println(letter);
  System.out.println("letter=" + letter);
  int extra = 7;
  extra *= 3;
  extra -= 1;
  System.out.println(extra);
 }
}'''
        Edytuj_WARTOŚĆ(maszyna, 'Calc.java', treść_WARTOŚĆ_cb0f2404)
        maszyna.polecenie('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        pozycja_wyjścia = maszyna.polecenie('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        WYNIK['guest_output'] = pozycja_wyjścia
        wpis_Lista = maszyna.polecenie('ls', ['Calc.class'])
        Rozmiar = int(re.search(r'Calc\.class\s+(\d+) bytes', wpis_Lista).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Katalog_WARTOŚĆ:
            ścieżka_2 = Path(Katalog_WARTOŚĆ) / 'Calc.class'
            dane = gość_Plik(maszyna, 3, Rozmiar, ścieżka_2)
            rzeczywisty_dane = subprocess.check_output(['java', '-Xverify:all', '-cp', Katalog_WARTOŚĆ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert rzeczywisty_dane.splitlines() == 기대, rzeczywisty_dane
            WYNIK['class_sha256'] = hashlib.sha256(dane).hexdigest()
            WYNIK['openjdk_output'] = rzeczywisty_dane
        # 실패한 Edytuj_WARTOŚĆ/컴파일은 기존 class를 보존한다.
        Edytuj_WARTOŚĆ(maszyna, 'Calc.java', 'not Java at all', Store_WARTOŚĆ=False)
        maszyna.polecenie('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for nieważny_KR in [
            'public class Calc { public static void main(String[] args) { int x = ; } }',
            'public class Calc { public static void main(String[] args) { int x = true; } }',
            'public class Calc { public static void main(String[] args) { int x = 2147483648; } }',
            'public class Calc { public static int f() { int x = 1; } }',
            'public class Calc { public static void main(String[] args) { Object x = new Object(); } }',
            'public class Other { public static void main(String[] args) {} }',
            'public class Calc { public static void main(String[] args) { int while = 3; } }',
            'public class Calc { public static void main(String[] args) { if (true) int x = 3; } }',
            'public class Calc { public static void main(String[] args) { int x = 010; } }',
        ]:
            Edytuj_WARTOŚĆ(maszyna, 'Calc.java', nieważny_KR)
            maszyna.polecenie('javac Calc.java', ['javac error:', 'Exit: 1'])
            maszyna.polecenie('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # iteracja_WARTOŚĆ 실행은 przestrzeń_użytkownika sterta_WARTOŚĆ/프레임을 매번 초기화한다.
        for identyfikator in range(12):
            maszyna.polecenie('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        maszyna.polecenie('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        maszyna.polecenie('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Edytuj_WARTOŚĆ(maszyna, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        maszyna.polecenie('javac Calc.java', ['Compiled:', 'Exit: 0'])
        maszyna.polecenie('java Calc', ['instruction limit', 'Exit: 1'])
        maszyna.polecenie('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Edytuj_WARTOŚĆ(maszyna, 'Bad.class', 'garbage')
        maszyna.polecenie('java Bad', ['JVM error:', 'Exit: 1'])
        maszyna.polecenie('rm Bad.class', ['Removed'])
        maszyna.polecenie('java Bad', ['cannot read class: -2'])
        # Edytuj_WARTOŚĆ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Uruchom_2 = len(maszyna.LOG_zapis)
        maszyna.직렬.sendall(b'edit Hello.java\n')
        maszyna.stan_oczekiwania('...> ', Uruchom_2)
        Uruchom_2 = len(maszyna.LOG_zapis)
        maszyna.직렬.sendall(b'x' * 129 + b'\n')
        maszyna.stan_oczekiwania('...> ', Uruchom_2)
        maszyna.polecenie('.save', ['Too much input; original preserved'])
        maszyna.polecenie('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Edytuj_WARTOŚĆ(maszyna, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for identyfikator in range(3):
            Edytuj_WARTOŚĆ(maszyna, 'f' + str(identyfikator), 'occupied')
        maszyna.polecenie('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        maszyna.polecenie('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in maszyna.LOG_zapis.decode('utf-8', 'replace')
        WYNIK['serial'] = maszyna.LOG_zapis.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(Rodzaj_WARTOŚĆ))
        return WYNIK
    finally:
        maszyna.Zamknięte()


def 주코드(dane):
    """손상 시험용 main Code의 rzeczywisty_dane nazwa_pliku 오프셋/길이만 읽는다."""
    stanowisko_WARTOŚĆ = 8
    def 짧():
        nonlocal stanowisko_WARTOŚĆ
        WARTOŚĆ = struct.unpack_from('>H', dane, stanowisko_WARTOŚĆ)[0]
        stanowisko_WARTOŚĆ += 2
        return WARTOŚĆ
    def 정():
        nonlocal stanowisko_WARTOŚĆ
        WARTOŚĆ = struct.unpack_from('>I', dane, stanowisko_WARTOŚĆ)[0]
        stanowisko_WARTOŚĆ += 4
        return WARTOŚĆ
    문자들 = {}
    for identyfikator in range(1, 짧()):
        Rodzaj_WARTOŚĆ = dane[stanowisko_WARTOŚĆ]
        stanowisko_WARTOŚĆ += 1
        if Rodzaj_WARTOŚĆ == 1:
            długość_WARTOŚĆ = 짧()
            문자들[identyfikator] = dane[stanowisko_WARTOŚĆ:stanowisko_WARTOŚĆ + długość_WARTOŚĆ]
            stanowisko_WARTOŚĆ += długość_WARTOŚĆ
        elif Rodzaj_WARTOŚĆ in (7, 8): stanowisko_WARTOŚĆ += 2
        elif Rodzaj_WARTOŚĆ in (3, 9, 10, 12): stanowisko_WARTOŚĆ += 4
        else: raise AssertionError(Rodzaj_WARTOŚĆ)
    stanowisko_WARTOŚĆ += 6
    towar_ILE_LICZB = 짧()
    stanowisko_WARTOŚĆ += towar_ILE_LICZB * 2
    assert 짧() == 0
    for identyfikator in range(짧()):
        짧()
        Nazwa = 짧()
        짧()
        for identyfikator in range(짧()):
            wartość_atrybutu = 짧()
            Rozmiar = 정()
            if 문자들[Nazwa] == b'main' and 문자들[wartość_atrybutu] == b'Code':
                return stanowisko_WARTOŚĆ + 8, struct.unpack_from('>I', dane, stanowisko_WARTOŚĆ + 4)[0]
            stanowisko_WARTOŚĆ += Rozmiar
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Katalog_WARTOŚĆ = Path(임시)
        (Katalog_WARTOŚĆ / 'build').mkdir()
        plik_źródłowy = Katalog_WARTOŚĆ / 'Imported.java'
        plik_źródłowy.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(plik_źródłowy)], check=True)
        원본 = (Katalog_WARTOŚĆ / 'Imported.class').read_bytes()
        KOD_WARTOŚĆ, długość_WARTOŚĆ = 주코드(원본)
        wariant_WARTOŚĆ = {}
        dane = bytearray(원본); dane[0] = 0; wariant_WARTOŚĆ['BadMagic'] = dane
        dane = bytearray(원본); dane[7] = 61; wariant_WARTOŚĆ['BadVer'] = dane
        dane = bytearray(원본); dane[8:10] = b'\xff\xff'; wariant_WARTOŚĆ['BadPool'] = dane
        dane = bytearray(원본); dane[KOD_WARTOŚĆ:KOD_WARTOŚĆ + długość_WARTOŚĆ] = bytes(długość_WARTOŚĆ)
        dane[KOD_WARTOŚĆ:KOD_WARTOŚĆ + 3] = b'\xa7\x00\x01'; dane[KOD_WARTOŚĆ + długość_WARTOŚĆ - 1] = 177; wariant_WARTOŚĆ['BadJump'] = dane
        dane = bytearray(원본); dane[KOD_WARTOŚĆ:KOD_WARTOŚĆ + długość_WARTOŚĆ] = bytes(długość_WARTOŚĆ)
        dane[KOD_WARTOŚĆ] = 87; dane[KOD_WARTOŚĆ + długość_WARTOŚĆ - 1] = 177; wariant_WARTOŚĆ['BadStack'] = dane
        # Nazwa 검사를 통과시켜 rzeczywisty_dane Wykonaj_polecenie 중의 operand_Stos 오류까지 검사한다.
        wariant_WARTOŚĆ['BadStack'] = wariant_WARTOŚĆ['BadStack'].replace(b'Imported', b'BadStack')
        wpis_WARTOŚĆ = ['Imported.class=' + str(Katalog_WARTOŚĆ / 'Imported.class'), 'Imported.java=' + str(plik_źródłowy)]
        for Nazwa, dane in wariant_WARTOŚĆ.items():
            ścieżka_2 = Katalog_WARTOŚĆ / (Nazwa + '.class'); ścieżka_2.write_bytes(dane)
            wpis_WARTOŚĆ.append(Nazwa + '.class=' + str(ścieżka_2))
        grupa_WARTOŚĆ = Katalog_WARTOŚĆ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(pozycja / 'narzędzia/자바파일묶기.py'), '-o', str(grupa_WARTOŚĆ)] + wpis_WARTOŚĆ, check=True)
        subprocess.run(['as', '--32', '-o', str(Katalog_WARTOŚĆ / 'user.o'), str(pozycja / 'rozruch_maszyny/przestrzeń_użytkownika.s')], cwd=str(Katalog_WARTOŚĆ), check=True)
        jądro_WARTOŚĆ = Katalog_WARTOŚĆ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozycja / 'rozruch_maszyny/układ_konsolidacji.ld'), '-o', str(jądro_WARTOŚĆ),
                        str(pozycja / 'build/boot.o'), str(pozycja / 'build/java.o'), str(Katalog_WARTOŚĆ / 'user.o'), str(pozycja / 'build/apps.o')], check=True)
        maszyna = maszyna_wirtualna(jądro_WARTOŚĆ, sieć_WARTOŚĆ=False)
        try:
            maszyna.polecenie('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            maszyna.polecenie('cat Imported.java', ['int[] values = new int[3]'])
            for Nazwa, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                maszyna.polecenie('java ' + Nazwa, [문구, 'Exit: 1'])
                maszyna.polecenie('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return maszyna.LOG_zapis.decode('utf-8', 'replace')
        finally:
            maszyna.Zamknięte()


if __name__ == '__main__':
    analizować_WARTOŚĆ = argparse.ArgumentParser()
    analizować_WARTOŚĆ.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argumenty = analizować_WARTOŚĆ.parse_args()
    WYNIK = {Rodzaj_WARTOŚĆ: przebieg_testu(Rodzaj_WARTOŚĆ) for Rodzaj_WARTOŚĆ in (('elf', 'iso') if argumenty.boot == 'both' else (argumenty.boot,))}
    WYNIK['import'] = 적재시험()
    (pozycja / 'build/자바시험.json').write_text(json.dumps(WYNIK, ensure_ascii=False, indent=2) + '\n')
