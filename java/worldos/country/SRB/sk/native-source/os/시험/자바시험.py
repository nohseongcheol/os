#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Vykonať_príkaz, zlyhanie_VALUE/zdroj_VALUE 경계 시험."""
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
from test_používateľ_sieť import virtuálny_počítač, Pozícia


def úprava_VALUE(počítač_5eb260fa, Názov, obsah_VALUE, Store_VALUE=True):
    Spustiť_2 = len(počítač_5eb260fa.LOG_RECORD)
    počítač_5eb260fa.직렬.sendall(('edit ' + Názov + '\n').encode())
    počítač_5eb260fa.stav_čakania('...> ', Spustiť_2)
    for riadok in obsah_VALUE.splitlines():
        assert len(riadok) <= 128
        Spustiť_2 = len(počítač_5eb260fa.LOG_RECORD)
        počítač_5eb260fa.직렬.sendall((riadok + '\n').encode())
        počítač_5eb260fa.stav_čakania('...> ', Spustiť_2)
    Spustiť_2 = len(počítač_5eb260fa.LOG_RECORD)
    počítač_5eb260fa.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    KR = počítač_5eb260fa.stav_čakania('jkoros> ', Spustiť_2)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in KR, KR


def Súbor_adresa():
    KR = subprocess.check_output(['nm', '-n', str(Pozícia / 'build/kernel.elf')], universal_newlines=True)
    for riadok in KR.splitlines():
        if riadok.endswith(' ram_files'):
            return int(riadok.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def hosť_Súbor(počítač_5eb260fa, 슬롯, Veľkosť, Cesta):
    # 시험 VM의 메모리에서 skutočný_údaje 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    adresa = Súbor_adresa() + 슬롯 * 16384
    počítač_5eb260fa.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(adresa, Veľkosť, Cesta)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Cesta.exists() and Cesta.stat().st_size == Veľkosť:
            return Cesta.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def test_spustiť(종류):
    počítač_5eb260fa = virtuálny_počítač(Pozícia / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, sieť_VALUE=False)
    KR = {}
    try:
        počítač_5eb260fa.Príkaz('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        počítač_5eb260fa.Príkaz('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        počítač_5eb260fa.Príkaz('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        počítač_5eb260fa.Príkaz('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        počítač_5eb260fa.Príkaz('java Missing', ['cannot read class: -2', 'Exit: 1'])
        počítač_5eb260fa.Príkaz('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        počítač_5eb260fa.Príkaz('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        obsah_VALUE = '''public class Calc {
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
        úprava_VALUE(počítač_5eb260fa, 'Calc.java', obsah_VALUE)
        počítač_5eb260fa.Príkaz('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Výstup = počítač_5eb260fa.Príkaz('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        KR['guest_output'] = Výstup
        položka_Zoznam = počítač_5eb260fa.Príkaz('ls', ['Calc.class'])
        Veľkosť = int(re.search(r'Calc\.class\s+(\d+) bytes', položka_Zoznam).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Adresár_VALUE:
            Cesta = Path(Adresár_VALUE) / 'Calc.class'
            údaje = hosť_Súbor(počítač_5eb260fa, 3, Veľkosť, Cesta)
            skutočný_údaje = subprocess.check_output(['java', '-Xverify:all', '-cp', Adresár_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert skutočný_údaje.splitlines() == 기대, skutočný_údaje
            KR['class_sha256'] = hashlib.sha256(údaje).hexdigest()
            KR['openjdk_output'] = skutočný_údaje
        # 실패한 úprava_VALUE/컴파일은 기존 class를 보존한다.
        úprava_VALUE(počítač_5eb260fa, 'Calc.java', 'not Java at all', Store_VALUE=False)
        počítač_5eb260fa.Príkaz('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for neplatné_KR in [
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
            úprava_VALUE(počítač_5eb260fa, 'Calc.java', neplatné_KR)
            počítač_5eb260fa.Príkaz('javac Calc.java', ['javac error:', 'Exit: 1'])
            počítač_5eb260fa.Príkaz('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # šprint_VALUE 실행은 používateľ halda_VALUE/프레임을 매번 초기화한다.
        for 수 in range(12):
            počítač_5eb260fa.Príkaz('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        počítač_5eb260fa.Príkaz('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        počítač_5eb260fa.Príkaz('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        úprava_VALUE(počítač_5eb260fa, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        počítač_5eb260fa.Príkaz('javac Calc.java', ['Compiled:', 'Exit: 0'])
        počítač_5eb260fa.Príkaz('java Calc', ['instruction limit', 'Exit: 1'])
        počítač_5eb260fa.Príkaz('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        úprava_VALUE(počítač_5eb260fa, 'Bad.class', 'garbage')
        počítač_5eb260fa.Príkaz('java Bad', ['JVM error:', 'Exit: 1'])
        počítač_5eb260fa.Príkaz('rm Bad.class', ['Removed'])
        počítač_5eb260fa.Príkaz('java Bad', ['cannot read class: -2'])
        # úprava_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Spustiť_2 = len(počítač_5eb260fa.LOG_RECORD)
        počítač_5eb260fa.직렬.sendall(b'edit Hello.java\n')
        počítač_5eb260fa.stav_čakania('...> ', Spustiť_2)
        Spustiť_2 = len(počítač_5eb260fa.LOG_RECORD)
        počítač_5eb260fa.직렬.sendall(b'x' * 129 + b'\n')
        počítač_5eb260fa.stav_čakania('...> ', Spustiť_2)
        počítač_5eb260fa.Príkaz('.save', ['Too much input; original preserved'])
        počítač_5eb260fa.Príkaz('javac Hello.java', ['Compiled:', 'Exit: 0'])
        úprava_VALUE(počítač_5eb260fa, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            úprava_VALUE(počítač_5eb260fa, 'f' + str(수), 'occupied')
        počítač_5eb260fa.Príkaz('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        počítač_5eb260fa.Príkaz('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in počítač_5eb260fa.LOG_RECORD.decode('utf-8', 'replace')
        KR['serial'] = počítač_5eb260fa.LOG_RECORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return KR
    finally:
        počítač_5eb260fa.Zatvoriť()


def 주코드(údaje):
    """손상 시험용 main Code의 skutočný_údaje Súbor 오프셋/길이만 읽는다."""
    pozícia_VALUE = 8
    def 짧():
        nonlocal pozícia_VALUE
        VALUE = struct.unpack_from('>H', údaje, pozícia_VALUE)[0]
        pozícia_VALUE += 2
        return VALUE
    def 정():
        nonlocal pozícia_VALUE
        VALUE = struct.unpack_from('>I', údaje, pozícia_VALUE)[0]
        pozícia_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = údaje[pozícia_VALUE]
        pozícia_VALUE += 1
        if 종류 == 1:
            dĺžka_VALUE = 짧()
            문자들[수] = údaje[pozícia_VALUE:pozícia_VALUE + dĺžka_VALUE]
            pozícia_VALUE += dĺžka_VALUE
        elif 종류 in (7, 8): pozícia_VALUE += 2
        elif 종류 in (3, 9, 10, 12): pozícia_VALUE += 4
        else: raise AssertionError(종류)
    pozícia_VALUE += 6
    položka_COUNT = 짧()
    pozícia_VALUE += položka_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Názov = 짧()
        짧()
        for 수 in range(짧()):
            atribút_VALUE = 짧()
            Veľkosť = 정()
            if 문자들[Názov] == b'main' and 문자들[atribút_VALUE] == b'Code':
                return pozícia_VALUE + 8, struct.unpack_from('>I', údaje, pozícia_VALUE + 4)[0]
            pozícia_VALUE += Veľkosť
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Adresár_VALUE = Path(임시)
        (Adresár_VALUE / 'build').mkdir()
        ZDROJ = Adresár_VALUE / 'Imported.java'
        ZDROJ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ZDROJ)], check=True)
        원본 = (Adresár_VALUE / 'Imported.class').read_bytes()
        kód_VALUE, dĺžka_VALUE = 주코드(원본)
        변형 = {}
        údaje = bytearray(원본); údaje[0] = 0; 변형['BadMagic'] = údaje
        údaje = bytearray(원본); údaje[7] = 61; 변형['BadVer'] = údaje
        údaje = bytearray(원본); údaje[8:10] = b'\xff\xff'; 변형['BadPool'] = údaje
        údaje = bytearray(원본); údaje[kód_VALUE:kód_VALUE + dĺžka_VALUE] = bytes(dĺžka_VALUE)
        údaje[kód_VALUE:kód_VALUE + 3] = b'\xa7\x00\x01'; údaje[kód_VALUE + dĺžka_VALUE - 1] = 177; 변형['BadJump'] = údaje
        údaje = bytearray(원본); údaje[kód_VALUE:kód_VALUE + dĺžka_VALUE] = bytes(dĺžka_VALUE)
        údaje[kód_VALUE] = 87; údaje[kód_VALUE + dĺžka_VALUE - 1] = 177; 변형['BadStack'] = údaje
        # Názov 검사를 통과시켜 skutočný_údaje Vykonať_príkaz 중의 operand_Vrstvy 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        položka_VALUE = ['Imported.class=' + str(Adresár_VALUE / 'Imported.class'), 'Imported.java=' + str(ZDROJ)]
        for Názov, údaje in 변형.items():
            Cesta = Adresár_VALUE / (Názov + '.class'); Cesta.write_bytes(údaje)
            položka_VALUE.append(Názov + '.class=' + str(Cesta))
        Skupina_VALUE = Adresár_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Pozícia / 'Nástroje/자바파일묶기.py'), '-o', str(Skupina_VALUE)] + položka_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Adresár_VALUE / 'user.o'), str(Pozícia / '부팅/používateľ.s')], cwd=str(Adresár_VALUE), check=True)
        jadro_VALUE = Adresár_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozícia / '부팅/odkaz_Navigácia.ld'), '-o', str(jadro_VALUE),
                        str(Pozícia / 'build/boot.o'), str(Pozícia / 'build/java.o'), str(Adresár_VALUE / 'user.o'), str(Pozícia / 'build/apps.o')], check=True)
        počítač_5eb260fa = virtuálny_počítač(jadro_VALUE, sieť_VALUE=False)
        try:
            počítač_5eb260fa.Príkaz('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            počítač_5eb260fa.Príkaz('cat Imported.java', ['int[] values = new int[3]'])
            for Názov, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                počítač_5eb260fa.Príkaz('java ' + Názov, [문구, 'Exit: 1'])
                počítač_5eb260fa.Príkaz('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return počítač_5eb260fa.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            počítač_5eb260fa.Zatvoriť()


if __name__ == '__main__':
    analyzovať_VALUE = argparse.ArgumentParser()
    analyzovať_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumenty = analyzovať_VALUE.parse_args()
    KR = {종류: test_spustiť(종류) for 종류 in (('elf', 'iso') if Argumenty.boot == 'both' else (Argumenty.boot,))}
    KR['import'] = 적재시험()
    (Pozícia / 'build/자바시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n')
