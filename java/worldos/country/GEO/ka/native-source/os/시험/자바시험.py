#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 შესრულება_ბრძანება, მარცხი_მნიშვნელობა/რესურსი_მნიშვნელობა 경계 시험."""
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
from 사용자통신시험 import ვირტუალური_კომპიუტერი, პოზიცია


def რედაქტირება_მნიშვნელობა(კომპიუტერი, სახელი, შიგთავსი_მნიშვნელობა, შენახვა_მნიშვნელობა=True):
    გაშვება = len(კომპიუტერი.ჟურნალი_ჩაწერა)
    კომპიუტერი.직렬.sendall(('edit ' + სახელი + '\n').encode())
    კომპიუტერი.მოლოდინი_სტატუსი('...> ', გაშვება)
    for ხაზი in შიგთავსი_მნიშვნელობა.splitlines():
        assert len(ხაზი) <= 128
        გაშვება = len(კომპიუტერი.ჟურნალი_ჩაწერა)
        კომპიუტერი.직렬.sendall((ხაზი + '\n').encode())
        კომპიუტერი.მოლოდინი_სტატუსი('...> ', გაშვება)
    გაშვება = len(კომპიუტერი.ჟურნალი_ჩაწერა)
    კომპიუტერი.직렬.sendall(b'.save\n' if შენახვა_მნიშვნელობა else b'.cancel\n')
    გაზომვა = კომპიუტერი.მოლოდინი_სტატუსი('jkoros> ', გაშვება)
    assert ('Saved:' if შენახვა_მნიშვნელობა else 'Cancelled; original preserved') in გაზომვა, გაზომვა


def ფაილი_მისამართი():
    გაზომვა = subprocess.check_output(['nm', '-n', str(პოზიცია / 'build/kernel.elf')], universal_newlines=True)
    for ხაზი in გაზომვა.splitlines():
        if ხაზი.endswith(' ram_files'):
            return int(ხაზი.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def სტუმარი_ფაილი(კომპიუტერი, სლოტი_მნიშვნელობა, ზომა, გეზი):
    # 시험 VM의 메모리에서 რეალური_მონაცემები 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    მისამართი = ფაილი_მისამართი() + სლოტი_მნიშვნელობა * 16384
    კომპიუტერი.მონიტორი_მნიშვნელობა.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(მისამართი, ზომა, გეზი)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if გეზი.exists() and გეზი.stat().st_size == ზომა:
            return გეზი.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ქსელი_მნიშვნელობა=False)
    გაზომვა = {}
    try:
        კომპიუტერი.ბრძანება('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        კომპიუტერი.ბრძანება('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        კომპიუტერი.ბრძანება('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        კომპიუტერი.ბრძანება('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        კომპიუტერი.ბრძანება('java Missing', ['cannot read class: -2', 'Exit: 1'])
        კომპიუტერი.ბრძანება('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        კომპიუტერი.ბრძანება('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        შიგთავსი_მნიშვნელობა = '''public class Calc {
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
        რედაქტირება_მნიშვნელობა(კომპიუტერი, 'Calc.java', შიგთავსი_მნიშვნელობა)
        კომპიუტერი.ბრძანება('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = კომპიუტერი.ბრძანება('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        გაზომვა['guest_output'] = 출력
        შენატანი_სია = კომპიუტერი.ბრძანება('ls', ['Calc.class'])
        ზომა = int(re.search(r'Calc\.class\s+(\d+) bytes', შენატანი_სია).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as საქაღალდე_მნიშვნელობა:
            გეზი = Path(საქაღალდე_მნიშვნელობა) / 'Calc.class'
            მონაცემები = სტუმარი_ფაილი(კომპიუტერი, 3, ზომა, გეზი)
            რეალური_მონაცემები = subprocess.check_output(['java', '-Xverify:all', '-cp', საქაღალდე_მნიშვნელობა, 'Calc', '6', 'guest'], universal_newlines=True)
            assert რეალური_მონაცემები.splitlines() == 기대, რეალური_მონაცემები
            გაზომვა['class_sha256'] = hashlib.sha256(მონაცემები).hexdigest()
            გაზომვა['openjdk_output'] = რეალური_მონაცემები
        # 실패한 რედაქტირება_მნიშვნელობა/컴파일은 기존 class를 보존한다.
        რედაქტირება_მნიშვნელობა(კომპიუტერი, 'Calc.java', 'not Java at all', შენახვა_მნიშვნელობა=False)
        კომპიუტერი.ბრძანება('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for არასწორი_გაზომვა in [
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
            რედაქტირება_მნიშვნელობა(კომპიუტერი, 'Calc.java', არასწორი_გაზომვა)
            კომპიუტერი.ბრძანება('javac Calc.java', ['javac error:', 'Exit: 1'])
            კომპიუტერი.ბრძანება('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # იტერაცია_მნიშვნელობა 실행은 მომხმარებელი 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            კომპიუტერი.ბრძანება('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        კომპიუტერი.ბრძანება('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        კომპიუტერი.ბრძანება('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        რედაქტირება_მნიშვნელობა(კომპიუტერი, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        კომპიუტერი.ბრძანება('javac Calc.java', ['Compiled:', 'Exit: 0'])
        კომპიუტერი.ბრძანება('java Calc', ['instruction limit', 'Exit: 1'])
        კომპიუტერი.ბრძანება('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        რედაქტირება_მნიშვნელობა(კომპიუტერი, 'Bad.class', 'garbage')
        კომპიუტერი.ბრძანება('java Bad', ['JVM error:', 'Exit: 1'])
        კომპიუტერი.ბრძანება('rm Bad.class', ['Removed'])
        კომპიუტერი.ბრძანება('java Bad', ['cannot read class: -2'])
        # რედაქტირება_მნიშვნელობა 입력의 넘친 부분을 잘라서 저장하지 않는다.
        გაშვება = len(კომპიუტერი.ჟურნალი_ჩაწერა)
        კომპიუტერი.직렬.sendall(b'edit Hello.java\n')
        კომპიუტერი.მოლოდინი_სტატუსი('...> ', გაშვება)
        გაშვება = len(კომპიუტერი.ჟურნალი_ჩაწერა)
        კომპიუტერი.직렬.sendall(b'x' * 129 + b'\n')
        კომპიუტერი.მოლოდინი_სტატუსი('...> ', გაშვება)
        კომპიუტერი.ბრძანება('.save', ['Too much input; original preserved'])
        კომპიუტერი.ბრძანება('javac Hello.java', ['Compiled:', 'Exit: 0'])
        რედაქტირება_მნიშვნელობა(კომპიუტერი, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            რედაქტირება_მნიშვნელობა(კომპიუტერი, 'f' + str(수), 'occupied')
        კომპიუტერი.ბრძანება('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        კომპიუტერი.ბრძანება('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
        გაზომვა['serial'] = კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return გაზომვა
    finally:
        კომპიუტერი.დახურვა()


def 주코드(მონაცემები):
    """손상 시험용 main Code의 რეალური_მონაცემები ფაილი 오프셋/길이만 읽는다."""
    პოზიცია_მნიშვნელობა = 8
    def 짧():
        nonlocal პოზიცია_მნიშვნელობა
        მნიშვნელობა = struct.unpack_from('>H', მონაცემები, პოზიცია_მნიშვნელობა)[0]
        პოზიცია_მნიშვნელობა += 2
        return მნიშვნელობა
    def 정():
        nonlocal პოზიცია_მნიშვნელობა
        მნიშვნელობა = struct.unpack_from('>I', მონაცემები, პოზიცია_მნიშვნელობა)[0]
        პოზიცია_მნიშვნელობა += 4
        return მნიშვნელობა
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = მონაცემები[პოზიცია_მნიშვნელობა]
        პოზიცია_მნიშვნელობა += 1
        if 종류 == 1:
            სიგრძე_მნიშვნელობა = 짧()
            문자들[수] = მონაცემები[პოზიცია_მნიშვნელობა:პოზიცია_მნიშვნელობა + სიგრძე_მნიშვნელობა]
            პოზიცია_მნიშვნელობა += სიგრძე_მნიშვნელობა
        elif 종류 in (7, 8): პოზიცია_მნიშვნელობა += 2
        elif 종류 in (3, 9, 10, 12): პოზიცია_მნიშვნელობა += 4
        else: raise AssertionError(종류)
    პოზიცია_მნიშვნელობა += 6
    개수 = 짧()
    პოზიცია_მნიშვნელობა += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        სახელი = 짧()
        짧()
        for 수 in range(짧()):
            ატრიბუტი_მნიშვნელობა = 짧()
            ზომა = 정()
            if 문자들[სახელი] == b'main' and 문자들[ატრიბუტი_მნიშვნელობა] == b'Code':
                return პოზიცია_მნიშვნელობა + 8, struct.unpack_from('>I', მონაცემები, პოზიცია_მნიშვნელობა + 4)[0]
            პოზიცია_მნიშვნელობა += ზომა
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        საქაღალდე_მნიშვნელობა = Path(임시)
        (საქაღალდე_მნიშვნელობა / 'build').mkdir()
        წყარო = საქაღალდე_მნიშვნელობა / 'Imported.java'
        წყარო.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(წყარო)], check=True)
        원본 = (საქაღალდე_მნიშვნელობა / 'Imported.class').read_bytes()
        კოდექსი_მნიშვნელობა, სიგრძე_მნიშვნელობა = 주코드(원본)
        변형 = {}
        მონაცემები = bytearray(원본); მონაცემები[0] = 0; 변형['BadMagic'] = მონაცემები
        მონაცემები = bytearray(원본); მონაცემები[7] = 61; 변형['BadVer'] = მონაცემები
        მონაცემები = bytearray(원본); მონაცემები[8:10] = b'\xff\xff'; 변형['BadPool'] = მონაცემები
        მონაცემები = bytearray(원본); მონაცემები[კოდექსი_მნიშვნელობა:კოდექსი_მნიშვნელობა + სიგრძე_მნიშვნელობა] = bytes(სიგრძე_მნიშვნელობა)
        მონაცემები[კოდექსი_მნიშვნელობა:კოდექსი_მნიშვნელობა + 3] = b'\xa7\x00\x01'; მონაცემები[კოდექსი_მნიშვნელობა + სიგრძე_მნიშვნელობა - 1] = 177; 변형['BadJump'] = მონაცემები
        მონაცემები = bytearray(원본); მონაცემები[კოდექსი_მნიშვნელობა:კოდექსი_მნიშვნელობა + სიგრძე_მნიშვნელობა] = bytes(სიგრძე_მნიშვნელობა)
        მონაცემები[კოდექსი_მნიშვნელობა] = 87; მონაცემები[კოდექსი_მნიშვნელობა + სიგრძე_მნიშვნელობა - 1] = 177; 변형['BadStack'] = მონაცემები
        # სახელი 검사를 통과시켜 რეალური_მონაცემები შესრულება_ბრძანება 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        შენატანი_მნიშვნელობა = ['Imported.class=' + str(საქაღალდე_მნიშვნელობა / 'Imported.class'), 'Imported.java=' + str(წყარო)]
        for სახელი, მონაცემები in 변형.items():
            გეზი = საქაღალდე_მნიშვნელობა / (სახელი + '.class'); გეზი.write_bytes(მონაცემები)
            შენატანი_მნიშვნელობა.append(სახელი + '.class=' + str(გეზი))
        ჯგუფი_მნიშვნელობა = საქაღალდე_მნიშვნელობა / 'build/java-files.bin'
        subprocess.run([sys.executable, str(პოზიცია / 'ხელსაწყოები/자바파일묶기.py'), '-o', str(ჯგუფი_მნიშვნელობა)] + შენატანი_მნიშვნელობა, check=True)
        subprocess.run(['as', '--32', '-o', str(საქაღალდე_მნიშვნელობა / 'user.o'), str(პოზიცია / '부팅/მომხმარებელი.s')], cwd=str(საქაღალდე_მნიშვნელობა), check=True)
        ბირთვი_მნიშვნელობა = საქაღალდე_მნიშვნელობა / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(პოზიცია / '부팅/ბმული_განლაგება.ld'), '-o', str(ბირთვი_მნიშვნელობა),
                        str(პოზიცია / 'build/boot.o'), str(პოზიცია / 'build/java.o'), str(საქაღალდე_მნიშვნელობა / 'user.o'), str(პოზიცია / 'build/apps.o')], check=True)
        კომპიუტერი = ვირტუალური_კომპიუტერი(ბირთვი_მნიშვნელობა, ქსელი_მნიშვნელობა=False)
        try:
            კომპიუტერი.ბრძანება('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            კომპიუტერი.ბრძანება('cat Imported.java', ['int[] values = new int[3]'])
            for სახელი, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                კომპიუტერი.ბრძანება('java ' + სახელი, [문구, 'Exit: 1'])
                კომპიუტერი.ბრძანება('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
        finally:
            კომპიუტერი.დახურვა()


if __name__ == '__main__':
    ანალიზი_მნიშვნელობა = argparse.ArgumentParser()
    ანალიზი_მნიშვნელობა.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ანალიზი_მნიშვნელობა.parse_args()
    გაზომვა = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    გაზომვა['import'] = 적재시험()
    (პოზიცია / 'build/자바시험.json').write_text(json.dumps(გაზომვა, ensure_ascii=False, indent=2) + '\n')
