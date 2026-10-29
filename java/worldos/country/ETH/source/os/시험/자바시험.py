#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ፈጽም_ትእዛዝ, ተስኖት_እሴት/ሃብት_እሴት 경계 시험."""
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
from 사용자통신시험 import ምናባዊ_ማሽን, አካባቢ


def አርትዕ_እሴት(ማሽን, ስም, ይዘት_እሴት, ማከማቻ_እሴት=True):
    ማስኬጃ = len(ማሽን.መዝግብ_ረድፍ)
    ማሽን.직렬.sendall(('edit ' + ስም + '\n').encode())
    ማሽን.መጠበቅ_ዞን('...> ', ማስኬጃ)
    for መስመር in ይዘት_እሴት.splitlines():
        assert len(መስመር) <= 128
        ማስኬጃ = len(ማሽን.መዝግብ_ረድፍ)
        ማሽን.직렬.sendall((መስመር + '\n').encode())
        ማሽን.መጠበቅ_ዞን('...> ', ማስኬጃ)
    ማስኬጃ = len(ማሽን.መዝግብ_ረድፍ)
    ማሽን.직렬.sendall(b'.save\n' if ማከማቻ_እሴት else b'.cancel\n')
    ልኬት = ማሽን.መጠበቅ_ዞን('jkoros> ', ማስኬጃ)
    assert ('Saved:' if ማከማቻ_እሴት else 'Cancelled; original preserved') in ልኬት, ልኬት


def ፋይል_አድራሻ():
    ልኬት = subprocess.check_output(['nm', '-n', str(አካባቢ / 'build/kernel.elf')], universal_newlines=True)
    for መስመር in ልኬት.splitlines():
        if መስመር.endswith(' ram_files'):
            return int(መስመር.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def እንግዳ_ፋይል(ማሽን, ማስገቢያ_ቀዳዳ_እሴት, መጠን, መተላለፊያ):
    # 시험 VM의 메모리에서 ትክክለኛ_ውሂብ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    አድራሻ = ፋይል_አድራሻ() + ማስገቢያ_ቀዳዳ_እሴት * 16384
    ማሽን.ማሳያ_እሴት.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(አድራሻ, መጠን, መተላለፊያ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if መተላለፊያ.exists() and መተላለፊያ.stat().st_size == መጠን:
            return መተላለፊያ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ማሽን = ምናባዊ_ማሽን(አካባቢ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, መረብ_እሴት=False)
    ልኬት = {}
    try:
        ማሽን.ትእዛዝ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ማሽን.ትእዛዝ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ማሽን.ትእዛዝ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ማሽን.ትእዛዝ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ማሽን.ትእዛዝ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ማሽን.ትእዛዝ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ማሽን.ትእዛዝ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ይዘት_እሴት = '''public class Calc {
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
        አርትዕ_እሴት(ማሽን, 'Calc.java', ይዘት_እሴት)
        ማሽን.ትእዛዝ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        ውጤት = ማሽን.ትእዛዝ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ልኬት['guest_output'] = ውጤት
        ምዝግብ_ዝርዝር = ማሽን.ትእዛዝ('ls', ['Calc.class'])
        መጠን = int(re.search(r'Calc\.class\s+(\d+) bytes', ምዝግብ_ዝርዝር).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ማውጫ_እሴት:
            መተላለፊያ = Path(ማውጫ_እሴት) / 'Calc.class'
            ውሂብ = እንግዳ_ፋይል(ማሽን, 3, መጠን, መተላለፊያ)
            ትክክለኛ_ውሂብ = subprocess.check_output(['java', '-Xverify:all', '-cp', ማውጫ_እሴት, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ትክክለኛ_ውሂብ.splitlines() == 기대, ትክክለኛ_ውሂብ
            ልኬት['class_sha256'] = hashlib.sha256(ውሂብ).hexdigest()
            ልኬት['openjdk_output'] = ትክክለኛ_ውሂብ
        # 실패한 አርትዕ_እሴት/컴파일은 기존 class를 보존한다.
        አርትዕ_እሴት(ማሽን, 'Calc.java', 'not Java at all', ማከማቻ_እሴት=False)
        ማሽን.ትእዛዝ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ልክ_ያልኾነ_ልኬት in [
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
            አርትዕ_እሴት(ማሽን, 'Calc.java', ልክ_ያልኾነ_ልኬት)
            ማሽን.ትእዛዝ('javac Calc.java', ['javac error:', 'Exit: 1'])
            ማሽን.ትእዛዝ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ሽምጥ_እሴት 실행은 ተጠቃሚ 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ማሽን.ትእዛዝ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ማሽን.ትእዛዝ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ማሽን.ትእዛዝ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        አርትዕ_እሴት(ማሽን, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ማሽን.ትእዛዝ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ማሽን.ትእዛዝ('java Calc', ['instruction limit', 'Exit: 1'])
        ማሽን.ትእዛዝ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        አርትዕ_እሴት(ማሽን, 'Bad.class', 'garbage')
        ማሽን.ትእዛዝ('java Bad', ['JVM error:', 'Exit: 1'])
        ማሽን.ትእዛዝ('rm Bad.class', ['Removed'])
        ማሽን.ትእዛዝ('java Bad', ['cannot read class: -2'])
        # አርትዕ_እሴት 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ማስኬጃ = len(ማሽን.መዝግብ_ረድፍ)
        ማሽን.직렬.sendall(b'edit Hello.java\n')
        ማሽን.መጠበቅ_ዞን('...> ', ማስኬጃ)
        ማስኬጃ = len(ማሽን.መዝግብ_ረድፍ)
        ማሽን.직렬.sendall(b'x' * 129 + b'\n')
        ማሽን.መጠበቅ_ዞን('...> ', ማስኬጃ)
        ማሽን.ትእዛዝ('.save', ['Too much input; original preserved'])
        ማሽን.ትእዛዝ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        አርትዕ_እሴት(ማሽን, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            አርትዕ_እሴት(ማሽን, 'f' + str(수), 'occupied')
        ማሽን.ትእዛዝ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ማሽን.ትእዛዝ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
        ልኬት['serial'] = ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ልኬት
    finally:
        ማሽን.መዝጊያ()


def 주코드(ውሂብ):
    """손상 시험용 main Code의 ትክክለኛ_ውሂብ ፋይል 오프셋/길이만 읽는다."""
    በቦታ_አስቀመጠ_እሴት = 8
    def 짧():
        nonlocal በቦታ_አስቀመጠ_እሴት
        እሴት = struct.unpack_from('>H', ውሂብ, በቦታ_አስቀመጠ_እሴት)[0]
        በቦታ_አስቀመጠ_እሴት += 2
        return እሴት
    def 정():
        nonlocal በቦታ_አስቀመጠ_እሴት
        እሴት = struct.unpack_from('>I', ውሂብ, በቦታ_አስቀመጠ_እሴት)[0]
        በቦታ_አስቀመጠ_እሴት += 4
        return እሴት
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ውሂብ[በቦታ_አስቀመጠ_እሴት]
        በቦታ_አስቀመጠ_እሴት += 1
        if 종류 == 1:
            ርዝመት_እሴት = 짧()
            문자들[수] = ውሂብ[በቦታ_አስቀመጠ_እሴት:በቦታ_አስቀመጠ_እሴት + ርዝመት_እሴት]
            በቦታ_አስቀመጠ_እሴት += ርዝመት_እሴት
        elif 종류 in (7, 8): በቦታ_አስቀመጠ_እሴት += 2
        elif 종류 in (3, 9, 10, 12): በቦታ_አስቀመጠ_እሴት += 4
        else: raise AssertionError(종류)
    በቦታ_አስቀመጠ_እሴት += 6
    개수 = 짧()
    በቦታ_አስቀመጠ_እሴት += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ስም = 짧()
        짧()
        for 수 in range(짧()):
            ዓይነታ_እሴት = 짧()
            መጠን = 정()
            if 문자들[ስም] == b'main' and 문자들[ዓይነታ_እሴት] == b'Code':
                return በቦታ_አስቀመጠ_እሴት + 8, struct.unpack_from('>I', ውሂብ, በቦታ_አስቀመጠ_እሴት + 4)[0]
            በቦታ_አስቀመጠ_እሴት += መጠን
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ማውጫ_እሴት = Path(임시)
        (ማውጫ_እሴት / 'build').mkdir()
        ምንጭ = ማውጫ_እሴት / 'Imported.java'
        ምንጭ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ምንጭ)], check=True)
        원본 = (ማውጫ_እሴት / 'Imported.class').read_bytes()
        코드, ርዝመት_እሴት = 주코드(원본)
        변형 = {}
        ውሂብ = bytearray(원본); ውሂብ[0] = 0; 변형['BadMagic'] = ውሂብ
        ውሂብ = bytearray(원본); ውሂብ[7] = 61; 변형['BadVer'] = ውሂብ
        ውሂብ = bytearray(원본); ውሂብ[8:10] = b'\xff\xff'; 변형['BadPool'] = ውሂብ
        ውሂብ = bytearray(원본); ውሂብ[코드:코드 + ርዝመት_እሴት] = bytes(ርዝመት_እሴት)
        ውሂብ[코드:코드 + 3] = b'\xa7\x00\x01'; ውሂብ[코드 + ርዝመት_እሴት - 1] = 177; 변형['BadJump'] = ውሂብ
        ውሂብ = bytearray(원본); ውሂብ[코드:코드 + ርዝመት_እሴት] = bytes(ርዝመት_እሴት)
        ውሂብ[코드] = 87; ውሂብ[코드 + ርዝመት_እሴት - 1] = 177; 변형['BadStack'] = ውሂብ
        # ስም 검사를 통과시켜 ትክክለኛ_ውሂብ ፈጽም_ትእዛዝ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ምዝግብ_እሴት = ['Imported.class=' + str(ማውጫ_እሴት / 'Imported.class'), 'Imported.java=' + str(ምንጭ)]
        for ስም, ውሂብ in 변형.items():
            መተላለፊያ = ማውጫ_እሴት / (ስም + '.class'); መተላለፊያ.write_bytes(ውሂብ)
            ምዝግብ_እሴት.append(ስም + '.class=' + str(መተላለፊያ))
        ቡድን_እሴት = ማውጫ_እሴት / 'build/java-files.bin'
        subprocess.run([sys.executable, str(አካባቢ / 'መሳሪያዎች/자바파일묶기.py'), '-o', str(ቡድን_እሴት)] + ምዝግብ_እሴት, check=True)
        subprocess.run(['as', '--32', '-o', str(ማውጫ_እሴት / 'user.o'), str(አካባቢ / '부팅/ተጠቃሚ.s')], cwd=str(ማውጫ_እሴት), check=True)
        ዓንኳር_እሴት = ማውጫ_እሴት / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(አካባቢ / '부팅/አገናኝ_አሰሳ.ld'), '-o', str(ዓንኳር_እሴት),
                        str(አካባቢ / 'build/boot.o'), str(አካባቢ / 'build/java.o'), str(ማውጫ_እሴት / 'user.o'), str(አካባቢ / 'build/apps.o')], check=True)
        ማሽን = ምናባዊ_ማሽን(ዓንኳር_እሴት, መረብ_እሴት=False)
        try:
            ማሽን.ትእዛዝ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ማሽን.ትእዛዝ('cat Imported.java', ['int[] values = new int[3]'])
            for ስም, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ማሽን.ትእዛዝ('java ' + ስም, [문구, 'Exit: 1'])
                ማሽን.ትእዛዝ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
        finally:
            ማሽን.መዝጊያ()


if __name__ == '__main__':
    ተንትን_እሴት = argparse.ArgumentParser()
    ተንትን_እሴት.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ተንትን_እሴት.parse_args()
    ልኬት = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    ልኬት['import'] = 적재시험()
    (አካባቢ / 'build/자바시험.json').write_text(json.dumps(ልኬት, ensure_ascii=False, indent=2) + '\n')
