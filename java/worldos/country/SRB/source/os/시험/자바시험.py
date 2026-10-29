#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Изврши_команда, неуспјех_вриједност/ресурс_вриједност 경계 시험."""
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
from 사용자통신시험 import виртуелно_рачунар, Положај


def Уреди_вриједност(рачунар, Назив, Садржај_вриједност, похранити_вриједност=True):
    Покрени = len(рачунар.евиденција_ред)
    рачунар.직렬.sendall(('edit ' + Назив + '\n').encode())
    рачунар.чекај_стање('...> ', Покрени)
    for Ред in Садржај_вриједност.splitlines():
        assert len(Ред) <= 128
        Покрени = len(рачунар.евиденција_ред)
        рачунар.직렬.sendall((Ред + '\n').encode())
        рачунар.чекај_стање('...> ', Покрени)
    Покрени = len(рачунар.евиденција_ред)
    рачунар.직렬.sendall(b'.save\n' if похранити_вриједност else b'.cancel\n')
    ИСХОД = рачунар.чекај_стање('jkoros> ', Покрени)
    assert ('Saved:' if похранити_вриједност else 'Cancelled; original preserved') in ИСХОД, ИСХОД


def фајл_адреса():
    ИСХОД = subprocess.check_output(['nm', '-n', str(Положај / 'build/kernel.elf')], universal_newlines=True)
    for Ред in ИСХОД.splitlines():
        if Ред.endswith(' ram_files'):
            return int(Ред.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def гост_фајл(рачунар, простор_за_унос_вриједност, Величина, ПУТАЊА):
    # 시험 VM의 메모리에서 стваран_подаци 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    адреса = фајл_адреса() + простор_за_унос_вриједност * 16384
    рачунар.монитор_вриједност.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(адреса, Величина, ПУТАЊА)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ПУТАЊА.exists() and ПУТАЊА.stat().st_size == Величина:
            return ПУТАЊА.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    рачунар = виртуелно_рачунар(Положај / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Мрежа_вриједност=False)
    ИСХОД = {}
    try:
        рачунар.Наредба('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        рачунар.Наредба('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        рачунар.Наредба('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        рачунар.Наредба('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        рачунар.Наредба('java Missing', ['cannot read class: -2', 'Exit: 1'])
        рачунар.Наредба('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        рачунар.Наредба('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Садржај_вриједност = '''public class Calc {
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
        Уреди_вриједност(рачунар, 'Calc.java', Садржај_вриједност)
        рачунар.Наредба('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Излаз = рачунар.Наредба('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ИСХОД['guest_output'] = Излаз
        унос_Листа = рачунар.Наредба('ls', ['Calc.class'])
        Величина = int(re.search(r'Calc\.class\s+(\d+) bytes', унос_Листа).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as именик_вриједност:
            ПУТАЊА = Path(именик_вриједност) / 'Calc.class'
            подаци = гост_фајл(рачунар, 3, Величина, ПУТАЊА)
            стваран_подаци = subprocess.check_output(['java', '-Xverify:all', '-cp', именик_вриједност, 'Calc', '6', 'guest'], universal_newlines=True)
            assert стваран_подаци.splitlines() == 기대, стваран_подаци
            ИСХОД['class_sha256'] = hashlib.sha256(подаци).hexdigest()
            ИСХОД['openjdk_output'] = стваран_подаци
        # 실패한 Уреди_вриједност/컴파일은 기존 class를 보존한다.
        Уреди_вриједност(рачунар, 'Calc.java', 'not Java at all', похранити_вриједност=False)
        рачунар.Наредба('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for неважеће_мера in [
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
            Уреди_вриједност(рачунар, 'Calc.java', неважеће_мера)
            рачунар.Наредба('javac Calc.java', ['javac error:', 'Exit: 1'])
            рачунар.Наредба('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # спринт_вриједност 실행은 корисник 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            рачунар.Наредба('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        рачунар.Наредба('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        рачунар.Наредба('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Уреди_вриједност(рачунар, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        рачунар.Наредба('javac Calc.java', ['Compiled:', 'Exit: 0'])
        рачунар.Наредба('java Calc', ['instruction limit', 'Exit: 1'])
        рачунар.Наредба('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Уреди_вриједност(рачунар, 'Bad.class', 'garbage')
        рачунар.Наредба('java Bad', ['JVM error:', 'Exit: 1'])
        рачунар.Наредба('rm Bad.class', ['Removed'])
        рачунар.Наредба('java Bad', ['cannot read class: -2'])
        # Уреди_вриједност 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Покрени = len(рачунар.евиденција_ред)
        рачунар.직렬.sendall(b'edit Hello.java\n')
        рачунар.чекај_стање('...> ', Покрени)
        Покрени = len(рачунар.евиденција_ред)
        рачунар.직렬.sendall(b'x' * 129 + b'\n')
        рачунар.чекај_стање('...> ', Покрени)
        рачунар.Наредба('.save', ['Too much input; original preserved'])
        рачунар.Наредба('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Уреди_вриједност(рачунар, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Уреди_вриједност(рачунар, 'f' + str(수), 'occupied')
        рачунар.Наредба('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        рачунар.Наредба('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in рачунар.евиденција_ред.decode('utf-8', 'replace')
        ИСХОД['serial'] = рачунар.евиденција_ред.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ИСХОД
    finally:
        рачунар.Затворен()


def 주코드(подаци):
    """손상 시험용 main Code의 стваран_подаци Датотека 오프셋/길이만 읽는다."""
    позиција_вриједност = 8
    def 짧():
        nonlocal позиција_вриједност
        вриједност = struct.unpack_from('>H', подаци, позиција_вриједност)[0]
        позиција_вриједност += 2
        return вриједност
    def 정():
        nonlocal позиција_вриједност
        вриједност = struct.unpack_from('>I', подаци, позиција_вриједност)[0]
        позиција_вриједност += 4
        return вриједност
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = подаци[позиција_вриједност]
        позиција_вриједност += 1
        if 종류 == 1:
            дужина_вриједност = 짧()
            문자들[수] = подаци[позиција_вриједност:позиција_вриједност + дужина_вриједност]
            позиција_вриједност += дужина_вриједност
        elif 종류 in (7, 8): позиција_вриједност += 2
        elif 종류 in (3, 9, 10, 12): позиција_вриједност += 4
        else: raise AssertionError(종류)
    позиција_вриједност += 6
    개수 = 짧()
    позиција_вриједност += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Назив = 짧()
        짧()
        for 수 in range(짧()):
            атрибут_вриједност = 짧()
            Величина = 정()
            if 문자들[Назив] == b'main' and 문자들[атрибут_вриједност] == b'Code':
                return позиција_вриједност + 8, struct.unpack_from('>I', подаци, позиција_вриједност + 4)[0]
            позиција_вриједност += Величина
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        именик_вриједност = Path(임시)
        (именик_вриједност / 'build').mkdir()
        ИЗВОР = именик_вриједност / 'Imported.java'
        ИЗВОР.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ИЗВОР)], check=True)
        원본 = (именик_вриједност / 'Imported.class').read_bytes()
        шифра_вриједност, дужина_вриједност = 주코드(원본)
        변형 = {}
        подаци = bytearray(원본); подаци[0] = 0; 변형['BadMagic'] = подаци
        подаци = bytearray(원본); подаци[7] = 61; 변형['BadVer'] = подаци
        подаци = bytearray(원본); подаци[8:10] = b'\xff\xff'; 변형['BadPool'] = подаци
        подаци = bytearray(원본); подаци[шифра_вриједност:шифра_вриједност + дужина_вриједност] = bytes(дужина_вриједност)
        подаци[шифра_вриједност:шифра_вриједност + 3] = b'\xa7\x00\x01'; подаци[шифра_вриједност + дужина_вриједност - 1] = 177; 변형['BadJump'] = подаци
        подаци = bytearray(원본); подаци[шифра_вриједност:шифра_вриједност + дужина_вриједност] = bytes(дужина_вриједност)
        подаци[шифра_вриједност] = 87; подаци[шифра_вриједност + дужина_вриједност - 1] = 177; 변형['BadStack'] = подаци
        # Назив 검사를 통과시켜 стваран_подаци Изврши_команда 중의 операнд_комплет 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        унос_вриједност = ['Imported.class=' + str(именик_вриједност / 'Imported.class'), 'Imported.java=' + str(ИЗВОР)]
        for Назив, подаци in 변형.items():
            ПУТАЊА = именик_вриједност / (Назив + '.class'); ПУТАЊА.write_bytes(подаци)
            унос_вриједност.append(Назив + '.class=' + str(ПУТАЊА))
        Група_вриједност = именик_вриједност / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Положај / 'Алатке/자바파일묶기.py'), '-o', str(Група_вриједност)] + унос_вриједност, check=True)
        subprocess.run(['as', '--32', '-o', str(именик_вриједност / 'user.o'), str(Положај / '부팅/корисник.s')], cwd=str(именик_вриједност), check=True)
        језгро_вриједност = именик_вриједност / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Положај / '부팅/Веза_изглед.ld'), '-o', str(језгро_вриједност),
                        str(Положај / 'build/boot.o'), str(Положај / 'build/java.o'), str(именик_вриједност / 'user.o'), str(Положај / 'build/apps.o')], check=True)
        рачунар = виртуелно_рачунар(језгро_вриједност, Мрежа_вриједност=False)
        try:
            рачунар.Наредба('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            рачунар.Наредба('cat Imported.java', ['int[] values = new int[3]'])
            for Назив, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                рачунар.Наредба('java ' + Назив, [문구, 'Exit: 1'])
                рачунар.Наредба('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return рачунар.евиденција_ред.decode('utf-8', 'replace')
        finally:
            рачунар.Затворен()


if __name__ == '__main__':
    рашчланити_вриједност = argparse.ArgumentParser()
    рашчланити_вриједност.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Аргументи = рашчланити_вриједност.parse_args()
    ИСХОД = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Аргументи.boot == 'both' else (Аргументи.boot,))}
    ИСХОД['import'] = 적재시험()
    (Положај / 'build/자바시험.json').write_text(json.dumps(ИСХОД, ensure_ascii=False, indent=2) + '\n')
