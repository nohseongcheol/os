#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 কার্যকর_করুন_আদেশ, বিফলতা_মান/রিসোর্স_মান 경계 시험."""
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
from 사용자통신시험 import কল্পিত_মেশিন, অবস্থান


def সম্পাদন_মান(মেশিন, নাম, সামগ্রি_মান, ভাণ্ডার_মান=True):
    চালনা = len(মেশিন.লগ_সারি)
    মেশিন.직렬.sendall(('edit ' + নাম + '\n').encode())
    মেশিন.অপেক্ষা_অবস্হা('...> ', চালনা)
    for নিবেশের_পঙ্_ক্তি in সামগ্রি_মান.splitlines():
        assert len(নিবেশের_পঙ্_ক্তি) <= 128
        চালনা = len(মেশিন.লগ_সারি)
        মেশিন.직렬.sendall((নিবেশের_পঙ্_ক্তি + '\n').encode())
        মেশিন.অপেক্ষা_অবস্হা('...> ', চালনা)
    চালনা = len(মেশিন.লগ_সারি)
    মেশিন.직렬.sendall(b'.save\n' if ভাণ্ডার_মান else b'.cancel\n')
    পরিমাপ = মেশিন.অপেক্ষা_অবস্হা('jkoros> ', চালনা)
    assert ('Saved:' if ভাণ্ডার_মান else 'Cancelled; original preserved') in পরিমাপ, পরিমাপ


def ফাইল_ইমেইল():
    পরিমাপ = subprocess.check_output(['nm', '-n', str(অবস্থান / 'build/kernel.elf')], universal_newlines=True)
    for নিবেশের_পঙ্_ক্তি in পরিমাপ.splitlines():
        if নিবেশের_পঙ্_ক্তি.endswith(' ram_files'):
            return int(নিবেশের_পঙ্_ক্তি.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def অতিথি_ফাইল(মেশিন, স্লট_মান, আকার, পথ_2):
    # 시험 VM의 메모리에서 প্রকৃত_ডাটা 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ইমেইল = ফাইল_ইমেইল() + স্লট_মান * 16384
    মেশিন.মনিটর_মান.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ইমেইল, আকার, পথ_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if পথ_2.exists() and পথ_2.stat().st_size == আকার:
            return পথ_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    মেশিন = কল্পিত_মেশিন(অবস্থান / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, নেটওয়ার্ক_মান=False)
    পরিমাপ = {}
    try:
        মেশিন.আদেশ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        মেশিন.আদেশ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        মেশিন.আদেশ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        মেশিন.আদেশ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        মেশিন.আদেশ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        মেশিন.আদেশ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        মেশিন.আদেশ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        সামগ্রি_মান = '''public class Calc {
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
        সম্পাদন_মান(মেশিন, 'Calc.java', সামগ্রি_মান)
        মেশিন.আদেশ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        নির্গম = মেশিন.আদেশ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        পরিমাপ['guest_output'] = নির্গম
        ভুক্তি_তালিকা = মেশিন.আদেশ('ls', ['Calc.class'])
        আকার = int(re.search(r'Calc\.class\s+(\d+) bytes', ভুক্তি_তালিকা).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ডিরেক্টরি_মান:
            পথ_2 = Path(ডিরেক্টরি_মান) / 'Calc.class'
            ডাটা = অতিথি_ফাইল(মেশিন, 3, আকার, পথ_2)
            প্রকৃত_ডাটা = subprocess.check_output(['java', '-Xverify:all', '-cp', ডিরেক্টরি_মান, 'Calc', '6', 'guest'], universal_newlines=True)
            assert প্রকৃত_ডাটা.splitlines() == 기대, প্রকৃত_ডাটা
            পরিমাপ['class_sha256'] = hashlib.sha256(ডাটা).hexdigest()
            পরিমাপ['openjdk_output'] = প্রকৃত_ডাটা
        # 실패한 সম্পাদন_মান/컴파일은 기존 class를 보존한다.
        সম্পাদন_মান(মেশিন, 'Calc.java', 'not Java at all', ভাণ্ডার_মান=False)
        মেশিন.আদেশ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for অবৈধ_পরিমাপ in [
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
            সম্পাদন_মান(মেশিন, 'Calc.java', অবৈধ_পরিমাপ)
            মেশিন.আদেশ('javac Calc.java', ['javac error:', 'Exit: 1'])
            মেশিন.আদেশ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # পুনরুক্তি_মান 실행은 ব্যবহারকারী 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            মেশিন.আদেশ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        মেশিন.আদেশ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        মেশিন.আদেশ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        সম্পাদন_মান(মেশিন, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        মেশিন.আদেশ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        মেশিন.আদেশ('java Calc', ['instruction limit', 'Exit: 1'])
        মেশিন.আদেশ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        সম্পাদন_মান(মেশিন, 'Bad.class', 'garbage')
        মেশিন.আদেশ('java Bad', ['JVM error:', 'Exit: 1'])
        মেশিন.আদেশ('rm Bad.class', ['Removed'])
        মেশিন.আদেশ('java Bad', ['cannot read class: -2'])
        # সম্পাদন_মান 입력의 넘친 부분을 잘라서 저장하지 않는다.
        চালনা = len(মেশিন.লগ_সারি)
        মেশিন.직렬.sendall(b'edit Hello.java\n')
        মেশিন.অপেক্ষা_অবস্হা('...> ', চালনা)
        চালনা = len(মেশিন.লগ_সারি)
        মেশিন.직렬.sendall(b'x' * 129 + b'\n')
        মেশিন.অপেক্ষা_অবস্হা('...> ', চালনা)
        মেশিন.আদেশ('.save', ['Too much input; original preserved'])
        মেশিন.আদেশ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        সম্পাদন_মান(মেশিন, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            সম্পাদন_মান(মেশিন, 'f' + str(수), 'occupied')
        মেশিন.আদেশ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        মেশিন.আদেশ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in মেশিন.লগ_সারি.decode('utf-8', 'replace')
        পরিমাপ['serial'] = মেশিন.লগ_সারি.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return পরিমাপ
    finally:
        মেশিন.বন্ধ_করুন()


def 주코드(ডাটা):
    """손상 시험용 main Code의 প্রকৃত_ডাটা নথির_নাম 오프셋/길이만 읽는다."""
    পদ_মান = 8
    def 짧():
        nonlocal পদ_মান
        মান = struct.unpack_from('>H', ডাটা, পদ_মান)[0]
        পদ_মান += 2
        return মান
    def 정():
        nonlocal পদ_মান
        মান = struct.unpack_from('>I', ডাটা, পদ_মান)[0]
        পদ_মান += 4
        return মান
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ডাটা[পদ_মান]
        পদ_মান += 1
        if 종류 == 1:
            দৈর্ঘ্য_মান = 짧()
            문자들[수] = ডাটা[পদ_মান:পদ_মান + দৈর্ঘ্য_মান]
            পদ_মান += দৈর্ঘ্য_মান
        elif 종류 in (7, 8): পদ_মান += 2
        elif 종류 in (3, 9, 10, 12): পদ_মান += 4
        else: raise AssertionError(종류)
    পদ_মান += 6
    개수 = 짧()
    পদ_মান += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        নাম = 짧()
        짧()
        for 수 in range(짧()):
            গুণ_মান = 짧()
            আকার = 정()
            if 문자들[নাম] == b'main' and 문자들[গুণ_মান] == b'Code':
                return পদ_মান + 8, struct.unpack_from('>I', ডাটা, পদ_মান + 4)[0]
            পদ_মান += আকার
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ডিরেক্টরি_মান = Path(임시)
        (ডিরেক্টরি_মান / 'build').mkdir()
        উৎস_নথি = ডিরেক্টরি_মান / 'Imported.java'
        উৎস_নথি.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(উৎস_নথি)], check=True)
        원본 = (ডিরেক্টরি_মান / 'Imported.class').read_bytes()
        কোড_মান, দৈর্ঘ্য_মান = 주코드(원본)
        변형 = {}
        ডাটা = bytearray(원본); ডাটা[0] = 0; 변형['BadMagic'] = ডাটা
        ডাটা = bytearray(원본); ডাটা[7] = 61; 변형['BadVer'] = ডাটা
        ডাটা = bytearray(원본); ডাটা[8:10] = b'\xff\xff'; 변형['BadPool'] = ডাটা
        ডাটা = bytearray(원본); ডাটা[কোড_মান:কোড_মান + দৈর্ঘ্য_মান] = bytes(দৈর্ঘ্য_মান)
        ডাটা[কোড_মান:কোড_মান + 3] = b'\xa7\x00\x01'; ডাটা[কোড_মান + দৈর্ঘ্য_মান - 1] = 177; 변형['BadJump'] = ডাটা
        ডাটা = bytearray(원본); ডাটা[কোড_মান:কোড_মান + দৈর্ঘ্য_মান] = bytes(দৈর্ঘ্য_মান)
        ডাটা[কোড_মান] = 87; ডাটা[কোড_মান + দৈর্ঘ্য_মান - 1] = 177; 변형['BadStack'] = ডাটা
        # নাম 검사를 통과시켜 প্রকৃত_ডাটা কার্যকর_করুন_আদেশ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ভুক্তি_মান = ['Imported.class=' + str(ডিরেক্টরি_মান / 'Imported.class'), 'Imported.java=' + str(উৎস_নথি)]
        for নাম, ডাটা in 변형.items():
            পথ_2 = ডিরেক্টরি_মান / (নাম + '.class'); পথ_2.write_bytes(ডাটা)
            ভুক্তি_মান.append(নাম + '.class=' + str(পথ_2))
        দল_মান = ডিরেক্টরি_মান / 'build/java-files.bin'
        subprocess.run([sys.executable, str(অবস্থান / 'সরঞ্জামগুলি/자바파일묶기.py'), '-o', str(দল_মান)] + ভুক্তি_মান, check=True)
        subprocess.run(['as', '--32', '-o', str(ডিরেক্টরি_মান / 'user.o'), str(অবস্থান / '부팅/ব্যবহারকারী.s')], cwd=str(ডিরেক্টরি_মান), check=True)
        কারনেল_মান = ডিরেক্টরি_মান / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(অবস্থান / '부팅/লিংক_লেআউট.ld'), '-o', str(কারনেল_মান),
                        str(অবস্থান / 'build/boot.o'), str(অবস্থান / 'build/java.o'), str(ডিরেক্টরি_মান / 'user.o'), str(অবস্থান / 'build/apps.o')], check=True)
        মেশিন = কল্পিত_মেশিন(কারনেল_মান, নেটওয়ার্ক_মান=False)
        try:
            মেশিন.আদেশ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            মেশিন.আদেশ('cat Imported.java', ['int[] values = new int[3]'])
            for নাম, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                মেশিন.আদেশ('java ' + নাম, [문구, 'Exit: 1'])
                মেশিন.আদেশ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return মেশিন.লগ_সারি.decode('utf-8', 'replace')
        finally:
            মেশিন.বন্ধ_করুন()


if __name__ == '__main__':
    বিভাজন_করা_মান = argparse.ArgumentParser()
    বিভাজন_করা_মান.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    আর্গুমেন্ট_তালিকা = বিভাজন_করা_মান.parse_args()
    পরিমাপ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if আর্গুমেন্ট_তালিকা.boot == 'both' else (আর্গুমেন্ট_তালিকা.boot,))}
    পরিমাপ['import'] = 적재시험()
    (অবস্থান / 'build/자바시험.json').write_text(json.dumps(পরিমাপ, ensure_ascii=False, indent=2) + '\n')
