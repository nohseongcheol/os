#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Rith_ordú, teip_VALUE/acmhainn_VALUE 경계 시험."""
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
from 사용자통신시험 import fíorúil_meaisín, suíomh


def cuir_in_eagar_VALUE(meaisín, Ainm, Inneachar_VALUE, Store_VALUE=True):
    Rith_2 = len(meaisín.LOG_ró)
    meaisín.직렬.sendall(('edit ' + Ainm + '\n').encode())
    meaisín.기다림('...> ', Rith_2)
    for Líne in Inneachar_VALUE.splitlines():
        assert len(Líne) <= 128
        Rith_2 = len(meaisín.LOG_ró)
        meaisín.직렬.sendall((Líne + '\n').encode())
        meaisín.기다림('...> ', Rith_2)
    Rith_2 = len(meaisín.LOG_ró)
    meaisín.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    tomhas = meaisín.기다림('jkoros> ', Rith_2)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in tomhas, tomhas


def comhad_ADDRESS():
    tomhas = subprocess.check_output(['nm', '-n', str(suíomh / 'build/kernel.elf')], universal_newlines=True)
    for Líne in tomhas.splitlines():
        if Líne.endswith(' ram_files'):
            return int(Líne.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def aoi_comhad(meaisín, spás_VALUE, Méid, CONAIR):
    # 시험 VM의 메모리에서 iarbhír_sonraí 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADDRESS = comhad_ADDRESS() + spás_VALUE * 16384
    meaisín.monatóir_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADDRESS, Méid, CONAIR)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if CONAIR.exists() and CONAIR.stat().st_size == Méid:
            return CONAIR.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    meaisín = fíorúil_meaisín(suíomh / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Líonra_VALUE=False)
    tomhas = {}
    try:
        meaisín.Ordú('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        meaisín.Ordú('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        meaisín.Ordú('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        meaisín.Ordú('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        meaisín.Ordú('java Missing', ['cannot read class: -2', 'Exit: 1'])
        meaisín.Ordú('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        meaisín.Ordú('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Inneachar_VALUE = '''public class Calc {
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
        cuir_in_eagar_VALUE(meaisín, 'Calc.java', Inneachar_VALUE)
        meaisín.Ordú('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Aschur = meaisín.Ordú('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        tomhas['guest_output'] = Aschur
        iontráil_Liosta = meaisín.Ordú('ls', ['Calc.class'])
        Méid = int(re.search(r'Calc\.class\s+(\d+) bytes', iontráil_Liosta).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as eolaire_VALUE:
            CONAIR = Path(eolaire_VALUE) / 'Calc.class'
            sonraí = aoi_comhad(meaisín, 3, Méid, CONAIR)
            iarbhír_sonraí = subprocess.check_output(['java', '-Xverify:all', '-cp', eolaire_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert iarbhír_sonraí.splitlines() == 기대, iarbhír_sonraí
            tomhas['class_sha256'] = hashlib.sha256(sonraí).hexdigest()
            tomhas['openjdk_output'] = iarbhír_sonraí
        # 실패한 cuir_in_eagar_VALUE/컴파일은 기존 class를 보존한다.
        cuir_in_eagar_VALUE(meaisín, 'Calc.java', 'not Java at all', Store_VALUE=False)
        meaisín.Ordú('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for neamhbhailí_tomhas in [
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
            cuir_in_eagar_VALUE(meaisín, 'Calc.java', neamhbhailí_tomhas)
            meaisín.Ordú('javac Calc.java', ['javac error:', 'Exit: 1'])
            meaisín.Ordú('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # atriall_VALUE 실행은 úsáideoir 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            meaisín.Ordú('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        meaisín.Ordú('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        meaisín.Ordú('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        cuir_in_eagar_VALUE(meaisín, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        meaisín.Ordú('javac Calc.java', ['Compiled:', 'Exit: 0'])
        meaisín.Ordú('java Calc', ['instruction limit', 'Exit: 1'])
        meaisín.Ordú('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        cuir_in_eagar_VALUE(meaisín, 'Bad.class', 'garbage')
        meaisín.Ordú('java Bad', ['JVM error:', 'Exit: 1'])
        meaisín.Ordú('rm Bad.class', ['Removed'])
        meaisín.Ordú('java Bad', ['cannot read class: -2'])
        # cuir_in_eagar_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Rith_2 = len(meaisín.LOG_ró)
        meaisín.직렬.sendall(b'edit Hello.java\n')
        meaisín.기다림('...> ', Rith_2)
        Rith_2 = len(meaisín.LOG_ró)
        meaisín.직렬.sendall(b'x' * 129 + b'\n')
        meaisín.기다림('...> ', Rith_2)
        meaisín.Ordú('.save', ['Too much input; original preserved'])
        meaisín.Ordú('javac Hello.java', ['Compiled:', 'Exit: 0'])
        cuir_in_eagar_VALUE(meaisín, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            cuir_in_eagar_VALUE(meaisín, 'f' + str(수), 'occupied')
        meaisín.Ordú('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        meaisín.Ordú('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in meaisín.LOG_ró.decode('utf-8', 'replace')
        tomhas['serial'] = meaisín.LOG_ró.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return tomhas
    finally:
        meaisín.Dún()


def 주코드(sonraí):
    """손상 시험용 main Code의 iarbhír_sonraí Comhad 오프셋/길이만 읽는다."""
    suíomh_VALUE = 8
    def 짧():
        nonlocal suíomh_VALUE
        VALUE = struct.unpack_from('>H', sonraí, suíomh_VALUE)[0]
        suíomh_VALUE += 2
        return VALUE
    def 정():
        nonlocal suíomh_VALUE
        VALUE = struct.unpack_from('>I', sonraí, suíomh_VALUE)[0]
        suíomh_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = sonraí[suíomh_VALUE]
        suíomh_VALUE += 1
        if 종류 == 1:
            fad_VALUE = 짧()
            문자들[수] = sonraí[suíomh_VALUE:suíomh_VALUE + fad_VALUE]
            suíomh_VALUE += fad_VALUE
        elif 종류 in (7, 8): suíomh_VALUE += 2
        elif 종류 in (3, 9, 10, 12): suíomh_VALUE += 4
        else: raise AssertionError(종류)
    suíomh_VALUE += 6
    mír_COUNT = 짧()
    suíomh_VALUE += mír_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Ainm = 짧()
        짧()
        for 수 in range(짧()):
            tréith_VALUE = 짧()
            Méid = 정()
            if 문자들[Ainm] == b'main' and 문자들[tréith_VALUE] == b'Code':
                return suíomh_VALUE + 8, struct.unpack_from('>I', sonraí, suíomh_VALUE + 4)[0]
            suíomh_VALUE += Méid
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        eolaire_VALUE = Path(임시)
        (eolaire_VALUE / 'build').mkdir()
        FOINSE = eolaire_VALUE / 'Imported.java'
        FOINSE.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(FOINSE)], check=True)
        원본 = (eolaire_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, fad_VALUE = 주코드(원본)
        변형 = {}
        sonraí = bytearray(원본); sonraí[0] = 0; 변형['BadMagic'] = sonraí
        sonraí = bytearray(원본); sonraí[7] = 61; 변형['BadVer'] = sonraí
        sonraí = bytearray(원본); sonraí[8:10] = b'\xff\xff'; 변형['BadPool'] = sonraí
        sonraí = bytearray(원본); sonraí[CODE_VALUE:CODE_VALUE + fad_VALUE] = bytes(fad_VALUE)
        sonraí[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; sonraí[CODE_VALUE + fad_VALUE - 1] = 177; 변형['BadJump'] = sonraí
        sonraí = bytearray(원본); sonraí[CODE_VALUE:CODE_VALUE + fad_VALUE] = bytes(fad_VALUE)
        sonraí[CODE_VALUE] = 87; sonraí[CODE_VALUE + fad_VALUE - 1] = 177; 변형['BadStack'] = sonraí
        # Ainm 검사를 통과시켜 iarbhír_sonraí Rith_ordú 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        iontráil_VALUE = ['Imported.class=' + str(eolaire_VALUE / 'Imported.class'), 'Imported.java=' + str(FOINSE)]
        for Ainm, sonraí in 변형.items():
            CONAIR = eolaire_VALUE / (Ainm + '.class'); CONAIR.write_bytes(sonraí)
            iontráil_VALUE.append(Ainm + '.class=' + str(CONAIR))
        Grúpa_VALUE = eolaire_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(suíomh / 'Uirlisí/자바파일묶기.py'), '-o', str(Grúpa_VALUE)] + iontráil_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(eolaire_VALUE / 'user.o'), str(suíomh / '부팅/úsáideoir.s')], cwd=str(eolaire_VALUE), check=True)
        eithne_VALUE = eolaire_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(suíomh / '부팅/Nasc_dáileadh.ld'), '-o', str(eithne_VALUE),
                        str(suíomh / 'build/boot.o'), str(suíomh / 'build/java.o'), str(eolaire_VALUE / 'user.o'), str(suíomh / 'build/apps.o')], check=True)
        meaisín = fíorúil_meaisín(eithne_VALUE, Líonra_VALUE=False)
        try:
            meaisín.Ordú('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            meaisín.Ordú('cat Imported.java', ['int[] values = new int[3]'])
            for Ainm, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                meaisín.Ordú('java ' + Ainm, [문구, 'Exit: 1'])
                meaisín.Ordú('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return meaisín.LOG_ró.decode('utf-8', 'replace')
        finally:
            meaisín.Dún()


if __name__ == '__main__':
    parsáil_VALUE = argparse.ArgumentParser()
    parsáil_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argóintí = parsáil_VALUE.parse_args()
    tomhas = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argóintí.boot == 'both' else (Argóintí.boot,))}
    tomhas['import'] = 적재시험()
    (suíomh / 'build/자바시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2) + '\n')
