#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ተግብር_ትእዛዝ, ፍሽለት_ዋጋ/ሃብቲ_ዋጋ 경계 시험."""
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
from 사용자통신시험 import መሳሊ_ማሽን, 위치


def ምዕራይ_ዋጋ(ማሽን, ሽም, ትሕዝቶ_ዋጋ, ከዝን_ዋጋ=True):
    ኣኺድ = len(ማሽን.ምዝጉብ_ሪጋ)
    ማሽን.직렬.sendall(('edit ' + ሽም + '\n').encode())
    ማሽን.기다림('...> ', ኣኺድ)
    for መስመር in ትሕዝቶ_ዋጋ.splitlines():
        assert len(መስመር) <= 128
        ኣኺድ = len(ማሽን.ምዝጉብ_ሪጋ)
        ማሽን.직렬.sendall((መስመር + '\n').encode())
        ማሽን.기다림('...> ', ኣኺድ)
    ኣኺድ = len(ማሽን.ምዝጉብ_ሪጋ)
    ማሽን.직렬.sendall(b'.save\n' if ከዝን_ዋጋ else b'.cancel\n')
    결과 = ማሽን.기다림('jkoros> ', ኣኺድ)
    assert ('Saved:' if ከዝን_ዋጋ else 'Cancelled; original preserved') in 결과, 결과


def ፋይል_ኣድራሻ():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for መስመር in 결과.splitlines():
        if መስመር.endswith(' ram_files'):
            return int(መስመር.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(ማሽን, መሰኩዒ_ዋጋ, መጠን, መገዲ):
    # 시험 VM의 메모리에서 ትኽክለኛ_ሓበሬታ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ኣድራሻ = ፋይል_ኣድራሻ() + መሰኩዒ_ዋጋ * 16384
    ማሽን.መርኣዪ_ዋጋ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ኣድራሻ, መጠን, መገዲ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if መገዲ.exists() and መገዲ.stat().st_size == መጠን:
            return መገዲ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ማሽን = መሳሊ_ማሽን(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ማሕበራዊ_ኔትወርክ_ዋጋ=False)
    결과 = {}
    try:
        ማሽን.ትእዛዝ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ማሽን.ትእዛዝ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ማሽን.ትእዛዝ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ማሽን.ትእዛዝ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ማሽን.ትእዛዝ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ማሽን.ትእዛዝ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ማሽን.ትእዛዝ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ትሕዝቶ_ዋጋ = '''public class Calc {
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
        ምዕራይ_ዋጋ(ማሽን, 'Calc.java', ትሕዝቶ_ዋጋ)
        ማሽን.ትእዛዝ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = ማሽን.ትእዛዝ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        ምእታው_ዝርዝር = ማሽን.ትእዛዝ('ls', ['Calc.class'])
        መጠን = int(re.search(r'Calc\.class\s+(\d+) bytes', ምእታው_ዝርዝር).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ሓባሪ_ማህደር_ዋጋ:
            መገዲ = Path(ሓባሪ_ማህደር_ዋጋ) / 'Calc.class'
            ሓበሬታ = 게스트파일(ማሽን, 3, መጠን, መገዲ)
            ትኽክለኛ_ሓበሬታ = subprocess.check_output(['java', '-Xverify:all', '-cp', ሓባሪ_ማህደር_ዋጋ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ትኽክለኛ_ሓበሬታ.splitlines() == 기대, ትኽክለኛ_ሓበሬታ
            결과['class_sha256'] = hashlib.sha256(ሓበሬታ).hexdigest()
            결과['openjdk_output'] = ትኽክለኛ_ሓበሬታ
        # 실패한 ምዕራይ_ዋጋ/컴파일은 기존 class를 보존한다.
        ምዕራይ_ዋጋ(ማሽን, 'Calc.java', 'not Java at all', ከዝን_ዋጋ=False)
        ማሽን.ትእዛዝ('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            ምዕራይ_ዋጋ(ማሽን, 'Calc.java', 잘못)
            ማሽን.ትእዛዝ('javac Calc.java', ['javac error:', 'Exit: 1'])
            ማሽን.ትእዛዝ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ዝርዝር_ዋጋ 실행은 ተጠቃሚ 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ማሽን.ትእዛዝ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ማሽን.ትእዛዝ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ማሽን.ትእዛዝ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ምዕራይ_ዋጋ(ማሽን, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ማሽን.ትእዛዝ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ማሽን.ትእዛዝ('java Calc', ['instruction limit', 'Exit: 1'])
        ማሽን.ትእዛዝ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ምዕራይ_ዋጋ(ማሽን, 'Bad.class', 'garbage')
        ማሽን.ትእዛዝ('java Bad', ['JVM error:', 'Exit: 1'])
        ማሽን.ትእዛዝ('rm Bad.class', ['Removed'])
        ማሽን.ትእዛዝ('java Bad', ['cannot read class: -2'])
        # ምዕራይ_ዋጋ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ኣኺድ = len(ማሽን.ምዝጉብ_ሪጋ)
        ማሽን.직렬.sendall(b'edit Hello.java\n')
        ማሽን.기다림('...> ', ኣኺድ)
        ኣኺድ = len(ማሽን.ምዝጉብ_ሪጋ)
        ማሽን.직렬.sendall(b'x' * 129 + b'\n')
        ማሽን.기다림('...> ', ኣኺድ)
        ማሽን.ትእዛዝ('.save', ['Too much input; original preserved'])
        ማሽን.ትእዛዝ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ምዕራይ_ዋጋ(ማሽን, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ምዕራይ_ዋጋ(ማሽን, 'f' + str(수), 'occupied')
        ማሽን.ትእዛዝ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ማሽን.ትእዛዝ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
        결과['serial'] = ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        ማሽን.ዕጸው()


def 주코드(ሓበሬታ):
    """손상 시험용 main Code의 ትኽክለኛ_ሓበሬታ ፋይል 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        ዋጋ = struct.unpack_from('>H', ሓበሬታ, 위치값)[0]
        위치값 += 2
        return ዋጋ
    def 정():
        nonlocal 위치값
        ዋጋ = struct.unpack_from('>I', ሓበሬታ, 위치값)[0]
        위치값 += 4
        return ዋጋ
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ሓበሬታ[위치값]
        위치값 += 1
        if 종류 == 1:
            ንውሓት_ዋጋ = 짧()
            문자들[수] = ሓበሬታ[위치값:위치값 + ንውሓት_ዋጋ]
            위치값 += ንውሓት_ዋጋ
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ሽም = 짧()
        짧()
        for 수 in range(짧()):
            ባህሪ_ዋጋ = 짧()
            መጠን = 정()
            if 문자들[ሽም] == b'main' and 문자들[ባህሪ_ዋጋ] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', ሓበሬታ, 위치값 + 4)[0]
            위치값 += መጠን
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ሓባሪ_ማህደር_ዋጋ = Path(임시)
        (ሓባሪ_ማህደር_ዋጋ / 'build').mkdir()
        ምንጪ = ሓባሪ_ማህደር_ዋጋ / 'Imported.java'
        ምንጪ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ምንጪ)], check=True)
        원본 = (ሓባሪ_ማህደር_ዋጋ / 'Imported.class').read_bytes()
        코드, ንውሓት_ዋጋ = 주코드(원본)
        변형 = {}
        ሓበሬታ = bytearray(원본); ሓበሬታ[0] = 0; 변형['BadMagic'] = ሓበሬታ
        ሓበሬታ = bytearray(원본); ሓበሬታ[7] = 61; 변형['BadVer'] = ሓበሬታ
        ሓበሬታ = bytearray(원본); ሓበሬታ[8:10] = b'\xff\xff'; 변형['BadPool'] = ሓበሬታ
        ሓበሬታ = bytearray(원본); ሓበሬታ[코드:코드 + ንውሓት_ዋጋ] = bytes(ንውሓት_ዋጋ)
        ሓበሬታ[코드:코드 + 3] = b'\xa7\x00\x01'; ሓበሬታ[코드 + ንውሓት_ዋጋ - 1] = 177; 변형['BadJump'] = ሓበሬታ
        ሓበሬታ = bytearray(원본); ሓበሬታ[코드:코드 + ንውሓት_ዋጋ] = bytes(ንውሓት_ዋጋ)
        ሓበሬታ[코드] = 87; ሓበሬታ[코드 + ንውሓት_ዋጋ - 1] = 177; 변형['BadStack'] = ሓበሬታ
        # ሽም 검사를 통과시켜 ትኽክለኛ_ሓበሬታ ተግብር_ትእዛዝ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ምእታው_ዋጋ = ['Imported.class=' + str(ሓባሪ_ማህደር_ዋጋ / 'Imported.class'), 'Imported.java=' + str(ምንጪ)]
        for ሽም, ሓበሬታ in 변형.items():
            መገዲ = ሓባሪ_ማህደር_ዋጋ / (ሽም + '.class'); መገዲ.write_bytes(ሓበሬታ)
            ምእታው_ዋጋ.append(ሽም + '.class=' + str(መገዲ))
        ጉጅለ_ዋጋ = ሓባሪ_ማህደር_ዋጋ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'መሳርሒታት/자바파일묶기.py'), '-o', str(ጉጅለ_ዋጋ)] + ምእታው_ዋጋ, check=True)
        subprocess.run(['as', '--32', '-o', str(ሓባሪ_ማህደር_ዋጋ / 'user.o'), str(위치 / '부팅/ተጠቃሚ.s')], cwd=str(ሓባሪ_ማህደር_ዋጋ), check=True)
        ፍረ_ዋጋ = ሓባሪ_ማህደር_ዋጋ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/መጋጠሚ_ኣቀማምጣ.ld'), '-o', str(ፍረ_ዋጋ),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(ሓባሪ_ማህደር_ዋጋ / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        ማሽን = መሳሊ_ማሽን(ፍረ_ዋጋ, ማሕበራዊ_ኔትወርክ_ዋጋ=False)
        try:
            ማሽን.ትእዛዝ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ማሽን.ትእዛዝ('cat Imported.java', ['int[] values = new int[3]'])
            for ሽም, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ማሽን.ትእዛዝ('java ' + ሽም, [문구, 'Exit: 1'])
                ማሽን.ትእዛዝ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
        finally:
            ማሽን.ዕጸው()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = 해석.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
