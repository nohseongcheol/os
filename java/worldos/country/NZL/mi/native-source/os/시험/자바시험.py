#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 kawe_tono, rahunga_uara/rauemi_uara 경계 시험."""
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
from 사용자통신시험 import mariko_mīhini, tūranga


def whakatika_uara(mīhini, Ingoa, Ihirangi_uara, Store_uara=True):
    whakahaere = len(mīhini.LOG_RECORD)
    mīhini.직렬.sendall(('edit ' + Ingoa + '\n').encode())
    mīhini.기다림('...> ', whakahaere)
    for hononga in Ihirangi_uara.splitlines():
        assert len(hononga) <= 128
        whakahaere = len(mīhini.LOG_RECORD)
        mīhini.직렬.sendall((hononga + '\n').encode())
        mīhini.기다림('...> ', whakahaere)
    whakahaere = len(mīhini.LOG_RECORD)
    mīhini.직렬.sendall(b'.save\n' if Store_uara else b'.cancel\n')
    mēhua = mīhini.기다림('jkoros> ', whakahaere)
    assert ('Saved:' if Store_uara else 'Cancelled; original preserved') in mēhua, mēhua


def kōnae_ADDRESS():
    mēhua = subprocess.check_output(['nm', '-n', str(tūranga / 'build/kernel.elf')], universal_newlines=True)
    for hononga in mēhua.splitlines():
        if hononga.endswith(' ram_files'):
            return int(hononga.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def manuhiri_kōnae(mīhini, kāniwha_uara, rahi, ara):
    # 시험 VM의 메모리에서 tūturu_raraunga 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADDRESS = kōnae_ADDRESS() + kāniwha_uara * 16384
    mīhini.kaupane_uara.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADDRESS, rahi, ara)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ara.exists() and ara.stat().st_size == rahi:
            return ara.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    mīhini = mariko_mīhini(tūranga / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, whatunga_uara=False)
    mēhua = {}
    try:
        mīhini.tono('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        mīhini.tono('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        mīhini.tono('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        mīhini.tono('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        mīhini.tono('java Missing', ['cannot read class: -2', 'Exit: 1'])
        mīhini.tono('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        mīhini.tono('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Ihirangi_uara = '''public class Calc {
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
        whakatika_uara(mīhini, 'Calc.java', Ihirangi_uara)
        mīhini.tono('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = mīhini.tono('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        mēhua['guest_output'] = 출력
        tāurunga_Rārangi = mīhini.tono('ls', ['Calc.class'])
        rahi = int(re.search(r'Calc\.class\s+(\d+) bytes', tāurunga_Rārangi).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as whaiaronga_uara:
            ara = Path(whaiaronga_uara) / 'Calc.class'
            raraunga = manuhiri_kōnae(mīhini, 3, rahi, ara)
            tūturu_raraunga = subprocess.check_output(['java', '-Xverify:all', '-cp', whaiaronga_uara, 'Calc', '6', 'guest'], universal_newlines=True)
            assert tūturu_raraunga.splitlines() == 기대, tūturu_raraunga
            mēhua['class_sha256'] = hashlib.sha256(raraunga).hexdigest()
            mēhua['openjdk_output'] = tūturu_raraunga
        # 실패한 whakatika_uara/컴파일은 기존 class를 보존한다.
        whakatika_uara(mīhini, 'Calc.java', 'not Java at all', Store_uara=False)
        mīhini.tono('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for muhu_mēhua in [
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
            whakatika_uara(mīhini, 'Calc.java', muhu_mēhua)
            mīhini.tono('javac Calc.java', ['javac error:', 'Exit: 1'])
            mīhini.tono('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # whitiauau_uara 실행은 kaiwhakamahi 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            mīhini.tono('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        mīhini.tono('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        mīhini.tono('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        whakatika_uara(mīhini, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        mīhini.tono('javac Calc.java', ['Compiled:', 'Exit: 0'])
        mīhini.tono('java Calc', ['instruction limit', 'Exit: 1'])
        mīhini.tono('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        whakatika_uara(mīhini, 'Bad.class', 'garbage')
        mīhini.tono('java Bad', ['JVM error:', 'Exit: 1'])
        mīhini.tono('rm Bad.class', ['Removed'])
        mīhini.tono('java Bad', ['cannot read class: -2'])
        # whakatika_uara 입력의 넘친 부분을 잘라서 저장하지 않는다.
        whakahaere = len(mīhini.LOG_RECORD)
        mīhini.직렬.sendall(b'edit Hello.java\n')
        mīhini.기다림('...> ', whakahaere)
        whakahaere = len(mīhini.LOG_RECORD)
        mīhini.직렬.sendall(b'x' * 129 + b'\n')
        mīhini.기다림('...> ', whakahaere)
        mīhini.tono('.save', ['Too much input; original preserved'])
        mīhini.tono('javac Hello.java', ['Compiled:', 'Exit: 0'])
        whakatika_uara(mīhini, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            whakatika_uara(mīhini, 'f' + str(수), 'occupied')
        mīhini.tono('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        mīhini.tono('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in mīhini.LOG_RECORD.decode('utf-8', 'replace')
        mēhua['serial'] = mīhini.LOG_RECORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return mēhua
    finally:
        mīhini.Kati()


def 주코드(raraunga):
    """손상 시험용 main Code의 tūturu_raraunga Kōnae 오프셋/길이만 읽는다."""
    tūranga_uara = 8
    def 짧():
        nonlocal tūranga_uara
        uara = struct.unpack_from('>H', raraunga, tūranga_uara)[0]
        tūranga_uara += 2
        return uara
    def 정():
        nonlocal tūranga_uara
        uara = struct.unpack_from('>I', raraunga, tūranga_uara)[0]
        tūranga_uara += 4
        return uara
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = raraunga[tūranga_uara]
        tūranga_uara += 1
        if 종류 == 1:
            roa_uara = 짧()
            문자들[수] = raraunga[tūranga_uara:tūranga_uara + roa_uara]
            tūranga_uara += roa_uara
        elif 종류 in (7, 8): tūranga_uara += 2
        elif 종류 in (3, 9, 10, 12): tūranga_uara += 4
        else: raise AssertionError(종류)
    tūranga_uara += 6
    tuemi_COUNT = 짧()
    tūranga_uara += tuemi_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Ingoa = 짧()
        짧()
        for 수 in range(짧()):
            huanga_uara = 짧()
            rahi = 정()
            if 문자들[Ingoa] == b'main' and 문자들[huanga_uara] == b'Code':
                return tūranga_uara + 8, struct.unpack_from('>I', raraunga, tūranga_uara + 4)[0]
            tūranga_uara += rahi
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        whaiaronga_uara = Path(임시)
        (whaiaronga_uara / 'build').mkdir()
        pūtake = whaiaronga_uara / 'Imported.java'
        pūtake.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(pūtake)], check=True)
        원본 = (whaiaronga_uara / 'Imported.class').read_bytes()
        CODE_uara, roa_uara = 주코드(원본)
        변형 = {}
        raraunga = bytearray(원본); raraunga[0] = 0; 변형['BadMagic'] = raraunga
        raraunga = bytearray(원본); raraunga[7] = 61; 변형['BadVer'] = raraunga
        raraunga = bytearray(원본); raraunga[8:10] = b'\xff\xff'; 변형['BadPool'] = raraunga
        raraunga = bytearray(원본); raraunga[CODE_uara:CODE_uara + roa_uara] = bytes(roa_uara)
        raraunga[CODE_uara:CODE_uara + 3] = b'\xa7\x00\x01'; raraunga[CODE_uara + roa_uara - 1] = 177; 변형['BadJump'] = raraunga
        raraunga = bytearray(원본); raraunga[CODE_uara:CODE_uara + roa_uara] = bytes(roa_uara)
        raraunga[CODE_uara] = 87; raraunga[CODE_uara + roa_uara - 1] = 177; 변형['BadStack'] = raraunga
        # Ingoa 검사를 통과시켜 tūturu_raraunga kawe_tono 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        tāurunga_uara = ['Imported.class=' + str(whaiaronga_uara / 'Imported.class'), 'Imported.java=' + str(pūtake)]
        for Ingoa, raraunga in 변형.items():
            ara = whaiaronga_uara / (Ingoa + '.class'); ara.write_bytes(raraunga)
            tāurunga_uara.append(Ingoa + '.class=' + str(ara))
        rōpū_uara = whaiaronga_uara / 'build/java-files.bin'
        subprocess.run([sys.executable, str(tūranga / 'Ngā_Utauta/자바파일묶기.py'), '-o', str(rōpū_uara)] + tāurunga_uara, check=True)
        subprocess.run(['as', '--32', '-o', str(whaiaronga_uara / 'user.o'), str(tūranga / '부팅/kaiwhakamahi.s')], cwd=str(whaiaronga_uara), check=True)
        kākano_uara_0611a8a8 = whaiaronga_uara / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(tūranga / '부팅/Hono_Tahora.ld'), '-o', str(kākano_uara_0611a8a8),
                        str(tūranga / 'build/boot.o'), str(tūranga / 'build/java.o'), str(whaiaronga_uara / 'user.o'), str(tūranga / 'build/apps.o')], check=True)
        mīhini = mariko_mīhini(kākano_uara_0611a8a8, whatunga_uara=False)
        try:
            mīhini.tono('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            mīhini.tono('cat Imported.java', ['int[] values = new int[3]'])
            for Ingoa, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                mīhini.tono('java ' + Ingoa, [문구, 'Exit: 1'])
                mīhini.tono('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return mīhini.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mīhini.Kati()


if __name__ == '__main__':
    poroporo_uara = argparse.ArgumentParser()
    poroporo_uara.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = poroporo_uara.parse_args()
    mēhua = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    mēhua['import'] = 적재시험()
    (tūranga / 'build/자바시험.json').write_text(json.dumps(mēhua, ensure_ascii=False, indent=2) + '\n')
