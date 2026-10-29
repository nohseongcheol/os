#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 gukora_ibwiriza, kudakora_agaciro/umutungo_agaciro 경계 시험."""
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
from 사용자통신시험 import kidafatika_imashini, 위치


def guhindura_agaciro(imashini, Izina, Ibirimo_agaciro, Store_agaciro=True):
    ihuriro = len(imashini.kubika_umurongo)
    imashini.직렬.sendall(('edit ' + Izina + '\n').encode())
    imashini.기다림('...> ', ihuriro)
    for umurongo in Ibirimo_agaciro.splitlines():
        assert len(umurongo) <= 128
        ihuriro = len(imashini.kubika_umurongo)
        imashini.직렬.sendall((umurongo + '\n').encode())
        imashini.기다림('...> ', ihuriro)
    ihuriro = len(imashini.kubika_umurongo)
    imashini.직렬.sendall(b'.save\n' if Store_agaciro else b'.cancel\n')
    결과 = imashini.기다림('jkoros> ', ihuriro)
    assert ('Saved:' if Store_agaciro else 'Cancelled; original preserved') in 결과, 결과


def dosiye_aderesi():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for umurongo in 결과.splitlines():
        if umurongo.endswith(' ram_files'):
            return int(umurongo.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(imashini, umwanya_agaciro, Ingano, Inzira):
    # 시험 VM의 메모리에서 nyakuri_amakurushingiro 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    aderesi = dosiye_aderesi() + umwanya_agaciro * 16384
    imashini.mugaragaza_agaciro.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(aderesi, Ingano, Inzira)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Inzira.exists() and Inzira.stat().st_size == Ingano:
            return Inzira.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    imashini = kidafatika_imashini(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Urusobemiyoboro_agaciro=False)
    결과 = {}
    try:
        imashini.Icyo_wifuza('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        imashini.Icyo_wifuza('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        imashini.Icyo_wifuza('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        imashini.Icyo_wifuza('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        imashini.Icyo_wifuza('java Missing', ['cannot read class: -2', 'Exit: 1'])
        imashini.Icyo_wifuza('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        imashini.Icyo_wifuza('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Ibirimo_agaciro = '''public class Calc {
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
        guhindura_agaciro(imashini, 'Calc.java', Ibirimo_agaciro)
        imashini.Icyo_wifuza('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = imashini.Icyo_wifuza('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        icyinjizwa_Urutonde = imashini.Icyo_wifuza('ls', ['Calc.class'])
        Ingano = int(re.search(r'Calc\.class\s+(\d+) bytes', icyinjizwa_Urutonde).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ububiko_agaciro_e5561a2b:
            Inzira = Path(ububiko_agaciro_e5561a2b) / 'Calc.class'
            amakurushingiro = 게스트파일(imashini, 3, Ingano, Inzira)
            nyakuri_amakurushingiro = subprocess.check_output(['java', '-Xverify:all', '-cp', ububiko_agaciro_e5561a2b, 'Calc', '6', 'guest'], universal_newlines=True)
            assert nyakuri_amakurushingiro.splitlines() == 기대, nyakuri_amakurushingiro
            결과['class_sha256'] = hashlib.sha256(amakurushingiro).hexdigest()
            결과['openjdk_output'] = nyakuri_amakurushingiro
        # 실패한 guhindura_agaciro/컴파일은 기존 class를 보존한다.
        guhindura_agaciro(imashini, 'Calc.java', 'not Java at all', Store_agaciro=False)
        imashini.Icyo_wifuza('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            guhindura_agaciro(imashini, 'Calc.java', 잘못)
            imashini.Icyo_wifuza('javac Calc.java', ['javac error:', 'Exit: 1'])
            imashini.Icyo_wifuza('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # isubiramo_agaciro 실행은 ukoresha 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            imashini.Icyo_wifuza('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        imashini.Icyo_wifuza('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        imashini.Icyo_wifuza('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        guhindura_agaciro(imashini, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        imashini.Icyo_wifuza('javac Calc.java', ['Compiled:', 'Exit: 0'])
        imashini.Icyo_wifuza('java Calc', ['instruction limit', 'Exit: 1'])
        imashini.Icyo_wifuza('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        guhindura_agaciro(imashini, 'Bad.class', 'garbage')
        imashini.Icyo_wifuza('java Bad', ['JVM error:', 'Exit: 1'])
        imashini.Icyo_wifuza('rm Bad.class', ['Removed'])
        imashini.Icyo_wifuza('java Bad', ['cannot read class: -2'])
        # guhindura_agaciro 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ihuriro = len(imashini.kubika_umurongo)
        imashini.직렬.sendall(b'edit Hello.java\n')
        imashini.기다림('...> ', ihuriro)
        ihuriro = len(imashini.kubika_umurongo)
        imashini.직렬.sendall(b'x' * 129 + b'\n')
        imashini.기다림('...> ', ihuriro)
        imashini.Icyo_wifuza('.save', ['Too much input; original preserved'])
        imashini.Icyo_wifuza('javac Hello.java', ['Compiled:', 'Exit: 0'])
        guhindura_agaciro(imashini, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            guhindura_agaciro(imashini, 'f' + str(수), 'occupied')
        imashini.Icyo_wifuza('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        imashini.Icyo_wifuza('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in imashini.kubika_umurongo.decode('utf-8', 'replace')
        결과['serial'] = imashini.kubika_umurongo.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        imashini.Gufunga()


def 주코드(amakurushingiro):
    """손상 시험용 main Code의 nyakuri_amakurushingiro Idosiye 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        agaciro = struct.unpack_from('>H', amakurushingiro, 위치값)[0]
        위치값 += 2
        return agaciro
    def 정():
        nonlocal 위치값
        agaciro = struct.unpack_from('>I', amakurushingiro, 위치값)[0]
        위치값 += 4
        return agaciro
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = amakurushingiro[위치값]
        위치값 += 1
        if 종류 == 1:
            uburebure_agaciro = 짧()
            문자들[수] = amakurushingiro[위치값:위치값 + uburebure_agaciro]
            위치값 += uburebure_agaciro
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Izina = 짧()
        짧()
        for 수 in range(짧()):
            ikiranga_agaciro = 짧()
            Ingano = 정()
            if 문자들[Izina] == b'main' and 문자들[ikiranga_agaciro] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', amakurushingiro, 위치값 + 4)[0]
            위치값 += Ingano
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ububiko_agaciro_e5561a2b = Path(임시)
        (ububiko_agaciro_e5561a2b / 'build').mkdir()
        Inkomoko = ububiko_agaciro_e5561a2b / 'Imported.java'
        Inkomoko.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Inkomoko)], check=True)
        원본 = (ububiko_agaciro_e5561a2b / 'Imported.class').read_bytes()
        코드, uburebure_agaciro = 주코드(원본)
        변형 = {}
        amakurushingiro = bytearray(원본); amakurushingiro[0] = 0; 변형['BadMagic'] = amakurushingiro
        amakurushingiro = bytearray(원본); amakurushingiro[7] = 61; 변형['BadVer'] = amakurushingiro
        amakurushingiro = bytearray(원본); amakurushingiro[8:10] = b'\xff\xff'; 변형['BadPool'] = amakurushingiro
        amakurushingiro = bytearray(원본); amakurushingiro[코드:코드 + uburebure_agaciro] = bytes(uburebure_agaciro)
        amakurushingiro[코드:코드 + 3] = b'\xa7\x00\x01'; amakurushingiro[코드 + uburebure_agaciro - 1] = 177; 변형['BadJump'] = amakurushingiro
        amakurushingiro = bytearray(원본); amakurushingiro[코드:코드 + uburebure_agaciro] = bytes(uburebure_agaciro)
        amakurushingiro[코드] = 87; amakurushingiro[코드 + uburebure_agaciro - 1] = 177; 변형['BadStack'] = amakurushingiro
        # Izina 검사를 통과시켜 nyakuri_amakurushingiro gukora_ibwiriza 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        icyinjizwa_agaciro = ['Imported.class=' + str(ububiko_agaciro_e5561a2b / 'Imported.class'), 'Imported.java=' + str(Inkomoko)]
        for Izina, amakurushingiro in 변형.items():
            Inzira = ububiko_agaciro_e5561a2b / (Izina + '.class'); Inzira.write_bytes(amakurushingiro)
            icyinjizwa_agaciro.append(Izina + '.class=' + str(Inzira))
        itsinda_agaciro = ububiko_agaciro_e5561a2b / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Ibikoresho/자바파일묶기.py'), '-o', str(itsinda_agaciro)] + icyinjizwa_agaciro, check=True)
        subprocess.run(['as', '--32', '-o', str(ububiko_agaciro_e5561a2b / 'user.o'), str(위치 / '부팅/ukoresha.s')], cwd=str(ububiko_agaciro_e5561a2b), check=True)
        intima_agaciro = ububiko_agaciro_e5561a2b / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Ihuza_Imimerere.ld'), '-o', str(intima_agaciro),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(ububiko_agaciro_e5561a2b / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        imashini = kidafatika_imashini(intima_agaciro, Urusobemiyoboro_agaciro=False)
        try:
            imashini.Icyo_wifuza('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            imashini.Icyo_wifuza('cat Imported.java', ['int[] values = new int[3]'])
            for Izina, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                imashini.Icyo_wifuza('java ' + Izina, [문구, 'Exit: 1'])
                imashini.Icyo_wifuza('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return imashini.kubika_umurongo.decode('utf-8', 'replace')
        finally:
            imashini.Gufunga()


if __name__ == '__main__':
    gusesengura_agaciro = argparse.ArgumentParser()
    gusesengura_agaciro.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = gusesengura_agaciro.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
