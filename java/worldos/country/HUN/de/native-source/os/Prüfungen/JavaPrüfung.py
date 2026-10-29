#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 befehlAusführen, fehlschlagWert/betriebsmittelEintragWert grenzstelleWert Prüfungen."""
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
from benutzerNetzwerkPrüfung import VirtuelleMaschine, position


def bearbeitenWert(maschine, Name, inhaltswertWert, ablegenDatenWert=True):
    ausführenVorgang = len(maschine.protokolldateiAufzeichnung)
    maschine.seriellWert.sendall(('edit ' + Name + '\n').encode())
    maschine.statuswertWarten('...> ', ausführenVorgang)
    for zeile in inhaltswertWert.splitlines():
        assert len(zeile) <= 128
        ausführenVorgang = len(maschine.protokolldateiAufzeichnung)
        maschine.seriellWert.sendall((zeile + '\n').encode())
        maschine.statuswertWarten('...> ', ausführenVorgang)
    ausführenVorgang = len(maschine.protokolldateiAufzeichnung)
    maschine.seriellWert.sendall(b'.save\n' if ablegenDatenWert else b'.cancel\n')
    ergebnis = maschine.statuswertWarten('jkoros> ', ausführenVorgang)
    assert ('Saved:' if ablegenDatenWert else 'Cancelled; original preserved') in ergebnis, ergebnis


def dateiAdresse():
    ergebnis = subprocess.check_output(['nm', '-n', str(position / 'build/kernel.elf')], universal_newlines=True)
    for zeile in ergebnis.splitlines():
        if zeile.endswith(' ram_files'):
            return int(zeile.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gastDatei(maschine, platzWert, größe, pfad):
    # Prüfungen VM의 메모리에서 tatsächlichDaten 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    adresse = dateiAdresse() + platzWert * 16384
    maschine.überwacherWert.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(adresse, größe, pfad)).encode())
    endung = time.monotonic() + 5
    while time.monotonic() < endung:
        if pfad.exists() and pfad.stat().st_size == größe:
            return pfad.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def ausführenVorgangPrüfung(artWert):
    maschine = VirtuelleMaschine(position / ('build/kernel.elf' if artWert == 'elf' else 'build/kernel.iso'), artWert, netzwerkWert=False)
    ergebnis = {}
    try:
        maschine.befehl('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        maschine.befehl('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        maschine.befehl('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        maschine.befehl('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        maschine.befehl('java Missing', ['cannot read class: -2', 'Exit: 1'])
        maschine.befehl('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        maschine.befehl('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        inhaltswertWert = '''public class Calc {
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
        bearbeitenWert(maschine, 'Calc.java', inhaltswertWert)
        maschine.befehl('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        erwartung = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Ausgabe = maschine.befehl('java Calc 6 guest', ['\r\n' + '\r\n'.join(erwartung) + '\r\n', 'Exit: 0'])
        ergebnis['guest_output'] = Ausgabe
        eintragListe = maschine.befehl('ls', ['Calc.class'])
        größe = int(re.search(r'Calc\.class\s+(\d+) bytes', eintragListe).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as verzeichnisWert:
            pfad = Path(verzeichnisWert) / 'Calc.class'
            Daten = gastDatei(maschine, 3, größe, pfad)
            tatsächlichDaten = subprocess.check_output(['java', '-Xverify:all', '-cp', verzeichnisWert, 'Calc', '6', 'guest'], universal_newlines=True)
            assert tatsächlichDaten.splitlines() == erwartung, tatsächlichDaten
            ergebnis['class_sha256'] = hashlib.sha256(Daten).hexdigest()
            ergebnis['openjdk_output'] = tatsächlichDaten
        # 실패한 bearbeitenWert/컴파일은 기존 class를 보존한다.
        bearbeitenWert(maschine, 'Calc.java', 'not Java at all', ablegenDatenWert=False)
        maschine.befehl('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ungültigErgebnis in [
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
            bearbeitenWert(maschine, 'Calc.java', ungültigErgebnis)
            maschine.befehl('javac Calc.java', ['javac error:', 'Exit: 1'])
            maschine.befehl('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # wiederholungsschrittWert 실행은 Benutzer speicherhaldeWert/프레임을 매번 초기화한다.
        for Zahl in range(12):
            maschine.befehl('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        maschine.befehl('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        maschine.befehl('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        bearbeitenWert(maschine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        maschine.befehl('javac Calc.java', ['Compiled:', 'Exit: 0'])
        maschine.befehl('java Calc', ['instruction limit', 'Exit: 1'])
        maschine.befehl('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        bearbeitenWert(maschine, 'Bad.class', 'garbage')
        maschine.befehl('java Bad', ['JVM error:', 'Exit: 1'])
        maschine.befehl('rm Bad.class', ['Removed'])
        maschine.befehl('java Bad', ['cannot read class: -2'])
        # bearbeitenWert 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ausführenVorgang = len(maschine.protokolldateiAufzeichnung)
        maschine.seriellWert.sendall(b'edit Hello.java\n')
        maschine.statuswertWarten('...> ', ausführenVorgang)
        ausführenVorgang = len(maschine.protokolldateiAufzeichnung)
        maschine.seriellWert.sendall(b'x' * 129 + b'\n')
        maschine.statuswertWarten('...> ', ausführenVorgang)
        maschine.befehl('.save', ['Too much input; original preserved'])
        maschine.befehl('javac Hello.java', ['Compiled:', 'Exit: 0'])
        bearbeitenWert(maschine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for Zahl in range(3):
            bearbeitenWert(maschine, 'f' + str(Zahl), 'occupied')
        maschine.befehl('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        maschine.befehl('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
        ergebnis['serial'] = maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(artWert))
        return ergebnis
    finally:
        maschine.schließen()


def hauptversionKode(Daten):
    """손상 시험용 main Code의 tatsächlichDaten Datei 오프셋/길이만 읽는다."""
    positionWert = 8
    def vorzeichenlosKurzLesen():
        nonlocal positionWert
        Wert = struct.unpack_from('>H', Daten, positionWert)[0]
        positionWert += 2
        return Wert
    def vorzeichenlosGanzzahlLesen():
        nonlocal positionWert
        Wert = struct.unpack_from('>I', Daten, positionWert)[0]
        positionWert += 4
        return Wert
    zeichenWerte = {}
    for Zahl in range(1, vorzeichenlosKurzLesen()):
        artWert = Daten[positionWert]
        positionWert += 1
        if artWert == 1:
            Länge = vorzeichenlosKurzLesen()
            zeichenWerte[Zahl] = Daten[positionWert:positionWert + Länge]
            positionWert += Länge
        elif artWert in (7, 8): positionWert += 2
        elif artWert in (3, 9, 10, 12): positionWert += 4
        else: raise AssertionError(artWert)
    positionWert += 6
    elementeintragAnzahl = vorzeichenlosKurzLesen()
    positionWert += elementeintragAnzahl * 2
    assert vorzeichenlosKurzLesen() == 0
    for Zahl in range(vorzeichenlosKurzLesen()):
        vorzeichenlosKurzLesen()
        Name = vorzeichenlosKurzLesen()
        vorzeichenlosKurzLesen()
        for Zahl in range(vorzeichenlosKurzLesen()):
            attributWert = vorzeichenlosKurzLesen()
            größe = vorzeichenlosGanzzahlLesen()
            if zeichenWerte[Name] == b'main' and zeichenWerte[attributWert] == b'Code':
                return positionWert + 8, struct.unpack_from('>I', Daten, positionWert + 4)[0]
            positionWert += größe
    raise AssertionError('main Code missing')


def ladendPrüfung():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as vorläufigWert:
        verzeichnisWert = Path(vorläufigWert)
        (verzeichnisWert / 'build').mkdir()
        Quelltext = verzeichnisWert / 'Imported.java'
        Quelltext.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(Quelltext)], check=True)
        ursprünglich = (verzeichnisWert / 'Imported.class').read_bytes()
        kodeWert, Länge = hauptversionKode(ursprünglich)
        varianteWert = {}
        Daten = bytearray(ursprünglich); Daten[0] = 0; varianteWert['BadMagic'] = Daten
        Daten = bytearray(ursprünglich); Daten[7] = 61; varianteWert['BadVer'] = Daten
        Daten = bytearray(ursprünglich); Daten[8:10] = b'\xff\xff'; varianteWert['BadPool'] = Daten
        Daten = bytearray(ursprünglich); Daten[kodeWert:kodeWert + Länge] = bytes(Länge)
        Daten[kodeWert:kodeWert + 3] = b'\xa7\x00\x01'; Daten[kodeWert + Länge - 1] = 177; varianteWert['BadJump'] = Daten
        Daten = bytearray(ursprünglich); Daten[kodeWert:kodeWert + Länge] = bytes(Länge)
        Daten[kodeWert] = 87; Daten[kodeWert + Länge - 1] = 177; varianteWert['BadStack'] = Daten
        # Name 검사를 통과시켜 tatsächlichDaten befehlAusführen 중의 operandStapel 오류까지 검사한다.
        varianteWert['BadStack'] = varianteWert['BadStack'].replace(b'Imported', b'BadStack')
        eintragWert = ['Imported.class=' + str(verzeichnisWert / 'Imported.class'), 'Imported.java=' + str(Quelltext)]
        for Name, Daten in varianteWert.items():
            pfad = verzeichnisWert / (Name + '.class'); pfad.write_bytes(Daten)
            eintragWert.append(Name + '.class=' + str(pfad))
        gruppeWert = verzeichnisWert / 'build/java-files.bin'
        subprocess.run([sys.executable, str(position / 'Werkzeuge/JavaDateienPacken.py'), '-o', str(gruppeWert)] + eintragWert, check=True)
        subprocess.run(['as', '--32', '-o', str(verzeichnisWert / 'user.o'), str(position / 'Startvorgang/Benutzer.s')], cwd=str(verzeichnisWert), check=True)
        betriebskernWert = verzeichnisWert / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position / 'Startvorgang/Bindungsanordnung.ld'), '-o', str(betriebskernWert),
                        str(position / 'build/boot.o'), str(position / 'build/java.o'), str(verzeichnisWert / 'user.o'), str(position / 'build/apps.o')], check=True)
        maschine = VirtuelleMaschine(betriebskernWert, netzwerkWert=False)
        try:
            maschine.befehl('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            maschine.befehl('cat Imported.java', ['int[] values = new int[3]'])
            for Name, wortgruppeWert in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                maschine.befehl('java ' + Name, [wortgruppeWert, 'Exit: 1'])
                maschine.befehl('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
        finally:
            maschine.schließen()


if __name__ == '__main__':
    wertAnalysieren = argparse.ArgumentParser()
    wertAnalysieren.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argumente = wertAnalysieren.parse_args()
    ergebnis = {artWert: ausführenVorgangPrüfung(artWert) for artWert in (('elf', 'iso') if argumente.boot == 'both' else (argumente.boot,))}
    ergebnis['import'] = ladendPrüfung()
    (position / 'build/JavaPrüfung.json').write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + '\n')
