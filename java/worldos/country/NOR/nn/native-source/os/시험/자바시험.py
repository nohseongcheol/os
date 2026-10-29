#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Utfør_kommando, feil_VALUE/ressurs_VALUE 경계 시험."""
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
from 사용자통신시험 import virtuell_maskin, Posisjon


def redigere_VALUE(maskin, Namn, Innhald_VALUE, Store_VALUE=True):
    Køyr_2 = len(maskin.LOG_rad)
    maskin.직렬.sendall(('edit ' + Namn + '\n').encode())
    maskin.vent_status('...> ', Køyr_2)
    for linje in Innhald_VALUE.splitlines():
        assert len(linje) <= 128
        Køyr_2 = len(maskin.LOG_rad)
        maskin.직렬.sendall((linje + '\n').encode())
        maskin.vent_status('...> ', Køyr_2)
    Køyr_2 = len(maskin.LOG_rad)
    maskin.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    forretningsmål = maskin.vent_status('jkoros> ', Køyr_2)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in forretningsmål, forretningsmål


def fil_ADDRESS():
    forretningsmål = subprocess.check_output(['nm', '-n', str(Posisjon / 'build/kernel.elf')], universal_newlines=True)
    for linje in forretningsmål.splitlines():
        if linje.endswith(' ram_files'):
            return int(linje.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gjest_fil(maskin, felt_VALUE, Storleik, STIGE):
    # 시험 VM의 메모리에서 faktisk_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADDRESS = fil_ADDRESS() + felt_VALUE * 16384
    maskin.skjerm_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADDRESS, Storleik, STIGE)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if STIGE.exists() and STIGE.stat().st_size == Storleik:
            return STIGE.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    maskin = virtuell_maskin(Posisjon / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Nettverk_VALUE=False)
    forretningsmål = {}
    try:
        maskin.Kommando('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        maskin.Kommando('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        maskin.Kommando('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        maskin.Kommando('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        maskin.Kommando('java Missing', ['cannot read class: -2', 'Exit: 1'])
        maskin.Kommando('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        maskin.Kommando('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Innhald_VALUE = '''public class Calc {
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
        redigere_VALUE(maskin, 'Calc.java', Innhald_VALUE)
        maskin.Kommando('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Utdata = maskin.Kommando('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        forretningsmål['guest_output'] = Utdata
        oppføring_Liste = maskin.Kommando('ls', ['Calc.class'])
        Storleik = int(re.search(r'Calc\.class\s+(\d+) bytes', oppføring_Liste).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as katalog_VALUE:
            STIGE = Path(katalog_VALUE) / 'Calc.class'
            data = gjest_fil(maskin, 3, Storleik, STIGE)
            faktisk_data = subprocess.check_output(['java', '-Xverify:all', '-cp', katalog_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert faktisk_data.splitlines() == 기대, faktisk_data
            forretningsmål['class_sha256'] = hashlib.sha256(data).hexdigest()
            forretningsmål['openjdk_output'] = faktisk_data
        # 실패한 redigere_VALUE/컴파일은 기존 class를 보존한다.
        redigere_VALUE(maskin, 'Calc.java', 'not Java at all', Store_VALUE=False)
        maskin.Kommando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ugyldig_forretningsmål in [
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
            redigere_VALUE(maskin, 'Calc.java', ugyldig_forretningsmål)
            maskin.Kommando('javac Calc.java', ['javac error:', 'Exit: 1'])
            maskin.Kommando('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # gjentaking_VALUE 실행은 brukar 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            maskin.Kommando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        maskin.Kommando('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        maskin.Kommando('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        redigere_VALUE(maskin, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        maskin.Kommando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        maskin.Kommando('java Calc', ['instruction limit', 'Exit: 1'])
        maskin.Kommando('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        redigere_VALUE(maskin, 'Bad.class', 'garbage')
        maskin.Kommando('java Bad', ['JVM error:', 'Exit: 1'])
        maskin.Kommando('rm Bad.class', ['Removed'])
        maskin.Kommando('java Bad', ['cannot read class: -2'])
        # redigere_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Køyr_2 = len(maskin.LOG_rad)
        maskin.직렬.sendall(b'edit Hello.java\n')
        maskin.vent_status('...> ', Køyr_2)
        Køyr_2 = len(maskin.LOG_rad)
        maskin.직렬.sendall(b'x' * 129 + b'\n')
        maskin.vent_status('...> ', Køyr_2)
        maskin.Kommando('.save', ['Too much input; original preserved'])
        maskin.Kommando('javac Hello.java', ['Compiled:', 'Exit: 0'])
        redigere_VALUE(maskin, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            redigere_VALUE(maskin, 'f' + str(수), 'occupied')
        maskin.Kommando('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        maskin.Kommando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in maskin.LOG_rad.decode('utf-8', 'replace')
        forretningsmål['serial'] = maskin.LOG_rad.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return forretningsmål
    finally:
        maskin.Lukk()


def 주코드(data):
    """손상 시험용 main Code의 faktisk_data Fil 오프셋/길이만 읽는다."""
    plassere_VALUE = 8
    def 짧():
        nonlocal plassere_VALUE
        VALUE = struct.unpack_from('>H', data, plassere_VALUE)[0]
        plassere_VALUE += 2
        return VALUE
    def 정():
        nonlocal plassere_VALUE
        VALUE = struct.unpack_from('>I', data, plassere_VALUE)[0]
        plassere_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = data[plassere_VALUE]
        plassere_VALUE += 1
        if 종류 == 1:
            lengd_VALUE = 짧()
            문자들[수] = data[plassere_VALUE:plassere_VALUE + lengd_VALUE]
            plassere_VALUE += lengd_VALUE
        elif 종류 in (7, 8): plassere_VALUE += 2
        elif 종류 in (3, 9, 10, 12): plassere_VALUE += 4
        else: raise AssertionError(종류)
    plassere_VALUE += 6
    vare_COUNT = 짧()
    plassere_VALUE += vare_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Namn = 짧()
        짧()
        for 수 in range(짧()):
            attributt_VALUE = 짧()
            Storleik = 정()
            if 문자들[Namn] == b'main' and 문자들[attributt_VALUE] == b'Code':
                return plassere_VALUE + 8, struct.unpack_from('>I', data, plassere_VALUE + 4)[0]
            plassere_VALUE += Storleik
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        katalog_VALUE = Path(임시)
        (katalog_VALUE / 'build').mkdir()
        KJELDE = katalog_VALUE / 'Imported.java'
        KJELDE.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(KJELDE)], check=True)
        원본 = (katalog_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, lengd_VALUE = 주코드(원본)
        변형 = {}
        data = bytearray(원본); data[0] = 0; 변형['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; 변형['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; 변형['BadPool'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + lengd_VALUE] = bytes(lengd_VALUE)
        data[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; data[CODE_VALUE + lengd_VALUE - 1] = 177; 변형['BadJump'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + lengd_VALUE] = bytes(lengd_VALUE)
        data[CODE_VALUE] = 87; data[CODE_VALUE + lengd_VALUE - 1] = 177; 변형['BadStack'] = data
        # Namn 검사를 통과시켜 faktisk_data Utfør_kommando 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        oppføring_VALUE = ['Imported.class=' + str(katalog_VALUE / 'Imported.class'), 'Imported.java=' + str(KJELDE)]
        for Namn, data in 변형.items():
            STIGE = katalog_VALUE / (Namn + '.class'); STIGE.write_bytes(data)
            oppføring_VALUE.append(Namn + '.class=' + str(STIGE))
        gruppe_VALUE = katalog_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Posisjon / 'Verktøy/자바파일묶기.py'), '-o', str(gruppe_VALUE)] + oppføring_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(katalog_VALUE / 'user.o'), str(Posisjon / '부팅/brukar.s')], cwd=str(katalog_VALUE), check=True)
        kjerne_VALUE = katalog_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisjon / '부팅/kople_Oppsett.ld'), '-o', str(kjerne_VALUE),
                        str(Posisjon / 'build/boot.o'), str(Posisjon / 'build/java.o'), str(katalog_VALUE / 'user.o'), str(Posisjon / 'build/apps.o')], check=True)
        maskin = virtuell_maskin(kjerne_VALUE, Nettverk_VALUE=False)
        try:
            maskin.Kommando('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            maskin.Kommando('cat Imported.java', ['int[] values = new int[3]'])
            for Namn, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                maskin.Kommando('java ' + Namn, [문구, 'Exit: 1'])
                maskin.Kommando('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return maskin.LOG_rad.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()


if __name__ == '__main__':
    dele_opp_VALUE = argparse.ArgumentParser()
    dele_opp_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argument = dele_opp_VALUE.parse_args()
    forretningsmål = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argument.boot == 'both' else (Argument.boot,))}
    forretningsmål['import'] = 적재시험()
    (Posisjon / 'build/자바시험.json').write_text(json.dumps(forretningsmål, ensure_ascii=False, indent=2) + '\n')
