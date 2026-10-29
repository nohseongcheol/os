#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 végrehajt_parancs, hiba_ÉRTÉK/erőforrás_ÉRTÉK határ_ÉRTÉK 시험."""
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
from teszt_felhasználó_hálózat import VM, Pozíció


def szerkeszt_ÉRTÉK(gép, Név, Tartalom_ÉRTÉK, tár_ÉRTÉK=True):
    Futtatás = len(gép.LOG_REKORD)
    gép.직렬.sendall(('edit ' + Név + '\n').encode())
    gép.várakozóállapot('...> ', Futtatás)
    for Vonal in Tartalom_ÉRTÉK.splitlines():
        assert len(Vonal) <= 128
        Futtatás = len(gép.LOG_REKORD)
        gép.직렬.sendall((Vonal + '\n').encode())
        gép.várakozóállapot('...> ', Futtatás)
    Futtatás = len(gép.LOG_REKORD)
    gép.직렬.sendall(b'.save\n' if tár_ÉRTÉK else b'.cancel\n')
    KR = gép.várakozóállapot('jkoros> ', Futtatás)
    assert ('Saved:' if tár_ÉRTÉK else 'Cancelled; original preserved') in KR, KR


def Fájl_CÍM():
    KR = subprocess.check_output(['nm', '-n', str(Pozíció / 'build/kernel.elf')], universal_newlines=True)
    for Vonal in KR.splitlines():
        if Vonal.endswith(' ram_files'):
            return int(Vonal.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def vendég_Fájl(gép, tárolóhely_ÉRTÉK, Méret, ÚTVONAL):
    # 시험 VM의 메모리에서 tényleges_adat 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    CÍM = Fájl_CÍM() + tárolóhely_ÉRTÉK * 16384
    gép.figyelő_ÉRTÉK.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(CÍM, Méret, ÚTVONAL)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ÚTVONAL.exists() and ÚTVONAL.stat().st_size == Méret:
            return ÚTVONAL.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def teszt_futtat(Altípus_ÉRTÉK):
    gép = VM(Pozíció / ('build/kernel.elf' if Altípus_ÉRTÉK == 'elf' else 'build/kernel.iso'), Altípus_ÉRTÉK, hálózat_ÉRTÉK=False)
    KR = {}
    try:
        gép.Parancs('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        gép.Parancs('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        gép.Parancs('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        gép.Parancs('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        gép.Parancs('java Missing', ['cannot read class: -2', 'Exit: 1'])
        gép.Parancs('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        gép.Parancs('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Tartalom_ÉRTÉK = '''public class Calc {
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
        szerkeszt_ÉRTÉK(gép, 'Calc.java', Tartalom_ÉRTÉK)
        gép.Parancs('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Kimenet = gép.Parancs('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        KR['guest_output'] = Kimenet
        bejegyzés_Lista = gép.Parancs('ls', ['Calc.class'])
        Méret = int(re.search(r'Calc\.class\s+(\d+) bytes', bejegyzés_Lista).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as címtár_ÉRTÉK:
            ÚTVONAL = Path(címtár_ÉRTÉK) / 'Calc.class'
            adat = vendég_Fájl(gép, 3, Méret, ÚTVONAL)
            tényleges_adat = subprocess.check_output(['java', '-Xverify:all', '-cp', címtár_ÉRTÉK, 'Calc', '6', 'guest'], universal_newlines=True)
            assert tényleges_adat.splitlines() == 기대, tényleges_adat
            KR['class_sha256'] = hashlib.sha256(adat).hexdigest()
            KR['openjdk_output'] = tényleges_adat
        # 실패한 szerkeszt_ÉRTÉK/컴파일은 기존 class를 보존한다.
        szerkeszt_ÉRTÉK(gép, 'Calc.java', 'not Java at all', tár_ÉRTÉK=False)
        gép.Parancs('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for alaptalan_KR in [
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
            szerkeszt_ÉRTÉK(gép, 'Calc.java', alaptalan_KR)
            gép.Parancs('javac Calc.java', ['javac error:', 'Exit: 1'])
            gép.Parancs('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # futam_ÉRTÉK 실행은 felhasználó halommemória_ÉRTÉK/프레임을 매번 초기화한다.
        for szám in range(12):
            gép.Parancs('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        gép.Parancs('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        gép.Parancs('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        szerkeszt_ÉRTÉK(gép, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        gép.Parancs('javac Calc.java', ['Compiled:', 'Exit: 0'])
        gép.Parancs('java Calc', ['instruction limit', 'Exit: 1'])
        gép.Parancs('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        szerkeszt_ÉRTÉK(gép, 'Bad.class', 'garbage')
        gép.Parancs('java Bad', ['JVM error:', 'Exit: 1'])
        gép.Parancs('rm Bad.class', ['Removed'])
        gép.Parancs('java Bad', ['cannot read class: -2'])
        # szerkeszt_ÉRTÉK 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Futtatás = len(gép.LOG_REKORD)
        gép.직렬.sendall(b'edit Hello.java\n')
        gép.várakozóállapot('...> ', Futtatás)
        Futtatás = len(gép.LOG_REKORD)
        gép.직렬.sendall(b'x' * 129 + b'\n')
        gép.várakozóállapot('...> ', Futtatás)
        gép.Parancs('.save', ['Too much input; original preserved'])
        gép.Parancs('javac Hello.java', ['Compiled:', 'Exit: 0'])
        szerkeszt_ÉRTÉK(gép, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for szám in range(3):
            szerkeszt_ÉRTÉK(gép, 'f' + str(szám), 'occupied')
        gép.Parancs('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        gép.Parancs('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in gép.LOG_REKORD.decode('utf-8', 'replace')
        KR['serial'] = gép.LOG_REKORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(Altípus_ÉRTÉK))
        return KR
    finally:
        gép.Bezárás()


def 주코드(adat):
    """손상 시험용 main Code의 tényleges_adat Fájl 오프셋/길이만 읽는다."""
    pozíció_ÉRTÉK = 8
    def 짧():
        nonlocal pozíció_ÉRTÉK
        ÉRTÉK = struct.unpack_from('>H', adat, pozíció_ÉRTÉK)[0]
        pozíció_ÉRTÉK += 2
        return ÉRTÉK
    def 정():
        nonlocal pozíció_ÉRTÉK
        ÉRTÉK = struct.unpack_from('>I', adat, pozíció_ÉRTÉK)[0]
        pozíció_ÉRTÉK += 4
        return ÉRTÉK
    문자들 = {}
    for szám in range(1, 짧()):
        Altípus_ÉRTÉK = adat[pozíció_ÉRTÉK]
        pozíció_ÉRTÉK += 1
        if Altípus_ÉRTÉK == 1:
            hossz_ÉRTÉK = 짧()
            문자들[szám] = adat[pozíció_ÉRTÉK:pozíció_ÉRTÉK + hossz_ÉRTÉK]
            pozíció_ÉRTÉK += hossz_ÉRTÉK
        elif Altípus_ÉRTÉK in (7, 8): pozíció_ÉRTÉK += 2
        elif Altípus_ÉRTÉK in (3, 9, 10, 12): pozíció_ÉRTÉK += 4
        else: raise AssertionError(Altípus_ÉRTÉK)
    pozíció_ÉRTÉK += 6
    cikk_DARAB = 짧()
    pozíció_ÉRTÉK += cikk_DARAB * 2
    assert 짧() == 0
    for szám in range(짧()):
        짧()
        Név = 짧()
        짧()
        for szám in range(짧()):
            attribútum_ÉRTÉK = 짧()
            Méret = 정()
            if 문자들[Név] == b'main' and 문자들[attribútum_ÉRTÉK] == b'Code':
                return pozíció_ÉRTÉK + 8, struct.unpack_from('>I', adat, pozíció_ÉRTÉK + 4)[0]
            pozíció_ÉRTÉK += Méret
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        címtár_ÉRTÉK = Path(임시)
        (címtár_ÉRTÉK / 'build').mkdir()
        FORRÁS = címtár_ÉRTÉK / 'Imported.java'
        FORRÁS.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(FORRÁS)], check=True)
        원본 = (címtár_ÉRTÉK / 'Imported.class').read_bytes()
        KÓD_ÉRTÉK, hossz_ÉRTÉK = 주코드(원본)
        változat_ÉRTÉK = {}
        adat = bytearray(원본); adat[0] = 0; változat_ÉRTÉK['BadMagic'] = adat
        adat = bytearray(원본); adat[7] = 61; változat_ÉRTÉK['BadVer'] = adat
        adat = bytearray(원본); adat[8:10] = b'\xff\xff'; változat_ÉRTÉK['BadPool'] = adat
        adat = bytearray(원본); adat[KÓD_ÉRTÉK:KÓD_ÉRTÉK + hossz_ÉRTÉK] = bytes(hossz_ÉRTÉK)
        adat[KÓD_ÉRTÉK:KÓD_ÉRTÉK + 3] = b'\xa7\x00\x01'; adat[KÓD_ÉRTÉK + hossz_ÉRTÉK - 1] = 177; változat_ÉRTÉK['BadJump'] = adat
        adat = bytearray(원본); adat[KÓD_ÉRTÉK:KÓD_ÉRTÉK + hossz_ÉRTÉK] = bytes(hossz_ÉRTÉK)
        adat[KÓD_ÉRTÉK] = 87; adat[KÓD_ÉRTÉK + hossz_ÉRTÉK - 1] = 177; változat_ÉRTÉK['BadStack'] = adat
        # Név 검사를 통과시켜 tényleges_adat végrehajt_parancs 중의 operandus_Sor 오류까지 검사한다.
        változat_ÉRTÉK['BadStack'] = változat_ÉRTÉK['BadStack'].replace(b'Imported', b'BadStack')
        bejegyzés_ÉRTÉK = ['Imported.class=' + str(címtár_ÉRTÉK / 'Imported.class'), 'Imported.java=' + str(FORRÁS)]
        for Név, adat in változat_ÉRTÉK.items():
            ÚTVONAL = címtár_ÉRTÉK / (Név + '.class'); ÚTVONAL.write_bytes(adat)
            bejegyzés_ÉRTÉK.append(Név + '.class=' + str(ÚTVONAL))
        Csoport_ÉRTÉK = címtár_ÉRTÉK / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Pozíció / 'Eszközök/자바파일묶기.py'), '-o', str(Csoport_ÉRTÉK)] + bejegyzés_ÉRTÉK, check=True)
        subprocess.run(['as', '--32', '-o', str(címtár_ÉRTÉK / 'user.o'), str(Pozíció / '부팅/felhasználó.s')], cwd=str(címtár_ÉRTÉK), check=True)
        kernel_ÉRTÉK = címtár_ÉRTÉK / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozíció / '부팅/csatol_Navigáció.ld'), '-o', str(kernel_ÉRTÉK),
                        str(Pozíció / 'build/boot.o'), str(Pozíció / 'build/java.o'), str(címtár_ÉRTÉK / 'user.o'), str(Pozíció / 'build/apps.o')], check=True)
        gép = VM(kernel_ÉRTÉK, hálózat_ÉRTÉK=False)
        try:
            gép.Parancs('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            gép.Parancs('cat Imported.java', ['int[] values = new int[3]'])
            for Név, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                gép.Parancs('java ' + Név, [문구, 'Exit: 1'])
                gép.Parancs('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return gép.LOG_REKORD.decode('utf-8', 'replace')
        finally:
            gép.Bezárás()


if __name__ == '__main__':
    elemez_ÉRTÉK = argparse.ArgumentParser()
    elemez_ÉRTÉK.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumentumok = elemez_ÉRTÉK.parse_args()
    KR = {Altípus_ÉRTÉK: teszt_futtat(Altípus_ÉRTÉK) for Altípus_ÉRTÉK in (('elf', 'iso') if Argumentumok.boot == 'both' else (Argumentumok.boot,))}
    KR['import'] = 적재시험()
    (Pozíció / 'build/자바시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n')
