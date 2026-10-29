#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 पाळो_दिवचो_आदेश, अपेस_मोल/साधनसामुग्री_मोल 경계 시험."""
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
from 사용자통신시험 import भ्रामक_यंत्र, स्थिती


def संपादन_करचें_मोल(यंत्र, नांव, अनुक्रमणिका_मोल, Store_मोल=True):
    चलोवप = len(यंत्र.LOG_नोंद)
    यंत्र.직렬.sendall(('edit ' + नांव + '\n').encode())
    यंत्र.기다림('...> ', चलोवप)
    for रेग in अनुक्रमणिका_मोल.splitlines():
        assert len(रेग) <= 128
        चलोवप = len(यंत्र.LOG_नोंद)
        यंत्र.직렬.sendall((रेग + '\n').encode())
        यंत्र.기다림('...> ', चलोवप)
    चलोवप = len(यंत्र.LOG_नोंद)
    यंत्र.직렬.sendall(b'.save\n' if Store_मोल else b'.cancel\n')
    मेजप = यंत्र.기다림('jkoros> ', चलोवप)
    assert ('Saved:' if Store_मोल else 'Cancelled; original preserved') in मेजप, मेजप


def फायल_नामो():
    मेजप = subprocess.check_output(['nm', '-n', str(स्थिती / 'build/kernel.elf')], universal_newlines=True)
    for रेग in मेजप.splitlines():
        if रेग.endswith(' ram_files'):
            return int(रेग.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def सोयरो_फायल(यंत्र, स्लॉट_मोल, आवाठ, पाथ):
    # 시험 VM의 메모리에서 प्रत्यक्ष_डेटा 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    नामो = फायल_नामो() + स्लॉट_मोल * 16384
    यंत्र.मॉनिटर_मोल.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(नामो, आवाठ, पाथ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if पाथ.exists() and पाथ.stat().st_size == आवाठ:
            return पाथ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    यंत्र = भ्रामक_यंत्र(स्थिती / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, नॅटवर्क_मोल=False)
    मेजप = {}
    try:
        यंत्र.आदेश('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        यंत्र.आदेश('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        यंत्र.आदेश('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        यंत्र.आदेश('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        यंत्र.आदेश('java Missing', ['cannot read class: -2', 'Exit: 1'])
        यंत्र.आदेश('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        यंत्र.आदेश('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        अनुक्रमणिका_मोल = '''public class Calc {
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
        संपादन_करचें_मोल(यंत्र, 'Calc.java', अनुक्रमणिका_मोल)
        यंत्र.आदेश('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = यंत्र.आदेश('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        मेजप['guest_output'] = 출력
        प्रवेश_सुची = यंत्र.आदेश('ls', ['Calc.class'])
        आवाठ = int(re.search(r'Calc\.class\s+(\d+) bytes', प्रवेश_सुची).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as नामावळ_मोल:
            पाथ = Path(नामावळ_मोल) / 'Calc.class'
            डेटा = सोयरो_फायल(यंत्र, 3, आवाठ, पाथ)
            प्रत्यक्ष_डेटा = subprocess.check_output(['java', '-Xverify:all', '-cp', नामावळ_मोल, 'Calc', '6', 'guest'], universal_newlines=True)
            assert प्रत्यक्ष_डेटा.splitlines() == 기대, प्रत्यक्ष_डेटा
            मेजप['class_sha256'] = hashlib.sha256(डेटा).hexdigest()
            मेजप['openjdk_output'] = प्रत्यक्ष_डेटा
        # 실패한 संपादन_करचें_मोल/컴파일은 기존 class를 보존한다.
        संपादन_करचें_मोल(यंत्र, 'Calc.java', 'not Java at all', Store_मोल=False)
        यंत्र.आदेश('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for अवैध_मेजप in [
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
            संपादन_करचें_मोल(यंत्र, 'Calc.java', अवैध_मेजप)
            यंत्र.आदेश('javac Calc.java', ['javac error:', 'Exit: 1'])
            यंत्र.आदेश('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # परतवण_मोल 실행은 उपेगकर्तो 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            यंत्र.आदेश('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        यंत्र.आदेश('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        यंत्र.आदेश('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        संपादन_करचें_मोल(यंत्र, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        यंत्र.आदेश('javac Calc.java', ['Compiled:', 'Exit: 0'])
        यंत्र.आदेश('java Calc', ['instruction limit', 'Exit: 1'])
        यंत्र.आदेश('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        संपादन_करचें_मोल(यंत्र, 'Bad.class', 'garbage')
        यंत्र.आदेश('java Bad', ['JVM error:', 'Exit: 1'])
        यंत्र.आदेश('rm Bad.class', ['Removed'])
        यंत्र.आदेश('java Bad', ['cannot read class: -2'])
        # संपादन_करचें_मोल 입력의 넘친 부분을 잘라서 저장하지 않는다.
        चलोवप = len(यंत्र.LOG_नोंद)
        यंत्र.직렬.sendall(b'edit Hello.java\n')
        यंत्र.기다림('...> ', चलोवप)
        चलोवप = len(यंत्र.LOG_नोंद)
        यंत्र.직렬.sendall(b'x' * 129 + b'\n')
        यंत्र.기다림('...> ', चलोवप)
        यंत्र.आदेश('.save', ['Too much input; original preserved'])
        यंत्र.आदेश('javac Hello.java', ['Compiled:', 'Exit: 0'])
        संपादन_करचें_मोल(यंत्र, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            संपादन_करचें_मोल(यंत्र, 'f' + str(수), 'occupied')
        यंत्र.आदेश('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        यंत्र.आदेश('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in यंत्र.LOG_नोंद.decode('utf-8', 'replace')
        मेजप['serial'] = यंत्र.LOG_नोंद.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return मेजप
    finally:
        यंत्र.शेवट()


def 주코드(डेटा):
    """손상 시험용 main Code의 प्रत्यक्ष_डेटा फायल 오프셋/길이만 읽는다."""
    स्थिती_मोल = 8
    def 짧():
        nonlocal स्थिती_मोल
        मोल = struct.unpack_from('>H', डेटा, स्थिती_मोल)[0]
        स्थिती_मोल += 2
        return मोल
    def 정():
        nonlocal स्थिती_मोल
        मोल = struct.unpack_from('>I', डेटा, स्थिती_मोल)[0]
        स्थिती_मोल += 4
        return मोल
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = डेटा[स्थिती_मोल]
        स्थिती_मोल += 1
        if 종류 == 1:
            लांबाय_मोल = 짧()
            문자들[수] = डेटा[स्थिती_मोल:स्थिती_मोल + लांबाय_मोल]
            स्थिती_मोल += लांबाय_मोल
        elif 종류 in (7, 8): स्थिती_मोल += 2
        elif 종류 in (3, 9, 10, 12): स्थिती_मोल += 4
        else: raise AssertionError(종류)
    स्थिती_मोल += 6
    आयटम_COUNT = 짧()
    स्थिती_मोल += आयटम_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        नांव = 짧()
        짧()
        for 수 in range(짧()):
            खाशेलपण_मोल = 짧()
            आवाठ = 정()
            if 문자들[नांव] == b'main' and 문자들[खाशेलपण_मोल] == b'Code':
                return स्थिती_मोल + 8, struct.unpack_from('>I', डेटा, स्थिती_मोल + 4)[0]
            स्थिती_मोल += आवाठ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        नामावळ_मोल = Path(임시)
        (नामावळ_मोल / 'build').mkdir()
        स्त्रोत = नामावळ_मोल / 'Imported.java'
        स्त्रोत.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(स्त्रोत)], check=True)
        원본 = (नामावळ_मोल / 'Imported.class').read_bytes()
        CODE_मोल, लांबाय_मोल = 주코드(원본)
        변형 = {}
        डेटा = bytearray(원본); डेटा[0] = 0; 변형['BadMagic'] = डेटा
        डेटा = bytearray(원본); डेटा[7] = 61; 변형['BadVer'] = डेटा
        डेटा = bytearray(원본); डेटा[8:10] = b'\xff\xff'; 변형['BadPool'] = डेटा
        डेटा = bytearray(원본); डेटा[CODE_मोल:CODE_मोल + लांबाय_मोल] = bytes(लांबाय_मोल)
        डेटा[CODE_मोल:CODE_मोल + 3] = b'\xa7\x00\x01'; डेटा[CODE_मोल + लांबाय_मोल - 1] = 177; 변형['BadJump'] = डेटा
        डेटा = bytearray(원본); डेटा[CODE_मोल:CODE_मोल + लांबाय_मोल] = bytes(लांबाय_मोल)
        डेटा[CODE_मोल] = 87; डेटा[CODE_मोल + लांबाय_मोल - 1] = 177; 변형['BadStack'] = डेटा
        # नांव 검사를 통과시켜 प्रत्यक्ष_डेटा पाळो_दिवचो_आदेश 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        प्रवेश_मोल = ['Imported.class=' + str(नामावळ_मोल / 'Imported.class'), 'Imported.java=' + str(स्त्रोत)]
        for नांव, डेटा in 변형.items():
            पाथ = नामावळ_मोल / (नांव + '.class'); पाथ.write_bytes(डेटा)
            प्रवेश_मोल.append(नांव + '.class=' + str(पाथ))
        गट_मोल = नामावळ_मोल / 'build/java-files.bin'
        subprocess.run([sys.executable, str(स्थिती / 'साधनां/자바파일묶기.py'), '-o', str(गट_मोल)] + प्रवेश_मोल, check=True)
        subprocess.run(['as', '--32', '-o', str(नामावळ_मोल / 'user.o'), str(स्थिती / '부팅/उपेगकर्तो.s')], cwd=str(नामावळ_मोल), check=True)
        कर्नेल_मोल = नामावळ_मोल / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थिती / '부팅/लिंक_रचणाय.ld'), '-o', str(कर्नेल_मोल),
                        str(स्थिती / 'build/boot.o'), str(स्थिती / 'build/java.o'), str(नामावळ_मोल / 'user.o'), str(स्थिती / 'build/apps.o')], check=True)
        यंत्र = भ्रामक_यंत्र(कर्नेल_मोल, नॅटवर्क_मोल=False)
        try:
            यंत्र.आदेश('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            यंत्र.आदेश('cat Imported.java', ['int[] values = new int[3]'])
            for नांव, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                यंत्र.आदेश('java ' + नांव, [문구, 'Exit: 1'])
                यंत्र.आदेश('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return यंत्र.LOG_नोंद.decode('utf-8', 'replace')
        finally:
            यंत्र.शेवट()


if __name__ == '__main__':
    व्याकरणी_फोडणिशी_मोल = argparse.ArgumentParser()
    व्याकरणी_फोडणिशी_मोल.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = व्याकरणी_फोडणिशी_मोल.parse_args()
    मेजप = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    मेजप['import'] = 적재시험()
    (स्थिती / 'build/자바시험.json').write_text(json.dumps(मेजप, ensure_ascii=False, indent=2) + '\n')
