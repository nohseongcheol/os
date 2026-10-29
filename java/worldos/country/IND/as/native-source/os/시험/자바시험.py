#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 নিষ্পাদন_আদেশ, বিফলতা_মান/সম্পদ_মান 경계 시험."""
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
from 사용자통신시험 import ভাৰ্ছুৱেল_মেচিন, অৱস্থান


def সম্পাদনা_মান(মেচিন, নাম, সামগ্ৰী_মান, জমা_কৰক_মান=True):
    সঞ্চালন = len(মেচিন.লগ_শাৰী)
    মেচিন.직렬.sendall(('edit ' + নাম + '\n').encode())
    মেচিন.기다림('...> ', সঞ্চালন)
    for লাইন in সামগ্ৰী_মান.splitlines():
        assert len(লাইন) <= 128
        সঞ্চালন = len(মেচিন.লগ_শাৰী)
        মেচিন.직렬.sendall((লাইন + '\n').encode())
        মেচিন.기다림('...> ', সঞ্চালন)
    সঞ্চালন = len(মেচিন.লগ_শাৰী)
    মেচিন.직렬.sendall(b'.save\n' if জমা_কৰক_মান else b'.cancel\n')
    পৰিমাপ = মেচিন.기다림('jkoros> ', সঞ্চালন)
    assert ('Saved:' if জমা_কৰক_মান else 'Cancelled; original preserved') in পৰিমাপ, পৰিমাপ


def ফাইল_ঠিকনা():
    পৰিমাপ = subprocess.check_output(['nm', '-n', str(অৱস্থান / 'build/kernel.elf')], universal_newlines=True)
    for লাইন in পৰিমাপ.splitlines():
        if লাইন.endswith(' ram_files'):
            return int(লাইন.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def অতিথি_ফাইল(মেচিন, শ্লট_মান, মাপ, পথ):
    # 시험 VM의 메모리에서 প্ৰকৃত_ডাটা 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ঠিকনা = ফাইল_ঠিকনা() + শ্লট_মান * 16384
    মেচিন.মনিটৰ_মান.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ঠিকনা, মাপ, পথ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if পথ.exists() and পথ.stat().st_size == মাপ:
            return পথ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, নেটৱৰ্ক_মান=False)
    পৰিমাপ = {}
    try:
        মেচিন.কমান্ড('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        মেচিন.কমান্ড('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        মেচিন.কমান্ড('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        মেচিন.কমান্ড('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        মেচিন.কমান্ড('java Missing', ['cannot read class: -2', 'Exit: 1'])
        মেচিন.কমান্ড('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        মেচিন.কমান্ড('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        সামগ্ৰী_মান = '''public class Calc {
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
        সম্পাদনা_মান(মেচিন, 'Calc.java', সামগ্ৰী_মান)
        মেচিন.কমান্ড('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        নিৰ্গম = মেচিন.কমান্ড('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        পৰিমাপ['guest_output'] = নিৰ্গম
        প্রবিষ্ট_সূচী = মেচিন.কমান্ড('ls', ['Calc.class'])
        মাপ = int(re.search(r'Calc\.class\s+(\d+) bytes', প্রবিষ্ট_সূচী).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ডাইৰেক্টৰী_মান:
            পথ = Path(ডাইৰেক্টৰী_মান) / 'Calc.class'
            ডাটা = অতিথি_ফাইল(মেচিন, 3, মাপ, পথ)
            প্ৰকৃত_ডাটা = subprocess.check_output(['java', '-Xverify:all', '-cp', ডাইৰেক্টৰী_মান, 'Calc', '6', 'guest'], universal_newlines=True)
            assert প্ৰকৃত_ডাটা.splitlines() == 기대, প্ৰকৃত_ডাটা
            পৰিমাপ['class_sha256'] = hashlib.sha256(ডাটা).hexdigest()
            পৰিমাপ['openjdk_output'] = প্ৰকৃত_ডাটা
        # 실패한 সম্পাদনা_মান/컴파일은 기존 class를 보존한다.
        সম্পাদনা_মান(মেচিন, 'Calc.java', 'not Java at all', জমা_কৰক_মান=False)
        মেচিন.কমান্ড('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for অবৈধ_পৰিমাপ in [
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
            সম্পাদনা_মান(মেচিন, 'Calc.java', অবৈধ_পৰিমাপ)
            মেচিন.কমান্ড('javac Calc.java', ['javac error:', 'Exit: 1'])
            মেচিন.কমান্ড('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # পুণৰাবৃত্তি_মান 실행은 ব্যৱহাৰকৰ্তা 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            মেচিন.কমান্ড('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        মেচিন.কমান্ড('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        মেচিন.কমান্ড('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        সম্পাদনা_মান(মেচিন, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        মেচিন.কমান্ড('javac Calc.java', ['Compiled:', 'Exit: 0'])
        মেচিন.কমান্ড('java Calc', ['instruction limit', 'Exit: 1'])
        মেচিন.কমান্ড('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        সম্পাদনা_মান(মেচিন, 'Bad.class', 'garbage')
        মেচিন.কমান্ড('java Bad', ['JVM error:', 'Exit: 1'])
        মেচিন.কমান্ড('rm Bad.class', ['Removed'])
        মেচিন.কমান্ড('java Bad', ['cannot read class: -2'])
        # সম্পাদনা_মান 입력의 넘친 부분을 잘라서 저장하지 않는다.
        সঞ্চালন = len(মেচিন.লগ_শাৰী)
        মেচিন.직렬.sendall(b'edit Hello.java\n')
        মেচিন.기다림('...> ', সঞ্চালন)
        সঞ্চালন = len(মেচিন.লগ_শাৰী)
        মেচিন.직렬.sendall(b'x' * 129 + b'\n')
        মেচিন.기다림('...> ', সঞ্চালন)
        মেচিন.কমান্ড('.save', ['Too much input; original preserved'])
        মেচিন.কমান্ড('javac Hello.java', ['Compiled:', 'Exit: 0'])
        সম্পাদনা_মান(মেচিন, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            সম্পাদনা_মান(মেচিন, 'f' + str(수), 'occupied')
        মেচিন.কমান্ড('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        মেচিন.কমান্ড('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
        পৰিমাপ['serial'] = মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return পৰিমাপ
    finally:
        মেচিন.বন্ধ_কৰক()


def 주코드(ডাটা):
    """손상 시험용 main Code의 প্ৰকৃত_ডাটা নথিপত্ৰ 오프셋/길이만 읽는다."""
    স্থান_সলনি_কৰক_মান = 8
    def 짧():
        nonlocal স্থান_সলনি_কৰক_মান
        মান = struct.unpack_from('>H', ডাটা, স্থান_সলনি_কৰক_মান)[0]
        স্থান_সলনি_কৰক_মান += 2
        return মান
    def 정():
        nonlocal স্থান_সলনি_কৰক_মান
        মান = struct.unpack_from('>I', ডাটা, স্থান_সলনি_কৰক_মান)[0]
        স্থান_সলনি_কৰক_মান += 4
        return মান
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ডাটা[স্থান_সলনি_কৰক_মান]
        স্থান_সলনি_কৰক_মান += 1
        if 종류 == 1:
            দৈর্ঘ্য_মান = 짧()
            문자들[수] = ডাটা[স্থান_সলনি_কৰক_মান:স্থান_সলনি_কৰক_মান + দৈর্ঘ্য_মান]
            স্থান_সলনি_কৰক_মান += দৈর্ঘ্য_মান
        elif 종류 in (7, 8): স্থান_সলনি_কৰক_মান += 2
        elif 종류 in (3, 9, 10, 12): স্থান_সলনি_কৰক_মান += 4
        else: raise AssertionError(종류)
    স্থান_সলনি_কৰক_মান += 6
    개수 = 짧()
    স্থান_সলনি_কৰক_মান += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        নাম = 짧()
        짧()
        for 수 in range(짧()):
            গুণাগুণ_মান = 짧()
            মাপ = 정()
            if 문자들[নাম] == b'main' and 문자들[গুণাগুণ_মান] == b'Code':
                return স্থান_সলনি_কৰক_মান + 8, struct.unpack_from('>I', ডাটা, স্থান_সলনি_কৰক_মান + 4)[0]
            স্থান_সলনি_কৰক_মান += মাপ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ডাইৰেক্টৰী_মান = Path(임시)
        (ডাইৰেক্টৰী_মান / 'build').mkdir()
        উৎস = ডাইৰেক্টৰী_মান / 'Imported.java'
        উৎস.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(উৎস)], check=True)
        원본 = (ডাইৰেক্টৰী_মান / 'Imported.class').read_bytes()
        코드, দৈর্ঘ্য_মান = 주코드(원본)
        변형 = {}
        ডাটা = bytearray(원본); ডাটা[0] = 0; 변형['BadMagic'] = ডাটা
        ডাটা = bytearray(원본); ডাটা[7] = 61; 변형['BadVer'] = ডাটা
        ডাটা = bytearray(원본); ডাটা[8:10] = b'\xff\xff'; 변형['BadPool'] = ডাটা
        ডাটা = bytearray(원본); ডাটা[코드:코드 + দৈর্ঘ্য_মান] = bytes(দৈর্ঘ্য_মান)
        ডাটা[코드:코드 + 3] = b'\xa7\x00\x01'; ডাটা[코드 + দৈর্ঘ্য_মান - 1] = 177; 변형['BadJump'] = ডাটা
        ডাটা = bytearray(원본); ডাটা[코드:코드 + দৈর্ঘ্য_মান] = bytes(দৈর্ঘ্য_মান)
        ডাটা[코드] = 87; ডাটা[코드 + দৈর্ঘ্য_মান - 1] = 177; 변형['BadStack'] = ডাটা
        # নাম 검사를 통과시켜 প্ৰকৃত_ডাটা নিষ্পাদন_আদেশ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        প্রবিষ্ট_মান = ['Imported.class=' + str(ডাইৰেক্টৰী_মান / 'Imported.class'), 'Imported.java=' + str(উৎস)]
        for নাম, ডাটা in 변형.items():
            পথ = ডাইৰেক্টৰী_মান / (নাম + '.class'); পথ.write_bytes(ডাটা)
            প্রবিষ্ট_মান.append(নাম + '.class=' + str(পথ))
        দল_মান = ডাইৰেক্টৰী_মান / 'build/java-files.bin'
        subprocess.run([sys.executable, str(অৱস্থান / 'সঁজুলিসমূহ/자바파일묶기.py'), '-o', str(দল_মান)] + প্রবিষ্ট_মান, check=True)
        subprocess.run(['as', '--32', '-o', str(ডাইৰেক্টৰী_মান / 'user.o'), str(অৱস্থান / '부팅/ব্যৱহাৰকৰ্তা.s')], cwd=str(ডাইৰেক্টৰী_মান), check=True)
        কাৰ্ণেল_মান = ডাইৰেক্টৰী_মান / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(অৱস্থান / '부팅/লিংক_লেআউট.ld'), '-o', str(কাৰ্ণেল_মান),
                        str(অৱস্থান / 'build/boot.o'), str(অৱস্থান / 'build/java.o'), str(ডাইৰেক্টৰী_মান / 'user.o'), str(অৱস্থান / 'build/apps.o')], check=True)
        মেচিন = ভাৰ্ছুৱেল_মেচিন(কাৰ্ণেল_মান, নেটৱৰ্ক_মান=False)
        try:
            মেচিন.কমান্ড('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            মেচিন.কমান্ড('cat Imported.java', ['int[] values = new int[3]'])
            for নাম, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                মেচিন.কমান্ড('java ' + নাম, [문구, 'Exit: 1'])
                মেচিন.কমান্ড('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
        finally:
            মেচিন.বন্ধ_কৰক()


if __name__ == '__main__':
    পাৰ্ছ_কৰক_মান = argparse.ArgumentParser()
    পাৰ্ছ_কৰক_মান.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = পাৰ্ছ_কৰক_মান.parse_args()
    পৰিমাপ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    পৰিমাপ['import'] = 적재시험()
    (অৱস্থান / 'build/자바시험.json').write_text(json.dumps(পৰিমাপ, ensure_ascii=False, indent=2) + '\n')
