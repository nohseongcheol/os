#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 실행, پاتېينه_ارزښت/سرچينه_ارزښت 경계 시험."""
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
from 사용자통신시험 import 가상기계, ځای


def سمون_ارزښت(기계, نوم, منځپانګه_ارزښت, 저장=True):
    ځغلول = len(기계.خبرال_کیل)
    기계.직렬.sendall(('edit ' + نوم + '\n').encode())
    기계.기다림('...> ', ځغلول)
    for ليکه in منځپانګه_ارزښت.splitlines():
        assert len(ليکه) <= 128
        ځغلول = len(기계.خبرال_کیل)
        기계.직렬.sendall((ليکه + '\n').encode())
        기계.기다림('...> ', ځغلول)
    ځغلول = len(기계.خبرال_کیل)
    기계.직렬.sendall(b'.save\n' if 저장 else b'.cancel\n')
    결과 = 기계.기다림('jkoros> ', ځغلول)
    assert ('Saved:' if 저장 else 'Cancelled; original preserved') in 결과, 결과


def دوتنه_پته():
    결과 = subprocess.check_output(['nm', '-n', str(ځای / 'build/kernel.elf')], universal_newlines=True)
    for ليکه in 결과.splitlines():
        if ليکه.endswith(' ram_files'):
            return int(ليکه.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(기계, 슬롯, کچ, يونلور):
    # 시험 VM의 메모리에서 실제 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    پته = دوتنه_پته() + 슬롯 * 16384
    기계.ليدانى_ارزښت.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(پته, کچ, يونلور)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if يونلور.exists() and يونلور.stat().st_size == کچ:
            return يونلور.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    기계 = 가상기계(ځای / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, جال_ارزښت=False)
    결과 = {}
    try:
        기계.بولۍ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        기계.بولۍ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        기계.بولۍ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        기계.بولۍ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        기계.بولۍ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        기계.بولۍ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        기계.بولۍ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        منځپانګه_ارزښت = '''public class Calc {
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
        سمون_ارزښت(기계, 'Calc.java', منځپانګه_ارزښت)
        기계.بولۍ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = 기계.بولۍ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        목록 = 기계.بولۍ('ls', ['Calc.class'])
        کچ = int(re.search(r'Calc\.class\s+(\d+) bytes', 목록).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as نوملړ_ارزښت:
            يونلور = Path(نوملړ_ارزښت) / 'Calc.class'
            اومتوک = 게스트파일(기계, 3, کچ, يونلور)
            실제 = subprocess.check_output(['java', '-Xverify:all', '-cp', نوملړ_ارزښت, 'Calc', '6', 'guest'], universal_newlines=True)
            assert 실제.splitlines() == 기대, 실제
            결과['class_sha256'] = hashlib.sha256(اومتوک).hexdigest()
            결과['openjdk_output'] = 실제
        # 실패한 سمون_ارزښت/컴파일은 기존 class를 보존한다.
        سمون_ارزښت(기계, 'Calc.java', 'not Java at all', 저장=False)
        기계.بولۍ('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            سمون_ارزښت(기계, 'Calc.java', 잘못)
            기계.بولۍ('javac Calc.java', ['javac error:', 'Exit: 1'])
            기계.بولۍ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # تکرار_ارزښت 실행은 کارن 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            기계.بولۍ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        기계.بولۍ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        기계.بولۍ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        سمون_ارزښت(기계, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        기계.بولۍ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        기계.بولۍ('java Calc', ['instruction limit', 'Exit: 1'])
        기계.بولۍ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        سمون_ارزښت(기계, 'Bad.class', 'garbage')
        기계.بولۍ('java Bad', ['JVM error:', 'Exit: 1'])
        기계.بولۍ('rm Bad.class', ['Removed'])
        기계.بولۍ('java Bad', ['cannot read class: -2'])
        # سمون_ارزښت 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ځغلول = len(기계.خبرال_کیل)
        기계.직렬.sendall(b'edit Hello.java\n')
        기계.기다림('...> ', ځغلول)
        ځغلول = len(기계.خبرال_کیل)
        기계.직렬.sendall(b'x' * 129 + b'\n')
        기계.기다림('...> ', ځغلول)
        기계.بولۍ('.save', ['Too much input; original preserved'])
        기계.بولۍ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        سمون_ارزښت(기계, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            سمون_ارزښت(기계, 'f' + str(수), 'occupied')
        기계.بولۍ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        기계.بولۍ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 기계.خبرال_کیل.decode('utf-8', 'replace')
        결과['serial'] = 기계.خبرال_کیل.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        기계.بندول()


def 주코드(اومتوک):
    """손상 시험용 main Code의 실제 دوتنه 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        ارزښت = struct.unpack_from('>H', اومتوک, 위치값)[0]
        위치값 += 2
        return ارزښت
    def 정():
        nonlocal 위치값
        ارزښت = struct.unpack_from('>I', اومتوک, 위치값)[0]
        위치값 += 4
        return ارزښت
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = اومتوک[위치값]
        위치값 += 1
        if 종류 == 1:
            اوږدوالى_ارزښت = 짧()
            문자들[수] = اومتوک[위치값:위치값 + اوږدوالى_ارزښت]
            위치값 += اوږدوالى_ارزښت
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        نوم = 짧()
        짧()
        for 수 in range(짧()):
            ځانتیا_ارزښت = 짧()
            کچ = 정()
            if 문자들[نوم] == b'main' and 문자들[ځانتیا_ارزښت] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', اومتوک, 위치값 + 4)[0]
            위치값 += کچ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        نوملړ_ارزښت = Path(임시)
        (نوملړ_ارزښت / 'build').mkdir()
        سرچينه = نوملړ_ارزښت / 'Imported.java'
        سرچينه.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(سرچينه)], check=True)
        원본 = (نوملړ_ارزښت / 'Imported.class').read_bytes()
        코드, اوږدوالى_ارزښت = 주코드(원본)
        변형 = {}
        اومتوک = bytearray(원본); اومتوک[0] = 0; 변형['BadMagic'] = اومتوک
        اومتوک = bytearray(원본); اومتوک[7] = 61; 변형['BadVer'] = اومتوک
        اومتوک = bytearray(원본); اومتوک[8:10] = b'\xff\xff'; 변형['BadPool'] = اومتوک
        اومتوک = bytearray(원본); اومتوک[코드:코드 + اوږدوالى_ارزښت] = bytes(اوږدوالى_ارزښت)
        اومتوک[코드:코드 + 3] = b'\xa7\x00\x01'; اومتوک[코드 + اوږدوالى_ارزښت - 1] = 177; 변형['BadJump'] = اومتوک
        اومتوک = bytearray(원본); اومتوک[코드:코드 + اوږدوالى_ارزښت] = bytes(اوږدوالى_ارزښت)
        اومتوک[코드] = 87; اومتوک[코드 + اوږدوالى_ارزښت - 1] = 177; 변형['BadStack'] = اومتوک
        # نوم 검사를 통과시켜 실제 실행 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ننوت_ارزښت = ['Imported.class=' + str(نوملړ_ارزښت / 'Imported.class'), 'Imported.java=' + str(سرچينه)]
        for نوم, اومتوک in 변형.items():
            يونلور = نوملړ_ارزښت / (نوم + '.class'); يونلور.write_bytes(اومتوک)
            ننوت_ارزښت.append(نوم + '.class=' + str(يونلور))
        ډله_ارزښت = نوملړ_ارزښت / 'build/java-files.bin'
        subprocess.run([sys.executable, str(ځای / '도구/자바파일묶기.py'), '-o', str(ډله_ارزښت)] + ننوت_ارزښت, check=True)
        subprocess.run(['as', '--32', '-o', str(نوملړ_ارزښت / 'user.o'), str(ځای / '부팅/کارن.s')], cwd=str(نوملړ_ارزښت), check=True)
        نوغی_ارزښت = نوملړ_ارزښت / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ځای / '부팅/پيوند_هډوانه.ld'), '-o', str(نوغی_ارزښت),
                        str(ځای / 'build/boot.o'), str(ځای / 'build/java.o'), str(نوملړ_ارزښت / 'user.o'), str(ځای / 'build/apps.o')], check=True)
        기계 = 가상기계(نوغی_ارزښت, جال_ارزښت=False)
        try:
            기계.بولۍ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            기계.بولۍ('cat Imported.java', ['int[] values = new int[3]'])
            for نوم, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                기계.بولۍ('java ' + نوم, [문구, 'Exit: 1'])
                기계.بولۍ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 기계.خبرال_کیل.decode('utf-8', 'replace')
        finally:
            기계.بندول()


if __name__ == '__main__':
    تجزیه_ارزښت = argparse.ArgumentParser()
    تجزیه_ارزښت.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = تجزیه_ارزښت.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (ځای / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
