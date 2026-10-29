#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 mee_nnyemiwu, ọdịdà_valuu/njìàrụọrụ_valuu 경계 시험."""
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
from 사용자통신시험 import kendìnuchè_ngwa_komputa, 위치


def dezìmà_valuu(ngwa_komputa, Aha, ndịnà_valuu, Store_valuu=True):
    Bido = len(ngwa_komputa.ndekọ_NDEKỌ)
    ngwa_komputa.직렬.sendall(('edit ' + Aha + '\n').encode())
    ngwa_komputa.기다림('...> ', Bido)
    for ahịrī in ndịnà_valuu.splitlines():
        assert len(ahịrī) <= 128
        Bido = len(ngwa_komputa.ndekọ_NDEKỌ)
        ngwa_komputa.직렬.sendall((ahịrī + '\n').encode())
        ngwa_komputa.기다림('...> ', Bido)
    Bido = len(ngwa_komputa.ndekọ_NDEKỌ)
    ngwa_komputa.직렬.sendall(b'.save\n' if Store_valuu else b'.cancel\n')
    결과 = ngwa_komputa.기다림('jkoros> ', Bido)
    assert ('Saved:' if Store_valuu else 'Cancelled; original preserved') in 결과, 결과


def ọbọakwụkwọ_àdreèsì():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for ahịrī in 결과.splitlines():
        if ahịrī.endswith(' ram_files'):
            return int(ahịrī.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(ngwa_komputa, oghere_valuu, Ụhara, ụzọ_ozi):
    # 시험 VM의 메모리에서 ǹdịnezie_datà 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    àdreèsì = ọbọakwụkwọ_àdreèsì() + oghere_valuu * 16384
    ngwa_komputa.enyo_kọmputà_valuu.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(àdreèsì, Ụhara, ụzọ_ozi)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ụzọ_ozi.exists() and ụzọ_ozi.stat().st_size == Ụhara:
            return ụzọ_ozi.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Netwọọkụ_valuu=False)
    결과 = {}
    try:
        ngwa_komputa.Ntiiwu('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        ngwa_komputa.Ntiiwu('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        ngwa_komputa.Ntiiwu('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        ngwa_komputa.Ntiiwu('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        ngwa_komputa.Ntiiwu('java Missing', ['cannot read class: -2', 'Exit: 1'])
        ngwa_komputa.Ntiiwu('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        ngwa_komputa.Ntiiwu('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        ndịnà_valuu = '''public class Calc {
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
        dezìmà_valuu(ngwa_komputa, 'Calc.java', ndịnà_valuu)
        ngwa_komputa.Ntiiwu('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = ngwa_komputa.Ntiiwu('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        ndebà_ndepụta = ngwa_komputa.Ntiiwu('ls', ['Calc.class'])
        Ụhara = int(re.search(r'Calc\.class\s+(\d+) bytes', ndebà_ndepụta).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as dàịrektrị_valuu:
            ụzọ_ozi = Path(dàịrektrị_valuu) / 'Calc.class'
            datà = 게스트파일(ngwa_komputa, 3, Ụhara, ụzọ_ozi)
            ǹdịnezie_datà = subprocess.check_output(['java', '-Xverify:all', '-cp', dàịrektrị_valuu, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ǹdịnezie_datà.splitlines() == 기대, ǹdịnezie_datà
            결과['class_sha256'] = hashlib.sha256(datà).hexdigest()
            결과['openjdk_output'] = ǹdịnezie_datà
        # 실패한 dezìmà_valuu/컴파일은 기존 class를 보존한다.
        dezìmà_valuu(ngwa_komputa, 'Calc.java', 'not Java at all', Store_valuu=False)
        ngwa_komputa.Ntiiwu('javac Calc.java', ['Compiled:', 'Exit: 0'])
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
            dezìmà_valuu(ngwa_komputa, 'Calc.java', 잘못)
            ngwa_komputa.Ntiiwu('javac Calc.java', ['javac error:', 'Exit: 1'])
            ngwa_komputa.Ntiiwu('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # memmekwa_valuu 실행은 òjìàrụ 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            ngwa_komputa.Ntiiwu('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        ngwa_komputa.Ntiiwu('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        ngwa_komputa.Ntiiwu('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        dezìmà_valuu(ngwa_komputa, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        ngwa_komputa.Ntiiwu('javac Calc.java', ['Compiled:', 'Exit: 0'])
        ngwa_komputa.Ntiiwu('java Calc', ['instruction limit', 'Exit: 1'])
        ngwa_komputa.Ntiiwu('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        dezìmà_valuu(ngwa_komputa, 'Bad.class', 'garbage')
        ngwa_komputa.Ntiiwu('java Bad', ['JVM error:', 'Exit: 1'])
        ngwa_komputa.Ntiiwu('rm Bad.class', ['Removed'])
        ngwa_komputa.Ntiiwu('java Bad', ['cannot read class: -2'])
        # dezìmà_valuu 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Bido = len(ngwa_komputa.ndekọ_NDEKỌ)
        ngwa_komputa.직렬.sendall(b'edit Hello.java\n')
        ngwa_komputa.기다림('...> ', Bido)
        Bido = len(ngwa_komputa.ndekọ_NDEKỌ)
        ngwa_komputa.직렬.sendall(b'x' * 129 + b'\n')
        ngwa_komputa.기다림('...> ', Bido)
        ngwa_komputa.Ntiiwu('.save', ['Too much input; original preserved'])
        ngwa_komputa.Ntiiwu('javac Hello.java', ['Compiled:', 'Exit: 0'])
        dezìmà_valuu(ngwa_komputa, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            dezìmà_valuu(ngwa_komputa, 'f' + str(수), 'occupied')
        ngwa_komputa.Ntiiwu('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        ngwa_komputa.Ntiiwu('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
        결과['serial'] = ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        ngwa_komputa.Mechie()


def 주코드(datà):
    """손상 시험용 main Code의 ǹdịnezie_datà Faịlụ 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        valuu = struct.unpack_from('>H', datà, 위치값)[0]
        위치값 += 2
        return valuu
    def 정():
        nonlocal 위치값
        valuu = struct.unpack_from('>I', datà, 위치값)[0]
        위치값 += 4
        return valuu
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = datà[위치값]
        위치값 += 1
        if 종류 == 1:
            ogologo_valuu = 짧()
            문자들[수] = datà[위치값:위치값 + ogologo_valuu]
            위치값 += ogologo_valuu
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Aha = 짧()
        짧()
        for 수 in range(짧()):
            njìama_valuu = 짧()
            Ụhara = 정()
            if 문자들[Aha] == b'main' and 문자들[njìama_valuu] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', datà, 위치값 + 4)[0]
            위치값 += Ụhara
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        dàịrektrị_valuu = Path(임시)
        (dàịrektrị_valuu / 'build').mkdir()
        ebensìbịa = dàịrektrị_valuu / 'Imported.java'
        ebensìbịa.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ebensìbịa)], check=True)
        원본 = (dàịrektrị_valuu / 'Imported.class').read_bytes()
        코드, ogologo_valuu = 주코드(원본)
        변형 = {}
        datà = bytearray(원본); datà[0] = 0; 변형['BadMagic'] = datà
        datà = bytearray(원본); datà[7] = 61; 변형['BadVer'] = datà
        datà = bytearray(원본); datà[8:10] = b'\xff\xff'; 변형['BadPool'] = datà
        datà = bytearray(원본); datà[코드:코드 + ogologo_valuu] = bytes(ogologo_valuu)
        datà[코드:코드 + 3] = b'\xa7\x00\x01'; datà[코드 + ogologo_valuu - 1] = 177; 변형['BadJump'] = datà
        datà = bytearray(원본); datà[코드:코드 + ogologo_valuu] = bytes(ogologo_valuu)
        datà[코드] = 87; datà[코드 + ogologo_valuu - 1] = 177; 변형['BadStack'] = datà
        # Aha 검사를 통과시켜 ǹdịnezie_datà mee_nnyemiwu 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ndebà_valuu = ['Imported.class=' + str(dàịrektrị_valuu / 'Imported.class'), 'Imported.java=' + str(ebensìbịa)]
        for Aha, datà in 변형.items():
            ụzọ_ozi = dàịrektrị_valuu / (Aha + '.class'); ụzọ_ozi.write_bytes(datà)
            ndebà_valuu.append(Aha + '.class=' + str(ụzọ_ozi))
        otu_valuu = dàịrektrị_valuu / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Ngwaọrụ/자바파일묶기.py'), '-o', str(otu_valuu)] + ndebà_valuu, check=True)
        subprocess.run(['as', '--32', '-o', str(dàịrektrị_valuu / 'user.o'), str(위치 / '부팅/òjìàrụ.s')], cwd=str(dàịrektrị_valuu), check=True)
        mkpụrụobī_kọmpùta_valuu = dàịrektrị_valuu / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Njikọ_Nhàzi.ld'), '-o', str(mkpụrụobī_kọmpùta_valuu),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(dàịrektrị_valuu / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        ngwa_komputa = kendìnuchè_ngwa_komputa(mkpụrụobī_kọmpùta_valuu, Netwọọkụ_valuu=False)
        try:
            ngwa_komputa.Ntiiwu('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            ngwa_komputa.Ntiiwu('cat Imported.java', ['int[] values = new int[3]'])
            for Aha, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                ngwa_komputa.Ntiiwu('java ' + Aha, [문구, 'Exit: 1'])
                ngwa_komputa.Ntiiwu('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
        finally:
            ngwa_komputa.Mechie()


if __name__ == '__main__':
    kerìsịa_valuu = argparse.ArgumentParser()
    kerìsịa_valuu.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = kerìsịa_valuu.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
