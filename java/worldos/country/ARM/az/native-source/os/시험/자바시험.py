#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 icra_etmək_əmr, xəta_VALUE/resurs_VALUE 경계 시험."""
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
from 사용자통신시험 import virtual_maşın, yerinə_qoymaq


def redaktə_VALUE(maşın, Ad, Məzmun_VALUE, Store_VALUE=True):
    İcra_Et = len(maşın.LOG_yaz)
    maşın.직렬.sendall(('edit ' + Ad + '\n').encode())
    maşın.gözlə_vəziyyət('...> ', İcra_Et)
    for Giriş in Məzmun_VALUE.splitlines():
        assert len(Giriş) <= 128
        İcra_Et = len(maşın.LOG_yaz)
        maşın.직렬.sendall((Giriş + '\n').encode())
        maşın.gözlə_vəziyyət('...> ', İcra_Et)
    İcra_Et = len(maşın.LOG_yaz)
    maşın.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    ölçü = maşın.gözlə_vəziyyət('jkoros> ', İcra_Et)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in ölçü, ölçü


def fayl_ünvan():
    ölçü = subprocess.check_output(['nm', '-n', str(yerinə_qoymaq / 'build/kernel.elf')], universal_newlines=True)
    for Giriş in ölçü.splitlines():
        if Giriş.endswith(' ram_files'):
            return int(Giriş.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def qonaq_fayl(maşın, slot_VALUE, Böyüklük, Cığır):
    # 시험 VM의 메모리에서 faktiki_verilənlər 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ünvan = fayl_ünvan() + slot_VALUE * 16384
    maşın.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ünvan, Böyüklük, Cığır)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Cığır.exists() and Cığır.stat().st_size == Böyüklük:
            return Cığır.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    maşın = virtual_maşın(yerinə_qoymaq / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Şəbəkə_VALUE=False)
    ölçü = {}
    try:
        maşın.Əmr('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        maşın.Əmr('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        maşın.Əmr('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        maşın.Əmr('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        maşın.Əmr('java Missing', ['cannot read class: -2', 'Exit: 1'])
        maşın.Əmr('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        maşın.Əmr('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Məzmun_VALUE = '''public class Calc {
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
        redaktə_VALUE(maşın, 'Calc.java', Məzmun_VALUE)
        maşın.Əmr('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = maşın.Əmr('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ölçü['guest_output'] = 출력
        daxiletmə_Siyahı = maşın.Əmr('ls', ['Calc.class'])
        Böyüklük = int(re.search(r'Calc\.class\s+(\d+) bytes', daxiletmə_Siyahı).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as kataloq_VALUE:
            Cığır = Path(kataloq_VALUE) / 'Calc.class'
            verilənlər = qonaq_fayl(maşın, 3, Böyüklük, Cığır)
            faktiki_verilənlər = subprocess.check_output(['java', '-Xverify:all', '-cp', kataloq_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert faktiki_verilənlər.splitlines() == 기대, faktiki_verilənlər
            ölçü['class_sha256'] = hashlib.sha256(verilənlər).hexdigest()
            ölçü['openjdk_output'] = faktiki_verilənlər
        # 실패한 redaktə_VALUE/컴파일은 기존 class를 보존한다.
        redaktə_VALUE(maşın, 'Calc.java', 'not Java at all', Store_VALUE=False)
        maşın.Əmr('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for yanlış_ölçü in [
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
            redaktə_VALUE(maşın, 'Calc.java', yanlış_ölçü)
            maşın.Əmr('javac Calc.java', ['javac error:', 'Exit: 1'])
            maşın.Əmr('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # iterasiya_VALUE 실행은 istifadəçi 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            maşın.Əmr('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        maşın.Əmr('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        maşın.Əmr('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        redaktə_VALUE(maşın, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        maşın.Əmr('javac Calc.java', ['Compiled:', 'Exit: 0'])
        maşın.Əmr('java Calc', ['instruction limit', 'Exit: 1'])
        maşın.Əmr('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        redaktə_VALUE(maşın, 'Bad.class', 'garbage')
        maşın.Əmr('java Bad', ['JVM error:', 'Exit: 1'])
        maşın.Əmr('rm Bad.class', ['Removed'])
        maşın.Əmr('java Bad', ['cannot read class: -2'])
        # redaktə_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        İcra_Et = len(maşın.LOG_yaz)
        maşın.직렬.sendall(b'edit Hello.java\n')
        maşın.gözlə_vəziyyət('...> ', İcra_Et)
        İcra_Et = len(maşın.LOG_yaz)
        maşın.직렬.sendall(b'x' * 129 + b'\n')
        maşın.gözlə_vəziyyət('...> ', İcra_Et)
        maşın.Əmr('.save', ['Too much input; original preserved'])
        maşın.Əmr('javac Hello.java', ['Compiled:', 'Exit: 0'])
        redaktə_VALUE(maşın, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            redaktə_VALUE(maşın, 'f' + str(수), 'occupied')
        maşın.Əmr('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        maşın.Əmr('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in maşın.LOG_yaz.decode('utf-8', 'replace')
        ölçü['serial'] = maşın.LOG_yaz.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ölçü
    finally:
        maşın.Bağla()


def 주코드(verilənlər):
    """손상 시험용 main Code의 faktiki_verilənlər FAYL 오프셋/길이만 읽는다."""
    yerinə_qoymaq_VALUE = 8
    def 짧():
        nonlocal yerinə_qoymaq_VALUE
        VALUE = struct.unpack_from('>H', verilənlər, yerinə_qoymaq_VALUE)[0]
        yerinə_qoymaq_VALUE += 2
        return VALUE
    def 정():
        nonlocal yerinə_qoymaq_VALUE
        VALUE = struct.unpack_from('>I', verilənlər, yerinə_qoymaq_VALUE)[0]
        yerinə_qoymaq_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = verilənlər[yerinə_qoymaq_VALUE]
        yerinə_qoymaq_VALUE += 1
        if 종류 == 1:
            uzunluq_VALUE = 짧()
            문자들[수] = verilənlər[yerinə_qoymaq_VALUE:yerinə_qoymaq_VALUE + uzunluq_VALUE]
            yerinə_qoymaq_VALUE += uzunluq_VALUE
        elif 종류 in (7, 8): yerinə_qoymaq_VALUE += 2
        elif 종류 in (3, 9, 10, 12): yerinə_qoymaq_VALUE += 4
        else: raise AssertionError(종류)
    yerinə_qoymaq_VALUE += 6
    element_COUNT = 짧()
    yerinə_qoymaq_VALUE += element_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Ad = 짧()
        짧()
        for 수 in range(짧()):
            atribut_VALUE = 짧()
            Böyüklük = 정()
            if 문자들[Ad] == b'main' and 문자들[atribut_VALUE] == b'Code':
                return yerinə_qoymaq_VALUE + 8, struct.unpack_from('>I', verilənlər, yerinə_qoymaq_VALUE + 4)[0]
            yerinə_qoymaq_VALUE += Böyüklük
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        kataloq_VALUE = Path(임시)
        (kataloq_VALUE / 'build').mkdir()
        QAYNAQ = kataloq_VALUE / 'Imported.java'
        QAYNAQ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(QAYNAQ)], check=True)
        원본 = (kataloq_VALUE / 'Imported.class').read_bytes()
        kod_VALUE, uzunluq_VALUE = 주코드(원본)
        변형 = {}
        verilənlər = bytearray(원본); verilənlər[0] = 0; 변형['BadMagic'] = verilənlər
        verilənlər = bytearray(원본); verilənlər[7] = 61; 변형['BadVer'] = verilənlər
        verilənlər = bytearray(원본); verilənlər[8:10] = b'\xff\xff'; 변형['BadPool'] = verilənlər
        verilənlər = bytearray(원본); verilənlər[kod_VALUE:kod_VALUE + uzunluq_VALUE] = bytes(uzunluq_VALUE)
        verilənlər[kod_VALUE:kod_VALUE + 3] = b'\xa7\x00\x01'; verilənlər[kod_VALUE + uzunluq_VALUE - 1] = 177; 변형['BadJump'] = verilənlər
        verilənlər = bytearray(원본); verilənlər[kod_VALUE:kod_VALUE + uzunluq_VALUE] = bytes(uzunluq_VALUE)
        verilənlər[kod_VALUE] = 87; verilənlər[kod_VALUE + uzunluq_VALUE - 1] = 177; 변형['BadStack'] = verilənlər
        # Ad 검사를 통과시켜 faktiki_verilənlər icra_etmək_əmr 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        daxiletmə_VALUE = ['Imported.class=' + str(kataloq_VALUE / 'Imported.class'), 'Imported.java=' + str(QAYNAQ)]
        for Ad, verilənlər in 변형.items():
            Cığır = kataloq_VALUE / (Ad + '.class'); Cığır.write_bytes(verilənlər)
            daxiletmə_VALUE.append(Ad + '.class=' + str(Cığır))
        Qrup_VALUE = kataloq_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(yerinə_qoymaq / 'Alətlər/자바파일묶기.py'), '-o', str(Qrup_VALUE)] + daxiletmə_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(kataloq_VALUE / 'user.o'), str(yerinə_qoymaq / '부팅/istifadəçi.s')], cwd=str(kataloq_VALUE), check=True)
        nüvə_VALUE = kataloq_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(yerinə_qoymaq / '부팅/keçid_Düzüm.ld'), '-o', str(nüvə_VALUE),
                        str(yerinə_qoymaq / 'build/boot.o'), str(yerinə_qoymaq / 'build/java.o'), str(kataloq_VALUE / 'user.o'), str(yerinə_qoymaq / 'build/apps.o')], check=True)
        maşın = virtual_maşın(nüvə_VALUE, Şəbəkə_VALUE=False)
        try:
            maşın.Əmr('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            maşın.Əmr('cat Imported.java', ['int[] values = new int[3]'])
            for Ad, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                maşın.Əmr('java ' + Ad, [문구, 'Exit: 1'])
                maşın.Əmr('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return maşın.LOG_yaz.decode('utf-8', 'replace')
        finally:
            maşın.Bağla()


if __name__ == '__main__':
    parselləmək_VALUE = argparse.ArgumentParser()
    parselləmək_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = parselləmək_VALUE.parse_args()
    ölçü = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    ölçü['import'] = 적재시험()
    (yerinə_qoymaq / 'build/자바시험.json').write_text(json.dumps(ölçü, ensure_ascii=False, indent=2) + '\n')
