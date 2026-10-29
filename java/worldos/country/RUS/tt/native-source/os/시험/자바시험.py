#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 үтәргә_команда, эштән_туктау_VALUE/ресурс_VALUE 경계 시험."""
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
from 사용자통신시험 import виртуаль_машина, урнаштыру


def төзәтү_VALUE(машина, исем, Эчтәлек_VALUE, Store_VALUE=True):
    эшләтү = len(машина.LOG_юл)
    машина.직렬.sendall(('edit ' + исем + '\n').encode())
    машина.기다림('...> ', эшләтү)
    for юл in Эчтәлек_VALUE.splitlines():
        assert len(юл) <= 128
        эшләтү = len(машина.LOG_юл)
        машина.직렬.sendall((юл + '\n').encode())
        машина.기다림('...> ', эшләтү)
    эшләтү = len(машина.LOG_юл)
    машина.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    үлчәм = машина.기다림('jkoros> ', эшләтү)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in үлчәм, үлчәм


def файл_адрес():
    үлчәм = subprocess.check_output(['nm', '-n', str(урнаштыру / 'build/kernel.elf')], universal_newlines=True)
    for юл in үлчәм.splitlines():
        if юл.endswith(' ram_files'):
            return int(юл.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def кунак_файл(машина, оя_VALUE, үлчәмен_үзгәртү, Yul):
    # 시험 VM의 메모리에서 фактик_мәгълүмат 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    адрес = файл_адрес() + оя_VALUE * 16384
    машина.монитор_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(адрес, үлчәмен_үзгәртү, Yul)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Yul.exists() and Yul.stat().st_size == үлчәмен_үзгәртү:
            return Yul.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    машина = виртуаль_машина(урнаштыру / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Челтәр_VALUE=False)
    үлчәм = {}
    try:
        машина.команда('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        машина.команда('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        машина.команда('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        машина.команда('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        машина.команда('java Missing', ['cannot read class: -2', 'Exit: 1'])
        машина.команда('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        машина.команда('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Эчтәлек_VALUE = '''public class Calc {
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
        төзәтү_VALUE(машина, 'Calc.java', Эчтәлек_VALUE)
        машина.команда('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = машина.команда('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        үлчәм['guest_output'] = 출력
        кертү_Исемлек = машина.команда('ls', ['Calc.class'])
        үлчәмен_үзгәртү = int(re.search(r'Calc\.class\s+(\d+) bytes', кертү_Исемлек).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as каталог_VALUE:
            Yul = Path(каталог_VALUE) / 'Calc.class'
            мәгълүмат = кунак_файл(машина, 3, үлчәмен_үзгәртү, Yul)
            фактик_мәгълүмат = subprocess.check_output(['java', '-Xverify:all', '-cp', каталог_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert фактик_мәгълүмат.splitlines() == 기대, фактик_мәгълүмат
            үлчәм['class_sha256'] = hashlib.sha256(мәгълүмат).hexdigest()
            үлчәм['openjdk_output'] = фактик_мәгълүмат
        # 실패한 төзәтү_VALUE/컴파일은 기존 class를 보존한다.
        төзәтү_VALUE(машина, 'Calc.java', 'not Java at all', Store_VALUE=False)
        машина.команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for дөрес_булмаган_үлчәм in [
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
            төзәтү_VALUE(машина, 'Calc.java', дөрес_булмаган_үлчәм)
            машина.команда('javac Calc.java', ['javac error:', 'Exit: 1'])
            машина.команда('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # итерация_VALUE 실행은 кулланучы 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            машина.команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        машина.команда('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        машина.команда('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        төзәтү_VALUE(машина, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        машина.команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        машина.команда('java Calc', ['instruction limit', 'Exit: 1'])
        машина.команда('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        төзәтү_VALUE(машина, 'Bad.class', 'garbage')
        машина.команда('java Bad', ['JVM error:', 'Exit: 1'])
        машина.команда('rm Bad.class', ['Removed'])
        машина.команда('java Bad', ['cannot read class: -2'])
        # төзәтү_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        эшләтү = len(машина.LOG_юл)
        машина.직렬.sendall(b'edit Hello.java\n')
        машина.기다림('...> ', эшләтү)
        эшләтү = len(машина.LOG_юл)
        машина.직렬.sendall(b'x' * 129 + b'\n')
        машина.기다림('...> ', эшләтү)
        машина.команда('.save', ['Too much input; original preserved'])
        машина.команда('javac Hello.java', ['Compiled:', 'Exit: 0'])
        төзәтү_VALUE(машина, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            төзәтү_VALUE(машина, 'f' + str(수), 'occupied')
        машина.команда('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        машина.команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in машина.LOG_юл.decode('utf-8', 'replace')
        үлчәм['serial'] = машина.LOG_юл.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return үлчәм
    finally:
        машина.Yap()


def 주코드(мәгълүмат):
    """손상 시험용 main Code의 фактик_мәгълүмат Birem 오프셋/길이만 읽는다."""
    урнаштыру_VALUE = 8
    def 짧():
        nonlocal урнаштыру_VALUE
        VALUE = struct.unpack_from('>H', мәгълүмат, урнаштыру_VALUE)[0]
        урнаштыру_VALUE += 2
        return VALUE
    def 정():
        nonlocal урнаштыру_VALUE
        VALUE = struct.unpack_from('>I', мәгълүмат, урнаштыру_VALUE)[0]
        урнаштыру_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = мәгълүмат[урнаштыру_VALUE]
        урнаштыру_VALUE += 1
        if 종류 == 1:
            озынлык_VALUE = 짧()
            문자들[수] = мәгълүмат[урнаштыру_VALUE:урнаштыру_VALUE + озынлык_VALUE]
            урнаштыру_VALUE += озынлык_VALUE
        elif 종류 in (7, 8): урнаштыру_VALUE += 2
        elif 종류 in (3, 9, 10, 12): урнаштыру_VALUE += 4
        else: raise AssertionError(종류)
    урнаштыру_VALUE += 6
    элемент_COUNT = 짧()
    урнаштыру_VALUE += элемент_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        исем = 짧()
        짧()
        for 수 in range(짧()):
            аергыч_VALUE_286d43f0 = 짧()
            үлчәмен_үзгәртү = 정()
            if 문자들[исем] == b'main' and 문자들[аергыч_VALUE_286d43f0] == b'Code':
                return урнаштыру_VALUE + 8, struct.unpack_from('>I', мәгълүмат, урнаштыру_VALUE + 4)[0]
            урнаштыру_VALUE += үлчәмен_үзгәртү
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        каталог_VALUE = Path(임시)
        (каталог_VALUE / 'build').mkdir()
        чыганак = каталог_VALUE / 'Imported.java'
        чыганак.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(чыганак)], check=True)
        원본 = (каталог_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, озынлык_VALUE = 주코드(원본)
        변형 = {}
        мәгълүмат = bytearray(원본); мәгълүмат[0] = 0; 변형['BadMagic'] = мәгълүмат
        мәгълүмат = bytearray(원본); мәгълүмат[7] = 61; 변형['BadVer'] = мәгълүмат
        мәгълүмат = bytearray(원본); мәгълүмат[8:10] = b'\xff\xff'; 변형['BadPool'] = мәгълүмат
        мәгълүмат = bytearray(원본); мәгълүмат[CODE_VALUE:CODE_VALUE + озынлык_VALUE] = bytes(озынлык_VALUE)
        мәгълүмат[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; мәгълүмат[CODE_VALUE + озынлык_VALUE - 1] = 177; 변형['BadJump'] = мәгълүмат
        мәгълүмат = bytearray(원본); мәгълүмат[CODE_VALUE:CODE_VALUE + озынлык_VALUE] = bytes(озынлык_VALUE)
        мәгълүмат[CODE_VALUE] = 87; мәгълүмат[CODE_VALUE + озынлык_VALUE - 1] = 177; 변형['BadStack'] = мәгълүмат
        # исем 검사를 통과시켜 фактик_мәгълүмат үтәргә_команда 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        кертү_VALUE = ['Imported.class=' + str(каталог_VALUE / 'Imported.class'), 'Imported.java=' + str(чыганак)]
        for исем, мәгълүмат in 변형.items():
            Yul = каталог_VALUE / (исем + '.class'); Yul.write_bytes(мәгълүмат)
            кертү_VALUE.append(исем + '.class=' + str(Yul))
        төркем_VALUE = каталог_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(урнаштыру / 'Кораллар/자바파일묶기.py'), '-o', str(төркем_VALUE)] + кертү_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(каталог_VALUE / 'user.o'), str(урнаштыру / '부팅/кулланучы.s')], cwd=str(каталог_VALUE), check=True)
        төш_VALUE = каталог_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(урнаштыру / '부팅/бәйләү_план.ld'), '-o', str(төш_VALUE),
                        str(урнаштыру / 'build/boot.o'), str(урнаштыру / 'build/java.o'), str(каталог_VALUE / 'user.o'), str(урнаштыру / 'build/apps.o')], check=True)
        машина = виртуаль_машина(төш_VALUE, Челтәр_VALUE=False)
        try:
            машина.команда('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            машина.команда('cat Imported.java', ['int[] values = new int[3]'])
            for исем, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                машина.команда('java ' + исем, [문구, 'Exit: 1'])
                машина.команда('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return машина.LOG_юл.decode('utf-8', 'replace')
        finally:
            машина.Yap()


if __name__ == '__main__':
    бүлү_VALUE = argparse.ArgumentParser()
    бүлү_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = бүлү_VALUE.parse_args()
    үлчәм = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    үлчәм['import'] = 적재시험()
    (урнаштыру / 'build/자바시험.json').write_text(json.dumps(үлчәм, ensure_ascii=False, indent=2) + '\n')
