#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 bajarmoq_buyruq, to_xtab_qolish_VALUE/resurs_VALUE 경계 시험."""
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
from 사용자통신시험 import 가상기계, Holati


def tahrirlamoq_VALUE(기계, Nomi, tarkib_VALUE, Store_VALUE=True):
    Bajarish = len(기계.LOG_satr)
    기계.직렬.sendall(('edit ' + Nomi + '\n').encode())
    기계.bir_daqiqa_holat('...> ', Bajarish)
    for satr in tarkib_VALUE.splitlines():
        assert len(satr) <= 128
        Bajarish = len(기계.LOG_satr)
        기계.직렬.sendall((satr + '\n').encode())
        기계.bir_daqiqa_holat('...> ', Bajarish)
    Bajarish = len(기계.LOG_satr)
    기계.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    o_lchov = 기계.bir_daqiqa_holat('jkoros> ', Bajarish)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in o_lchov, o_lchov


def fayl_manzil():
    o_lchov = subprocess.check_output(['nm', '-n', str(Holati / 'build/kernel.elf')], universal_newlines=True)
    for satr in o_lchov.splitlines():
        if satr.endswith(' ram_files'):
            return int(satr.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def mehmon_fayl(기계, in_VALUE, Hajmi, yo_l):
    # 시험 VM의 메모리에서 real_ma_lumotlar 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    manzil = fayl_manzil() + in_VALUE * 16384
    기계.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(manzil, Hajmi, yo_l)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if yo_l.exists() and yo_l.stat().st_size == Hajmi:
            return yo_l.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    기계 = 가상기계(Holati / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Tarmoq_VALUE=False)
    o_lchov = {}
    try:
        기계.Buyruq('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        기계.Buyruq('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        기계.Buyruq('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        기계.Buyruq('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        기계.Buyruq('java Missing', ['cannot read class: -2', 'Exit: 1'])
        기계.Buyruq('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        기계.Buyruq('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        tarkib_VALUE = '''public class Calc {
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
        tahrirlamoq_VALUE(기계, 'Calc.java', tarkib_VALUE)
        기계.Buyruq('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = 기계.Buyruq('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        o_lchov['guest_output'] = 출력
        kiritish_Ro_yxat = 기계.Buyruq('ls', ['Calc.class'])
        Hajmi = int(re.search(r'Calc\.class\s+(\d+) bytes', kiritish_Ro_yxat).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as katalog_VALUE:
            yo_l = Path(katalog_VALUE) / 'Calc.class'
            ma_lumotlar = mehmon_fayl(기계, 3, Hajmi, yo_l)
            real_ma_lumotlar = subprocess.check_output(['java', '-Xverify:all', '-cp', katalog_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert real_ma_lumotlar.splitlines() == 기대, real_ma_lumotlar
            o_lchov['class_sha256'] = hashlib.sha256(ma_lumotlar).hexdigest()
            o_lchov['openjdk_output'] = real_ma_lumotlar
        # 실패한 tahrirlamoq_VALUE/컴파일은 기존 class를 보존한다.
        tahrirlamoq_VALUE(기계, 'Calc.java', 'not Java at all', Store_VALUE=False)
        기계.Buyruq('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for xato_o_lchov in [
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
            tahrirlamoq_VALUE(기계, 'Calc.java', xato_o_lchov)
            기계.Buyruq('javac Calc.java', ['javac error:', 'Exit: 1'])
            기계.Buyruq('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 foydalanuvchi 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            기계.Buyruq('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        기계.Buyruq('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        기계.Buyruq('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        tahrirlamoq_VALUE(기계, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        기계.Buyruq('javac Calc.java', ['Compiled:', 'Exit: 0'])
        기계.Buyruq('java Calc', ['instruction limit', 'Exit: 1'])
        기계.Buyruq('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        tahrirlamoq_VALUE(기계, 'Bad.class', 'garbage')
        기계.Buyruq('java Bad', ['JVM error:', 'Exit: 1'])
        기계.Buyruq('rm Bad.class', ['Removed'])
        기계.Buyruq('java Bad', ['cannot read class: -2'])
        # tahrirlamoq_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Bajarish = len(기계.LOG_satr)
        기계.직렬.sendall(b'edit Hello.java\n')
        기계.bir_daqiqa_holat('...> ', Bajarish)
        Bajarish = len(기계.LOG_satr)
        기계.직렬.sendall(b'x' * 129 + b'\n')
        기계.bir_daqiqa_holat('...> ', Bajarish)
        기계.Buyruq('.save', ['Too much input; original preserved'])
        기계.Buyruq('javac Hello.java', ['Compiled:', 'Exit: 0'])
        tahrirlamoq_VALUE(기계, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            tahrirlamoq_VALUE(기계, 'f' + str(수), 'occupied')
        기계.Buyruq('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        기계.Buyruq('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 기계.LOG_satr.decode('utf-8', 'replace')
        o_lchov['serial'] = 기계.LOG_satr.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return o_lchov
    finally:
        기계.Yopish()


def 주코드(ma_lumotlar):
    """손상 시험용 main Code의 real_ma_lumotlar Fayl 오프셋/길이만 읽는다."""
    holat_VALUE = 8
    def 짧():
        nonlocal holat_VALUE
        VALUE = struct.unpack_from('>H', ma_lumotlar, holat_VALUE)[0]
        holat_VALUE += 2
        return VALUE
    def 정():
        nonlocal holat_VALUE
        VALUE = struct.unpack_from('>I', ma_lumotlar, holat_VALUE)[0]
        holat_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = ma_lumotlar[holat_VALUE]
        holat_VALUE += 1
        if 종류 == 1:
            uzunlik_VALUE = 짧()
            문자들[수] = ma_lumotlar[holat_VALUE:holat_VALUE + uzunlik_VALUE]
            holat_VALUE += uzunlik_VALUE
        elif 종류 in (7, 8): holat_VALUE += 2
        elif 종류 in (3, 9, 10, 12): holat_VALUE += 4
        else: raise AssertionError(종류)
    holat_VALUE += 6
    element_COUNT = 짧()
    holat_VALUE += element_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Nomi = 짧()
        짧()
        for 수 in range(짧()):
            xususiyat_VALUE = 짧()
            Hajmi = 정()
            if 문자들[Nomi] == b'main' and 문자들[xususiyat_VALUE] == b'Code':
                return holat_VALUE + 8, struct.unpack_from('>I', ma_lumotlar, holat_VALUE + 4)[0]
            holat_VALUE += Hajmi
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        katalog_VALUE = Path(임시)
        (katalog_VALUE / 'build').mkdir()
        manba = katalog_VALUE / 'Imported.java'
        manba.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(manba)], check=True)
        원본 = (katalog_VALUE / 'Imported.class').read_bytes()
        kod_VALUE, uzunlik_VALUE = 주코드(원본)
        변형 = {}
        ma_lumotlar = bytearray(원본); ma_lumotlar[0] = 0; 변형['BadMagic'] = ma_lumotlar
        ma_lumotlar = bytearray(원본); ma_lumotlar[7] = 61; 변형['BadVer'] = ma_lumotlar
        ma_lumotlar = bytearray(원본); ma_lumotlar[8:10] = b'\xff\xff'; 변형['BadPool'] = ma_lumotlar
        ma_lumotlar = bytearray(원본); ma_lumotlar[kod_VALUE:kod_VALUE + uzunlik_VALUE] = bytes(uzunlik_VALUE)
        ma_lumotlar[kod_VALUE:kod_VALUE + 3] = b'\xa7\x00\x01'; ma_lumotlar[kod_VALUE + uzunlik_VALUE - 1] = 177; 변형['BadJump'] = ma_lumotlar
        ma_lumotlar = bytearray(원본); ma_lumotlar[kod_VALUE:kod_VALUE + uzunlik_VALUE] = bytes(uzunlik_VALUE)
        ma_lumotlar[kod_VALUE] = 87; ma_lumotlar[kod_VALUE + uzunlik_VALUE - 1] = 177; 변형['BadStack'] = ma_lumotlar
        # Nomi 검사를 통과시켜 real_ma_lumotlar bajarmoq_buyruq 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        kiritish_VALUE = ['Imported.class=' + str(katalog_VALUE / 'Imported.class'), 'Imported.java=' + str(manba)]
        for Nomi, ma_lumotlar in 변형.items():
            yo_l = katalog_VALUE / (Nomi + '.class'); yo_l.write_bytes(ma_lumotlar)
            kiritish_VALUE.append(Nomi + '.class=' + str(yo_l))
        Guruh_VALUE = katalog_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Holati / 'Vositalar/자바파일묶기.py'), '-o', str(Guruh_VALUE)] + kiritish_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(katalog_VALUE / 'user.o'), str(Holati / '부팅/foydalanuvchi.s')], cwd=str(katalog_VALUE), check=True)
        o_zak_VALUE = katalog_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Holati / '부팅/ulash_Maket.ld'), '-o', str(o_zak_VALUE),
                        str(Holati / 'build/boot.o'), str(Holati / 'build/java.o'), str(katalog_VALUE / 'user.o'), str(Holati / 'build/apps.o')], check=True)
        기계 = 가상기계(o_zak_VALUE, Tarmoq_VALUE=False)
        try:
            기계.Buyruq('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            기계.Buyruq('cat Imported.java', ['int[] values = new int[3]'])
            for Nomi, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                기계.Buyruq('java ' + Nomi, [문구, 'Exit: 1'])
                기계.Buyruq('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 기계.LOG_satr.decode('utf-8', 'replace')
        finally:
            기계.Yopish()


if __name__ == '__main__':
    tahlil_qilmoq_VALUE = argparse.ArgumentParser()
    tahlil_qilmoq_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = tahlil_qilmoq_VALUE.parse_args()
    o_lchov = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    o_lchov['import'] = 적재시험()
    (Holati / 'build/자바시험.json').write_text(json.dumps(o_lchov, ensure_ascii=False, indent=2) + '\n')
