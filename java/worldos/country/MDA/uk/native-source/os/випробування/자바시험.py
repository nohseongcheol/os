#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Виконати_команда, неполадка_значення/ресурс_значення 경계 випробування."""
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
from 사용자통신시험 import ВМ, позиція


def правка_значення(комп_ютер, Назва, Вміст_значення, сховище_значення=True):
    запустити = len(комп_ютер.журнал_запис)
    комп_ютер.직렬.sendall(('edit ' + Назва + '\n').encode())
    комп_ютер.стан_очікування('...> ', запустити)
    for рядок_введення in Вміст_значення.splitlines():
        assert len(рядок_введення) <= 128
        запустити = len(комп_ютер.журнал_запис)
        комп_ютер.직렬.sendall((рядок_введення + '\n').encode())
        комп_ютер.стан_очікування('...> ', запустити)
    запустити = len(комп_ютер.журнал_запис)
    комп_ютер.직렬.sendall(b'.save\n' if сховище_значення else b'.cancel\n')
    результат = комп_ютер.стан_очікування('jkoros> ', запустити)
    assert ('Saved:' if сховище_значення else 'Cancelled; original preserved') in результат, результат


def Файл_адреса():
    результат = subprocess.check_output(['nm', '-n', str(позиція / 'build/kernel.elf')], universal_newlines=True)
    for рядок_введення in результат.splitlines():
        if рядок_введення.endswith(' ram_files'):
            return int(рядок_введення.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def гість_Файл(комп_ютер, 슬롯, Розмір, шлях):
    # випробування VM의 메모리에서 фактично_дані 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    Адреса = Файл_адреса() + 슬롯 * 16384
    комп_ютер.монітор_значення.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(Адреса, Розмір, шлях)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if шлях.exists() and шлях.stat().st_size == Розмір:
            return шлях.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    комп_ютер = ВМ(позиція / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, мережа_значення=False)
    результат = {}
    try:
        комп_ютер.команда('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        комп_ютер.команда('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        комп_ютер.команда('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        комп_ютер.команда('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        комп_ютер.команда('java Missing', ['cannot read class: -2', 'Exit: 1'])
        комп_ютер.команда('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        комп_ютер.команда('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Вміст_значення = '''public class Calc {
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
        правка_значення(комп_ютер, 'Calc.java', Вміст_значення)
        комп_ютер.команда('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Вивід = комп_ютер.команда('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        результат['guest_output'] = Вивід
        запис_список = комп_ютер.команда('ls', ['Calc.class'])
        Розмір = int(re.search(r'Calc\.class\s+(\d+) bytes', запис_список).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Каталог_значення:
            шлях = Path(Каталог_значення) / 'Calc.class'
            дані = гість_Файл(комп_ютер, 3, Розмір, шлях)
            фактично_дані = subprocess.check_output(['java', '-Xverify:all', '-cp', Каталог_значення, 'Calc', '6', 'guest'], universal_newlines=True)
            assert фактично_дані.splitlines() == 기대, фактично_дані
            результат['class_sha256'] = hashlib.sha256(дані).hexdigest()
            результат['openjdk_output'] = фактично_дані
        # 실패한 правка_значення/컴파일은 기존 class를 보존한다.
        правка_значення(комп_ютер, 'Calc.java', 'not Java at all', сховище_значення=False)
        комп_ютер.команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for недійсний_КР in [
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
            правка_значення(комп_ютер, 'Calc.java', недійсний_КР)
            комп_ютер.команда('javac Calc.java', ['javac error:', 'Exit: 1'])
            комп_ютер.команда('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # спринт_значення 실행은 простір_користувача динамічна_пам_ять_значення/프레임을 매번 초기화한다.
        for 수 in range(12):
            комп_ютер.команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        комп_ютер.команда('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        комп_ютер.команда('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        правка_значення(комп_ютер, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        комп_ютер.команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        комп_ютер.команда('java Calc', ['instruction limit', 'Exit: 1'])
        комп_ютер.команда('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        правка_значення(комп_ютер, 'Bad.class', 'garbage')
        комп_ютер.команда('java Bad', ['JVM error:', 'Exit: 1'])
        комп_ютер.команда('rm Bad.class', ['Removed'])
        комп_ютер.команда('java Bad', ['cannot read class: -2'])
        # правка_значення 입력의 넘친 부분을 잘라서 저장하지 않는다.
        запустити = len(комп_ютер.журнал_запис)
        комп_ютер.직렬.sendall(b'edit Hello.java\n')
        комп_ютер.стан_очікування('...> ', запустити)
        запустити = len(комп_ютер.журнал_запис)
        комп_ютер.직렬.sendall(b'x' * 129 + b'\n')
        комп_ютер.стан_очікування('...> ', запустити)
        комп_ютер.команда('.save', ['Too much input; original preserved'])
        комп_ютер.команда('javac Hello.java', ['Compiled:', 'Exit: 0'])
        правка_значення(комп_ютер, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            правка_значення(комп_ютер, 'f' + str(수), 'occupied')
        комп_ютер.команда('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        комп_ютер.команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in комп_ютер.журнал_запис.decode('utf-8', 'replace')
        результат['serial'] = комп_ютер.журнал_запис.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return результат
    finally:
        комп_ютер.Закрити()


def 주코드(дані):
    """손상 시험용 main Code의 фактично_дані файл 오프셋/길이만 읽는다."""
    посада_значення = 8
    def 짧():
        nonlocal посада_значення
        значення = struct.unpack_from('>H', дані, посада_значення)[0]
        посада_значення += 2
        return значення
    def 정():
        nonlocal посада_значення
        значення = struct.unpack_from('>I', дані, посада_значення)[0]
        посада_значення += 4
        return значення
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = дані[посада_значення]
        посада_значення += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[수] = дані[посада_значення:посада_значення + 길이]
            посада_значення += 길이
        elif 종류 in (7, 8): посада_значення += 2
        elif 종류 in (3, 9, 10, 12): посада_значення += 4
        else: raise AssertionError(종류)
    посада_значення += 6
    개수 = 짧()
    посада_значення += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Назва = 짧()
        짧()
        for 수 in range(짧()):
            атрибут_значення = 짧()
            Розмір = 정()
            if 문자들[Назва] == b'main' and 문자들[атрибут_значення] == b'Code':
                return посада_значення + 8, struct.unpack_from('>I', дані, посада_значення + 4)[0]
            посада_значення += Розмір
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Каталог_значення = Path(임시)
        (Каталог_значення / 'build').mkdir()
        вихіднийКод = Каталог_значення / 'Imported.java'
        вихіднийКод.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(вихіднийКод)], check=True)
        원본 = (Каталог_значення / 'Imported.class').read_bytes()
        код_значення, 길이 = 주코드(원본)
        변형 = {}
        дані = bytearray(원본); дані[0] = 0; 변형['BadMagic'] = дані
        дані = bytearray(원본); дані[7] = 61; 변형['BadVer'] = дані
        дані = bytearray(원본); дані[8:10] = b'\xff\xff'; 변형['BadPool'] = дані
        дані = bytearray(원본); дані[код_значення:код_значення + 길이] = bytes(길이)
        дані[код_значення:код_значення + 3] = b'\xa7\x00\x01'; дані[код_значення + 길이 - 1] = 177; 변형['BadJump'] = дані
        дані = bytearray(원본); дані[код_значення:код_значення + 길이] = bytes(길이)
        дані[код_значення] = 87; дані[код_значення + 길이 - 1] = 177; 변형['BadStack'] = дані
        # Назва 검사를 통과시켜 фактично_дані Виконати_команда 중의 операнд_Стіс 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        запис_значення_962f286b = ['Imported.class=' + str(Каталог_значення / 'Imported.class'), 'Imported.java=' + str(вихіднийКод)]
        for Назва, дані in 변형.items():
            шлях = Каталог_значення / (Назва + '.class'); шлях.write_bytes(дані)
            запис_значення_962f286b.append(Назва + '.class=' + str(шлях))
        Група_значення = Каталог_значення / 'build/java-files.bin'
        subprocess.run([sys.executable, str(позиція / 'інструменти/자바파일묶기.py'), '-o', str(Група_значення)] + запис_значення_962f286b, check=True)
        subprocess.run(['as', '--32', '-o', str(Каталог_значення / 'user.o'), str(позиція / 'запуск_машини/простір_користувача.s')], cwd=str(Каталог_значення), check=True)
        ядро_значення = Каталог_значення / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(позиція / 'запуск_машини/схема_компонування.ld'), '-o', str(ядро_значення),
                        str(позиція / 'build/boot.o'), str(позиція / 'build/java.o'), str(Каталог_значення / 'user.o'), str(позиція / 'build/apps.o')], check=True)
        комп_ютер = ВМ(ядро_значення, мережа_значення=False)
        try:
            комп_ютер.команда('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            комп_ютер.команда('cat Imported.java', ['int[] values = new int[3]'])
            for Назва, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                комп_ютер.команда('java ' + Назва, [문구, 'Exit: 1'])
                комп_ютер.команда('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return комп_ютер.журнал_запис.decode('utf-8', 'replace')
        finally:
            комп_ютер.Закрити()


if __name__ == '__main__':
    аналізувати_значення = argparse.ArgumentParser()
    аналізувати_значення.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    аргументи = аналізувати_значення.parse_args()
    результат = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if аргументи.boot == 'both' else (аргументи.boot,))}
    результат['import'] = 적재시험()
    (позиція / 'build/자바시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2) + '\n')
