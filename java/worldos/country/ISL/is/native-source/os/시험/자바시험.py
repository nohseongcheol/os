#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 keyra_skipun, bilun_VALUE/tilfang_VALUE 경계 시험."""
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
from 사용자통신시험 import sýndar_vél, Staðsetning


def breyta_VALUE(vél, Heiti, Efni_VALUE, Store_VALUE=True):
    Keyra_2 = len(vél.LOG_lína)
    vél.직렬.sendall(('edit ' + Heiti + '\n').encode())
    vél.Bíddu_staða('...> ', Keyra_2)
    for Lína in Efni_VALUE.splitlines():
        assert len(Lína) <= 128
        Keyra_2 = len(vél.LOG_lína)
        vél.직렬.sendall((Lína + '\n').encode())
        vél.Bíddu_staða('...> ', Keyra_2)
    Keyra_2 = len(vél.LOG_lína)
    vél.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    NIÐURSTAÐA = vél.Bíddu_staða('jkoros> ', Keyra_2)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in NIÐURSTAÐA, NIÐURSTAÐA


def skrá_slóð():
    NIÐURSTAÐA = subprocess.check_output(['nm', '-n', str(Staðsetning / 'build/kernel.elf')], universal_newlines=True)
    for Lína in NIÐURSTAÐA.splitlines():
        if Lína.endswith(' ram_files'):
            return int(Lína.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gestur_skrá(vél, rauf_VALUE, Stærð, SLÓÐ):
    # 시험 VM의 메모리에서 raun_gögn 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    slóð = skrá_slóð() + rauf_VALUE * 16384
    vél.skjár_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(slóð, Stærð, SLÓÐ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if SLÓÐ.exists() and SLÓÐ.stat().st_size == Stærð:
            return SLÓÐ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    vél = sýndar_vél(Staðsetning / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Net_VALUE=False)
    NIÐURSTAÐA = {}
    try:
        vél.Skipun('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        vél.Skipun('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        vél.Skipun('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        vél.Skipun('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        vél.Skipun('java Missing', ['cannot read class: -2', 'Exit: 1'])
        vél.Skipun('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        vél.Skipun('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Efni_VALUE = '''public class Calc {
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
        breyta_VALUE(vél, 'Calc.java', Efni_VALUE)
        vél.Skipun('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        úttak = vél.Skipun('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        NIÐURSTAÐA['guest_output'] = úttak
        færsla_Listi = vél.Skipun('ls', ['Calc.class'])
        Stærð = int(re.search(r'Calc\.class\s+(\d+) bytes', færsla_Listi).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as skráasafn_VALUE:
            SLÓÐ = Path(skráasafn_VALUE) / 'Calc.class'
            gögn = gestur_skrá(vél, 3, Stærð, SLÓÐ)
            raun_gögn = subprocess.check_output(['java', '-Xverify:all', '-cp', skráasafn_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert raun_gögn.splitlines() == 기대, raun_gögn
            NIÐURSTAÐA['class_sha256'] = hashlib.sha256(gögn).hexdigest()
            NIÐURSTAÐA['openjdk_output'] = raun_gögn
        # 실패한 breyta_VALUE/컴파일은 기존 class를 보존한다.
        breyta_VALUE(vél, 'Calc.java', 'not Java at all', Store_VALUE=False)
        vél.Skipun('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ógilt_mæld_stærð in [
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
            breyta_VALUE(vél, 'Calc.java', ógilt_mæld_stærð)
            vél.Skipun('javac Calc.java', ['javac error:', 'Exit: 1'])
            vél.Skipun('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ítrekun_VALUE 실행은 notandi 힙/프레임을 매번 초기화한다.
        for númer in range(12):
            vél.Skipun('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        vél.Skipun('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        vél.Skipun('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        breyta_VALUE(vél, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        vél.Skipun('javac Calc.java', ['Compiled:', 'Exit: 0'])
        vél.Skipun('java Calc', ['instruction limit', 'Exit: 1'])
        vél.Skipun('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        breyta_VALUE(vél, 'Bad.class', 'garbage')
        vél.Skipun('java Bad', ['JVM error:', 'Exit: 1'])
        vél.Skipun('rm Bad.class', ['Removed'])
        vél.Skipun('java Bad', ['cannot read class: -2'])
        # breyta_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Keyra_2 = len(vél.LOG_lína)
        vél.직렬.sendall(b'edit Hello.java\n')
        vél.Bíddu_staða('...> ', Keyra_2)
        Keyra_2 = len(vél.LOG_lína)
        vél.직렬.sendall(b'x' * 129 + b'\n')
        vél.Bíddu_staða('...> ', Keyra_2)
        vél.Skipun('.save', ['Too much input; original preserved'])
        vél.Skipun('javac Hello.java', ['Compiled:', 'Exit: 0'])
        breyta_VALUE(vél, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for númer in range(3):
            breyta_VALUE(vél, 'f' + str(númer), 'occupied')
        vél.Skipun('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        vél.Skipun('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in vél.LOG_lína.decode('utf-8', 'replace')
        NIÐURSTAÐA['serial'] = vél.LOG_lína.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return NIÐURSTAÐA
    finally:
        vél.Loka()


def 주코드(gögn):
    """손상 시험용 main Code의 raun_gögn Skrá 오프셋/길이만 읽는다."""
    staða_VALUE = 8
    def 짧():
        nonlocal staða_VALUE
        VALUE = struct.unpack_from('>H', gögn, staða_VALUE)[0]
        staða_VALUE += 2
        return VALUE
    def 정():
        nonlocal staða_VALUE
        VALUE = struct.unpack_from('>I', gögn, staða_VALUE)[0]
        staða_VALUE += 4
        return VALUE
    문자들 = {}
    for númer in range(1, 짧()):
        종류 = gögn[staða_VALUE]
        staða_VALUE += 1
        if 종류 == 1:
            lengd_VALUE = 짧()
            문자들[númer] = gögn[staða_VALUE:staða_VALUE + lengd_VALUE]
            staða_VALUE += lengd_VALUE
        elif 종류 in (7, 8): staða_VALUE += 2
        elif 종류 in (3, 9, 10, 12): staða_VALUE += 4
        else: raise AssertionError(종류)
    staða_VALUE += 6
    vara_COUNT = 짧()
    staða_VALUE += vara_COUNT * 2
    assert 짧() == 0
    for númer in range(짧()):
        짧()
        Heiti = 짧()
        짧()
        for númer in range(짧()):
            eigind_VALUE = 짧()
            Stærð = 정()
            if 문자들[Heiti] == b'main' and 문자들[eigind_VALUE] == b'Code':
                return staða_VALUE + 8, struct.unpack_from('>I', gögn, staða_VALUE + 4)[0]
            staða_VALUE += Stærð
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        skráasafn_VALUE = Path(임시)
        (skráasafn_VALUE / 'build').mkdir()
        Uppruni = skráasafn_VALUE / 'Imported.java'
        Uppruni.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Uppruni)], check=True)
        원본 = (skráasafn_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, lengd_VALUE = 주코드(원본)
        afbrigði_VALUE = {}
        gögn = bytearray(원본); gögn[0] = 0; afbrigði_VALUE['BadMagic'] = gögn
        gögn = bytearray(원본); gögn[7] = 61; afbrigði_VALUE['BadVer'] = gögn
        gögn = bytearray(원본); gögn[8:10] = b'\xff\xff'; afbrigði_VALUE['BadPool'] = gögn
        gögn = bytearray(원본); gögn[CODE_VALUE:CODE_VALUE + lengd_VALUE] = bytes(lengd_VALUE)
        gögn[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; gögn[CODE_VALUE + lengd_VALUE - 1] = 177; afbrigði_VALUE['BadJump'] = gögn
        gögn = bytearray(원본); gögn[CODE_VALUE:CODE_VALUE + lengd_VALUE] = bytes(lengd_VALUE)
        gögn[CODE_VALUE] = 87; gögn[CODE_VALUE + lengd_VALUE - 1] = 177; afbrigði_VALUE['BadStack'] = gögn
        # Heiti 검사를 통과시켜 raun_gögn keyra_skipun 중의 스택 오류까지 검사한다.
        afbrigði_VALUE['BadStack'] = afbrigði_VALUE['BadStack'].replace(b'Imported', b'BadStack')
        færsla_VALUE = ['Imported.class=' + str(skráasafn_VALUE / 'Imported.class'), 'Imported.java=' + str(Uppruni)]
        for Heiti, gögn in afbrigði_VALUE.items():
            SLÓÐ = skráasafn_VALUE / (Heiti + '.class'); SLÓÐ.write_bytes(gögn)
            færsla_VALUE.append(Heiti + '.class=' + str(SLÓÐ))
        Hópur_VALUE = skráasafn_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Staðsetning / 'Verkfæri/자바파일묶기.py'), '-o', str(Hópur_VALUE)] + færsla_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(skráasafn_VALUE / 'user.o'), str(Staðsetning / '부팅/notandi.s')], cwd=str(skráasafn_VALUE), check=True)
        kjarni_VALUE = skráasafn_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Staðsetning / '부팅/tengja_útlit.ld'), '-o', str(kjarni_VALUE),
                        str(Staðsetning / 'build/boot.o'), str(Staðsetning / 'build/java.o'), str(skráasafn_VALUE / 'user.o'), str(Staðsetning / 'build/apps.o')], check=True)
        vél = sýndar_vél(kjarni_VALUE, Net_VALUE=False)
        try:
            vél.Skipun('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            vél.Skipun('cat Imported.java', ['int[] values = new int[3]'])
            for Heiti, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                vél.Skipun('java ' + Heiti, [문구, 'Exit: 1'])
                vél.Skipun('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return vél.LOG_lína.decode('utf-8', 'replace')
        finally:
            vél.Loka()


if __name__ == '__main__':
    þátta_VALUE = argparse.ArgumentParser()
    þátta_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Viðföng = þátta_VALUE.parse_args()
    NIÐURSTAÐA = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Viðföng.boot == 'both' else (Viðföng.boot,))}
    NIÐURSTAÐA['import'] = 적재시험()
    (Staðsetning / 'build/자바시험.json').write_text(json.dumps(NIÐURSTAÐA, ensure_ascii=False, indent=2) + '\n')
