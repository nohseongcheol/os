#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 изпълнявам_команда, отказ_стойност/ресурс_стойност 경계 시험."""
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
from 사용자통신시험 import виртуална_машина, Позиция


def редакция_стойност(машина, Име, Съдържание_стойност, хранилище_стойност=True):
    Стартиране = len(машина.регистрирам_запис)
    машина.직렬.sendall(('edit ' + Име + '\n').encode())
    машина.състояние_на_изчакване('...> ', Стартиране)
    for ред in Съдържание_стойност.splitlines():
        assert len(ред) <= 128
        Стартиране = len(машина.регистрирам_запис)
        машина.직렬.sendall((ред + '\n').encode())
        машина.състояние_на_изчакване('...> ', Стартиране)
    Стартиране = len(машина.регистрирам_запис)
    машина.직렬.sendall(b'.save\n' if хранилище_стойност else b'.cancel\n')
    РЕЗУЛТАТ = машина.състояние_на_изчакване('jkoros> ', Стартиране)
    assert ('Saved:' if хранилище_стойност else 'Cancelled; original preserved') in РЕЗУЛТАТ, РЕЗУЛТАТ


def Файл_адрес():
    РЕЗУЛТАТ = subprocess.check_output(['nm', '-n', str(Позиция / 'build/kernel.elf')], universal_newlines=True)
    for ред in РЕЗУЛТАТ.splitlines():
        if ред.endswith(' ram_files'):
            return int(ред.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def гост_Файл(машина, 슬롯, Размер, ПЪТ):
    # 시험 VM의 메모리에서 действителен_данни 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    адрес = Файл_адрес() + 슬롯 * 16384
    машина.монитор_стойност.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(адрес, Размер, ПЪТ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ПЪТ.exists() and ПЪТ.stat().st_size == Размер:
            return ПЪТ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    машина = виртуална_машина(Позиция / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, мрежа_стойност=False)
    РЕЗУЛТАТ = {}
    try:
        машина.Команда('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        машина.Команда('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        машина.Команда('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        машина.Команда('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        машина.Команда('java Missing', ['cannot read class: -2', 'Exit: 1'])
        машина.Команда('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        машина.Команда('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Съдържание_стойност = '''public class Calc {
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
        редакция_стойност(машина, 'Calc.java', Съдържание_стойност)
        машина.Команда('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Изход = машина.Команда('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        РЕЗУЛТАТ['guest_output'] = Изход
        запис_Списък = машина.Команда('ls', ['Calc.class'])
        Размер = int(re.search(r'Calc\.class\s+(\d+) bytes', запис_Списък).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as указател_стойност:
            ПЪТ = Path(указател_стойност) / 'Calc.class'
            данни = гост_Файл(машина, 3, Размер, ПЪТ)
            действителен_данни = subprocess.check_output(['java', '-Xverify:all', '-cp', указател_стойност, 'Calc', '6', 'guest'], universal_newlines=True)
            assert действителен_данни.splitlines() == 기대, действителен_данни
            РЕЗУЛТАТ['class_sha256'] = hashlib.sha256(данни).hexdigest()
            РЕЗУЛТАТ['openjdk_output'] = действителен_данни
        # 실패한 редакция_стойност/컴파일은 기존 class를 보존한다.
        редакция_стойност(машина, 'Calc.java', 'not Java at all', хранилище_стойност=False)
        машина.Команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for невалиден_мярка in [
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
            редакция_стойност(машина, 'Calc.java', невалиден_мярка)
            машина.Команда('javac Calc.java', ['javac error:', 'Exit: 1'])
            машина.Команда('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # спринт_стойност 실행은 потребител 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            машина.Команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        машина.Команда('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        машина.Команда('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        редакция_стойност(машина, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        машина.Команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        машина.Команда('java Calc', ['instruction limit', 'Exit: 1'])
        машина.Команда('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        редакция_стойност(машина, 'Bad.class', 'garbage')
        машина.Команда('java Bad', ['JVM error:', 'Exit: 1'])
        машина.Команда('rm Bad.class', ['Removed'])
        машина.Команда('java Bad', ['cannot read class: -2'])
        # редакция_стойност 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Стартиране = len(машина.регистрирам_запис)
        машина.직렬.sendall(b'edit Hello.java\n')
        машина.състояние_на_изчакване('...> ', Стартиране)
        Стартиране = len(машина.регистрирам_запис)
        машина.직렬.sendall(b'x' * 129 + b'\n')
        машина.състояние_на_изчакване('...> ', Стартиране)
        машина.Команда('.save', ['Too much input; original preserved'])
        машина.Команда('javac Hello.java', ['Compiled:', 'Exit: 0'])
        редакция_стойност(машина, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            редакция_стойност(машина, 'f' + str(수), 'occupied')
        машина.Команда('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        машина.Команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in машина.регистрирам_запис.decode('utf-8', 'replace')
        РЕЗУЛТАТ['serial'] = машина.регистрирам_запис.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return РЕЗУЛТАТ
    finally:
        машина.Затворен()


def 주코드(данни):
    """손상 시험용 main Code의 действителен_данни Файл 오프셋/길이만 읽는다."""
    позиция_стойност = 8
    def 짧():
        nonlocal позиция_стойност
        стойност = struct.unpack_from('>H', данни, позиция_стойност)[0]
        позиция_стойност += 2
        return стойност
    def 정():
        nonlocal позиция_стойност
        стойност = struct.unpack_from('>I', данни, позиция_стойност)[0]
        позиция_стойност += 4
        return стойност
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = данни[позиция_стойност]
        позиция_стойност += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[수] = данни[позиция_стойност:позиция_стойност + 길이]
            позиция_стойност += 길이
        elif 종류 in (7, 8): позиция_стойност += 2
        elif 종류 in (3, 9, 10, 12): позиция_стойност += 4
        else: raise AssertionError(종류)
    позиция_стойност += 6
    개수 = 짧()
    позиция_стойност += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Име = 짧()
        짧()
        for 수 in range(짧()):
            атрибут_стойност = 짧()
            Размер = 정()
            if 문자들[Име] == b'main' and 문자들[атрибут_стойност] == b'Code':
                return позиция_стойност + 8, struct.unpack_from('>I', данни, позиция_стойност + 4)[0]
            позиция_стойност += Размер
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        указател_стойност = Path(임시)
        (указател_стойност / 'build').mkdir()
        ИЗТОЧНИК = указател_стойност / 'Imported.java'
        ИЗТОЧНИК.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ИЗТОЧНИК)], check=True)
        원본 = (указател_стойност / 'Imported.class').read_bytes()
        код_стойност, 길이 = 주코드(원본)
        변형 = {}
        данни = bytearray(원본); данни[0] = 0; 변형['BadMagic'] = данни
        данни = bytearray(원본); данни[7] = 61; 변형['BadVer'] = данни
        данни = bytearray(원본); данни[8:10] = b'\xff\xff'; 변형['BadPool'] = данни
        данни = bytearray(원본); данни[код_стойност:код_стойност + 길이] = bytes(길이)
        данни[код_стойност:код_стойност + 3] = b'\xa7\x00\x01'; данни[код_стойност + 길이 - 1] = 177; 변형['BadJump'] = данни
        данни = bytearray(원본); данни[код_стойност:код_стойност + 길이] = bytes(길이)
        данни[код_стойност] = 87; данни[код_стойност + 길이 - 1] = 177; 변형['BadStack'] = данни
        # Име 검사를 통과시켜 действителен_данни изпълнявам_команда 중의 операнд_стек 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        запис_стойност = ['Imported.class=' + str(указател_стойност / 'Imported.class'), 'Imported.java=' + str(ИЗТОЧНИК)]
        for Име, данни in 변형.items():
            ПЪТ = указател_стойност / (Име + '.class'); ПЪТ.write_bytes(данни)
            запис_стойност.append(Име + '.class=' + str(ПЪТ))
        Група_стойност = указател_стойност / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Позиция / 'Инструменти/자바파일묶기.py'), '-o', str(Група_стойност)] + запис_стойност, check=True)
        subprocess.run(['as', '--32', '-o', str(указател_стойност / 'user.o'), str(Позиция / '부팅/потребител.s')], cwd=str(указател_стойност), check=True)
        ядро_стойност = указател_стойност / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Позиция / '부팅/Връзка_схема.ld'), '-o', str(ядро_стойност),
                        str(Позиция / 'build/boot.o'), str(Позиция / 'build/java.o'), str(указател_стойност / 'user.o'), str(Позиция / 'build/apps.o')], check=True)
        машина = виртуална_машина(ядро_стойност, мрежа_стойност=False)
        try:
            машина.Команда('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            машина.Команда('cat Imported.java', ['int[] values = new int[3]'])
            for Име, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                машина.Команда('java ' + Име, [문구, 'Exit: 1'])
                машина.Команда('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return машина.регистрирам_запис.decode('utf-8', 'replace')
        finally:
            машина.Затворен()


if __name__ == '__main__':
    анализирам_стойност = argparse.ArgumentParser()
    анализирам_стойност.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Параметри = анализирам_стойност.parse_args()
    РЕЗУЛТАТ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Параметри.boot == 'both' else (Параметри.boot,))}
    РЕЗУЛТАТ['import'] = 적재시험()
    (Позиция / 'build/자바시험.json').write_text(json.dumps(РЕЗУЛТАТ, ensure_ascii=False, indent=2) + '\n')
