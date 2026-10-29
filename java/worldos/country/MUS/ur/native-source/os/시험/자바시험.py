#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 نفاذ_کریں_حکم, ناکامی_قدر/ذریعہ_قدر 경계 시험."""
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
from 사용자통신시험 import مجازی_مشین, مقام


def تدوین_قدر(مشین, نام, مشمول_قدر, ذخیرہ_کریں_قدر=True):
    چلائیں = len(مشین.لاگ_صف)
    مشین.직렬.sendall(('edit ' + نام + '\n').encode())
    مشین.انتظار_حالت('...> ', چلائیں)
    for اندراج_کی_سطر in مشمول_قدر.splitlines():
        assert len(اندراج_کی_سطر) <= 128
        چلائیں = len(مشین.لاگ_صف)
        مشین.직렬.sendall((اندراج_کی_سطر + '\n').encode())
        مشین.انتظار_حالت('...> ', چلائیں)
    چلائیں = len(مشین.لاگ_صف)
    مشین.직렬.sendall(b'.save\n' if ذخیرہ_کریں_قدر else b'.cancel\n')
    پیمائش = مشین.انتظار_حالت('jkoros> ', چلائیں)
    assert ('Saved:' if ذخیرہ_کریں_قدر else 'Cancelled; original preserved') in پیمائش, پیمائش


def فائل_پتہ():
    پیمائش = subprocess.check_output(['nm', '-n', str(مقام / 'build/kernel.elf')], universal_newlines=True)
    for اندراج_کی_سطر in پیمائش.splitlines():
        if اندراج_کی_سطر.endswith(' ram_files'):
            return int(اندراج_کی_سطر.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def مہمان_فائل(مشین, سلاٹ_قدر, حجم, راستہ_2):
    # 시험 VM의 메모리에서 اصل_کوائف 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    پتہ = فائل_پتہ() + سلاٹ_قدر * 16384
    مشین.مانیٹر_قدر.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(پتہ, حجم, راستہ_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if راستہ_2.exists() and راستہ_2.stat().st_size == حجم:
            return راستہ_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    مشین = مجازی_مشین(مقام / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, نیٹ_ورک_قدر=False)
    پیمائش = {}
    try:
        مشین.حکم('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        مشین.حکم('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        مشین.حکم('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        مشین.حکم('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        مشین.حکم('java Missing', ['cannot read class: -2', 'Exit: 1'])
        مشین.حکم('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        مشین.حکم('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        مشمول_قدر = '''public class Calc {
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
        تدوین_قدر(مشین, 'Calc.java', مشمول_قدر)
        مشین.حکم('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        اخراج_کا_مقام = مشین.حکم('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        پیمائش['guest_output'] = اخراج_کا_مقام
        اندراج_فہرست = مشین.حکم('ls', ['Calc.class'])
        حجم = int(re.search(r'Calc\.class\s+(\d+) bytes', اندراج_فہرست).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ڈائریکٹری_قدر:
            راستہ_2 = Path(ڈائریکٹری_قدر) / 'Calc.class'
            کوائف = مہمان_فائل(مشین, 3, حجم, راستہ_2)
            اصل_کوائف = subprocess.check_output(['java', '-Xverify:all', '-cp', ڈائریکٹری_قدر, 'Calc', '6', 'guest'], universal_newlines=True)
            assert اصل_کوائف.splitlines() == 기대, اصل_کوائف
            پیمائش['class_sha256'] = hashlib.sha256(کوائف).hexdigest()
            پیمائش['openjdk_output'] = اصل_کوائف
        # 실패한 تدوین_قدر/컴파일은 기존 class를 보존한다.
        تدوین_قدر(مشین, 'Calc.java', 'not Java at all', ذخیرہ_کریں_قدر=False)
        مشین.حکم('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for بے_جواز_پیمائش in [
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
            تدوین_قدر(مشین, 'Calc.java', بے_جواز_پیمائش)
            مشین.حکم('javac Calc.java', ['javac error:', 'Exit: 1'])
            مشین.حکم('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # تکرار_قدر 실행은 صارف 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            مشین.حکم('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        مشین.حکم('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        مشین.حکم('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        تدوین_قدر(مشین, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        مشین.حکم('javac Calc.java', ['Compiled:', 'Exit: 0'])
        مشین.حکم('java Calc', ['instruction limit', 'Exit: 1'])
        مشین.حکم('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        تدوین_قدر(مشین, 'Bad.class', 'garbage')
        مشین.حکم('java Bad', ['JVM error:', 'Exit: 1'])
        مشین.حکم('rm Bad.class', ['Removed'])
        مشین.حکم('java Bad', ['cannot read class: -2'])
        # تدوین_قدر 입력의 넘친 부분을 잘라서 저장하지 않는다.
        چلائیں = len(مشین.لاگ_صف)
        مشین.직렬.sendall(b'edit Hello.java\n')
        مشین.انتظار_حالت('...> ', چلائیں)
        چلائیں = len(مشین.لاگ_صف)
        مشین.직렬.sendall(b'x' * 129 + b'\n')
        مشین.انتظار_حالت('...> ', چلائیں)
        مشین.حکم('.save', ['Too much input; original preserved'])
        مشین.حکم('javac Hello.java', ['Compiled:', 'Exit: 0'])
        تدوین_قدر(مشین, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            تدوین_قدر(مشین, 'f' + str(수), 'occupied')
        مشین.حکم('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        مشین.حکم('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in مشین.لاگ_صف.decode('utf-8', 'replace')
        پیمائش['serial'] = مشین.لاگ_صف.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return پیمائش
    finally:
        مشین.بند_کریں()


def 주코드(کوائف):
    """손상 시험용 main Code의 اصل_کوائف فائل_کا_نام 오프셋/길이만 읽는다."""
    پوزیشن_ٹھیک_کریں_قدر = 8
    def 짧():
        nonlocal پوزیشن_ٹھیک_کریں_قدر
        قدر = struct.unpack_from('>H', کوائف, پوزیشن_ٹھیک_کریں_قدر)[0]
        پوزیشن_ٹھیک_کریں_قدر += 2
        return قدر
    def 정():
        nonlocal پوزیشن_ٹھیک_کریں_قدر
        قدر = struct.unpack_from('>I', کوائف, پوزیشن_ٹھیک_کریں_قدر)[0]
        پوزیشن_ٹھیک_کریں_قدر += 4
        return قدر
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = کوائف[پوزیشن_ٹھیک_کریں_قدر]
        پوزیشن_ٹھیک_کریں_قدر += 1
        if 종류 == 1:
            لمبا_ئی_قدر = 짧()
            문자들[수] = کوائف[پوزیشن_ٹھیک_کریں_قدر:پوزیشن_ٹھیک_کریں_قدر + لمبا_ئی_قدر]
            پوزیشن_ٹھیک_کریں_قدر += لمبا_ئی_قدر
        elif 종류 in (7, 8): پوزیشن_ٹھیک_کریں_قدر += 2
        elif 종류 in (3, 9, 10, 12): پوزیشن_ٹھیک_کریں_قدر += 4
        else: raise AssertionError(종류)
    پوزیشن_ٹھیک_کریں_قدر += 6
    개수 = 짧()
    پوزیشن_ٹھیک_کریں_قدر += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        نام = 짧()
        짧()
        for 수 in range(짧()):
            وصف_قدر = 짧()
            حجم = 정()
            if 문자들[نام] == b'main' and 문자들[وصف_قدر] == b'Code':
                return پوزیشن_ٹھیک_کریں_قدر + 8, struct.unpack_from('>I', کوائف, پوزیشن_ٹھیک_کریں_قدر + 4)[0]
            پوزیشن_ٹھیک_کریں_قدر += حجم
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ڈائریکٹری_قدر = Path(임시)
        (ڈائریکٹری_قدر / 'build').mkdir()
        ماخذ_فائل = ڈائریکٹری_قدر / 'Imported.java'
        ماخذ_فائل.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ماخذ_فائل)], check=True)
        원본 = (ڈائریکٹری_قدر / 'Imported.class').read_bytes()
        코드, لمبا_ئی_قدر = 주코드(원본)
        변형 = {}
        کوائف = bytearray(원본); کوائف[0] = 0; 변형['BadMagic'] = کوائف
        کوائف = bytearray(원본); کوائف[7] = 61; 변형['BadVer'] = کوائف
        کوائف = bytearray(원본); کوائف[8:10] = b'\xff\xff'; 변형['BadPool'] = کوائف
        کوائف = bytearray(원본); کوائف[코드:코드 + لمبا_ئی_قدر] = bytes(لمبا_ئی_قدر)
        کوائف[코드:코드 + 3] = b'\xa7\x00\x01'; کوائف[코드 + لمبا_ئی_قدر - 1] = 177; 변형['BadJump'] = کوائف
        کوائف = bytearray(원본); کوائف[코드:코드 + لمبا_ئی_قدر] = bytes(لمبا_ئی_قدر)
        کوائف[코드] = 87; کوائف[코드 + لمبا_ئی_قدر - 1] = 177; 변형['BadStack'] = کوائف
        # نام 검사를 통과시켜 اصل_کوائف نفاذ_کریں_حکم 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        اندراج_قدر = ['Imported.class=' + str(ڈائریکٹری_قدر / 'Imported.class'), 'Imported.java=' + str(ماخذ_فائل)]
        for نام, کوائف in 변형.items():
            راستہ_2 = ڈائریکٹری_قدر / (نام + '.class'); راستہ_2.write_bytes(کوائف)
            اندراج_قدر.append(نام + '.class=' + str(راستہ_2))
        گروپ_قدر = ڈائریکٹری_قدر / 'build/java-files.bin'
        subprocess.run([sys.executable, str(مقام / 'ٹولز/자바파일묶기.py'), '-o', str(گروپ_قدر)] + اندراج_قدر, check=True)
        subprocess.run(['as', '--32', '-o', str(ڈائریکٹری_قدر / 'user.o'), str(مقام / '부팅/صارف.s')], cwd=str(ڈائریکٹری_قدر), check=True)
        کرنیل_قدر = ڈائریکٹری_قدر / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(مقام / '부팅/ربط_ترتیب.ld'), '-o', str(کرنیل_قدر),
                        str(مقام / 'build/boot.o'), str(مقام / 'build/java.o'), str(ڈائریکٹری_قدر / 'user.o'), str(مقام / 'build/apps.o')], check=True)
        مشین = مجازی_مشین(کرنیل_قدر, نیٹ_ورک_قدر=False)
        try:
            مشین.حکم('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            مشین.حکم('cat Imported.java', ['int[] values = new int[3]'])
            for نام, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                مشین.حکم('java ' + نام, [문구, 'Exit: 1'])
                مشین.حکم('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return مشین.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشین.بند_کریں()


if __name__ == '__main__':
    پارس_قدر = argparse.ArgumentParser()
    پارس_قدر.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    دلائل = پارس_قدر.parse_args()
    پیمائش = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if دلائل.boot == 'both' else (دلائل.boot,))}
    پیمائش['import'] = 적재시험()
    (مقام / 'build/자바시험.json').write_text(json.dumps(پیمائش, ensure_ascii=False, indent=2) + '\n')
