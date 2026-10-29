#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Provést_příkaz, selhání_HODNOTA/zdroj_HODNOTA mez_HODNOTA zkoušky."""
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
from test_uživatel_síť import virtuální_počítač, pozice


def úprava_HODNOTA(počítač, Název, Obsah_HODNOTA, Store_HODNOTA=True):
    Spustit_2 = len(počítač.LOGZ_ZÁZNAM)
    počítač.직렬.sendall(('edit ' + Název + '\n').encode())
    počítač.čekací_stav('...> ', Spustit_2)
    for vstupní_řádek in Obsah_HODNOTA.splitlines():
        assert len(vstupní_řádek) <= 128
        Spustit_2 = len(počítač.LOGZ_ZÁZNAM)
        počítač.직렬.sendall((vstupní_řádek + '\n').encode())
        počítač.čekací_stav('...> ', Spustit_2)
    Spustit_2 = len(počítač.LOGZ_ZÁZNAM)
    počítač.직렬.sendall(b'.save\n' if Store_HODNOTA else b'.cancel\n')
    VÝSLEDEK = počítač.čekací_stav('jkoros> ', Spustit_2)
    assert ('Saved:' if Store_HODNOTA else 'Cancelled; original preserved') in VÝSLEDEK, VÝSLEDEK


def Soubor_ODKAZ():
    VÝSLEDEK = subprocess.check_output(['nm', '-n', str(pozice / 'build/kernel.elf')], universal_newlines=True)
    for vstupní_řádek in VÝSLEDEK.splitlines():
        if vstupní_řádek.endswith(' ram_files'):
            return int(vstupní_řádek.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def host_Soubor(počítač, přihrádka_HODNOTA, Velikost, cesta_2):
    # zkoušky VM의 메모리에서 skutečný_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    Adresa = Soubor_ODKAZ() + přihrádka_HODNOTA * 16384
    počítač.monitor_HODNOTA.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(Adresa, Velikost, cesta_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if cesta_2.exists() and cesta_2.stat().st_size == Velikost:
            return cesta_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def testovací_běh(Druh_HODNOTA):
    počítač = virtuální_počítač(pozice / ('build/kernel.elf' if Druh_HODNOTA == 'elf' else 'build/kernel.iso'), Druh_HODNOTA, síť_HODNOTA=False)
    VÝSLEDEK = {}
    try:
        počítač.příkaz('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        počítač.příkaz('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        počítač.příkaz('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        počítač.příkaz('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        počítač.příkaz('java Missing', ['cannot read class: -2', 'Exit: 1'])
        počítač.příkaz('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        počítač.příkaz('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Obsah_HODNOTA = '''public class Calc {
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
        úprava_HODNOTA(počítač, 'Calc.java', Obsah_HODNOTA)
        počítač.příkaz('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        výstupní_pozice = počítač.příkaz('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        VÝSLEDEK['guest_output'] = výstupní_pozice
        položka_Seznam = počítač.příkaz('ls', ['Calc.class'])
        Velikost = int(re.search(r'Calc\.class\s+(\d+) bytes', položka_Seznam).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Adresář_HODNOTA:
            cesta_2 = Path(Adresář_HODNOTA) / 'Calc.class'
            data = host_Soubor(počítač, 3, Velikost, cesta_2)
            skutečný_data = subprocess.check_output(['java', '-Xverify:all', '-cp', Adresář_HODNOTA, 'Calc', '6', 'guest'], universal_newlines=True)
            assert skutečný_data.splitlines() == 기대, skutečný_data
            VÝSLEDEK['class_sha256'] = hashlib.sha256(data).hexdigest()
            VÝSLEDEK['openjdk_output'] = skutečný_data
        # 실패한 úprava_HODNOTA/컴파일은 기존 class를 보존한다.
        úprava_HODNOTA(počítač, 'Calc.java', 'not Java at all', Store_HODNOTA=False)
        počítač.příkaz('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for neplatný_KV in [
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
            úprava_HODNOTA(počítač, 'Calc.java', neplatný_KV)
            počítač.příkaz('javac Calc.java', ['javac error:', 'Exit: 1'])
            počítač.příkaz('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_HODNOTA 실행은 uživatelský_prostor halda_HODNOTA/프레임을 매번 초기화한다.
        for číslo in range(12):
            počítač.příkaz('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        počítač.příkaz('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        počítač.příkaz('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        úprava_HODNOTA(počítač, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        počítač.příkaz('javac Calc.java', ['Compiled:', 'Exit: 0'])
        počítač.příkaz('java Calc', ['instruction limit', 'Exit: 1'])
        počítač.příkaz('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        úprava_HODNOTA(počítač, 'Bad.class', 'garbage')
        počítač.příkaz('java Bad', ['JVM error:', 'Exit: 1'])
        počítač.příkaz('rm Bad.class', ['Removed'])
        počítač.příkaz('java Bad', ['cannot read class: -2'])
        # úprava_HODNOTA 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Spustit_2 = len(počítač.LOGZ_ZÁZNAM)
        počítač.직렬.sendall(b'edit Hello.java\n')
        počítač.čekací_stav('...> ', Spustit_2)
        Spustit_2 = len(počítač.LOGZ_ZÁZNAM)
        počítač.직렬.sendall(b'x' * 129 + b'\n')
        počítač.čekací_stav('...> ', Spustit_2)
        počítač.příkaz('.save', ['Too much input; original preserved'])
        počítač.příkaz('javac Hello.java', ['Compiled:', 'Exit: 0'])
        úprava_HODNOTA(počítač, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for číslo in range(3):
            úprava_HODNOTA(počítač, 'f' + str(číslo), 'occupied')
        počítač.příkaz('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        počítač.příkaz('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in počítač.LOGZ_ZÁZNAM.decode('utf-8', 'replace')
        VÝSLEDEK['serial'] = počítač.LOGZ_ZÁZNAM.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(Druh_HODNOTA))
        return VÝSLEDEK
    finally:
        počítač.Zavřené()


def 주코드(data):
    """손상 시험용 main Code의 skutečný_data název_souboru 오프셋/길이만 읽는다."""
    pozice_HODNOTA = 8
    def 짧():
        nonlocal pozice_HODNOTA
        HODNOTA = struct.unpack_from('>H', data, pozice_HODNOTA)[0]
        pozice_HODNOTA += 2
        return HODNOTA
    def 정():
        nonlocal pozice_HODNOTA
        HODNOTA = struct.unpack_from('>I', data, pozice_HODNOTA)[0]
        pozice_HODNOTA += 4
        return HODNOTA
    문자들 = {}
    for číslo in range(1, 짧()):
        Druh_HODNOTA = data[pozice_HODNOTA]
        pozice_HODNOTA += 1
        if Druh_HODNOTA == 1:
            délka_HODNOTA = 짧()
            문자들[číslo] = data[pozice_HODNOTA:pozice_HODNOTA + délka_HODNOTA]
            pozice_HODNOTA += délka_HODNOTA
        elif Druh_HODNOTA in (7, 8): pozice_HODNOTA += 2
        elif Druh_HODNOTA in (3, 9, 10, 12): pozice_HODNOTA += 4
        else: raise AssertionError(Druh_HODNOTA)
    pozice_HODNOTA += 6
    zboží_POČET = 짧()
    pozice_HODNOTA += zboží_POČET * 2
    assert 짧() == 0
    for číslo in range(짧()):
        짧()
        Název = 짧()
        짧()
        for číslo in range(짧()):
            hodnota_atributu = 짧()
            Velikost = 정()
            if 문자들[Název] == b'main' and 문자들[hodnota_atributu] == b'Code':
                return pozice_HODNOTA + 8, struct.unpack_from('>I', data, pozice_HODNOTA + 4)[0]
            pozice_HODNOTA += Velikost
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Adresář_HODNOTA = Path(임시)
        (Adresář_HODNOTA / 'build').mkdir()
        zdrojový_soubor = Adresář_HODNOTA / 'Imported.java'
        zdrojový_soubor.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(zdrojový_soubor)], check=True)
        원본 = (Adresář_HODNOTA / 'Imported.class').read_bytes()
        KÓD_HODNOTA, délka_HODNOTA = 주코드(원본)
        varianta_HODNOTA = {}
        data = bytearray(원본); data[0] = 0; varianta_HODNOTA['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; varianta_HODNOTA['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; varianta_HODNOTA['BadPool'] = data
        data = bytearray(원본); data[KÓD_HODNOTA:KÓD_HODNOTA + délka_HODNOTA] = bytes(délka_HODNOTA)
        data[KÓD_HODNOTA:KÓD_HODNOTA + 3] = b'\xa7\x00\x01'; data[KÓD_HODNOTA + délka_HODNOTA - 1] = 177; varianta_HODNOTA['BadJump'] = data
        data = bytearray(원본); data[KÓD_HODNOTA:KÓD_HODNOTA + délka_HODNOTA] = bytes(délka_HODNOTA)
        data[KÓD_HODNOTA] = 87; data[KÓD_HODNOTA + délka_HODNOTA - 1] = 177; varianta_HODNOTA['BadStack'] = data
        # Název 검사를 통과시켜 skutečný_data Provést_příkaz 중의 operand_Štos 오류까지 검사한다.
        varianta_HODNOTA['BadStack'] = varianta_HODNOTA['BadStack'].replace(b'Imported', b'BadStack')
        položka_HODNOTA = ['Imported.class=' + str(Adresář_HODNOTA / 'Imported.class'), 'Imported.java=' + str(zdrojový_soubor)]
        for Název, data in varianta_HODNOTA.items():
            cesta_2 = Adresář_HODNOTA / (Název + '.class'); cesta_2.write_bytes(data)
            položka_HODNOTA.append(Název + '.class=' + str(cesta_2))
        Skupina_HODNOTA = Adresář_HODNOTA / 'build/java-files.bin'
        subprocess.run([sys.executable, str(pozice / 'nástroje/자바파일묶기.py'), '-o', str(Skupina_HODNOTA)] + položka_HODNOTA, check=True)
        subprocess.run(['as', '--32', '-o', str(Adresář_HODNOTA / 'user.o'), str(pozice / 'spuštění_stroje/uživatelský_prostor.s')], cwd=str(Adresář_HODNOTA), check=True)
        jádro_HODNOTA = Adresář_HODNOTA / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozice / 'spuštění_stroje/rozvržení_spojování.ld'), '-o', str(jádro_HODNOTA),
                        str(pozice / 'build/boot.o'), str(pozice / 'build/java.o'), str(Adresář_HODNOTA / 'user.o'), str(pozice / 'build/apps.o')], check=True)
        počítač = virtuální_počítač(jádro_HODNOTA, síť_HODNOTA=False)
        try:
            počítač.příkaz('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            počítač.příkaz('cat Imported.java', ['int[] values = new int[3]'])
            for Název, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                počítač.příkaz('java ' + Název, [문구, 'Exit: 1'])
                počítač.příkaz('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return počítač.LOGZ_ZÁZNAM.decode('utf-8', 'replace')
        finally:
            počítač.Zavřené()


if __name__ == '__main__':
    parsovat_HODNOTA = argparse.ArgumentParser()
    parsovat_HODNOTA.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argumenty = parsovat_HODNOTA.parse_args()
    VÝSLEDEK = {Druh_HODNOTA: testovací_běh(Druh_HODNOTA) for Druh_HODNOTA in (('elf', 'iso') if argumenty.boot == 'both' else (argumenty.boot,))}
    VÝSLEDEK['import'] = 적재시험()
    (pozice / 'build/자바시험.json').write_text(json.dumps(VÝSLEDEK, ensure_ascii=False, indent=2) + '\n')
