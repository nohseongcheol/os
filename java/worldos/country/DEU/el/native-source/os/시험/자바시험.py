#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 εκτελώ_εντολή, αποτυχία_τιμή/πόρος_τιμή όριο_τιμή 시험."""
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
from δοκιμή_χρήστης_δίκτυο import εικονική_μηχανή, Θέση


def Τροποποίησε_τιμή(υπολογιστής_5eb260fa, Όνομα, Περιεχόμενο_τιμή, αποθηκεύω_τιμή=True):
    Εκτέλεση_2 = len(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
    υπολογιστής_5eb260fa.직렬.sendall(('edit ' + Όνομα + '\n').encode())
    υπολογιστής_5eb260fa.κατάσταση_αναμονής('...> ', Εκτέλεση_2)
    for Γραμμή in Περιεχόμενο_τιμή.splitlines():
        assert len(Γραμμή) <= 128
        Εκτέλεση_2 = len(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
        υπολογιστής_5eb260fa.직렬.sendall((Γραμμή + '\n').encode())
        υπολογιστής_5eb260fa.κατάσταση_αναμονής('...> ', Εκτέλεση_2)
    Εκτέλεση_2 = len(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
    υπολογιστής_5eb260fa.직렬.sendall(b'.save\n' if αποθηκεύω_τιμή else b'.cancel\n')
    μέτρηση = υπολογιστής_5eb260fa.κατάσταση_αναμονής('jkoros> ', Εκτέλεση_2)
    assert ('Saved:' if αποθηκεύω_τιμή else 'Cancelled; original preserved') in μέτρηση, μέτρηση


def Αρχείο_διεύθυνση():
    μέτρηση = subprocess.check_output(['nm', '-n', str(Θέση / 'build/kernel.elf')], universal_newlines=True)
    for Γραμμή in μέτρηση.splitlines():
        if Γραμμή.endswith(' ram_files'):
            return int(Γραμμή.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def Επισκέπτης_Αρχείο(υπολογιστής_5eb260fa, υποδοχή_τιμή_ff41a4f1, Μέγεθος, ΔΙΑΔΡΟΜΗ):
    # 시험 VM의 메모리에서 πραγματικός_δεδομένα 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    διεύθυνση = Αρχείο_διεύθυνση() + υποδοχή_τιμή_ff41a4f1 * 16384
    υπολογιστής_5eb260fa.οθόνη_τιμή.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(διεύθυνση, Μέγεθος, ΔΙΑΔΡΟΜΗ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ΔΙΑΔΡΟΜΗ.exists() and ΔΙΑΔΡΟΜΗ.stat().st_size == Μέγεθος:
            return ΔΙΑΔΡΟΜΗ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def εκτέλεση_δοκιμής(종류):
    υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, δίκτυο_τιμή=False)
    μέτρηση = {}
    try:
        υπολογιστής_5eb260fa.Εντολή('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        υπολογιστής_5eb260fa.Εντολή('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        υπολογιστής_5eb260fa.Εντολή('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        υπολογιστής_5eb260fa.Εντολή('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        υπολογιστής_5eb260fa.Εντολή('java Missing', ['cannot read class: -2', 'Exit: 1'])
        υπολογιστής_5eb260fa.Εντολή('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        υπολογιστής_5eb260fa.Εντολή('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Περιεχόμενο_τιμή = '''public class Calc {
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
        Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'Calc.java', Περιεχόμενο_τιμή)
        υπολογιστής_5eb260fa.Εντολή('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Έξοδος = υπολογιστής_5eb260fa.Εντολή('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        μέτρηση['guest_output'] = Έξοδος
        καταχώρηση_Λίστα = υπολογιστής_5eb260fa.Εντολή('ls', ['Calc.class'])
        Μέγεθος = int(re.search(r'Calc\.class\s+(\d+) bytes', καταχώρηση_Λίστα).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Κατάλογος_τιμή:
            ΔΙΑΔΡΟΜΗ = Path(Κατάλογος_τιμή) / 'Calc.class'
            δεδομένα = Επισκέπτης_Αρχείο(υπολογιστής_5eb260fa, 3, Μέγεθος, ΔΙΑΔΡΟΜΗ)
            πραγματικός_δεδομένα = subprocess.check_output(['java', '-Xverify:all', '-cp', Κατάλογος_τιμή, 'Calc', '6', 'guest'], universal_newlines=True)
            assert πραγματικός_δεδομένα.splitlines() == 기대, πραγματικός_δεδομένα
            μέτρηση['class_sha256'] = hashlib.sha256(δεδομένα).hexdigest()
            μέτρηση['openjdk_output'] = πραγματικός_δεδομένα
        # 실패한 Τροποποίησε_τιμή/컴파일은 기존 class를 보존한다.
        Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'Calc.java', 'not Java at all', αποθηκεύω_τιμή=False)
        υπολογιστής_5eb260fa.Εντολή('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for άκυρος_μέτρηση in [
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
            Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'Calc.java', άκυρος_μέτρηση)
            υπολογιστής_5eb260fa.Εντολή('javac Calc.java', ['javac error:', 'Exit: 1'])
            υπολογιστής_5eb260fa.Εντολή('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # επανάληψη_τιμή 실행은 χρήστης σωρός_τιμή/프레임을 매번 초기화한다.
        for 수 in range(12):
            υπολογιστής_5eb260fa.Εντολή('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        υπολογιστής_5eb260fa.Εντολή('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        υπολογιστής_5eb260fa.Εντολή('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        υπολογιστής_5eb260fa.Εντολή('javac Calc.java', ['Compiled:', 'Exit: 0'])
        υπολογιστής_5eb260fa.Εντολή('java Calc', ['instruction limit', 'Exit: 1'])
        υπολογιστής_5eb260fa.Εντολή('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'Bad.class', 'garbage')
        υπολογιστής_5eb260fa.Εντολή('java Bad', ['JVM error:', 'Exit: 1'])
        υπολογιστής_5eb260fa.Εντολή('rm Bad.class', ['Removed'])
        υπολογιστής_5eb260fa.Εντολή('java Bad', ['cannot read class: -2'])
        # Τροποποίησε_τιμή 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Εκτέλεση_2 = len(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
        υπολογιστής_5eb260fa.직렬.sendall(b'edit Hello.java\n')
        υπολογιστής_5eb260fa.κατάσταση_αναμονής('...> ', Εκτέλεση_2)
        Εκτέλεση_2 = len(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
        υπολογιστής_5eb260fa.직렬.sendall(b'x' * 129 + b'\n')
        υπολογιστής_5eb260fa.κατάσταση_αναμονής('...> ', Εκτέλεση_2)
        υπολογιστής_5eb260fa.Εντολή('.save', ['Too much input; original preserved'])
        υπολογιστής_5eb260fa.Εντολή('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'f' + str(수), 'occupied')
        υπολογιστής_5eb260fa.Εντολή('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        υπολογιστής_5eb260fa.Εντολή('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
        μέτρηση['serial'] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return μέτρηση
    finally:
        υπολογιστής_5eb260fa.Κλείσιμο()


def 주코드(δεδομένα):
    """손상 시험용 main Code의 πραγματικός_δεδομένα Αρχείο 오프셋/길이만 읽는다."""
    θέση_τιμή = 8
    def 짧():
        nonlocal θέση_τιμή
        τιμή = struct.unpack_from('>H', δεδομένα, θέση_τιμή)[0]
        θέση_τιμή += 2
        return τιμή
    def 정():
        nonlocal θέση_τιμή
        τιμή = struct.unpack_from('>I', δεδομένα, θέση_τιμή)[0]
        θέση_τιμή += 4
        return τιμή
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = δεδομένα[θέση_τιμή]
        θέση_τιμή += 1
        if 종류 == 1:
            διάρκεια_τιμή = 짧()
            문자들[수] = δεδομένα[θέση_τιμή:θέση_τιμή + διάρκεια_τιμή]
            θέση_τιμή += διάρκεια_τιμή
        elif 종류 in (7, 8): θέση_τιμή += 2
        elif 종류 in (3, 9, 10, 12): θέση_τιμή += 4
        else: raise AssertionError(종류)
    θέση_τιμή += 6
    개수 = 짧()
    θέση_τιμή += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Όνομα = 짧()
        짧()
        for 수 in range(짧()):
            χαρακτηριστικό_τιμή_286d43f0 = 짧()
            Μέγεθος = 정()
            if 문자들[Όνομα] == b'main' and 문자들[χαρακτηριστικό_τιμή_286d43f0] == b'Code':
                return θέση_τιμή + 8, struct.unpack_from('>I', δεδομένα, θέση_τιμή + 4)[0]
            θέση_τιμή += Μέγεθος
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Κατάλογος_τιμή = Path(임시)
        (Κατάλογος_τιμή / 'build').mkdir()
        ΠΗΓΗ = Κατάλογος_τιμή / 'Imported.java'
        ΠΗΓΗ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ΠΗΓΗ)], check=True)
        원본 = (Κατάλογος_τιμή / 'Imported.class').read_bytes()
        κωδικός_τιμή, διάρκεια_τιμή = 주코드(원본)
        χαρακτηριστικό_τιμή = {}
        δεδομένα = bytearray(원본); δεδομένα[0] = 0; χαρακτηριστικό_τιμή['BadMagic'] = δεδομένα
        δεδομένα = bytearray(원본); δεδομένα[7] = 61; χαρακτηριστικό_τιμή['BadVer'] = δεδομένα
        δεδομένα = bytearray(원본); δεδομένα[8:10] = b'\xff\xff'; χαρακτηριστικό_τιμή['BadPool'] = δεδομένα
        δεδομένα = bytearray(원본); δεδομένα[κωδικός_τιμή:κωδικός_τιμή + διάρκεια_τιμή] = bytes(διάρκεια_τιμή)
        δεδομένα[κωδικός_τιμή:κωδικός_τιμή + 3] = b'\xa7\x00\x01'; δεδομένα[κωδικός_τιμή + διάρκεια_τιμή - 1] = 177; χαρακτηριστικό_τιμή['BadJump'] = δεδομένα
        δεδομένα = bytearray(원본); δεδομένα[κωδικός_τιμή:κωδικός_τιμή + διάρκεια_τιμή] = bytes(διάρκεια_τιμή)
        δεδομένα[κωδικός_τιμή] = 87; δεδομένα[κωδικός_τιμή + διάρκεια_τιμή - 1] = 177; χαρακτηριστικό_τιμή['BadStack'] = δεδομένα
        # Όνομα 검사를 통과시켜 πραγματικός_δεδομένα εκτελώ_εντολή 중의 τελεστέος_δέσμη 오류까지 검사한다.
        χαρακτηριστικό_τιμή['BadStack'] = χαρακτηριστικό_τιμή['BadStack'].replace(b'Imported', b'BadStack')
        καταχώρηση_τιμή = ['Imported.class=' + str(Κατάλογος_τιμή / 'Imported.class'), 'Imported.java=' + str(ΠΗΓΗ)]
        for Όνομα, δεδομένα in χαρακτηριστικό_τιμή.items():
            ΔΙΑΔΡΟΜΗ = Κατάλογος_τιμή / (Όνομα + '.class'); ΔΙΑΔΡΟΜΗ.write_bytes(δεδομένα)
            καταχώρηση_τιμή.append(Όνομα + '.class=' + str(ΔΙΑΔΡΟΜΗ))
        Ομάδα_τιμή = Κατάλογος_τιμή / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Θέση / 'Εργαλεία/자바파일묶기.py'), '-o', str(Ομάδα_τιμή)] + καταχώρηση_τιμή, check=True)
        subprocess.run(['as', '--32', '-o', str(Κατάλογος_τιμή / 'user.o'), str(Θέση / '부팅/χρήστης.s')], cwd=str(Κατάλογος_τιμή), check=True)
        πυρήνας_τιμή = Κατάλογος_τιμή / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Θέση / '부팅/συνδέω_Διάταξη.ld'), '-o', str(πυρήνας_τιμή),
                        str(Θέση / 'build/boot.o'), str(Θέση / 'build/java.o'), str(Κατάλογος_τιμή / 'user.o'), str(Θέση / 'build/apps.o')], check=True)
        υπολογιστής_5eb260fa = εικονική_μηχανή(πυρήνας_τιμή, δίκτυο_τιμή=False)
        try:
            υπολογιστής_5eb260fa.Εντολή('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            υπολογιστής_5eb260fa.Εντολή('cat Imported.java', ['int[] values = new int[3]'])
            for Όνομα, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                υπολογιστής_5eb260fa.Εντολή('java ' + Όνομα, [문구, 'Exit: 1'])
                υπολογιστής_5eb260fa.Εντολή('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
        finally:
            υπολογιστής_5eb260fa.Κλείσιμο()


if __name__ == '__main__':
    ανάλυση_τιμή_7cebddfb = argparse.ArgumentParser()
    ανάλυση_τιμή_7cebddfb.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Παράμετροι = ανάλυση_τιμή_7cebddfb.parse_args()
    μέτρηση = {종류: εκτέλεση_δοκιμής(종류) for 종류 in (('elf', 'iso') if Παράμετροι.boot == 'both' else (Παράμετροι.boot,))}
    μέτρηση['import'] = 적재시험()
    (Θέση / 'build/자바시험.json').write_text(json.dumps(μέτρηση, ensure_ascii=False, indent=2) + '\n')
