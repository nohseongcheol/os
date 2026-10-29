#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 실행, itigaqtuq_atuutilik/qarasaujalirijjutiit_atuutilik 경계 시험."""
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


def aaqqigiarli_atuutilik(기계, atiq, Ilulingit_atuutilik, tuqqurli_atuutilik=True):
    시작 = len(기계.papattivik_sanimukutaak)
    기계.직렬.sendall(('edit ' + atiq + '\n').encode())
    기계.기다림('...> ', 시작)
    for titikutaak in Ilulingit_atuutilik.splitlines():
        assert len(titikutaak) <= 128
        시작 = len(기계.papattivik_sanimukutaak)
        기계.직렬.sendall((titikutaak + '\n').encode())
        기계.기다림('...> ', 시작)
    시작 = len(기계.papattivik_sanimukutaak)
    기계.직렬.sendall(b'.save\n' if tuqqurli_atuutilik else b'.cancel\n')
    결과 = 기계.기다림('jkoros> ', 시작)
    assert ('Saved:' if tuqqurli_atuutilik else 'Cancelled; original preserved') in 결과, 결과


def ini_turaarut():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for titikutaak in 결과.splitlines():
        if titikutaak.endswith(' ram_files'):
            return int(titikutaak.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(기계, 슬롯, anininga, aqqut):
    # 시험 VM의 메모리에서 taannallarik_titiqqat 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    turaarut = ini_turaarut() + 슬롯 * 16384
    기계.qarasaujaup_saqqijaarutinga_atuutilik.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(turaarut, anininga, aqqut)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if aqqut.exists() and aqqut.stat().st_size == anininga:
            return aqqut.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Kasuqatigiitsimajut_atuutilik=False)
    결과 = {}
    try:
        기계.piqujijjut('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        기계.piqujijjut('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        기계.piqujijjut('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        기계.piqujijjut('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        기계.piqujijjut('java Missing', ['cannot read class: -2', 'Exit: 1'])
        기계.piqujijjut('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        기계.piqujijjut('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Ilulingit_atuutilik = '''public class Calc {
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
        aaqqigiarli_atuutilik(기계, 'Calc.java', Ilulingit_atuutilik)
        기계.piqujijjut('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = 기계.piqujijjut('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        Iliniku_Titiqpalliagaq = 기계.piqujijjut('ls', ['Calc.class'])
        anininga = int(re.search(r'Calc\.class\s+(\d+) bytes', Iliniku_Titiqpalliagaq).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as tukimuagutiit_atuutilik:
            aqqut = Path(tukimuagutiit_atuutilik) / 'Calc.class'
            titiqqat = 게스트파일(기계, 3, anininga, aqqut)
            taannallarik_titiqqat = subprocess.check_output(['java', '-Xverify:all', '-cp', tukimuagutiit_atuutilik, 'Calc', '6', 'guest'], universal_newlines=True)
            assert taannallarik_titiqqat.splitlines() == 기대, taannallarik_titiqqat
            결과['class_sha256'] = hashlib.sha256(titiqqat).hexdigest()
            결과['openjdk_output'] = taannallarik_titiqqat
        # 실패한 aaqqigiarli_atuutilik/컴파일은 기존 class를 보존한다.
        aaqqigiarli_atuutilik(기계, 'Calc.java', 'not Java at all', tuqqurli_atuutilik=False)
        기계.piqujijjut('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            aaqqigiarli_atuutilik(기계, 'Calc.java', 잘못)
            기계.piqujijjut('javac Calc.java', ['javac error:', 'Exit: 1'])
            기계.piqujijjut('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # utiqtaqtuq_atuutilik 실행은 atuqtuq 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            기계.piqujijjut('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        기계.piqujijjut('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        기계.piqujijjut('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        aaqqigiarli_atuutilik(기계, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        기계.piqujijjut('javac Calc.java', ['Compiled:', 'Exit: 0'])
        기계.piqujijjut('java Calc', ['instruction limit', 'Exit: 1'])
        기계.piqujijjut('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        aaqqigiarli_atuutilik(기계, 'Bad.class', 'garbage')
        기계.piqujijjut('java Bad', ['JVM error:', 'Exit: 1'])
        기계.piqujijjut('rm Bad.class', ['Removed'])
        기계.piqujijjut('java Bad', ['cannot read class: -2'])
        # aaqqigiarli_atuutilik 입력의 넘친 부분을 잘라서 저장하지 않는다.
        시작 = len(기계.papattivik_sanimukutaak)
        기계.직렬.sendall(b'edit Hello.java\n')
        기계.기다림('...> ', 시작)
        시작 = len(기계.papattivik_sanimukutaak)
        기계.직렬.sendall(b'x' * 129 + b'\n')
        기계.기다림('...> ', 시작)
        기계.piqujijjut('.save', ['Too much input; original preserved'])
        기계.piqujijjut('javac Hello.java', ['Compiled:', 'Exit: 0'])
        aaqqigiarli_atuutilik(기계, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            aaqqigiarli_atuutilik(기계, 'f' + str(수), 'occupied')
        기계.piqujijjut('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        기계.piqujijjut('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 기계.papattivik_sanimukutaak.decode('utf-8', 'replace')
        결과['serial'] = 기계.papattivik_sanimukutaak.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        기계.matuli()


def 주코드(titiqqat):
    """손상 시험용 main Code의 taannallarik_titiqqat ini 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        atuutilik = struct.unpack_from('>H', titiqqat, 위치값)[0]
        위치값 += 2
        return atuutilik
    def 정():
        nonlocal 위치값
        atuutilik = struct.unpack_from('>I', titiqqat, 위치값)[0]
        위치값 += 4
        return atuutilik
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = titiqqat[위치값]
        위치값 += 1
        if 종류 == 1:
            takininga_atuutilik = 짧()
            문자들[수] = titiqqat[위치값:위치값 + takininga_atuutilik]
            위치값 += takininga_atuutilik
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        atiq = 짧()
        짧()
        for 수 in range(짧()):
            piuluqqutit_atuutilik = 짧()
            anininga = 정()
            if 문자들[atiq] == b'main' and 문자들[piuluqqutit_atuutilik] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', titiqqat, 위치값 + 4)[0]
            위치값 += anininga
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        tukimuagutiit_atuutilik = Path(임시)
        (tukimuagutiit_atuutilik / 'build').mkdir()
        pivviujuq = tukimuagutiit_atuutilik / 'Imported.java'
        pivviujuq.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(pivviujuq)], check=True)
        원본 = (tukimuagutiit_atuutilik / 'Imported.class').read_bytes()
        코드, takininga_atuutilik = 주코드(원본)
        변형 = {}
        titiqqat = bytearray(원본); titiqqat[0] = 0; 변형['BadMagic'] = titiqqat
        titiqqat = bytearray(원본); titiqqat[7] = 61; 변형['BadVer'] = titiqqat
        titiqqat = bytearray(원본); titiqqat[8:10] = b'\xff\xff'; 변형['BadPool'] = titiqqat
        titiqqat = bytearray(원본); titiqqat[코드:코드 + takininga_atuutilik] = bytes(takininga_atuutilik)
        titiqqat[코드:코드 + 3] = b'\xa7\x00\x01'; titiqqat[코드 + takininga_atuutilik - 1] = 177; 변형['BadJump'] = titiqqat
        titiqqat = bytearray(원본); titiqqat[코드:코드 + takininga_atuutilik] = bytes(takininga_atuutilik)
        titiqqat[코드] = 87; titiqqat[코드 + takininga_atuutilik - 1] = 177; 변형['BadStack'] = titiqqat
        # atiq 검사를 통과시켜 taannallarik_titiqqat 실행 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        Iliniku_atuutilik = ['Imported.class=' + str(tukimuagutiit_atuutilik / 'Imported.class'), 'Imported.java=' + str(pivviujuq)]
        for atiq, titiqqat in 변형.items():
            aqqut = tukimuagutiit_atuutilik / (atiq + '.class'); aqqut.write_bytes(titiqqat)
            Iliniku_atuutilik.append(atiq + '.class=' + str(aqqut))
        katinngajut_atuutilik = tukimuagutiit_atuutilik / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / '도구/자바파일묶기.py'), '-o', str(katinngajut_atuutilik)] + Iliniku_atuutilik, check=True)
        subprocess.run(['as', '--32', '-o', str(tukimuagutiit_atuutilik / 'user.o'), str(위치 / '부팅/atuqtuq.s')], cwd=str(tukimuagutiit_atuutilik), check=True)
        kernel_atuutilik = tukimuagutiit_atuutilik / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/kasurvik_ilinganinga.ld'), '-o', str(kernel_atuutilik),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(tukimuagutiit_atuutilik / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        기계 = 가상기계(kernel_atuutilik, Kasuqatigiitsimajut_atuutilik=False)
        try:
            기계.piqujijjut('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            기계.piqujijjut('cat Imported.java', ['int[] values = new int[3]'])
            for atiq, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                기계.piqujijjut('java ' + atiq, [문구, 'Exit: 1'])
                기계.piqujijjut('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 기계.papattivik_sanimukutaak.decode('utf-8', 'replace')
        finally:
            기계.matuli()


if __name__ == '__main__':
    agguqtuut_atuutilik = argparse.ArgumentParser()
    agguqtuut_atuutilik.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = agguqtuut_atuutilik.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
