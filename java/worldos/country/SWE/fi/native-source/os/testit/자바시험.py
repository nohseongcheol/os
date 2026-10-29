#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Suorita_komento, virhe_ARVO/resurssi_ARVO rajattu_alue_ARVO testit."""
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
from testi_käyttäjä_verkko import VM, paikka


def muutos_ARVO(kone, Nimi, Sisältö_ARVO, Store_ARVO=True):
    Suorita_2 = len(kone.LOG_TIETUE)
    kone.직렬.sendall(('edit ' + Nimi + '\n').encode())
    kone.odotustila('...> ', Suorita_2)
    for syöterivi in Sisältö_ARVO.splitlines():
        assert len(syöterivi) <= 128
        Suorita_2 = len(kone.LOG_TIETUE)
        kone.직렬.sendall((syöterivi + '\n').encode())
        kone.odotustila('...> ', Suorita_2)
    Suorita_2 = len(kone.LOG_TIETUE)
    kone.직렬.sendall(b'.save\n' if Store_ARVO else b'.cancel\n')
    TULOS = kone.odotustila('jkoros> ', Suorita_2)
    assert ('Saved:' if Store_ARVO else 'Cancelled; original preserved') in TULOS, TULOS


def Tiedosto_OSOITE():
    TULOS = subprocess.check_output(['nm', '-n', str(paikka / 'build/kernel.elf')], universal_newlines=True)
    for syöterivi in TULOS.splitlines():
        if syöterivi.endswith(' ram_files'):
            return int(syöterivi.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def vieras_Tiedosto(kone, paikka_ARVO, Koko, polku_2):
    # testit VM의 메모리에서 todellinen_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    OSOITE = Tiedosto_OSOITE() + paikka_ARVO * 16384
    kone.näyttö_ARVO.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(OSOITE, Koko, polku_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if polku_2.exists() and polku_2.stat().st_size == Koko:
            return polku_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def testi_suorittaa(종류):
    kone = VM(paikka / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, verkko_ARVO=False)
    TULOS = {}
    try:
        kone.komento('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        kone.komento('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        kone.komento('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        kone.komento('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        kone.komento('java Missing', ['cannot read class: -2', 'Exit: 1'])
        kone.komento('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        kone.komento('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Sisältö_ARVO = '''public class Calc {
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
        muutos_ARVO(kone, 'Calc.java', Sisältö_ARVO)
        kone.komento('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        tulostuspaikka = kone.komento('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        TULOS['guest_output'] = tulostuspaikka
        merkintä_luettelo = kone.komento('ls', ['Calc.class'])
        Koko = int(re.search(r'Calc\.class\s+(\d+) bytes', merkintä_luettelo).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Directory_ARVO:
            polku_2 = Path(Directory_ARVO) / 'Calc.class'
            data = vieras_Tiedosto(kone, 3, Koko, polku_2)
            todellinen_data = subprocess.check_output(['java', '-Xverify:all', '-cp', Directory_ARVO, 'Calc', '6', 'guest'], universal_newlines=True)
            assert todellinen_data.splitlines() == 기대, todellinen_data
            TULOS['class_sha256'] = hashlib.sha256(data).hexdigest()
            TULOS['openjdk_output'] = todellinen_data
        # 실패한 muutos_ARVO/컴파일은 기존 class를 보존한다.
        muutos_ARVO(kone, 'Calc.java', 'not Java at all', Store_ARVO=False)
        kone.komento('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for pätemätön_KR in [
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
            muutos_ARVO(kone, 'Calc.java', pätemätön_KR)
            kone.komento('javac Calc.java', ['javac error:', 'Exit: 1'])
            kone.komento('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprintti_ARVO 실행은 käyttäjätila keko_ARVO/프레임을 매번 초기화한다.
        for numero in range(12):
            kone.komento('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        kone.komento('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        kone.komento('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        muutos_ARVO(kone, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        kone.komento('javac Calc.java', ['Compiled:', 'Exit: 0'])
        kone.komento('java Calc', ['instruction limit', 'Exit: 1'])
        kone.komento('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        muutos_ARVO(kone, 'Bad.class', 'garbage')
        kone.komento('java Bad', ['JVM error:', 'Exit: 1'])
        kone.komento('rm Bad.class', ['Removed'])
        kone.komento('java Bad', ['cannot read class: -2'])
        # muutos_ARVO 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Suorita_2 = len(kone.LOG_TIETUE)
        kone.직렬.sendall(b'edit Hello.java\n')
        kone.odotustila('...> ', Suorita_2)
        Suorita_2 = len(kone.LOG_TIETUE)
        kone.직렬.sendall(b'x' * 129 + b'\n')
        kone.odotustila('...> ', Suorita_2)
        kone.komento('.save', ['Too much input; original preserved'])
        kone.komento('javac Hello.java', ['Compiled:', 'Exit: 0'])
        muutos_ARVO(kone, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for numero in range(3):
            muutos_ARVO(kone, 'f' + str(numero), 'occupied')
        kone.komento('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        kone.komento('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in kone.LOG_TIETUE.decode('utf-8', 'replace')
        TULOS['serial'] = kone.LOG_TIETUE.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return TULOS
    finally:
        kone.Sulje()


def 주코드(data):
    """손상 시험용 main Code의 todellinen_data tiedoston_nimi 오프셋/길이만 읽는다."""
    toimi_ARVO = 8
    def 짧():
        nonlocal toimi_ARVO
        ARVO = struct.unpack_from('>H', data, toimi_ARVO)[0]
        toimi_ARVO += 2
        return ARVO
    def lukea_etumerkitön_kokonaisluku():
        nonlocal toimi_ARVO
        ARVO = struct.unpack_from('>I', data, toimi_ARVO)[0]
        toimi_ARVO += 4
        return ARVO
    문자들 = {}
    for numero in range(1, 짧()):
        종류 = data[toimi_ARVO]
        toimi_ARVO += 1
        if 종류 == 1:
            kesto_ARVO = 짧()
            문자들[numero] = data[toimi_ARVO:toimi_ARVO + kesto_ARVO]
            toimi_ARVO += kesto_ARVO
        elif 종류 in (7, 8): toimi_ARVO += 2
        elif 종류 in (3, 9, 10, 12): toimi_ARVO += 4
        else: raise AssertionError(종류)
    toimi_ARVO += 6
    kohde_LASKE = 짧()
    toimi_ARVO += kohde_LASKE * 2
    assert 짧() == 0
    for numero in range(짧()):
        짧()
        Nimi = 짧()
        짧()
        for numero in range(짧()):
            määritteen_arvo = 짧()
            Koko = lukea_etumerkitön_kokonaisluku()
            if 문자들[Nimi] == b'main' and 문자들[määritteen_arvo] == b'Code':
                return toimi_ARVO + 8, struct.unpack_from('>I', data, toimi_ARVO + 4)[0]
            toimi_ARVO += Koko
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Directory_ARVO = Path(임시)
        (Directory_ARVO / 'build').mkdir()
        lähdetiedosto = Directory_ARVO / 'Imported.java'
        lähdetiedosto.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(lähdetiedosto)], check=True)
        원본 = (Directory_ARVO / 'Imported.class').read_bytes()
        KOODI_ARVO, kesto_ARVO = 주코드(원본)
        variaatio_ARVO = {}
        data = bytearray(원본); data[0] = 0; variaatio_ARVO['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; variaatio_ARVO['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; variaatio_ARVO['BadPool'] = data
        data = bytearray(원본); data[KOODI_ARVO:KOODI_ARVO + kesto_ARVO] = bytes(kesto_ARVO)
        data[KOODI_ARVO:KOODI_ARVO + 3] = b'\xa7\x00\x01'; data[KOODI_ARVO + kesto_ARVO - 1] = 177; variaatio_ARVO['BadJump'] = data
        data = bytearray(원본); data[KOODI_ARVO:KOODI_ARVO + kesto_ARVO] = bytes(kesto_ARVO)
        data[KOODI_ARVO] = 87; data[KOODI_ARVO + kesto_ARVO - 1] = 177; variaatio_ARVO['BadStack'] = data
        # Nimi 검사를 통과시켜 todellinen_data Suorita_komento 중의 operandi_Pino 오류까지 검사한다.
        variaatio_ARVO['BadStack'] = variaatio_ARVO['BadStack'].replace(b'Imported', b'BadStack')
        merkintä_ARVO_962f286b = ['Imported.class=' + str(Directory_ARVO / 'Imported.class'), 'Imported.java=' + str(lähdetiedosto)]
        for Nimi, data in variaatio_ARVO.items():
            polku_2 = Directory_ARVO / (Nimi + '.class'); polku_2.write_bytes(data)
            merkintä_ARVO_962f286b.append(Nimi + '.class=' + str(polku_2))
        Ryhmä_ARVO = Directory_ARVO / 'build/java-files.bin'
        subprocess.run([sys.executable, str(paikka / 'työkalut/자바파일묶기.py'), '-o', str(Ryhmä_ARVO)] + merkintä_ARVO_962f286b, check=True)
        subprocess.run(['as', '--32', '-o', str(Directory_ARVO / 'user.o'), str(paikka / 'koneen_käynnistys/käyttäjätila.s')], cwd=str(Directory_ARVO), check=True)
        ydin_ARVO = Directory_ARVO / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(paikka / 'koneen_käynnistys/linkitysasettelu.ld'), '-o', str(ydin_ARVO),
                        str(paikka / 'build/boot.o'), str(paikka / 'build/java.o'), str(Directory_ARVO / 'user.o'), str(paikka / 'build/apps.o')], check=True)
        kone = VM(ydin_ARVO, verkko_ARVO=False)
        try:
            kone.komento('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            kone.komento('cat Imported.java', ['int[] values = new int[3]'])
            for Nimi, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                kone.komento('java ' + Nimi, [문구, 'Exit: 1'])
                kone.komento('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return kone.LOG_TIETUE.decode('utf-8', 'replace')
        finally:
            kone.Sulje()


if __name__ == '__main__':
    jäsentää_ARVO = argparse.ArgumentParser()
    jäsentää_ARVO.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argumentit = jäsentää_ARVO.parse_args()
    TULOS = {종류: testi_suorittaa(종류) for 종류 in (('elf', 'iso') if argumentit.boot == 'both' else (argumentit.boot,))}
    TULOS['import'] = 적재시험()
    (paikka / 'build/자바시험.json').write_text(json.dumps(TULOS, ensure_ascii=False, indent=2) + '\n')
