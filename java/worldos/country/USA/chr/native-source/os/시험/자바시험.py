#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ, ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ/ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ 경계 시험."""
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
from ᎠᏓᎪᎵᏰᏍᎩ_ᎬᏗᏍᎩ_ᏧᎾᏚᏓᎵ import 가상기계, 위치


def ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, ᏚᏙᎥᎢ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, Store_ᏧᎬᏩᎶᏗᏯ=True):
    ᎠᎢᏎᏍᏗ = len(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
    기계.직렬.sendall(('edit ' + ᏚᏙᎥᎢ + '\n').encode())
    기계.기다림('...> ', ᎠᎢᏎᏍᏗ)
    for ᏚᏓᏅᏅᎢ in ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.splitlines():
        assert len(ᏚᏓᏅᏅᎢ) <= 128
        ᎠᎢᏎᏍᏗ = len(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        기계.직렬.sendall((ᏚᏓᏅᏅᎢ + '\n').encode())
        기계.기다림('...> ', ᎠᎢᏎᏍᏗ)
    ᎠᎢᏎᏍᏗ = len(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
    기계.직렬.sendall(b'.save\n' if Store_ᏧᎬᏩᎶᏗᏯ else b'.cancel\n')
    결과 = 기계.기다림('jkoros> ', ᎠᎢᏎᏍᏗ)
    assert ('Saved:' if Store_ᏧᎬᏩᎶᏗᏯ else 'Cancelled; original preserved') in 결과, 결과


def ᎠᏍᏆᏂᎪᏙᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for ᏚᏓᏅᏅᎢ in 결과.splitlines():
        if ᏚᏓᏅᏅᎢ.endswith(' ram_files'):
            return int(ᏚᏓᏅᏅᎢ.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ᎠᏓᏩᏛᎯᏙᎯ_ᎠᏍᏆᏂᎪᏙᏗ(기계, 슬롯, ᎢᎩᏓ, ᎠᏍᏓᏩᏛᏍᏗ):
    # 시험 VM의 메모리에서 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = ᎠᏍᏆᏂᎪᏙᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ() + 슬롯 * 16384
    기계.ᎠᏓᏴᎵᏛᏍᎩ_ᏧᎬᏩᎶᏗᏯ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎢᎩᏓ, ᎠᏍᏓᏩᏛᏍᏗ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ᎠᏍᏓᏩᏛᏍᏗ.exists() and ᎠᏍᏓᏩᏛᏍᏗ.stat().st_size == ᎢᎩᏓ:
            return ᎠᏍᏓᏩᏛᏍᏗ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def ᎠᏓᎪᎵᏰᏍᎩ_ᎠᎢᏎᏍᏗ(종류):
    기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ᏧᎾᏚᏓᎵ_ᏧᎬᏩᎶᏗᏯ=False)
    결과 = {}
    try:
        기계.ᎤᏁᏤᎸᎩ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        기계.ᎤᏁᏤᎸᎩ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        기계.ᎤᏁᏤᎸᎩ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        기계.ᎤᏁᏤᎸᎩ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        기계.ᎤᏁᏤᎸᎩ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        기계.ᎤᏁᏤᎸᎩ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        기계.ᎤᏁᏤᎸᎩ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ = '''public class Calc {
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
        ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'Calc.java', ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ)
        기계.ᎤᏁᏤᎸᎩ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = 기계.ᎤᏁᏤᎸᎩ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ = 기계.ᎤᏁᏤᎸᎩ('ls', ['Calc.class'])
        ᎢᎩᏓ = int(re.search(r'Calc\.class\s+(\d+) bytes', Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ:
            ᎠᏍᏓᏩᏛᏍᏗ = Path(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ) / 'Calc.class'
            ᎦᏟᏌᏅᎯ = ᎠᏓᏩᏛᎯᏙᎯ_ᎠᏍᏆᏂᎪᏙᏗ(기계, 3, ᎢᎩᏓ, ᎠᏍᏓᏩᏛᏍᏗ)
            ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ = subprocess.check_output(['java', '-Xverify:all', '-cp', ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ.splitlines() == 기대, ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ
            결과['class_sha256'] = hashlib.sha256(ᎦᏟᏌᏅᎯ).hexdigest()
            결과['openjdk_output'] = ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ
        # 실패한 ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ/컴파일은 기존 class를 보존한다.
        ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'Calc.java', 'not Java at all', Store_ᏧᎬᏩᎶᏗᏯ=False)
        기계.ᎤᏁᏤᎸᎩ('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'Calc.java', 잘못)
            기계.ᎤᏁᏤᎸᎩ('javac Calc.java', ['javac error:', 'Exit: 1'])
            기계.ᎤᏁᏤᎸᎩ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # 반복 실행은 ᎬᏗᏍᎩ 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            기계.ᎤᏁᏤᎸᎩ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        기계.ᎤᏁᏤᎸᎩ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        기계.ᎤᏁᏤᎸᎩ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        기계.ᎤᏁᏤᎸᎩ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        기계.ᎤᏁᏤᎸᎩ('java Calc', ['instruction limit', 'Exit: 1'])
        기계.ᎤᏁᏤᎸᎩ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'Bad.class', 'garbage')
        기계.ᎤᏁᏤᎸᎩ('java Bad', ['JVM error:', 'Exit: 1'])
        기계.ᎤᏁᏤᎸᎩ('rm Bad.class', ['Removed'])
        기계.ᎤᏁᏤᎸᎩ('java Bad', ['cannot read class: -2'])
        # ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ᎠᎢᏎᏍᏗ = len(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        기계.직렬.sendall(b'edit Hello.java\n')
        기계.기다림('...> ', ᎠᎢᏎᏍᏗ)
        ᎠᎢᏎᏍᏗ = len(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        기계.직렬.sendall(b'x' * 129 + b'\n')
        기계.기다림('...> ', ᎠᎢᏎᏍᏗ)
        기계.ᎤᏁᏤᎸᎩ('.save', ['Too much input; original preserved'])
        기계.ᎤᏁᏤᎸᎩ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'f' + str(수), 'occupied')
        기계.ᎤᏁᏤᎸᎩ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        기계.ᎤᏁᏤᎸᎩ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
        결과['serial'] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        기계.ᎯᏍᏚᎲᎦ()


def 주코드(ᎦᏟᏌᏅᎯ):
    """손상 시험용 main Code의 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ ᎠᏍᏆᏂᎪᏙᏗ 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        ᏧᎬᏩᎶᏗᏯ = struct.unpack_from('>H', ᎦᏟᏌᏅᎯ, 위치값)[0]
        위치값 += 2
        return ᏧᎬᏩᎶᏗᏯ
    def 정():
        nonlocal 위치값
        ᏧᎬᏩᎶᏗᏯ = struct.unpack_from('>I', ᎦᏟᏌᏅᎯ, 위치값)[0]
        위치값 += 4
        return ᏧᎬᏩᎶᏗᏯ
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ᎦᏟᏌᏅᎯ[위치값]
        위치값 += 1
        if 종류 == 1:
            ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = 짧()
            문자들[수] = ᎦᏟᏌᏅᎯ[위치값:위치값 + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ]
            위치값 += ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ᏚᏙᎥᎢ = 짧()
        짧()
        for 수 in range(짧()):
            ᏄᏍᏛ_ᎠᎦᏅᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 짧()
            ᎢᎩᏓ = 정()
            if 문자들[ᏚᏙᎥᎢ] == b'main' and 문자들[ᏄᏍᏛ_ᎠᎦᏅᏛᎢ_ᏧᎬᏩᎶᏗᏯ] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', ᎦᏟᏌᏅᎯ, 위치값 + 4)[0]
            위치값 += ᎢᎩᏓ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ = Path(임시)
        (ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'build').mkdir()
        ᎦᏟᏌᏅᎯ_0201f362 = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'Imported.java'
        ᎦᏟᏌᏅᎯ_0201f362.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ᎦᏟᏌᏅᎯ_0201f362)], check=True)
        원본 = (ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'Imported.class').read_bytes()
        코드, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = 주코드(원본)
        변형 = {}
        ᎦᏟᏌᏅᎯ = bytearray(원본); ᎦᏟᏌᏅᎯ[0] = 0; 변형['BadMagic'] = ᎦᏟᏌᏅᎯ
        ᎦᏟᏌᏅᎯ = bytearray(원본); ᎦᏟᏌᏅᎯ[7] = 61; 변형['BadVer'] = ᎦᏟᏌᏅᎯ
        ᎦᏟᏌᏅᎯ = bytearray(원본); ᎦᏟᏌᏅᎯ[8:10] = b'\xff\xff'; 변형['BadPool'] = ᎦᏟᏌᏅᎯ
        ᎦᏟᏌᏅᎯ = bytearray(원본); ᎦᏟᏌᏅᎯ[코드:코드 + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ] = bytes(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ)
        ᎦᏟᏌᏅᎯ[코드:코드 + 3] = b'\xa7\x00\x01'; ᎦᏟᏌᏅᎯ[코드 + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ - 1] = 177; 변형['BadJump'] = ᎦᏟᏌᏅᎯ
        ᎦᏟᏌᏅᎯ = bytearray(원본); ᎦᏟᏌᏅᎯ[코드:코드 + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ] = bytes(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ)
        ᎦᏟᏌᏅᎯ[코드] = 87; ᎦᏟᏌᏅᎯ[코드 + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ - 1] = 177; 변형['BadStack'] = ᎦᏟᏌᏅᎯ
        # ᏚᏙᎥᎢ 검사를 통과시켜 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = ['Imported.class=' + str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'Imported.class'), 'Imported.java=' + str(ᎦᏟᏌᏅᎯ_0201f362)]
        for ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ in 변형.items():
            ᎠᏍᏓᏩᏛᏍᏗ = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / (ᏚᏙᎥᎢ + '.class'); ᎠᏍᏓᏩᏛᏍᏗ.write_bytes(ᎦᏟᏌᏅᎯ)
            Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.append(ᏚᏙᎥᎢ + '.class=' + str(ᎠᏍᏓᏩᏛᏍᏗ))
        ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / '도구/자바파일묶기.py'), '-o', str(ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ)] + Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ, check=True)
        subprocess.run(['as', '--32', '-o', str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'user.o'), str(위치 / '부팅/ᎬᏗᏍᎩ.s')], cwd=str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ), check=True)
        kernel_ᏧᎬᏩᎶᏗᏯ = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/ᎫᏓᎸᎢ_ᏱᎬᏂ.ld'), '-o', str(kernel_ᏧᎬᏩᎶᏗᏯ),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        기계 = 가상기계(kernel_ᏧᎬᏩᎶᏗᏯ, ᏧᎾᏚᏓᎵ_ᏧᎬᏩᎶᏗᏯ=False)
        try:
            기계.ᎤᏁᏤᎸᎩ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            기계.ᎤᏁᏤᎸᎩ('cat Imported.java', ['int[] values = new int[3]'])
            for ᏚᏙᎥᎢ, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                기계.ᎤᏁᏤᎸᎩ('java ' + ᏚᏙᎥᎢ, [문구, 'Exit: 1'])
                기계.ᎤᏁᏤᎸᎩ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
        finally:
            기계.ᎯᏍᏚᎲᎦ()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = 해석.parse_args()
    결과 = {종류: ᎠᏓᎪᎵᏰᏍᎩ_ᎠᎢᏎᏍᏗ(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
