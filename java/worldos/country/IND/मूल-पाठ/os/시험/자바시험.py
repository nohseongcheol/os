#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 निष्पादित_करें_आदेश, विफलता_मान/संसाधन_मान 경계 시험."""
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
from 사용자통신시험 import वर्चुअल_मशीन, स्थान


def संपादन_मान(यंत्र, नाम, सामग्री_मान, स्टोर_मान=True):
    चलाएँ = len(यंत्र.लॉग_रिकॉर्ड)
    यंत्र.직렬.sendall(('edit ' + नाम + '\n').encode())
    यंत्र.प्रतीक्षा_स्थिति('...> ', चलाएँ)
    for पंक्ति in सामग्री_मान.splitlines():
        assert len(पंक्ति) <= 128
        चलाएँ = len(यंत्र.लॉग_रिकॉर्ड)
        यंत्र.직렬.sendall((पंक्ति + '\n').encode())
        यंत्र.प्रतीक्षा_स्थिति('...> ', चलाएँ)
    चलाएँ = len(यंत्र.लॉग_रिकॉर्ड)
    यंत्र.직렬.sendall(b'.save\n' if स्टोर_मान else b'.cancel\n')
    परिणाम = यंत्र.प्रतीक्षा_स्थिति('jkoros> ', चलाएँ)
    assert ('Saved:' if स्टोर_मान else 'Cancelled; original preserved') in परिणाम, परिणाम


def फ़ाइल_पता():
    परिणाम = subprocess.check_output(['nm', '-n', str(स्थान / 'build/kernel.elf')], universal_newlines=True)
    for पंक्ति in परिणाम.splitlines():
        if पंक्ति.endswith(' ram_files'):
            return int(पंक्ति.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def अतिथि_फ़ाइल(यंत्र, 슬롯, आकार, पथ):
    # 시험 VM의 메모리에서 वास्तविक_डेटा 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    पता = फ़ाइल_पता() + 슬롯 * 16384
    यंत्र.मॉनीटर_मान.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(पता, आकार, पथ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if पथ.exists() and पथ.stat().st_size == आकार:
            return पथ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def जाँच_मार्ग(종류):
    यंत्र = वर्चुअल_मशीन(स्थान / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, नेटवर्क_मान=False)
    परिणाम = {}
    try:
        यंत्र.आदेश('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        यंत्र.आदेश('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        यंत्र.आदेश('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        यंत्र.आदेश('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        यंत्र.आदेश('java Missing', ['cannot read class: -2', 'Exit: 1'])
        यंत्र.आदेश('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        यंत्र.आदेश('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
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
        संपादन_मान(यंत्र, 'Calc.java', सामग्री_मान)
        यंत्र.आदेश('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        निर्गम = यंत्र.आदेश('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        परिणाम['guest_output'] = निर्गम
        एन्ट्री_सूची = यंत्र.आदेश('ls', ['Calc.class'])
        आकार = int(re.search(r'Calc\.class\s+(\d+) bytes', एन्ट्री_सूची).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as डायरेक्टरी_मान:
            पथ = Path(डायरेक्टरी_मान) / 'Calc.class'
            आँकड़े = अतिथि_फ़ाइल(यंत्र, 3, आकार, पथ)
            वास्तविक_डेटा = subprocess.check_output(['java', '-Xverify:all', '-cp', डायरेक्टरी_मान, 'Calc', '6', 'guest'], universal_newlines=True)
            assert वास्तविक_डेटा.splitlines() == 기대, वास्तविक_डेटा
            परिणाम['class_sha256'] = hashlib.sha256(आँकड़े).hexdigest()
            परिणाम['openjdk_output'] = वास्तविक_डेटा
        # 실패한 संपादन_मान/컴파일은 기존 class를 보존한다.
        संपादन_मान(यंत्र, 'Calc.java', 'not Java at all', स्टोर_मान=False)
        यंत्र.आदेश('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for अमान्य_परिणाम in [
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
            संपादन_मान(यंत्र, 'Calc.java', अमान्य_परिणाम)
            यंत्र.आदेश('javac Calc.java', ['javac error:', 'Exit: 1'])
            यंत्र.आदेश('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # पुनरावृति_मान 실행은 उपयोगकर्ता ढ़ेर_मान/프레임을 매번 초기화한다.
        for 수 in range(12):
            यंत्र.आदेश('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        यंत्र.आदेश('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        यंत्र.आदेश('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        संपादन_मान(यंत्र, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        यंत्र.आदेश('javac Calc.java', ['Compiled:', 'Exit: 0'])
        यंत्र.आदेश('java Calc', ['instruction limit', 'Exit: 1'])
        यंत्र.आदेश('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        संपादन_मान(यंत्र, 'Bad.class', 'garbage')
        यंत्र.आदेश('java Bad', ['JVM error:', 'Exit: 1'])
        यंत्र.आदेश('rm Bad.class', ['Removed'])
        यंत्र.आदेश('java Bad', ['cannot read class: -2'])
        # संपादन_मान 입력의 넘친 부분을 잘라서 저장하지 않는다.
        चलाएँ = len(यंत्र.लॉग_रिकॉर्ड)
        यंत्र.직렬.sendall(b'edit Hello.java\n')
        यंत्र.प्रतीक्षा_स्थिति('...> ', चलाएँ)
        चलाएँ = len(यंत्र.लॉग_रिकॉर्ड)
        यंत्र.직렬.sendall(b'x' * 129 + b'\n')
        यंत्र.प्रतीक्षा_स्थिति('...> ', चलाएँ)
        यंत्र.आदेश('.save', ['Too much input; original preserved'])
        यंत्र.आदेश('javac Hello.java', ['Compiled:', 'Exit: 0'])
        संपादन_मान(यंत्र, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            संपादन_मान(यंत्र, 'f' + str(수), 'occupied')
        यंत्र.आदेश('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        यंत्र.आदेश('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
        परिणाम['serial'] = यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return परिणाम
    finally:
        यंत्र.बंदकरें()


def 주코드(आँकड़े):
    """손상 시험용 main Code의 वास्तविक_डेटा संचिका 오프셋/길이만 읽는다."""
    पद_मान = 8
    def 짧():
        nonlocal पद_मान
        मान = struct.unpack_from('>H', आँकड़े, पद_मान)[0]
        पद_मान += 2
        return मान
    def पढें_अचिह्नांकित_पूर्णांक():
        nonlocal पद_मान
        मान = struct.unpack_from('>I', आँकड़े, पद_मान)[0]
        पद_मान += 4
        return मान
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = आँकड़े[पद_मान]
        पद_मान += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[수] = आँकड़े[पद_मान:पद_मान + 길이]
            पद_मान += 길이
        elif 종류 in (7, 8): पद_मान += 2
        elif 종류 in (3, 9, 10, 12): पद_मान += 4
        else: raise AssertionError(종류)
    पद_मान += 6
    개수 = 짧()
    पद_मान += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        नाम = 짧()
        짧()
        for 수 in range(짧()):
            विशेषता_मान = 짧()
            आकार = पढें_अचिह्नांकित_पूर्णांक()
            if 문자들[नाम] == b'main' and 문자들[विशेषता_मान] == b'Code':
                return पद_मान + 8, struct.unpack_from('>I', आँकड़े, पद_मान + 4)[0]
            पद_मान += आकार
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        डायरेक्टरी_मान = Path(임시)
        (डायरेक्टरी_मान / 'build').mkdir()
        स्रोत = डायरेक्टरी_मान / 'Imported.java'
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
        원본 = (डायरेक्टरी_मान / 'Imported.class').read_bytes()
        कोड_मान, 길이 = 주코드(원본)
        변형 = {}
        आँकड़े = bytearray(원본); आँकड़े[0] = 0; 변형['BadMagic'] = आँकड़े
        आँकड़े = bytearray(원본); आँकड़े[7] = 61; 변형['BadVer'] = आँकड़े
        आँकड़े = bytearray(원본); आँकड़े[8:10] = b'\xff\xff'; 변형['BadPool'] = आँकड़े
        आँकड़े = bytearray(원본); आँकड़े[कोड_मान:कोड_मान + 길이] = bytes(길이)
        आँकड़े[कोड_मान:कोड_मान + 3] = b'\xa7\x00\x01'; आँकड़े[कोड_मान + 길이 - 1] = 177; 변형['BadJump'] = आँकड़े
        आँकड़े = bytearray(원본); आँकड़े[कोड_मान:कोड_मान + 길이] = bytes(길이)
        आँकड़े[कोड_मान] = 87; आँकड़े[कोड_मान + 길이 - 1] = 177; 변형['BadStack'] = आँकड़े
        # नाम 검사를 통과시켜 वास्तविक_डेटा निष्पादित_करें_आदेश 중의 ऑपरेंड_स्टैक 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        एन्ट्री_मान = ['Imported.class=' + str(डायरेक्टरी_मान / 'Imported.class'), 'Imported.java=' + str(स्रोत)]
        for नाम, आँकड़े in 변형.items():
            पथ = डायरेक्टरी_मान / (नाम + '.class'); पथ.write_bytes(आँकड़े)
            एन्ट्री_मान.append(नाम + '.class=' + str(पथ))
        समूह_मान = डायरेक्टरी_मान / 'build/java-files.bin'
        subprocess.run([sys.executable, str(स्थान / 'उपकरण/자바파일묶기.py'), '-o', str(समूह_मान)] + एन्ट्री_मान, check=True)
        subprocess.run(['as', '--32', '-o', str(डायरेक्टरी_मान / 'user.o'), str(स्थान / '부팅/उपयोगकर्ता.s')], cwd=str(डायरेक्टरी_मान), check=True)
        कर्नेल_मान = डायरेक्टरी_मान / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थान / '부팅/लिंक_लेआउट.ld'), '-o', str(कर्नेल_मान),
                        str(स्थान / 'build/boot.o'), str(स्थान / 'build/java.o'), str(डायरेक्टरी_मान / 'user.o'), str(स्थान / 'build/apps.o')], check=True)
        यंत्र = वर्चुअल_मशीन(कर्नेल_मान, नेटवर्क_मान=False)
        try:
            यंत्र.आदेश('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            यंत्र.आदेश('cat Imported.java', ['int[] values = new int[3]'])
            for नाम, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                यंत्र.आदेश('java ' + नाम, [문구, 'Exit: 1'])
                यंत्र.आदेश('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
        finally:
            यंत्र.बंदकरें()


if __name__ == '__main__':
    पार्स_करें_मान = argparse.ArgumentParser()
    पार्स_करें_मान.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    तर्क = पार्स_करें_मान.parse_args()
    परिणाम = {종류: जाँच_मार्ग(종류) for 종류 in (('elf', 'iso') if तर्क.boot == 'both' else (तर्क.boot,))}
    परिणाम['import'] = 적재시험()
    (स्थान / 'build/자바시험.json').write_text(json.dumps(परिणाम, ensure_ascii=False, indent=2) + '\n')
