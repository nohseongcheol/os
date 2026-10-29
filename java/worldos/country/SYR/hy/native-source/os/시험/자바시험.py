#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 կատարել_հրաման, ձախողում_արժեք/միջոց_արժեք 경계 시험."""
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
from 사용자통신시험 import վիրտուալ_մեքենա, Դիրք


def խմբագրել_արժեք(մեքենա, Անուն, Բովանդակություն_արժեք, պահեստավորել_արժեք=True):
    Գործարկել = len(մեքենա.մատյան_տող)
    մեքենա.직렬.sendall(('edit ' + Անուն + '\n').encode())
    մեքենա.기다림('...> ', Գործարկել)
    for կապ in Բովանդակություն_արժեք.splitlines():
        assert len(կապ) <= 128
        Գործարկել = len(մեքենա.մատյան_տող)
        մեքենա.직렬.sendall((կապ + '\n').encode())
        մեքենա.기다림('...> ', Գործարկել)
    Գործարկել = len(մեքենա.մատյան_տող)
    մեքենա.직렬.sendall(b'.save\n' if պահեստավորել_արժեք else b'.cancel\n')
    չափ = մեքենա.기다림('jkoros> ', Գործարկել)
    assert ('Saved:' if պահեստավորել_արժեք else 'Cancelled; original preserved') in չափ, չափ


def նիշք_հասցե():
    չափ = subprocess.check_output(['nm', '-n', str(Դիրք / 'build/kernel.elf')], universal_newlines=True)
    for կապ in չափ.splitlines():
        if կապ.endswith(' ram_files'):
            return int(կապ.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def հյուր_նիշք(մեքենա, փորակ_արժեք, Չափս, Ճանապարհ):
    # 시험 VM의 메모리에서 իրական_տվյալ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    հասցե = նիշք_հասցե() + փորակ_արժեք * 16384
    մեքենա.մոնիտոր_արժեք.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(հասցե, Չափս, Ճանապարհ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Ճանապարհ.exists() and Ճանապարհ.stat().st_size == Չափս:
            return Ճանապարհ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    մեքենա = վիրտուալ_մեքենա(Դիրք / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Ցանց_արժեք=False)
    չափ = {}
    try:
        մեքենա.Հրահանգ('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        մեքենա.Հրահանգ('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        մեքենա.Հրահանգ('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        մեքենա.Հրահանգ('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        մեքենա.Հրահանգ('java Missing', ['cannot read class: -2', 'Exit: 1'])
        մեքենա.Հրահանգ('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        մեքենա.Հրահանգ('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Բովանդակություն_արժեք = '''public class Calc {
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
        խմբագրել_արժեք(մեքենա, 'Calc.java', Բովանդակություն_արժեք)
        մեքենա.Հրահանգ('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Ելք = մեքենա.Հրահանգ('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        չափ['guest_output'] = Ելք
        մուտքագրում_Ցուցակ = մեքենա.Հրահանգ('ls', ['Calc.class'])
        Չափս = int(re.search(r'Calc\.class\s+(\d+) bytes', մուտքագրում_Ցուցակ).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as գրացուցակ_արժեք:
            Ճանապարհ = Path(գրացուցակ_արժեք) / 'Calc.class'
            տվյալ = հյուր_նիշք(մեքենա, 3, Չափս, Ճանապարհ)
            իրական_տվյալ = subprocess.check_output(['java', '-Xverify:all', '-cp', գրացուցակ_արժեք, 'Calc', '6', 'guest'], universal_newlines=True)
            assert իրական_տվյալ.splitlines() == 기대, իրական_տվյալ
            չափ['class_sha256'] = hashlib.sha256(տվյալ).hexdigest()
            չափ['openjdk_output'] = իրական_տվյալ
        # 실패한 խմբագրել_արժեք/컴파일은 기존 class를 보존한다.
        խմբագրել_արժեք(մեքենա, 'Calc.java', 'not Java at all', պահեստավորել_արժեք=False)
        մեքենա.Հրահանգ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for անվավեր_չափ in [
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
            խմբագրել_արժեք(մեքենա, 'Calc.java', անվավեր_չափ)
            մեքենա.Հրահանգ('javac Calc.java', ['javac error:', 'Exit: 1'])
            մեքենա.Հրահանգ('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # բազմակրկնություն_արժեք 실행은 օգտվող 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            մեքենա.Հրահանգ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        մեքենա.Հրահանգ('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        մեքենա.Հրահանգ('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        խմբագրել_արժեք(մեքենա, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        մեքենա.Հրահանգ('javac Calc.java', ['Compiled:', 'Exit: 0'])
        մեքենա.Հրահանգ('java Calc', ['instruction limit', 'Exit: 1'])
        մեքենա.Հրահանգ('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        խմբագրել_արժեք(մեքենա, 'Bad.class', 'garbage')
        մեքենա.Հրահանգ('java Bad', ['JVM error:', 'Exit: 1'])
        մեքենա.Հրահանգ('rm Bad.class', ['Removed'])
        մեքենա.Հրահանգ('java Bad', ['cannot read class: -2'])
        # խմբագրել_արժեք 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Գործարկել = len(մեքենա.մատյան_տող)
        մեքենա.직렬.sendall(b'edit Hello.java\n')
        մեքենա.기다림('...> ', Գործարկել)
        Գործարկել = len(մեքենա.մատյան_տող)
        մեքենա.직렬.sendall(b'x' * 129 + b'\n')
        մեքենա.기다림('...> ', Գործարկել)
        մեքենա.Հրահանգ('.save', ['Too much input; original preserved'])
        մեքենա.Հրահանգ('javac Hello.java', ['Compiled:', 'Exit: 0'])
        խմբագրել_արժեք(մեքենա, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            խմբագրել_արժեք(մեքենա, 'f' + str(수), 'occupied')
        մեքենա.Հրահանգ('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        մեքենա.Հրահանգ('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in մեքենա.մատյան_տող.decode('utf-8', 'replace')
        չափ['serial'] = մեքենա.մատյան_տող.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return չափ
    finally:
        մեքենա.Փակ()


def 주코드(տվյալ):
    """손상 시험용 main Code의 իրական_տվյալ Ֆայլ 오프셋/길이만 읽는다."""
    դիրք_արժեք = 8
    def 짧():
        nonlocal դիրք_արժեք
        արժեք = struct.unpack_from('>H', տվյալ, դիրք_արժեք)[0]
        դիրք_արժեք += 2
        return արժեք
    def 정():
        nonlocal դիրք_արժեք
        արժեք = struct.unpack_from('>I', տվյալ, դիրք_արժեք)[0]
        դիրք_արժեք += 4
        return արժեք
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = տվյալ[դիրք_արժեք]
        դիրք_արժեք += 1
        if 종류 == 1:
            տեւողություն_արժեք = 짧()
            문자들[수] = տվյալ[դիրք_արժեք:դիրք_արժեք + տեւողություն_արժեք]
            դիրք_արժեք += տեւողություն_արժեք
        elif 종류 in (7, 8): դիրք_արժեք += 2
        elif 종류 in (3, 9, 10, 12): դիրք_արժեք += 4
        else: raise AssertionError(종류)
    դիրք_արժեք += 6
    개수 = 짧()
    դիրք_արժեք += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Անուն = 짧()
        짧()
        for 수 in range(짧()):
            հատկանիշ_արժեք = 짧()
            Չափս = 정()
            if 문자들[Անուն] == b'main' and 문자들[հատկանիշ_արժեք] == b'Code':
                return դիրք_արժեք + 8, struct.unpack_from('>I', տվյալ, դիրք_արժեք + 4)[0]
            դիրք_արժեք += Չափս
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        գրացուցակ_արժեք = Path(임시)
        (գրացուցակ_արժեք / 'build').mkdir()
        ԱՂԲՅՈՒՐ = գրացուցակ_արժեք / 'Imported.java'
        ԱՂԲՅՈՒՐ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ԱՂԲՅՈՒՐ)], check=True)
        원본 = (գրացուցակ_արժեք / 'Imported.class').read_bytes()
        կոդ_արժեք, տեւողություն_արժեք = 주코드(원본)
        변형 = {}
        տվյալ = bytearray(원본); տվյալ[0] = 0; 변형['BadMagic'] = տվյալ
        տվյալ = bytearray(원본); տվյալ[7] = 61; 변형['BadVer'] = տվյալ
        տվյալ = bytearray(원본); տվյալ[8:10] = b'\xff\xff'; 변형['BadPool'] = տվյալ
        տվյալ = bytearray(원본); տվյալ[կոդ_արժեք:կոդ_արժեք + տեւողություն_արժեք] = bytes(տեւողություն_արժեք)
        տվյալ[կոդ_արժեք:կոդ_արժեք + 3] = b'\xa7\x00\x01'; տվյալ[կոդ_արժեք + տեւողություն_արժեք - 1] = 177; 변형['BadJump'] = տվյալ
        տվյալ = bytearray(원본); տվյալ[կոդ_արժեք:կոդ_արժեք + տեւողություն_արժեք] = bytes(տեւողություն_արժեք)
        տվյալ[կոդ_արժեք] = 87; տվյալ[կոդ_արժեք + տեւողություն_արժեք - 1] = 177; 변형['BadStack'] = տվյալ
        # Անուն 검사를 통과시켜 իրական_տվյալ կատարել_հրաման 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        մուտքագրում_արժեք = ['Imported.class=' + str(գրացուցակ_արժեք / 'Imported.class'), 'Imported.java=' + str(ԱՂԲՅՈՒՐ)]
        for Անուն, տվյալ in 변형.items():
            Ճանապարհ = գրացուցակ_արժեք / (Անուն + '.class'); Ճանապարհ.write_bytes(տվյալ)
            մուտքագրում_արժեք.append(Անուն + '.class=' + str(Ճանապարհ))
        խումբ_արժեք = գրացուցակ_արժեք / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Դիրք / 'Գործիքներ/자바파일묶기.py'), '-o', str(խումբ_արժեք)] + մուտքագրում_արժեք, check=True)
        subprocess.run(['as', '--32', '-o', str(գրացուցակ_արժեք / 'user.o'), str(Դիրք / '부팅/օգտվող.s')], cwd=str(գրացուցակ_արժեք), check=True)
        միջուկ_արժեք = գրացուցակ_արժեք / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Դիրք / '부팅/կապ_Դասավորություն.ld'), '-o', str(միջուկ_արժեք),
                        str(Դիրք / 'build/boot.o'), str(Դիրք / 'build/java.o'), str(գրացուցակ_արժեք / 'user.o'), str(Դիրք / 'build/apps.o')], check=True)
        մեքենա = վիրտուալ_մեքենա(միջուկ_արժեք, Ցանց_արժեք=False)
        try:
            մեքենա.Հրահանգ('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            մեքենա.Հրահանգ('cat Imported.java', ['int[] values = new int[3]'])
            for Անուն, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                մեքենա.Հրահանգ('java ' + Անուն, [문구, 'Exit: 1'])
                մեքենա.Հրահանգ('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return մեքենա.մատյան_տող.decode('utf-8', 'replace')
        finally:
            մեքենա.Փակ()


if __name__ == '__main__':
    վերլուծել_արժեք = argparse.ArgumentParser()
    վերլուծել_արժեք.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = վերլուծել_արժեք.parse_args()
    չափ = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    չափ['import'] = 적재시험()
    (Դիրք / 'build/자바시험.json').write_text(json.dumps(չափ, ensure_ascii=False, indent=2) + '\n')
