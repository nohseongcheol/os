#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ينفذ_أمر, فشل_قيمة/مصدر_قيمة 경계 اختبارات."""
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
from يختبر_مستخدم_شبكة import جهاز_ظاهري, موضع


def يحرر_قيمة(جهاز, اسم, محتوى_قيمة, مخزن_قيمة=True):
    تشغيل = len(جهاز.سجل_سجل)
    جهاز.직렬.sendall(('edit ' + اسم + '\n').encode())
    جهاز.حالة_انتظار('...> ', تشغيل)
    for سطر in محتوى_قيمة.splitlines():
        assert len(سطر) <= 128
        تشغيل = len(جهاز.سجل_سجل)
        جهاز.직렬.sendall((سطر + '\n').encode())
        جهاز.حالة_انتظار('...> ', تشغيل)
    تشغيل = len(جهاز.سجل_سجل)
    جهاز.직렬.sendall(b'.save\n' if مخزن_قيمة else b'.cancel\n')
    نتيجة = جهاز.حالة_انتظار('jkoros> ', تشغيل)
    assert ('Saved:' if مخزن_قيمة else 'Cancelled; original preserved') in نتيجة, نتيجة


def ملف_عنوان():
    نتيجة = subprocess.check_output(['nm', '-n', str(موضع / 'build/kernel.elf')], universal_newlines=True)
    for سطر in نتيجة.splitlines():
        if سطر.endswith(' ram_files'):
            return int(سطر.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ضيف_ملف(جهاز, فتحة_قيمة, حجم, مسار):
    # اختبارات VM의 메모리에서 الفعلي_بيانات 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    عنوان = ملف_عنوان() + فتحة_قيمة * 16384
    جهاز.يراقب_قيمة.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(عنوان, حجم, مسار)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if مسار.exists() and مسار.stat().st_size == حجم:
            return مسار.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def مجموعة_الاختبارات(종류):
    جهاز = جهاز_ظاهري(موضع / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, شبكة_قيمة=False)
    نتيجة = {}
    try:
        جهاز.أمر('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        جهاز.أمر('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        جهاز.أمر('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        جهاز.أمر('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        جهاز.أمر('java Missing', ['cannot read class: -2', 'Exit: 1'])
        جهاز.أمر('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        جهاز.أمر('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        محتوى_قيمة = '''public class Calc {
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
        يحرر_قيمة(جهاز, 'Calc.java', محتوى_قيمة)
        جهاز.أمر('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        مخرجات = جهاز.أمر('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        نتيجة['guest_output'] = مخرجات
        إدخال_قائمة_f07b3200 = جهاز.أمر('ls', ['Calc.class'])
        حجم = int(re.search(r'Calc\.class\s+(\d+) bytes', إدخال_قائمة_f07b3200).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as دليل_قيمة:
            مسار = Path(دليل_قيمة) / 'Calc.class'
            بيانات = ضيف_ملف(جهاز, 3, حجم, مسار)
            الفعلي_بيانات = subprocess.check_output(['java', '-Xverify:all', '-cp', دليل_قيمة, 'Calc', '6', 'guest'], universal_newlines=True)
            assert الفعلي_بيانات.splitlines() == 기대, الفعلي_بيانات
            نتيجة['class_sha256'] = hashlib.sha256(بيانات).hexdigest()
            نتيجة['openjdk_output'] = الفعلي_بيانات
        # 실패한 يحرر_قيمة/컴파일은 기존 class를 보존한다.
        يحرر_قيمة(جهاز, 'Calc.java', 'not Java at all', مخزن_قيمة=False)
        جهاز.أمر('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for غير_صالح_مقياس in [
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
            يحرر_قيمة(جهاز, 'Calc.java', غير_صالح_مقياس)
            جهاز.أمر('javac Calc.java', ['javac error:', 'Exit: 1'])
            جهاز.أمر('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # تكرار_قيمة 실행은 فضاء_المستخدم كومة_ذاكرة_مؤقتة_قيمة/프레임을 매번 초기화한다.
        for رقم in range(12):
            جهاز.أمر('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        جهاز.أمر('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        جهاز.أمر('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        يحرر_قيمة(جهاز, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        جهاز.أمر('javac Calc.java', ['Compiled:', 'Exit: 0'])
        جهاز.أمر('java Calc', ['instruction limit', 'Exit: 1'])
        جهاز.أمر('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        يحرر_قيمة(جهاز, 'Bad.class', 'garbage')
        جهاز.أمر('java Bad', ['JVM error:', 'Exit: 1'])
        جهاز.أمر('rm Bad.class', ['Removed'])
        جهاز.أمر('java Bad', ['cannot read class: -2'])
        # يحرر_قيمة 입력의 넘친 부분을 잘라서 저장하지 않는다.
        تشغيل = len(جهاز.سجل_سجل)
        جهاز.직렬.sendall(b'edit Hello.java\n')
        جهاز.حالة_انتظار('...> ', تشغيل)
        تشغيل = len(جهاز.سجل_سجل)
        جهاز.직렬.sendall(b'x' * 129 + b'\n')
        جهاز.حالة_انتظار('...> ', تشغيل)
        جهاز.أمر('.save', ['Too much input; original preserved'])
        جهاز.أمر('javac Hello.java', ['Compiled:', 'Exit: 0'])
        يحرر_قيمة(جهاز, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for رقم in range(3):
            يحرر_قيمة(جهاز, 'f' + str(رقم), 'occupied')
        جهاز.أمر('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        جهاز.أمر('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in جهاز.سجل_سجل.decode('utf-8', 'replace')
        نتيجة['serial'] = جهاز.سجل_سجل.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return نتيجة
    finally:
        جهاز.إغلاق()


def 주코드(بيانات):
    """손상 시험용 main Code의 الفعلي_بيانات ملف 오프셋/길이만 읽는다."""
    منصب_قيمة = 8
    def 짧():
        nonlocal منصب_قيمة
        قيمة = struct.unpack_from('>H', بيانات, منصب_قيمة)[0]
        منصب_قيمة += 2
        return قيمة
    def يقرأ_عدد_صحيح_بلا_إشارة():
        nonlocal منصب_قيمة
        قيمة = struct.unpack_from('>I', بيانات, منصب_قيمة)[0]
        منصب_قيمة += 4
        return قيمة
    문자들 = {}
    for رقم in range(1, 짧()):
        종류 = بيانات[منصب_قيمة]
        منصب_قيمة += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[رقم] = بيانات[منصب_قيمة:منصب_قيمة + 길이]
            منصب_قيمة += 길이
        elif 종류 in (7, 8): منصب_قيمة += 2
        elif 종류 in (3, 9, 10, 12): منصب_قيمة += 4
        else: raise AssertionError(종류)
    منصب_قيمة += 6
    개수 = 짧()
    منصب_قيمة += 개수 * 2
    assert 짧() == 0
    for رقم in range(짧()):
        짧()
        اسم = 짧()
        짧()
        for رقم in range(짧()):
            قيمة_السمة = 짧()
            حجم = يقرأ_عدد_صحيح_بلا_إشارة()
            if 문자들[اسم] == b'main' and 문자들[قيمة_السمة] == b'Code':
                return منصب_قيمة + 8, struct.unpack_from('>I', بيانات, منصب_قيمة + 4)[0]
            منصب_قيمة += حجم
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        دليل_قيمة = Path(임시)
        (دليل_قيمة / 'build').mkdir()
        مصدر = دليل_قيمة / 'Imported.java'
        مصدر.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(مصدر)], check=True)
        원본 = (دليل_قيمة / 'Imported.class').read_bytes()
        رمز_قيمة_f3cd31ee, 길이 = 주코드(원본)
        변형 = {}
        بيانات = bytearray(원본); بيانات[0] = 0; 변형['BadMagic'] = بيانات
        بيانات = bytearray(원본); بيانات[7] = 61; 변형['BadVer'] = بيانات
        بيانات = bytearray(원본); بيانات[8:10] = b'\xff\xff'; 변형['BadPool'] = بيانات
        بيانات = bytearray(원본); بيانات[رمز_قيمة_f3cd31ee:رمز_قيمة_f3cd31ee + 길이] = bytes(길이)
        بيانات[رمز_قيمة_f3cd31ee:رمز_قيمة_f3cd31ee + 3] = b'\xa7\x00\x01'; بيانات[رمز_قيمة_f3cd31ee + 길이 - 1] = 177; 변형['BadJump'] = بيانات
        بيانات = bytearray(원본); بيانات[رمز_قيمة_f3cd31ee:رمز_قيمة_f3cd31ee + 길이] = bytes(길이)
        بيانات[رمز_قيمة_f3cd31ee] = 87; بيانات[رمز_قيمة_f3cd31ee + 길이 - 1] = 177; 변형['BadStack'] = بيانات
        # اسم 검사를 통과시켜 الفعلي_بيانات ينفذ_أمر 중의 مُعامل_رمز 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        إدخال_قيمة_962f286b = ['Imported.class=' + str(دليل_قيمة / 'Imported.class'), 'Imported.java=' + str(مصدر)]
        for اسم, بيانات in 변형.items():
            مسار = دليل_قيمة / (اسم + '.class'); مسار.write_bytes(بيانات)
            إدخال_قيمة_962f286b.append(اسم + '.class=' + str(مسار))
        يجمع_قيمة = دليل_قيمة / 'build/java-files.bin'
        subprocess.run([sys.executable, str(موضع / 'أدوات/자바파일묶기.py'), '-o', str(يجمع_قيمة)] + إدخال_قيمة_962f286b, check=True)
        subprocess.run(['as', '--32', '-o', str(دليل_قيمة / 'user.o'), str(موضع / 'إقلاع_الآلة/فضاء_المستخدم.s')], cwd=str(دليل_قيمة), check=True)
        نواة_قيمة = دليل_قيمة / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(موضع / 'إقلاع_الآلة/تخطيط_الربط.ld'), '-o', str(نواة_قيمة),
                        str(موضع / 'build/boot.o'), str(موضع / 'build/java.o'), str(دليل_قيمة / 'user.o'), str(موضع / 'build/apps.o')], check=True)
        جهاز = جهاز_ظاهري(نواة_قيمة, شبكة_قيمة=False)
        try:
            جهاز.أمر('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            جهاز.أمر('cat Imported.java', ['int[] values = new int[3]'])
            for اسم, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                جهاز.أمر('java ' + اسم, [문구, 'Exit: 1'])
                جهاز.أمر('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return جهاز.سجل_سجل.decode('utf-8', 'replace')
        finally:
            جهاز.إغلاق()


if __name__ == '__main__':
    يوزّع_قيمة = argparse.ArgumentParser()
    يوزّع_قيمة.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    وسائط = يوزّع_قيمة.parse_args()
    نتيجة = {종류: مجموعة_الاختبارات(종류) for 종류 in (('elf', 'iso') if وسائط.boot == 'both' else (وسائط.boot,))}
    نتيجة['import'] = 적재시험()
    (موضع / 'build/자바시험.json').write_text(json.dumps(نتيجة, ensure_ascii=False, indent=2) + '\n')
