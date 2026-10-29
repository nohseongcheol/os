#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 gnìomhaich_àithne, fàilligeadh_VALUE/goireas_VALUE 경계 시험."""
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
from 사용자통신시험 import mas_fhìor_inneal, suidhich


def deasaich_VALUE(inneal, Ainm, susbaint_VALUE, Store_VALUE=True):
    ruith = len(inneal.LOG_ràgh)
    inneal.직렬.sendall(('edit ' + Ainm + '\n').encode())
    inneal.fuirich_cor('...> ', ruith)
    for loidhne in susbaint_VALUE.splitlines():
        assert len(loidhne) <= 128
        ruith = len(inneal.LOG_ràgh)
        inneal.직렬.sendall((loidhne + '\n').encode())
        inneal.fuirich_cor('...> ', ruith)
    ruith = len(inneal.LOG_ràgh)
    inneal.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    tomhas = inneal.fuirich_cor('jkoros> ', ruith)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in tomhas, tomhas


def faidhle_ADDRESS():
    tomhas = subprocess.check_output(['nm', '-n', str(suidhich / 'build/kernel.elf')], universal_newlines=True)
    for loidhne in tomhas.splitlines():
        if loidhne.endswith(' ram_files'):
            return int(loidhne.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def aoigh_faidhle(inneal, slot_VALUE, atharraich_am_meud, Slighe):
    # 시험 VM의 메모리에서 dearbh_dàta 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADDRESS = faidhle_ADDRESS() + slot_VALUE * 16384
    inneal.monatair_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADDRESS, atharraich_am_meud, Slighe)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Slighe.exists() and Slighe.stat().st_size == atharraich_am_meud:
            return Slighe.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    inneal = mas_fhìor_inneal(suidhich / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, lìonra_VALUE=False)
    tomhas = {}
    try:
        inneal.àithne('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        inneal.àithne('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        inneal.àithne('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        inneal.àithne('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        inneal.àithne('java Missing', ['cannot read class: -2', 'Exit: 1'])
        inneal.àithne('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        inneal.àithne('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        susbaint_VALUE = '''public class Calc {
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
        deasaich_VALUE(inneal, 'Calc.java', susbaint_VALUE)
        inneal.àithne('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = inneal.àithne('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        tomhas['guest_output'] = 출력
        cur_a_steach_Liosta = inneal.àithne('ls', ['Calc.class'])
        atharraich_am_meud = int(re.search(r'Calc\.class\s+(\d+) bytes', cur_a_steach_Liosta).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as eòlaire_VALUE:
            Slighe = Path(eòlaire_VALUE) / 'Calc.class'
            dàta = aoigh_faidhle(inneal, 3, atharraich_am_meud, Slighe)
            dearbh_dàta = subprocess.check_output(['java', '-Xverify:all', '-cp', eòlaire_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert dearbh_dàta.splitlines() == 기대, dearbh_dàta
            tomhas['class_sha256'] = hashlib.sha256(dàta).hexdigest()
            tomhas['openjdk_output'] = dearbh_dàta
        # 실패한 deasaich_VALUE/컴파일은 기존 class를 보존한다.
        deasaich_VALUE(inneal, 'Calc.java', 'not Java at all', Store_VALUE=False)
        inneal.àithne('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for mì_dhligheach_tomhas in [
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
            deasaich_VALUE(inneal, 'Calc.java', mì_dhligheach_tomhas)
            inneal.àithne('javac Calc.java', ['javac error:', 'Exit: 1'])
            inneal.àithne('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # ath_thriall_VALUE 실행은 cleachdaiche 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            inneal.àithne('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        inneal.àithne('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        inneal.àithne('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        deasaich_VALUE(inneal, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        inneal.àithne('javac Calc.java', ['Compiled:', 'Exit: 0'])
        inneal.àithne('java Calc', ['instruction limit', 'Exit: 1'])
        inneal.àithne('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        deasaich_VALUE(inneal, 'Bad.class', 'garbage')
        inneal.àithne('java Bad', ['JVM error:', 'Exit: 1'])
        inneal.àithne('rm Bad.class', ['Removed'])
        inneal.àithne('java Bad', ['cannot read class: -2'])
        # deasaich_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ruith = len(inneal.LOG_ràgh)
        inneal.직렬.sendall(b'edit Hello.java\n')
        inneal.fuirich_cor('...> ', ruith)
        ruith = len(inneal.LOG_ràgh)
        inneal.직렬.sendall(b'x' * 129 + b'\n')
        inneal.fuirich_cor('...> ', ruith)
        inneal.àithne('.save', ['Too much input; original preserved'])
        inneal.àithne('javac Hello.java', ['Compiled:', 'Exit: 0'])
        deasaich_VALUE(inneal, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            deasaich_VALUE(inneal, 'f' + str(수), 'occupied')
        inneal.àithne('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        inneal.àithne('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in inneal.LOG_ràgh.decode('utf-8', 'replace')
        tomhas['serial'] = inneal.LOG_ràgh.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return tomhas
    finally:
        inneal.dùin()


def 주코드(dàta):
    """손상 시험용 main Code의 dearbh_dàta faidhle 오프셋/길이만 읽는다."""
    suidhich_VALUE = 8
    def 짧():
        nonlocal suidhich_VALUE
        VALUE = struct.unpack_from('>H', dàta, suidhich_VALUE)[0]
        suidhich_VALUE += 2
        return VALUE
    def 정():
        nonlocal suidhich_VALUE
        VALUE = struct.unpack_from('>I', dàta, suidhich_VALUE)[0]
        suidhich_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = dàta[suidhich_VALUE]
        suidhich_VALUE += 1
        if 종류 == 1:
            faid_VALUE = 짧()
            문자들[수] = dàta[suidhich_VALUE:suidhich_VALUE + faid_VALUE]
            suidhich_VALUE += faid_VALUE
        elif 종류 in (7, 8): suidhich_VALUE += 2
        elif 종류 in (3, 9, 10, 12): suidhich_VALUE += 4
        else: raise AssertionError(종류)
    suidhich_VALUE += 6
    nì_COUNT = 짧()
    suidhich_VALUE += nì_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Ainm = 짧()
        짧()
        for 수 in range(짧()):
            buadh_VALUE = 짧()
            atharraich_am_meud = 정()
            if 문자들[Ainm] == b'main' and 문자들[buadh_VALUE] == b'Code':
                return suidhich_VALUE + 8, struct.unpack_from('>I', dàta, suidhich_VALUE + 4)[0]
            suidhich_VALUE += atharraich_am_meud
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        eòlaire_VALUE = Path(임시)
        (eòlaire_VALUE / 'build').mkdir()
        tùs = eòlaire_VALUE / 'Imported.java'
        tùs.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(tùs)], check=True)
        원본 = (eòlaire_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, faid_VALUE = 주코드(원본)
        변형 = {}
        dàta = bytearray(원본); dàta[0] = 0; 변형['BadMagic'] = dàta
        dàta = bytearray(원본); dàta[7] = 61; 변형['BadVer'] = dàta
        dàta = bytearray(원본); dàta[8:10] = b'\xff\xff'; 변형['BadPool'] = dàta
        dàta = bytearray(원본); dàta[CODE_VALUE:CODE_VALUE + faid_VALUE] = bytes(faid_VALUE)
        dàta[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; dàta[CODE_VALUE + faid_VALUE - 1] = 177; 변형['BadJump'] = dàta
        dàta = bytearray(원본); dàta[CODE_VALUE:CODE_VALUE + faid_VALUE] = bytes(faid_VALUE)
        dàta[CODE_VALUE] = 87; dàta[CODE_VALUE + faid_VALUE - 1] = 177; 변형['BadStack'] = dàta
        # Ainm 검사를 통과시켜 dearbh_dàta gnìomhaich_àithne 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        cur_a_steach_VALUE = ['Imported.class=' + str(eòlaire_VALUE / 'Imported.class'), 'Imported.java=' + str(tùs)]
        for Ainm, dàta in 변형.items():
            Slighe = eòlaire_VALUE / (Ainm + '.class'); Slighe.write_bytes(dàta)
            cur_a_steach_VALUE.append(Ainm + '.class=' + str(Slighe))
        buidheann_VALUE = eòlaire_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(suidhich / 'innealan/자바파일묶기.py'), '-o', str(buidheann_VALUE)] + cur_a_steach_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(eòlaire_VALUE / 'user.o'), str(suidhich / '부팅/cleachdaiche.s')], cwd=str(eòlaire_VALUE), check=True)
        eitean_VALUE = eòlaire_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(suidhich / '부팅/ceangal_co_dhealbhachd.ld'), '-o', str(eitean_VALUE),
                        str(suidhich / 'build/boot.o'), str(suidhich / 'build/java.o'), str(eòlaire_VALUE / 'user.o'), str(suidhich / 'build/apps.o')], check=True)
        inneal = mas_fhìor_inneal(eitean_VALUE, lìonra_VALUE=False)
        try:
            inneal.àithne('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            inneal.àithne('cat Imported.java', ['int[] values = new int[3]'])
            for Ainm, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                inneal.àithne('java ' + Ainm, [문구, 'Exit: 1'])
                inneal.àithne('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return inneal.LOG_ràgh.decode('utf-8', 'replace')
        finally:
            inneal.dùin()


if __name__ == '__main__':
    해석 = argparse.ArgumentParser()
    해석.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = 해석.parse_args()
    tomhas = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    tomhas['import'] = 적재시험()
    (suidhich / 'build/자바시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2) + '\n')
