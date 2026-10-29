#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 실행, сбой_ЗНАЧЕН/ресурс_ЗНАЧЕН граница_ЗНАЧЕН испытания."""
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
from тест_пользователь_сеть import VM, позиция


def правка_ЗНАЧЕН(компьютер_5eb260fa, Название, контент_ЗНАЧЕН, Store_ЗНАЧЕН=True):
    запустить = len(компьютер_5eb260fa.LOG_ЗАПИСЬ)
    компьютер_5eb260fa.직렬.sendall(('edit ' + Название + '\n').encode())
    компьютер_5eb260fa.состояние_ожидания('...> ', запустить)
    for строка_ввода in контент_ЗНАЧЕН.splitlines():
        assert len(строка_ввода) <= 128
        запустить = len(компьютер_5eb260fa.LOG_ЗАПИСЬ)
        компьютер_5eb260fa.직렬.sendall((строка_ввода + '\n').encode())
        компьютер_5eb260fa.состояние_ожидания('...> ', запустить)
    запустить = len(компьютер_5eb260fa.LOG_ЗАПИСЬ)
    компьютер_5eb260fa.직렬.sendall(b'.save\n' if Store_ЗНАЧЕН else b'.cancel\n')
    результат = компьютер_5eb260fa.состояние_ожидания('jkoros> ', запустить)
    assert ('Saved:' if Store_ЗНАЧЕН else 'Cancelled; original preserved') in результат, результат


def файл_АДРЕС():
    результат = subprocess.check_output(['nm', '-n', str(позиция / 'build/kernel.elf')], universal_newlines=True)
    for строка_ввода in результат.splitlines():
        if строка_ввода.endswith(' ram_files'):
            return int(строка_ввода.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def гость_файл(компьютер_5eb260fa, слот_ЗНАЧЕН, Размер, путь):
    # испытания VM의 메모리에서 фактический_данные 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    АДРЕС = файл_АДРЕС() + слот_ЗНАЧЕН * 16384
    компьютер_5eb260fa.монитор_ЗНАЧЕН.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(АДРЕС, Размер, путь)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if путь.exists() and путь.stat().st_size == Размер:
            return путь.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def тестовый_запуск(Вид_ЗНАЧЕН):
    компьютер_5eb260fa = VM(позиция / ('build/kernel.elf' if Вид_ЗНАЧЕН == 'elf' else 'build/kernel.iso'), Вид_ЗНАЧЕН, сеть_ЗНАЧЕН=False)
    результат = {}
    try:
        компьютер_5eb260fa.команда('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        компьютер_5eb260fa.команда('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        компьютер_5eb260fa.команда('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        компьютер_5eb260fa.команда('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        компьютер_5eb260fa.команда('java Missing', ['cannot read class: -2', 'Exit: 1'])
        компьютер_5eb260fa.команда('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        компьютер_5eb260fa.команда('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        контент_ЗНАЧЕН = '''public class Calc {
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
        правка_ЗНАЧЕН(компьютер_5eb260fa, 'Calc.java', контент_ЗНАЧЕН)
        компьютер_5eb260fa.команда('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        текстовыйВывод = компьютер_5eb260fa.команда('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        результат['guest_output'] = текстовыйВывод
        ввод_Список = компьютер_5eb260fa.команда('ls', ['Calc.class'])
        Размер = int(re.search(r'Calc\.class\s+(\d+) bytes', ввод_Список).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Каталог_ЗНАЧЕН:
            путь = Path(Каталог_ЗНАЧЕН) / 'Calc.class'
            данные = гость_файл(компьютер_5eb260fa, 3, Размер, путь)
            фактический_данные = subprocess.check_output(['java', '-Xverify:all', '-cp', Каталог_ЗНАЧЕН, 'Calc', '6', 'guest'], universal_newlines=True)
            assert фактический_данные.splitlines() == 기대, фактический_данные
            результат['class_sha256'] = hashlib.sha256(данные).hexdigest()
            результат['openjdk_output'] = фактический_данные
        # 실패한 правка_ЗНАЧЕН/컴파일은 기존 class를 보존한다.
        правка_ЗНАЧЕН(компьютер_5eb260fa, 'Calc.java', 'not Java at all', Store_ЗНАЧЕН=False)
        компьютер_5eb260fa.команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for неверный_KR in [
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
            правка_ЗНАЧЕН(компьютер_5eb260fa, 'Calc.java', неверный_KR)
            компьютер_5eb260fa.команда('javac Calc.java', ['javac error:', 'Exit: 1'])
            компьютер_5eb260fa.команда('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # спринт_ЗНАЧЕН 실행은 пространство_пользователя куча_ЗНАЧЕН/프레임을 매번 초기화한다.
        for 수 in range(12):
            компьютер_5eb260fa.команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        компьютер_5eb260fa.команда('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        компьютер_5eb260fa.команда('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        правка_ЗНАЧЕН(компьютер_5eb260fa, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        компьютер_5eb260fa.команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        компьютер_5eb260fa.команда('java Calc', ['instruction limit', 'Exit: 1'])
        компьютер_5eb260fa.команда('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        правка_ЗНАЧЕН(компьютер_5eb260fa, 'Bad.class', 'garbage')
        компьютер_5eb260fa.команда('java Bad', ['JVM error:', 'Exit: 1'])
        компьютер_5eb260fa.команда('rm Bad.class', ['Removed'])
        компьютер_5eb260fa.команда('java Bad', ['cannot read class: -2'])
        # правка_ЗНАЧЕН 입력의 넘친 부분을 잘라서 저장하지 않는다.
        запустить = len(компьютер_5eb260fa.LOG_ЗАПИСЬ)
        компьютер_5eb260fa.직렬.sendall(b'edit Hello.java\n')
        компьютер_5eb260fa.состояние_ожидания('...> ', запустить)
        запустить = len(компьютер_5eb260fa.LOG_ЗАПИСЬ)
        компьютер_5eb260fa.직렬.sendall(b'x' * 129 + b'\n')
        компьютер_5eb260fa.состояние_ожидания('...> ', запустить)
        компьютер_5eb260fa.команда('.save', ['Too much input; original preserved'])
        компьютер_5eb260fa.команда('javac Hello.java', ['Compiled:', 'Exit: 0'])
        правка_ЗНАЧЕН(компьютер_5eb260fa, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            правка_ЗНАЧЕН(компьютер_5eb260fa, 'f' + str(수), 'occupied')
        компьютер_5eb260fa.команда('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        компьютер_5eb260fa.команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
        результат['serial'] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(Вид_ЗНАЧЕН))
        return результат
    finally:
        компьютер_5eb260fa.Закрыть()


def 주코드(данные):
    """손상 시험용 main Code의 фактический_данные файл 오프셋/길이만 읽는다."""
    позиция_ЗНАЧЕН = 8
    def 짧():
        nonlocal позиция_ЗНАЧЕН
        ЗНАЧЕН = struct.unpack_from('>H', данные, позиция_ЗНАЧЕН)[0]
        позиция_ЗНАЧЕН += 2
        return ЗНАЧЕН
    def чтение_целое_число_без_знака():
        nonlocal позиция_ЗНАЧЕН
        ЗНАЧЕН = struct.unpack_from('>I', данные, позиция_ЗНАЧЕН)[0]
        позиция_ЗНАЧЕН += 4
        return ЗНАЧЕН
    문자들 = {}
    for 수 in range(1, 짧()):
        Вид_ЗНАЧЕН = данные[позиция_ЗНАЧЕН]
        позиция_ЗНАЧЕН += 1
        if Вид_ЗНАЧЕН == 1:
            длина_ЗНАЧЕН = 짧()
            문자들[수] = данные[позиция_ЗНАЧЕН:позиция_ЗНАЧЕН + длина_ЗНАЧЕН]
            позиция_ЗНАЧЕН += длина_ЗНАЧЕН
        elif Вид_ЗНАЧЕН in (7, 8): позиция_ЗНАЧЕН += 2
        elif Вид_ЗНАЧЕН in (3, 9, 10, 12): позиция_ЗНАЧЕН += 4
        else: raise AssertionError(Вид_ЗНАЧЕН)
    позиция_ЗНАЧЕН += 6
    товар_СЧЁТ = 짧()
    позиция_ЗНАЧЕН += товар_СЧЁТ * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Название = 짧()
        짧()
        for 수 in range(짧()):
            значение_атрибута = 짧()
            Размер = чтение_целое_число_без_знака()
            if 문자들[Название] == b'main' and 문자들[значение_атрибута] == b'Code':
                return позиция_ЗНАЧЕН + 8, struct.unpack_from('>I', данные, позиция_ЗНАЧЕН + 4)[0]
            позиция_ЗНАЧЕН += Размер
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Каталог_ЗНАЧЕН = Path(임시)
        (Каталог_ЗНАЧЕН / 'build').mkdir()
        исходныйКод = Каталог_ЗНАЧЕН / 'Imported.java'
        исходныйКод.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(исходныйКод)], check=True)
        원본 = (Каталог_ЗНАЧЕН / 'Imported.class').read_bytes()
        кодовое_значение, длина_ЗНАЧЕН = 주코드(원본)
        вариант_ЗНАЧЕН = {}
        данные = bytearray(원본); данные[0] = 0; вариант_ЗНАЧЕН['BadMagic'] = данные
        данные = bytearray(원본); данные[7] = 61; вариант_ЗНАЧЕН['BadVer'] = данные
        данные = bytearray(원본); данные[8:10] = b'\xff\xff'; вариант_ЗНАЧЕН['BadPool'] = данные
        данные = bytearray(원본); данные[кодовое_значение:кодовое_значение + длина_ЗНАЧЕН] = bytes(длина_ЗНАЧЕН)
        данные[кодовое_значение:кодовое_значение + 3] = b'\xa7\x00\x01'; данные[кодовое_значение + длина_ЗНАЧЕН - 1] = 177; вариант_ЗНАЧЕН['BadJump'] = данные
        данные = bytearray(원본); данные[кодовое_значение:кодовое_значение + длина_ЗНАЧЕН] = bytes(длина_ЗНАЧЕН)
        данные[кодовое_значение] = 87; данные[кодовое_значение + длина_ЗНАЧЕН - 1] = 177; вариант_ЗНАЧЕН['BadStack'] = данные
        # Название 검사를 통과시켜 фактический_данные 실행 중의 операнд_стек 오류까지 검사한다.
        вариант_ЗНАЧЕН['BadStack'] = вариант_ЗНАЧЕН['BadStack'].replace(b'Imported', b'BadStack')
        ввод_ЗНАЧЕН = ['Imported.class=' + str(Каталог_ЗНАЧЕН / 'Imported.class'), 'Imported.java=' + str(исходныйКод)]
        for Название, данные in вариант_ЗНАЧЕН.items():
            путь = Каталог_ЗНАЧЕН / (Название + '.class'); путь.write_bytes(данные)
            ввод_ЗНАЧЕН.append(Название + '.class=' + str(путь))
        Группа_ЗНАЧЕН = Каталог_ЗНАЧЕН / 'build/java-files.bin'
        subprocess.run([sys.executable, str(позиция / 'инструменты/자바파일묶기.py'), '-o', str(Группа_ЗНАЧЕН)] + ввод_ЗНАЧЕН, check=True)
        subprocess.run(['as', '--32', '-o', str(Каталог_ЗНАЧЕН / 'user.o'), str(позиция / 'запуск_машины/пространство_пользователя.s')], cwd=str(Каталог_ЗНАЧЕН), check=True)
        ядро_ЗНАЧЕН = Каталог_ЗНАЧЕН / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(позиция / 'запуск_машины/схема_компоновки.ld'), '-o', str(ядро_ЗНАЧЕН),
                        str(позиция / 'build/boot.o'), str(позиция / 'build/java.o'), str(Каталог_ЗНАЧЕН / 'user.o'), str(позиция / 'build/apps.o')], check=True)
        компьютер_5eb260fa = VM(ядро_ЗНАЧЕН, сеть_ЗНАЧЕН=False)
        try:
            компьютер_5eb260fa.команда('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            компьютер_5eb260fa.команда('cat Imported.java', ['int[] values = new int[3]'])
            for Название, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                компьютер_5eb260fa.команда('java ' + Название, [문구, 'Exit: 1'])
                компьютер_5eb260fa.команда('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
        finally:
            компьютер_5eb260fa.Закрыть()


if __name__ == '__main__':
    анализировать_ЗНАЧЕН = argparse.ArgumentParser()
    анализировать_ЗНАЧЕН.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    аргументы = анализировать_ЗНАЧЕН.parse_args()
    результат = {Вид_ЗНАЧЕН: тестовый_запуск(Вид_ЗНАЧЕН) for Вид_ЗНАЧЕН in (('elf', 'iso') if аргументы.boot == 'both' else (аргументы.boot,))}
    результат['import'] = 적재시험()
    (позиция / 'build/자바시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2) + '\n')
