#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 gudanar_Umarni, Kasa_aiki_Daraja/albarkatu_Daraja 경계 시험."""
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
from 사용자통신시험 import Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa, 위치


def gyaran_Daraja(na_ura_mai_kwakwalwa, Suna, kunshiya_Daraja, Ajiye_Daraja=True):
    Tafiyar_da = len(na_ura_mai_kwakwalwa.logu_naɗa)
    na_ura_mai_kwakwalwa.직렬.sendall(('edit ' + Suna + '\n').encode())
    na_ura_mai_kwakwalwa.jira_Matsayi('...> ', Tafiyar_da)
    for Layi in kunshiya_Daraja.splitlines():
        assert len(Layi) <= 128
        Tafiyar_da = len(na_ura_mai_kwakwalwa.logu_naɗa)
        na_ura_mai_kwakwalwa.직렬.sendall((Layi + '\n').encode())
        na_ura_mai_kwakwalwa.jira_Matsayi('...> ', Tafiyar_da)
    Tafiyar_da = len(na_ura_mai_kwakwalwa.logu_naɗa)
    na_ura_mai_kwakwalwa.직렬.sendall(b'.save\n' if Ajiye_Daraja else b'.cancel\n')
    결과 = na_ura_mai_kwakwalwa.jira_Matsayi('jkoros> ', Tafiyar_da)
    assert ('Saved:' if Ajiye_Daraja else 'Cancelled; original preserved') in 결과, 결과


def Fayil_imel():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for Layi in 결과.splitlines():
        if Layi.endswith(' ram_files'):
            return int(Layi.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def baƙo_Fayil(na_ura_mai_kwakwalwa, rami_Daraja, Girma, Hanyar_shiga):
    # 시험 VM의 메모리에서 Na_hakika_Tarin_bayani 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    imel = Fayil_imel() + rami_Daraja * 16384
    na_ura_mai_kwakwalwa.Allon_kwamfuta_Daraja.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(imel, Girma, Hanyar_shiga)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Hanyar_shiga.exists() and Hanyar_shiga.stat().st_size == Girma:
            return Hanyar_shiga.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Hanyar_sadarwa_Daraja=False)
    결과 = {}
    try:
        na_ura_mai_kwakwalwa.Umarni('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        na_ura_mai_kwakwalwa.Umarni('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        na_ura_mai_kwakwalwa.Umarni('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        na_ura_mai_kwakwalwa.Umarni('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        na_ura_mai_kwakwalwa.Umarni('java Missing', ['cannot read class: -2', 'Exit: 1'])
        na_ura_mai_kwakwalwa.Umarni('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        na_ura_mai_kwakwalwa.Umarni('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        kunshiya_Daraja = '''public class Calc {
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
        gyaran_Daraja(na_ura_mai_kwakwalwa, 'Calc.java', kunshiya_Daraja)
        na_ura_mai_kwakwalwa.Umarni('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = na_ura_mai_kwakwalwa.Umarni('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        Mashigar_bayanai_Jeri = na_ura_mai_kwakwalwa.Umarni('ls', ['Calc.class'])
        Girma = int(re.search(r'Calc\.class\s+(\d+) bytes', Mashigar_bayanai_Jeri).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ma_ajiya_Daraja:
            Hanyar_shiga = Path(ma_ajiya_Daraja) / 'Calc.class'
            Tarin_bayani = baƙo_Fayil(na_ura_mai_kwakwalwa, 3, Girma, Hanyar_shiga)
            Na_hakika_Tarin_bayani = subprocess.check_output(['java', '-Xverify:all', '-cp', ma_ajiya_Daraja, 'Calc', '6', 'guest'], universal_newlines=True)
            assert Na_hakika_Tarin_bayani.splitlines() == 기대, Na_hakika_Tarin_bayani
            결과['class_sha256'] = hashlib.sha256(Tarin_bayani).hexdigest()
            결과['openjdk_output'] = Na_hakika_Tarin_bayani
        # 실패한 gyaran_Daraja/컴파일은 기존 class를 보존한다.
        gyaran_Daraja(na_ura_mai_kwakwalwa, 'Calc.java', 'not Java at all', Ajiye_Daraja=False)
        na_ura_mai_kwakwalwa.Umarni('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            gyaran_Daraja(na_ura_mai_kwakwalwa, 'Calc.java', 잘못)
            na_ura_mai_kwakwalwa.Umarni('javac Calc.java', ['javac error:', 'Exit: 1'])
            na_ura_mai_kwakwalwa.Umarni('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sifirint_Daraja 실행은 Mai_anfani_da_kwamfuta 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            na_ura_mai_kwakwalwa.Umarni('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        na_ura_mai_kwakwalwa.Umarni('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        na_ura_mai_kwakwalwa.Umarni('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        gyaran_Daraja(na_ura_mai_kwakwalwa, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        na_ura_mai_kwakwalwa.Umarni('javac Calc.java', ['Compiled:', 'Exit: 0'])
        na_ura_mai_kwakwalwa.Umarni('java Calc', ['instruction limit', 'Exit: 1'])
        na_ura_mai_kwakwalwa.Umarni('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        gyaran_Daraja(na_ura_mai_kwakwalwa, 'Bad.class', 'garbage')
        na_ura_mai_kwakwalwa.Umarni('java Bad', ['JVM error:', 'Exit: 1'])
        na_ura_mai_kwakwalwa.Umarni('rm Bad.class', ['Removed'])
        na_ura_mai_kwakwalwa.Umarni('java Bad', ['cannot read class: -2'])
        # gyaran_Daraja 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Tafiyar_da = len(na_ura_mai_kwakwalwa.logu_naɗa)
        na_ura_mai_kwakwalwa.직렬.sendall(b'edit Hello.java\n')
        na_ura_mai_kwakwalwa.jira_Matsayi('...> ', Tafiyar_da)
        Tafiyar_da = len(na_ura_mai_kwakwalwa.logu_naɗa)
        na_ura_mai_kwakwalwa.직렬.sendall(b'x' * 129 + b'\n')
        na_ura_mai_kwakwalwa.jira_Matsayi('...> ', Tafiyar_da)
        na_ura_mai_kwakwalwa.Umarni('.save', ['Too much input; original preserved'])
        na_ura_mai_kwakwalwa.Umarni('javac Hello.java', ['Compiled:', 'Exit: 0'])
        gyaran_Daraja(na_ura_mai_kwakwalwa, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            gyaran_Daraja(na_ura_mai_kwakwalwa, 'f' + str(수), 'occupied')
        na_ura_mai_kwakwalwa.Umarni('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        na_ura_mai_kwakwalwa.Umarni('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
        결과['serial'] = na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        na_ura_mai_kwakwalwa.Rufe()


def 주코드(Tarin_bayani):
    """손상 시험용 main Code의 Na_hakika_Tarin_bayani Fayil 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        Daraja = struct.unpack_from('>H', Tarin_bayani, 위치값)[0]
        위치값 += 2
        return Daraja
    def 정():
        nonlocal 위치값
        Daraja = struct.unpack_from('>I', Tarin_bayani, 위치값)[0]
        위치값 += 4
        return Daraja
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = Tarin_bayani[위치값]
        위치값 += 1
        if 종류 == 1:
            Tsawo_Daraja = 짧()
            문자들[수] = Tarin_bayani[위치값:위치값 + Tsawo_Daraja]
            위치값 += Tsawo_Daraja
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Suna = 짧()
        짧()
        for 수 in range(짧()):
            siffofi_Daraja = 짧()
            Girma = 정()
            if 문자들[Suna] == b'main' and 문자들[siffofi_Daraja] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', Tarin_bayani, 위치값 + 4)[0]
            위치값 += Girma
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ma_ajiya_Daraja = Path(임시)
        (ma_ajiya_Daraja / 'build').mkdir()
        tushe = ma_ajiya_Daraja / 'Imported.java'
        tushe.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(tushe)], check=True)
        원본 = (ma_ajiya_Daraja / 'Imported.class').read_bytes()
        lambar_sirri_Daraja, Tsawo_Daraja = 주코드(원본)
        변형 = {}
        Tarin_bayani = bytearray(원본); Tarin_bayani[0] = 0; 변형['BadMagic'] = Tarin_bayani
        Tarin_bayani = bytearray(원본); Tarin_bayani[7] = 61; 변형['BadVer'] = Tarin_bayani
        Tarin_bayani = bytearray(원본); Tarin_bayani[8:10] = b'\xff\xff'; 변형['BadPool'] = Tarin_bayani
        Tarin_bayani = bytearray(원본); Tarin_bayani[lambar_sirri_Daraja:lambar_sirri_Daraja + Tsawo_Daraja] = bytes(Tsawo_Daraja)
        Tarin_bayani[lambar_sirri_Daraja:lambar_sirri_Daraja + 3] = b'\xa7\x00\x01'; Tarin_bayani[lambar_sirri_Daraja + Tsawo_Daraja - 1] = 177; 변형['BadJump'] = Tarin_bayani
        Tarin_bayani = bytearray(원본); Tarin_bayani[lambar_sirri_Daraja:lambar_sirri_Daraja + Tsawo_Daraja] = bytes(Tsawo_Daraja)
        Tarin_bayani[lambar_sirri_Daraja] = 87; Tarin_bayani[lambar_sirri_Daraja + Tsawo_Daraja - 1] = 177; 변형['BadStack'] = Tarin_bayani
        # Suna 검사를 통과시켜 Na_hakika_Tarin_bayani gudanar_Umarni 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        Mashigar_bayanai_Daraja = ['Imported.class=' + str(ma_ajiya_Daraja / 'Imported.class'), 'Imported.java=' + str(tushe)]
        for Suna, Tarin_bayani in 변형.items():
            Hanyar_shiga = ma_ajiya_Daraja / (Suna + '.class'); Hanyar_shiga.write_bytes(Tarin_bayani)
            Mashigar_bayanai_Daraja.append(Suna + '.class=' + str(Hanyar_shiga))
        gungu_Daraja = ma_ajiya_Daraja / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Kaya/자바파일묶기.py'), '-o', str(gungu_Daraja)] + Mashigar_bayanai_Daraja, check=True)
        subprocess.run(['as', '--32', '-o', str(ma_ajiya_Daraja / 'user.o'), str(위치 / '부팅/Mai_anfani_da_kwamfuta.s')], cwd=str(ma_ajiya_Daraja), check=True)
        Kwara_Daraja = ma_ajiya_Daraja / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Kafa_Zagaye.ld'), '-o', str(Kwara_Daraja),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(ma_ajiya_Daraja / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(Kwara_Daraja, Hanyar_sadarwa_Daraja=False)
        try:
            na_ura_mai_kwakwalwa.Umarni('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            na_ura_mai_kwakwalwa.Umarni('cat Imported.java', ['int[] values = new int[3]'])
            for Suna, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                na_ura_mai_kwakwalwa.Umarni('java ' + Suna, [문구, 'Exit: 1'])
                na_ura_mai_kwakwalwa.Umarni('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
        finally:
            na_ura_mai_kwakwalwa.Rufe()


if __name__ == '__main__':
    Daddatse_Daraja = argparse.ArgumentParser()
    Daddatse_Daraja.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = Daddatse_Daraja.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
