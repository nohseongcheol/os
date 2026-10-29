#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ಪೂರೈಸು_ಆದೇಶ, ವೈಫಲ್ಯ_ಮೌಲ್ಯ/ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ 경계 시험."""
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
from 사용자통신시험 import ಅಗೋಚರ_ಯಂತ್ರ, ಸ್ಥಾನ


def ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, ಹೆಸರು, ವಿಷಯ_ಮೌಲ್ಯ, ಸ್ಟೋರ್_ಮೌಲ್ಯ=True):
    ಚಲಾಯಿಸು_2 = len(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
    ಯಂತ್ರ.직렬.sendall(('edit ' + ಹೆಸರು + '\n').encode())
    ಯಂತ್ರ.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('...> ', ಚಲಾಯಿಸು_2)
    for ಸಾಲು in ವಿಷಯ_ಮೌಲ್ಯ.splitlines():
        assert len(ಸಾಲು) <= 128
        ಚಲಾಯಿಸು_2 = len(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
        ಯಂತ್ರ.직렬.sendall((ಸಾಲು + '\n').encode())
        ಯಂತ್ರ.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('...> ', ಚಲಾಯಿಸು_2)
    ಚಲಾಯಿಸು_2 = len(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
    ಯಂತ್ರ.직렬.sendall(b'.save\n' if ಸ್ಟೋರ್_ಮೌಲ್ಯ else b'.cancel\n')
    ಮಾಪನ = ಯಂತ್ರ.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('jkoros> ', ಚಲಾಯಿಸು_2)
    assert ('Saved:' if ಸ್ಟೋರ್_ಮೌಲ್ಯ else 'Cancelled; original preserved') in ಮಾಪನ, ಮಾಪನ


def ಫೈಲ್_ಇಮೇಲ್():
    ಮಾಪನ = subprocess.check_output(['nm', '-n', str(ಸ್ಥಾನ / 'build/kernel.elf')], universal_newlines=True)
    for ಸಾಲು in ಮಾಪನ.splitlines():
        if ಸಾಲು.endswith(' ram_files'):
            return int(ಸಾಲು.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ಅತಿಥಿ_ಫೈಲ್(ಯಂತ್ರ, ಸ್ಲಾಟ್_ಮೌಲ್ಯ, ಗಾತ್ರ, ಮಾರ್ಗ):
    # 시험 VM의 메모리에서 ನಿಜವಾದ_ಡೇಟಾ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ಇಮೇಲ್ = ಫೈಲ್_ಇಮೇಲ್() + ಸ್ಲಾಟ್_ಮೌಲ್ಯ * 16384
    ಯಂತ್ರ.ಮಾನಿಟರ್_ಮೌಲ್ಯ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ಇಮೇಲ್, ಗಾತ್ರ, ಮಾರ್ಗ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ಮಾರ್ಗ.exists() and ಮಾರ್ಗ.stat().st_size == ಗಾತ್ರ:
            return ಮಾರ್ಗ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ನೆಟ್_ವರ್ಕ್_ಮೌಲ್ಯ=False)
    ಮಾಪನ = {}
    try:
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ವಿಷಯ_ಮೌಲ್ಯ = '''public class Calc {
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
        ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'Calc.java', ವಿಷಯ_ಮೌಲ್ಯ)
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        ಔಟ್_ಪುಟ್ = ಯಂತ್ರ.ಆಜ್ಞೆ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ಮಾಪನ['guest_output'] = ಔಟ್_ಪುಟ್
        ನಮೂದು_ಪಟ್ಟಿ = ಯಂತ್ರ.ಆಜ್ಞೆ('ls', ['Calc.class'])
        ಗಾತ್ರ = int(re.search(r'Calc\.class\s+(\d+) bytes', ನಮೂದು_ಪಟ್ಟಿ).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ:
            ಮಾರ್ಗ = Path(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ) / 'Calc.class'
            ಡೇಟಾ = ಅತಿಥಿ_ಫೈಲ್(ಯಂತ್ರ, 3, ಗಾತ್ರ, ಮಾರ್ಗ)
            ನಿಜವಾದ_ಡೇಟಾ = subprocess.check_output(['java', '-Xverify:all', '-cp', ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ನಿಜವಾದ_ಡೇಟಾ.splitlines() == 기대, ನಿಜವಾದ_ಡೇಟಾ
            ಮಾಪನ['class_sha256'] = hashlib.sha256(ಡೇಟಾ).hexdigest()
            ಮಾಪನ['openjdk_output'] = ನಿಜವಾದ_ಡೇಟಾ
        # 실패한 ಸಂಪಾದನೆ_ಮೌಲ್ಯ/컴파일은 기존 class를 보존한다.
        ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'Calc.java', 'not Java at all', ಸ್ಟೋರ್_ಮೌಲ್ಯ=False)
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ಅಮಾನ್ಯ_ಮಾಪನ in [
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
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'Calc.java', ಅಮಾನ್ಯ_ಮಾಪನ)
            ಯಂತ್ರ.ಆಜ್ಞೆ('javac Calc.java', ['javac error:', 'Exit: 1'])
            ಯಂತ್ರ.ಆಜ್ಞೆ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ಸ್ಪ್ರಿಂಟ್_ಮೌಲ್ಯ 실행은 ಬಳಕೆದಾರ 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ಯಂತ್ರ.ಆಜ್ಞೆ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('java Calc', ['instruction limit', 'Exit: 1'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'Bad.class', 'garbage')
        ಯಂತ್ರ.ಆಜ್ಞೆ('java Bad', ['JVM error:', 'Exit: 1'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('rm Bad.class', ['Removed'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('java Bad', ['cannot read class: -2'])
        # ಸಂಪಾದನೆ_ಮೌಲ್ಯ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ಚಲಾಯಿಸು_2 = len(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
        ಯಂತ್ರ.직렬.sendall(b'edit Hello.java\n')
        ಯಂತ್ರ.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('...> ', ಚಲಾಯಿಸು_2)
        ಚಲಾಯಿಸು_2 = len(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
        ಯಂತ್ರ.직렬.sendall(b'x' * 129 + b'\n')
        ಯಂತ್ರ.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('...> ', ಚಲಾಯಿಸು_2)
        ಯಂತ್ರ.ಆಜ್ಞೆ('.save', ['Too much input; original preserved'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'f' + str(수), 'occupied')
        ಯಂತ್ರ.ಆಜ್ಞೆ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ಯಂತ್ರ.ಆಜ್ಞೆ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
        ಮಾಪನ['serial'] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ಮಾಪನ
    finally:
        ಯಂತ್ರ.ಮುಚ್ಚು()


def 주코드(ಡೇಟಾ):
    """손상 시험용 main Code의 ನಿಜವಾದ_ಡೇಟಾ ಕಡತ 오프셋/길이만 읽는다."""
    ಹುದ್ದೆ_ಮೌಲ್ಯ = 8
    def 짧():
        nonlocal ಹುದ್ದೆ_ಮೌಲ್ಯ
        ಮೌಲ್ಯ = struct.unpack_from('>H', ಡೇಟಾ, ಹುದ್ದೆ_ಮೌಲ್ಯ)[0]
        ಹುದ್ದೆ_ಮೌಲ್ಯ += 2
        return ಮೌಲ್ಯ
    def 정():
        nonlocal ಹುದ್ದೆ_ಮೌಲ್ಯ
        ಮೌಲ್ಯ = struct.unpack_from('>I', ಡೇಟಾ, ಹುದ್ದೆ_ಮೌಲ್ಯ)[0]
        ಹುದ್ದೆ_ಮೌಲ್ಯ += 4
        return ಮೌಲ್ಯ
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ಡೇಟಾ[ಹುದ್ದೆ_ಮೌಲ್ಯ]
        ಹುದ್ದೆ_ಮೌಲ್ಯ += 1
        if 종류 == 1:
            ಉದ್ದ_ಮೌಲ್ಯ = 짧()
            문자들[수] = ಡೇಟಾ[ಹುದ್ದೆ_ಮೌಲ್ಯ:ಹುದ್ದೆ_ಮೌಲ್ಯ + ಉದ್ದ_ಮೌಲ್ಯ]
            ಹುದ್ದೆ_ಮೌಲ್ಯ += ಉದ್ದ_ಮೌಲ್ಯ
        elif 종류 in (7, 8): ಹುದ್ದೆ_ಮೌಲ್ಯ += 2
        elif 종류 in (3, 9, 10, 12): ಹುದ್ದೆ_ಮೌಲ್ಯ += 4
        else: raise AssertionError(종류)
    ಹುದ್ದೆ_ಮೌಲ್ಯ += 6
    개수 = 짧()
    ಹುದ್ದೆ_ಮೌಲ್ಯ += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ಹೆಸರು = 짧()
        짧()
        for 수 in range(짧()):
            ವಿಶೇಷಣ_ಮೌಲ್ಯ = 짧()
            ಗಾತ್ರ = 정()
            if 문자들[ಹೆಸರು] == b'main' and 문자들[ವಿಶೇಷಣ_ಮೌಲ್ಯ] == b'Code':
                return ಹುದ್ದೆ_ಮೌಲ್ಯ + 8, struct.unpack_from('>I', ಡೇಟಾ, ಹುದ್ದೆ_ಮೌಲ್ಯ + 4)[0]
            ಹುದ್ದೆ_ಮೌಲ್ಯ += ಗಾತ್ರ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ = Path(임시)
        (ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'build').mkdir()
        ಮೂಲ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'Imported.java'
        ಮೂಲ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ಮೂಲ)], check=True)
        원본 = (ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'Imported.class').read_bytes()
        ಕೋಡ್_ಮೌಲ್ಯ, ಉದ್ದ_ಮೌಲ್ಯ = 주코드(원본)
        변형 = {}
        ಡೇಟಾ = bytearray(원본); ಡೇಟಾ[0] = 0; 변형['BadMagic'] = ಡೇಟಾ
        ಡೇಟಾ = bytearray(원본); ಡೇಟಾ[7] = 61; 변형['BadVer'] = ಡೇಟಾ
        ಡೇಟಾ = bytearray(원본); ಡೇಟಾ[8:10] = b'\xff\xff'; 변형['BadPool'] = ಡೇಟಾ
        ಡೇಟಾ = bytearray(원본); ಡೇಟಾ[ಕೋಡ್_ಮೌಲ್ಯ:ಕೋಡ್_ಮೌಲ್ಯ + ಉದ್ದ_ಮೌಲ್ಯ] = bytes(ಉದ್ದ_ಮೌಲ್ಯ)
        ಡೇಟಾ[ಕೋಡ್_ಮೌಲ್ಯ:ಕೋಡ್_ಮೌಲ್ಯ + 3] = b'\xa7\x00\x01'; ಡೇಟಾ[ಕೋಡ್_ಮೌಲ್ಯ + ಉದ್ದ_ಮೌಲ್ಯ - 1] = 177; 변형['BadJump'] = ಡೇಟಾ
        ಡೇಟಾ = bytearray(원본); ಡೇಟಾ[ಕೋಡ್_ಮೌಲ್ಯ:ಕೋಡ್_ಮೌಲ್ಯ + ಉದ್ದ_ಮೌಲ್ಯ] = bytes(ಉದ್ದ_ಮೌಲ್ಯ)
        ಡೇಟಾ[ಕೋಡ್_ಮೌಲ್ಯ] = 87; ಡೇಟಾ[ಕೋಡ್_ಮೌಲ್ಯ + ಉದ್ದ_ಮೌಲ್ಯ - 1] = 177; 변형['BadStack'] = ಡೇಟಾ
        # ಹೆಸರು 검사를 통과시켜 ನಿಜವಾದ_ಡೇಟಾ ಪೂರೈಸು_ಆದೇಶ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ನಮೂದು_ಮೌಲ್ಯ = ['Imported.class=' + str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'Imported.class'), 'Imported.java=' + str(ಮೂಲ)]
        for ಹೆಸರು, ಡೇಟಾ in 변형.items():
            ಮಾರ್ಗ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / (ಹೆಸರು + '.class'); ಮಾರ್ಗ.write_bytes(ಡೇಟಾ)
            ನಮೂದು_ಮೌಲ್ಯ.append(ಹೆಸರು + '.class=' + str(ಮಾರ್ಗ))
        ಸಮೂಹ_ಮೌಲ್ಯ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(ಸ್ಥಾನ / 'ಪರಿಕರಗಳು/자바파일묶기.py'), '-o', str(ಸಮೂಹ_ಮೌಲ್ಯ)] + ನಮೂದು_ಮೌಲ್ಯ, check=True)
        subprocess.run(['as', '--32', '-o', str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'user.o'), str(ಸ್ಥಾನ / '부팅/ಬಳಕೆದಾರ.s')], cwd=str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ), check=True)
        ಕರ್ನಲ್_ಮೌಲ್ಯ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ಸ್ಥಾನ / '부팅/ಜೋಡಣೆ_ಲೇಔಟ್.ld'), '-o', str(ಕರ್ನಲ್_ಮೌಲ್ಯ),
                        str(ಸ್ಥಾನ / 'build/boot.o'), str(ಸ್ಥಾನ / 'build/java.o'), str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'user.o'), str(ಸ್ಥಾನ / 'build/apps.o')], check=True)
        ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಕರ್ನಲ್_ಮೌಲ್ಯ, ನೆಟ್_ವರ್ಕ್_ಮೌಲ್ಯ=False)
        try:
            ಯಂತ್ರ.ಆಜ್ಞೆ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ಯಂತ್ರ.ಆಜ್ಞೆ('cat Imported.java', ['int[] values = new int[3]'])
            for ಹೆಸರು, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ಯಂತ್ರ.ಆಜ್ಞೆ('java ' + ಹೆಸರು, [문구, 'Exit: 1'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
        finally:
            ಯಂತ್ರ.ಮುಚ್ಚು()


if __name__ == '__main__':
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ = argparse.ArgumentParser()
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.parse_args()
    ಮಾಪನ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    ಮಾಪನ['import'] = 적재시험()
    (ಸ್ಥಾನ / 'build/자바시험.json').write_text(json.dumps(ಮಾಪನ, ensure_ascii=False, indent=2) + '\n')
