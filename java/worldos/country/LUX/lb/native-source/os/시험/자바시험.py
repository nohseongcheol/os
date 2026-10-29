#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ausféieren_Befeel, Feeler_VALUE/Ressource_VALUE 경계 시험."""
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
from 사용자통신시험 import virtuell_Computer, positionéieren


def Editéieren_VALUE(Computer, Numm, Inhalt_VALUE, Store_VALUE=True):
    Laf = len(Computer.LOG_Rei)
    Computer.직렬.sendall(('edit ' + Numm + '\n').encode())
    Computer.Waart_Status('...> ', Laf)
    for Zeil in Inhalt_VALUE.splitlines():
        assert len(Zeil) <= 128
        Laf = len(Computer.LOG_Rei)
        Computer.직렬.sendall((Zeil + '\n').encode())
        Computer.Waart_Status('...> ', Laf)
    Laf = len(Computer.LOG_Rei)
    Computer.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    Mooss = Computer.Waart_Status('jkoros> ', Laf)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in Mooss, Mooss


def Fichier_Adress():
    Mooss = subprocess.check_output(['nm', '-n', str(positionéieren / 'build/kernel.elf')], universal_newlines=True)
    for Zeil in Mooss.splitlines():
        if Zeil.endswith(' ram_files'):
            return int(Zeil.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def Gaascht_Fichier(Computer, Slot_VALUE, d_Gréisst_veränneren, Wee):
    # 시험 VM의 메모리에서 aktuell_Daten 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    Adress = Fichier_Adress() + Slot_VALUE * 16384
    Computer.Schierm_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(Adress, d_Gréisst_veränneren, Wee)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Wee.exists() and Wee.stat().st_size == d_Gréisst_veränneren:
            return Wee.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    Computer = virtuell_Computer(positionéieren / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Reseau_VALUE=False)
    Mooss = {}
    try:
        Computer.Befeel('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        Computer.Befeel('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        Computer.Befeel('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        Computer.Befeel('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        Computer.Befeel('java Missing', ['cannot read class: -2', 'Exit: 1'])
        Computer.Befeel('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        Computer.Befeel('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Inhalt_VALUE = '''public class Calc {
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
        Editéieren_VALUE(Computer, 'Calc.java', Inhalt_VALUE)
        Computer.Befeel('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = Computer.Befeel('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        Mooss['guest_output'] = 출력
        Agab_Lëscht = Computer.Befeel('ls', ['Calc.class'])
        d_Gréisst_veränneren = int(re.search(r'Calc\.class\s+(\d+) bytes', Agab_Lëscht).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Verzeechnes_VALUE:
            Wee = Path(Verzeechnes_VALUE) / 'Calc.class'
            Daten = Gaascht_Fichier(Computer, 3, d_Gréisst_veränneren, Wee)
            aktuell_Daten = subprocess.check_output(['java', '-Xverify:all', '-cp', Verzeechnes_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert aktuell_Daten.splitlines() == 기대, aktuell_Daten
            Mooss['class_sha256'] = hashlib.sha256(Daten).hexdigest()
            Mooss['openjdk_output'] = aktuell_Daten
        # 실패한 Editéieren_VALUE/컴파일은 기존 class를 보존한다.
        Editéieren_VALUE(Computer, 'Calc.java', 'not Java at all', Store_VALUE=False)
        Computer.Befeel('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ongëlteg_Mooss in [
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
            Editéieren_VALUE(Computer, 'Calc.java', ongëlteg_Mooss)
            Computer.Befeel('javac Calc.java', ['javac error:', 'Exit: 1'])
            Computer.Befeel('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # Iteratioun_VALUE 실행은 Benotzer 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            Computer.Befeel('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        Computer.Befeel('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        Computer.Befeel('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Editéieren_VALUE(Computer, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        Computer.Befeel('javac Calc.java', ['Compiled:', 'Exit: 0'])
        Computer.Befeel('java Calc', ['instruction limit', 'Exit: 1'])
        Computer.Befeel('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Editéieren_VALUE(Computer, 'Bad.class', 'garbage')
        Computer.Befeel('java Bad', ['JVM error:', 'Exit: 1'])
        Computer.Befeel('rm Bad.class', ['Removed'])
        Computer.Befeel('java Bad', ['cannot read class: -2'])
        # Editéieren_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Laf = len(Computer.LOG_Rei)
        Computer.직렬.sendall(b'edit Hello.java\n')
        Computer.Waart_Status('...> ', Laf)
        Laf = len(Computer.LOG_Rei)
        Computer.직렬.sendall(b'x' * 129 + b'\n')
        Computer.Waart_Status('...> ', Laf)
        Computer.Befeel('.save', ['Too much input; original preserved'])
        Computer.Befeel('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Editéieren_VALUE(Computer, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Editéieren_VALUE(Computer, 'f' + str(수), 'occupied')
        Computer.Befeel('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        Computer.Befeel('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in Computer.LOG_Rei.decode('utf-8', 'replace')
        Mooss['serial'] = Computer.LOG_Rei.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return Mooss
    finally:
        Computer.Clôture()


def 주코드(Daten):
    """손상 시험용 main Code의 aktuell_Daten Fichier 오프셋/길이만 읽는다."""
    positionéieren_VALUE = 8
    def 짧():
        nonlocal positionéieren_VALUE
        VALUE = struct.unpack_from('>H', Daten, positionéieren_VALUE)[0]
        positionéieren_VALUE += 2
        return VALUE
    def 정():
        nonlocal positionéieren_VALUE
        VALUE = struct.unpack_from('>I', Daten, positionéieren_VALUE)[0]
        positionéieren_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = Daten[positionéieren_VALUE]
        positionéieren_VALUE += 1
        if 종류 == 1:
            Längt_VALUE = 짧()
            문자들[수] = Daten[positionéieren_VALUE:positionéieren_VALUE + Längt_VALUE]
            positionéieren_VALUE += Längt_VALUE
        elif 종류 in (7, 8): positionéieren_VALUE += 2
        elif 종류 in (3, 9, 10, 12): positionéieren_VALUE += 4
        else: raise AssertionError(종류)
    positionéieren_VALUE += 6
    Element_COUNT = 짧()
    positionéieren_VALUE += Element_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Numm = 짧()
        짧()
        for 수 in range(짧()):
            Attribut_VALUE = 짧()
            d_Gréisst_veränneren = 정()
            if 문자들[Numm] == b'main' and 문자들[Attribut_VALUE] == b'Code':
                return positionéieren_VALUE + 8, struct.unpack_from('>I', Daten, positionéieren_VALUE + 4)[0]
            positionéieren_VALUE += d_Gréisst_veränneren
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Verzeechnes_VALUE = Path(임시)
        (Verzeechnes_VALUE / 'build').mkdir()
        Quell = Verzeechnes_VALUE / 'Imported.java'
        Quell.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Quell)], check=True)
        원본 = (Verzeechnes_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, Längt_VALUE = 주코드(원본)
        변형 = {}
        Daten = bytearray(원본); Daten[0] = 0; 변형['BadMagic'] = Daten
        Daten = bytearray(원본); Daten[7] = 61; 변형['BadVer'] = Daten
        Daten = bytearray(원본); Daten[8:10] = b'\xff\xff'; 변형['BadPool'] = Daten
        Daten = bytearray(원본); Daten[CODE_VALUE:CODE_VALUE + Längt_VALUE] = bytes(Längt_VALUE)
        Daten[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; Daten[CODE_VALUE + Längt_VALUE - 1] = 177; 변형['BadJump'] = Daten
        Daten = bytearray(원본); Daten[CODE_VALUE:CODE_VALUE + Längt_VALUE] = bytes(Längt_VALUE)
        Daten[CODE_VALUE] = 87; Daten[CODE_VALUE + Längt_VALUE - 1] = 177; 변형['BadStack'] = Daten
        # Numm 검사를 통과시켜 aktuell_Daten ausféieren_Befeel 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        Agab_VALUE = ['Imported.class=' + str(Verzeechnes_VALUE / 'Imported.class'), 'Imported.java=' + str(Quell)]
        for Numm, Daten in 변형.items():
            Wee = Verzeechnes_VALUE / (Numm + '.class'); Wee.write_bytes(Daten)
            Agab_VALUE.append(Numm + '.class=' + str(Wee))
        Grupp_VALUE = Verzeechnes_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(positionéieren / 'Tools/자바파일묶기.py'), '-o', str(Grupp_VALUE)] + Agab_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Verzeechnes_VALUE / 'user.o'), str(positionéieren / '부팅/Benotzer.s')], cwd=str(Verzeechnes_VALUE), check=True)
        Kernel_VALUE = Verzeechnes_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(positionéieren / '부팅/Link_Layout.ld'), '-o', str(Kernel_VALUE),
                        str(positionéieren / 'build/boot.o'), str(positionéieren / 'build/java.o'), str(Verzeechnes_VALUE / 'user.o'), str(positionéieren / 'build/apps.o')], check=True)
        Computer = virtuell_Computer(Kernel_VALUE, Reseau_VALUE=False)
        try:
            Computer.Befeel('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            Computer.Befeel('cat Imported.java', ['int[] values = new int[3]'])
            for Numm, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                Computer.Befeel('java ' + Numm, [문구, 'Exit: 1'])
                Computer.Befeel('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return Computer.LOG_Rei.decode('utf-8', 'replace')
        finally:
            Computer.Clôture()


if __name__ == '__main__':
    analyséieren_VALUE = argparse.ArgumentParser()
    analyséieren_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = analyséieren_VALUE.parse_args()
    Mooss = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    Mooss['import'] = 적재시험()
    (positionéieren / 'build/자바시험.json').write_text(json.dumps(Mooss, ensure_ascii=False, indent=2) + '\n')
