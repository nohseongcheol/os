#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 def_ndigel, foo_xëyma/Kàttan_xëyma 경계 시험."""
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
from 사용자통신시험 import luy_feeñ_te_jëmmadi_masin, 위치


def soppi_xëyma(masin, tur_253d1510, Këmb_xëyma, Store_xëyma=True):
    daw = len(masin.làq_Dënk)
    masin.직렬.sendall(('edit ' + tur_253d1510 + '\n').encode())
    masin.기다림('...> ', daw)
    for buum in Këmb_xëyma.splitlines():
        assert len(buum) <= 128
        daw = len(masin.làq_Dënk)
        masin.직렬.sendall((buum + '\n').encode())
        masin.기다림('...> ', daw)
    daw = len(masin.làq_Dënk)
    masin.직렬.sendall(b'.save\n' if Store_xëyma else b'.cancel\n')
    결과 = masin.기다림('jkoros> ', daw)
    assert ('Saved:' if Store_xëyma else 'Cancelled; original preserved') in 결과, 결과


def bara_denc_dëkkuwaay():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for buum in 결과.splitlines():
        if buum.endswith(' ram_files'):
            return int(buum.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gan_bara_denc(masin, xar_xar_xëyma, tolluwaay, Yoonu_jëmale):
    # 시험 VM의 메모리에서 liteew_mbir 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    dëkkuwaay = bara_denc_dëkkuwaay() + xar_xar_xëyma * 16384
    masin.wonekaay_xëyma.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(dëkkuwaay, tolluwaay, Yoonu_jëmale)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Yoonu_jëmale.exists() and Yoonu_jëmale.stat().st_size == tolluwaay:
            return Yoonu_jëmale.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    masin = luy_feeñ_te_jëmmadi_masin(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, mbaal_xëyma=False)
    결과 = {}
    try:
        masin.ndigel('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        masin.ndigel('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        masin.ndigel('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        masin.ndigel('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        masin.ndigel('java Missing', ['cannot read class: -2', 'Exit: 1'])
        masin.ndigel('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        masin.ndigel('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Këmb_xëyma = '''public class Calc {
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
        soppi_xëyma(masin, 'Calc.java', Këmb_xëyma)
        masin.ndigel('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = masin.ndigel('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        dugal_xabaar_lim = masin.ndigel('ls', ['Calc.class'])
        tolluwaay = int(re.search(r'Calc\.class\s+(\d+) bytes', dugal_xabaar_lim).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as dàmb_xëyma:
            Yoonu_jëmale = Path(dàmb_xëyma) / 'Calc.class'
            mbir = gan_bara_denc(masin, 3, tolluwaay, Yoonu_jëmale)
            liteew_mbir = subprocess.check_output(['java', '-Xverify:all', '-cp', dàmb_xëyma, 'Calc', '6', 'guest'], universal_newlines=True)
            assert liteew_mbir.splitlines() == 기대, liteew_mbir
            결과['class_sha256'] = hashlib.sha256(mbir).hexdigest()
            결과['openjdk_output'] = liteew_mbir
        # 실패한 soppi_xëyma/컴파일은 기존 class를 보존한다.
        soppi_xëyma(masin, 'Calc.java', 'not Java at all', Store_xëyma=False)
        masin.ndigel('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            soppi_xëyma(masin, 'Calc.java', 잘못)
            masin.ndigel('javac Calc.java', ['javac error:', 'Exit: 1'])
            masin.ndigel('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # baamtu_xëyma 실행은 kiy_jariñoo_internet 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            masin.ndigel('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        masin.ndigel('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        masin.ndigel('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        soppi_xëyma(masin, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        masin.ndigel('javac Calc.java', ['Compiled:', 'Exit: 0'])
        masin.ndigel('java Calc', ['instruction limit', 'Exit: 1'])
        masin.ndigel('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        soppi_xëyma(masin, 'Bad.class', 'garbage')
        masin.ndigel('java Bad', ['JVM error:', 'Exit: 1'])
        masin.ndigel('rm Bad.class', ['Removed'])
        masin.ndigel('java Bad', ['cannot read class: -2'])
        # soppi_xëyma 입력의 넘친 부분을 잘라서 저장하지 않는다.
        daw = len(masin.làq_Dënk)
        masin.직렬.sendall(b'edit Hello.java\n')
        masin.기다림('...> ', daw)
        daw = len(masin.làq_Dënk)
        masin.직렬.sendall(b'x' * 129 + b'\n')
        masin.기다림('...> ', daw)
        masin.ndigel('.save', ['Too much input; original preserved'])
        masin.ndigel('javac Hello.java', ['Compiled:', 'Exit: 0'])
        soppi_xëyma(masin, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            soppi_xëyma(masin, 'f' + str(수), 'occupied')
        masin.ndigel('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        masin.ndigel('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in masin.làq_Dënk.decode('utf-8', 'replace')
        결과['serial'] = masin.làq_Dënk.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        masin.Tej()


def 주코드(mbir):
    """손상 시험용 main Code의 liteew_mbir bara_denc 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        xëyma = struct.unpack_from('>H', mbir, 위치값)[0]
        위치값 += 2
        return xëyma
    def 정():
        nonlocal 위치값
        xëyma = struct.unpack_from('>I', mbir, 위치값)[0]
        위치값 += 4
        return xëyma
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = mbir[위치값]
        위치값 += 1
        if 종류 == 1:
            diir_xëyma = 짧()
            문자들[수] = mbir[위치값:위치값 + diir_xëyma]
            위치값 += diir_xëyma
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        tur_253d1510 = 짧()
        짧()
        for 수 in range(짧()):
            jagle_xëyma = 짧()
            tolluwaay = 정()
            if 문자들[tur_253d1510] == b'main' and 문자들[jagle_xëyma] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', mbir, 위치값 + 4)[0]
            위치값 += tolluwaay
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        dàmb_xëyma = Path(임시)
        (dàmb_xëyma / 'build').mkdir()
        Cosaan = dàmb_xëyma / 'Imported.java'
        Cosaan.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Cosaan)], check=True)
        원본 = (dàmb_xëyma / 'Imported.class').read_bytes()
        코드, diir_xëyma = 주코드(원본)
        변형 = {}
        mbir = bytearray(원본); mbir[0] = 0; 변형['BadMagic'] = mbir
        mbir = bytearray(원본); mbir[7] = 61; 변형['BadVer'] = mbir
        mbir = bytearray(원본); mbir[8:10] = b'\xff\xff'; 변형['BadPool'] = mbir
        mbir = bytearray(원본); mbir[코드:코드 + diir_xëyma] = bytes(diir_xëyma)
        mbir[코드:코드 + 3] = b'\xa7\x00\x01'; mbir[코드 + diir_xëyma - 1] = 177; 변형['BadJump'] = mbir
        mbir = bytearray(원본); mbir[코드:코드 + diir_xëyma] = bytes(diir_xëyma)
        mbir[코드] = 87; mbir[코드 + diir_xëyma - 1] = 177; 변형['BadStack'] = mbir
        # tur_253d1510 검사를 통과시켜 liteew_mbir def_ndigel 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        dugal_xabaar_xëyma = ['Imported.class=' + str(dàmb_xëyma / 'Imported.class'), 'Imported.java=' + str(Cosaan)]
        for tur_253d1510, mbir in 변형.items():
            Yoonu_jëmale = dàmb_xëyma / (tur_253d1510 + '.class'); Yoonu_jëmale.write_bytes(mbir)
            dugal_xabaar_xëyma.append(tur_253d1510 + '.class=' + str(Yoonu_jëmale))
        mboolo_xëyma = dàmb_xëyma / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Jumtukaay_yi/자바파일묶기.py'), '-o', str(mboolo_xëyma)] + dugal_xabaar_xëyma, check=True)
        subprocess.run(['as', '--32', '-o', str(dàmb_xëyma / 'user.o'), str(위치 / '부팅/kiy_jariñoo_internet.s')], cwd=str(dàmb_xëyma), check=True)
        xoox_xëyma = dàmb_xëyma / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/lëkkale_Tëralin.ld'), '-o', str(xoox_xëyma),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(dàmb_xëyma / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        masin = luy_feeñ_te_jëmmadi_masin(xoox_xëyma, mbaal_xëyma=False)
        try:
            masin.ndigel('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            masin.ndigel('cat Imported.java', ['int[] values = new int[3]'])
            for tur_253d1510, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                masin.ndigel('java ' + tur_253d1510, [문구, 'Exit: 1'])
                masin.ndigel('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return masin.làq_Dënk.decode('utf-8', 'replace')
        finally:
            masin.Tej()


if __name__ == '__main__':
    Segg_xëyma = argparse.ArgumentParser()
    Segg_xëyma.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = Segg_xëyma.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
