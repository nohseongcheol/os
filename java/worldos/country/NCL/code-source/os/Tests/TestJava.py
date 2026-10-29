#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 exécuterCommande, valeurÉchec/valeurRessource valeurFrontière Tests."""
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
from testRéseauUtilisateur import MachineVirtuelle, position


def valeurÉditer(machine, nom, valeurContenuValeur, valeurStocker=True):
    lancer = len(machine.enregistrementJournal)
    machine.valeurSériel.sendall(('edit ' + nom + '\n').encode())
    machine.attendreÉtatValeur('...> ', lancer)
    for ligne in valeurContenuValeur.splitlines():
        assert len(ligne) <= 128
        lancer = len(machine.enregistrementJournal)
        machine.valeurSériel.sendall((ligne + '\n').encode())
        machine.attendreÉtatValeur('...> ', lancer)
    lancer = len(machine.enregistrementJournal)
    machine.valeurSériel.sendall(b'.save\n' if valeurStocker else b'.cancel\n')
    résultat = machine.attendreÉtatValeur('jkoros> ', lancer)
    assert ('Saved:' if valeurStocker else 'Cancelled; original preserved') in résultat, résultat


def adresseFichier():
    résultat = subprocess.check_output(['nm', '-n', str(position / 'build/kernel.elf')], universal_newlines=True)
    for ligne in résultat.splitlines():
        if ligne.endswith(' ram_files'):
            return int(ligne.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def fichierInvité(machine, valeurEmplacement, taille, chemin):
    # Tests VM의 메모리에서 donnéesEffectif 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    adresse = adresseFichier() + valeurEmplacement * 16384
    machine.valeurMoniteur.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(adresse, taille, chemin)).encode())
    terminaison = time.monotonic() + 5
    while time.monotonic() < terminaison:
        if chemin.exists() and chemin.stat().st_size == taille:
            return chemin.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def testLancer(valeurGenre):
    machine = MachineVirtuelle(position / ('build/kernel.elf' if valeurGenre == 'elf' else 'build/kernel.iso'), valeurGenre, valeurRéseau=False)
    résultat = {}
    try:
        machine.commande('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        machine.commande('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        machine.commande('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        machine.commande('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        machine.commande('java Missing', ['cannot read class: -2', 'Exit: 1'])
        machine.commande('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        machine.commande('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        valeurContenuValeur = '''public class Calc {
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
        valeurÉditer(machine, 'Calc.java', valeurContenuValeur)
        machine.commande('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        attente = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Sortie = machine.commande('java Calc 6 guest', ['\r\n' + '\r\n'.join(attente) + '\r\n', 'Exit: 0'])
        résultat['guest_output'] = Sortie
        listeEntréeÉlément = machine.commande('ls', ['Calc.class'])
        taille = int(re.search(r'Calc\.class\s+(\d+) bytes', listeEntréeÉlément).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as valeurRépertoire:
            chemin = Path(valeurRépertoire) / 'Calc.class'
            Données = fichierInvité(machine, 3, taille, chemin)
            donnéesEffectif = subprocess.check_output(['java', '-Xverify:all', '-cp', valeurRépertoire, 'Calc', '6', 'guest'], universal_newlines=True)
            assert donnéesEffectif.splitlines() == attente, donnéesEffectif
            résultat['class_sha256'] = hashlib.sha256(Données).hexdigest()
            résultat['openjdk_output'] = donnéesEffectif
        # 실패한 valeurÉditer/컴파일은 기존 class를 보존한다.
        valeurÉditer(machine, 'Calc.java', 'not Java at all', valeurStocker=False)
        machine.commande('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for résultatInvalide in [
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
            valeurÉditer(machine, 'Calc.java', résultatInvalide)
            machine.commande('javac Calc.java', ['javac error:', 'Exit: 1'])
            machine.commande('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # valeurItération 실행은 Utilisateur valeurTas/프레임을 매번 초기화한다.
        for nombre in range(12):
            machine.commande('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        machine.commande('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        machine.commande('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        valeurÉditer(machine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        machine.commande('javac Calc.java', ['Compiled:', 'Exit: 0'])
        machine.commande('java Calc', ['instruction limit', 'Exit: 1'])
        machine.commande('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        valeurÉditer(machine, 'Bad.class', 'garbage')
        machine.commande('java Bad', ['JVM error:', 'Exit: 1'])
        machine.commande('rm Bad.class', ['Removed'])
        machine.commande('java Bad', ['cannot read class: -2'])
        # valeurÉditer 입력의 넘친 부분을 잘라서 저장하지 않는다.
        lancer = len(machine.enregistrementJournal)
        machine.valeurSériel.sendall(b'edit Hello.java\n')
        machine.attendreÉtatValeur('...> ', lancer)
        lancer = len(machine.enregistrementJournal)
        machine.valeurSériel.sendall(b'x' * 129 + b'\n')
        machine.attendreÉtatValeur('...> ', lancer)
        machine.commande('.save', ['Too much input; original preserved'])
        machine.commande('javac Hello.java', ['Compiled:', 'Exit: 0'])
        valeurÉditer(machine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for nombre in range(3):
            valeurÉditer(machine, 'f' + str(nombre), 'occupied')
        machine.commande('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        machine.commande('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in machine.enregistrementJournal.decode('utf-8', 'replace')
        résultat['serial'] = machine.enregistrementJournal.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(valeurGenre))
        return résultat
    finally:
        machine.fermer()


def codeMajeur(Données):
    """손상 시험용 main Code의 donnéesEffectif Fichier 오프셋/길이만 읽는다."""
    valeurPosition = 8
    def lireCourtNonSigné():
        nonlocal valeurPosition
        valeur = struct.unpack_from('>H', Données, valeurPosition)[0]
        valeurPosition += 2
        return valeur
    def lireEntierNonSigné():
        nonlocal valeurPosition
        valeur = struct.unpack_from('>I', Données, valeurPosition)[0]
        valeurPosition += 4
        return valeur
    valeursCaractère = {}
    for nombre in range(1, lireCourtNonSigné()):
        valeurGenre = Données[valeurPosition]
        valeurPosition += 1
        if valeurGenre == 1:
            longueur = lireCourtNonSigné()
            valeursCaractère[nombre] = Données[valeurPosition:valeurPosition + longueur]
            valeurPosition += longueur
        elif valeurGenre in (7, 8): valeurPosition += 2
        elif valeurGenre in (3, 9, 10, 12): valeurPosition += 4
        else: raise AssertionError(valeurGenre)
    valeurPosition += 6
    nombreÉlémentsÉlémentListe = lireCourtNonSigné()
    valeurPosition += nombreÉlémentsÉlémentListe * 2
    assert lireCourtNonSigné() == 0
    for nombre in range(lireCourtNonSigné()):
        lireCourtNonSigné()
        nom = lireCourtNonSigné()
        lireCourtNonSigné()
        for nombre in range(lireCourtNonSigné()):
            valeurAttribut = lireCourtNonSigné()
            taille = lireEntierNonSigné()
            if valeursCaractère[nom] == b'main' and valeursCaractère[valeurAttribut] == b'Code':
                return valeurPosition + 8, struct.unpack_from('>I', Données, valeurPosition + 4)[0]
            valeurPosition += taille
    raise AssertionError('main Code missing')


def testChargementEnCours():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as valeurTemporaire:
        valeurRépertoire = Path(valeurTemporaire)
        (valeurRépertoire / 'build').mkdir()
        source = valeurRépertoire / 'Imported.java'
        source.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(source)], check=True)
        original = (valeurRépertoire / 'Imported.class').read_bytes()
        valeurCode, longueur = codeMajeur(original)
        valeurVariante = {}
        Données = bytearray(original); Données[0] = 0; valeurVariante['BadMagic'] = Données
        Données = bytearray(original); Données[7] = 61; valeurVariante['BadVer'] = Données
        Données = bytearray(original); Données[8:10] = b'\xff\xff'; valeurVariante['BadPool'] = Données
        Données = bytearray(original); Données[valeurCode:valeurCode + longueur] = bytes(longueur)
        Données[valeurCode:valeurCode + 3] = b'\xa7\x00\x01'; Données[valeurCode + longueur - 1] = 177; valeurVariante['BadJump'] = Données
        Données = bytearray(original); Données[valeurCode:valeurCode + longueur] = bytes(longueur)
        Données[valeurCode] = 87; Données[valeurCode + longueur - 1] = 177; valeurVariante['BadStack'] = Données
        # nom 검사를 통과시켜 donnéesEffectif exécuterCommande 중의 pileOpérande 오류까지 검사한다.
        valeurVariante['BadStack'] = valeurVariante['BadStack'].replace(b'Imported', b'BadStack')
        valeurEntréeÉlément = ['Imported.class=' + str(valeurRépertoire / 'Imported.class'), 'Imported.java=' + str(source)]
        for nom, Données in valeurVariante.items():
            chemin = valeurRépertoire / (nom + '.class'); chemin.write_bytes(Données)
            valeurEntréeÉlément.append(nom + '.class=' + str(chemin))
        valeurGroupe = valeurRépertoire / 'build/java-files.bin'
        subprocess.run([sys.executable, str(position / 'Outils/EmballerFichiersJava.py'), '-o', str(valeurGroupe)] + valeurEntréeÉlément, check=True)
        subprocess.run(['as', '--32', '-o', str(valeurRépertoire / 'user.o'), str(position / 'Amorçage/Utilisateur.s')], cwd=str(valeurRépertoire), check=True)
        valeurNoyau = valeurRépertoire / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position / 'Amorçage/DispositionLiens.ld'), '-o', str(valeurNoyau),
                        str(position / 'build/boot.o'), str(position / 'build/java.o'), str(valeurRépertoire / 'user.o'), str(position / 'build/apps.o')], check=True)
        machine = MachineVirtuelle(valeurNoyau, valeurRéseau=False)
        try:
            machine.commande('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            machine.commande('cat Imported.java', ['int[] values = new int[3]'])
            for nom, valeurExpressionPhrase in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                machine.commande('java ' + nom, [valeurExpressionPhrase, 'Exit: 1'])
                machine.commande('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return machine.enregistrementJournal.decode('utf-8', 'replace')
        finally:
            machine.fermer()


if __name__ == '__main__':
    analyserValeur = argparse.ArgumentParser()
    analyserValeur.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    arguments = analyserValeur.parse_args()
    résultat = {valeurGenre: testLancer(valeurGenre) for valeurGenre in (('elf', 'iso') if arguments.boot == 'both' else (arguments.boot,))}
    résultat['import'] = testChargementEnCours()
    (position / 'build/TestJava.json').write_text(json.dumps(résultat, ensure_ascii=False, indent=2) + '\n')
