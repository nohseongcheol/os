#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 실행, ella_njaru/wallitorde_njaru 경계 시험."""
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
from 사용자통신시험 import 가상기계, 위치


def feewnditde_njaru(기계, innde, loowdi_njaru, resde_njaru=True):
    huutoraade = len(기계.suurnal_winndande)
    기계.직렬.sendall(('edit ' + innde + '\n').encode())
    기계.기다림('...> ', huutoraade)
    for diidol in loowdi_njaru.splitlines():
        assert len(diidol) <= 128
        huutoraade = len(기계.suurnal_winndande)
        기계.직렬.sendall((diidol + '\n').encode())
        기계.기다림('...> ', huutoraade)
    huutoraade = len(기계.suurnal_winndande)
    기계.직렬.sendall(b'.save\n' if resde_njaru else b'.cancel\n')
    결과 = 기계.기다림('jkoros> ', huutoraade)
    assert ('Saved:' if resde_njaru else 'Cancelled; original preserved') in 결과, 결과


def fiilde_ñiiɓirde():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for diidol in 결과.splitlines():
        if diidol.endswith(' ram_files'):
            return int(diidol.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(기계, 슬롯, waylude_etannde, laawol):
    # 시험 VM의 메모리에서 laatii_keɓe 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ñiiɓirde = fiilde_ñiiɓirde() + 슬롯 * 16384
    기계.moniteer_njaru.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ñiiɓirde, waylude_etannde, laawol)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if laawol.exists() and laawol.stat().st_size == waylude_etannde:
            return laawol.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, laylaytol_njaru=False)
    결과 = {}
    try:
        기계.ginol('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        기계.ginol('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        기계.ginol('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        기계.ginol('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        기계.ginol('java Missing', ['cannot read class: -2', 'Exit: 1'])
        기계.ginol('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        기계.ginol('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        loowdi_njaru = '''public class Calc {
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
        feewnditde_njaru(기계, 'Calc.java', loowdi_njaru)
        기계.ginol('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = 기계.ginol('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        naatnugol_Doggol = 기계.ginol('ls', ['Calc.class'])
        waylude_etannde = int(re.search(r'Calc\.class\s+(\d+) bytes', naatnugol_Doggol).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as mooftordu_njaru:
            laawol = Path(mooftordu_njaru) / 'Calc.class'
            keɓe = 게스트파일(기계, 3, waylude_etannde, laawol)
            laatii_keɓe = subprocess.check_output(['java', '-Xverify:all', '-cp', mooftordu_njaru, 'Calc', '6', 'guest'], universal_newlines=True)
            assert laatii_keɓe.splitlines() == 기대, laatii_keɓe
            결과['class_sha256'] = hashlib.sha256(keɓe).hexdigest()
            결과['openjdk_output'] = laatii_keɓe
        # 실패한 feewnditde_njaru/컴파일은 기존 class를 보존한다.
        feewnditde_njaru(기계, 'Calc.java', 'not Java at all', resde_njaru=False)
        기계.ginol('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            feewnditde_njaru(기계, 'Calc.java', 잘못)
            기계.ginol('javac Calc.java', ['javac error:', 'Exit: 1'])
            기계.ginol('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # 반복 실행은 kuutoro 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            기계.ginol('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        기계.ginol('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        기계.ginol('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        feewnditde_njaru(기계, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        기계.ginol('javac Calc.java', ['Compiled:', 'Exit: 0'])
        기계.ginol('java Calc', ['instruction limit', 'Exit: 1'])
        기계.ginol('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        feewnditde_njaru(기계, 'Bad.class', 'garbage')
        기계.ginol('java Bad', ['JVM error:', 'Exit: 1'])
        기계.ginol('rm Bad.class', ['Removed'])
        기계.ginol('java Bad', ['cannot read class: -2'])
        # feewnditde_njaru 입력의 넘친 부분을 잘라서 저장하지 않는다.
        huutoraade = len(기계.suurnal_winndande)
        기계.직렬.sendall(b'edit Hello.java\n')
        기계.기다림('...> ', huutoraade)
        huutoraade = len(기계.suurnal_winndande)
        기계.직렬.sendall(b'x' * 129 + b'\n')
        기계.기다림('...> ', huutoraade)
        기계.ginol('.save', ['Too much input; original preserved'])
        기계.ginol('javac Hello.java', ['Compiled:', 'Exit: 0'])
        feewnditde_njaru(기계, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            feewnditde_njaru(기계, 'f' + str(수), 'occupied')
        기계.ginol('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        기계.ginol('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 기계.suurnal_winndande.decode('utf-8', 'replace')
        결과['serial'] = 기계.suurnal_winndande.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        기계.uddude()


def 주코드(keɓe):
    """손상 시험용 main Code의 laatii_keɓe fiilde 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        njaru = struct.unpack_from('>H', keɓe, 위치값)[0]
        위치값 += 2
        return njaru
    def 정():
        nonlocal 위치값
        njaru = struct.unpack_from('>I', keɓe, 위치값)[0]
        위치값 += 4
        return njaru
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = keɓe[위치값]
        위치값 += 1
        if 종류 == 1:
            njuuteendi_njaru = 짧()
            문자들[수] = keɓe[위치값:위치값 + njuuteendi_njaru]
            위치값 += njuuteendi_njaru
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        innde = 짧()
        짧()
        for 수 in range(짧()):
            mbaadi_njaru = 짧()
            waylude_etannde = 정()
            if 문자들[innde] == b'main' and 문자들[mbaadi_njaru] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', keɓe, 위치값 + 4)[0]
            위치값 += waylude_etannde
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        mooftordu_njaru = Path(임시)
        (mooftordu_njaru / 'build').mkdir()
        sewnde = mooftordu_njaru / 'Imported.java'
        sewnde.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(sewnde)], check=True)
        원본 = (mooftordu_njaru / 'Imported.class').read_bytes()
        코드, njuuteendi_njaru = 주코드(원본)
        변형 = {}
        keɓe = bytearray(원본); keɓe[0] = 0; 변형['BadMagic'] = keɓe
        keɓe = bytearray(원본); keɓe[7] = 61; 변형['BadVer'] = keɓe
        keɓe = bytearray(원본); keɓe[8:10] = b'\xff\xff'; 변형['BadPool'] = keɓe
        keɓe = bytearray(원본); keɓe[코드:코드 + njuuteendi_njaru] = bytes(njuuteendi_njaru)
        keɓe[코드:코드 + 3] = b'\xa7\x00\x01'; keɓe[코드 + njuuteendi_njaru - 1] = 177; 변형['BadJump'] = keɓe
        keɓe = bytearray(원본); keɓe[코드:코드 + njuuteendi_njaru] = bytes(njuuteendi_njaru)
        keɓe[코드] = 87; keɓe[코드 + njuuteendi_njaru - 1] = 177; 변형['BadStack'] = keɓe
        # innde 검사를 통과시켜 laatii_keɓe 실행 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        naatnugol_njaru = ['Imported.class=' + str(mooftordu_njaru / 'Imported.class'), 'Imported.java=' + str(sewnde)]
        for innde, keɓe in 변형.items():
            laawol = mooftordu_njaru / (innde + '.class'); laawol.write_bytes(keɓe)
            naatnugol_njaru.append(innde + '.class=' + str(laawol))
        seto_njaru = mooftordu_njaru / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / '도구/자바파일묶기.py'), '-o', str(seto_njaru)] + naatnugol_njaru, check=True)
        subprocess.run(['as', '--32', '-o', str(mooftordu_njaru / 'user.o'), str(위치 / '부팅/kuutoro.s')], cwd=str(mooftordu_njaru), check=True)
        aaluude_njaru = mooftordu_njaru / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/jokkere_lelngo.ld'), '-o', str(aaluude_njaru),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(mooftordu_njaru / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        기계 = 가상기계(aaluude_njaru, laylaytol_njaru=False)
        try:
            기계.ginol('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            기계.ginol('cat Imported.java', ['int[] values = new int[3]'])
            for innde, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                기계.ginol('java ' + innde, [문구, 'Exit: 1'])
                기계.ginol('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 기계.suurnal_winndande.decode('utf-8', 'replace')
        finally:
            기계.uddude()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = 해석.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
