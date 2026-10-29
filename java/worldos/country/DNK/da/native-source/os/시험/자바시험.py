#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Udfør_kommando, fejl_VÆRDI/ressource_VÆRDI grænse_VÆRDI 시험."""
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
from test_bruger_netværk import VM, Placering


def Rediger_VÆRDI(maskine, Navn, Indhold_VÆRDI, Store_VÆRDI=True):
    Kør_2 = len(maskine.LOG_post)
    maskine.직렬.sendall(('edit ' + Navn + '\n').encode())
    maskine.ventetilstand('...> ', Kør_2)
    for Linje in Indhold_VÆRDI.splitlines():
        assert len(Linje) <= 128
        Kør_2 = len(maskine.LOG_post)
        maskine.직렬.sendall((Linje + '\n').encode())
        maskine.ventetilstand('...> ', Kør_2)
    Kør_2 = len(maskine.LOG_post)
    maskine.직렬.sendall(b'.save\n' if Store_VÆRDI else b'.cancel\n')
    KR = maskine.ventetilstand('jkoros> ', Kør_2)
    assert ('Saved:' if Store_VÆRDI else 'Cancelled; original preserved') in KR, KR


def fil_mail():
    KR = subprocess.check_output(['nm', '-n', str(Placering / 'build/kernel.elf')], universal_newlines=True)
    for Linje in KR.splitlines():
        if Linje.endswith(' ram_files'):
            return int(Linje.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gæst_fil(maskine, udvidelsesstik_VÆRDI, Størrelse, Sti):
    # 시험 VM의 메모리에서 faktisk_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    mail = fil_mail() + udvidelsesstik_VÆRDI * 16384
    maskine.monitor_VÆRDI.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(mail, Størrelse, Sti)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Sti.exists() and Sti.stat().st_size == Størrelse:
            return Sti.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def testkørsel(종류):
    maskine = VM(Placering / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, netværk_VÆRDI=False)
    KR = {}
    try:
        maskine.Kommando('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        maskine.Kommando('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        maskine.Kommando('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        maskine.Kommando('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        maskine.Kommando('java Missing', ['cannot read class: -2', 'Exit: 1'])
        maskine.Kommando('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        maskine.Kommando('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Indhold_VÆRDI = '''public class Calc {
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
        Rediger_VÆRDI(maskine, 'Calc.java', Indhold_VÆRDI)
        maskine.Kommando('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Udgang = maskine.Kommando('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        KR['guest_output'] = Udgang
        post_Liste = maskine.Kommando('ls', ['Calc.class'])
        Størrelse = int(re.search(r'Calc\.class\s+(\d+) bytes', post_Liste).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as mappe_VÆRDI:
            Sti = Path(mappe_VÆRDI) / 'Calc.class'
            data = gæst_fil(maskine, 3, Størrelse, Sti)
            faktisk_data = subprocess.check_output(['java', '-Xverify:all', '-cp', mappe_VÆRDI, 'Calc', '6', 'guest'], universal_newlines=True)
            assert faktisk_data.splitlines() == 기대, faktisk_data
            KR['class_sha256'] = hashlib.sha256(data).hexdigest()
            KR['openjdk_output'] = faktisk_data
        # 실패한 Rediger_VÆRDI/컴파일은 기존 class를 보존한다.
        Rediger_VÆRDI(maskine, 'Calc.java', 'not Java at all', Store_VÆRDI=False)
        maskine.Kommando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ugyldig_KR in [
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
            Rediger_VÆRDI(maskine, 'Calc.java', ugyldig_KR)
            maskine.Kommando('javac Calc.java', ['javac error:', 'Exit: 1'])
            maskine.Kommando('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VÆRDI 실행은 bruger heap_VÆRDI/프레임을 매번 초기화한다.
        for tal in range(12):
            maskine.Kommando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        maskine.Kommando('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        maskine.Kommando('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Rediger_VÆRDI(maskine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        maskine.Kommando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        maskine.Kommando('java Calc', ['instruction limit', 'Exit: 1'])
        maskine.Kommando('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Rediger_VÆRDI(maskine, 'Bad.class', 'garbage')
        maskine.Kommando('java Bad', ['JVM error:', 'Exit: 1'])
        maskine.Kommando('rm Bad.class', ['Removed'])
        maskine.Kommando('java Bad', ['cannot read class: -2'])
        # Rediger_VÆRDI 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Kør_2 = len(maskine.LOG_post)
        maskine.직렬.sendall(b'edit Hello.java\n')
        maskine.ventetilstand('...> ', Kør_2)
        Kør_2 = len(maskine.LOG_post)
        maskine.직렬.sendall(b'x' * 129 + b'\n')
        maskine.ventetilstand('...> ', Kør_2)
        maskine.Kommando('.save', ['Too much input; original preserved'])
        maskine.Kommando('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Rediger_VÆRDI(maskine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for tal in range(3):
            Rediger_VÆRDI(maskine, 'f' + str(tal), 'occupied')
        maskine.Kommando('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        maskine.Kommando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in maskine.LOG_post.decode('utf-8', 'replace')
        KR['serial'] = maskine.LOG_post.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return KR
    finally:
        maskine.Luk()


def 주코드(data):
    """손상 시험용 main Code의 faktisk_data Fil 오프셋/길이만 읽는다."""
    placere_VÆRDI = 8
    def 짧():
        nonlocal placere_VÆRDI
        VÆRDI = struct.unpack_from('>H', data, placere_VÆRDI)[0]
        placere_VÆRDI += 2
        return VÆRDI
    def 정():
        nonlocal placere_VÆRDI
        VÆRDI = struct.unpack_from('>I', data, placere_VÆRDI)[0]
        placere_VÆRDI += 4
        return VÆRDI
    문자들 = {}
    for tal in range(1, 짧()):
        종류 = data[placere_VÆRDI]
        placere_VÆRDI += 1
        if 종류 == 1:
            varighed_VÆRDI = 짧()
            문자들[tal] = data[placere_VÆRDI:placere_VÆRDI + varighed_VÆRDI]
            placere_VÆRDI += varighed_VÆRDI
        elif 종류 in (7, 8): placere_VÆRDI += 2
        elif 종류 in (3, 9, 10, 12): placere_VÆRDI += 4
        else: raise AssertionError(종류)
    placere_VÆRDI += 6
    vare_TÆL = 짧()
    placere_VÆRDI += vare_TÆL * 2
    assert 짧() == 0
    for tal in range(짧()):
        짧()
        Navn = 짧()
        짧()
        for tal in range(짧()):
            attribut_VÆRDI = 짧()
            Størrelse = 정()
            if 문자들[Navn] == b'main' and 문자들[attribut_VÆRDI] == b'Code':
                return placere_VÆRDI + 8, struct.unpack_from('>I', data, placere_VÆRDI + 4)[0]
            placere_VÆRDI += Størrelse
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        mappe_VÆRDI = Path(임시)
        (mappe_VÆRDI / 'build').mkdir()
        KILDE = mappe_VÆRDI / 'Imported.java'
        KILDE.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(KILDE)], check=True)
        원본 = (mappe_VÆRDI / 'Imported.class').read_bytes()
        KODE_VÆRDI, varighed_VÆRDI = 주코드(원본)
        variant_VÆRDI = {}
        data = bytearray(원본); data[0] = 0; variant_VÆRDI['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; variant_VÆRDI['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; variant_VÆRDI['BadPool'] = data
        data = bytearray(원본); data[KODE_VÆRDI:KODE_VÆRDI + varighed_VÆRDI] = bytes(varighed_VÆRDI)
        data[KODE_VÆRDI:KODE_VÆRDI + 3] = b'\xa7\x00\x01'; data[KODE_VÆRDI + varighed_VÆRDI - 1] = 177; variant_VÆRDI['BadJump'] = data
        data = bytearray(원본); data[KODE_VÆRDI:KODE_VÆRDI + varighed_VÆRDI] = bytes(varighed_VÆRDI)
        data[KODE_VÆRDI] = 87; data[KODE_VÆRDI + varighed_VÆRDI - 1] = 177; variant_VÆRDI['BadStack'] = data
        # Navn 검사를 통과시켜 faktisk_data Udfør_kommando 중의 operand_Stak 오류까지 검사한다.
        variant_VÆRDI['BadStack'] = variant_VÆRDI['BadStack'].replace(b'Imported', b'BadStack')
        post_VÆRDI_962f286b = ['Imported.class=' + str(mappe_VÆRDI / 'Imported.class'), 'Imported.java=' + str(KILDE)]
        for Navn, data in variant_VÆRDI.items():
            Sti = mappe_VÆRDI / (Navn + '.class'); Sti.write_bytes(data)
            post_VÆRDI_962f286b.append(Navn + '.class=' + str(Sti))
        gruppe_VÆRDI = mappe_VÆRDI / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Placering / 'Værktøjer/자바파일묶기.py'), '-o', str(gruppe_VÆRDI)] + post_VÆRDI_962f286b, check=True)
        subprocess.run(['as', '--32', '-o', str(mappe_VÆRDI / 'user.o'), str(Placering / '부팅/bruger.s')], cwd=str(mappe_VÆRDI), check=True)
        kerne_VÆRDI = mappe_VÆRDI / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Placering / '부팅/Link_Layout.ld'), '-o', str(kerne_VÆRDI),
                        str(Placering / 'build/boot.o'), str(Placering / 'build/java.o'), str(mappe_VÆRDI / 'user.o'), str(Placering / 'build/apps.o')], check=True)
        maskine = VM(kerne_VÆRDI, netværk_VÆRDI=False)
        try:
            maskine.Kommando('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            maskine.Kommando('cat Imported.java', ['int[] values = new int[3]'])
            for Navn, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                maskine.Kommando('java ' + Navn, [문구, 'Exit: 1'])
                maskine.Kommando('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return maskine.LOG_post.decode('utf-8', 'replace')
        finally:
            maskine.Luk()


if __name__ == '__main__':
    opdele_tekst_VÆRDI = argparse.ArgumentParser()
    opdele_tekst_VÆRDI.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumenter = opdele_tekst_VÆRDI.parse_args()
    KR = {종류: testkørsel(종류) for 종류 in (('elf', 'iso') if Argumenter.boot == 'both' else (Argumenter.boot,))}
    KR['import'] = 적재시험()
    (Placering / 'build/자바시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n')
