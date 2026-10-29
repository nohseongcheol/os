#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 실행, неуспјех_вриједност/ресурс_вриједност 경계 시험."""
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
from 사용자통신시험 import 가상기계, 위치


def уређивати_вриједност(기계, назив, Садржај_вриједност, похранити_вриједност=True):
    시작 = len(기계.дневник_рада_ред)
    기계.직렬.sendall(('edit ' + назив + '\n').encode())
    기계.기다림('...> ', 시작)
    for редак in Садржај_вриједност.splitlines():
        assert len(редак) <= 128
        시작 = len(기계.дневник_рада_ред)
        기계.직렬.sendall((редак + '\n').encode())
        기계.기다림('...> ', 시작)
    시작 = len(기계.дневник_рада_ред)
    기계.직렬.sendall(b'.save\n' if похранити_вриједност else b'.cancel\n')
    결과 = 기계.기다림('jkoros> ', 시작)
    assert ('Saved:' if похранити_вриједност else 'Cancelled; original preserved') in 결과, 결과


def фајл_адреса():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for редак in 결과.splitlines():
        if редак.endswith(' ram_files'):
            return int(редак.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(기계, 슬롯, подесити_величину, пут):
    # 시험 VM의 메모리에서 стваран_подаци 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    адреса = фајл_адреса() + 슬롯 * 16384
    기계.монитор_вриједност.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(адреса, подесити_величину, пут)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if пут.exists() and пут.stat().st_size == подесити_величину:
            return пут.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Мрежа_вриједност=False)
    결과 = {}
    try:
        기계.команда('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        기계.команда('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        기계.команда('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        기계.команда('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        기계.команда('java Missing', ['cannot read class: -2', 'Exit: 1'])
        기계.команда('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        기계.команда('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Садржај_вриједност = '''public class Calc {
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
        уређивати_вриједност(기계, 'Calc.java', Садржај_вриједност)
        기계.команда('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = 기계.команда('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        унос_списак = 기계.команда('ls', ['Calc.class'])
        подесити_величину = int(re.search(r'Calc\.class\s+(\d+) bytes', унос_списак).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as директориј_вриједност:
            пут = Path(директориј_вриједност) / 'Calc.class'
            подаци = 게스트파일(기계, 3, подесити_величину, пут)
            стваран_подаци = subprocess.check_output(['java', '-Xverify:all', '-cp', директориј_вриједност, 'Calc', '6', 'guest'], universal_newlines=True)
            assert стваран_подаци.splitlines() == 기대, стваран_подаци
            결과['class_sha256'] = hashlib.sha256(подаци).hexdigest()
            결과['openjdk_output'] = стваран_подаци
        # 실패한 уређивати_вриједност/컴파일은 기존 class를 보존한다.
        уређивати_вриједност(기계, 'Calc.java', 'not Java at all', похранити_вриједност=False)
        기계.команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            уређивати_вриједност(기계, 'Calc.java', 잘못)
            기계.команда('javac Calc.java', ['javac error:', 'Exit: 1'])
            기계.команда('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # понављање_вриједност 실행은 корисник 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            기계.команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        기계.команда('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        기계.команда('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        уређивати_вриједност(기계, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        기계.команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        기계.команда('java Calc', ['instruction limit', 'Exit: 1'])
        기계.команда('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        уређивати_вриједност(기계, 'Bad.class', 'garbage')
        기계.команда('java Bad', ['JVM error:', 'Exit: 1'])
        기계.команда('rm Bad.class', ['Removed'])
        기계.команда('java Bad', ['cannot read class: -2'])
        # уређивати_вриједност 입력의 넘친 부분을 잘라서 저장하지 않는다.
        시작 = len(기계.дневник_рада_ред)
        기계.직렬.sendall(b'edit Hello.java\n')
        기계.기다림('...> ', 시작)
        시작 = len(기계.дневник_рада_ред)
        기계.직렬.sendall(b'x' * 129 + b'\n')
        기계.기다림('...> ', 시작)
        기계.команда('.save', ['Too much input; original preserved'])
        기계.команда('javac Hello.java', ['Compiled:', 'Exit: 0'])
        уређивати_вриједност(기계, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            уређивати_вриједност(기계, 'f' + str(수), 'occupied')
        기계.команда('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        기계.команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 기계.дневник_рада_ред.decode('utf-8', 'replace')
        결과['serial'] = 기계.дневник_рада_ред.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        기계.затворити()


def 주코드(подаци):
    """손상 시험용 main Code의 стваран_подаци фајл 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        вриједност = struct.unpack_from('>H', подаци, 위치값)[0]
        위치값 += 2
        return вриједност
    def 정():
        nonlocal 위치값
        вриједност = struct.unpack_from('>I', подаци, 위치값)[0]
        위치값 += 4
        return вриједност
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = подаци[위치값]
        위치값 += 1
        if 종류 == 1:
            дужина_вриједност = 짧()
            문자들[수] = подаци[위치값:위치값 + дужина_вриједност]
            위치값 += дужина_вриједност
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        назив = 짧()
        짧()
        for 수 in range(짧()):
            атрибут_вриједност = 짧()
            подесити_величину = 정()
            if 문자들[назив] == b'main' and 문자들[атрибут_вриједност] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', подаци, 위치값 + 4)[0]
            위치값 += подесити_величину
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        директориј_вриједност = Path(임시)
        (директориј_вриједност / 'build').mkdir()
        извор = директориј_вриједност / 'Imported.java'
        извор.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(извор)], check=True)
        원본 = (директориј_вриједност / 'Imported.class').read_bytes()
        코드, дужина_вриједност = 주코드(원본)
        변형 = {}
        подаци = bytearray(원본); подаци[0] = 0; 변형['BadMagic'] = подаци
        подаци = bytearray(원본); подаци[7] = 61; 변형['BadVer'] = подаци
        подаци = bytearray(원본); подаци[8:10] = b'\xff\xff'; 변형['BadPool'] = подаци
        подаци = bytearray(원본); подаци[코드:코드 + дужина_вриједност] = bytes(дужина_вриједност)
        подаци[코드:코드 + 3] = b'\xa7\x00\x01'; подаци[코드 + дужина_вриједност - 1] = 177; 변형['BadJump'] = подаци
        подаци = bytearray(원본); подаци[코드:코드 + дужина_вриједност] = bytes(дужина_вриједност)
        подаци[코드] = 87; подаци[코드 + дужина_вриједност - 1] = 177; 변형['BadStack'] = подаци
        # назив 검사를 통과시켜 стваран_подаци 실행 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        унос_вриједност = ['Imported.class=' + str(директориј_вриједност / 'Imported.class'), 'Imported.java=' + str(извор)]
        for назив, подаци in 변형.items():
            пут = директориј_вриједност / (назив + '.class'); пут.write_bytes(подаци)
            унос_вриједност.append(назив + '.class=' + str(пут))
        група_вриједност = директориј_вриједност / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / '도구/자바파일묶기.py'), '-o', str(група_вриједност)] + унос_вриједност, check=True)
        subprocess.run(['as', '--32', '-o', str(директориј_вриједност / 'user.o'), str(위치 / '부팅/корисник.s')], cwd=str(директориј_вриједност), check=True)
        језгро_вриједност = директориј_вриједност / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/веза_изглед.ld'), '-o', str(језгро_вриједност),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(директориј_вриједност / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        기계 = 가상기계(језгро_вриједност, Мрежа_вриједност=False)
        try:
            기계.команда('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            기계.команда('cat Imported.java', ['int[] values = new int[3]'])
            for назив, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                기계.команда('java ' + назив, [문구, 'Exit: 1'])
                기계.команда('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 기계.дневник_рада_ред.decode('utf-8', 'replace')
        finally:
            기계.затворити()


if __name__ == '__main__':
    рашчлањивати_вриједност = argparse.ArgumentParser()
    рашчлањивати_вриједност.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = рашчлањивати_вриједност.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
