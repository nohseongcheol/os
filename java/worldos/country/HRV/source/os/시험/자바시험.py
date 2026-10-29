#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Izvrši_naredba, kvar_VALUE/resurs_VALUE 경계 시험."""
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
from 사용자통신시험 import VM, Položaj


def Uredi_VALUE(stroj, Ime, Sadržaj_VALUE, Store_VALUE=True):
    Pokreni = len(stroj.LOG_zapis)
    stroj.직렬.sendall(('edit ' + Ime + '\n').encode())
    stroj.stanje_čekanja('...> ', Pokreni)
    for red in Sadržaj_VALUE.splitlines():
        assert len(red) <= 128
        Pokreni = len(stroj.LOG_zapis)
        stroj.직렬.sendall((red + '\n').encode())
        stroj.stanje_čekanja('...> ', Pokreni)
    Pokreni = len(stroj.LOG_zapis)
    stroj.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    REZULTAT = stroj.stanje_čekanja('jkoros> ', Pokreni)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in REZULTAT, REZULTAT


def Datoteka_adresa():
    REZULTAT = subprocess.check_output(['nm', '-n', str(Položaj / 'build/kernel.elf')], universal_newlines=True)
    for red in REZULTAT.splitlines():
        if red.endswith(' ram_files'):
            return int(red.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gost_Datoteka(stroj, 슬롯, Veličina, PUTANJA):
    # 시험 VM의 메모리에서 stvaran_podaci 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    adresa = Datoteka_adresa() + 슬롯 * 16384
    stroj.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(adresa, Veličina, PUTANJA)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if PUTANJA.exists() and PUTANJA.stat().st_size == Veličina:
            return PUTANJA.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    stroj = VM(Položaj / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, mreža_VALUE=False)
    REZULTAT = {}
    try:
        stroj.Naredba('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        stroj.Naredba('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        stroj.Naredba('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        stroj.Naredba('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        stroj.Naredba('java Missing', ['cannot read class: -2', 'Exit: 1'])
        stroj.Naredba('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        stroj.Naredba('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Sadržaj_VALUE = '''public class Calc {
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
        Uredi_VALUE(stroj, 'Calc.java', Sadržaj_VALUE)
        stroj.Naredba('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Izlaz = stroj.Naredba('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        REZULTAT['guest_output'] = Izlaz
        unos_Popis = stroj.Naredba('ls', ['Calc.class'])
        Veličina = int(re.search(r'Calc\.class\s+(\d+) bytes', unos_Popis).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as imenik_VALUE:
            PUTANJA = Path(imenik_VALUE) / 'Calc.class'
            podaci = gost_Datoteka(stroj, 3, Veličina, PUTANJA)
            stvaran_podaci = subprocess.check_output(['java', '-Xverify:all', '-cp', imenik_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert stvaran_podaci.splitlines() == 기대, stvaran_podaci
            REZULTAT['class_sha256'] = hashlib.sha256(podaci).hexdigest()
            REZULTAT['openjdk_output'] = stvaran_podaci
        # 실패한 Uredi_VALUE/컴파일은 기존 class를 보존한다.
        Uredi_VALUE(stroj, 'Calc.java', 'not Java at all', Store_VALUE=False)
        stroj.Naredba('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for nevaljan_KR in [
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
            Uredi_VALUE(stroj, 'Calc.java', nevaljan_KR)
            stroj.Naredba('javac Calc.java', ['javac error:', 'Exit: 1'])
            stroj.Naredba('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 korisnik 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            stroj.Naredba('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        stroj.Naredba('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        stroj.Naredba('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Uredi_VALUE(stroj, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        stroj.Naredba('javac Calc.java', ['Compiled:', 'Exit: 0'])
        stroj.Naredba('java Calc', ['instruction limit', 'Exit: 1'])
        stroj.Naredba('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Uredi_VALUE(stroj, 'Bad.class', 'garbage')
        stroj.Naredba('java Bad', ['JVM error:', 'Exit: 1'])
        stroj.Naredba('rm Bad.class', ['Removed'])
        stroj.Naredba('java Bad', ['cannot read class: -2'])
        # Uredi_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Pokreni = len(stroj.LOG_zapis)
        stroj.직렬.sendall(b'edit Hello.java\n')
        stroj.stanje_čekanja('...> ', Pokreni)
        Pokreni = len(stroj.LOG_zapis)
        stroj.직렬.sendall(b'x' * 129 + b'\n')
        stroj.stanje_čekanja('...> ', Pokreni)
        stroj.Naredba('.save', ['Too much input; original preserved'])
        stroj.Naredba('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Uredi_VALUE(stroj, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Uredi_VALUE(stroj, 'f' + str(수), 'occupied')
        stroj.Naredba('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        stroj.Naredba('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in stroj.LOG_zapis.decode('utf-8', 'replace')
        REZULTAT['serial'] = stroj.LOG_zapis.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return REZULTAT
    finally:
        stroj.Zatvori()


def 주코드(podaci):
    """손상 시험용 main Code의 stvaran_podaci Datoteka 오프셋/길이만 읽는다."""
    položaj_VALUE = 8
    def 짧():
        nonlocal položaj_VALUE
        VALUE = struct.unpack_from('>H', podaci, položaj_VALUE)[0]
        položaj_VALUE += 2
        return VALUE
    def 정():
        nonlocal položaj_VALUE
        VALUE = struct.unpack_from('>I', podaci, položaj_VALUE)[0]
        položaj_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = podaci[položaj_VALUE]
        položaj_VALUE += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[수] = podaci[položaj_VALUE:položaj_VALUE + 길이]
            položaj_VALUE += 길이
        elif 종류 in (7, 8): položaj_VALUE += 2
        elif 종류 in (3, 9, 10, 12): položaj_VALUE += 4
        else: raise AssertionError(종류)
    položaj_VALUE += 6
    artikl_COUNT = 짧()
    položaj_VALUE += artikl_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Ime = 짧()
        짧()
        for 수 in range(짧()):
            atribut_VALUE = 짧()
            Veličina = 정()
            if 문자들[Ime] == b'main' and 문자들[atribut_VALUE] == b'Code':
                return položaj_VALUE + 8, struct.unpack_from('>I', podaci, položaj_VALUE + 4)[0]
            položaj_VALUE += Veličina
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        imenik_VALUE = Path(임시)
        (imenik_VALUE / 'build').mkdir()
        IZVOR = imenik_VALUE / 'Imported.java'
        IZVOR.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(IZVOR)], check=True)
        원본 = (imenik_VALUE / 'Imported.class').read_bytes()
        kod_VALUE, 길이 = 주코드(원본)
        변형 = {}
        podaci = bytearray(원본); podaci[0] = 0; 변형['BadMagic'] = podaci
        podaci = bytearray(원본); podaci[7] = 61; 변형['BadVer'] = podaci
        podaci = bytearray(원본); podaci[8:10] = b'\xff\xff'; 변형['BadPool'] = podaci
        podaci = bytearray(원본); podaci[kod_VALUE:kod_VALUE + 길이] = bytes(길이)
        podaci[kod_VALUE:kod_VALUE + 3] = b'\xa7\x00\x01'; podaci[kod_VALUE + 길이 - 1] = 177; 변형['BadJump'] = podaci
        podaci = bytearray(원본); podaci[kod_VALUE:kod_VALUE + 길이] = bytes(길이)
        podaci[kod_VALUE] = 87; podaci[kod_VALUE + 길이 - 1] = 177; 변형['BadStack'] = podaci
        # Ime 검사를 통과시켜 stvaran_podaci Izvrši_naredba 중의 operand_hrpa 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        unos_VALUE = ['Imported.class=' + str(imenik_VALUE / 'Imported.class'), 'Imported.java=' + str(IZVOR)]
        for Ime, podaci in 변형.items():
            PUTANJA = imenik_VALUE / (Ime + '.class'); PUTANJA.write_bytes(podaci)
            unos_VALUE.append(Ime + '.class=' + str(PUTANJA))
        Grupa_VALUE = imenik_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Položaj / 'Alati/자바파일묶기.py'), '-o', str(Grupa_VALUE)] + unos_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(imenik_VALUE / 'user.o'), str(Položaj / '부팅/korisnik.s')], cwd=str(imenik_VALUE), check=True)
        jezgra_sustava_VALUE = imenik_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Položaj / '부팅/veza_Raspored.ld'), '-o', str(jezgra_sustava_VALUE),
                        str(Položaj / 'build/boot.o'), str(Položaj / 'build/java.o'), str(imenik_VALUE / 'user.o'), str(Položaj / 'build/apps.o')], check=True)
        stroj = VM(jezgra_sustava_VALUE, mreža_VALUE=False)
        try:
            stroj.Naredba('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            stroj.Naredba('cat Imported.java', ['int[] values = new int[3]'])
            for Ime, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                stroj.Naredba('java ' + Ime, [문구, 'Exit: 1'])
                stroj.Naredba('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return stroj.LOG_zapis.decode('utf-8', 'replace')
        finally:
            stroj.Zatvori()


if __name__ == '__main__':
    rastavljati_VALUE = argparse.ArgumentParser()
    rastavljati_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumenti = rastavljati_VALUE.parse_args()
    REZULTAT = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argumenti.boot == 'both' else (Argumenti.boot,))}
    REZULTAT['import'] = 적재시험()
    (Položaj / 'build/자바시험.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2) + '\n')
