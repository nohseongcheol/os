#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 اجرا_فرمان, عدم_موفقیت_مقدار/منبع_مقدار 경계 시험."""
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
from 사용자통신시험 import مجازی_دستگاه, مرتب_کردن


def ویرایش_مقدار(دستگاه, نام, محتوا_مقدار, ذخیره_مقدار=True):
    اجرا_2 = len(دستگاه.واقعه_نگار_ردیف)
    دستگاه.직렬.sendall(('edit ' + نام + '\n').encode())
    دستگاه.منتظر_ماندن_وضعیت('...> ', اجرا_2)
    for خط in محتوا_مقدار.splitlines():
        assert len(خط) <= 128
        اجرا_2 = len(دستگاه.واقعه_نگار_ردیف)
        دستگاه.직렬.sendall((خط + '\n').encode())
        دستگاه.منتظر_ماندن_وضعیت('...> ', اجرا_2)
    اجرا_2 = len(دستگاه.واقعه_نگار_ردیف)
    دستگاه.직렬.sendall(b'.save\n' if ذخیره_مقدار else b'.cancel\n')
    سنجش = دستگاه.منتظر_ماندن_وضعیت('jkoros> ', اجرا_2)
    assert ('Saved:' if ذخیره_مقدار else 'Cancelled; original preserved') in سنجش, سنجش


def فایل_آدرس():
    سنجش = subprocess.check_output(['nm', '-n', str(مرتب_کردن / 'build/kernel.elf')], universal_newlines=True)
    for خط in سنجش.splitlines():
        if خط.endswith(' ram_files'):
            return int(خط.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def مهمان_فایل(دستگاه, شکاف_مقدار, اندازه, مسیر):
    # 시험 VM의 메모리에서 واقعی_داده_ها 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    آدرس = فایل_آدرس() + شکاف_مقدار * 16384
    دستگاه.مانیتور_مقدار.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(آدرس, اندازه, مسیر)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if مسیر.exists() and مسیر.stat().st_size == اندازه:
            return مسیر.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    دستگاه = مجازی_دستگاه(مرتب_کردن / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, شبکه_مقدار=False)
    سنجش = {}
    try:
        دستگاه.فرمان('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        دستگاه.فرمان('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        دستگاه.فرمان('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        دستگاه.فرمان('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        دستگاه.فرمان('java Missing', ['cannot read class: -2', 'Exit: 1'])
        دستگاه.فرمان('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        دستگاه.فرمان('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        محتوا_مقدار = '''public class Calc {
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
        ویرایش_مقدار(دستگاه, 'Calc.java', محتوا_مقدار)
        دستگاه.فرمان('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        خروجی = دستگاه.فرمان('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        سنجش['guest_output'] = خروجی
        ورودی_لیست = دستگاه.فرمان('ls', ['Calc.class'])
        اندازه = int(re.search(r'Calc\.class\s+(\d+) bytes', ورودی_لیست).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as فهرست_مقدار_e5561a2b:
            مسیر = Path(فهرست_مقدار_e5561a2b) / 'Calc.class'
            داده_ها = مهمان_فایل(دستگاه, 3, اندازه, مسیر)
            واقعی_داده_ها = subprocess.check_output(['java', '-Xverify:all', '-cp', فهرست_مقدار_e5561a2b, 'Calc', '6', 'guest'], universal_newlines=True)
            assert واقعی_داده_ها.splitlines() == 기대, واقعی_داده_ها
            سنجش['class_sha256'] = hashlib.sha256(داده_ها).hexdigest()
            سنجش['openjdk_output'] = واقعی_داده_ها
        # 실패한 ویرایش_مقدار/컴파일은 기존 class를 보존한다.
        ویرایش_مقدار(دستگاه, 'Calc.java', 'not Java at all', ذخیره_مقدار=False)
        دستگاه.فرمان('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for بی_اعتبار_سنجش in [
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
            ویرایش_مقدار(دستگاه, 'Calc.java', بی_اعتبار_سنجش)
            دستگاه.فرمان('javac Calc.java', ['javac error:', 'Exit: 1'])
            دستگاه.فرمان('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # تکرار_مقدار 실행은 کاربر 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            دستگاه.فرمان('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        دستگاه.فرمان('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        دستگاه.فرمان('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ویرایش_مقدار(دستگاه, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        دستگاه.فرمان('javac Calc.java', ['Compiled:', 'Exit: 0'])
        دستگاه.فرمان('java Calc', ['instruction limit', 'Exit: 1'])
        دستگاه.فرمان('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ویرایش_مقدار(دستگاه, 'Bad.class', 'garbage')
        دستگاه.فرمان('java Bad', ['JVM error:', 'Exit: 1'])
        دستگاه.فرمان('rm Bad.class', ['Removed'])
        دستگاه.فرمان('java Bad', ['cannot read class: -2'])
        # ویرایش_مقدار 입력의 넘친 부분을 잘라서 저장하지 않는다.
        اجرا_2 = len(دستگاه.واقعه_نگار_ردیف)
        دستگاه.직렬.sendall(b'edit Hello.java\n')
        دستگاه.منتظر_ماندن_وضعیت('...> ', اجرا_2)
        اجرا_2 = len(دستگاه.واقعه_نگار_ردیف)
        دستگاه.직렬.sendall(b'x' * 129 + b'\n')
        دستگاه.منتظر_ماندن_وضعیت('...> ', اجرا_2)
        دستگاه.فرمان('.save', ['Too much input; original preserved'])
        دستگاه.فرمان('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ویرایش_مقدار(دستگاه, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ویرایش_مقدار(دستگاه, 'f' + str(수), 'occupied')
        دستگاه.فرمان('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        دستگاه.فرمان('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
        سنجش['serial'] = دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return سنجش
    finally:
        دستگاه.بستن()


def 주코드(داده_ها):
    """손상 시험용 main Code의 واقعی_داده_ها پرونده 오프셋/길이만 읽는다."""
    مرتب_کردن_مقدار = 8
    def 짧():
        nonlocal مرتب_کردن_مقدار
        مقدار = struct.unpack_from('>H', داده_ها, مرتب_کردن_مقدار)[0]
        مرتب_کردن_مقدار += 2
        return مقدار
    def 정():
        nonlocal مرتب_کردن_مقدار
        مقدار = struct.unpack_from('>I', داده_ها, مرتب_کردن_مقدار)[0]
        مرتب_کردن_مقدار += 4
        return مقدار
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = داده_ها[مرتب_کردن_مقدار]
        مرتب_کردن_مقدار += 1
        if 종류 == 1:
            طول_مقدار = 짧()
            문자들[수] = داده_ها[مرتب_کردن_مقدار:مرتب_کردن_مقدار + طول_مقدار]
            مرتب_کردن_مقدار += طول_مقدار
        elif 종류 in (7, 8): مرتب_کردن_مقدار += 2
        elif 종류 in (3, 9, 10, 12): مرتب_کردن_مقدار += 4
        else: raise AssertionError(종류)
    مرتب_کردن_مقدار += 6
    개수 = 짧()
    مرتب_کردن_مقدار += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        نام = 짧()
        짧()
        for 수 in range(짧()):
            مشخصه_مقدار = 짧()
            اندازه = 정()
            if 문자들[نام] == b'main' and 문자들[مشخصه_مقدار] == b'Code':
                return مرتب_کردن_مقدار + 8, struct.unpack_from('>I', داده_ها, مرتب_کردن_مقدار + 4)[0]
            مرتب_کردن_مقدار += اندازه
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        فهرست_مقدار_e5561a2b = Path(임시)
        (فهرست_مقدار_e5561a2b / 'build').mkdir()
        مبداء = فهرست_مقدار_e5561a2b / 'Imported.java'
        مبداء.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(مبداء)], check=True)
        원본 = (فهرست_مقدار_e5561a2b / 'Imported.class').read_bytes()
        کد_مقدار, طول_مقدار = 주코드(원본)
        변형 = {}
        داده_ها = bytearray(원본); داده_ها[0] = 0; 변형['BadMagic'] = داده_ها
        داده_ها = bytearray(원본); داده_ها[7] = 61; 변형['BadVer'] = داده_ها
        داده_ها = bytearray(원본); داده_ها[8:10] = b'\xff\xff'; 변형['BadPool'] = داده_ها
        داده_ها = bytearray(원본); داده_ها[کد_مقدار:کد_مقدار + طول_مقدار] = bytes(طول_مقدار)
        داده_ها[کد_مقدار:کد_مقدار + 3] = b'\xa7\x00\x01'; داده_ها[کد_مقدار + طول_مقدار - 1] = 177; 변형['BadJump'] = داده_ها
        داده_ها = bytearray(원본); داده_ها[کد_مقدار:کد_مقدار + طول_مقدار] = bytes(طول_مقدار)
        داده_ها[کد_مقدار] = 87; داده_ها[کد_مقدار + طول_مقدار - 1] = 177; 변형['BadStack'] = داده_ها
        # نام 검사를 통과시켜 واقعی_داده_ها اجرا_فرمان 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ورودی_مقدار = ['Imported.class=' + str(فهرست_مقدار_e5561a2b / 'Imported.class'), 'Imported.java=' + str(مبداء)]
        for نام, داده_ها in 변형.items():
            مسیر = فهرست_مقدار_e5561a2b / (نام + '.class'); مسیر.write_bytes(داده_ها)
            ورودی_مقدار.append(نام + '.class=' + str(مسیر))
        گروه_مقدار = فهرست_مقدار_e5561a2b / 'build/java-files.bin'
        subprocess.run([sys.executable, str(مرتب_کردن / 'ابزارها/자바파일묶기.py'), '-o', str(گروه_مقدار)] + ورودی_مقدار, check=True)
        subprocess.run(['as', '--32', '-o', str(فهرست_مقدار_e5561a2b / 'user.o'), str(مرتب_کردن / '부팅/کاربر.s')], cwd=str(فهرست_مقدار_e5561a2b), check=True)
        هسته_مقدار = فهرست_مقدار_e5561a2b / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(مرتب_کردن / '부팅/پیوند_پیمایش.ld'), '-o', str(هسته_مقدار),
                        str(مرتب_کردن / 'build/boot.o'), str(مرتب_کردن / 'build/java.o'), str(فهرست_مقدار_e5561a2b / 'user.o'), str(مرتب_کردن / 'build/apps.o')], check=True)
        دستگاه = مجازی_دستگاه(هسته_مقدار, شبکه_مقدار=False)
        try:
            دستگاه.فرمان('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            دستگاه.فرمان('cat Imported.java', ['int[] values = new int[3]'])
            for نام, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                دستگاه.فرمان('java ' + نام, [문구, 'Exit: 1'])
                دستگاه.فرمان('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
        finally:
            دستگاه.بستن()


if __name__ == '__main__':
    تفسیر_مقدار = argparse.ArgumentParser()
    تفسیر_مقدار.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    نشانوندها = تفسیر_مقدار.parse_args()
    سنجش = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if نشانوندها.boot == 'both' else (نشانوندها.boot,))}
    سنجش['import'] = 적재시험()
    (مرتب_کردن / 'build/자바시험.json').write_text(json.dumps(سنجش, ensure_ascii=False, indent=2) + '\n')
