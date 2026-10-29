#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 аткаруу_буйрук, натыйжасыз_маани/ресурс_маани 경계 시험."""
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
from 사용자통신시험 import виртуалдык_машина, Турган_жери


def түзөтүү_маани(машина, Аты, Мазмун_маани, сактагыч_маани=True):
    Жүргүзүү = len(машина.жазуу_катар)
    машина.직렬.sendall(('edit ' + Аты + '\n').encode())
    машина.기다림('...> ', Жүргүзүү)
    for сап in Мазмун_маани.splitlines():
        assert len(сап) <= 128
        Жүргүзүү = len(машина.жазуу_катар)
        машина.직렬.sendall((сап + '\n').encode())
        машина.기다림('...> ', Жүргүзүү)
    Жүргүзүү = len(машина.жазуу_катар)
    машина.직렬.sendall(b'.save\n' if сактагыч_маани else b'.cancel\n')
    결과 = машина.기다림('jkoros> ', Жүргүзүү)
    assert ('Saved:' if сактагыч_маани else 'Cancelled; original preserved') in 결과, 결과


def файл_дарек():
    결과 = subprocess.check_output(['nm', '-n', str(Турган_жери / 'build/kernel.elf')], universal_newlines=True)
    for сап in 결과.splitlines():
        if сап.endswith(' ram_files'):
            return int(сап.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(машина, оюкча_маани, Өлчөмү, ЖОЛ):
    # 시험 VM의 메모리에서 актуалдуу_берилмелер 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    дарек = файл_дарек() + оюкча_маани * 16384
    машина.монитор_маани.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(дарек, Өлчөмү, ЖОЛ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ЖОЛ.exists() and ЖОЛ.stat().st_size == Өлчөмү:
            return ЖОЛ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    машина = виртуалдык_машина(Турган_жери / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Желе_маани=False)
    결과 = {}
    try:
        машина.Команда('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        машина.Команда('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        машина.Команда('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        машина.Команда('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        машина.Команда('java Missing', ['cannot read class: -2', 'Exit: 1'])
        машина.Команда('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        машина.Команда('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Мазмун_маани = '''public class Calc {
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
        түзөтүү_маани(машина, 'Calc.java', Мазмун_маани)
        машина.Команда('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Чыгыш = машина.Команда('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = Чыгыш
        киргизме_жазуу_Тизме = машина.Команда('ls', ['Calc.class'])
        Өлчөмү = int(re.search(r'Calc\.class\s+(\d+) bytes', киргизме_жазуу_Тизме).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as каталог_маани:
            ЖОЛ = Path(каталог_маани) / 'Calc.class'
            берилмелер = 게스트파일(машина, 3, Өлчөмү, ЖОЛ)
            актуалдуу_берилмелер = subprocess.check_output(['java', '-Xverify:all', '-cp', каталог_маани, 'Calc', '6', 'guest'], universal_newlines=True)
            assert актуалдуу_берилмелер.splitlines() == 기대, актуалдуу_берилмелер
            결과['class_sha256'] = hashlib.sha256(берилмелер).hexdigest()
            결과['openjdk_output'] = актуалдуу_берилмелер
        # 실패한 түзөтүү_маани/컴파일은 기존 class를 보존한다.
        түзөтүү_маани(машина, 'Calc.java', 'not Java at all', сактагыч_маани=False)
        машина.Команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for 잘못 in [
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
            түзөтүү_маани(машина, 'Calc.java', 잘못)
            машина.Команда('javac Calc.java', ['javac error:', 'Exit: 1'])
            машина.Команда('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # итерация_маани 실행은 колдонуучу 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            машина.Команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        машина.Команда('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        машина.Команда('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        түзөтүү_маани(машина, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        машина.Команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        машина.Команда('java Calc', ['instruction limit', 'Exit: 1'])
        машина.Команда('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        түзөтүү_маани(машина, 'Bad.class', 'garbage')
        машина.Команда('java Bad', ['JVM error:', 'Exit: 1'])
        машина.Команда('rm Bad.class', ['Removed'])
        машина.Команда('java Bad', ['cannot read class: -2'])
        # түзөтүү_маани 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Жүргүзүү = len(машина.жазуу_катар)
        машина.직렬.sendall(b'edit Hello.java\n')
        машина.기다림('...> ', Жүргүзүү)
        Жүргүзүү = len(машина.жазуу_катар)
        машина.직렬.sendall(b'x' * 129 + b'\n')
        машина.기다림('...> ', Жүргүзүү)
        машина.Команда('.save', ['Too much input; original preserved'])
        машина.Команда('javac Hello.java', ['Compiled:', 'Exit: 0'])
        түзөтүү_маани(машина, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            түзөтүү_маани(машина, 'f' + str(수), 'occupied')
        машина.Команда('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        машина.Команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in машина.жазуу_катар.decode('utf-8', 'replace')
        결과['serial'] = машина.жазуу_катар.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        машина.Жабуу()


def 주코드(берилмелер):
    """손상 시험용 main Code의 актуалдуу_берилмелер Файл 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        маани = struct.unpack_from('>H', берилмелер, 위치값)[0]
        위치값 += 2
        return маани
    def 정():
        nonlocal 위치값
        маани = struct.unpack_from('>I', берилмелер, 위치값)[0]
        위치값 += 4
        return маани
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = берилмелер[위치값]
        위치값 += 1
        if 종류 == 1:
            узундук_маани = 짧()
            문자들[수] = берилмелер[위치값:위치값 + узундук_маани]
            위치값 += узундук_маани
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Аты = 짧()
        짧()
        for 수 in range(짧()):
            атрибут_маани = 짧()
            Өлчөмү = 정()
            if 문자들[Аты] == b'main' and 문자들[атрибут_маани] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', берилмелер, 위치값 + 4)[0]
            위치값 += Өлчөмү
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        каталог_маани = Path(임시)
        (каталог_маани / 'build').mkdir()
        Булак = каталог_маани / 'Imported.java'
        Булак.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Булак)], check=True)
        원본 = (каталог_маани / 'Imported.class').read_bytes()
        코드, узундук_маани = 주코드(원본)
        변형 = {}
        берилмелер = bytearray(원본); берилмелер[0] = 0; 변형['BadMagic'] = берилмелер
        берилмелер = bytearray(원본); берилмелер[7] = 61; 변형['BadVer'] = берилмелер
        берилмелер = bytearray(원본); берилмелер[8:10] = b'\xff\xff'; 변형['BadPool'] = берилмелер
        берилмелер = bytearray(원본); берилмелер[코드:코드 + узундук_маани] = bytes(узундук_маани)
        берилмелер[코드:코드 + 3] = b'\xa7\x00\x01'; берилмелер[코드 + узундук_маани - 1] = 177; 변형['BadJump'] = берилмелер
        берилмелер = bytearray(원본); берилмелер[코드:코드 + узундук_маани] = bytes(узундук_маани)
        берилмелер[코드] = 87; берилмелер[코드 + узундук_маани - 1] = 177; 변형['BadStack'] = берилмелер
        # Аты 검사를 통과시켜 актуалдуу_берилмелер аткаруу_буйрук 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        киргизме_жазуу_маани = ['Imported.class=' + str(каталог_маани / 'Imported.class'), 'Imported.java=' + str(Булак)]
        for Аты, берилмелер in 변형.items():
            ЖОЛ = каталог_маани / (Аты + '.class'); ЖОЛ.write_bytes(берилмелер)
            киргизме_жазуу_маани.append(Аты + '.class=' + str(ЖОЛ))
        топ_маани = каталог_маани / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Турган_жери / 'Куралдар/자바파일묶기.py'), '-o', str(топ_маани)] + киргизме_жазуу_маани, check=True)
        subprocess.run(['as', '--32', '-o', str(каталог_маани / 'user.o'), str(Турган_жери / '부팅/колдонуучу.s')], cwd=str(каталог_маани), check=True)
        өзөк_маани = каталог_маани / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Турган_жери / '부팅/Шилтеме_түзүлүш.ld'), '-o', str(өзөк_маани),
                        str(Турган_жери / 'build/boot.o'), str(Турган_жери / 'build/java.o'), str(каталог_маани / 'user.o'), str(Турган_жери / 'build/apps.o')], check=True)
        машина = виртуалдык_машина(өзөк_маани, Желе_маани=False)
        try:
            машина.Команда('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            машина.Команда('cat Imported.java', ['int[] values = new int[3]'])
            for Аты, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                машина.Команда('java ' + Аты, [문구, 'Exit: 1'])
                машина.Команда('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return машина.жазуу_катар.decode('utf-8', 'replace')
        finally:
            машина.Жабуу()


if __name__ == '__main__':
    талдоо_маани = argparse.ArgumentParser()
    талдоо_маани.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = талдоо_маани.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (Турган_жери / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
