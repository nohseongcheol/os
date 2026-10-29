#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 تعميل_ڪرڻ_حڪم, ناڪامي_قدر/ذريعو_قدر 경계 시험."""
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
from 사용자통신시험 import مجازي_مشين, 위치


def تدوين_قدر(مشين, نالو, مواد_قدر, روڪيو_قدر=True):
    هلائڻ = len(مشين.لاگ_صف)
    مشين.직렬.sendall(('edit ' + نالو + '\n').encode())
    مشين.기다림('...> ', هلائڻ)
    for لڪير in مواد_قدر.splitlines():
        assert len(لڪير) <= 128
        هلائڻ = len(مشين.لاگ_صف)
        مشين.직렬.sendall((لڪير + '\n').encode())
        مشين.기다림('...> ', هلائڻ)
    هلائڻ = len(مشين.لاگ_صف)
    مشين.직렬.sendall(b'.save\n' if روڪيو_قدر else b'.cancel\n')
    결과 = مشين.기다림('jkoros> ', هلائڻ)
    assert ('Saved:' if روڪيو_قدر else 'Cancelled; original preserved') in 결과, 결과


def فائل_پتو():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for لڪير in 결과.splitlines():
        if لڪير.endswith(' ram_files'):
            return int(لڪير.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(مشين, سوراخ_قدر, سائيز, راههه):
    # 시험 VM의 메모리에서 اصلي_ڪوائف 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    پتو = فائل_پتو() + سوراخ_قدر * 16384
    مشين.مانيٽر_قدر.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(پتو, سائيز, راههه)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if راههه.exists() and راههه.stat().st_size == سائيز:
            return راههه.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    مشين = مجازي_مشين(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, نيٽ_ورڪ_قدر=False)
    결과 = {}
    try:
        مشين.حڪم('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        مشين.حڪم('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        مشين.حڪم('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        مشين.حڪم('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        مشين.حڪم('java Missing', ['cannot read class: -2', 'Exit: 1'])
        مشين.حڪم('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        مشين.حڪم('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        مواد_قدر = '''public class Calc {
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
        تدوين_قدر(مشين, 'Calc.java', مواد_قدر)
        مشين.حڪم('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = مشين.حڪم('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        داخلا_فهرست = مشين.حڪم('ls', ['Calc.class'])
        سائيز = int(re.search(r'Calc\.class\s+(\d+) bytes', داخلا_فهرست).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ڊائريڪٽري_قدر:
            راههه = Path(ڊائريڪٽري_قدر) / 'Calc.class'
            ڪوائف = 게스트파일(مشين, 3, سائيز, راههه)
            اصلي_ڪوائف = subprocess.check_output(['java', '-Xverify:all', '-cp', ڊائريڪٽري_قدر, 'Calc', '6', 'guest'], universal_newlines=True)
            assert اصلي_ڪوائف.splitlines() == 기대, اصلي_ڪوائف
            결과['class_sha256'] = hashlib.sha256(ڪوائف).hexdigest()
            결과['openjdk_output'] = اصلي_ڪوائف
        # 실패한 تدوين_قدر/컴파일은 기존 class를 보존한다.
        تدوين_قدر(مشين, 'Calc.java', 'not Java at all', روڪيو_قدر=False)
        مشين.حڪم('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            تدوين_قدر(مشين, 'Calc.java', 잘못)
            مشين.حڪم('javac Calc.java', ['javac error:', 'Exit: 1'])
            مشين.حڪم('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # دهرائڻ_قدر 실행은 صارف 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            مشين.حڪم('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        مشين.حڪم('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        مشين.حڪم('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        تدوين_قدر(مشين, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        مشين.حڪم('javac Calc.java', ['Compiled:', 'Exit: 0'])
        مشين.حڪم('java Calc', ['instruction limit', 'Exit: 1'])
        مشين.حڪم('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        تدوين_قدر(مشين, 'Bad.class', 'garbage')
        مشين.حڪم('java Bad', ['JVM error:', 'Exit: 1'])
        مشين.حڪم('rm Bad.class', ['Removed'])
        مشين.حڪم('java Bad', ['cannot read class: -2'])
        # تدوين_قدر 입력의 넘친 부분을 잘라서 저장하지 않는다.
        هلائڻ = len(مشين.لاگ_صف)
        مشين.직렬.sendall(b'edit Hello.java\n')
        مشين.기다림('...> ', هلائڻ)
        هلائڻ = len(مشين.لاگ_صف)
        مشين.직렬.sendall(b'x' * 129 + b'\n')
        مشين.기다림('...> ', هلائڻ)
        مشين.حڪم('.save', ['Too much input; original preserved'])
        مشين.حڪم('javac Hello.java', ['Compiled:', 'Exit: 0'])
        تدوين_قدر(مشين, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            تدوين_قدر(مشين, 'f' + str(수), 'occupied')
        مشين.حڪم('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        مشين.حڪم('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in مشين.لاگ_صف.decode('utf-8', 'replace')
        결과['serial'] = مشين.لاگ_صف.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        مشين.بند_ڪرڻ()


def 주코드(ڪوائف):
    """손상 시험용 main Code의 اصلي_ڪوائف فائل 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        قدر = struct.unpack_from('>H', ڪوائف, 위치값)[0]
        위치값 += 2
        return قدر
    def 정():
        nonlocal 위치값
        قدر = struct.unpack_from('>I', ڪوائف, 위치값)[0]
        위치값 += 4
        return قدر
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ڪوائف[위치값]
        위치값 += 1
        if 종류 == 1:
            لمبائي_قدر = 짧()
            문자들[수] = ڪوائف[위치값:위치값 + لمبائي_قدر]
            위치값 += لمبائي_قدر
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        نالو = 짧()
        짧()
        for 수 in range(짧()):
            منسوب_ڪرڻ_قدر = 짧()
            سائيز = 정()
            if 문자들[نالو] == b'main' and 문자들[منسوب_ڪرڻ_قدر] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', ڪوائف, 위치값 + 4)[0]
            위치값 += سائيز
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ڊائريڪٽري_قدر = Path(임시)
        (ڊائريڪٽري_قدر / 'build').mkdir()
        ماخذ = ڊائريڪٽري_قدر / 'Imported.java'
        ماخذ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ماخذ)], check=True)
        원본 = (ڊائريڪٽري_قدر / 'Imported.class').read_bytes()
        코드, لمبائي_قدر = 주코드(원본)
        변형 = {}
        ڪوائف = bytearray(원본); ڪوائف[0] = 0; 변형['BadMagic'] = ڪوائف
        ڪوائف = bytearray(원본); ڪوائف[7] = 61; 변형['BadVer'] = ڪوائف
        ڪوائف = bytearray(원본); ڪوائف[8:10] = b'\xff\xff'; 변형['BadPool'] = ڪوائف
        ڪوائف = bytearray(원본); ڪوائف[코드:코드 + لمبائي_قدر] = bytes(لمبائي_قدر)
        ڪوائف[코드:코드 + 3] = b'\xa7\x00\x01'; ڪوائف[코드 + لمبائي_قدر - 1] = 177; 변형['BadJump'] = ڪوائف
        ڪوائف = bytearray(원본); ڪوائف[코드:코드 + لمبائي_قدر] = bytes(لمبائي_قدر)
        ڪوائف[코드] = 87; ڪوائف[코드 + لمبائي_قدر - 1] = 177; 변형['BadStack'] = ڪوائف
        # نالو 검사를 통과시켜 اصلي_ڪوائف تعميل_ڪرڻ_حڪم 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        داخلا_قدر = ['Imported.class=' + str(ڊائريڪٽري_قدر / 'Imported.class'), 'Imported.java=' + str(ماخذ)]
        for نالو, ڪوائف in 변형.items():
            راههه = ڊائريڪٽري_قدر / (نالو + '.class'); راههه.write_bytes(ڪوائف)
            داخلا_قدر.append(نالو + '.class=' + str(راههه))
        گروپ_قدر = ڊائريڪٽري_قدر / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'اوزار/자바파일묶기.py'), '-o', str(گروپ_قدر)] + داخلا_قدر, check=True)
        subprocess.run(['as', '--32', '-o', str(ڊائريڪٽري_قدر / 'user.o'), str(위치 / '부팅/صارف.s')], cwd=str(ڊائريڪٽري_قدر), check=True)
        ڪرنل_قدر = ڊائريڪٽري_قدر / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/ڪڙي_لي_آئوٽ.ld'), '-o', str(ڪرنل_قدر),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(ڊائريڪٽري_قدر / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        مشين = مجازي_مشين(ڪرنل_قدر, نيٽ_ورڪ_قدر=False)
        try:
            مشين.حڪم('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            مشين.حڪم('cat Imported.java', ['int[] values = new int[3]'])
            for نالو, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                مشين.حڪم('java ' + نالو, [문구, 'Exit: 1'])
                مشين.حڪم('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return مشين.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشين.بند_ڪرڻ()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = 해석.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
