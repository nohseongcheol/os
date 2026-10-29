#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 phethagatša_taelo, go_palelwa_boleng/mothopo_boleng 경계 시험."""
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
from 사용자통신시험 import sethalwa_motšhene, 위치


def rulaganya_boleng(motšhene, Leina, Diteng_boleng, lota_boleng=True):
    Diriša = len(motšhene.pego_rei)
    motšhene.직렬.sendall(('edit ' + Leina + '\n').encode())
    motšhene.기다림('...> ', Diriša)
    for mothaladi in Diteng_boleng.splitlines():
        assert len(mothaladi) <= 128
        Diriša = len(motšhene.pego_rei)
        motšhene.직렬.sendall((mothaladi + '\n').encode())
        motšhene.기다림('...> ', Diriša)
    Diriša = len(motšhene.pego_rei)
    motšhene.직렬.sendall(b'.save\n' if lota_boleng else b'.cancel\n')
    결과 = motšhene.기다림('jkoros> ', Diriša)
    assert ('Saved:' if lota_boleng else 'Cancelled; original preserved') in 결과, 결과


def faele_atrese():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for mothaladi in 결과.splitlines():
        if mothaladi.endswith(' ram_files'):
            return int(mothaladi.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def moeng_faele(motšhene, sekgobana_boleng, Bogolo, Tsejana):
    # 시험 VM의 메모리에서 kgonthe_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    atrese = faele_atrese() + sekgobana_boleng * 16384
    motšhene.mmonithara_boleng.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(atrese, Bogolo, Tsejana)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Tsejana.exists() and Tsejana.stat().st_size == Bogolo:
            return Tsejana.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    motšhene = sethalwa_motšhene(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Netweke_boleng=False)
    결과 = {}
    try:
        motšhene.Taelo('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        motšhene.Taelo('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        motšhene.Taelo('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        motšhene.Taelo('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        motšhene.Taelo('java Missing', ['cannot read class: -2', 'Exit: 1'])
        motšhene.Taelo('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        motšhene.Taelo('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Diteng_boleng = '''public class Calc {
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
        rulaganya_boleng(motšhene, 'Calc.java', Diteng_boleng)
        motšhene.Taelo('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = motšhene.Taelo('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        go_tsenya_tshedimošo_Lenaneo = motšhene.Taelo('ls', ['Calc.class'])
        Bogolo = int(re.search(r'Calc\.class\s+(\d+) bytes', go_tsenya_tshedimošo_Lenaneo).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as lelokelelo_boleng:
            Tsejana = Path(lelokelelo_boleng) / 'Calc.class'
            data = moeng_faele(motšhene, 3, Bogolo, Tsejana)
            kgonthe_data = subprocess.check_output(['java', '-Xverify:all', '-cp', lelokelelo_boleng, 'Calc', '6', 'guest'], universal_newlines=True)
            assert kgonthe_data.splitlines() == 기대, kgonthe_data
            결과['class_sha256'] = hashlib.sha256(data).hexdigest()
            결과['openjdk_output'] = kgonthe_data
        # 실패한 rulaganya_boleng/컴파일은 기존 class를 보존한다.
        rulaganya_boleng(motšhene, 'Calc.java', 'not Java at all', lota_boleng=False)
        motšhene.Taelo('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            rulaganya_boleng(motšhene, 'Calc.java', 잘못)
            motšhene.Taelo('javac Calc.java', ['javac error:', 'Exit: 1'])
            motšhene.Taelo('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # poeletšo_boleng 실행은 mošomiši 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            motšhene.Taelo('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        motšhene.Taelo('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        motšhene.Taelo('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        rulaganya_boleng(motšhene, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        motšhene.Taelo('javac Calc.java', ['Compiled:', 'Exit: 0'])
        motšhene.Taelo('java Calc', ['instruction limit', 'Exit: 1'])
        motšhene.Taelo('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        rulaganya_boleng(motšhene, 'Bad.class', 'garbage')
        motšhene.Taelo('java Bad', ['JVM error:', 'Exit: 1'])
        motšhene.Taelo('rm Bad.class', ['Removed'])
        motšhene.Taelo('java Bad', ['cannot read class: -2'])
        # rulaganya_boleng 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Diriša = len(motšhene.pego_rei)
        motšhene.직렬.sendall(b'edit Hello.java\n')
        motšhene.기다림('...> ', Diriša)
        Diriša = len(motšhene.pego_rei)
        motšhene.직렬.sendall(b'x' * 129 + b'\n')
        motšhene.기다림('...> ', Diriša)
        motšhene.Taelo('.save', ['Too much input; original preserved'])
        motšhene.Taelo('javac Hello.java', ['Compiled:', 'Exit: 0'])
        rulaganya_boleng(motšhene, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            rulaganya_boleng(motšhene, 'f' + str(수), 'occupied')
        motšhene.Taelo('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        motšhene.Taelo('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in motšhene.pego_rei.decode('utf-8', 'replace')
        결과['serial'] = motšhene.pego_rei.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        motšhene.Tswalela()


def 주코드(data):
    """손상 시험용 main Code의 kgonthe_data Faele 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        boleng = struct.unpack_from('>H', data, 위치값)[0]
        위치값 += 2
        return boleng
    def 정():
        nonlocal 위치값
        boleng = struct.unpack_from('>I', data, 위치값)[0]
        위치값 += 4
        return boleng
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = data[위치값]
        위치값 += 1
        if 종류 == 1:
            botelele_boleng = 짧()
            문자들[수] = data[위치값:위치값 + botelele_boleng]
            위치값 += botelele_boleng
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Leina = 짧()
        짧()
        for 수 in range(짧()):
            tlhaodi_ya_faele_boleng = 짧()
            Bogolo = 정()
            if 문자들[Leina] == b'main' and 문자들[tlhaodi_ya_faele_boleng] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', data, 위치값 + 4)[0]
            위치값 += Bogolo
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        lelokelelo_boleng = Path(임시)
        (lelokelelo_boleng / 'build').mkdir()
        mohlodi = lelokelelo_boleng / 'Imported.java'
        mohlodi.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(mohlodi)], check=True)
        원본 = (lelokelelo_boleng / 'Imported.class').read_bytes()
        코드, botelele_boleng = 주코드(원본)
        변형 = {}
        data = bytearray(원본); data[0] = 0; 변형['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; 변형['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; 변형['BadPool'] = data
        data = bytearray(원본); data[코드:코드 + botelele_boleng] = bytes(botelele_boleng)
        data[코드:코드 + 3] = b'\xa7\x00\x01'; data[코드 + botelele_boleng - 1] = 177; 변형['BadJump'] = data
        data = bytearray(원본); data[코드:코드 + botelele_boleng] = bytes(botelele_boleng)
        data[코드] = 87; data[코드 + botelele_boleng - 1] = 177; 변형['BadStack'] = data
        # Leina 검사를 통과시켜 kgonthe_data phethagatša_taelo 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        go_tsenya_tshedimošo_boleng = ['Imported.class=' + str(lelokelelo_boleng / 'Imported.class'), 'Imported.java=' + str(mohlodi)]
        for Leina, data in 변형.items():
            Tsejana = lelokelelo_boleng / (Leina + '.class'); Tsejana.write_bytes(data)
            go_tsenya_tshedimošo_boleng.append(Leina + '.class=' + str(Tsejana))
        sehlopha_boleng = lelokelelo_boleng / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Ditholosi/자바파일묶기.py'), '-o', str(sehlopha_boleng)] + go_tsenya_tshedimošo_boleng, check=True)
        subprocess.run(['as', '--32', '-o', str(lelokelelo_boleng / 'user.o'), str(위치 / '부팅/mošomiši.s')], cwd=str(lelokelelo_boleng), check=True)
        khenele_boleng = lelokelelo_boleng / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/linke_Sebopego.ld'), '-o', str(khenele_boleng),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(lelokelelo_boleng / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        motšhene = sethalwa_motšhene(khenele_boleng, Netweke_boleng=False)
        try:
            motšhene.Taelo('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            motšhene.Taelo('cat Imported.java', ['int[] values = new int[3]'])
            for Leina, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                motšhene.Taelo('java ' + Leina, [문구, 'Exit: 1'])
                motšhene.Taelo('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return motšhene.pego_rei.decode('utf-8', 'replace')
        finally:
            motšhene.Tswalela()


if __name__ == '__main__':
    ripaganya_boleng = argparse.ArgumentParser()
    ripaganya_boleng.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = ripaganya_boleng.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
