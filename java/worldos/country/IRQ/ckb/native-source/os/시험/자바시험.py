#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 جێبەجێکردن_فەرمان, شکستهێنان_نرخ/ژێدەر_نرخ 경계 시험."""
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
from 사용자통신시험 import مەجازی_مەکینه, 위치


def بژار_نرخ(مەکینه, ناو, ناوەرۆک_نرخ, Store_نرخ=True):
    ڕادان = len(مەکینه.تۆمار_ڕزن)
    مەکینه.직렬.sendall(('edit ' + ناو + '\n').encode())
    مەکینه.چاوەڕوان_کردن_دۆخ('...> ', ڕادان)
    for دێڕ in ناوەرۆک_نرخ.splitlines():
        assert len(دێڕ) <= 128
        ڕادان = len(مەکینه.تۆمار_ڕزن)
        مەکینه.직렬.sendall((دێڕ + '\n').encode())
        مەکینه.چاوەڕوان_کردن_دۆخ('...> ', ڕادان)
    ڕادان = len(مەکینه.تۆمار_ڕزن)
    مەکینه.직렬.sendall(b'.save\n' if Store_نرخ else b'.cancel\n')
    결과 = مەکینه.چاوەڕوان_کردن_دۆخ('jkoros> ', ڕادان)
    assert ('Saved:' if Store_نرخ else 'Cancelled; original preserved') in 결과, 결과


def فایل_ناونیشان():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for دێڕ in 결과.splitlines():
        if دێڕ.endswith(' ram_files'):
            return int(دێڕ.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(مەکینه, کەلێن_بۆ_نووسین_یان_رەمز_نرخ, گۆڕینی_ئەندازە, گوزەر):
    # 시험 VM의 메모리에서 ڕاستەکی_دەیتا 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ناونیشان = فایل_ناونیشان() + کەلێن_بۆ_نووسین_یان_رەمز_نرخ * 16384
    مەکینه.مۆنیتۆر_نرخ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ناونیشان, گۆڕینی_ئەندازە, گوزەر)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if گوزەر.exists() and گوزەر.stat().st_size == گۆڕینی_ئەندازە:
            return گوزەر.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    مەکینه = مەجازی_مەکینه(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, تۆڕ_نرخ=False)
    결과 = {}
    try:
        مەکینه.فەرمان('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        مەکینه.فەرمان('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        مەکینه.فەرمان('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        مەکینه.فەرمان('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        مەکینه.فەرمان('java Missing', ['cannot read class: -2', 'Exit: 1'])
        مەکینه.فەرمان('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        مەکینه.فەرمان('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ناوەرۆک_نرخ = '''public class Calc {
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
        بژار_نرخ(مەکینه, 'Calc.java', ناوەرۆک_نرخ)
        مەکینه.فەرمان('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = مەکینه.فەرمان('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        تێنووسین_لیست = مەکینه.فەرمان('ls', ['Calc.class'])
        گۆڕینی_ئەندازە = int(re.search(r'Calc\.class\s+(\d+) bytes', تێنووسین_لیست).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ڕێبەرنامە_نرخ:
            گوزەر = Path(ڕێبەرنامە_نرخ) / 'Calc.class'
            دەیتا = 게스트파일(مەکینه, 3, گۆڕینی_ئەندازە, گوزەر)
            ڕاستەکی_دەیتا = subprocess.check_output(['java', '-Xverify:all', '-cp', ڕێبەرنامە_نرخ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ڕاستەکی_دەیتا.splitlines() == 기대, ڕاستەکی_دەیتا
            결과['class_sha256'] = hashlib.sha256(دەیتا).hexdigest()
            결과['openjdk_output'] = ڕاستەکی_دەیتا
        # 실패한 بژار_نرخ/컴파일은 기존 class를 보존한다.
        بژار_نرخ(مەکینه, 'Calc.java', 'not Java at all', Store_نرخ=False)
        مەکینه.فەرمان('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            بژار_نرخ(مەکینه, 'Calc.java', 잘못)
            مەکینه.فەرمان('javac Calc.java', ['javac error:', 'Exit: 1'])
            مەکینه.فەرمان('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # دووبارەکردنەوە_نرخ 실행은 بەکارهێنەر 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            مەکینه.فەرمان('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        مەکینه.فەرمان('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        مەکینه.فەرمان('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        بژار_نرخ(مەکینه, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        مەکینه.فەرمان('javac Calc.java', ['Compiled:', 'Exit: 0'])
        مەکینه.فەرمان('java Calc', ['instruction limit', 'Exit: 1'])
        مەکینه.فەرمان('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        بژار_نرخ(مەکینه, 'Bad.class', 'garbage')
        مەکینه.فەرمان('java Bad', ['JVM error:', 'Exit: 1'])
        مەکینه.فەرمان('rm Bad.class', ['Removed'])
        مەکینه.فەرمان('java Bad', ['cannot read class: -2'])
        # بژار_نرخ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ڕادان = len(مەکینه.تۆمار_ڕزن)
        مەکینه.직렬.sendall(b'edit Hello.java\n')
        مەکینه.چاوەڕوان_کردن_دۆخ('...> ', ڕادان)
        ڕادان = len(مەکینه.تۆمار_ڕزن)
        مەکینه.직렬.sendall(b'x' * 129 + b'\n')
        مەکینه.چاوەڕوان_کردن_دۆخ('...> ', ڕادان)
        مەکینه.فەرمان('.save', ['Too much input; original preserved'])
        مەکینه.فەرمان('javac Hello.java', ['Compiled:', 'Exit: 0'])
        بژار_نرخ(مەکینه, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            بژار_نرخ(مەکینه, 'f' + str(수), 'occupied')
        مەکینه.فەرمان('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        مەکینه.فەرمان('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
        결과['serial'] = مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        مەکینه.داخستن()


def 주코드(دەیتا):
    """손상 시험용 main Code의 ڕاستەکی_دەیتا فایل 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        نرخ = struct.unpack_from('>H', دەیتا, 위치값)[0]
        위치값 += 2
        return نرخ
    def 정():
        nonlocal 위치값
        نرخ = struct.unpack_from('>I', دەیتا, 위치값)[0]
        위치값 += 4
        return نرخ
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = دەیتا[위치값]
        위치값 += 1
        if 종류 == 1:
            درێژی_نرخ = 짧()
            문자들[수] = دەیتا[위치값:위치값 + درێژی_نرخ]
            위치값 += درێژی_نرخ
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ناو = 짧()
        짧()
        for 수 in range(짧()):
            تایبەتمەندی_نرخ = 짧()
            گۆڕینی_ئەندازە = 정()
            if 문자들[ناو] == b'main' and 문자들[تایبەتمەندی_نرخ] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', دەیتا, 위치값 + 4)[0]
            위치값 += گۆڕینی_ئەندازە
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ڕێبەرنامە_نرخ = Path(임시)
        (ڕێبەرنامە_نرخ / 'build').mkdir()
        ژێدەر = ڕێبەرنامە_نرخ / 'Imported.java'
        ژێدەر.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ژێدەر)], check=True)
        원본 = (ڕێبەرنامە_نرخ / 'Imported.class').read_bytes()
        코드, درێژی_نرخ = 주코드(원본)
        변형 = {}
        دەیتا = bytearray(원본); دەیتا[0] = 0; 변형['BadMagic'] = دەیتا
        دەیتا = bytearray(원본); دەیتا[7] = 61; 변형['BadVer'] = دەیتا
        دەیتا = bytearray(원본); دەیتا[8:10] = b'\xff\xff'; 변형['BadPool'] = دەیتا
        دەیتا = bytearray(원본); دەیتا[코드:코드 + درێژی_نرخ] = bytes(درێژی_نرخ)
        دەیتا[코드:코드 + 3] = b'\xa7\x00\x01'; دەیتا[코드 + درێژی_نرخ - 1] = 177; 변형['BadJump'] = دەیتا
        دەیتا = bytearray(원본); دەیتا[코드:코드 + درێژی_نرخ] = bytes(درێژی_نرخ)
        دەیتا[코드] = 87; دەیتا[코드 + درێژی_نرخ - 1] = 177; 변형['BadStack'] = دەیتا
        # ناو 검사를 통과시켜 ڕاستەکی_دەیتا جێبەجێکردن_فەرمان 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        تێنووسین_نرخ = ['Imported.class=' + str(ڕێبەرنامە_نرخ / 'Imported.class'), 'Imported.java=' + str(ژێدەر)]
        for ناو, دەیتا in 변형.items():
            گوزەر = ڕێبەرنامە_نرخ / (ناو + '.class'); گوزەر.write_bytes(دەیتا)
            تێنووسین_نرخ.append(ناو + '.class=' + str(گوزەر))
        گروپ_نرخ = ڕێبەرنامە_نرخ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'ئامرازەکان/자바파일묶기.py'), '-o', str(گروپ_نرخ)] + تێنووسین_نرخ, check=True)
        subprocess.run(['as', '--32', '-o', str(ڕێبەرنامە_نرخ / 'user.o'), str(위치 / '부팅/بەکارهێنەر.s')], cwd=str(ڕێبەرنامە_نرخ), check=True)
        کوورەک_نرخ = ڕێبەرنامە_نرخ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/لینك_ڕیزبەست.ld'), '-o', str(کوورەک_نرخ),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(ڕێبەرنامە_نرخ / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        مەکینه = مەجازی_مەکینه(کوورەک_نرخ, تۆڕ_نرخ=False)
        try:
            مەکینه.فەرمان('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            مەکینه.فەرمان('cat Imported.java', ['int[] values = new int[3]'])
            for ناو, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                مەکینه.فەرمان('java ' + ناو, [문구, 'Exit: 1'])
                مەکینه.فەرمان('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
        finally:
            مەکینه.داخستن()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = 해석.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
