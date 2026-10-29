#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ṣiṣẹ́_àṣẹ, ìkùnà_iye/ohun_àmúlò_iye 경계 시험."""
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
from 사용자통신시험 import àfojúunúṣe_maṣíìnì, 위치


def ṣàtúnṣe_iye(maṣíìnì, Orúkọ, Àkóónú_iye, Store_iye=True):
    Rọ́ọ̀nù = len(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
    maṣíìnì.직렬.sendall(('edit ' + Orúkọ + '\n').encode())
    maṣíìnì.기다림('...> ', Rọ́ọ̀nù)
    for ìlà in Àkóónú_iye.splitlines():
        assert len(ìlà) <= 128
        Rọ́ọ̀nù = len(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
        maṣíìnì.직렬.sendall((ìlà + '\n').encode())
        maṣíìnì.기다림('...> ', Rọ́ọ̀nù)
    Rọ́ọ̀nù = len(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
    maṣíìnì.직렬.sendall(b'.save\n' if Store_iye else b'.cancel\n')
    결과 = maṣíìnì.기다림('jkoros> ', Rọ́ọ̀nù)
    assert ('Saved:' if Store_iye else 'Cancelled; original preserved') in 결과, 결과


def fáìlì_àdírẹ́ẹ̀sì():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for ìlà in 결과.splitlines():
        if ìlà.endswith(' ram_files'):
            return int(ìlà.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def àlejò_fáìlì(maṣíìnì, ààyè_ìfàyọkàsí_iye, Ìwọ̀n, ọ̀nà):
    # 시험 VM의 메모리에서 gangan_détà 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    àdírẹ́ẹ̀sì = fáìlì_àdírẹ́ẹ̀sì() + ààyè_ìfàyọkàsí_iye * 16384
    maṣíìnì.aṣàfihàn_iye.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(àdírẹ́ẹ̀sì, Ìwọ̀n, ọ̀nà)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ọ̀nà.exists() and ọ̀nà.stat().st_size == Ìwọ̀n:
            return ọ̀nà.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Alásopọ̀_iye=False)
    결과 = {}
    try:
        maṣíìnì.Àṣẹ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        maṣíìnì.Àṣẹ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        maṣíìnì.Àṣẹ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        maṣíìnì.Àṣẹ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        maṣíìnì.Àṣẹ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        maṣíìnì.Àṣẹ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        maṣíìnì.Àṣẹ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Àkóónú_iye = '''public class Calc {
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
        ṣàtúnṣe_iye(maṣíìnì, 'Calc.java', Àkóónú_iye)
        maṣíìnì.Àṣẹ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = maṣíìnì.Àṣẹ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        ìgbéwọlé_Àtòkọ = maṣíìnì.Àṣẹ('ls', ['Calc.class'])
        Ìwọ̀n = int(re.search(r'Calc\.class\s+(\d+) bytes', ìgbéwọlé_Àtòkọ).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as àkójọpọ̀_fáìlì_iye:
            ọ̀nà = Path(àkójọpọ̀_fáìlì_iye) / 'Calc.class'
            détà = àlejò_fáìlì(maṣíìnì, 3, Ìwọ̀n, ọ̀nà)
            gangan_détà = subprocess.check_output(['java', '-Xverify:all', '-cp', àkójọpọ̀_fáìlì_iye, 'Calc', '6', 'guest'], universal_newlines=True)
            assert gangan_détà.splitlines() == 기대, gangan_détà
            결과['class_sha256'] = hashlib.sha256(détà).hexdigest()
            결과['openjdk_output'] = gangan_détà
        # 실패한 ṣàtúnṣe_iye/컴파일은 기존 class를 보존한다.
        ṣàtúnṣe_iye(maṣíìnì, 'Calc.java', 'not Java at all', Store_iye=False)
        maṣíìnì.Àṣẹ('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            ṣàtúnṣe_iye(maṣíìnì, 'Calc.java', 잘못)
            maṣíìnì.Àṣẹ('javac Calc.java', ['javac error:', 'Exit: 1'])
            maṣíìnì.Àṣẹ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # àṣetúnṣe_iye 실행은 aṣàmúlò 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            maṣíìnì.Àṣẹ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        maṣíìnì.Àṣẹ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        maṣíìnì.Àṣẹ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ṣàtúnṣe_iye(maṣíìnì, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        maṣíìnì.Àṣẹ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        maṣíìnì.Àṣẹ('java Calc', ['instruction limit', 'Exit: 1'])
        maṣíìnì.Àṣẹ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ṣàtúnṣe_iye(maṣíìnì, 'Bad.class', 'garbage')
        maṣíìnì.Àṣẹ('java Bad', ['JVM error:', 'Exit: 1'])
        maṣíìnì.Àṣẹ('rm Bad.class', ['Removed'])
        maṣíìnì.Àṣẹ('java Bad', ['cannot read class: -2'])
        # ṣàtúnṣe_iye 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Rọ́ọ̀nù = len(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
        maṣíìnì.직렬.sendall(b'edit Hello.java\n')
        maṣíìnì.기다림('...> ', Rọ́ọ̀nù)
        Rọ́ọ̀nù = len(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
        maṣíìnì.직렬.sendall(b'x' * 129 + b'\n')
        maṣíìnì.기다림('...> ', Rọ́ọ̀nù)
        maṣíìnì.Àṣẹ('.save', ['Too much input; original preserved'])
        maṣíìnì.Àṣẹ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ṣàtúnṣe_iye(maṣíìnì, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ṣàtúnṣe_iye(maṣíìnì, 'f' + str(수), 'occupied')
        maṣíìnì.Àṣẹ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        maṣíìnì.Àṣẹ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
        결과['serial'] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        maṣíìnì.Ti()


def 주코드(détà):
    """손상 시험용 main Code의 gangan_détà Fáìlì 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        iye = struct.unpack_from('>H', détà, 위치값)[0]
        위치값 += 2
        return iye
    def 정():
        nonlocal 위치값
        iye = struct.unpack_from('>I', détà, 위치값)[0]
        위치값 += 4
        return iye
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = détà[위치값]
        위치값 += 1
        if 종류 == 1:
            gígùn_iye = 짧()
            문자들[수] = détà[위치값:위치값 + gígùn_iye]
            위치값 += gígùn_iye
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Orúkọ = 짧()
        짧()
        for 수 in range(짧()):
            àwòmọ́_iye = 짧()
            Ìwọ̀n = 정()
            if 문자들[Orúkọ] == b'main' and 문자들[àwòmọ́_iye] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', détà, 위치값 + 4)[0]
            위치값 += Ìwọ̀n
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        àkójọpọ̀_fáìlì_iye = Path(임시)
        (àkójọpọ̀_fáìlì_iye / 'build').mkdir()
        orísun = àkójọpọ̀_fáìlì_iye / 'Imported.java'
        orísun.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(orísun)], check=True)
        원본 = (àkójọpọ̀_fáìlì_iye / 'Imported.class').read_bytes()
        코드, gígùn_iye = 주코드(원본)
        변형 = {}
        détà = bytearray(원본); détà[0] = 0; 변형['BadMagic'] = détà
        détà = bytearray(원본); détà[7] = 61; 변형['BadVer'] = détà
        détà = bytearray(원본); détà[8:10] = b'\xff\xff'; 변형['BadPool'] = détà
        détà = bytearray(원본); détà[코드:코드 + gígùn_iye] = bytes(gígùn_iye)
        détà[코드:코드 + 3] = b'\xa7\x00\x01'; détà[코드 + gígùn_iye - 1] = 177; 변형['BadJump'] = détà
        détà = bytearray(원본); détà[코드:코드 + gígùn_iye] = bytes(gígùn_iye)
        détà[코드] = 87; détà[코드 + gígùn_iye - 1] = 177; 변형['BadStack'] = détà
        # Orúkọ 검사를 통과시켜 gangan_détà ṣiṣẹ́_àṣẹ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ìgbéwọlé_iye = ['Imported.class=' + str(àkójọpọ̀_fáìlì_iye / 'Imported.class'), 'Imported.java=' + str(orísun)]
        for Orúkọ, détà in 변형.items():
            ọ̀nà = àkójọpọ̀_fáìlì_iye / (Orúkọ + '.class'); ọ̀nà.write_bytes(détà)
            ìgbéwọlé_iye.append(Orúkọ + '.class=' + str(ọ̀nà))
        Àjọṣe_iye = àkójọpọ̀_fáìlì_iye / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Àwọn_irinṣẹ́/자바파일묶기.py'), '-o', str(Àjọṣe_iye)] + ìgbéwọlé_iye, check=True)
        subprocess.run(['as', '--32', '-o', str(àkójọpọ̀_fáìlì_iye / 'user.o'), str(위치 / '부팅/aṣàmúlò.s')], cwd=str(àkójọpọ̀_fáìlì_iye), check=True)
        kánẹ́ẹ̀lì_iye = àkójọpọ̀_fáìlì_iye / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/ṣàsopọ̀_ètò_ìrísí.ld'), '-o', str(kánẹ́ẹ̀lì_iye),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(àkójọpọ̀_fáìlì_iye / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        maṣíìnì = àfojúunúṣe_maṣíìnì(kánẹ́ẹ̀lì_iye, Alásopọ̀_iye=False)
        try:
            maṣíìnì.Àṣẹ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            maṣíìnì.Àṣẹ('cat Imported.java', ['int[] values = new int[3]'])
            for Orúkọ, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                maṣíìnì.Àṣẹ('java ' + Orúkọ, [문구, 'Exit: 1'])
                maṣíìnì.Àṣẹ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
        finally:
            maṣíìnì.Ti()


if __name__ == '__main__':
    ìpínsíwẹ́wẹ́_iye = argparse.ArgumentParser()
    ìpínsíwẹ́wẹ́_iye.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ìpínsíwẹ́wẹ́_iye.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
