#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Uitvoeren_opdracht, fout_WAARDE/bron_WAARDE grens_WAARDE tests."""
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
from test_gebruiker_net import VM, positie


def Bewerk_WAARDE(machine, Naam, Inhoud_WAARDE, Store_WAARDE=True):
    starten = len(machine.LOG_RECORD)
    machine.직렬.sendall(('edit ' + Naam + '\n').encode())
    machine.wachtstatus('...> ', starten)
    for invoerregel in Inhoud_WAARDE.splitlines():
        assert len(invoerregel) <= 128
        starten = len(machine.LOG_RECORD)
        machine.직렬.sendall((invoerregel + '\n').encode())
        machine.wachtstatus('...> ', starten)
    starten = len(machine.LOG_RECORD)
    machine.직렬.sendall(b'.save\n' if Store_WAARDE else b'.cancel\n')
    resultaat = machine.wachtstatus('jkoros> ', starten)
    assert ('Saved:' if Store_WAARDE else 'Cancelled; original preserved') in resultaat, resultaat


def Bestand_ADRES():
    resultaat = subprocess.check_output(['nm', '-n', str(positie / 'build/kernel.elf')], universal_newlines=True)
    for invoerregel in resultaat.splitlines():
        if invoerregel.endswith(' ram_files'):
            return int(invoerregel.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gast_Bestand(machine, sleuf_WAARDE, Grootte, pad):
    # tests VM의 메모리에서 werkelijk_gegevens 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADRES = Bestand_ADRES() + sleuf_WAARDE * 16384
    machine.monitor_WAARDE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADRES, Grootte, pad)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if pad.exists() and pad.stat().st_size == Grootte:
            return pad.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def test_uitvoeren(soort_WAARDE):
    machine = VM(positie / ('build/kernel.elf' if soort_WAARDE == 'elf' else 'build/kernel.iso'), soort_WAARDE, net_WAARDE=False)
    resultaat = {}
    try:
        machine.opdracht('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        machine.opdracht('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        machine.opdracht('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        machine.opdracht('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        machine.opdracht('java Missing', ['cannot read class: -2', 'Exit: 1'])
        machine.opdracht('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        machine.opdracht('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Inhoud_WAARDE = '''public class Calc {
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
        Bewerk_WAARDE(machine, 'Calc.java', Inhoud_WAARDE)
        machine.opdracht('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        tekstuitvoer = machine.opdracht('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        resultaat['guest_output'] = tekstuitvoer
        invoer_Lijst_f07b3200 = machine.opdracht('ls', ['Calc.class'])
        Grootte = int(re.search(r'Calc\.class\s+(\d+) bytes', invoer_Lijst_f07b3200).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as map_WAARDE:
            pad = Path(map_WAARDE) / 'Calc.class'
            gegevens = gast_Bestand(machine, 3, Grootte, pad)
            werkelijk_gegevens = subprocess.check_output(['java', '-Xverify:all', '-cp', map_WAARDE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert werkelijk_gegevens.splitlines() == 기대, werkelijk_gegevens
            resultaat['class_sha256'] = hashlib.sha256(gegevens).hexdigest()
            resultaat['openjdk_output'] = werkelijk_gegevens
        # 실패한 Bewerk_WAARDE/컴파일은 기존 class를 보존한다.
        Bewerk_WAARDE(machine, 'Calc.java', 'not Java at all', Store_WAARDE=False)
        machine.opdracht('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for nietig_HR in [
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
            Bewerk_WAARDE(machine, 'Calc.java', nietig_HR)
            machine.opdracht('javac Calc.java', ['javac error:', 'Exit: 1'])
            machine.opdracht('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_WAARDE 실행은 gebruikersruimte heap_WAARDE/프레임을 매번 초기화한다.
        for nummer in range(12):
            machine.opdracht('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        machine.opdracht('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        machine.opdracht('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Bewerk_WAARDE(machine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        machine.opdracht('javac Calc.java', ['Compiled:', 'Exit: 0'])
        machine.opdracht('java Calc', ['instruction limit', 'Exit: 1'])
        machine.opdracht('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Bewerk_WAARDE(machine, 'Bad.class', 'garbage')
        machine.opdracht('java Bad', ['JVM error:', 'Exit: 1'])
        machine.opdracht('rm Bad.class', ['Removed'])
        machine.opdracht('java Bad', ['cannot read class: -2'])
        # Bewerk_WAARDE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        starten = len(machine.LOG_RECORD)
        machine.직렬.sendall(b'edit Hello.java\n')
        machine.wachtstatus('...> ', starten)
        starten = len(machine.LOG_RECORD)
        machine.직렬.sendall(b'x' * 129 + b'\n')
        machine.wachtstatus('...> ', starten)
        machine.opdracht('.save', ['Too much input; original preserved'])
        machine.opdracht('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Bewerk_WAARDE(machine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for nummer in range(3):
            Bewerk_WAARDE(machine, 'f' + str(nummer), 'occupied')
        machine.opdracht('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        machine.opdracht('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in machine.LOG_RECORD.decode('utf-8', 'replace')
        resultaat['serial'] = machine.LOG_RECORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(soort_WAARDE))
        return resultaat
    finally:
        machine.Sluiten()


def 주코드(gegevens):
    """손상 시험용 main Code의 werkelijk_gegevens bestand 오프셋/길이만 읽는다."""
    functie_WAARDE = 8
    def 짧():
        nonlocal functie_WAARDE
        WAARDE = struct.unpack_from('>H', gegevens, functie_WAARDE)[0]
        functie_WAARDE += 2
        return WAARDE
    def 정():
        nonlocal functie_WAARDE
        WAARDE = struct.unpack_from('>I', gegevens, functie_WAARDE)[0]
        functie_WAARDE += 4
        return WAARDE
    문자들 = {}
    for nummer in range(1, 짧()):
        soort_WAARDE = gegevens[functie_WAARDE]
        functie_WAARDE += 1
        if soort_WAARDE == 1:
            tijdsduur_WAARDE = 짧()
            문자들[nummer] = gegevens[functie_WAARDE:functie_WAARDE + tijdsduur_WAARDE]
            functie_WAARDE += tijdsduur_WAARDE
        elif soort_WAARDE in (7, 8): functie_WAARDE += 2
        elif soort_WAARDE in (3, 9, 10, 12): functie_WAARDE += 4
        else: raise AssertionError(soort_WAARDE)
    functie_WAARDE += 6
    item_AANTAL = 짧()
    functie_WAARDE += item_AANTAL * 2
    assert 짧() == 0
    for nummer in range(짧()):
        짧()
        Naam = 짧()
        짧()
        for nummer in range(짧()):
            kenmerkwaarde = 짧()
            Grootte = 정()
            if 문자들[Naam] == b'main' and 문자들[kenmerkwaarde] == b'Code':
                return functie_WAARDE + 8, struct.unpack_from('>I', gegevens, functie_WAARDE + 4)[0]
            functie_WAARDE += Grootte
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        map_WAARDE = Path(임시)
        (map_WAARDE / 'build').mkdir()
        broncode = map_WAARDE / 'Imported.java'
        broncode.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(broncode)], check=True)
        원본 = (map_WAARDE / 'Imported.class').read_bytes()
        CODE_WAARDE, tijdsduur_WAARDE = 주코드(원본)
        variant_WAARDE = {}
        gegevens = bytearray(원본); gegevens[0] = 0; variant_WAARDE['BadMagic'] = gegevens
        gegevens = bytearray(원본); gegevens[7] = 61; variant_WAARDE['BadVer'] = gegevens
        gegevens = bytearray(원본); gegevens[8:10] = b'\xff\xff'; variant_WAARDE['BadPool'] = gegevens
        gegevens = bytearray(원본); gegevens[CODE_WAARDE:CODE_WAARDE + tijdsduur_WAARDE] = bytes(tijdsduur_WAARDE)
        gegevens[CODE_WAARDE:CODE_WAARDE + 3] = b'\xa7\x00\x01'; gegevens[CODE_WAARDE + tijdsduur_WAARDE - 1] = 177; variant_WAARDE['BadJump'] = gegevens
        gegevens = bytearray(원본); gegevens[CODE_WAARDE:CODE_WAARDE + tijdsduur_WAARDE] = bytes(tijdsduur_WAARDE)
        gegevens[CODE_WAARDE] = 87; gegevens[CODE_WAARDE + tijdsduur_WAARDE - 1] = 177; variant_WAARDE['BadStack'] = gegevens
        # Naam 검사를 통과시켜 werkelijk_gegevens Uitvoeren_opdracht 중의 operand_stack 오류까지 검사한다.
        variant_WAARDE['BadStack'] = variant_WAARDE['BadStack'].replace(b'Imported', b'BadStack')
        invoer_WAARDE_962f286b = ['Imported.class=' + str(map_WAARDE / 'Imported.class'), 'Imported.java=' + str(broncode)]
        for Naam, gegevens in variant_WAARDE.items():
            pad = map_WAARDE / (Naam + '.class'); pad.write_bytes(gegevens)
            invoer_WAARDE_962f286b.append(Naam + '.class=' + str(pad))
        Groep_WAARDE = map_WAARDE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(positie / 'hulpmiddelen/자바파일묶기.py'), '-o', str(Groep_WAARDE)] + invoer_WAARDE_962f286b, check=True)
        subprocess.run(['as', '--32', '-o', str(map_WAARDE / 'user.o'), str(positie / 'machineopstart/gebruikersruimte.s')], cwd=str(map_WAARDE), check=True)
        kernel_WAARDE = map_WAARDE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(positie / 'machineopstart/koppelindeling.ld'), '-o', str(kernel_WAARDE),
                        str(positie / 'build/boot.o'), str(positie / 'build/java.o'), str(map_WAARDE / 'user.o'), str(positie / 'build/apps.o')], check=True)
        machine = VM(kernel_WAARDE, net_WAARDE=False)
        try:
            machine.opdracht('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            machine.opdracht('cat Imported.java', ['int[] values = new int[3]'])
            for Naam, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                machine.opdracht('java ' + Naam, [문구, 'Exit: 1'])
                machine.opdracht('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return machine.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            machine.Sluiten()


if __name__ == '__main__':
    parseren_WAARDE = argparse.ArgumentParser()
    parseren_WAARDE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argumenten = parseren_WAARDE.parse_args()
    resultaat = {soort_WAARDE: test_uitvoeren(soort_WAARDE) for soort_WAARDE in (('elf', 'iso') if argumenten.boot == 'both' else (argumenten.boot,))}
    resultaat['import'] = 적재시험()
    (positie / 'build/자바시험.json').write_text(json.dumps(resultaat, ensure_ascii=False, indent=2) + '\n')
