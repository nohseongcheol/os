#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 иҷро_кардан_фармон, нокомӣ_қимат/захира_қимат 경계 시험."""
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
from 사용자통신시험 import виртуалӣ_компютер, 위치


def таҳрир_қимат(компютер, Ном, Мӯҳтаво_қимат, ҳифз_кардан_қимат=True):
    порча = len(компютер.сабт_кардан_сабт)
    компютер.직렬.sendall(('edit ' + Ном + '\n').encode())
    компютер.기다림('...> ', порча)
    for хат in Мӯҳтаво_қимат.splitlines():
        assert len(хат) <= 128
        порча = len(компютер.сабт_кардан_сабт)
        компютер.직렬.sendall((хат + '\n').encode())
        компютер.기다림('...> ', порча)
    порча = len(компютер.сабт_кардан_сабт)
    компютер.직렬.sendall(b'.save\n' if ҳифз_кардан_қимат else b'.cancel\n')
    결과 = компютер.기다림('jkoros> ', порча)
    assert ('Saved:' if ҳифз_кардан_қимат else 'Cancelled; original preserved') in 결과, 결과


def файл_суроға():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for хат in 결과.splitlines():
        if хат.endswith(' ram_files'):
            return int(хат.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def меҳмон_файл(компютер, ковокӣ_қимат, андоза_кардан, масир):
    # 시험 VM의 메모리에서 воқеӣ_иттилоот 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    суроға = файл_суроға() + ковокӣ_қимат * 16384
    компютер.монитор_қимат.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(суроға, андоза_кардан, масир)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if масир.exists() and масир.stat().st_size == андоза_кардан:
            return масир.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    компютер = виртуалӣ_компютер(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Шабака_қимат=False)
    결과 = {}
    try:
        компютер.фармон('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        компютер.фармон('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        компютер.фармон('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        компютер.фармон('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        компютер.фармон('java Missing', ['cannot read class: -2', 'Exit: 1'])
        компютер.фармон('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        компютер.фармон('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Мӯҳтаво_қимат = '''public class Calc {
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
        таҳрир_қимат(компютер, 'Calc.java', Мӯҳтаво_қимат)
        компютер.фармон('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = компютер.фармон('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        ворида_Рӯйхат = компютер.фармон('ls', ['Calc.class'])
        андоза_кардан = int(re.search(r'Calc\.class\s+(\d+) bytes', ворида_Рӯйхат).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as директория_қимат:
            масир = Path(директория_қимат) / 'Calc.class'
            иттилоот = меҳмон_файл(компютер, 3, андоза_кардан, масир)
            воқеӣ_иттилоот = subprocess.check_output(['java', '-Xverify:all', '-cp', директория_қимат, 'Calc', '6', 'guest'], universal_newlines=True)
            assert воқеӣ_иттилоот.splitlines() == 기대, воқеӣ_иттилоот
            결과['class_sha256'] = hashlib.sha256(иттилоот).hexdigest()
            결과['openjdk_output'] = воқеӣ_иттилоот
        # 실패한 таҳрир_қимат/컴파일은 기존 class를 보존한다.
        таҳрир_қимат(компютер, 'Calc.java', 'not Java at all', ҳифз_кардан_қимат=False)
        компютер.фармон('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            таҳрир_қимат(компютер, 'Calc.java', 잘못)
            компютер.фармон('javac Calc.java', ['javac error:', 'Exit: 1'])
            компютер.фармон('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # такрор_қимат 실행은 корбар 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            компютер.фармон('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        компютер.фармон('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        компютер.фармон('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        таҳрир_қимат(компютер, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        компютер.фармон('javac Calc.java', ['Compiled:', 'Exit: 0'])
        компютер.фармон('java Calc', ['instruction limit', 'Exit: 1'])
        компютер.фармон('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        таҳрир_қимат(компютер, 'Bad.class', 'garbage')
        компютер.фармон('java Bad', ['JVM error:', 'Exit: 1'])
        компютер.фармон('rm Bad.class', ['Removed'])
        компютер.фармон('java Bad', ['cannot read class: -2'])
        # таҳрир_қимат 입력의 넘친 부분을 잘라서 저장하지 않는다.
        порча = len(компютер.сабт_кардан_сабт)
        компютер.직렬.sendall(b'edit Hello.java\n')
        компютер.기다림('...> ', порча)
        порча = len(компютер.сабт_кардан_сабт)
        компютер.직렬.sendall(b'x' * 129 + b'\n')
        компютер.기다림('...> ', порча)
        компютер.фармон('.save', ['Too much input; original preserved'])
        компютер.фармон('javac Hello.java', ['Compiled:', 'Exit: 0'])
        таҳрир_қимат(компютер, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            таҳрир_қимат(компютер, 'f' + str(수), 'occupied')
        компютер.фармон('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        компютер.фармон('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
        결과['serial'] = компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        компютер.Пӯшидан()


def 주코드(иттилоот):
    """손상 시험용 main Code의 воқеӣ_иттилоот Файл 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        қимат = struct.unpack_from('>H', иттилоот, 위치값)[0]
        위치값 += 2
        return қимат
    def 정():
        nonlocal 위치값
        қимат = struct.unpack_from('>I', иттилоот, 위치값)[0]
        위치값 += 4
        return қимат
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = иттилоот[위치값]
        위치값 += 1
        if 종류 == 1:
            дарозӣ_қимат = 짧()
            문자들[수] = иттилоот[위치값:위치값 + дарозӣ_қимат]
            위치값 += дарозӣ_қимат
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Ном = 짧()
        짧()
        for 수 in range(짧()):
            сифат_қимат = 짧()
            андоза_кардан = 정()
            if 문자들[Ном] == b'main' and 문자들[сифат_қимат] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', иттилоот, 위치값 + 4)[0]
            위치값 += андоза_кардан
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        директория_қимат = Path(임시)
        (директория_қимат / 'build').mkdir()
        манбаъ = директория_қимат / 'Imported.java'
        манбаъ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(манбаъ)], check=True)
        원본 = (директория_қимат / 'Imported.class').read_bytes()
        코드, дарозӣ_қимат = 주코드(원본)
        변형 = {}
        иттилоот = bytearray(원본); иттилоот[0] = 0; 변형['BadMagic'] = иттилоот
        иттилоот = bytearray(원본); иттилоот[7] = 61; 변형['BadVer'] = иттилоот
        иттилоот = bytearray(원본); иттилоот[8:10] = b'\xff\xff'; 변형['BadPool'] = иттилоот
        иттилоот = bytearray(원본); иттилоот[코드:코드 + дарозӣ_қимат] = bytes(дарозӣ_қимат)
        иттилоот[코드:코드 + 3] = b'\xa7\x00\x01'; иттилоот[코드 + дарозӣ_қимат - 1] = 177; 변형['BadJump'] = иттилоот
        иттилоот = bytearray(원본); иттилоот[코드:코드 + дарозӣ_қимат] = bytes(дарозӣ_қимат)
        иттилоот[코드] = 87; иттилоот[코드 + дарозӣ_қимат - 1] = 177; 변형['BadStack'] = иттилоот
        # Ном 검사를 통과시켜 воқеӣ_иттилоот иҷро_кардан_фармон 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ворида_қимат = ['Imported.class=' + str(директория_қимат / 'Imported.class'), 'Imported.java=' + str(манбаъ)]
        for Ном, иттилоот in 변형.items():
            масир = директория_қимат / (Ном + '.class'); масир.write_bytes(иттилоот)
            ворида_қимат.append(Ном + '.class=' + str(масир))
        гуруҳ_қимат = директория_қимат / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Абзорҳо/자바파일묶기.py'), '-o', str(гуруҳ_қимат)] + ворида_қимат, check=True)
        subprocess.run(['as', '--32', '-o', str(директория_қимат / 'user.o'), str(위치 / '부팅/корбар.s')], cwd=str(директория_қимат), check=True)
        ҳаста_қимат = директория_қимат / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Пайванд_Тарҳбандӣ.ld'), '-o', str(ҳаста_қимат),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(директория_қимат / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        компютер = виртуалӣ_компютер(ҳаста_қимат, Шабака_қимат=False)
        try:
            компютер.фармон('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            компютер.фармон('cat Imported.java', ['int[] values = new int[3]'])
            for Ном, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                компютер.фармон('java ' + Ном, [문구, 'Exit: 1'])
                компютер.фармон('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
        finally:
            компютер.Пӯшидан()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = 해석.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
