#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 uitvoer_bevel, faling_VALUE/hulpbron_VALUE 경계 시험."""
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
from 사용자통신시험 import virtueel_masjien, Posisie


def redigeer_VALUE(masjien, Naam, Inhoud_VALUE, bêre_VALUE=True):
    Loop = len(masjien.LOG_ry)
    masjien.직렬.sendall(('edit ' + Naam + '\n').encode())
    masjien.wag_stand('...> ', Loop)
    for lyn in Inhoud_VALUE.splitlines():
        assert len(lyn) <= 128
        Loop = len(masjien.LOG_ry)
        masjien.직렬.sendall((lyn + '\n').encode())
        masjien.wag_stand('...> ', Loop)
    Loop = len(masjien.LOG_ry)
    masjien.직렬.sendall(b'.save\n' if bêre_VALUE else b'.cancel\n')
    maatreël = masjien.wag_stand('jkoros> ', Loop)
    assert ('Saved:' if bêre_VALUE else 'Cancelled; original preserved') in maatreël, maatreël


def lêer_adres():
    maatreël = subprocess.check_output(['nm', '-n', str(Posisie / 'build/kernel.elf')], universal_newlines=True)
    for lyn in maatreël.splitlines():
        if lyn.endswith(' ram_files'):
            return int(lyn.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gas_lêer(masjien, gleuf_VALUE, Grootte, Pad):
    # 시험 VM의 메모리에서 werklik_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    adres = lêer_adres() + gleuf_VALUE * 16384
    masjien.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(adres, Grootte, Pad)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Pad.exists() and Pad.stat().st_size == Grootte:
            return Pad.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    masjien = virtueel_masjien(Posisie / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Netwerk_VALUE=False)
    maatreël = {}
    try:
        masjien.Opdrag('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        masjien.Opdrag('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        masjien.Opdrag('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        masjien.Opdrag('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        masjien.Opdrag('java Missing', ['cannot read class: -2', 'Exit: 1'])
        masjien.Opdrag('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        masjien.Opdrag('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Inhoud_VALUE = '''public class Calc {
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
        redigeer_VALUE(masjien, 'Calc.java', Inhoud_VALUE)
        masjien.Opdrag('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Afvoer = masjien.Opdrag('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        maatreël['guest_output'] = Afvoer
        inskrywing_Lys = masjien.Opdrag('ls', ['Calc.class'])
        Grootte = int(re.search(r'Calc\.class\s+(\d+) bytes', inskrywing_Lys).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as gids_VALUE:
            Pad = Path(gids_VALUE) / 'Calc.class'
            data = gas_lêer(masjien, 3, Grootte, Pad)
            werklik_data = subprocess.check_output(['java', '-Xverify:all', '-cp', gids_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert werklik_data.splitlines() == 기대, werklik_data
            maatreël['class_sha256'] = hashlib.sha256(data).hexdigest()
            maatreël['openjdk_output'] = werklik_data
        # 실패한 redigeer_VALUE/컴파일은 기존 class를 보존한다.
        redigeer_VALUE(masjien, 'Calc.java', 'not Java at all', bêre_VALUE=False)
        masjien.Opdrag('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ongeldig_maatreël in [
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
            redigeer_VALUE(masjien, 'Calc.java', ongeldig_maatreël)
            masjien.Opdrag('javac Calc.java', ['javac error:', 'Exit: 1'])
            masjien.Opdrag('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 gebruiker 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            masjien.Opdrag('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        masjien.Opdrag('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        masjien.Opdrag('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        redigeer_VALUE(masjien, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        masjien.Opdrag('javac Calc.java', ['Compiled:', 'Exit: 0'])
        masjien.Opdrag('java Calc', ['instruction limit', 'Exit: 1'])
        masjien.Opdrag('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        redigeer_VALUE(masjien, 'Bad.class', 'garbage')
        masjien.Opdrag('java Bad', ['JVM error:', 'Exit: 1'])
        masjien.Opdrag('rm Bad.class', ['Removed'])
        masjien.Opdrag('java Bad', ['cannot read class: -2'])
        # redigeer_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Loop = len(masjien.LOG_ry)
        masjien.직렬.sendall(b'edit Hello.java\n')
        masjien.wag_stand('...> ', Loop)
        Loop = len(masjien.LOG_ry)
        masjien.직렬.sendall(b'x' * 129 + b'\n')
        masjien.wag_stand('...> ', Loop)
        masjien.Opdrag('.save', ['Too much input; original preserved'])
        masjien.Opdrag('javac Hello.java', ['Compiled:', 'Exit: 0'])
        redigeer_VALUE(masjien, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            redigeer_VALUE(masjien, 'f' + str(수), 'occupied')
        masjien.Opdrag('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        masjien.Opdrag('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in masjien.LOG_ry.decode('utf-8', 'replace')
        maatreël['serial'] = masjien.LOG_ry.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return maatreël
    finally:
        masjien.Sluit()


def 주코드(data):
    """손상 시험용 main Code의 werklik_data Lêer 오프셋/길이만 읽는다."""
    plaas_VALUE = 8
    def 짧():
        nonlocal plaas_VALUE
        VALUE = struct.unpack_from('>H', data, plaas_VALUE)[0]
        plaas_VALUE += 2
        return VALUE
    def 정():
        nonlocal plaas_VALUE
        VALUE = struct.unpack_from('>I', data, plaas_VALUE)[0]
        plaas_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = data[plaas_VALUE]
        plaas_VALUE += 1
        if 종류 == 1:
            lengte_VALUE = 짧()
            문자들[수] = data[plaas_VALUE:plaas_VALUE + lengte_VALUE]
            plaas_VALUE += lengte_VALUE
        elif 종류 in (7, 8): plaas_VALUE += 2
        elif 종류 in (3, 9, 10, 12): plaas_VALUE += 4
        else: raise AssertionError(종류)
    plaas_VALUE += 6
    item_COUNT = 짧()
    plaas_VALUE += item_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Naam = 짧()
        짧()
        for 수 in range(짧()):
            kenmerk_VALUE = 짧()
            Grootte = 정()
            if 문자들[Naam] == b'main' and 문자들[kenmerk_VALUE] == b'Code':
                return plaas_VALUE + 8, struct.unpack_from('>I', data, plaas_VALUE + 4)[0]
            plaas_VALUE += Grootte
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        gids_VALUE = Path(임시)
        (gids_VALUE / 'build').mkdir()
        Bron = gids_VALUE / 'Imported.java'
        Bron.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Bron)], check=True)
        원본 = (gids_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, lengte_VALUE = 주코드(원본)
        변형 = {}
        data = bytearray(원본); data[0] = 0; 변형['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; 변형['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; 변형['BadPool'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + lengte_VALUE] = bytes(lengte_VALUE)
        data[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; data[CODE_VALUE + lengte_VALUE - 1] = 177; 변형['BadJump'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + lengte_VALUE] = bytes(lengte_VALUE)
        data[CODE_VALUE] = 87; data[CODE_VALUE + lengte_VALUE - 1] = 177; 변형['BadStack'] = data
        # Naam 검사를 통과시켜 werklik_data uitvoer_bevel 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        inskrywing_VALUE = ['Imported.class=' + str(gids_VALUE / 'Imported.class'), 'Imported.java=' + str(Bron)]
        for Naam, data in 변형.items():
            Pad = gids_VALUE / (Naam + '.class'); Pad.write_bytes(data)
            inskrywing_VALUE.append(Naam + '.class=' + str(Pad))
        Groep_VALUE = gids_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Posisie / 'Nutsmiddels/자바파일묶기.py'), '-o', str(Groep_VALUE)] + inskrywing_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(gids_VALUE / 'user.o'), str(Posisie / '부팅/gebruiker.s')], cwd=str(gids_VALUE), check=True)
        kern_VALUE = gids_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisie / '부팅/Skakel_Uitleg.ld'), '-o', str(kern_VALUE),
                        str(Posisie / 'build/boot.o'), str(Posisie / 'build/java.o'), str(gids_VALUE / 'user.o'), str(Posisie / 'build/apps.o')], check=True)
        masjien = virtueel_masjien(kern_VALUE, Netwerk_VALUE=False)
        try:
            masjien.Opdrag('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            masjien.Opdrag('cat Imported.java', ['int[] values = new int[3]'])
            for Naam, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                masjien.Opdrag('java ' + Naam, [문구, 'Exit: 1'])
                masjien.Opdrag('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return masjien.LOG_ry.decode('utf-8', 'replace')
        finally:
            masjien.Sluit()


if __name__ == '__main__':
    ontleed_VALUE = argparse.ArgumentParser()
    ontleed_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ontleed_VALUE.parse_args()
    maatreël = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    maatreël['import'] = 적재시험()
    (Posisie / 'build/자바시험.json').write_text(json.dumps(maatreël, ensure_ascii=False, indent=2) + '\n')
