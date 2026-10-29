#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 yenza_umyalo, ukwehluleka_inani/insiza_inani 경계 시험."""
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
from 사용자통신시험 import utalagu_umshini, 위치


def hlela_inani(umshini, Igama, Okuqukethwe_inani, Store_inani=True):
    Sebenzisa = len(umshini.loga_umugqa)
    umshini.직렬.sendall(('edit ' + Igama + '\n').encode())
    umshini.기다림('...> ', Sebenzisa)
    for umugqa in Okuqukethwe_inani.splitlines():
        assert len(umugqa) <= 128
        Sebenzisa = len(umshini.loga_umugqa)
        umshini.직렬.sendall((umugqa + '\n').encode())
        umshini.기다림('...> ', Sebenzisa)
    Sebenzisa = len(umshini.loga_umugqa)
    umshini.직렬.sendall(b'.save\n' if Store_inani else b'.cancel\n')
    결과 = umshini.기다림('jkoros> ', Sebenzisa)
    assert ('Saved:' if Store_inani else 'Cancelled; original preserved') in 결과, 결과


def ifayela_ikheli():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for umugqa in 결과.splitlines():
        if umugqa.endswith(' ram_files'):
            return int(umugqa.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def isivakashi_ifayela(umshini, isikhala_inani, Ubungako, Indlela_2):
    # 시험 VM의 메모리에서 ulwazi_ngokwenzekile_imininingwane 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ikheli = ifayela_ikheli() + isikhala_inani * 16384
    umshini.imonitha_inani.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ikheli, Ubungako, Indlela_2)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Indlela_2.exists() and Indlela_2.stat().st_size == Ubungako:
            return Indlela_2.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    umshini = utalagu_umshini(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, iNethiwekhi_inani=False)
    결과 = {}
    try:
        umshini.Umlayelo('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        umshini.Umlayelo('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        umshini.Umlayelo('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        umshini.Umlayelo('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        umshini.Umlayelo('java Missing', ['cannot read class: -2', 'Exit: 1'])
        umshini.Umlayelo('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        umshini.Umlayelo('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Okuqukethwe_inani = '''public class Calc {
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
        hlela_inani(umshini, 'Calc.java', Okuqukethwe_inani)
        umshini.Umlayelo('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = umshini.Umlayelo('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        okufakwayo_Uhlu = umshini.Umlayelo('ls', ['Calc.class'])
        Ubungako = int(re.search(r'Calc\.class\s+(\d+) bytes', okufakwayo_Uhlu).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as umkhombandlela_inani:
            Indlela_2 = Path(umkhombandlela_inani) / 'Calc.class'
            imininingwane = isivakashi_ifayela(umshini, 3, Ubungako, Indlela_2)
            ulwazi_ngokwenzekile_imininingwane = subprocess.check_output(['java', '-Xverify:all', '-cp', umkhombandlela_inani, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ulwazi_ngokwenzekile_imininingwane.splitlines() == 기대, ulwazi_ngokwenzekile_imininingwane
            결과['class_sha256'] = hashlib.sha256(imininingwane).hexdigest()
            결과['openjdk_output'] = ulwazi_ngokwenzekile_imininingwane
        # 실패한 hlela_inani/컴파일은 기존 class를 보존한다.
        hlela_inani(umshini, 'Calc.java', 'not Java at all', Store_inani=False)
        umshini.Umlayelo('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            hlela_inani(umshini, 'Calc.java', 잘못)
            umshini.Umlayelo('javac Calc.java', ['javac error:', 'Exit: 1'])
            umshini.Umlayelo('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # impinda_inani 실행은 umsebenzisi 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            umshini.Umlayelo('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        umshini.Umlayelo('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        umshini.Umlayelo('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        hlela_inani(umshini, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        umshini.Umlayelo('javac Calc.java', ['Compiled:', 'Exit: 0'])
        umshini.Umlayelo('java Calc', ['instruction limit', 'Exit: 1'])
        umshini.Umlayelo('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        hlela_inani(umshini, 'Bad.class', 'garbage')
        umshini.Umlayelo('java Bad', ['JVM error:', 'Exit: 1'])
        umshini.Umlayelo('rm Bad.class', ['Removed'])
        umshini.Umlayelo('java Bad', ['cannot read class: -2'])
        # hlela_inani 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Sebenzisa = len(umshini.loga_umugqa)
        umshini.직렬.sendall(b'edit Hello.java\n')
        umshini.기다림('...> ', Sebenzisa)
        Sebenzisa = len(umshini.loga_umugqa)
        umshini.직렬.sendall(b'x' * 129 + b'\n')
        umshini.기다림('...> ', Sebenzisa)
        umshini.Umlayelo('.save', ['Too much input; original preserved'])
        umshini.Umlayelo('javac Hello.java', ['Compiled:', 'Exit: 0'])
        hlela_inani(umshini, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            hlela_inani(umshini, 'f' + str(수), 'occupied')
        umshini.Umlayelo('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        umshini.Umlayelo('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in umshini.loga_umugqa.decode('utf-8', 'replace')
        결과['serial'] = umshini.loga_umugqa.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        umshini.Vala()


def 주코드(imininingwane):
    """손상 시험용 main Code의 ulwazi_ngokwenzekile_imininingwane Ihele 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        inani = struct.unpack_from('>H', imininingwane, 위치값)[0]
        위치값 += 2
        return inani
    def 정():
        nonlocal 위치값
        inani = struct.unpack_from('>I', imininingwane, 위치값)[0]
        위치값 += 4
        return inani
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = imininingwane[위치값]
        위치값 += 1
        if 종류 == 1:
            ubude_inani = 짧()
            문자들[수] = imininingwane[위치값:위치값 + ubude_inani]
            위치값 += ubude_inani
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Igama = 짧()
        짧()
        for 수 in range(짧()):
            isibaluli_inani = 짧()
            Ubungako = 정()
            if 문자들[Igama] == b'main' and 문자들[isibaluli_inani] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', imininingwane, 위치값 + 4)[0]
            위치값 += Ubungako
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        umkhombandlela_inani = Path(임시)
        (umkhombandlela_inani / 'build').mkdir()
        umthombo = umkhombandlela_inani / 'Imported.java'
        umthombo.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(umthombo)], check=True)
        원본 = (umkhombandlela_inani / 'Imported.class').read_bytes()
        코드, ubude_inani = 주코드(원본)
        변형 = {}
        imininingwane = bytearray(원본); imininingwane[0] = 0; 변형['BadMagic'] = imininingwane
        imininingwane = bytearray(원본); imininingwane[7] = 61; 변형['BadVer'] = imininingwane
        imininingwane = bytearray(원본); imininingwane[8:10] = b'\xff\xff'; 변형['BadPool'] = imininingwane
        imininingwane = bytearray(원본); imininingwane[코드:코드 + ubude_inani] = bytes(ubude_inani)
        imininingwane[코드:코드 + 3] = b'\xa7\x00\x01'; imininingwane[코드 + ubude_inani - 1] = 177; 변형['BadJump'] = imininingwane
        imininingwane = bytearray(원본); imininingwane[코드:코드 + ubude_inani] = bytes(ubude_inani)
        imininingwane[코드] = 87; imininingwane[코드 + ubude_inani - 1] = 177; 변형['BadStack'] = imininingwane
        # Igama 검사를 통과시켜 ulwazi_ngokwenzekile_imininingwane yenza_umyalo 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        okufakwayo_inani = ['Imported.class=' + str(umkhombandlela_inani / 'Imported.class'), 'Imported.java=' + str(umthombo)]
        for Igama, imininingwane in 변형.items():
            Indlela_2 = umkhombandlela_inani / (Igama + '.class'); Indlela_2.write_bytes(imininingwane)
            okufakwayo_inani.append(Igama + '.class=' + str(Indlela_2))
        iqoqo_inani = umkhombandlela_inani / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Amathuluzi/자바파일묶기.py'), '-o', str(iqoqo_inani)] + okufakwayo_inani, check=True)
        subprocess.run(['as', '--32', '-o', str(umkhombandlela_inani / 'user.o'), str(위치 / '부팅/umsebenzisi.s')], cwd=str(umkhombandlela_inani), check=True)
        ikhenela_inani = umkhombandlela_inani / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/xhuma_I_layout.ld'), '-o', str(ikhenela_inani),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(umkhombandlela_inani / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        umshini = utalagu_umshini(ikhenela_inani, iNethiwekhi_inani=False)
        try:
            umshini.Umlayelo('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            umshini.Umlayelo('cat Imported.java', ['int[] values = new int[3]'])
            for Igama, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                umshini.Umlayelo('java ' + Igama, [문구, 'Exit: 1'])
                umshini.Umlayelo('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return umshini.loga_umugqa.decode('utf-8', 'replace')
        finally:
            umshini.Vala()


if __name__ == '__main__':
    zawula_inani = argparse.ArgumentParser()
    zawula_inani.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = zawula_inani.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
