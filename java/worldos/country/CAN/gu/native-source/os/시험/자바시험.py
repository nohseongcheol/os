#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 અમલ_કરો_આદેશ, નિષ્ફળતા_મૂલ્ય/સાધન_મૂલ્ય 경계 시험."""
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
from 사용자통신시험 import વર્ચુઅલ_મશીન, સ્થાન


def સંપાદન_મૂલ્ય(મશીન, નામ, સામગ્રી_મૂલ્ય, સંગ્રહ_કરવો_મૂલ્ય=True):
    ચલાવો_2 = len(મશીન.લૉગ_પંક્તિ)
    મશીન.직렬.sendall(('edit ' + નામ + '\n').encode())
    મશીન.પ્રતીક્ષા_સ્થિતિ('...> ', ચલાવો_2)
    for લાઇન in સામગ્રી_મૂલ્ય.splitlines():
        assert len(લાઇન) <= 128
        ચલાવો_2 = len(મશીન.લૉગ_પંક્તિ)
        મશીન.직렬.sendall((લાઇન + '\n').encode())
        મશીન.પ્રતીક્ષા_સ્થિતિ('...> ', ચલાવો_2)
    ચલાવો_2 = len(મશીન.લૉગ_પંક્તિ)
    મશીન.직렬.sendall(b'.save\n' if સંગ્રહ_કરવો_મૂલ્ય else b'.cancel\n')
    પરિમાણ = મશીન.પ્રતીક્ષા_સ્થિતિ('jkoros> ', ચલાવો_2)
    assert ('Saved:' if સંગ્રહ_કરવો_મૂલ્ય else 'Cancelled; original preserved') in પરિમાણ, પરિમાણ


def ફાઇલ_સરનામું():
    પરિમાણ = subprocess.check_output(['nm', '-n', str(સ્થાન / 'build/kernel.elf')], universal_newlines=True)
    for લાઇન in પરિમાણ.splitlines():
        if લાઇન.endswith(' ram_files'):
            return int(લાઇન.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def અતિથિ_ફાઇલ(મશીન, સ્લૉટ_મૂલ્ય, માપ, પથ):
    # 시험 VM의 메모리에서 વાસ્તવિક_ડેટા 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    સરનામું = ફાઇલ_સરનામું() + સ્લૉટ_મૂલ્ય * 16384
    મશીન.મૉનિટર_મૂલ્ય.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(સરનામું, માપ, પથ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if પથ.exists() and પથ.stat().st_size == માપ:
            return પથ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    મશીન = વર્ચુઅલ_મશીન(સ્થાન / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, નેટવર્ક_મૂલ્ય=False)
    પરિમાણ = {}
    try:
        મશીન.આદેશ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        મશીન.આદેશ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        મશીન.આદેશ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        મશીન.આદેશ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        મશીન.આદેશ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        મશીન.આદેશ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        મશીન.આદેશ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        સામગ્રી_મૂલ્ય = '''public class Calc {
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
        સંપાદન_મૂલ્ય(મશીન, 'Calc.java', સામગ્રી_મૂલ્ય)
        મશીન.આદેશ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        આઉટપુટ = મશીન.આદેશ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        પરિમાણ['guest_output'] = આઉટપુટ
        પ્રવેશ_સૂચી = મશીન.આદેશ('ls', ['Calc.class'])
        માપ = int(re.search(r'Calc\.class\s+(\d+) bytes', પ્રવેશ_સૂચી).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as નિર્દેશિકા_મૂલ્ય:
            પથ = Path(નિર્દેશિકા_મૂલ્ય) / 'Calc.class'
            ડેટા = અતિથિ_ફાઇલ(મશીન, 3, માપ, પથ)
            વાસ્તવિક_ડેટા = subprocess.check_output(['java', '-Xverify:all', '-cp', નિર્દેશિકા_મૂલ્ય, 'Calc', '6', 'guest'], universal_newlines=True)
            assert વાસ્તવિક_ડેટા.splitlines() == 기대, વાસ્તવિક_ડેટા
            પરિમાણ['class_sha256'] = hashlib.sha256(ડેટા).hexdigest()
            પરિમાણ['openjdk_output'] = વાસ્તવિક_ડેટા
        # 실패한 સંપાદન_મૂલ્ય/컴파일은 기존 class를 보존한다.
        સંપાદન_મૂલ્ય(મશીન, 'Calc.java', 'not Java at all', સંગ્રહ_કરવો_મૂલ્ય=False)
        મશીન.આદેશ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for અમાન્ય_પરિમાણ in [
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
            સંપાદન_મૂલ્ય(મશીન, 'Calc.java', અમાન્ય_પરિમાણ)
            મશીન.આદેશ('javac Calc.java', ['javac error:', 'Exit: 1'])
            મશીન.આદેશ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # પુનરાવર્તન_મૂલ્ય 실행은 ઉપયોગકર્તા 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            મશીન.આદેશ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        મશીન.આદેશ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        મશીન.આદેશ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        સંપાદન_મૂલ્ય(મશીન, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        મશીન.આદેશ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        મશીન.આદેશ('java Calc', ['instruction limit', 'Exit: 1'])
        મશીન.આદેશ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        સંપાદન_મૂલ્ય(મશીન, 'Bad.class', 'garbage')
        મશીન.આદેશ('java Bad', ['JVM error:', 'Exit: 1'])
        મશીન.આદેશ('rm Bad.class', ['Removed'])
        મશીન.આદેશ('java Bad', ['cannot read class: -2'])
        # સંપાદન_મૂલ્ય 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ચલાવો_2 = len(મશીન.લૉગ_પંક્તિ)
        મશીન.직렬.sendall(b'edit Hello.java\n')
        મશીન.પ્રતીક્ષા_સ્થિતિ('...> ', ચલાવો_2)
        ચલાવો_2 = len(મશીન.લૉગ_પંક્તિ)
        મશીન.직렬.sendall(b'x' * 129 + b'\n')
        મશીન.પ્રતીક્ષા_સ્થિતિ('...> ', ચલાવો_2)
        મશીન.આદેશ('.save', ['Too much input; original preserved'])
        મશીન.આદેશ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        સંપાદન_મૂલ્ય(મશીન, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            સંપાદન_મૂલ્ય(મશીન, 'f' + str(수), 'occupied')
        મશીન.આદેશ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        મશીન.આદેશ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
        પરિમાણ['serial'] = મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return પરિમાણ
    finally:
        મશીન.બંધ_કરો()


def 주코드(ડેટા):
    """손상 시험용 main Code의 વાસ્તવિક_ડેટા ફાઈલ 오프셋/길이만 읽는다."""
    સ્થિતિ_મૂલ્ય = 8
    def 짧():
        nonlocal સ્થિતિ_મૂલ્ય
        મૂલ્ય = struct.unpack_from('>H', ડેટા, સ્થિતિ_મૂલ્ય)[0]
        સ્થિતિ_મૂલ્ય += 2
        return મૂલ્ય
    def 정():
        nonlocal સ્થિતિ_મૂલ્ય
        મૂલ્ય = struct.unpack_from('>I', ડેટા, સ્થિતિ_મૂલ્ય)[0]
        સ્થિતિ_મૂલ્ય += 4
        return મૂલ્ય
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ડેટા[સ્થિતિ_મૂલ્ય]
        સ્થિતિ_મૂલ્ય += 1
        if 종류 == 1:
            લંબાઈ_મૂલ્ય = 짧()
            문자들[수] = ડેટા[સ્થિતિ_મૂલ્ય:સ્થિતિ_મૂલ્ય + લંબાઈ_મૂલ્ય]
            સ્થિતિ_મૂલ્ય += લંબાઈ_મૂલ્ય
        elif 종류 in (7, 8): સ્થિતિ_મૂલ્ય += 2
        elif 종류 in (3, 9, 10, 12): સ્થિતિ_મૂલ્ય += 4
        else: raise AssertionError(종류)
    સ્થિતિ_મૂલ્ય += 6
    개수 = 짧()
    સ્થિતિ_મૂલ્ય += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        નામ = 짧()
        짧()
        for 수 in range(짧()):
            વિશેષતા_મૂલ્ય = 짧()
            માપ = 정()
            if 문자들[નામ] == b'main' and 문자들[વિશેષતા_મૂલ્ય] == b'Code':
                return સ્થિતિ_મૂલ્ય + 8, struct.unpack_from('>I', ડેટા, સ્થિતિ_મૂલ્ય + 4)[0]
            સ્થિતિ_મૂલ્ય += માપ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        નિર્દેશિકા_મૂલ્ય = Path(임시)
        (નિર્દેશિકા_મૂલ્ય / 'build').mkdir()
        સ્રોત = નિર્દેશિકા_મૂલ્ય / 'Imported.java'
        સ્રોત.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(સ્રોત)], check=True)
        원본 = (નિર્દેશિકા_મૂલ્ય / 'Imported.class').read_bytes()
        코드, લંબાઈ_મૂલ્ય = 주코드(원본)
        변형 = {}
        ડેટા = bytearray(원본); ડેટા[0] = 0; 변형['BadMagic'] = ડેટા
        ડેટા = bytearray(원본); ડેટા[7] = 61; 변형['BadVer'] = ડેટા
        ડેટા = bytearray(원본); ડેટા[8:10] = b'\xff\xff'; 변형['BadPool'] = ડેટા
        ડેટા = bytearray(원본); ડેટા[코드:코드 + લંબાઈ_મૂલ્ય] = bytes(લંબાઈ_મૂલ્ય)
        ડેટા[코드:코드 + 3] = b'\xa7\x00\x01'; ડેટા[코드 + લંબાઈ_મૂલ્ય - 1] = 177; 변형['BadJump'] = ડેટા
        ડેટા = bytearray(원본); ડેટા[코드:코드 + લંબાઈ_મૂલ્ય] = bytes(લંબાઈ_મૂલ્ય)
        ડેટા[코드] = 87; ડેટા[코드 + લંબાઈ_મૂલ્ય - 1] = 177; 변형['BadStack'] = ડેટા
        # નામ 검사를 통과시켜 વાસ્તવિક_ડેટા અમલ_કરો_આદેશ 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        પ્રવેશ_મૂલ્ય = ['Imported.class=' + str(નિર્દેશિકા_મૂલ્ય / 'Imported.class'), 'Imported.java=' + str(સ્રોત)]
        for નામ, ડેટા in 변형.items():
            પથ = નિર્દેશિકા_મૂલ્ય / (નામ + '.class'); પથ.write_bytes(ડેટા)
            પ્રવેશ_મૂલ્ય.append(નામ + '.class=' + str(પથ))
        સમૂહ_મૂલ્ય = નિર્દેશિકા_મૂલ્ય / 'build/java-files.bin'
        subprocess.run([sys.executable, str(સ્થાન / 'ઉપકરણો/자바파일묶기.py'), '-o', str(સમૂહ_મૂલ્ય)] + પ્રવેશ_મૂલ્ય, check=True)
        subprocess.run(['as', '--32', '-o', str(નિર્દેશિકા_મૂલ્ય / 'user.o'), str(સ્થાન / '부팅/ઉપયોગકર્તા.s')], cwd=str(નિર્દેશિકા_મૂલ્ય), check=True)
        કર્નેલ_મૂલ્ય = નિર્દેશિકા_મૂલ્ય / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(સ્થાન / '부팅/લિંક_લેઆઉટ.ld'), '-o', str(કર્નેલ_મૂલ્ય),
                        str(સ્થાન / 'build/boot.o'), str(સ્થાન / 'build/java.o'), str(નિર્દેશિકા_મૂલ્ય / 'user.o'), str(સ્થાન / 'build/apps.o')], check=True)
        મશીન = વર્ચુઅલ_મશીન(કર્નેલ_મૂલ્ય, નેટવર્ક_મૂલ્ય=False)
        try:
            મશીન.આદેશ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            મશીન.આદેશ('cat Imported.java', ['int[] values = new int[3]'])
            for નામ, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                મશીન.આદેશ('java ' + નામ, [문구, 'Exit: 1'])
                મશીન.આદેશ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
        finally:
            મશીન.બંધ_કરો()


if __name__ == '__main__':
    પાર્સ_કરો_મૂલ્ય = argparse.ArgumentParser()
    પાર્સ_કરો_મૂલ્ય.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    દલીલો = પાર્સ_કરો_મૂલ્ય.parse_args()
    પરિમાણ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if દલીલો.boot == 'both' else (દલીલો.boot,))}
    પરિમાણ['import'] = 적재시험()
    (સ્થાન / 'build/자바시험.json').write_text(json.dumps(પરિમાણ, ensure_ascii=False, indent=2) + '\n')
