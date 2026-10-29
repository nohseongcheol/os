#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 köra_kommando, fel_värde/resurs_värde gräns_värde tester."""
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
from test_användare_nätverk import VM, position


def ändring_värde(dator, Namn, Innehåll_värde, Store_värde=True):
    Kör = len(dator.LOG_POST)
    dator.직렬.sendall(('edit ' + Namn + '\n').encode())
    dator.tillståndet_Vänta('...> ', Kör)
    for inmatningsrad in Innehåll_värde.splitlines():
        assert len(inmatningsrad) <= 128
        Kör = len(dator.LOG_POST)
        dator.직렬.sendall((inmatningsrad + '\n').encode())
        dator.tillståndet_Vänta('...> ', Kör)
    Kör = len(dator.LOG_POST)
    dator.직렬.sendall(b'.save\n' if Store_värde else b'.cancel\n')
    RESULTAT = dator.tillståndet_Vänta('jkoros> ', Kör)
    assert ('Saved:' if Store_värde else 'Cancelled; original preserved') in RESULTAT, RESULTAT


def fil_ADRESS():
    RESULTAT = subprocess.check_output(['nm', '-n', str(position / 'build/kernel.elf')], universal_newlines=True)
    for inmatningsrad in RESULTAT.splitlines():
        if inmatningsrad.endswith(' ram_files'):
            return int(inmatningsrad.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gäst_fil(dator, fack_värde, Storlek, sökväg_2):
    # tester VM의 메모리에서 verklig_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    Adress = fil_ADRESS() + fack_värde * 16384
    dator.övervaka_värde.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(Adress, Storlek, sökväg_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if sökväg_2.exists() and sökväg_2.stat().st_size == Storlek:
            return sökväg_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def test_köra(variant_värde):
    dator = VM(position / ('build/kernel.elf' if variant_värde == 'elf' else 'build/kernel.iso'), variant_värde, nätverk_värde=False)
    RESULTAT = {}
    try:
        dator.kommando('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        dator.kommando('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        dator.kommando('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        dator.kommando('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        dator.kommando('java Missing', ['cannot read class: -2', 'Exit: 1'])
        dator.kommando('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        dator.kommando('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Innehåll_värde = '''public class Calc {
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
        ändring_värde(dator, 'Calc.java', Innehåll_värde)
        dator.kommando('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        utmatningsposition = dator.kommando('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        RESULTAT['guest_output'] = utmatningsposition
        post_ange = dator.kommando('ls', ['Calc.class'])
        Storlek = int(re.search(r'Calc\.class\s+(\d+) bytes', post_ange).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Katalog_värde:
            sökväg_2 = Path(Katalog_värde) / 'Calc.class'
            data = gäst_fil(dator, 3, Storlek, sökväg_2)
            verklig_data = subprocess.check_output(['java', '-Xverify:all', '-cp', Katalog_värde, 'Calc', '6', 'guest'], universal_newlines=True)
            assert verklig_data.splitlines() == 기대, verklig_data
            RESULTAT['class_sha256'] = hashlib.sha256(data).hexdigest()
            RESULTAT['openjdk_output'] = verklig_data
        # 실패한 ändring_värde/컴파일은 기존 class를 보존한다.
        ändring_värde(dator, 'Calc.java', 'not Java at all', Store_värde=False)
        dator.kommando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ogiltig_KR in [
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
            ändring_värde(dator, 'Calc.java', ogiltig_KR)
            dator.kommando('javac Calc.java', ['javac error:', 'Exit: 1'])
            dator.kommando('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_värde 실행은 användarutrymme heap_värde/프레임을 매번 초기화한다.
        for nummer in range(12):
            dator.kommando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        dator.kommando('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        dator.kommando('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ändring_värde(dator, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        dator.kommando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        dator.kommando('java Calc', ['instruction limit', 'Exit: 1'])
        dator.kommando('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ändring_värde(dator, 'Bad.class', 'garbage')
        dator.kommando('java Bad', ['JVM error:', 'Exit: 1'])
        dator.kommando('rm Bad.class', ['Removed'])
        dator.kommando('java Bad', ['cannot read class: -2'])
        # ändring_värde 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Kör = len(dator.LOG_POST)
        dator.직렬.sendall(b'edit Hello.java\n')
        dator.tillståndet_Vänta('...> ', Kör)
        Kör = len(dator.LOG_POST)
        dator.직렬.sendall(b'x' * 129 + b'\n')
        dator.tillståndet_Vänta('...> ', Kör)
        dator.kommando('.save', ['Too much input; original preserved'])
        dator.kommando('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ändring_värde(dator, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for nummer in range(3):
            ändring_värde(dator, 'f' + str(nummer), 'occupied')
        dator.kommando('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        dator.kommando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in dator.LOG_POST.decode('utf-8', 'replace')
        RESULTAT['serial'] = dator.LOG_POST.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(variant_värde))
        return RESULTAT
    finally:
        dator.Stäng()


def 주코드(data):
    """손상 시험용 main Code의 verklig_data filnamn 오프셋/길이만 읽는다."""
    placera_värde = 8
    def 짧():
        nonlocal placera_värde
        värde = struct.unpack_from('>H', data, placera_värde)[0]
        placera_värde += 2
        return värde
    def läsa_heltal_utan_tecken():
        nonlocal placera_värde
        värde = struct.unpack_from('>I', data, placera_värde)[0]
        placera_värde += 4
        return värde
    문자들 = {}
    for nummer in range(1, 짧()):
        variant_värde = data[placera_värde]
        placera_värde += 1
        if variant_värde == 1:
            längd_värde = 짧()
            문자들[nummer] = data[placera_värde:placera_värde + längd_värde]
            placera_värde += längd_värde
        elif variant_värde in (7, 8): placera_värde += 2
        elif variant_värde in (3, 9, 10, 12): placera_värde += 4
        else: raise AssertionError(variant_värde)
    placera_värde += 6
    objekt_ANTAL = 짧()
    placera_värde += objekt_ANTAL * 2
    assert 짧() == 0
    for nummer in range(짧()):
        짧()
        Namn = 짧()
        짧()
        for nummer in range(짧()):
            attribut_värde = 짧()
            Storlek = läsa_heltal_utan_tecken()
            if 문자들[Namn] == b'main' and 문자들[attribut_värde] == b'Code':
                return placera_värde + 8, struct.unpack_from('>I', data, placera_värde + 4)[0]
            placera_värde += Storlek
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Katalog_värde = Path(임시)
        (Katalog_värde / 'build').mkdir()
        källfil = Katalog_värde / 'Imported.java'
        källfil.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(källfil)], check=True)
        원본 = (Katalog_värde / 'Imported.class').read_bytes()
        KOD_värde, längd_värde = 주코드(원본)
        variant_värde_27a9c9e1 = {}
        data = bytearray(원본); data[0] = 0; variant_värde_27a9c9e1['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; variant_värde_27a9c9e1['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; variant_värde_27a9c9e1['BadPool'] = data
        data = bytearray(원본); data[KOD_värde:KOD_värde + längd_värde] = bytes(längd_värde)
        data[KOD_värde:KOD_värde + 3] = b'\xa7\x00\x01'; data[KOD_värde + längd_värde - 1] = 177; variant_värde_27a9c9e1['BadJump'] = data
        data = bytearray(원본); data[KOD_värde:KOD_värde + längd_värde] = bytes(längd_värde)
        data[KOD_värde] = 87; data[KOD_värde + längd_värde - 1] = 177; variant_värde_27a9c9e1['BadStack'] = data
        # Namn 검사를 통과시켜 verklig_data köra_kommando 중의 operand_Stack 오류까지 검사한다.
        variant_värde_27a9c9e1['BadStack'] = variant_värde_27a9c9e1['BadStack'].replace(b'Imported', b'BadStack')
        post_värde = ['Imported.class=' + str(Katalog_värde / 'Imported.class'), 'Imported.java=' + str(källfil)]
        for Namn, data in variant_värde_27a9c9e1.items():
            sökväg_2 = Katalog_värde / (Namn + '.class'); sökväg_2.write_bytes(data)
            post_värde.append(Namn + '.class=' + str(sökväg_2))
        grupp_värde = Katalog_värde / 'build/java-files.bin'
        subprocess.run([sys.executable, str(position / 'verktyg/자바파일묶기.py'), '-o', str(grupp_värde)] + post_värde, check=True)
        subprocess.run(['as', '--32', '-o', str(Katalog_värde / 'user.o'), str(position / 'maskinstart/användarutrymme.s')], cwd=str(Katalog_värde), check=True)
        kärna_värde = Katalog_värde / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position / 'maskinstart/länkningslayout.ld'), '-o', str(kärna_värde),
                        str(position / 'build/boot.o'), str(position / 'build/java.o'), str(Katalog_värde / 'user.o'), str(position / 'build/apps.o')], check=True)
        dator = VM(kärna_värde, nätverk_värde=False)
        try:
            dator.kommando('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            dator.kommando('cat Imported.java', ['int[] values = new int[3]'])
            for Namn, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                dator.kommando('java ' + Namn, [문구, 'Exit: 1'])
                dator.kommando('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return dator.LOG_POST.decode('utf-8', 'replace')
        finally:
            dator.Stäng()


if __name__ == '__main__':
    parsa_värde = argparse.ArgumentParser()
    parsa_värde.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argument = parsa_värde.parse_args()
    RESULTAT = {variant_värde: test_köra(variant_värde) for variant_värde in (('elf', 'iso') if argument.boot == 'both' else (argument.boot,))}
    RESULTAT['import'] = 적재시험()
    (position / 'build/자바시험.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2) + '\n')
