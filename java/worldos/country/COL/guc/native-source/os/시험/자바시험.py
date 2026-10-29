#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 실행, ajachitia_ajutuu/ama_anaajatü_ajutuu 경계 시험."""
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


def anaataa_ajutuu(기계, 이름, alu_ujatüü_ajutuu, 저장=True):
    시작 = len(기계.aa_innachikimaajatü_aparatsee)
    기계.직렬.sendall(('edit ' + 이름 + '\n').encode())
    기계.기다림('...> ', 시작)
    for liinia in alu_ujatüü_ajutuu.splitlines():
        assert len(liinia) <= 128
        시작 = len(기계.aa_innachikimaajatü_aparatsee)
        기계.직렬.sendall((liinia + '\n').encode())
        기계.기다림('...> ', 시작)
    시작 = len(기계.aa_innachikimaajatü_aparatsee)
    기계.직렬.sendall(b'.save\n' if 저장 else b'.cancel\n')
    결과 = 기계.기다림('jkoros> ', 시작)
    assert ('Saved:' if 저장 else 'Cancelled; original preserved') in 결과, 결과


def anaajaalaa_ejepüsee():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for liinia in 결과.splitlines():
        if liinia.endswith(' ram_files'):
            return int(liinia.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(기계, 슬롯, 크기, wopu_a_ttaaleemüin):
    # 시험 VM의 메모리에서 실제 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ejepüsee = anaajaalaa_ejepüsee() + 슬롯 * 16384
    기계.anajia_ajutuu.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ejepüsee, 크기, wopu_a_ttaaleemüin)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if wopu_a_ttaaleemüin.exists() and wopu_a_ttaaleemüin.stat().st_size == 크기:
            return wopu_a_ttaaleemüin.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, kusu_ajutuu=False)
    결과 = {}
    try:
        기계.aluwataaya('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        기계.aluwataaya('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        기계.aluwataaya('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        기계.aluwataaya('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        기계.aluwataaya('java Missing', ['cannot read class: -2', 'Exit: 1'])
        기계.aluwataaya('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        기계.aluwataaya('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        alu_ujatüü_ajutuu = '''public class Calc {
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
        anaataa_ajutuu(기계, 'Calc.java', alu_ujatüü_ajutuu)
        기계.aluwataaya('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = 기계.aluwataaya('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        목록 = 기계.aluwataaya('ls', ['Calc.class'])
        크기 = int(re.search(r'Calc\.class\s+(\d+) bytes', 목록).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as anaajaalee_ajutuu:
            wopu_a_ttaaleemüin = Path(anaajaalee_ajutuu) / 'Calc.class'
            atijaaya = 게스트파일(기계, 3, 크기, wopu_a_ttaaleemüin)
            실제 = subprocess.check_output(['java', '-Xverify:all', '-cp', anaajaalee_ajutuu, 'Calc', '6', 'guest'], universal_newlines=True)
            assert 실제.splitlines() == 기대, 실제
            결과['class_sha256'] = hashlib.sha256(atijaaya).hexdigest()
            결과['openjdk_output'] = 실제
        # 실패한 anaataa_ajutuu/컴파일은 기존 class를 보존한다.
        anaataa_ajutuu(기계, 'Calc.java', 'not Java at all', 저장=False)
        기계.aluwataaya('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            anaataa_ajutuu(기계, 'Calc.java', 잘못)
            기계.aluwataaya('javac Calc.java', ['javac error:', 'Exit: 1'])
            기계.aluwataaya('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # a_lakaa_ajutuu 실행은 ka_yataayakalü 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            기계.aluwataaya('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        기계.aluwataaya('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        기계.aluwataaya('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        anaataa_ajutuu(기계, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        기계.aluwataaya('javac Calc.java', ['Compiled:', 'Exit: 0'])
        기계.aluwataaya('java Calc', ['instruction limit', 'Exit: 1'])
        기계.aluwataaya('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        anaataa_ajutuu(기계, 'Bad.class', 'garbage')
        기계.aluwataaya('java Bad', ['JVM error:', 'Exit: 1'])
        기계.aluwataaya('rm Bad.class', ['Removed'])
        기계.aluwataaya('java Bad', ['cannot read class: -2'])
        # anaataa_ajutuu 입력의 넘친 부분을 잘라서 저장하지 않는다.
        시작 = len(기계.aa_innachikimaajatü_aparatsee)
        기계.직렬.sendall(b'edit Hello.java\n')
        기계.기다림('...> ', 시작)
        시작 = len(기계.aa_innachikimaajatü_aparatsee)
        기계.직렬.sendall(b'x' * 129 + b'\n')
        기계.기다림('...> ', 시작)
        기계.aluwataaya('.save', ['Too much input; original preserved'])
        기계.aluwataaya('javac Hello.java', ['Compiled:', 'Exit: 0'])
        anaataa_ajutuu(기계, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            anaataa_ajutuu(기계, 'f' + str(수), 'occupied')
        기계.aluwataaya('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        기계.aluwataaya('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 기계.aa_innachikimaajatü_aparatsee.decode('utf-8', 'replace')
        결과['serial'] = 기계.aa_innachikimaajatü_aparatsee.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        기계.asürülaa()


def 주코드(atijaaya):
    """손상 시험용 main Code의 실제 anaajaalaa 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        ajutuu = struct.unpack_from('>H', atijaaya, 위치값)[0]
        위치값 += 2
        return ajutuu
    def 정():
        nonlocal 위치값
        ajutuu = struct.unpack_from('>I', atijaaya, 위치값)[0]
        위치값 += 4
        return ajutuu
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = atijaaya[위치값]
        위치값 += 1
        if 종류 == 1:
            akaliaa_ajutuu = 짧()
            문자들[수] = atijaaya[위치값:위치값 + akaliaa_ajutuu]
            위치값 += akaliaa_ajutuu
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        이름 = 짧()
        짧()
        for 수 in range(짧()):
            anaajaalaakua_ipa_ajutuu = 짧()
            크기 = 정()
            if 문자들[이름] == b'main' and 문자들[anaajaalaakua_ipa_ajutuu] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', atijaaya, 위치값 + 4)[0]
            위치값 += 크기
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        anaajaalee_ajutuu = Path(임시)
        (anaajaalee_ajutuu / 'build').mkdir()
        eejeejetülein = anaajaalee_ajutuu / 'Imported.java'
        eejeejetülein.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(eejeejetülein)], check=True)
        원본 = (anaajaalee_ajutuu / 'Imported.class').read_bytes()
        코드, akaliaa_ajutuu = 주코드(원본)
        변형 = {}
        atijaaya = bytearray(원본); atijaaya[0] = 0; 변형['BadMagic'] = atijaaya
        atijaaya = bytearray(원본); atijaaya[7] = 61; 변형['BadVer'] = atijaaya
        atijaaya = bytearray(원본); atijaaya[8:10] = b'\xff\xff'; 변형['BadPool'] = atijaaya
        atijaaya = bytearray(원본); atijaaya[코드:코드 + akaliaa_ajutuu] = bytes(akaliaa_ajutuu)
        atijaaya[코드:코드 + 3] = b'\xa7\x00\x01'; atijaaya[코드 + akaliaa_ajutuu - 1] = 177; 변형['BadJump'] = atijaaya
        atijaaya = bytearray(원본); atijaaya[코드:코드 + akaliaa_ajutuu] = bytes(akaliaa_ajutuu)
        atijaaya[코드] = 87; atijaaya[코드 + akaliaa_ajutuu - 1] = 177; 변형['BadStack'] = atijaaya
        # 이름 검사를 통과시켜 실제 실행 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ekeroliaa_ajutuu = ['Imported.class=' + str(anaajaalee_ajutuu / 'Imported.class'), 'Imported.java=' + str(eejeejetülein)]
        for 이름, atijaaya in 변형.items():
            wopu_a_ttaaleemüin = anaajaalee_ajutuu / (이름 + '.class'); wopu_a_ttaaleemüin.write_bytes(atijaaya)
            ekeroliaa_ajutuu.append(이름 + '.class=' + str(wopu_a_ttaaleemüin))
        akotchijuushi_ajutuu = anaajaalee_ajutuu / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / '도구/자바파일묶기.py'), '-o', str(akotchijuushi_ajutuu)] + ekeroliaa_ajutuu, check=True)
        subprocess.run(['as', '--32', '-o', str(anaajaalee_ajutuu / 'user.o'), str(위치 / '부팅/ka_yataayakalü.s')], cwd=str(anaajaalee_ajutuu), check=True)
        keetnerü_ajutuu = anaajaalee_ajutuu / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/wopu_akumajiakuai_pa.ld'), '-o', str(keetnerü_ajutuu),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(anaajaalee_ajutuu / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        기계 = 가상기계(keetnerü_ajutuu, kusu_ajutuu=False)
        try:
            기계.aluwataaya('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            기계.aluwataaya('cat Imported.java', ['int[] values = new int[3]'])
            for 이름, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                기계.aluwataaya('java ' + 이름, [문구, 'Exit: 1'])
                기계.aluwataaya('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 기계.aa_innachikimaajatü_aparatsee.decode('utf-8', 'replace')
        finally:
            기계.asürülaa()


if __name__ == '__main__':
    akatajaa_ajutuu = argparse.ArgumentParser()
    akatajaa_ajutuu.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = akatajaa_ajutuu.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
