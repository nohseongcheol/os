#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 diragatsa_Taelo, palelo_Boleng/sediriswa_Boleng 경계 시험."""
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
from 사용자통신시험 import seka_motšhine, 위치


def Tseleganya_Boleng(motšhine, leina, Diteng_Boleng, Store_Boleng=True):
    dirisa = len(motšhine.rekota_mola)
    motšhine.직렬.sendall(('edit ' + leina + '\n').encode())
    motšhine.기다림('...> ', dirisa)
    for Mola in Diteng_Boleng.splitlines():
        assert len(Mola) <= 128
        dirisa = len(motšhine.rekota_mola)
        motšhine.직렬.sendall((Mola + '\n').encode())
        motšhine.기다림('...> ', dirisa)
    dirisa = len(motšhine.rekota_mola)
    motšhine.직렬.sendall(b'.save\n' if Store_Boleng else b'.cancel\n')
    결과 = motšhine.기다림('jkoros> ', dirisa)
    assert ('Saved:' if Store_Boleng else 'Cancelled; original preserved') in 결과, 결과


def faele_aterese():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for Mola in 결과.splitlines():
        if Mola.endswith(' ram_files'):
            return int(Mola.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def moeng_faele(motšhine, sebaka_Boleng, lekanya, tsela):
    # 시험 VM의 메모리에서 tota_tshedimosetso 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    aterese = faele_aterese() + sebaka_Boleng * 16384
    motšhine.monithara_Boleng.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(aterese, lekanya, tsela)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if tsela.exists() and tsela.stat().st_size == lekanya:
            return tsela.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    motšhine = seka_motšhine(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Neteweke_Boleng=False)
    결과 = {}
    try:
        motšhine.Taelo('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        motšhine.Taelo('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        motšhine.Taelo('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        motšhine.Taelo('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        motšhine.Taelo('java Missing', ['cannot read class: -2', 'Exit: 1'])
        motšhine.Taelo('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        motšhine.Taelo('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Diteng_Boleng = '''public class Calc {
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
        Tseleganya_Boleng(motšhine, 'Calc.java', Diteng_Boleng)
        motšhine.Taelo('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = motšhine.Taelo('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        tsenyo_lenaane = motšhine.Taelo('ls', ['Calc.class'])
        lekanya = int(re.search(r'Calc\.class\s+(\d+) bytes', tsenyo_lenaane).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Lenaneofaele_Boleng:
            tsela = Path(Lenaneofaele_Boleng) / 'Calc.class'
            tshedimosetso = moeng_faele(motšhine, 3, lekanya, tsela)
            tota_tshedimosetso = subprocess.check_output(['java', '-Xverify:all', '-cp', Lenaneofaele_Boleng, 'Calc', '6', 'guest'], universal_newlines=True)
            assert tota_tshedimosetso.splitlines() == 기대, tota_tshedimosetso
            결과['class_sha256'] = hashlib.sha256(tshedimosetso).hexdigest()
            결과['openjdk_output'] = tota_tshedimosetso
        # 실패한 Tseleganya_Boleng/컴파일은 기존 class를 보존한다.
        Tseleganya_Boleng(motšhine, 'Calc.java', 'not Java at all', Store_Boleng=False)
        motšhine.Taelo('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            Tseleganya_Boleng(motšhine, 'Calc.java', 잘못)
            motšhine.Taelo('javac Calc.java', ['javac error:', 'Exit: 1'])
            motšhine.Taelo('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # poeletso_Boleng 실행은 modirisi 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            motšhine.Taelo('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        motšhine.Taelo('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        motšhine.Taelo('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Tseleganya_Boleng(motšhine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        motšhine.Taelo('javac Calc.java', ['Compiled:', 'Exit: 0'])
        motšhine.Taelo('java Calc', ['instruction limit', 'Exit: 1'])
        motšhine.Taelo('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Tseleganya_Boleng(motšhine, 'Bad.class', 'garbage')
        motšhine.Taelo('java Bad', ['JVM error:', 'Exit: 1'])
        motšhine.Taelo('rm Bad.class', ['Removed'])
        motšhine.Taelo('java Bad', ['cannot read class: -2'])
        # Tseleganya_Boleng 입력의 넘친 부분을 잘라서 저장하지 않는다.
        dirisa = len(motšhine.rekota_mola)
        motšhine.직렬.sendall(b'edit Hello.java\n')
        motšhine.기다림('...> ', dirisa)
        dirisa = len(motšhine.rekota_mola)
        motšhine.직렬.sendall(b'x' * 129 + b'\n')
        motšhine.기다림('...> ', dirisa)
        motšhine.Taelo('.save', ['Too much input; original preserved'])
        motšhine.Taelo('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Tseleganya_Boleng(motšhine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Tseleganya_Boleng(motšhine, 'f' + str(수), 'occupied')
        motšhine.Taelo('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        motšhine.Taelo('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in motšhine.rekota_mola.decode('utf-8', 'replace')
        결과['serial'] = motšhine.rekota_mola.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        motšhine.tswala()


def 주코드(tshedimosetso):
    """손상 시험용 main Code의 tota_tshedimosetso faele 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        Boleng = struct.unpack_from('>H', tshedimosetso, 위치값)[0]
        위치값 += 2
        return Boleng
    def 정():
        nonlocal 위치값
        Boleng = struct.unpack_from('>I', tshedimosetso, 위치값)[0]
        위치값 += 4
        return Boleng
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = tshedimosetso[위치값]
        위치값 += 1
        if 종류 == 1:
            boleele_Boleng = 짧()
            문자들[수] = tshedimosetso[위치값:위치값 + boleele_Boleng]
            위치값 += boleele_Boleng
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        leina = 짧()
        짧()
        for 수 in range(짧()):
            nonofo_Boleng = 짧()
            lekanya = 정()
            if 문자들[leina] == b'main' and 문자들[nonofo_Boleng] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', tshedimosetso, 위치값 + 4)[0]
            위치값 += lekanya
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Lenaneofaele_Boleng = Path(임시)
        (Lenaneofaele_Boleng / 'build').mkdir()
        Motswedi = Lenaneofaele_Boleng / 'Imported.java'
        Motswedi.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Motswedi)], check=True)
        원본 = (Lenaneofaele_Boleng / 'Imported.class').read_bytes()
        코드, boleele_Boleng = 주코드(원본)
        변형 = {}
        tshedimosetso = bytearray(원본); tshedimosetso[0] = 0; 변형['BadMagic'] = tshedimosetso
        tshedimosetso = bytearray(원본); tshedimosetso[7] = 61; 변형['BadVer'] = tshedimosetso
        tshedimosetso = bytearray(원본); tshedimosetso[8:10] = b'\xff\xff'; 변형['BadPool'] = tshedimosetso
        tshedimosetso = bytearray(원본); tshedimosetso[코드:코드 + boleele_Boleng] = bytes(boleele_Boleng)
        tshedimosetso[코드:코드 + 3] = b'\xa7\x00\x01'; tshedimosetso[코드 + boleele_Boleng - 1] = 177; 변형['BadJump'] = tshedimosetso
        tshedimosetso = bytearray(원본); tshedimosetso[코드:코드 + boleele_Boleng] = bytes(boleele_Boleng)
        tshedimosetso[코드] = 87; tshedimosetso[코드 + boleele_Boleng - 1] = 177; 변형['BadStack'] = tshedimosetso
        # leina 검사를 통과시켜 tota_tshedimosetso diragatsa_Taelo 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        tsenyo_Boleng = ['Imported.class=' + str(Lenaneofaele_Boleng / 'Imported.class'), 'Imported.java=' + str(Motswedi)]
        for leina, tshedimosetso in 변형.items():
            tsela = Lenaneofaele_Boleng / (leina + '.class'); tsela.write_bytes(tshedimosetso)
            tsenyo_Boleng.append(leina + '.class=' + str(tsela))
        setlhopha_Boleng = Lenaneofaele_Boleng / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Thuluse/자바파일묶기.py'), '-o', str(setlhopha_Boleng)] + tsenyo_Boleng, check=True)
        subprocess.run(['as', '--32', '-o', str(Lenaneofaele_Boleng / 'user.o'), str(위치 / '부팅/modirisi.s')], cwd=str(Lenaneofaele_Boleng), check=True)
        Khenele_Boleng = Lenaneofaele_Boleng / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Kgokagano_Boalo.ld'), '-o', str(Khenele_Boleng),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(Lenaneofaele_Boleng / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        motšhine = seka_motšhine(Khenele_Boleng, Neteweke_Boleng=False)
        try:
            motšhine.Taelo('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            motšhine.Taelo('cat Imported.java', ['int[] values = new int[3]'])
            for leina, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                motšhine.Taelo('java ' + leina, [문구, 'Exit: 1'])
                motšhine.Taelo('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return motšhine.rekota_mola.decode('utf-8', 'replace')
        finally:
            motšhine.tswala()


if __name__ == '__main__':
    go_lokolola_Boleng = argparse.ArgumentParser()
    go_lokolola_Boleng.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = go_lokolola_Boleng.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
