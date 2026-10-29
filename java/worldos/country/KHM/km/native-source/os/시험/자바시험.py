#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 អនុវត្ត_ពាក្យបញ្ជា, បរាជ័យ_តំលៃ/ធនធាន_តំលៃ 경계 시험."""
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
from 사용자통신시험 import និម្មិត_ម៉ាស៊ីន, កំណត់ទីតាំង


def កែសម្រួល_តំលៃ(ម៉ាស៊ីន, ឈ្មោះ, មាតិកា_តំលៃ, ផ្ទុក_តំលៃ=True):
    រត់ = len(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
    ម៉ាស៊ីន.직렬.sendall(('edit ' + ឈ្មោះ + '\n').encode())
    ម៉ាស៊ីន.រង់ចាំ_ភាព('...> ', រត់)
    for បន្ទាត់ in មាតិកា_តំលៃ.splitlines():
        assert len(បន្ទាត់) <= 128
        រត់ = len(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
        ម៉ាស៊ីន.직렬.sendall((បន្ទាត់ + '\n').encode())
        ម៉ាស៊ីន.រង់ចាំ_ភាព('...> ', រត់)
    រត់ = len(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
    ម៉ាស៊ីន.직렬.sendall(b'.save\n' if ផ្ទុក_តំលៃ else b'.cancel\n')
    ការវាស់វែង = ម៉ាស៊ីន.រង់ចាំ_ភាព('jkoros> ', រត់)
    assert ('Saved:' if ផ្ទុក_តំលៃ else 'Cancelled; original preserved') in ការវាស់វែង, ការវាស់វែង


def ឯកសារ_អ៊ីម៉ែល():
    ការវាស់វែង = subprocess.check_output(['nm', '-n', str(កំណត់ទីតាំង / 'build/kernel.elf')], universal_newlines=True)
    for បន្ទាត់ in ការវាស់វែង.splitlines():
        if បន្ទាត់.endswith(' ram_files'):
            return int(បន្ទាត់.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ភ្ញៀវ_ឯកសារ(ម៉ាស៊ីន, ចន្លោះប្រហោង_តំលៃ, ដាក់ទំហំ, ផ្លូវ):
    # 시험 VM의 메모리에서 ដែលពិត_ទិន្នន័យ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    អ៊ីម៉ែល = ឯកសារ_អ៊ីម៉ែល() + ចន្លោះប្រហោង_តំលៃ * 16384
    ម៉ាស៊ីន.ម៉ូនីទ័រ_តំលៃ.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(អ៊ីម៉ែល, ដាក់ទំហំ, ផ្លូវ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ផ្លូវ.exists() and ផ្លូវ.stat().st_size == ដាក់ទំហំ:
            return ផ្លូវ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, ណិតវឺក_តំលៃ=False)
    ការវាស់វែង = {}
    try:
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        មាតិកា_តំលៃ = '''public class Calc {
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
        កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'Calc.java', មាតិកា_តំលៃ)
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        លទ្ធផល = ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ការវាស់វែង['guest_output'] = លទ្ធផល
        ការបញ្ចូល_បញ្ជី = ម៉ាស៊ីន.ពាក្យ_បញ្ជា('ls', ['Calc.class'])
        ដាក់ទំហំ = int(re.search(r'Calc\.class\s+(\d+) bytes', ការបញ្ចូល_បញ្ជី).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as បញ្ជី_តំលៃ:
            ផ្លូវ = Path(បញ្ជី_តំលៃ) / 'Calc.class'
            ទិន្នន័យ = ភ្ញៀវ_ឯកសារ(ម៉ាស៊ីន, 3, ដាក់ទំហំ, ផ្លូវ)
            ដែលពិត_ទិន្នន័យ = subprocess.check_output(['java', '-Xverify:all', '-cp', បញ្ជី_តំលៃ, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ដែលពិត_ទិន្នន័យ.splitlines() == 기대, ដែលពិត_ទិន្នន័យ
            ការវាស់វែង['class_sha256'] = hashlib.sha256(ទិន្នន័យ).hexdigest()
            ការវាស់វែង['openjdk_output'] = ដែលពិត_ទិន្នន័យ
        # 실패한 កែសម្រួល_តំលៃ/컴파일은 기존 class를 보존한다.
        កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'Calc.java', 'not Java at all', ផ្ទុក_តំលៃ=False)
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for មិនត្រឹមត្រូវ_ការវាស់វែង in [
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
            កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'Calc.java', មិនត្រឹមត្រូវ_ការវាស់វែង)
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Calc.java', ['javac error:', 'Exit: 1'])
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ការធ្វើឡើងវិញ_តំលៃ 실행은 អ្នកប្រើ 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Calc', ['instruction limit', 'Exit: 1'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'Bad.class', 'garbage')
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Bad', ['JVM error:', 'Exit: 1'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('rm Bad.class', ['Removed'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Bad', ['cannot read class: -2'])
        # កែសម្រួល_តំលៃ 입력의 넘친 부분을 잘라서 저장하지 않는다.
        រត់ = len(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
        ម៉ាស៊ីន.직렬.sendall(b'edit Hello.java\n')
        ម៉ាស៊ីន.រង់ចាំ_ភាព('...> ', រត់)
        រត់ = len(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
        ម៉ាស៊ីន.직렬.sendall(b'x' * 129 + b'\n')
        ម៉ាស៊ីន.រង់ចាំ_ភាព('...> ', រត់)
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('.save', ['Too much input; original preserved'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Hello.java', ['Compiled:', 'Exit: 0'])
        កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'f' + str(수), 'occupied')
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
        ការវាស់វែង['serial'] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ការវាស់វែង
    finally:
        ម៉ាស៊ីន.បិទ()


def 주코드(ទិន្នន័យ):
    """손상 시험용 main Code의 ដែលពិត_ទិន្នន័យ ឯកសារ 오프셋/길이만 읽는다."""
    កំណត់ទីតាំង_តំលៃ = 8
    def 짧():
        nonlocal កំណត់ទីតាំង_តំលៃ
        តំលៃ = struct.unpack_from('>H', ទិន្នន័យ, កំណត់ទីតាំង_តំលៃ)[0]
        កំណត់ទីតាំង_តំលៃ += 2
        return តំលៃ
    def 정():
        nonlocal កំណត់ទីតាំង_តំលៃ
        តំលៃ = struct.unpack_from('>I', ទិន្នន័យ, កំណត់ទីតាំង_តំលៃ)[0]
        កំណត់ទីតាំង_តំលៃ += 4
        return តំលៃ
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ទិន្នន័យ[កំណត់ទីតាំង_តំលៃ]
        កំណត់ទីតាំង_តំលៃ += 1
        if 종류 == 1:
            ប្រវែង_តំលៃ = 짧()
            문자들[수] = ទិន្នន័យ[កំណត់ទីតាំង_តំលៃ:កំណត់ទីតាំង_តំលៃ + ប្រវែង_តំលៃ]
            កំណត់ទីតាំង_តំលៃ += ប្រវែង_តំលៃ
        elif 종류 in (7, 8): កំណត់ទីតាំង_តំលៃ += 2
        elif 종류 in (3, 9, 10, 12): កំណត់ទីតាំង_តំលៃ += 4
        else: raise AssertionError(종류)
    កំណត់ទីតាំង_តំលៃ += 6
    개수 = 짧()
    កំណត់ទីតាំង_តំលៃ += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ឈ្មោះ = 짧()
        짧()
        for 수 in range(짧()):
            លក្ខណះ_តំលៃ = 짧()
            ដាក់ទំហំ = 정()
            if 문자들[ឈ្មោះ] == b'main' and 문자들[លក្ខណះ_តំលៃ] == b'Code':
                return កំណត់ទីតាំង_តំលៃ + 8, struct.unpack_from('>I', ទិន្នន័យ, កំណត់ទីតាំង_តំលៃ + 4)[0]
            កំណត់ទីតាំង_តំលៃ += ដាក់ទំហំ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        បញ្ជី_តំលៃ = Path(임시)
        (បញ្ជី_តំលៃ / 'build').mkdir()
        ប្រភព = បញ្ជី_តំលៃ / 'Imported.java'
        ប្រភព.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ប្រភព)], check=True)
        원본 = (បញ្ជី_តំលៃ / 'Imported.class').read_bytes()
        កូដ_តំលៃ, ប្រវែង_តំលៃ = 주코드(원본)
        변형 = {}
        ទិន្នន័យ = bytearray(원본); ទិន្នន័យ[0] = 0; 변형['BadMagic'] = ទិន្នន័យ
        ទិន្នន័យ = bytearray(원본); ទិន្នន័យ[7] = 61; 변형['BadVer'] = ទិន្នន័យ
        ទិន្នន័យ = bytearray(원본); ទិន្នន័យ[8:10] = b'\xff\xff'; 변형['BadPool'] = ទិន្នន័យ
        ទិន្នន័យ = bytearray(원본); ទិន្នន័យ[កូដ_តំលៃ:កូដ_តំលៃ + ប្រវែង_តំលៃ] = bytes(ប្រវែង_តំលៃ)
        ទិន្នន័យ[កូដ_តំលៃ:កូដ_តំលៃ + 3] = b'\xa7\x00\x01'; ទិន្នន័យ[កូដ_តំលៃ + ប្រវែង_តំលៃ - 1] = 177; 변형['BadJump'] = ទិន្នន័យ
        ទិន្នន័យ = bytearray(원본); ទិន្នន័យ[កូដ_តំលៃ:កូដ_តំលៃ + ប្រវែង_តំលៃ] = bytes(ប្រវែង_តំលៃ)
        ទិន្នន័យ[កូដ_តំលៃ] = 87; ទិន្នន័យ[កូដ_តំលៃ + ប្រវែង_តំលៃ - 1] = 177; 변형['BadStack'] = ទិន្នន័យ
        # ឈ្មោះ 검사를 통과시켜 ដែលពិត_ទិន្នន័យ អនុវត្ត_ពាក្យបញ្ជា 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ការបញ្ចូល_តំលៃ = ['Imported.class=' + str(បញ្ជី_តំលៃ / 'Imported.class'), 'Imported.java=' + str(ប្រភព)]
        for ឈ្មោះ, ទិន្នន័យ in 변형.items():
            ផ្លូវ = បញ្ជី_តំលៃ / (ឈ្មោះ + '.class'); ផ្លូវ.write_bytes(ទិន្នន័យ)
            ការបញ្ចូល_តំលៃ.append(ឈ្មោះ + '.class=' + str(ផ្លូវ))
        ក្រុម_តំលៃ = បញ្ជី_តំលៃ / 'build/java-files.bin'
        subprocess.run([sys.executable, str(កំណត់ទីតាំង / 'ឧបករណ៍/자바파일묶기.py'), '-o', str(ក្រុម_តំលៃ)] + ការបញ្ចូល_តំលៃ, check=True)
        subprocess.run(['as', '--32', '-o', str(បញ្ជី_តំលៃ / 'user.o'), str(កំណត់ទីតាំង / '부팅/អ្នកប្រើ.s')], cwd=str(បញ្ជី_តំលៃ), check=True)
        ខឺណេល_តំលៃ = បញ្ជី_តំលៃ / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(កំណត់ទីតាំង / '부팅/តំណ_ប្លង់.ld'), '-o', str(ខឺណេល_តំលៃ),
                        str(កំណត់ទីតាំង / 'build/boot.o'), str(កំណត់ទីតាំង / 'build/java.o'), str(បញ្ជី_តំលៃ / 'user.o'), str(កំណត់ទីតាំង / 'build/apps.o')], check=True)
        ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(ខឺណេល_តំលៃ, ណិតវឺក_តំលៃ=False)
        try:
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('cat Imported.java', ['int[] values = new int[3]'])
            for ឈ្មោះ, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java ' + ឈ្មោះ, [문구, 'Exit: 1'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
        finally:
            ម៉ាស៊ីន.បិទ()


if __name__ == '__main__':
    ញែក_តំលៃ = argparse.ArgumentParser()
    ញែក_តំលៃ.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    អាគុយម៉ង់ = ញែក_តំលៃ.parse_args()
    ការវាស់វែង = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if អាគុយម៉ង់.boot == 'both' else (អាគុយម៉ង់.boot,))}
    ការវាស់វែង['import'] = 적재시험()
    (កំណត់ទីតាំង / 'build/자바시험.json').write_text(json.dumps(ការវាស់វែង, ensure_ascii=False, indent=2) + '\n')
