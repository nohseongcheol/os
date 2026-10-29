#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ýerine_ýetir_buýruk, näsazlyk_baha/gor_baha 경계 시험."""
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
from 사용자통신시험 import hyýaly_kompýuter, 위치


def redaktirle_baha(kompýuter, Ad, Mazmun_baha, Store_baha=True):
    Bitir = len(kompýuter.hasaba_alyş_setir)
    kompýuter.직렬.sendall(('edit ' + Ad + '\n').encode())
    kompýuter.기다림('...> ', Bitir)
    for setir in Mazmun_baha.splitlines():
        assert len(setir) <= 128
        Bitir = len(kompýuter.hasaba_alyş_setir)
        kompýuter.직렬.sendall((setir + '\n').encode())
        kompýuter.기다림('...> ', Bitir)
    Bitir = len(kompýuter.hasaba_alyş_setir)
    kompýuter.직렬.sendall(b'.save\n' if Store_baha else b'.cancel\n')
    결과 = kompýuter.기다림('jkoros> ', Bitir)
    assert ('Saved:' if Store_baha else 'Cancelled; original preserved') in 결과, 결과


def faýl_salgy():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for setir in 결과.splitlines():
        if setir.endswith(' ram_files'):
            return int(setir.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(kompýuter, ýer_baha, Ululyk, Ýol):
    # 시험 VM의 메모리에서 hakyky_maglumat 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    salgy = faýl_salgy() + ýer_baha * 16384
    kompýuter.monitor_baha.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(salgy, Ululyk, Ýol)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Ýol.exists() and Ýol.stat().st_size == Ululyk:
            return Ýol.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    kompýuter = hyýaly_kompýuter(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Tor_baha=False)
    결과 = {}
    try:
        kompýuter.buýruk('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        kompýuter.buýruk('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        kompýuter.buýruk('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        kompýuter.buýruk('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        kompýuter.buýruk('java Missing', ['cannot read class: -2', 'Exit: 1'])
        kompýuter.buýruk('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        kompýuter.buýruk('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Mazmun_baha = '''public class Calc {
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
        redaktirle_baha(kompýuter, 'Calc.java', Mazmun_baha)
        kompýuter.buýruk('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = kompýuter.buýruk('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        girizmeklik_Sanaw = kompýuter.buýruk('ls', ['Calc.class'])
        Ululyk = int(re.search(r'Calc\.class\s+(\d+) bytes', girizmeklik_Sanaw).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as katalog_baha:
            Ýol = Path(katalog_baha) / 'Calc.class'
            maglumat = 게스트파일(kompýuter, 3, Ululyk, Ýol)
            hakyky_maglumat = subprocess.check_output(['java', '-Xverify:all', '-cp', katalog_baha, 'Calc', '6', 'guest'], universal_newlines=True)
            assert hakyky_maglumat.splitlines() == 기대, hakyky_maglumat
            결과['class_sha256'] = hashlib.sha256(maglumat).hexdigest()
            결과['openjdk_output'] = hakyky_maglumat
        # 실패한 redaktirle_baha/컴파일은 기존 class를 보존한다.
        redaktirle_baha(kompýuter, 'Calc.java', 'not Java at all', Store_baha=False)
        kompýuter.buýruk('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            redaktirle_baha(kompýuter, 'Calc.java', 잘못)
            kompýuter.buýruk('javac Calc.java', ['javac error:', 'Exit: 1'])
            kompýuter.buýruk('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # iterasiýa_baha 실행은 ulanyjy 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            kompýuter.buýruk('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        kompýuter.buýruk('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        kompýuter.buýruk('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        redaktirle_baha(kompýuter, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        kompýuter.buýruk('javac Calc.java', ['Compiled:', 'Exit: 0'])
        kompýuter.buýruk('java Calc', ['instruction limit', 'Exit: 1'])
        kompýuter.buýruk('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        redaktirle_baha(kompýuter, 'Bad.class', 'garbage')
        kompýuter.buýruk('java Bad', ['JVM error:', 'Exit: 1'])
        kompýuter.buýruk('rm Bad.class', ['Removed'])
        kompýuter.buýruk('java Bad', ['cannot read class: -2'])
        # redaktirle_baha 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Bitir = len(kompýuter.hasaba_alyş_setir)
        kompýuter.직렬.sendall(b'edit Hello.java\n')
        kompýuter.기다림('...> ', Bitir)
        Bitir = len(kompýuter.hasaba_alyş_setir)
        kompýuter.직렬.sendall(b'x' * 129 + b'\n')
        kompýuter.기다림('...> ', Bitir)
        kompýuter.buýruk('.save', ['Too much input; original preserved'])
        kompýuter.buýruk('javac Hello.java', ['Compiled:', 'Exit: 0'])
        redaktirle_baha(kompýuter, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            redaktirle_baha(kompýuter, 'f' + str(수), 'occupied')
        kompýuter.buýruk('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        kompýuter.buýruk('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in kompýuter.hasaba_alyş_setir.decode('utf-8', 'replace')
        결과['serial'] = kompýuter.hasaba_alyş_setir.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        kompýuter.Ýap()


def 주코드(maglumat):
    """손상 시험용 main Code의 hakyky_maglumat Faýl 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        baha = struct.unpack_from('>H', maglumat, 위치값)[0]
        위치값 += 2
        return baha
    def 정():
        nonlocal 위치값
        baha = struct.unpack_from('>I', maglumat, 위치값)[0]
        위치값 += 4
        return baha
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = maglumat[위치값]
        위치값 += 1
        if 종류 == 1:
            dowamlylyk_baha = 짧()
            문자들[수] = maglumat[위치값:위치값 + dowamlylyk_baha]
            위치값 += dowamlylyk_baha
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Ad = 짧()
        짧()
        for 수 in range(짧()):
            alamat_baha = 짧()
            Ululyk = 정()
            if 문자들[Ad] == b'main' and 문자들[alamat_baha] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', maglumat, 위치값 + 4)[0]
            위치값 += Ululyk
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        katalog_baha = Path(임시)
        (katalog_baha / 'build').mkdir()
        Çeşme = katalog_baha / 'Imported.java'
        Çeşme.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Çeşme)], check=True)
        원본 = (katalog_baha / 'Imported.class').read_bytes()
        코드, dowamlylyk_baha = 주코드(원본)
        변형 = {}
        maglumat = bytearray(원본); maglumat[0] = 0; 변형['BadMagic'] = maglumat
        maglumat = bytearray(원본); maglumat[7] = 61; 변형['BadVer'] = maglumat
        maglumat = bytearray(원본); maglumat[8:10] = b'\xff\xff'; 변형['BadPool'] = maglumat
        maglumat = bytearray(원본); maglumat[코드:코드 + dowamlylyk_baha] = bytes(dowamlylyk_baha)
        maglumat[코드:코드 + 3] = b'\xa7\x00\x01'; maglumat[코드 + dowamlylyk_baha - 1] = 177; 변형['BadJump'] = maglumat
        maglumat = bytearray(원본); maglumat[코드:코드 + dowamlylyk_baha] = bytes(dowamlylyk_baha)
        maglumat[코드] = 87; maglumat[코드 + dowamlylyk_baha - 1] = 177; 변형['BadStack'] = maglumat
        # Ad 검사를 통과시켜 hakyky_maglumat ýerine_ýetir_buýruk 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        girizmeklik_baha = ['Imported.class=' + str(katalog_baha / 'Imported.class'), 'Imported.java=' + str(Çeşme)]
        for Ad, maglumat in 변형.items():
            Ýol = katalog_baha / (Ad + '.class'); Ýol.write_bytes(maglumat)
            girizmeklik_baha.append(Ad + '.class=' + str(Ýol))
        topar_baha = katalog_baha / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Gurallar/자바파일묶기.py'), '-o', str(topar_baha)] + girizmeklik_baha, check=True)
        subprocess.run(['as', '--32', '-o', str(katalog_baha / 'user.o'), str(위치 / '부팅/ulanyjy.s')], cwd=str(katalog_baha), check=True)
        ýadro_baha = katalog_baha / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Bag_Ýerleşiş.ld'), '-o', str(ýadro_baha),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(katalog_baha / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        kompýuter = hyýaly_kompýuter(ýadro_baha, Tor_baha=False)
        try:
            kompýuter.buýruk('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            kompýuter.buýruk('cat Imported.java', ['int[] values = new int[3]'])
            for Ad, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                kompýuter.buýruk('java ' + Ad, [문구, 'Exit: 1'])
                kompýuter.buýruk('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return kompýuter.hasaba_alyş_setir.decode('utf-8', 'replace')
        finally:
            kompýuter.Ýap()


if __name__ == '__main__':
    seljer_baha = argparse.ArgumentParser()
    seljer_baha.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = seljer_baha.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
