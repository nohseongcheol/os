#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Izvedi_ukaz, napaka_VALUE/vir_VALUE 경계 시험."""
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
from preskusiti_uporabnik_mreža import navidezni_računalnik, Položaj


def Uredi_VALUE(računalnik, Ime, vsebina_VALUE, Store_VALUE=True):
    Zaženi = len(računalnik.LOG_zapis)
    računalnik.직렬.sendall(('edit ' + Ime + '\n').encode())
    računalnik.čakalno_stanje('...> ', Zaženi)
    for Črtni in vsebina_VALUE.splitlines():
        assert len(Črtni) <= 128
        Zaženi = len(računalnik.LOG_zapis)
        računalnik.직렬.sendall((Črtni + '\n').encode())
        računalnik.čakalno_stanje('...> ', Zaženi)
    Zaženi = len(računalnik.LOG_zapis)
    računalnik.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    REZULTAT = računalnik.čakalno_stanje('jkoros> ', Zaženi)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in REZULTAT, REZULTAT


def Datoteka_naslov():
    REZULTAT = subprocess.check_output(['nm', '-n', str(Položaj / 'build/kernel.elf')], universal_newlines=True)
    for Črtni in REZULTAT.splitlines():
        if Črtni.endswith(' ram_files'):
            return int(Črtni.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gost_Datoteka(računalnik, 슬롯, Velikost, POT):
    # 시험 VM의 메모리에서 dejanski_podatki 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    naslov = Datoteka_naslov() + 슬롯 * 16384
    računalnik.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(naslov, Velikost, POT)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if POT.exists() and POT.stat().st_size == Velikost:
            return POT.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def preskusiti_izvajati(종류):
    računalnik = navidezni_računalnik(Položaj / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, mreža_VALUE=False)
    REZULTAT = {}
    try:
        računalnik.Ukaz('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        računalnik.Ukaz('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        računalnik.Ukaz('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        računalnik.Ukaz('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        računalnik.Ukaz('java Missing', ['cannot read class: -2', 'Exit: 1'])
        računalnik.Ukaz('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        računalnik.Ukaz('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        vsebina_VALUE = '''public class Calc {
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
        Uredi_VALUE(računalnik, 'Calc.java', vsebina_VALUE)
        računalnik.Ukaz('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Izpis = računalnik.Ukaz('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        REZULTAT['guest_output'] = Izpis
        vnos_Seznam = računalnik.Ukaz('ls', ['Calc.class'])
        Velikost = int(re.search(r'Calc\.class\s+(\d+) bytes', vnos_Seznam).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Imenik_VALUE:
            POT = Path(Imenik_VALUE) / 'Calc.class'
            podatki = gost_Datoteka(računalnik, 3, Velikost, POT)
            dejanski_podatki = subprocess.check_output(['java', '-Xverify:all', '-cp', Imenik_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert dejanski_podatki.splitlines() == 기대, dejanski_podatki
            REZULTAT['class_sha256'] = hashlib.sha256(podatki).hexdigest()
            REZULTAT['openjdk_output'] = dejanski_podatki
        # 실패한 Uredi_VALUE/컴파일은 기존 class를 보존한다.
        Uredi_VALUE(računalnik, 'Calc.java', 'not Java at all', Store_VALUE=False)
        računalnik.Ukaz('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for neveljaven_KR in [
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
            Uredi_VALUE(računalnik, 'Calc.java', neveljaven_KR)
            računalnik.Ukaz('javac Calc.java', ['javac error:', 'Exit: 1'])
            računalnik.Ukaz('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 uporabnik kopica_VALUE/프레임을 매번 초기화한다.
        for 수 in range(12):
            računalnik.Ukaz('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        računalnik.Ukaz('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        računalnik.Ukaz('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Uredi_VALUE(računalnik, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        računalnik.Ukaz('javac Calc.java', ['Compiled:', 'Exit: 0'])
        računalnik.Ukaz('java Calc', ['instruction limit', 'Exit: 1'])
        računalnik.Ukaz('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Uredi_VALUE(računalnik, 'Bad.class', 'garbage')
        računalnik.Ukaz('java Bad', ['JVM error:', 'Exit: 1'])
        računalnik.Ukaz('rm Bad.class', ['Removed'])
        računalnik.Ukaz('java Bad', ['cannot read class: -2'])
        # Uredi_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Zaženi = len(računalnik.LOG_zapis)
        računalnik.직렬.sendall(b'edit Hello.java\n')
        računalnik.čakalno_stanje('...> ', Zaženi)
        Zaženi = len(računalnik.LOG_zapis)
        računalnik.직렬.sendall(b'x' * 129 + b'\n')
        računalnik.čakalno_stanje('...> ', Zaženi)
        računalnik.Ukaz('.save', ['Too much input; original preserved'])
        računalnik.Ukaz('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Uredi_VALUE(računalnik, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Uredi_VALUE(računalnik, 'f' + str(수), 'occupied')
        računalnik.Ukaz('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        računalnik.Ukaz('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in računalnik.LOG_zapis.decode('utf-8', 'replace')
        REZULTAT['serial'] = računalnik.LOG_zapis.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return REZULTAT
    finally:
        računalnik.Zapri()


def 주코드(podatki):
    """손상 시험용 main Code의 dejanski_podatki Datoteka 오프셋/길이만 읽는다."""
    položaj_VALUE = 8
    def 짧():
        nonlocal položaj_VALUE
        VALUE = struct.unpack_from('>H', podatki, položaj_VALUE)[0]
        položaj_VALUE += 2
        return VALUE
    def 정():
        nonlocal položaj_VALUE
        VALUE = struct.unpack_from('>I', podatki, položaj_VALUE)[0]
        položaj_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = podatki[položaj_VALUE]
        položaj_VALUE += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[수] = podatki[položaj_VALUE:položaj_VALUE + 길이]
            položaj_VALUE += 길이
        elif 종류 in (7, 8): položaj_VALUE += 2
        elif 종류 in (3, 9, 10, 12): položaj_VALUE += 4
        else: raise AssertionError(종류)
    položaj_VALUE += 6
    element_COUNT = 짧()
    položaj_VALUE += element_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Ime = 짧()
        짧()
        for 수 in range(짧()):
            atribut_VALUE = 짧()
            Velikost = 정()
            if 문자들[Ime] == b'main' and 문자들[atribut_VALUE] == b'Code':
                return položaj_VALUE + 8, struct.unpack_from('>I', podatki, položaj_VALUE + 4)[0]
            položaj_VALUE += Velikost
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Imenik_VALUE = Path(임시)
        (Imenik_VALUE / 'build').mkdir()
        VIR = Imenik_VALUE / 'Imported.java'
        VIR.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(VIR)], check=True)
        원본 = (Imenik_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, 길이 = 주코드(원본)
        변형 = {}
        podatki = bytearray(원본); podatki[0] = 0; 변형['BadMagic'] = podatki
        podatki = bytearray(원본); podatki[7] = 61; 변형['BadVer'] = podatki
        podatki = bytearray(원본); podatki[8:10] = b'\xff\xff'; 변형['BadPool'] = podatki
        podatki = bytearray(원본); podatki[CODE_VALUE:CODE_VALUE + 길이] = bytes(길이)
        podatki[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; podatki[CODE_VALUE + 길이 - 1] = 177; 변형['BadJump'] = podatki
        podatki = bytearray(원본); podatki[CODE_VALUE:CODE_VALUE + 길이] = bytes(길이)
        podatki[CODE_VALUE] = 87; podatki[CODE_VALUE + 길이 - 1] = 177; 변형['BadStack'] = podatki
        # Ime 검사를 통과시켜 dejanski_podatki Izvedi_ukaz 중의 operand_Sklad 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        vnos_VALUE = ['Imported.class=' + str(Imenik_VALUE / 'Imported.class'), 'Imported.java=' + str(VIR)]
        for Ime, podatki in 변형.items():
            POT = Imenik_VALUE / (Ime + '.class'); POT.write_bytes(podatki)
            vnos_VALUE.append(Ime + '.class=' + str(POT))
        Skupina_VALUE = Imenik_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Položaj / 'Orodja/자바파일묶기.py'), '-o', str(Skupina_VALUE)] + vnos_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Imenik_VALUE / 'user.o'), str(Položaj / '부팅/uporabnik.s')], cwd=str(Imenik_VALUE), check=True)
        jedro_VALUE = Imenik_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Položaj / '부팅/Povezava_Krmarjenje.ld'), '-o', str(jedro_VALUE),
                        str(Položaj / 'build/boot.o'), str(Položaj / 'build/java.o'), str(Imenik_VALUE / 'user.o'), str(Položaj / 'build/apps.o')], check=True)
        računalnik = navidezni_računalnik(jedro_VALUE, mreža_VALUE=False)
        try:
            računalnik.Ukaz('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            računalnik.Ukaz('cat Imported.java', ['int[] values = new int[3]'])
            for Ime, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                računalnik.Ukaz('java ' + Ime, [문구, 'Exit: 1'])
                računalnik.Ukaz('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return računalnik.LOG_zapis.decode('utf-8', 'replace')
        finally:
            računalnik.Zapri()


if __name__ == '__main__':
    razčlenjevati_VALUE = argparse.ArgumentParser()
    razčlenjevati_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumenti = razčlenjevati_VALUE.parse_args()
    REZULTAT = {종류: preskusiti_izvajati(종류) for 종류 in (('elf', 'iso') if Argumenti.boot == 'both' else (Argumenti.boot,))}
    REZULTAT['import'] = 적재시험()
    (Položaj / 'build/자바시험.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2) + '\n')
