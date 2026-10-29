#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 орындау_пәрмен, қате_мән/ресурс_мән 경계 시험."""
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
from 사용자통신시험 import виртуалды_машина, Орны


def өңдеу_мән(компьютер, Аты, мазмұн_мән, сақтау_мән=True):
    Орындау_2 = len(компьютер.журнал_жол)
    компьютер.직렬.sendall(('edit ' + Аты + '\n').encode())
    компьютер.күту_күйі('...> ', Орындау_2)
    for Жол in мазмұн_мән.splitlines():
        assert len(Жол) <= 128
        Орындау_2 = len(компьютер.журнал_жол)
        компьютер.직렬.sendall((Жол + '\n').encode())
        компьютер.күту_күйі('...> ', Орындау_2)
    Орындау_2 = len(компьютер.журнал_жол)
    компьютер.직렬.sendall(b'.save\n' if сақтау_мән else b'.cancel\n')
    НӘТИЖЕ = компьютер.күту_күйі('jkoros> ', Орындау_2)
    assert ('Saved:' if сақтау_мән else 'Cancelled; original preserved') in НӘТИЖЕ, НӘТИЖЕ


def файл_мекенжай():
    НӘТИЖЕ = subprocess.check_output(['nm', '-n', str(Орны / 'build/kernel.elf')], universal_newlines=True)
    for Жол in НӘТИЖЕ.splitlines():
        if Жол.endswith(' ram_files'):
            return int(Жол.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def қонақ_файл(компьютер, 슬롯, Өлшемі, Жол_2):
    # 시험 VM의 메모리에서 нақты_деректер 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    мекенжай = файл_мекенжай() + 슬롯 * 16384
    компьютер.бақылау_мән.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(мекенжай, Өлшемі, Жол_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Жол_2.exists() and Жол_2.stat().st_size == Өлшемі:
            return Жол_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    компьютер = виртуалды_машина(Орны / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, желі_мән=False)
    НӘТИЖЕ = {}
    try:
        компьютер.Команда('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        компьютер.Команда('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        компьютер.Команда('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        компьютер.Команда('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        компьютер.Команда('java Missing', ['cannot read class: -2', 'Exit: 1'])
        компьютер.Команда('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        компьютер.Команда('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        мазмұн_мән = '''public class Calc {
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
        өңдеу_мән(компьютер, 'Calc.java', мазмұн_мән)
        компьютер.Команда('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Шығысы = компьютер.Команда('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        НӘТИЖЕ['guest_output'] = Шығысы
        енгізу_Тізім = компьютер.Команда('ls', ['Calc.class'])
        Өлшемі = int(re.search(r'Calc\.class\s+(\d+) bytes', енгізу_Тізім).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as каталог_мән:
            Жол_2 = Path(каталог_мән) / 'Calc.class'
            деректер = қонақ_файл(компьютер, 3, Өлшемі, Жол_2)
            нақты_деректер = subprocess.check_output(['java', '-Xverify:all', '-cp', каталог_мән, 'Calc', '6', 'guest'], universal_newlines=True)
            assert нақты_деректер.splitlines() == 기대, нақты_деректер
            НӘТИЖЕ['class_sha256'] = hashlib.sha256(деректер).hexdigest()
            НӘТИЖЕ['openjdk_output'] = нақты_деректер
        # 실패한 өңдеу_мән/컴파일은 기존 class를 보존한다.
        өңдеу_мән(компьютер, 'Calc.java', 'not Java at all', сақтау_мән=False)
        компьютер.Команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for дұрыс_емес_өлшем in [
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
            өңдеу_мән(компьютер, 'Calc.java', дұрыс_емес_өлшем)
            компьютер.Команда('javac Calc.java', ['javac error:', 'Exit: 1'])
            компьютер.Команда('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # спринт_мән 실행은 пайдаланушы 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            компьютер.Команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        компьютер.Команда('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        компьютер.Команда('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        өңдеу_мән(компьютер, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        компьютер.Команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        компьютер.Команда('java Calc', ['instruction limit', 'Exit: 1'])
        компьютер.Команда('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        өңдеу_мән(компьютер, 'Bad.class', 'garbage')
        компьютер.Команда('java Bad', ['JVM error:', 'Exit: 1'])
        компьютер.Команда('rm Bad.class', ['Removed'])
        компьютер.Команда('java Bad', ['cannot read class: -2'])
        # өңдеу_мән 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Орындау_2 = len(компьютер.журнал_жол)
        компьютер.직렬.sendall(b'edit Hello.java\n')
        компьютер.күту_күйі('...> ', Орындау_2)
        Орындау_2 = len(компьютер.журнал_жол)
        компьютер.직렬.sendall(b'x' * 129 + b'\n')
        компьютер.күту_күйі('...> ', Орындау_2)
        компьютер.Команда('.save', ['Too much input; original preserved'])
        компьютер.Команда('javac Hello.java', ['Compiled:', 'Exit: 0'])
        өңдеу_мән(компьютер, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            өңдеу_мән(компьютер, 'f' + str(수), 'occupied')
        компьютер.Команда('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        компьютер.Команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in компьютер.журнал_жол.decode('utf-8', 'replace')
        НӘТИЖЕ['serial'] = компьютер.журнал_жол.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return НӘТИЖЕ
    finally:
        компьютер.Жабу()


def 주코드(деректер):
    """손상 시험용 main Code의 нақты_деректер Файл 오프셋/길이만 읽는다."""
    лауазым_мән = 8
    def 짧():
        nonlocal лауазым_мән
        мән = struct.unpack_from('>H', деректер, лауазым_мән)[0]
        лауазым_мән += 2
        return мән
    def 정():
        nonlocal лауазым_мән
        мән = struct.unpack_from('>I', деректер, лауазым_мән)[0]
        лауазым_мән += 4
        return мән
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = деректер[лауазым_мән]
        лауазым_мән += 1
        if 종류 == 1:
            ұзындық_мән = 짧()
            문자들[수] = деректер[лауазым_мән:лауазым_мән + ұзындық_мән]
            лауазым_мән += ұзындық_мән
        elif 종류 in (7, 8): лауазым_мән += 2
        elif 종류 in (3, 9, 10, 12): лауазым_мән += 4
        else: raise AssertionError(종류)
    лауазым_мән += 6
    개수 = 짧()
    лауазым_мән += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Аты = 짧()
        짧()
        for 수 in range(짧()):
            атрибут_мән = 짧()
            Өлшемі = 정()
            if 문자들[Аты] == b'main' and 문자들[атрибут_мән] == b'Code':
                return лауазым_мән + 8, struct.unpack_from('>I', деректер, лауазым_мән + 4)[0]
            лауазым_мән += Өлшемі
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        каталог_мән = Path(임시)
        (каталог_мән / 'build').mkdir()
        Неден = каталог_мән / 'Imported.java'
        Неден.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Неден)], check=True)
        원본 = (каталог_мән / 'Imported.class').read_bytes()
        код_мән, ұзындық_мән = 주코드(원본)
        변형 = {}
        деректер = bytearray(원본); деректер[0] = 0; 변형['BadMagic'] = деректер
        деректер = bytearray(원본); деректер[7] = 61; 변형['BadVer'] = деректер
        деректер = bytearray(원본); деректер[8:10] = b'\xff\xff'; 변형['BadPool'] = деректер
        деректер = bytearray(원본); деректер[код_мән:код_мән + ұзындық_мән] = bytes(ұзындық_мән)
        деректер[код_мән:код_мән + 3] = b'\xa7\x00\x01'; деректер[код_мән + ұзындық_мән - 1] = 177; 변형['BadJump'] = деректер
        деректер = bytearray(원본); деректер[код_мән:код_мән + ұзындық_мән] = bytes(ұзындық_мән)
        деректер[код_мән] = 87; деректер[код_мән + ұзындық_мән - 1] = 177; 변형['BadStack'] = деректер
        # Аты 검사를 통과시켜 нақты_деректер орындау_пәрмен 중의 операнд_Бума 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        енгізу_мән = ['Imported.class=' + str(каталог_мән / 'Imported.class'), 'Imported.java=' + str(Неден)]
        for Аты, деректер in 변형.items():
            Жол_2 = каталог_мән / (Аты + '.class'); Жол_2.write_bytes(деректер)
            енгізу_мән.append(Аты + '.class=' + str(Жол_2))
        Топ_мән = каталог_мән / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Орны / 'Құралдар/자바파일묶기.py'), '-o', str(Топ_мән)] + енгізу_мән, check=True)
        subprocess.run(['as', '--32', '-o', str(каталог_мән / 'user.o'), str(Орны / '부팅/пайдаланушы.s')], cwd=str(каталог_мән), check=True)
        ядро_мән = каталог_мән / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Орны / '부팅/Cілтеме_макет.ld'), '-o', str(ядро_мән),
                        str(Орны / 'build/boot.o'), str(Орны / 'build/java.o'), str(каталог_мән / 'user.o'), str(Орны / 'build/apps.o')], check=True)
        компьютер = виртуалды_машина(ядро_мән, желі_мән=False)
        try:
            компьютер.Команда('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            компьютер.Команда('cat Imported.java', ['int[] values = new int[3]'])
            for Аты, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                компьютер.Команда('java ' + Аты, [문구, 'Exit: 1'])
                компьютер.Команда('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return компьютер.журнал_жол.decode('utf-8', 'replace')
        finally:
            компьютер.Жабу()


if __name__ == '__main__':
    талдау_мән = argparse.ArgumentParser()
    талдау_мән.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Аргументтер = талдау_мән.parse_args()
    НӘТИЖЕ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Аргументтер.boot == 'both' else (Аргументтер.boot,))}
    НӘТИЖЕ['import'] = 적재시험()
    (Орны / 'build/자바시험.json').write_text(json.dumps(НӘТИЖЕ, ensure_ascii=False, indent=2) + '\n')
