#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 कार्यान्वयन_गर्नुहोस्_आदेश, विफल_मान/स्रोत_मान 경계 시험."""
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
from 사용자통신시험 import अवास्तविक_मेशिन, स्थिति


def सम्पादन_गर्नुहोस्_मान(मेशिन, नाम, सामग्री_मान, भण्डार_गर्नुहोस्_मान=True):
    चलाउनुहोस् = len(मेशिन.लग_रेकर्ड)
    मेशिन.직렬.sendall(('edit ' + नाम + '\n').encode())
    मेशिन.기다림('...> ', चलाउनुहोस्)
    for रेखा in सामग्री_मान.splitlines():
        assert len(रेखा) <= 128
        चलाउनुहोस् = len(मेशिन.लग_रेकर्ड)
        मेशिन.직렬.sendall((रेखा + '\n').encode())
        मेशिन.기다림('...> ', चलाउनुहोस्)
    चलाउनुहोस् = len(मेशिन.लग_रेकर्ड)
    मेशिन.직렬.sendall(b'.save\n' if भण्डार_गर्नुहोस्_मान else b'.cancel\n')
    मापन = मेशिन.기다림('jkoros> ', चलाउनुहोस्)
    assert ('Saved:' if भण्डार_गर्नुहोस्_मान else 'Cancelled; original preserved') in मापन, मापन


def फाइल_ठेगाना():
    मापन = subprocess.check_output(['nm', '-n', str(स्थिति / 'build/kernel.elf')], universal_newlines=True)
    for रेखा in मापन.splitlines():
        if रेखा.endswith(' ram_files'):
            return int(रेखा.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def अतिथि_फाइल(मेशिन, स्लट_मान, आकार, मार्ग):
    # 시험 VM의 메모리에서 वास्तविक_लगत 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ठेगाना = फाइल_ठेगाना() + स्लट_मान * 16384
    मेशिन.मनिटर_मान.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ठेगाना, आकार, मार्ग)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if मार्ग.exists() and मार्ग.stat().st_size == आकार:
            return मार्ग.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    मेशिन = अवास्तविक_मेशिन(स्थिति / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, सञ्जाल_मान=False)
    मापन = {}
    try:
        मेशिन.आदेश('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        मेशिन.आदेश('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        मेशिन.आदेश('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        मेशिन.आदेश('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        मेशिन.आदेश('java Missing', ['cannot read class: -2', 'Exit: 1'])
        मेशिन.आदेश('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        मेशिन.आदेश('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        सामग्री_मान = '''public class Calc {
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
        सम्पादन_गर्नुहोस्_मान(मेशिन, 'Calc.java', सामग्री_मान)
        मेशिन.आदेश('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = मेशिन.आदेश('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        मापन['guest_output'] = 출력
        प्रविष्टि_सूची = मेशिन.आदेश('ls', ['Calc.class'])
        आकार = int(re.search(r'Calc\.class\s+(\d+) bytes', प्रविष्टि_सूची).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as डाइरेक्टरी_मान:
            मार्ग = Path(डाइरेक्टरी_मान) / 'Calc.class'
            लगत = अतिथि_फाइल(मेशिन, 3, आकार, मार्ग)
            वास्तविक_लगत = subprocess.check_output(['java', '-Xverify:all', '-cp', डाइरेक्टरी_मान, 'Calc', '6', 'guest'], universal_newlines=True)
            assert वास्तविक_लगत.splitlines() == 기대, वास्तविक_लगत
            मापन['class_sha256'] = hashlib.sha256(लगत).hexdigest()
            मापन['openjdk_output'] = वास्तविक_लगत
        # 실패한 सम्पादन_गर्नुहोस्_मान/컴파일은 기존 class를 보존한다.
        सम्पादन_गर्नुहोस्_मान(मेशिन, 'Calc.java', 'not Java at all', भण्डार_गर्नुहोस्_मान=False)
        मेशिन.आदेश('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for अवैधानिक_मापन in [
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
            सम्पादन_गर्नुहोस्_मान(मेशिन, 'Calc.java', अवैधानिक_मापन)
            मेशिन.आदेश('javac Calc.java', ['javac error:', 'Exit: 1'])
            मेशिन.आदेश('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # दोहर्_याउनु_मान 실행은 प्रयोगकर्ता 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            मेशिन.आदेश('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        मेशिन.आदेश('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        मेशिन.आदेश('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        सम्पादन_गर्नुहोस्_मान(मेशिन, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        मेशिन.आदेश('javac Calc.java', ['Compiled:', 'Exit: 0'])
        मेशिन.आदेश('java Calc', ['instruction limit', 'Exit: 1'])
        मेशिन.आदेश('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        सम्पादन_गर्नुहोस्_मान(मेशिन, 'Bad.class', 'garbage')
        मेशिन.आदेश('java Bad', ['JVM error:', 'Exit: 1'])
        मेशिन.आदेश('rm Bad.class', ['Removed'])
        मेशिन.आदेश('java Bad', ['cannot read class: -2'])
        # सम्पादन_गर्नुहोस्_मान 입력의 넘친 부분을 잘라서 저장하지 않는다.
        चलाउनुहोस् = len(मेशिन.लग_रेकर्ड)
        मेशिन.직렬.sendall(b'edit Hello.java\n')
        मेशिन.기다림('...> ', चलाउनुहोस्)
        चलाउनुहोस् = len(मेशिन.लग_रेकर्ड)
        मेशिन.직렬.sendall(b'x' * 129 + b'\n')
        मेशिन.기다림('...> ', चलाउनुहोस्)
        मेशिन.आदेश('.save', ['Too much input; original preserved'])
        मेशिन.आदेश('javac Hello.java', ['Compiled:', 'Exit: 0'])
        सम्पादन_गर्नुहोस्_मान(मेशिन, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            सम्पादन_गर्नुहोस्_मान(मेशिन, 'f' + str(수), 'occupied')
        मेशिन.आदेश('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        मेशिन.आदेश('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
        मापन['serial'] = मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return मापन
    finally:
        मेशिन.बन्दगर्नुहोस्()


def 주코드(लगत):
    """손상 시험용 main Code의 वास्तविक_लगत फाइल 오프셋/길이만 읽는다."""
    राख्नुहोस्_मान = 8
    def 짧():
        nonlocal राख्नुहोस्_मान
        मान = struct.unpack_from('>H', लगत, राख्नुहोस्_मान)[0]
        राख्नुहोस्_मान += 2
        return मान
    def 정():
        nonlocal राख्नुहोस्_मान
        मान = struct.unpack_from('>I', लगत, राख्नुहोस्_मान)[0]
        राख्नुहोस्_मान += 4
        return मान
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = लगत[राख्नुहोस्_मान]
        राख्नुहोस्_मान += 1
        if 종류 == 1:
            लम्बाइ_मान = 짧()
            문자들[수] = लगत[राख्नुहोस्_मान:राख्नुहोस्_मान + लम्बाइ_मान]
            राख्नुहोस्_मान += लम्बाइ_मान
        elif 종류 in (7, 8): राख्नुहोस्_मान += 2
        elif 종류 in (3, 9, 10, 12): राख्नुहोस्_मान += 4
        else: raise AssertionError(종류)
    राख्नुहोस्_मान += 6
    개수 = 짧()
    राख्नुहोस्_मान += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        नाम = 짧()
        짧()
        for 수 in range(짧()):
            विशेषण_मान = 짧()
            आकार = 정()
            if 문자들[नाम] == b'main' and 문자들[विशेषण_मान] == b'Code':
                return राख्नुहोस्_मान + 8, struct.unpack_from('>I', लगत, राख्नुहोस्_मान + 4)[0]
            राख्नुहोस्_मान += आकार
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        डाइरेक्टरी_मान = Path(임시)
        (डाइरेक्टरी_मान / 'build').mkdir()
        स्रोत = डाइरेक्टरी_मान / 'Imported.java'
        स्रोत.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(स्रोत)], check=True)
        원본 = (डाइरेक्टरी_मान / 'Imported.class').read_bytes()
        코드, लम्बाइ_मान = 주코드(원본)
        변형 = {}
        लगत = bytearray(원본); लगत[0] = 0; 변형['BadMagic'] = लगत
        लगत = bytearray(원본); लगत[7] = 61; 변형['BadVer'] = लगत
        लगत = bytearray(원본); लगत[8:10] = b'\xff\xff'; 변형['BadPool'] = लगत
        लगत = bytearray(원본); लगत[코드:코드 + लम्बाइ_मान] = bytes(लम्बाइ_मान)
        लगत[코드:코드 + 3] = b'\xa7\x00\x01'; लगत[코드 + लम्बाइ_मान - 1] = 177; 변형['BadJump'] = लगत
        लगत = bytearray(원본); लगत[코드:코드 + लम्बाइ_मान] = bytes(लम्बाइ_मान)
        लगत[코드] = 87; लगत[코드 + लम्बाइ_मान - 1] = 177; 변형['BadStack'] = लगत
        # नाम 검사를 통과시켜 वास्तविक_लगत कार्यान्वयन_गर्नुहोस्_आदेश 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        प्रविष्टि_मान = ['Imported.class=' + str(डाइरेक्टरी_मान / 'Imported.class'), 'Imported.java=' + str(स्रोत)]
        for नाम, लगत in 변형.items():
            मार्ग = डाइरेक्टरी_मान / (नाम + '.class'); मार्ग.write_bytes(लगत)
            प्रविष्टि_मान.append(नाम + '.class=' + str(मार्ग))
        समूह_मान = डाइरेक्टरी_मान / 'build/java-files.bin'
        subprocess.run([sys.executable, str(स्थिति / 'उपकरणहरू/자바파일묶기.py'), '-o', str(समूह_मान)] + प्रविष्टि_मान, check=True)
        subprocess.run(['as', '--32', '-o', str(डाइरेक्टरी_मान / 'user.o'), str(स्थिति / '부팅/प्रयोगकर्ता.s')], cwd=str(डाइरेक्टरी_मान), check=True)
        कर्णेल_मान = डाइरेक्टरी_मान / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थिति / '부팅/लिङ्क_लेआउट.ld'), '-o', str(कर्णेल_मान),
                        str(स्थिति / 'build/boot.o'), str(स्थिति / 'build/java.o'), str(डाइरेक्टरी_मान / 'user.o'), str(स्थिति / 'build/apps.o')], check=True)
        मेशिन = अवास्तविक_मेशिन(कर्णेल_मान, सञ्जाल_मान=False)
        try:
            मेशिन.आदेश('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            मेशिन.आदेश('cat Imported.java', ['int[] values = new int[3]'])
            for नाम, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                मेशिन.आदेश('java ' + नाम, [문구, 'Exit: 1'])
                मेशिन.आदेश('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
        finally:
            मेशिन.बन्दगर्नुहोस्()


if __name__ == '__main__':
    पदच्छेद_गर्नुहोस्_मान = argparse.ArgumentParser()
    पदच्छेद_गर्नुहोस्_मान.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    तर्क = पदच्छेद_गर्नुहोस्_मान.parse_args()
    मापन = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if तर्क.boot == 'both' else (तर्क.boot,))}
    मापन['import'] = 적재시험()
    (स्थिति / 'build/자바시험.json').write_text(json.dumps(मापन, ensure_ascii=False, indent=2) + '\n')
