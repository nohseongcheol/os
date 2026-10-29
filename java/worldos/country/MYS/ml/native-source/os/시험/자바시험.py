#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 നടപ്പാക്കുക_കമാന്_ഡ്, പരാജയം_മൂല്യം/ഉറവിടം_മൂല്യം 경계 시험."""
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
from 사용자통신시험 import അയഥാര്_ഥ_മെഷീൻ, സ്ഥാനം


def ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, പേരു്, ഉള്ളടക്കം_മൂല്യം, സ്_റ്റോർ_മൂല്യം=True):
    നടപ്പിലാക്കുക = len(മെഷീൻ.ലോഗ്_രേഖ)
    മെഷീൻ.직렬.sendall(('edit ' + പേരു് + '\n').encode())
    മെഷീൻ.കാക്കുക_അവസ്ഥ('...> ', നടപ്പിലാക്കുക)
    for ലൈൻ in ഉള്ളടക്കം_മൂല്യം.splitlines():
        assert len(ലൈൻ) <= 128
        നടപ്പിലാക്കുക = len(മെഷീൻ.ലോഗ്_രേഖ)
        മെഷീൻ.직렬.sendall((ലൈൻ + '\n').encode())
        മെഷീൻ.കാക്കുക_അവസ്ഥ('...> ', നടപ്പിലാക്കുക)
    നടപ്പിലാക്കുക = len(മെഷീൻ.ലോഗ്_രേഖ)
    മെഷീൻ.직렬.sendall(b'.save\n' if സ്_റ്റോർ_മൂല്യം else b'.cancel\n')
    അളവ് = മെഷീൻ.കാക്കുക_അവസ്ഥ('jkoros> ', നടപ്പിലാക്കുക)
    assert ('Saved:' if സ്_റ്റോർ_മൂല്യം else 'Cancelled; original preserved') in അളവ്, അളവ്


def ഫയല്_ഇമെയിൽ():
    അളവ് = subprocess.check_output(['nm', '-n', str(സ്ഥാനം / 'build/kernel.elf')], universal_newlines=True)
    for ലൈൻ in അളവ്.splitlines():
        if ലൈൻ.endswith(' ram_files'):
            return int(ലൈൻ.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def അതിഥി_ഫയല്(മെഷീൻ, സ്ലോട്ട്_മൂല്യം, വലിപ്പം, വഴി):
    # 시험 VM의 메모리에서 വാസ്തവമായ_ഡാറ്റാ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ഇമെയിൽ = ഫയല്_ഇമെയിൽ() + സ്ലോട്ട്_മൂല്യം * 16384
    മെഷീൻ.മോണിട്ടര്_മൂല്യം.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ഇമെയിൽ, വലിപ്പം, വഴി)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if വഴി.exists() and വഴി.stat().st_size == വലിപ്പം:
            return വഴി.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def പരിശോധന_പ്രവര്_ത്തനം(종류):
    മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, നെറ്റ്_വർക്ക്_മൂല്യം=False)
    അളവ് = {}
    try:
        മെഷീൻ.ആജ്ഞ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        മെഷീൻ.ആജ്ഞ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        മെഷീൻ.ആജ്ഞ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        മെഷീൻ.ആജ്ഞ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        മെഷീൻ.ആജ്ഞ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        മെഷീൻ.ആജ്ഞ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        മെഷീൻ.ആജ്ഞ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ഉള്ളടക്കം_മൂല്യം = '''public class Calc {
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
        ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'Calc.java', ഉള്ളടക്കം_മൂല്യം)
        മെഷീൻ.ആജ്ഞ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        ഫലം = മെഷീൻ.ആജ്ഞ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        അളവ്['guest_output'] = ഫലം
        എന്_ട്രി_ലിസ്റ്റ് = മെഷീൻ.ആജ്ഞ('ls', ['Calc.class'])
        വലിപ്പം = int(re.search(r'Calc\.class\s+(\d+) bytes', എന്_ട്രി_ലിസ്റ്റ്).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ഡയറക്ടറി_മൂല്യം:
            വഴി = Path(ഡയറക്ടറി_മൂല്യം) / 'Calc.class'
            ഡാറ്റാ = അതിഥി_ഫയല്(മെഷീൻ, 3, വലിപ്പം, വഴി)
            വാസ്തവമായ_ഡാറ്റാ = subprocess.check_output(['java', '-Xverify:all', '-cp', ഡയറക്ടറി_മൂല്യം, 'Calc', '6', 'guest'], universal_newlines=True)
            assert വാസ്തവമായ_ഡാറ്റാ.splitlines() == 기대, വാസ്തവമായ_ഡാറ്റാ
            അളവ്['class_sha256'] = hashlib.sha256(ഡാറ്റാ).hexdigest()
            അളവ്['openjdk_output'] = വാസ്തവമായ_ഡാറ്റാ
        # 실패한 ചിട്ടപ്പെടുത്തല്_മൂല്യം/컴파일은 기존 class를 보존한다.
        ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'Calc.java', 'not Java at all', സ്_റ്റോർ_മൂല്യം=False)
        മെഷീൻ.ആജ്ഞ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for അസാധുവായ_അളവ് in [
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
            ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'Calc.java', അസാധുവായ_അളവ്)
            മെഷീൻ.ആജ്ഞ('javac Calc.java', ['javac error:', 'Exit: 1'])
            മെഷീൻ.ആജ്ഞ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ആവര്_ത്തനം_മൂല്യം 실행은 ഉപയോക്താവ് സമൂഹം_മൂല്യം/프레임을 매번 초기화한다.
        for 수 in range(12):
            മെഷീൻ.ആജ്ഞ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        മെഷീൻ.ആജ്ഞ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        മെഷീൻ.ആജ്ഞ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        മെഷീൻ.ആജ്ഞ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        മെഷീൻ.ആജ്ഞ('java Calc', ['instruction limit', 'Exit: 1'])
        മെഷീൻ.ആജ്ഞ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'Bad.class', 'garbage')
        മെഷീൻ.ആജ്ഞ('java Bad', ['JVM error:', 'Exit: 1'])
        മെഷീൻ.ആജ്ഞ('rm Bad.class', ['Removed'])
        മെഷീൻ.ആജ്ഞ('java Bad', ['cannot read class: -2'])
        # ചിട്ടപ്പെടുത്തല്_മൂല്യം 입력의 넘친 부분을 잘라서 저장하지 않는다.
        നടപ്പിലാക്കുക = len(മെഷീൻ.ലോഗ്_രേഖ)
        മെഷീൻ.직렬.sendall(b'edit Hello.java\n')
        മെഷീൻ.കാക്കുക_അവസ്ഥ('...> ', നടപ്പിലാക്കുക)
        നടപ്പിലാക്കുക = len(മെഷീൻ.ലോഗ്_രേഖ)
        മെഷീൻ.직렬.sendall(b'x' * 129 + b'\n')
        മെഷീൻ.കാക്കുക_അവസ്ഥ('...> ', നടപ്പിലാക്കുക)
        മെഷീൻ.ആജ്ഞ('.save', ['Too much input; original preserved'])
        മെഷീൻ.ആജ്ഞ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'f' + str(수), 'occupied')
        മെഷീൻ.ആജ്ഞ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        മെഷീൻ.ആജ്ഞ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
        അളവ്['serial'] = മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return അളവ്
    finally:
        മെഷീൻ.അടയ്ക്കു()


def 주코드(ഡാറ്റാ):
    """손상 시험용 main Code의 വാസ്തവമായ_ഡാറ്റാ ഫയല് 오프셋/길이만 읽는다."""
    പദവി_മൂല്യം = 8
    def 짧():
        nonlocal പദവി_മൂല്യം
        മൂല്യം = struct.unpack_from('>H', ഡാറ്റാ, പദവി_മൂല്യം)[0]
        പദവി_മൂല്യം += 2
        return മൂല്യം
    def 정():
        nonlocal പദവി_മൂല്യം
        മൂല്യം = struct.unpack_from('>I', ഡാറ്റാ, പദവി_മൂല്യം)[0]
        പദവി_മൂല്യം += 4
        return മൂല്യം
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ഡാറ്റാ[പദവി_മൂല്യം]
        പദവി_മൂല്യം += 1
        if 종류 == 1:
            ദൈര്_ഘ്യം_മൂല്യം = 짧()
            문자들[수] = ഡാറ്റാ[പദവി_മൂല്യം:പദവി_മൂല്യം + ദൈര്_ഘ്യം_മൂല്യം]
            പദവി_മൂല്യം += ദൈര്_ഘ്യം_മൂല്യം
        elif 종류 in (7, 8): പദവി_മൂല്യം += 2
        elif 종류 in (3, 9, 10, 12): പദവി_മൂല്യം += 4
        else: raise AssertionError(종류)
    പദവി_മൂല്യം += 6
    개수 = 짧()
    പദവി_മൂല്യം += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        പേരു് = 짧()
        짧()
        for 수 in range(짧()):
            ആട്രിബ്യൂട്ട്_മൂല്യം = 짧()
            വലിപ്പം = 정()
            if 문자들[പേരു്] == b'main' and 문자들[ആട്രിബ്യൂട്ട്_മൂല്യം] == b'Code':
                return പദവി_മൂല്യം + 8, struct.unpack_from('>I', ഡാറ്റാ, പദവി_മൂല്യം + 4)[0]
            പദവി_മൂല്യം += വലിപ്പം
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ഡയറക്ടറി_മൂല്യം = Path(임시)
        (ഡയറക്ടറി_മൂല്യം / 'build').mkdir()
        ഉറവിടം = ഡയറക്ടറി_മൂല്യം / 'Imported.java'
        ഉറവിടം.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ഉറവിടം)], check=True)
        원본 = (ഡയറക്ടറി_മൂല്യം / 'Imported.class').read_bytes()
        കോഡ്_മൂല്യം, ദൈര്_ഘ്യം_മൂല്യം = 주코드(원본)
        변형 = {}
        ഡാറ്റാ = bytearray(원본); ഡാറ്റാ[0] = 0; 변형['BadMagic'] = ഡാറ്റാ
        ഡാറ്റാ = bytearray(원본); ഡാറ്റാ[7] = 61; 변형['BadVer'] = ഡാറ്റാ
        ഡാറ്റാ = bytearray(원본); ഡാറ്റാ[8:10] = b'\xff\xff'; 변형['BadPool'] = ഡാറ്റാ
        ഡാറ്റാ = bytearray(원본); ഡാറ്റാ[കോഡ്_മൂല്യം:കോഡ്_മൂല്യം + ദൈര്_ഘ്യം_മൂല്യം] = bytes(ദൈര്_ഘ്യം_മൂല്യം)
        ഡാറ്റാ[കോഡ്_മൂല്യം:കോഡ്_മൂല്യം + 3] = b'\xa7\x00\x01'; ഡാറ്റാ[കോഡ്_മൂല്യം + ദൈര്_ഘ്യം_മൂല്യം - 1] = 177; 변형['BadJump'] = ഡാറ്റാ
        ഡാറ്റാ = bytearray(원본); ഡാറ്റാ[കോഡ്_മൂല്യം:കോഡ്_മൂല്യം + ദൈര്_ഘ്യം_മൂല്യം] = bytes(ദൈര്_ഘ്യം_മൂല്യം)
        ഡാറ്റാ[കോഡ്_മൂല്യം] = 87; ഡാറ്റാ[കോഡ്_മൂല്യം + ദൈര്_ഘ്യം_മൂല്യം - 1] = 177; 변형['BadStack'] = ഡാറ്റാ
        # പേരു് 검사를 통과시켜 വാസ്തവമായ_ഡാറ്റാ നടപ്പാക്കുക_കമാന്_ഡ് 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        എന്_ട്രി_മൂല്യം = ['Imported.class=' + str(ഡയറക്ടറി_മൂല്യം / 'Imported.class'), 'Imported.java=' + str(ഉറവിടം)]
        for പേരു്, ഡാറ്റാ in 변형.items():
            വഴി = ഡയറക്ടറി_മൂല്യം / (പേരു് + '.class'); വഴി.write_bytes(ഡാറ്റാ)
            എന്_ട്രി_മൂല്യം.append(പേരു് + '.class=' + str(വഴി))
        സംഘം_മൂല്യം = ഡയറക്ടറി_മൂല്യം / 'build/java-files.bin'
        subprocess.run([sys.executable, str(സ്ഥാനം / 'ഉപകരണങ്ങൾ/자바파일묶기.py'), '-o', str(സംഘം_മൂല്യം)] + എന്_ട്രി_മൂല്യം, check=True)
        subprocess.run(['as', '--32', '-o', str(ഡയറക്ടറി_മൂല്യം / 'user.o'), str(സ്ഥാനം / '부팅/ഉപയോക്താവ്.s')], cwd=str(ഡയറക്ടറി_മൂല്യം), check=True)
        കെര്_ണല്_മൂല്യം = ഡയറക്ടറി_മൂല്യം / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(സ്ഥാനം / '부팅/ലിങ്ക്_ലേഔട്ട്.ld'), '-o', str(കെര്_ണല്_മൂല്യം),
                        str(സ്ഥാനം / 'build/boot.o'), str(സ്ഥാനം / 'build/java.o'), str(ഡയറക്ടറി_മൂല്യം / 'user.o'), str(സ്ഥാനം / 'build/apps.o')], check=True)
        മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(കെര്_ണല്_മൂല്യം, നെറ്റ്_വർക്ക്_മൂല്യം=False)
        try:
            മെഷീൻ.ആജ്ഞ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            മെഷീൻ.ആജ്ഞ('cat Imported.java', ['int[] values = new int[3]'])
            for പേരു്, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                മെഷീൻ.ആജ്ഞ('java ' + പേരു്, [문구, 'Exit: 1'])
                മെഷീൻ.ആജ്ഞ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
        finally:
            മെഷീൻ.അടയ്ക്കു()


if __name__ == '__main__':
    പാര്_സ്_ചെയ്യുക_മൂല്യം = argparse.ArgumentParser()
    പാര്_സ്_ചെയ്യുക_മൂല്യം.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = പാര്_സ്_ചെയ്യുക_മൂല്യം.parse_args()
    അളവ് = {종류: പരിശോധന_പ്രവര്_ത്തനം(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    അളവ്['import'] = 적재시험()
    (സ്ഥാനം / 'build/자바시험.json').write_text(json.dumps(അളവ്, ensure_ascii=False, indent=2) + '\n')
