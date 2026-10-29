#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ක්_රියාත්මක_කරන්න_විධානය, අසමත්වීම_අගය/සම්පත_අගය 경계 시험."""
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
from 사용자통신시험 import අතථ්_ය_යන්ත්_රය, පිහිටීම


def සකසන්න_අගය(යන්ත්_රය, නම, අන්තර්ගතය_අගය, ගබඩා_කරන්න_අගය=True):
    ක්_රියාත්මක_කරන්න_2 = len(යන්ත්_රය.ලොගය_පේළිය)
    යන්ත්_රය.직렬.sendall(('edit ' + නම + '\n').encode())
    යන්ත්_රය.기다림('...> ', ක්_රියාත්මක_කරන්න_2)
    for පේළිය in අන්තර්ගතය_අගය.splitlines():
        assert len(පේළිය) <= 128
        ක්_රියාත්මක_කරන්න_2 = len(යන්ත්_රය.ලොගය_පේළිය)
        යන්ත්_රය.직렬.sendall((පේළිය + '\n').encode())
        යන්ත්_රය.기다림('...> ', ක්_රියාත්මක_කරන්න_2)
    ක්_රියාත්මක_කරන්න_2 = len(යන්ත්_රය.ලොගය_පේළිය)
    යන්ත්_රය.직렬.sendall(b'.save\n' if ගබඩා_කරන්න_අගය else b'.cancel\n')
    결과 = යන්ත්_රය.기다림('jkoros> ', ක්_රියාත්මක_කරන්න_2)
    assert ('Saved:' if ගබඩා_කරන්න_අගය else 'Cancelled; original preserved') in 결과, 결과


def ගොනුව_යොමුව():
    결과 = subprocess.check_output(['nm', '-n', str(පිහිටීම / 'build/kernel.elf')], universal_newlines=True)
    for පේළිය in 결과.splitlines():
        if පේළිය.endswith(' ram_files'):
            return int(පේළිය.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def අමුත්තා_ගොනුව(යන්ත්_රය, විවරය_අගය, ප්_රමාණය, මාර්_ගය):
    # 시험 VM의 메모리에서 තථ්_ය_දත්ත 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    යොමුව = ගොනුව_යොමුව() + විවරය_අගය * 16384
    යන්ත්_රය.මොනිටරය_අගය.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(යොමුව, ප්_රමාණය, මාර්_ගය)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if මාර්_ගය.exists() and මාර්_ගය.stat().st_size == ප්_රමාණය:
            return මාර්_ගය.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ජාලය_අගය=False)
    결과 = {}
    try:
        යන්ත්_රය.විධානය('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        යන්ත්_රය.විධානය('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        යන්ත්_රය.විධානය('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        යන්ත්_රය.විධානය('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        යන්ත්_රය.විධානය('java Missing', ['cannot read class: -2', 'Exit: 1'])
        යන්ත්_රය.විධානය('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        යන්ත්_රය.විධානය('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        අන්තර්ගතය_අගය = '''public class Calc {
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
        සකසන්න_අගය(යන්ත්_රය, 'Calc.java', අන්තර්ගතය_අගය)
        යන්ත්_රය.විධානය('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = යන්ත්_රය.විධානය('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        පිවිසුම_ලැයිස්තුව = යන්ත්_රය.විධානය('ls', ['Calc.class'])
        ප්_රමාණය = int(re.search(r'Calc\.class\s+(\d+) bytes', පිවිසුම_ලැයිස්තුව).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as නාමාවලිය_අගය:
            මාර්_ගය = Path(නාමාවලිය_අගය) / 'Calc.class'
            දත්ත = අමුත්තා_ගොනුව(යන්ත්_රය, 3, ප්_රමාණය, මාර්_ගය)
            තථ්_ය_දත්ත = subprocess.check_output(['java', '-Xverify:all', '-cp', නාමාවලිය_අගය, 'Calc', '6', 'guest'], universal_newlines=True)
            assert තථ්_ය_දත්ත.splitlines() == 기대, තථ්_ය_දත්ත
            결과['class_sha256'] = hashlib.sha256(දත්ත).hexdigest()
            결과['openjdk_output'] = තථ්_ය_දත්ත
        # 실패한 සකසන්න_අගය/컴파일은 기존 class를 보존한다.
        සකසන්න_අගය(යන්ත්_රය, 'Calc.java', 'not Java at all', ගබඩා_කරන්න_අගය=False)
        යන්ත්_රය.විධානය('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            සකසන්න_අගය(යන්ත්_රය, 'Calc.java', 잘못)
            යන්ත්_රය.විධානය('javac Calc.java', ['javac error:', 'Exit: 1'])
            යන්ත්_රය.විධානය('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # පුනර්කරණය_අගය 실행은 පරිශීලක 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            යන්ත්_රය.විධානය('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        යන්ත්_රය.විධානය('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        යන්ත්_රය.විධානය('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        සකසන්න_අගය(යන්ත්_රය, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        යන්ත්_රය.විධානය('javac Calc.java', ['Compiled:', 'Exit: 0'])
        යන්ත්_රය.විධානය('java Calc', ['instruction limit', 'Exit: 1'])
        යන්ත්_රය.විධානය('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        සකසන්න_අගය(යන්ත්_රය, 'Bad.class', 'garbage')
        යන්ත්_රය.විධානය('java Bad', ['JVM error:', 'Exit: 1'])
        යන්ත්_රය.විධානය('rm Bad.class', ['Removed'])
        යන්ත්_රය.විධානය('java Bad', ['cannot read class: -2'])
        # සකසන්න_අගය 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ක්_රියාත්මක_කරන්න_2 = len(යන්ත්_රය.ලොගය_පේළිය)
        යන්ත්_රය.직렬.sendall(b'edit Hello.java\n')
        යන්ත්_රය.기다림('...> ', ක්_රියාත්මක_කරන්න_2)
        ක්_රියාත්මක_කරන්න_2 = len(යන්ත්_රය.ලොගය_පේළිය)
        යන්ත්_රය.직렬.sendall(b'x' * 129 + b'\n')
        යන්ත්_රය.기다림('...> ', ක්_රියාත්මක_කරන්න_2)
        යන්ත්_රය.විධානය('.save', ['Too much input; original preserved'])
        යන්ත්_රය.විධානය('javac Hello.java', ['Compiled:', 'Exit: 0'])
        සකසන්න_අගය(යන්ත්_රය, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            සකසන්න_අගය(යන්ත්_රය, 'f' + str(수), 'occupied')
        යන්ත්_රය.විධානය('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        යන්ත්_රය.විධානය('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
        결과['serial'] = යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        යන්ත්_රය.වසන්න()


def 주코드(දත්ත):
    """손상 시험용 main Code의 තථ්_ය_දත්ත ගොනු 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        අගය = struct.unpack_from('>H', දත්ත, 위치값)[0]
        위치값 += 2
        return අගය
    def 정():
        nonlocal 위치값
        අගය = struct.unpack_from('>I', දත්ත, 위치값)[0]
        위치값 += 4
        return අගය
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = දත්ත[위치값]
        위치값 += 1
        if 종류 == 1:
            දිග_අගය = 짧()
            문자들[수] = දත්ත[위치값:위치값 + දිග_අගය]
            위치값 += දිග_අගය
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        නම = 짧()
        짧()
        for 수 in range(짧()):
            ගුණාංගය_අගය = 짧()
            ප්_රමාණය = 정()
            if 문자들[නම] == b'main' and 문자들[ගුණාංගය_අගය] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', දත්ත, 위치값 + 4)[0]
            위치값 += ප්_රමාණය
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        නාමාවලිය_අගය = Path(임시)
        (නාමාවලිය_අගය / 'build').mkdir()
        මූලය = නාමාවලිය_අගය / 'Imported.java'
        මූලය.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(මූලය)], check=True)
        원본 = (නාමාවලිය_අගය / 'Imported.class').read_bytes()
        코드, දිග_අගය = 주코드(원본)
        변형 = {}
        දත්ත = bytearray(원본); දත්ත[0] = 0; 변형['BadMagic'] = දත්ත
        දත්ත = bytearray(원본); දත්ත[7] = 61; 변형['BadVer'] = දත්ත
        දත්ත = bytearray(원본); දත්ත[8:10] = b'\xff\xff'; 변형['BadPool'] = දත්ත
        දත්ත = bytearray(원본); දත්ත[코드:코드 + දිග_අගය] = bytes(දිග_අගය)
        දත්ත[코드:코드 + 3] = b'\xa7\x00\x01'; දත්ත[코드 + දිග_අගය - 1] = 177; 변형['BadJump'] = දත්ත
        දත්ත = bytearray(원본); දත්ත[코드:코드 + දිග_අගය] = bytes(දිග_අගය)
        දත්ත[코드] = 87; දත්ත[코드 + දිග_අගය - 1] = 177; 변형['BadStack'] = දත්ත
        # නම 검사를 통과시켜 තථ්_ය_දත්ත ක්_රියාත්මක_කරන්න_විධානය 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        පිවිසුම_අගය = ['Imported.class=' + str(නාමාවලිය_අගය / 'Imported.class'), 'Imported.java=' + str(මූලය)]
        for නම, දත්ත in 변형.items():
            මාර්_ගය = නාමාවලිය_අගය / (නම + '.class'); මාර්_ගය.write_bytes(දත්ත)
            පිවිසුම_අගය.append(නම + '.class=' + str(මාර්_ගය))
        සමූහය_අගය = නාමාවලිය_අගය / 'build/java-files.bin'
        subprocess.run([sys.executable, str(පිහිටීම / 'මෙවලම්/자바파일묶기.py'), '-o', str(සමූහය_අගය)] + පිවිසුම_අගය, check=True)
        subprocess.run(['as', '--32', '-o', str(නාමාවලිය_අගය / 'user.o'), str(පිහිටීම / '부팅/පරිශීලක.s')], cwd=str(නාමාවලිය_අගය), check=True)
        කර්නලය_අගය = නාමාවලිය_අගය / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(පිහිටීම / '부팅/සබැඳිය_සැකැස්ම.ld'), '-o', str(කර්නලය_අගය),
                        str(පිහිටීම / 'build/boot.o'), str(පිහිටීම / 'build/java.o'), str(නාමාවලිය_අගය / 'user.o'), str(පිහිටීම / 'build/apps.o')], check=True)
        යන්ත්_රය = අතථ්_ය_යන්ත්_රය(කර්නලය_අගය, ජාලය_අගය=False)
        try:
            යන්ත්_රය.විධානය('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            යන්ත්_රය.විධානය('cat Imported.java', ['int[] values = new int[3]'])
            for නම, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                යන්ත්_රය.විධානය('java ' + නම, [문구, 'Exit: 1'])
                යන්ත්_රය.විධානය('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
        finally:
            යන්ත්_රය.වසන්න()


if __name__ == '__main__':
    විශ්ලේෂණය_කරන්න_අගය = argparse.ArgumentParser()
    විශ්ලේෂණය_කරන්න_අගය.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    විස්තාරක = විශ්ලේෂණය_කරන්න_අගය.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if විස්තාරක.boot == 'both' else (විස්තාරක.boot,))}
    결과['import'] = 적재시험()
    (පිහිටීම / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
