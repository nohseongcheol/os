"""tatsächlichDaten ELF befehlAusführen + OpenJDK ergebnis 대조. vorläufigWert Prüfungen 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

Übersetzer = Path(__file__).resolve().parents[1] / 'Übersetzer.py'


class systemnahPrüfung(unittest.TestCase):
    def setUp(self):
        self.vorläufigWert = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.vorläufigWert.cleanup)
        self.verzeichnisWert = Path(self.vorläufigWert.name)

    def quelltextÜbersetzen(self, Quelltext, eintragAnhängen=None, erfolgWert=True, zielobjektWert='linux', exportiertWert=None):
        pfadListe = []
        for Name, inhaltswertWert in dict({'Prüfungen': Quelltext}, **(eintragAnhängen or {})).items():
            pfad = self.verzeichnisWert / (Name + '.java')
            pfad.write_text(inhaltswertWert, encoding='utf-8')
            pfadListe.append(str(pfad))
        befehl = [sys.executable, str(Übersetzer), '--target', zielobjektWert, '--entry', 'Prüfungen.ausführenVorgang', '-o', str(self.verzeichnisWert / 'native')]
        if exportiertWert is not None: befehl += ['--export', exportiertWert]
        ergebnis = subprocess.run(befehl + pfadListe,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if erfolgWert:
            self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ergebnis.returncode, 0)
            self.assertIn('quelltextÜbersetzen fehler'.encode(), ergebnis.stderr)
        return ergebnis

    def ausführungErgebnis(self):
        return subprocess.run([str(self.verzeichnisWert / 'native')], timeout=5).returncode

    def javaVergleich(self, Quelltext, eintragAnhängen=None):
        self.quelltextÜbersetzen(Quelltext, eintragAnhängen)
        (self.verzeichnisWert / 'Wirtssystem.java').write_text(
            'public class Wirtssystem { public static void main(String[] argumente) { System.exit(Prüfungen.ausführenVorgang()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.verzeichnisWert)] +
                       [str(pfad) for pfad in self.verzeichnisWert.glob('*.java')], check=True, timeout=30)
        erwartung = subprocess.run(['java', '-cp', str(self.verzeichnisWert), 'Wirtssystem'], timeout=5).returncode
        tatsächlichDaten = self.ausführungErgebnis()
        self.assertGreaterEqual(tatsächlichDaten, 0, '신호로 hatVerlassen (샌드박스의 32비트 syscall grenzwertWert 여부 überprüfen)')
        self.assertEqual(tatsächlichDaten, erwartung)

    def ganzzahlArithmetikUndVerschiebungenPrüfung(self):
        self.javaVergleich('''public class Prüfungen {
            static int mischenArithmetik(int ersterOperand, int zweiterOperand) {
                return ((ersterOperand + zweiterOperand) ^ (ersterOperand - zweiterOperand) ^ (ersterOperand * zweiterOperand) ^ (ersterOperand & zweiterOperand) ^ (ersterOperand | zweiterOperand))
                    + (ersterOperand << zweiterOperand) + (ersterOperand >> zweiterOperand) + (ersterOperand >>> zweiterOperand);
            }
            public static int ausführenVorgang() {
                int summeWert = 7;
                int Wert = 12345;
                for (int Nummer = -65; Nummer <= 65; Nummer++) {
                    Wert = Wert * 1664525 + 1013904223;
                    summeWert = summeWert * 31 + mischenArithmetik(Wert, Nummer);
                    summeWert += (byte)Wert + (short)Wert + (char)Wert;
                }
                return (summeWert & 0x7fffffff) % 251;
            }
        }''')

    def divisionExtremwertWertePrüfung(self):
        self.javaVergleich('''public class Prüfungen {
            static int[] Wert = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ausführenVorgang() {
                int summeWert = 13;
                for (int ersterOperand = 0; ersterOperand < Wert.length; ersterOperand++)
                    for (int zweiterOperand = 1; zweiterOperand < Wert.length; zweiterOperand++)
                        summeWert = summeWert * 31 + Wert[ersterOperand] / Wert[zweiterOperand] + Wert[ersterOperand] % Wert[zweiterOperand];
                return (summeWert & 0x7fffffff) % 251;
            }
        }''')

    def felderListeUndVerweisePrüfung(self):
        self.javaVergleich('''public class Prüfungen {
            static int[] eintragErstellen(int größe) { return new int[größe]; }
            public static int ausführenVorgang() {
                int[] ersterOperand = eintragErstellen(8); int[] zweiterOperand = ersterOperand; int[] leerwertObjekt = new int[0];
                if (ersterOperand != zweiterOperand || ersterOperand == null || leerwertObjekt.length != 0 || ersterOperand[7] != 0) return 99;
                int Wert = (ersterOperand[2] = 40); ersterOperand[2]++; ++ersterOperand[3]; ersterOperand[2] += 7;
                return Wert + zweiterOperand[2] + zweiterOperand[3];
            }
        }''')

    def statischDatenfelderUndArgumentReihenfolgePrüfung(self):
        self.javaVergleich('''public class Prüfungen {
            static int Wert = hilfsWert.anfänglichWert();
            static int berechnung(int ersterOperand, int zweiterOperand, int dritterOperand, int vierterOperand, int fünfterOperand) {
                return ersterOperand + zweiterOperand * 2 + dritterOperand * 3 + vierterOperand * 4 + fünfterOperand * 5;
            }
            public static int ausführenVorgang() { return berechnung(1, 2, 3, 4, Wert) + hilfsWert.lesen(); }
        }''', {'hilfsWert': '''public class hilfsWert {
            static int Wert = 3;
            static int anfänglichWert() { return ++Wert; }
            static int lesen() { return Wert; }
        }'''})

    def initialisierungZyklusPrüfung(self):
        self.javaVergleich('''public class Prüfungen {
            static int Wert = hilfsWert.lesen() + 1;
            public static int ausführenVorgang() { return Wert * 10 + hilfsWert.lesen(); }
        }''', {'hilfsWert': '''public class hilfsWert {
            static int Wert = Prüfungen.Wert + 2;
            static int lesen() { return Wert; }
        }'''})

    def verändertUTF8ZeichenkettenPrüfung(self):
        self.javaVergleich('''public class Prüfungen {
            static String Text = "한글\\u0000😀";
            public static int ausführenVorgang() {
                if (Text != "한글\\u0000😀") return 99;
                return (Text.length() + Text.charAt(2) + Text.charAt(3) + Text.charAt(4)) % 251;
            }
        }''')

    def umschaltenUndRekursionPrüfung(self):
        self.javaVergleich('''public class Prüfungen {
            static int fakultät(int Wert) { return Wert <= 1 ? 1 : Wert * fakultät(Wert - 1); }
            static int dichtUmschaltenFallliste(int Wert) {
                switch (Wert) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int dünnbesetztUmschaltenFallliste(int Wert) {
                switch (Wert) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ausführenVorgang() { return (fakultät(5) + dichtUmschaltenFallliste(0) + dichtUmschaltenFallliste(2) + dichtUmschaltenFallliste(9) + dünnbesetztUmschaltenFallliste(-1000) + dünnbesetztUmschaltenFallliste(0)) % 251; }
        }''')

    def breitLokalVariablenPrüfung(self):
        Deklarationen = '\n'.join('int Wert{} = {};'.format(Nummer, Nummer) for Nummer in range(270))
        additionErgebnis = '+'.join('Wert{}'.format(Nummer) for Nummer in range(270))
        self.javaVergleich('public class Prüfungen { public static int ausführenVorgang() {' + Deklarationen +
                    'wert269 += 300; return (' + additionErgebnis + ') % 251; } }')

    def laufzeitFehlerNummernPrüfung(self):
        fallEinträge = [
            ('int nullwertOperand = 0; return 1 / nullwertOperand;', 101),
            ('int[] Wert = null; return Wert.length;', 102),
            ('int[] Wert = new int[1]; return Wert[1];', 103),
            ('int[] Wert = new int[1]; Wert[-1] = 3; return 0;', 103),
            ('int Wert = -1; return new int[Wert].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] ersterOperand = new int[65535]; return new int[1].length;', 105),
        ]
        for rumpfWert, erwartung in fallEinträge:
            with self.subTest(rumpfWert=rumpfWert):
                self.quelltextÜbersetzen('public class Prüfungen { public static int ausführenVorgang() { ' + rumpfWert + ' } }')
                self.assertEqual(self.ausführungErgebnis(), erwartung)

    def nichtUnterstütztMerkmalZurückgewiesenPrüfung(self):
        fallEinträge = [
            'static long Wert; public static int ausführenVorgang() { return 0; }',
            'public static int ausführenVorgang() { Object Wert = new Object(); return 0; }',
            'public static int ausführenVorgang() { System.out.println("hello"); return 0; }',
            'public static int ausführenVorgang() { try { return 1; } catch (Exception fehler) { return 2; } }',
            'public static synchronized int ausführenVorgang() { return 0; }',
            'public static int ausführenVorgang() { return new byte[3].length; }',
            'static native int externWert(); public static int ausführenVorgang() { return externWert(); }',
            'int Wert; public static int ausführenVorgang() { return 0; }',
        ]
        for rumpfWert in fallEinträge:
            with self.subTest(rumpfWert=rumpfWert):
                self.quelltextÜbersetzen('public class Prüfungen { ' + rumpfWert + ' }', erfolgWert=False)

    def bestehendAusgabeBewahrtEingeschaltetFehlschlagPrüfung(self):
        Ausgabe = self.verzeichnisWert / 'native'
        Ausgabe.write_bytes(b'original-output')
        self.quelltextÜbersetzen('public class Prüfungen { public static int ausführenVorgang() { return missing; } }', erfolgWert=False)
        self.assertEqual(Ausgabe.read_bytes(), b'original-output')

    def eLFUndEigenständigLaufendAusführungPrüfung(self):
        self.quelltextÜbersetzen('public class Prüfungen { public static int ausführenVorgang() { return 37; } }')
        self.assertEqual((self.verzeichnisWert / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Tabelle = subprocess.check_output(['readelf', '-l', str(self.verzeichnisWert / 'native')])
        self.assertNotIn(b'INTERP', Tabelle)
        self.assertEqual(self.ausführungErgebnis(), 37)

    def benutzerELFUndABITrennungPrüfung(self):
        self.quelltextÜbersetzen('public class Prüfungen { public static int ausführenVorgang() { return Benutzer.ausführungErlaubnis(); } }',
                    {'Benutzer': 'public class Benutzer { public static native int ausführungErlaubnis(); }'}, zielobjektWert='user')
        Daten = (self.verzeichnisWert / 'native').read_bytes()
        self.assertEqual(Daten[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', Daten, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.verzeichnisWert / 'native')]))
        # Benutzer ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.quelltextÜbersetzen('public class Prüfungen { public static int ausführenVorgang() { return Gerät.hardwarePortLesen(1); } }',
                    {'Gerät': 'public class Gerät { public static native int hardwarePortLesen(int Wert); }'}, erfolgWert=False, zielobjektWert='user')

    def exportierenValidierungPrüfung(self):
        Quelltext = 'public class Prüfungen { public static int ausführenVorgang() { return 0; } static int aufrufen(int Wert) { return Wert; } }'
        self.quelltextÜbersetzen(Quelltext, zielobjektWert='kernel', exportiertWert='kernel_dispatch=Prüfungen.aufrufen')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.verzeichnisWert / 'native')]))
        self.quelltextÜbersetzen(Quelltext, erfolgWert=False, exportiertWert='bad;name=Prüfungen.aufrufen')
        self.quelltextÜbersetzen(Quelltext, erfolgWert=False, exportiertWert='missing=Prüfungen.fehlendMethode')


if __name__ == '__main__':
    unittest.main()
