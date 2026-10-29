#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 இயக்கு_கட்டளை, செயலிழப்பு_மதிப்பு/வளம்_மதிப்பு 경계 시험."""
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
from 사용자통신시험 import தோற்றநிலை_இயந்திரம், இடம்


def திருத்து_மதிப்பு(இயந்திரம், பெயர், உள்ளடக்கம்_மதிப்பு, சேகரி_மதிப்பு=True):
    செயல்படுத்துக = len(இயந்திரம்.பதிவு_பதிவு)
    இயந்திரம்.직렬.sendall(('edit ' + பெயர் + '\n').encode())
    இயந்திரம்.காத்திரு_நிலை('...> ', செயல்படுத்துக)
    for உள்ளீட்டு_வரி in உள்ளடக்கம்_மதிப்பு.splitlines():
        assert len(உள்ளீட்டு_வரி) <= 128
        செயல்படுத்துக = len(இயந்திரம்.பதிவு_பதிவு)
        இயந்திரம்.직렬.sendall((உள்ளீட்டு_வரி + '\n').encode())
        இயந்திரம்.காத்திரு_நிலை('...> ', செயல்படுத்துக)
    செயல்படுத்துக = len(இயந்திரம்.பதிவு_பதிவு)
    இயந்திரம்.직렬.sendall(b'.save\n' if சேகரி_மதிப்பு else b'.cancel\n')
    அளவிடக்கூடியது = இயந்திரம்.காத்திரு_நிலை('jkoros> ', செயல்படுத்துக)
    assert ('Saved:' if சேகரி_மதிப்பு else 'Cancelled; original preserved') in அளவிடக்கூடியது, அளவிடக்கூடியது


def கோப்பு_முகவரி():
    அளவிடக்கூடியது = subprocess.check_output(['nm', '-n', str(இடம் / 'build/kernel.elf')], universal_newlines=True)
    for உள்ளீட்டு_வரி in அளவிடக்கூடியது.splitlines():
        if உள்ளீட்டு_வரி.endswith(' ram_files'):
            return int(உள்ளீட்டு_வரி.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def விருந்தினர்_கோப்பு(இயந்திரம், ஸ்லாட்_மதிப்பு, அளவு, பாதை_2):
    # 시험 VM의 메모리에서 அசல்_தரவு 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    முகவரி = கோப்பு_முகவரி() + ஸ்லாட்_மதிப்பு * 16384
    இயந்திரம்.திரையகம்_மதிப்பு.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(முகவரி, அளவு, பாதை_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if பாதை_2.exists() and பாதை_2.stat().st_size == அளவு:
            return பாதை_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def சோதனை_இயக்கம்(종류):
    இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, பிணையம்_மதிப்பு=False)
    அளவிடக்கூடியது = {}
    try:
        இயந்திரம்.கட்டளை('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        இயந்திரம்.கட்டளை('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        இயந்திரம்.கட்டளை('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        இயந்திரம்.கட்டளை('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        இயந்திரம்.கட்டளை('java Missing', ['cannot read class: -2', 'Exit: 1'])
        இயந்திரம்.கட்டளை('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        இயந்திரம்.கட்டளை('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        உள்ளடக்கம்_மதிப்பு = '''public class Calc {
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
        திருத்து_மதிப்பு(இயந்திரம், 'Calc.java', உள்ளடக்கம்_மதிப்பு)
        இயந்திரம்.கட்டளை('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        வெளியீட்டு_இடம் = இயந்திரம்.கட்டளை('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        அளவிடக்கூடியது['guest_output'] = வெளியீட்டு_இடம்
        உள்ளீடு_பட்டியல் = இயந்திரம்.கட்டளை('ls', ['Calc.class'])
        அளவு = int(re.search(r'Calc\.class\s+(\d+) bytes', உள்ளீடு_பட்டியல்).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as கோப்பகம்_மதிப்பு:
            பாதை_2 = Path(கோப்பகம்_மதிப்பு) / 'Calc.class'
            தரவு = விருந்தினர்_கோப்பு(இயந்திரம், 3, அளவு, பாதை_2)
            அசல்_தரவு = subprocess.check_output(['java', '-Xverify:all', '-cp', கோப்பகம்_மதிப்பு, 'Calc', '6', 'guest'], universal_newlines=True)
            assert அசல்_தரவு.splitlines() == 기대, அசல்_தரவு
            அளவிடக்கூடியது['class_sha256'] = hashlib.sha256(தரவு).hexdigest()
            அளவிடக்கூடியது['openjdk_output'] = அசல்_தரவு
        # 실패한 திருத்து_மதிப்பு/컴파일은 기존 class를 보존한다.
        திருத்து_மதிப்பு(இயந்திரம், 'Calc.java', 'not Java at all', சேகரி_மதிப்பு=False)
        இயந்திரம்.கட்டளை('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for செல்லுபடியாகாத_அளவிடக்கூடியது in [
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
            திருத்து_மதிப்பு(இயந்திரம், 'Calc.java', செல்லுபடியாகாத_அளவிடக்கூடியது)
            இயந்திரம்.கட்டளை('javac Calc.java', ['javac error:', 'Exit: 1'])
            இயந்திரம்.கட்டளை('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # மீள்செயல்_மதிப்பு 실행은 பயனர் குவியல்_மதிப்பு/프레임을 매번 초기화한다.
        for 수 in range(12):
            இயந்திரம்.கட்டளை('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        இயந்திரம்.கட்டளை('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        இயந்திரம்.கட்டளை('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        திருத்து_மதிப்பு(இயந்திரம், 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        இயந்திரம்.கட்டளை('javac Calc.java', ['Compiled:', 'Exit: 0'])
        இயந்திரம்.கட்டளை('java Calc', ['instruction limit', 'Exit: 1'])
        இயந்திரம்.கட்டளை('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        திருத்து_மதிப்பு(இயந்திரம், 'Bad.class', 'garbage')
        இயந்திரம்.கட்டளை('java Bad', ['JVM error:', 'Exit: 1'])
        இயந்திரம்.கட்டளை('rm Bad.class', ['Removed'])
        இயந்திரம்.கட்டளை('java Bad', ['cannot read class: -2'])
        # திருத்து_மதிப்பு 입력의 넘친 부분을 잘라서 저장하지 않는다.
        செயல்படுத்துக = len(இயந்திரம்.பதிவு_பதிவு)
        இயந்திரம்.직렬.sendall(b'edit Hello.java\n')
        இயந்திரம்.காத்திரு_நிலை('...> ', செயல்படுத்துக)
        செயல்படுத்துக = len(இயந்திரம்.பதிவு_பதிவு)
        இயந்திரம்.직렬.sendall(b'x' * 129 + b'\n')
        இயந்திரம்.காத்திரு_நிலை('...> ', செயல்படுத்துக)
        இயந்திரம்.கட்டளை('.save', ['Too much input; original preserved'])
        இயந்திரம்.கட்டளை('javac Hello.java', ['Compiled:', 'Exit: 0'])
        திருத்து_மதிப்பு(இயந்திரம், 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            திருத்து_மதிப்பு(இயந்திரம், 'f' + str(수), 'occupied')
        இயந்திரம்.கட்டளை('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        இயந்திரம்.கட்டளை('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
        அளவிடக்கூடியது['serial'] = இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return அளவிடக்கூடியது
    finally:
        இயந்திரம்.மூடு()


def 주코드(தரவு):
    """손상 시험용 main Code의 அசல்_தரவு கோப்பின்_பெயர் 오프셋/길이만 읽는다."""
    நிலை_மதிப்பு = 8
    def 짧():
        nonlocal நிலை_மதிப்பு
        மதிப்பு = struct.unpack_from('>H', தரவு, நிலை_மதிப்பு)[0]
        நிலை_மதிப்பு += 2
        return மதிப்பு
    def 정():
        nonlocal நிலை_மதிப்பு
        மதிப்பு = struct.unpack_from('>I', தரவு, நிலை_மதிப்பு)[0]
        நிலை_மதிப்பு += 4
        return மதிப்பு
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = தரவு[நிலை_மதிப்பு]
        நிலை_மதிப்பு += 1
        if 종류 == 1:
            நீளம்_மதிப்பு = 짧()
            문자들[수] = தரவு[நிலை_மதிப்பு:நிலை_மதிப்பு + நீளம்_மதிப்பு]
            நிலை_மதிப்பு += நீளம்_மதிப்பு
        elif 종류 in (7, 8): நிலை_மதிப்பு += 2
        elif 종류 in (3, 9, 10, 12): நிலை_மதிப்பு += 4
        else: raise AssertionError(종류)
    நிலை_மதிப்பு += 6
    개수 = 짧()
    நிலை_மதிப்பு += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        பெயர் = 짧()
        짧()
        for 수 in range(짧()):
            பண்புக்கூறு_மதிப்பு = 짧()
            அளவு = 정()
            if 문자들[பெயர்] == b'main' and 문자들[பண்புக்கூறு_மதிப்பு] == b'Code':
                return நிலை_மதிப்பு + 8, struct.unpack_from('>I', தரவு, நிலை_மதிப்பு + 4)[0]
            நிலை_மதிப்பு += அளவு
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        கோப்பகம்_மதிப்பு = Path(임시)
        (கோப்பகம்_மதிப்பு / 'build').mkdir()
        மூலக்_கோப்பு = கோப்பகம்_மதிப்பு / 'Imported.java'
        மூலக்_கோப்பு.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(மூலக்_கோப்பு)], check=True)
        원본 = (கோப்பகம்_மதிப்பு / 'Imported.class').read_bytes()
        குறியீடு_மதிப்பு, நீளம்_மதிப்பு = 주코드(원본)
        변형 = {}
        தரவு = bytearray(원본); தரவு[0] = 0; 변형['BadMagic'] = தரவு
        தரவு = bytearray(원본); தரவு[7] = 61; 변형['BadVer'] = தரவு
        தரவு = bytearray(원본); தரவு[8:10] = b'\xff\xff'; 변형['BadPool'] = தரவு
        தரவு = bytearray(원본); தரவு[குறியீடு_மதிப்பு:குறியீடு_மதிப்பு + நீளம்_மதிப்பு] = bytes(நீளம்_மதிப்பு)
        தரவு[குறியீடு_மதிப்பு:குறியீடு_மதிப்பு + 3] = b'\xa7\x00\x01'; தரவு[குறியீடு_மதிப்பு + நீளம்_மதிப்பு - 1] = 177; 변형['BadJump'] = தரவு
        தரவு = bytearray(원본); தரவு[குறியீடு_மதிப்பு:குறியீடு_மதிப்பு + நீளம்_மதிப்பு] = bytes(நீளம்_மதிப்பு)
        தரவு[குறியீடு_மதிப்பு] = 87; தரவு[குறியீடு_மதிப்பு + நீளம்_மதிப்பு - 1] = 177; 변형['BadStack'] = தரவு
        # பெயர் 검사를 통과시켜 அசல்_தரவு இயக்கு_கட்டளை 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        உள்ளீடு_மதிப்பு = ['Imported.class=' + str(கோப்பகம்_மதிப்பு / 'Imported.class'), 'Imported.java=' + str(மூலக்_கோப்பு)]
        for பெயர், தரவு in 변형.items():
            பாதை_2 = கோப்பகம்_மதிப்பு / (பெயர் + '.class'); பாதை_2.write_bytes(தரவு)
            உள்ளீடு_மதிப்பு.append(பெயர் + '.class=' + str(பாதை_2))
        குழு_மதிப்பு = கோப்பகம்_மதிப்பு / 'build/java-files.bin'
        subprocess.run([sys.executable, str(இடம் / 'கருவிகள்/자바파일묶기.py'), '-o', str(குழு_மதிப்பு)] + உள்ளீடு_மதிப்பு, check=True)
        subprocess.run(['as', '--32', '-o', str(கோப்பகம்_மதிப்பு / 'user.o'), str(இடம் / '부팅/பயனர்.s')], cwd=str(கோப்பகம்_மதிப்பு), check=True)
        கரு_மதிப்பு = கோப்பகம்_மதிப்பு / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(இடம் / '부팅/இணை_லேஅவுட்.ld'), '-o', str(கரு_மதிப்பு),
                        str(இடம் / 'build/boot.o'), str(இடம் / 'build/java.o'), str(கோப்பகம்_மதிப்பு / 'user.o'), str(இடம் / 'build/apps.o')], check=True)
        இயந்திரம் = தோற்றநிலை_இயந்திரம்(கரு_மதிப்பு, பிணையம்_மதிப்பு=False)
        try:
            இயந்திரம்.கட்டளை('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            இயந்திரம்.கட்டளை('cat Imported.java', ['int[] values = new int[3]'])
            for பெயர், 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                இயந்திரம்.கட்டளை('java ' + பெயர், [문구, 'Exit: 1'])
                இயந்திரம்.கட்டளை('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
        finally:
            இயந்திரம்.மூடு()


if __name__ == '__main__':
    அலகிடு_மதிப்பு = argparse.ArgumentParser()
    அலகிடு_மதிப்பு.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    செயலுருபுகள் = அலகிடு_மதிப்பு.parse_args()
    அளவிடக்கூடியது = {종류: சோதனை_இயக்கம்(종류) for 종류 in (('elf', 'iso') if செயலுருபுகள்.boot == 'both' else (செயலுருபுகள்.boot,))}
    அளவிடக்கூடியது['import'] = 적재시험()
    (இடம் / 'build/자바시험.json').write_text(json.dumps(அளவிடக்கூடியது, ensure_ascii=False, indent=2) + '\n')
