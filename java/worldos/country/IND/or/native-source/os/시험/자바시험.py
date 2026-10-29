#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ, ବିଫଳତା_ମୂଲ୍ୟ/ଉତ୍ସ_ମୂଲ୍ୟ 경계 시험."""
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
from 사용자통신시험 import ବାସ୍ତବ_ମେସିନ୍, ଅବସ୍ଥାନ


def ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, ନାମ, ବିଷୟ_ମୂଲ୍ୟ, ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ=True):
    ଚଳାନ୍ତୁ = len(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
    ମେସିନ୍.직렬.sendall(('edit ' + ନାମ + '\n').encode())
    ମେସିନ୍.ଅପେକ୍ଷା_ସ୍ଥିତି('...> ', ଚଳାନ୍ତୁ)
    for ରେଖା in ବିଷୟ_ମୂଲ୍ୟ.splitlines():
        assert len(ରେଖା) <= 128
        ଚଳାନ୍ତୁ = len(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
        ମେସିନ୍.직렬.sendall((ରେଖା + '\n').encode())
        ମେସିନ୍.ଅପେକ୍ଷା_ସ୍ଥିତି('...> ', ଚଳାନ୍ତୁ)
    ଚଳାନ୍ତୁ = len(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
    ମେସିନ୍.직렬.sendall(b'.save\n' if ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ else b'.cancel\n')
    ମାପ = ମେସିନ୍.ଅପେକ୍ଷା_ସ୍ଥିତି('jkoros> ', ଚଳାନ୍ତୁ)
    assert ('Saved:' if ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ else 'Cancelled; original preserved') in ମାପ, ମାପ


def ଫାଇଲ୍_ଠିକଣା():
    ମାପ = subprocess.check_output(['nm', '-n', str(ଅବସ୍ଥାନ / 'build/kernel.elf')], universal_newlines=True)
    for ରେଖା in ମାପ.splitlines():
        if ରେଖା.endswith(' ram_files'):
            return int(ରେଖା.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ଅତିଥି_ଫାଇଲ୍(ମେସିନ୍, ସ୍ଲଟ୍_ମୂଲ୍ୟ, ଆକାର, ପଥ):
    # 시험 VM의 메모리에서 ପ୍ରକୃତ_ଡାଟା 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ଠିକଣା = ଫାଇଲ୍_ଠିକଣା() + ସ୍ଲଟ୍_ମୂଲ୍ୟ * 16384
    ମେସିନ୍.ମନିଟର୍_ମୂଲ୍ୟ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ଠିକଣା, ଆକାର, ପଥ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ପଥ.exists() and ପଥ.stat().st_size == ଆକାର:
            return ପଥ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ନେଟ୍_ୱାର୍କ୍_ମୂଲ୍ୟ=False)
    ମାପ = {}
    try:
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ବିଷୟ_ମୂଲ୍ୟ = '''public class Calc {
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
        ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'Calc.java', ବିଷୟ_ମୂଲ୍ୟ)
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        ନିର୍ଗମ = ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ମାପ['guest_output'] = ନିର୍ଗମ
        ଏଣ୍ଟ୍ରି_ତାଲିକା = ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('ls', ['Calc.class'])
        ଆକାର = int(re.search(r'Calc\.class\s+(\d+) bytes', ଏଣ୍ଟ୍ରି_ତାଲିକା).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ:
            ପଥ = Path(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ) / 'Calc.class'
            ଡାଟା = ଅତିଥି_ଫାଇଲ୍(ମେସିନ୍, 3, ଆକାର, ପଥ)
            ପ୍ରକୃତ_ଡାଟା = subprocess.check_output(['java', '-Xverify:all', '-cp', ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ପ୍ରକୃତ_ଡାଟା.splitlines() == 기대, ପ୍ରକୃତ_ଡାଟା
            ମାପ['class_sha256'] = hashlib.sha256(ଡାଟା).hexdigest()
            ମାପ['openjdk_output'] = ପ୍ରକୃତ_ଡାଟା
        # 실패한 ସଂପାଦନା_ମୂଲ୍ୟ/컴파일은 기존 class를 보존한다.
        ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'Calc.java', 'not Java at all', ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ=False)
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ଅବୈଧ_ମାପ in [
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
            ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'Calc.java', ଅବୈଧ_ମାପ)
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Calc.java', ['javac error:', 'Exit: 1'])
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ବାରମ୍ବାର_ମୂଲ୍ୟ 실행은 ଉପଭୋକ୍ତା 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Calc', ['instruction limit', 'Exit: 1'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'Bad.class', 'garbage')
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Bad', ['JVM error:', 'Exit: 1'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('rm Bad.class', ['Removed'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Bad', ['cannot read class: -2'])
        # ସଂପାଦନା_ମୂଲ୍ୟ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ଚଳାନ୍ତୁ = len(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
        ମେସିନ୍.직렬.sendall(b'edit Hello.java\n')
        ମେସିନ୍.ଅପେକ୍ଷା_ସ୍ଥିତି('...> ', ଚଳାନ୍ତୁ)
        ଚଳାନ୍ତୁ = len(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
        ମେସିନ୍.직렬.sendall(b'x' * 129 + b'\n')
        ମେସିନ୍.ଅପେକ୍ଷା_ସ୍ଥିତି('...> ', ଚଳାନ୍ତୁ)
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('.save', ['Too much input; original preserved'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'f' + str(수), 'occupied')
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
        ମାପ['serial'] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ମାପ
    finally:
        ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()


def 주코드(ଡାଟା):
    """손상 시험용 main Code의 ପ୍ରକୃତ_ଡାଟା ଫାଇଲ 오프셋/길이만 읽는다."""
    ସ୍ଥିତି_ମୂଲ୍ୟ = 8
    def 짧():
        nonlocal ସ୍ଥିତି_ମୂଲ୍ୟ
        ମୂଲ୍ୟ = struct.unpack_from('>H', ଡାଟା, ସ୍ଥିତି_ମୂଲ୍ୟ)[0]
        ସ୍ଥିତି_ମୂଲ୍ୟ += 2
        return ମୂଲ୍ୟ
    def 정():
        nonlocal ସ୍ଥିତି_ମୂଲ୍ୟ
        ମୂଲ୍ୟ = struct.unpack_from('>I', ଡାଟା, ସ୍ଥିତି_ମୂଲ୍ୟ)[0]
        ସ୍ଥିତି_ମୂଲ୍ୟ += 4
        return ମୂଲ୍ୟ
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ଡାଟା[ସ୍ଥିତି_ମୂଲ୍ୟ]
        ସ୍ଥିତି_ମୂଲ୍ୟ += 1
        if 종류 == 1:
            ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = 짧()
            문자들[수] = ଡାଟା[ସ୍ଥିତି_ମୂଲ୍ୟ:ସ୍ଥିତି_ମୂଲ୍ୟ + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ]
            ସ୍ଥିତି_ମୂଲ୍ୟ += ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ
        elif 종류 in (7, 8): ସ୍ଥିତି_ମୂଲ୍ୟ += 2
        elif 종류 in (3, 9, 10, 12): ସ୍ଥିତି_ମୂଲ୍ୟ += 4
        else: raise AssertionError(종류)
    ସ୍ଥିତି_ମୂଲ୍ୟ += 6
    개수 = 짧()
    ସ୍ଥିତି_ମୂଲ୍ୟ += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ନାମ = 짧()
        짧()
        for 수 in range(짧()):
            ଗୁଣ_ମୂଲ୍ୟ = 짧()
            ଆକାର = 정()
            if 문자들[ନାମ] == b'main' and 문자들[ଗୁଣ_ମୂଲ୍ୟ] == b'Code':
                return ସ୍ଥିତି_ମୂଲ୍ୟ + 8, struct.unpack_from('>I', ଡାଟା, ସ୍ଥିତି_ମୂଲ୍ୟ + 4)[0]
            ସ୍ଥିତି_ମୂଲ୍ୟ += ଆକାର
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ = Path(임시)
        (ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'build').mkdir()
        ଉତ୍ସ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'Imported.java'
        ଉତ୍ସ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ଉତ୍ସ)], check=True)
        원본 = (ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'Imported.class').read_bytes()
        코드, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = 주코드(원본)
        변형 = {}
        ଡାଟା = bytearray(원본); ଡାଟା[0] = 0; 변형['BadMagic'] = ଡାଟା
        ଡାଟା = bytearray(원본); ଡାଟା[7] = 61; 변형['BadVer'] = ଡାଟା
        ଡାଟା = bytearray(원본); ଡାଟା[8:10] = b'\xff\xff'; 변형['BadPool'] = ଡାଟା
        ଡାଟା = bytearray(원본); ଡାଟା[코드:코드 + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ] = bytes(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ)
        ଡାଟା[코드:코드 + 3] = b'\xa7\x00\x01'; ଡାଟା[코드 + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ - 1] = 177; 변형['BadJump'] = ଡାଟା
        ଡାଟା = bytearray(원본); ଡାଟା[코드:코드 + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ] = bytes(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ)
        ଡାଟା[코드] = 87; ଡାଟା[코드 + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ - 1] = 177; 변형['BadStack'] = ଡାଟା
        # ନାମ 검사를 통과시켜 ପ୍ରକୃତ_ଡାଟା ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = ['Imported.class=' + str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'Imported.class'), 'Imported.java=' + str(ଉତ୍ସ)]
        for ନାମ, ଡାଟା in 변형.items():
            ପଥ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / (ନାମ + '.class'); ପଥ.write_bytes(ଡାଟା)
            ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.append(ନାମ + '.class=' + str(ପଥ))
        ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(ଅବସ୍ଥାନ / 'ଉପକରଣସମୂହ/자바파일묶기.py'), '-o', str(ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ)] + ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, check=True)
        subprocess.run(['as', '--32', '-o', str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'user.o'), str(ଅବସ୍ଥାନ / '부팅/ଉପଭୋକ୍ତା.s')], cwd=str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ), check=True)
        କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ଅବସ୍ଥାନ / '부팅/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld'), '-o', str(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ),
                        str(ଅବସ୍ଥାନ / 'build/boot.o'), str(ଅବସ୍ଥାନ / 'build/java.o'), str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'user.o'), str(ଅବସ୍ଥାନ / 'build/apps.o')], check=True)
        ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ, ନେଟ୍_ୱାର୍କ୍_ମୂଲ୍ୟ=False)
        try:
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('cat Imported.java', ['int[] values = new int[3]'])
            for ନାମ, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java ' + ନାମ, [문구, 'Exit: 1'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
        finally:
            ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()


if __name__ == '__main__':
    ପାର୍ସ_ମୂଲ୍ୟ = argparse.ArgumentParser()
    ପାର୍ସ_ମୂଲ୍ୟ.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ପାର୍ସ_ମୂଲ୍ୟ.parse_args()
    ମାପ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    ମାପ['import'] = 적재시험()
    (ଅବସ୍ଥାନ / 'build/자바시험.json').write_text(json.dumps(ମାପ, ensure_ascii=False, indent=2) + '\n')
