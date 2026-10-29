#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ئىجرا_قىلىش_بۇيرۇق, مەغلۇپ_بولۇش_قىممىتى/مەنبە_قىممىتى 경계 시험."""
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
from 사용자통신시험 import مەۋھۇم_ماشىنا, ئورۇن


def تەھرىرلەش_قىممىتى(ماشىنا, ئاتى, مەزمۇن_قىممىتى, ساقلىماق_قىممىتى=True):
    ئىجرا_قىل_2 = len(ماشىنا.خاتىرە_قۇر)
    ماشىنا.직렬.sendall(('edit ' + ئاتى + '\n').encode())
    ماشىنا.기다림('...> ', ئىجرا_قىل_2)
    for قۇر in مەزمۇن_قىممىتى.splitlines():
        assert len(قۇر) <= 128
        ئىجرا_قىل_2 = len(ماشىنا.خاتىرە_قۇر)
        ماشىنا.직렬.sendall((قۇر + '\n').encode())
        ماشىنا.기다림('...> ', ئىجرا_قىل_2)
    ئىجرا_قىل_2 = len(ماشىنا.خاتىرە_قۇر)
    ماشىنا.직렬.sendall(b'.save\n' if ساقلىماق_قىممىتى else b'.cancel\n')
    ئۆلچەم = ماشىنا.기다림('jkoros> ', ئىجرا_قىل_2)
    assert ('Saved:' if ساقلىماق_قىممىتى else 'Cancelled; original preserved') in ئۆلچەم, ئۆلچەم


def ھۆججەت_ئادرېس():
    ئۆلچەم = subprocess.check_output(['nm', '-n', str(ئورۇن / 'build/kernel.elf')], universal_newlines=True)
    for قۇر in ئۆلچەم.splitlines():
        if قۇر.endswith(' ram_files'):
            return int(قۇر.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def مېھمان_ھۆججەت(ماشىنا, ئوقۇر_قىممىتى, چوڭلۇقى, يول):
    # 시험 VM의 메모리에서 ھەقىقىي_مەلۇمات 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ئادرېس = ھۆججەت_ئادرېس() + ئوقۇر_قىممىتى * 16384
    ماشىنا.كۆرسەتكۈچ_قىممىتى.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ئادرېس, چوڭلۇقى, يول)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if يول.exists() and يول.stat().st_size == چوڭلۇقى:
            return يول.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, تور_قىممىتى=False)
    ئۆلچەم = {}
    try:
        ماشىنا.بۇيرۇق('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ماشىنا.بۇيرۇق('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ماشىنا.بۇيرۇق('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ماشىنا.بۇيرۇق('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ماشىنا.بۇيرۇق('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ماشىنا.بۇيرۇق('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ماشىنا.بۇيرۇق('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        مەزمۇن_قىممىتى = '''public class Calc {
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
        تەھرىرلەش_قىممىتى(ماشىنا, 'Calc.java', مەزمۇن_قىممىتى)
        ماشىنا.بۇيرۇق('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        چىقار = ماشىنا.بۇيرۇق('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ئۆلچەم['guest_output'] = چىقار
        كىرگۈزۈش_تىزىم = ماشىنا.بۇيرۇق('ls', ['Calc.class'])
        چوڭلۇقى = int(re.search(r'Calc\.class\s+(\d+) bytes', كىرگۈزۈش_تىزىم).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as مۇندەرىجە_قىممىتى:
            يول = Path(مۇندەرىجە_قىممىتى) / 'Calc.class'
            مەلۇمات = مېھمان_ھۆججەت(ماشىنا, 3, چوڭلۇقى, يول)
            ھەقىقىي_مەلۇمات = subprocess.check_output(['java', '-Xverify:all', '-cp', مۇندەرىجە_قىممىتى, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ھەقىقىي_مەلۇمات.splitlines() == 기대, ھەقىقىي_مەلۇمات
            ئۆلچەم['class_sha256'] = hashlib.sha256(مەلۇمات).hexdigest()
            ئۆلچەم['openjdk_output'] = ھەقىقىي_مەلۇمات
        # 실패한 تەھرىرلەش_قىممىتى/컴파일은 기존 class를 보존한다.
        تەھرىرلەش_قىممىتى(ماشىنا, 'Calc.java', 'not Java at all', ساقلىماق_قىممىتى=False)
        ماشىنا.بۇيرۇق('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ئۈنۈمسىز_ئۆلچەم in [
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
            تەھرىرلەش_قىممىتى(ماشىنا, 'Calc.java', ئۈنۈمسىز_ئۆلچەم)
            ماشىنا.بۇيرۇق('javac Calc.java', ['javac error:', 'Exit: 1'])
            ماشىنا.بۇيرۇق('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ئېنتىراتسىيە_قىممىتى 실행은 ئىشلەتكۈچى 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ماشىنا.بۇيرۇق('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ماشىنا.بۇيرۇق('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ماشىنا.بۇيرۇق('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        تەھرىرلەش_قىممىتى(ماشىنا, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ماشىنا.بۇيرۇق('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ماشىنا.بۇيرۇق('java Calc', ['instruction limit', 'Exit: 1'])
        ماشىنا.بۇيرۇق('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        تەھرىرلەش_قىممىتى(ماشىنا, 'Bad.class', 'garbage')
        ماشىنا.بۇيرۇق('java Bad', ['JVM error:', 'Exit: 1'])
        ماشىنا.بۇيرۇق('rm Bad.class', ['Removed'])
        ماشىنا.بۇيرۇق('java Bad', ['cannot read class: -2'])
        # تەھرىرلەش_قىممىتى 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ئىجرا_قىل_2 = len(ماشىنا.خاتىرە_قۇر)
        ماشىنا.직렬.sendall(b'edit Hello.java\n')
        ماشىنا.기다림('...> ', ئىجرا_قىل_2)
        ئىجرا_قىل_2 = len(ماشىنا.خاتىرە_قۇر)
        ماشىنا.직렬.sendall(b'x' * 129 + b'\n')
        ماشىنا.기다림('...> ', ئىجرا_قىل_2)
        ماشىنا.بۇيرۇق('.save', ['Too much input; original preserved'])
        ماشىنا.بۇيرۇق('javac Hello.java', ['Compiled:', 'Exit: 0'])
        تەھرىرلەش_قىممىتى(ماشىنا, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            تەھرىرلەش_قىممىتى(ماشىنا, 'f' + str(수), 'occupied')
        ماشىنا.بۇيرۇق('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ماشىنا.بۇيرۇق('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
        ئۆلچەم['serial'] = ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ئۆلچەم
    finally:
        ماشىنا.ياپ()


def 주코드(مەلۇمات):
    """손상 시험용 main Code의 ھەقىقىي_مەلۇمات ھۆججەت 오프셋/길이만 읽는다."""
    ئورۇنلاشتۇرۇش_قىممىتى = 8
    def 짧():
        nonlocal ئورۇنلاشتۇرۇش_قىممىتى
        قىممىتى = struct.unpack_from('>H', مەلۇمات, ئورۇنلاشتۇرۇش_قىممىتى)[0]
        ئورۇنلاشتۇرۇش_قىممىتى += 2
        return قىممىتى
    def 정():
        nonlocal ئورۇنلاشتۇرۇش_قىممىتى
        قىممىتى = struct.unpack_from('>I', مەلۇمات, ئورۇنلاشتۇرۇش_قىممىتى)[0]
        ئورۇنلاشتۇرۇش_قىممىتى += 4
        return قىممىتى
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = مەلۇمات[ئورۇنلاشتۇرۇش_قىممىتى]
        ئورۇنلاشتۇرۇش_قىممىتى += 1
        if 종류 == 1:
            ئۇزۇنلۇق_قىممىتى = 짧()
            문자들[수] = مەلۇمات[ئورۇنلاشتۇرۇش_قىممىتى:ئورۇنلاشتۇرۇش_قىممىتى + ئۇزۇنلۇق_قىممىتى]
            ئورۇنلاشتۇرۇش_قىممىتى += ئۇزۇنلۇق_قىممىتى
        elif 종류 in (7, 8): ئورۇنلاشتۇرۇش_قىممىتى += 2
        elif 종류 in (3, 9, 10, 12): ئورۇنلاشتۇرۇش_قىممىتى += 4
        else: raise AssertionError(종류)
    ئورۇنلاشتۇرۇش_قىممىتى += 6
    개수 = 짧()
    ئورۇنلاشتۇرۇش_قىممىتى += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ئاتى = 짧()
        짧()
        for 수 in range(짧()):
            خاسلىق_قىممىتى = 짧()
            چوڭلۇقى = 정()
            if 문자들[ئاتى] == b'main' and 문자들[خاسلىق_قىممىتى] == b'Code':
                return ئورۇنلاشتۇرۇش_قىممىتى + 8, struct.unpack_from('>I', مەلۇمات, ئورۇنلاشتۇرۇش_قىممىتى + 4)[0]
            ئورۇنلاشتۇرۇش_قىممىتى += چوڭلۇقى
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        مۇندەرىجە_قىممىتى = Path(임시)
        (مۇندەرىجە_قىممىتى / 'build').mkdir()
        مەنبە = مۇندەرىجە_قىممىتى / 'Imported.java'
        مەنبە.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(مەنبە)], check=True)
        원본 = (مۇندەرىجە_قىممىتى / 'Imported.class').read_bytes()
        코드, ئۇزۇنلۇق_قىممىتى = 주코드(원본)
        변형 = {}
        مەلۇمات = bytearray(원본); مەلۇمات[0] = 0; 변형['BadMagic'] = مەلۇمات
        مەلۇمات = bytearray(원본); مەلۇمات[7] = 61; 변형['BadVer'] = مەلۇمات
        مەلۇمات = bytearray(원본); مەلۇمات[8:10] = b'\xff\xff'; 변형['BadPool'] = مەلۇمات
        مەلۇمات = bytearray(원본); مەلۇمات[코드:코드 + ئۇزۇنلۇق_قىممىتى] = bytes(ئۇزۇنلۇق_قىممىتى)
        مەلۇمات[코드:코드 + 3] = b'\xa7\x00\x01'; مەلۇمات[코드 + ئۇزۇنلۇق_قىممىتى - 1] = 177; 변형['BadJump'] = مەلۇمات
        مەلۇمات = bytearray(원본); مەلۇمات[코드:코드 + ئۇزۇنلۇق_قىممىتى] = bytes(ئۇزۇنلۇق_قىممىتى)
        مەلۇمات[코드] = 87; مەلۇمات[코드 + ئۇزۇنلۇق_قىممىتى - 1] = 177; 변형['BadStack'] = مەلۇمات
        # ئاتى 검사를 통과시켜 ھەقىقىي_مەلۇمات ئىجرا_قىلىش_بۇيرۇق 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        كىرگۈزۈش_قىممىتى = ['Imported.class=' + str(مۇندەرىجە_قىممىتى / 'Imported.class'), 'Imported.java=' + str(مەنبە)]
        for ئاتى, مەلۇمات in 변형.items():
            يول = مۇندەرىجە_قىممىتى / (ئاتى + '.class'); يول.write_bytes(مەلۇمات)
            كىرگۈزۈش_قىممىتى.append(ئاتى + '.class=' + str(يول))
        توپ_قىممىتى = مۇندەرىجە_قىممىتى / 'build/java-files.bin'
        subprocess.run([sys.executable, str(ئورۇن / 'قوراللار/자바파일묶기.py'), '-o', str(توپ_قىممىتى)] + كىرگۈزۈش_قىممىتى, check=True)
        subprocess.run(['as', '--32', '-o', str(مۇندەرىجە_قىممىتى / 'user.o'), str(ئورۇن / '부팅/ئىشلەتكۈچى.s')], cwd=str(مۇندەرىجە_قىممىتى), check=True)
        يادرو_قىممىتى = مۇندەرىجە_قىممىتى / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ئورۇن / '부팅/ئۇلانما_لايىھە.ld'), '-o', str(يادرو_قىممىتى),
                        str(ئورۇن / 'build/boot.o'), str(ئورۇن / 'build/java.o'), str(مۇندەرىجە_قىممىتى / 'user.o'), str(ئورۇن / 'build/apps.o')], check=True)
        ماشىنا = مەۋھۇم_ماشىنا(يادرو_قىممىتى, تور_قىممىتى=False)
        try:
            ماشىنا.بۇيرۇق('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ماشىنا.بۇيرۇق('cat Imported.java', ['int[] values = new int[3]'])
            for ئاتى, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ماشىنا.بۇيرۇق('java ' + ئاتى, [문구, 'Exit: 1'])
                ماشىنا.بۇيرۇق('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
        finally:
            ماشىنا.ياپ()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    ئۆزگەرگۈچىلەر = 해석.parse_args()
    ئۆلچەم = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if ئۆزگەرگۈچىلەر.boot == 'both' else (ئۆزگەرگۈچىلەر.boot,))}
    ئۆلچەم['import'] = 적재시험()
    (ئورۇن / 'build/자바시험.json').write_text(json.dumps(ئۆلچەم, ensure_ascii=False, indent=2) + '\n')
