#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 выканаць_каманда, няўдача_значэнне/рэсурс_значэнне 경계 시험."""
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
from 사용자통신시험 import віртуальны_камп_ютар, Пазіцыя


def рэдагаваць_значэнне(камп_ютар, Назва, кантэнт_значэнне, сховішча_значэнне=True):
    Выканаць = len(камп_ютар.журнал_запіс)
    камп_ютар.직렬.sendall(('edit ' + Назва + '\n').encode())
    камп_ютар.чакае_стан('...> ', Выканаць)
    for лінія in кантэнт_значэнне.splitlines():
        assert len(лінія) <= 128
        Выканаць = len(камп_ютар.журнал_запіс)
        камп_ютар.직렬.sendall((лінія + '\n').encode())
        камп_ютар.чакае_стан('...> ', Выканаць)
    Выканаць = len(камп_ютар.журнал_запіс)
    камп_ютар.직렬.sendall(b'.save\n' if сховішча_значэнне else b'.cancel\n')
    결과 = камп_ютар.чакае_стан('jkoros> ', Выканаць)
    assert ('Saved:' if сховішча_значэнне else 'Cancelled; original preserved') in 결과, 결과


def файл_адрас():
    결과 = subprocess.check_output(['nm', '-n', str(Пазіцыя / 'build/kernel.elf')], universal_newlines=True)
    for лінія in 결과.splitlines():
        if лінія.endswith(' ram_files'):
            return int(лінія.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def госць_файл(камп_ютар, слот_значэнне, Памер, ШЛЯХ):
    # 시험 VM의 메모리에서 фактычны_дадзеныя 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    адрас = файл_адрас() + слот_значэнне * 16384
    камп_ютар.манітор_значэнне.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(адрас, Памер, ШЛЯХ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ШЛЯХ.exists() and ШЛЯХ.stat().st_size == Памер:
            return ШЛЯХ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    камп_ютар = віртуальны_камп_ютар(Пазіцыя / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Сетка_значэнне=False)
    결과 = {}
    try:
        камп_ютар.Загад('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        камп_ютар.Загад('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        камп_ютар.Загад('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        камп_ютар.Загад('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        камп_ютар.Загад('java Missing', ['cannot read class: -2', 'Exit: 1'])
        камп_ютар.Загад('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        камп_ютар.Загад('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        кантэнт_значэнне = '''public class Calc {
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
        рэдагаваць_значэнне(камп_ютар, 'Calc.java', кантэнт_значэнне)
        камп_ютар.Загад('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Выхад = камп_ютар.Загад('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = Выхад
        увядзенне_Спіс = камп_ютар.Загад('ls', ['Calc.class'])
        Памер = int(re.search(r'Calc\.class\s+(\d+) bytes', увядзенне_Спіс).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as каталог_значэнне:
            ШЛЯХ = Path(каталог_значэнне) / 'Calc.class'
            дадзеныя = госць_файл(камп_ютар, 3, Памер, ШЛЯХ)
            фактычны_дадзеныя = subprocess.check_output(['java', '-Xverify:all', '-cp', каталог_значэнне, 'Calc', '6', 'guest'], universal_newlines=True)
            assert фактычны_дадзеныя.splitlines() == 기대, фактычны_дадзеныя
            결과['class_sha256'] = hashlib.sha256(дадзеныя).hexdigest()
            결과['openjdk_output'] = фактычны_дадзеныя
        # 실패한 рэдагаваць_значэнне/컴파일은 기존 class를 보존한다.
        рэдагаваць_значэнне(камп_ютар, 'Calc.java', 'not Java at all', сховішча_значэнне=False)
        камп_ютар.Загад('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            рэдагаваць_значэнне(камп_ютар, 'Calc.java', 잘못)
            камп_ютар.Загад('javac Calc.java', ['javac error:', 'Exit: 1'])
            камп_ютар.Загад('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # спрынт_значэнне 실행은 карыстальнік 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            камп_ютар.Загад('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        камп_ютар.Загад('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        камп_ютар.Загад('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        рэдагаваць_значэнне(камп_ютар, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        камп_ютар.Загад('javac Calc.java', ['Compiled:', 'Exit: 0'])
        камп_ютар.Загад('java Calc', ['instruction limit', 'Exit: 1'])
        камп_ютар.Загад('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        рэдагаваць_значэнне(камп_ютар, 'Bad.class', 'garbage')
        камп_ютар.Загад('java Bad', ['JVM error:', 'Exit: 1'])
        камп_ютар.Загад('rm Bad.class', ['Removed'])
        камп_ютар.Загад('java Bad', ['cannot read class: -2'])
        # рэдагаваць_значэнне 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Выканаць = len(камп_ютар.журнал_запіс)
        камп_ютар.직렬.sendall(b'edit Hello.java\n')
        камп_ютар.чакае_стан('...> ', Выканаць)
        Выканаць = len(камп_ютар.журнал_запіс)
        камп_ютар.직렬.sendall(b'x' * 129 + b'\n')
        камп_ютар.чакае_стан('...> ', Выканаць)
        камп_ютар.Загад('.save', ['Too much input; original preserved'])
        камп_ютар.Загад('javac Hello.java', ['Compiled:', 'Exit: 0'])
        рэдагаваць_значэнне(камп_ютар, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            рэдагаваць_значэнне(камп_ютар, 'f' + str(수), 'occupied')
        камп_ютар.Загад('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        камп_ютар.Загад('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in камп_ютар.журнал_запіс.decode('utf-8', 'replace')
        결과['serial'] = камп_ютар.журнал_запіс.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        камп_ютар.Закрыць()


def 주코드(дадзеныя):
    """손상 시험용 main Code의 фактычны_дадзеныя Файл 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        значэнне = struct.unpack_from('>H', дадзеныя, 위치값)[0]
        위치값 += 2
        return значэнне
    def 정():
        nonlocal 위치값
        значэнне = struct.unpack_from('>I', дадзеныя, 위치값)[0]
        위치값 += 4
        return значэнне
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = дадзеныя[위치값]
        위치값 += 1
        if 종류 == 1:
            даўжыня_значэнне = 짧()
            문자들[수] = дадзеныя[위치값:위치값 + даўжыня_значэнне]
            위치값 += даўжыня_значэнне
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Назва = 짧()
        짧()
        for 수 in range(짧()):
            атрыбут_значэнне = 짧()
            Памер = 정()
            if 문자들[Назва] == b'main' and 문자들[атрыбут_значэнне] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', дадзеныя, 위치값 + 4)[0]
            위치값 += Памер
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        каталог_значэнне = Path(임시)
        (каталог_значэнне / 'build').mkdir()
        КРЫНІЦА = каталог_значэнне / 'Imported.java'
        КРЫНІЦА.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(КРЫНІЦА)], check=True)
        원본 = (каталог_значэнне / 'Imported.class').read_bytes()
        код_значэнне, даўжыня_значэнне = 주코드(원본)
        변형 = {}
        дадзеныя = bytearray(원본); дадзеныя[0] = 0; 변형['BadMagic'] = дадзеныя
        дадзеныя = bytearray(원본); дадзеныя[7] = 61; 변형['BadVer'] = дадзеныя
        дадзеныя = bytearray(원본); дадзеныя[8:10] = b'\xff\xff'; 변형['BadPool'] = дадзеныя
        дадзеныя = bytearray(원본); дадзеныя[код_значэнне:код_значэнне + даўжыня_значэнне] = bytes(даўжыня_значэнне)
        дадзеныя[код_значэнне:код_значэнне + 3] = b'\xa7\x00\x01'; дадзеныя[код_значэнне + даўжыня_значэнне - 1] = 177; 변형['BadJump'] = дадзеныя
        дадзеныя = bytearray(원본); дадзеныя[код_значэнне:код_значэнне + даўжыня_значэнне] = bytes(даўжыня_значэнне)
        дадзеныя[код_значэнне] = 87; дадзеныя[код_значэнне + даўжыня_значэнне - 1] = 177; 변형['BadStack'] = дадзеныя
        # Назва 검사를 통과시켜 фактычны_дадзеныя выканаць_каманда 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        увядзенне_значэнне = ['Imported.class=' + str(каталог_значэнне / 'Imported.class'), 'Imported.java=' + str(КРЫНІЦА)]
        for Назва, дадзеныя in 변형.items():
            ШЛЯХ = каталог_значэнне / (Назва + '.class'); ШЛЯХ.write_bytes(дадзеныя)
            увядзенне_значэнне.append(Назва + '.class=' + str(ШЛЯХ))
        Група_значэнне = каталог_значэнне / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Пазіцыя / 'Інструменты/자바파일묶기.py'), '-o', str(Група_значэнне)] + увядзенне_значэнне, check=True)
        subprocess.run(['as', '--32', '-o', str(каталог_значэнне / 'user.o'), str(Пазіцыя / '부팅/карыстальнік.s')], cwd=str(каталог_значэнне), check=True)
        ядро_значэнне = каталог_значэнне / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Пазіцыя / '부팅/сувязь_Макет.ld'), '-o', str(ядро_значэнне),
                        str(Пазіцыя / 'build/boot.o'), str(Пазіцыя / 'build/java.o'), str(каталог_значэнне / 'user.o'), str(Пазіцыя / 'build/apps.o')], check=True)
        камп_ютар = віртуальны_камп_ютар(ядро_значэнне, Сетка_значэнне=False)
        try:
            камп_ютар.Загад('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            камп_ютар.Загад('cat Imported.java', ['int[] values = new int[3]'])
            for Назва, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                камп_ютар.Загад('java ' + Назва, [문구, 'Exit: 1'])
                камп_ютар.Загад('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return камп_ютар.журнал_запіс.decode('utf-8', 'replace')
        finally:
            камп_ютар.Закрыць()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = 해석.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (Пазіцыя / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
