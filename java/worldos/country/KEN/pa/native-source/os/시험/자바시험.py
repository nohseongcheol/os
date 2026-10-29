#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼, ਅਸਫਲ_ਕੀਮਤ/ਸੰਸਾਧਨ_ਕੀਮਤ 경계 시험."""
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
from 사용자통신시험 import ਵਰਚੁਅਲ_ਮਸ਼ੀਨ, ਸਥਿਤੀ


def ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, ਨਾਂ, ਤਤਕਰਾ_ਕੀਮਤ, ਸੰਭਾਲੋ_ਕੀਮਤ=True):
    ਚਲਾਓ_2 = len(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
    ਮਸ਼ੀਨ.직렬.sendall(('edit ' + ਨਾਂ + '\n').encode())
    ਮਸ਼ੀਨ.기다림('...> ', ਚਲਾਓ_2)
    for ਲਾਈਨ in ਤਤਕਰਾ_ਕੀਮਤ.splitlines():
        assert len(ਲਾਈਨ) <= 128
        ਚਲਾਓ_2 = len(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
        ਮਸ਼ੀਨ.직렬.sendall((ਲਾਈਨ + '\n').encode())
        ਮਸ਼ੀਨ.기다림('...> ', ਚਲਾਓ_2)
    ਚਲਾਓ_2 = len(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
    ਮਸ਼ੀਨ.직렬.sendall(b'.save\n' if ਸੰਭਾਲੋ_ਕੀਮਤ else b'.cancel\n')
    ਮਾਪ = ਮਸ਼ੀਨ.기다림('jkoros> ', ਚਲਾਓ_2)
    assert ('Saved:' if ਸੰਭਾਲੋ_ਕੀਮਤ else 'Cancelled; original preserved') in ਮਾਪ, ਮਾਪ


def ਲਿਖਤ_ਪੱਤਰ_ਪਤਾ():
    ਮਾਪ = subprocess.check_output(['nm', '-n', str(ਸਥਿਤੀ / 'build/kernel.elf')], universal_newlines=True)
    for ਲਾਈਨ in ਮਾਪ.splitlines():
        if ਲਾਈਨ.endswith(' ram_files'):
            return int(ਲਾਈਨ.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ਗੈਸਟ_ਲਿਖਤ_ਪੱਤਰ(ਮਸ਼ੀਨ, ਸਲੌਟ_ਕੀਮਤ, ਆਕਾਰ, ਮਾਰਗ):
    # 시험 VM의 메모리에서 ਅਸਲ_ਸਮੱਗਰੀ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ਪਤਾ = ਲਿਖਤ_ਪੱਤਰ_ਪਤਾ() + ਸਲੌਟ_ਕੀਮਤ * 16384
    ਮਸ਼ੀਨ.ਮੌਨੀਟਰ_ਕੀਮਤ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ਪਤਾ, ਆਕਾਰ, ਮਾਰਗ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ਮਾਰਗ.exists() and ਮਾਰਗ.stat().st_size == ਆਕਾਰ:
            return ਮਾਰਗ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ਨੈਟਵਰਕ_ਕੀਮਤ=False)
    ਮਾਪ = {}
    try:
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ਤਤਕਰਾ_ਕੀਮਤ = '''public class Calc {
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
        ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'Calc.java', ਤਤਕਰਾ_ਕੀਮਤ)
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        ਆਉਟਪੁੱਟ = ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ਮਾਪ['guest_output'] = ਆਉਟਪੁੱਟ
        ਦਾਖਲਾ_ਸੂਚੀ = ਮਸ਼ੀਨ.ਕਮਾਂਡ('ls', ['Calc.class'])
        ਆਕਾਰ = int(re.search(r'Calc\.class\s+(\d+) bytes', ਦਾਖਲਾ_ਸੂਚੀ).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ:
            ਮਾਰਗ = Path(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ) / 'Calc.class'
            ਸਮੱਗਰੀ = ਗੈਸਟ_ਲਿਖਤ_ਪੱਤਰ(ਮਸ਼ੀਨ, 3, ਆਕਾਰ, ਮਾਰਗ)
            ਅਸਲ_ਸਮੱਗਰੀ = subprocess.check_output(['java', '-Xverify:all', '-cp', ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ਅਸਲ_ਸਮੱਗਰੀ.splitlines() == 기대, ਅਸਲ_ਸਮੱਗਰੀ
            ਮਾਪ['class_sha256'] = hashlib.sha256(ਸਮੱਗਰੀ).hexdigest()
            ਮਾਪ['openjdk_output'] = ਅਸਲ_ਸਮੱਗਰੀ
        # 실패한 ਸੰਪਾਦਨ_ਕੀਮਤ/컴파일은 기존 class를 보존한다.
        ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'Calc.java', 'not Java at all', ਸੰਭਾਲੋ_ਕੀਮਤ=False)
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ਅਯੋਗ_ਮਾਪ in [
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
            ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'Calc.java', ਅਯੋਗ_ਮਾਪ)
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Calc.java', ['javac error:', 'Exit: 1'])
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ਦੋਹਰਾਵ_ਕੀਮਤ 실행은 ਉਪਭੋਗਤਾ 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Calc', ['instruction limit', 'Exit: 1'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'Bad.class', 'garbage')
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Bad', ['JVM error:', 'Exit: 1'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('rm Bad.class', ['Removed'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Bad', ['cannot read class: -2'])
        # ਸੰਪਾਦਨ_ਕੀਮਤ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ਚਲਾਓ_2 = len(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
        ਮਸ਼ੀਨ.직렬.sendall(b'edit Hello.java\n')
        ਮਸ਼ੀਨ.기다림('...> ', ਚਲਾਓ_2)
        ਚਲਾਓ_2 = len(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
        ਮਸ਼ੀਨ.직렬.sendall(b'x' * 129 + b'\n')
        ਮਸ਼ੀਨ.기다림('...> ', ਚਲਾਓ_2)
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('.save', ['Too much input; original preserved'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'f' + str(수), 'occupied')
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
        ਮਾਪ['serial'] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ਮਾਪ
    finally:
        ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()


def 주코드(ਸਮੱਗਰੀ):
    """손상 시험용 main Code의 ਅਸਲ_ਸਮੱਗਰੀ ਫਾਇਲ 오프셋/길이만 읽는다."""
    ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ = 8
    def 짧():
        nonlocal ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ
        ਕੀਮਤ = struct.unpack_from('>H', ਸਮੱਗਰੀ, ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ)[0]
        ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += 2
        return ਕੀਮਤ
    def 정():
        nonlocal ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ
        ਕੀਮਤ = struct.unpack_from('>I', ਸਮੱਗਰੀ, ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ)[0]
        ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += 4
        return ਕੀਮਤ
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ਸਮੱਗਰੀ[ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ]
        ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += 1
        if 종류 == 1:
            ਲੰਬਾਈ_ਕੀਮਤ = 짧()
            문자들[수] = ਸਮੱਗਰੀ[ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ:ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ + ਲੰਬਾਈ_ਕੀਮਤ]
            ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += ਲੰਬਾਈ_ਕੀਮਤ
        elif 종류 in (7, 8): ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += 2
        elif 종류 in (3, 9, 10, 12): ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += 4
        else: raise AssertionError(종류)
    ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += 6
    개수 = 짧()
    ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ਨਾਂ = 짧()
        짧()
        for 수 in range(짧()):
            ਯੋਗ_ਕੀਮਤ = 짧()
            ਆਕਾਰ = 정()
            if 문자들[ਨਾਂ] == b'main' and 문자들[ਯੋਗ_ਕੀਮਤ] == b'Code':
                return ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ + 8, struct.unpack_from('>I', ਸਮੱਗਰੀ, ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ + 4)[0]
            ਸਥਿਤੀ_ਬਦਲੋ_ਕੀਮਤ += ਆਕਾਰ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ = Path(임시)
        (ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'build').mkdir()
        ਸਰੋਤ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'Imported.java'
        ਸਰੋਤ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ਸਰੋਤ)], check=True)
        원본 = (ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'Imported.class').read_bytes()
        코드, ਲੰਬਾਈ_ਕੀਮਤ = 주코드(원본)
        변형 = {}
        ਸਮੱਗਰੀ = bytearray(원본); ਸਮੱਗਰੀ[0] = 0; 변형['BadMagic'] = ਸਮੱਗਰੀ
        ਸਮੱਗਰੀ = bytearray(원본); ਸਮੱਗਰੀ[7] = 61; 변형['BadVer'] = ਸਮੱਗਰੀ
        ਸਮੱਗਰੀ = bytearray(원본); ਸਮੱਗਰੀ[8:10] = b'\xff\xff'; 변형['BadPool'] = ਸਮੱਗਰੀ
        ਸਮੱਗਰੀ = bytearray(원본); ਸਮੱਗਰੀ[코드:코드 + ਲੰਬਾਈ_ਕੀਮਤ] = bytes(ਲੰਬਾਈ_ਕੀਮਤ)
        ਸਮੱਗਰੀ[코드:코드 + 3] = b'\xa7\x00\x01'; ਸਮੱਗਰੀ[코드 + ਲੰਬਾਈ_ਕੀਮਤ - 1] = 177; 변형['BadJump'] = ਸਮੱਗਰੀ
        ਸਮੱਗਰੀ = bytearray(원본); ਸਮੱਗਰੀ[코드:코드 + ਲੰਬਾਈ_ਕੀਮਤ] = bytes(ਲੰਬਾਈ_ਕੀਮਤ)
        ਸਮੱਗਰੀ[코드] = 87; ਸਮੱਗਰੀ[코드 + ਲੰਬਾਈ_ਕੀਮਤ - 1] = 177; 변형['BadStack'] = ਸਮੱਗਰੀ
        # ਨਾਂ 검사를 통과시켜 ਅਸਲ_ਸਮੱਗਰੀ ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ਦਾਖਲਾ_ਕੀਮਤ = ['Imported.class=' + str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'Imported.class'), 'Imported.java=' + str(ਸਰੋਤ)]
        for ਨਾਂ, ਸਮੱਗਰੀ in 변형.items():
            ਮਾਰਗ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / (ਨਾਂ + '.class'); ਮਾਰਗ.write_bytes(ਸਮੱਗਰੀ)
            ਦਾਖਲਾ_ਕੀਮਤ.append(ਨਾਂ + '.class=' + str(ਮਾਰਗ))
        ਸਮੂਹ_ਕੀਮਤ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(ਸਥਿਤੀ / 'ਸਾਧਨ/자바파일묶기.py'), '-o', str(ਸਮੂਹ_ਕੀਮਤ)] + ਦਾਖਲਾ_ਕੀਮਤ, check=True)
        subprocess.run(['as', '--32', '-o', str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'user.o'), str(ਸਥਿਤੀ / '부팅/ਉਪਭੋਗਤਾ.s')], cwd=str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ), check=True)
        ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ਸਥਿਤੀ / '부팅/ਲਿੰਕ_ਖਾਕਾ.ld'), '-o', str(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ),
                        str(ਸਥਿਤੀ / 'build/boot.o'), str(ਸਥਿਤੀ / 'build/java.o'), str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'user.o'), str(ਸਥਿਤੀ / 'build/apps.o')], check=True)
        ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ, ਨੈਟਵਰਕ_ਕੀਮਤ=False)
        try:
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('cat Imported.java', ['int[] values = new int[3]'])
            for ਨਾਂ, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('java ' + ਨਾਂ, [문구, 'Exit: 1'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
        finally:
            ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()


if __name__ == '__main__':
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ = argparse.ArgumentParser()
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    ਆਰਗੂਮੈਂਟ = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.parse_args()
    ਮਾਪ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if ਆਰਗੂਮੈਂਟ.boot == 'both' else (ਆਰਗੂਮੈਂਟ.boot,))}
    ਮਾਪ['import'] = 적재시험()
    (ਸਥਿਤੀ / 'build/자바시험.json').write_text(json.dumps(ਮਾਪ, ensure_ascii=False, indent=2) + '\n')
