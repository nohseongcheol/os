"""donnéesEffectif ELF exécuterCommande + OpenJDK résultat 대조. valeurTemporaire Tests 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

Compilateur = Path(__file__).resolve().parents[1] / 'Compilateur.py'


class testNatif(unittest.TestCase):
    def setUp(self):
        self.valeurTemporaire = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.valeurTemporaire.cleanup)
        self.valeurRépertoire = Path(self.valeurTemporaire.name)

    def compilerSource(self, source, ajouterFinEntréeÉlément=None, valeurSuccès=True, valeurCible='linux', valeurExporté=None):
        listeChemin = []
        for nom, valeurContenuValeur in dict({'Tests': source}, **(ajouterFinEntréeÉlément or {})).items():
            chemin = self.valeurRépertoire / (nom + '.java')
            chemin.write_text(valeurContenuValeur, encoding='utf-8')
            listeChemin.append(str(chemin))
        commande = [sys.executable, str(Compilateur), '--target', valeurCible, '--entry', 'Tests.lancer', '-o', str(self.valeurRépertoire / 'native')]
        if valeurExporté is not None: commande += ['--export', valeurExporté]
        résultat = subprocess.run(commande + listeChemin,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if valeurSuccès:
            self.assertEqual(résultat.returncode, 0, résultat.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(résultat.returncode, 0)
            self.assertIn('compilerSource erreur'.encode(), résultat.stderr)
        return résultat

    def résultatExécution(self):
        return subprocess.run([str(self.valeurRépertoire / 'native')], timeout=5).returncode

    def comparaisonJava(self, source, ajouterFinEntréeÉlément=None):
        self.compilerSource(source, ajouterFinEntréeÉlément)
        (self.valeurRépertoire / 'Hôte.java').write_text(
            'public class Hôte { public static void main(String[] arguments) { System.exit(Tests.lancer()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.valeurRépertoire)] +
                       [str(chemin) for chemin in self.valeurRépertoire.glob('*.java')], check=True, timeout=30)
        attente = subprocess.run(['java', '-cp', str(self.valeurRépertoire), 'Hôte'], timeout=5).returncode
        donnéesEffectif = self.résultatExécution()
        self.assertGreaterEqual(donnéesEffectif, 0, '신호로 possèdeQuitté (샌드박스의 32비트 syscall valeurLimite 여부 vérifier)')
        self.assertEqual(donnéesEffectif, attente)

    def testDécalagesEtArithmétiqueEntier(self):
        self.comparaisonJava('''public class Tests {
            static int arithmétiqueMélanger(int opérandePremier, int opérandeDeuxième) {
                return ((opérandePremier + opérandeDeuxième) ^ (opérandePremier - opérandeDeuxième) ^ (opérandePremier * opérandeDeuxième) ^ (opérandePremier & opérandeDeuxième) ^ (opérandePremier | opérandeDeuxième))
                    + (opérandePremier << opérandeDeuxième) + (opérandePremier >> opérandeDeuxième) + (opérandePremier >>> opérandeDeuxième);
            }
            public static int lancer() {
                int valeurSomme = 7;
                int valeur = 12345;
                for (int numéro = -65; numéro <= 65; numéro++) {
                    valeur = valeur * 1664525 + 1013904223;
                    valeurSomme = valeurSomme * 31 + arithmétiqueMélanger(valeur, numéro);
                    valeurSomme += (byte)valeur + (short)valeur + (char)valeur;
                }
                return (valeurSomme & 0x7fffffff) % 251;
            }
        }''')

    def testValeursExtrêmeDivision(self):
        self.comparaisonJava('''public class Tests {
            static int[] valeur = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int lancer() {
                int valeurSomme = 13;
                for (int opérandePremier = 0; opérandePremier < valeur.length; opérandePremier++)
                    for (int opérandeDeuxième = 1; opérandeDeuxième < valeur.length; opérandeDeuxième++)
                        valeurSomme = valeurSomme * 31 + valeur[opérandePremier] / valeur[opérandeDeuxième] + valeur[opérandePremier] % valeur[opérandeDeuxième];
                return (valeurSomme & 0x7fffffff) % 251;
            }
        }''')

    def testRéférencesEtTableaux(self):
        self.comparaisonJava('''public class Tests {
            static int[] créerEntréeÉlément(int taille) { return new int[taille]; }
            public static int lancer() {
                int[] opérandePremier = créerEntréeÉlément(8); int[] opérandeDeuxième = opérandePremier; int[] objetVide = new int[0];
                if (opérandePremier != opérandeDeuxième || opérandePremier == null || objetVide.length != 0 || opérandePremier[7] != 0) return 99;
                int valeur = (opérandePremier[2] = 40); opérandePremier[2]++; ++opérandePremier[3]; opérandePremier[2] += 7;
                return valeur + opérandeDeuxième[2] + opérandeDeuxième[3];
            }
        }''')

    def testOrdreArgumentEtChampsStatique(self):
        self.comparaisonJava('''public class Tests {
            static int valeur = valeurAuxiliaire.valeurInitialValeur();
            static int calculRésultat(int opérandePremier, int opérandeDeuxième, int opérandeTroisième, int opérandeQuatrième, int opérandeCinquième) {
                return opérandePremier + opérandeDeuxième * 2 + opérandeTroisième * 3 + opérandeQuatrième * 4 + opérandeCinquième * 5;
            }
            public static int lancer() { return calculRésultat(1, 2, 3, 4, valeur) + valeurAuxiliaire.lire(); }
        }''', {'valeurAuxiliaire': '''public class valeurAuxiliaire {
            static int valeur = 3;
            static int valeurInitialValeur() { return ++valeur; }
            static int lire() { return valeur; }
        }'''})

    def testCycleInitialisation(self):
        self.comparaisonJava('''public class Tests {
            static int valeur = valeurAuxiliaire.lire() + 1;
            public static int lancer() { return valeur * 10 + valeurAuxiliaire.lire(); }
        }''', {'valeurAuxiliaire': '''public class valeurAuxiliaire {
            static int valeur = Tests.valeur + 2;
            static int lire() { return valeur; }
        }'''})

    def testChaînes8UTFModifié(self):
        self.comparaisonJava('''public class Tests {
            static String texte = "한글\\u0000😀";
            public static int lancer() {
                if (texte != "한글\\u0000😀") return 99;
                return (texte.length() + texte.charAt(2) + texte.charAt(3) + texte.charAt(4)) % 251;
            }
        }''')

    def testRécursionEtCommuter(self):
        self.comparaisonJava('''public class Tests {
            static int factorielle(int valeur) { return valeur <= 1 ? 1 : valeur * factorielle(valeur - 1); }
            static int casListeCommuterDense(int valeur) {
                switch (valeur) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int casListeCommuterClairsemé(int valeur) {
                switch (valeur) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int lancer() { return (factorielle(5) + casListeCommuterDense(0) + casListeCommuterDense(2) + casListeCommuterDense(9) + casListeCommuterClairsemé(-1000) + casListeCommuterClairsemé(0)) % 251; }
        }''')

    def testVariablesLocalLarge(self):
        Déclarations = '\n'.join('int valeur{} = {};'.format(numéro, numéro) for numéro in range(270))
        résultatAddition = '+'.join('valeur{}'.format(numéro) for numéro in range(270))
        self.comparaisonJava('public class Tests { public static int lancer() {' + Déclarations +
                    'valeur269 += 300; return (' + résultatAddition + ') % 251; } }')

    def testNumérosErreurEnvironnementExécution(self):
        entréesListeCas = [
            ('int opérandeZéro = 0; return 1 / opérandeZéro;', 101),
            ('int[] valeur = null; return valeur.length;', 102),
            ('int[] valeur = new int[1]; return valeur[1];', 103),
            ('int[] valeur = new int[1]; valeur[-1] = 3; return 0;', 103),
            ('int valeur = -1; return new int[valeur].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] opérandePremier = new int[65535]; return new int[1].length;', 105),
        ]
        for valeurCorps, attente in entréesListeCas:
            with self.subTest(valeurCorps=valeurCorps):
                self.compilerSource('public class Tests { public static int lancer() { ' + valeurCorps + ' } }')
                self.assertEqual(self.résultatExécution(), attente)

    def testRejetéFonctionnalitéNonPrisEnCharge(self):
        entréesListeCas = [
            'static long valeur; public static int lancer() { return 0; }',
            'public static int lancer() { Object valeur = new Object(); return 0; }',
            'public static int lancer() { System.out.println("hello"); return 0; }',
            'public static int lancer() { try { return 1; } catch (Exception erreur) { return 2; } }',
            'public static synchronized int lancer() { return 0; }',
            'public static int lancer() { return new byte[3].length; }',
            'static native int valeurExtérieur(); public static int lancer() { return valeurExtérieur(); }',
            'int valeur; public static int lancer() { return 0; }',
        ]
        for valeurCorps in entréesListeCas:
            with self.subTest(valeurCorps=valeurCorps):
                self.compilerSource('public class Tests { ' + valeurCorps + ' }', valeurSuccès=False)

    def testÉchecActivéPréservéSortieExistant(self):
        Sortie = self.valeurRépertoire / 'native'
        Sortie.write_bytes(b'original-output')
        self.compilerSource('public class Tests { public static int lancer() { return missing; } }', valeurSuccès=False)
        self.assertEqual(Sortie.read_bytes(), b'original-output')

    def testExécutionAutonomeEtELF(self):
        self.compilerSource('public class Tests { public static int lancer() { return 37; } }')
        self.assertEqual((self.valeurRépertoire / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Table = subprocess.check_output(['readelf', '-l', str(self.valeurRépertoire / 'native')])
        self.assertNotIn(b'INTERP', Table)
        self.assertEqual(self.résultatExécution(), 37)

    def testSéparationABIEtELFUtilisateur(self):
        self.compilerSource('public class Tests { public static int lancer() { return Utilisateur.permissionExécution(); } }',
                    {'Utilisateur': 'public class Utilisateur { public static native int permissionExécution(); }'}, valeurCible='user')
        Données = (self.valeurRépertoire / 'native').read_bytes()
        self.assertEqual(Données[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', Données, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.valeurRépertoire / 'native')]))
        # Utilisateur ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.compilerSource('public class Tests { public static int lancer() { return Périphérique.lirePortMatériel(1); } }',
                    {'Périphérique': 'public class Périphérique { public static native int lirePortMatériel(int valeur); }'}, valeurSuccès=False, valeurCible='user')

    def testValidationExporter(self):
        source = 'public class Tests { public static int lancer() { return 0; } static int invoquer(int valeur) { return valeur; } }'
        self.compilerSource(source, valeurCible='kernel', valeurExporté='kernel_dispatch=Tests.invoquer')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.valeurRépertoire / 'native')]))
        self.compilerSource(source, valeurSuccès=False, valeurExporté='bad;name=Tests.invoquer')
        self.compilerSource(source, valeurSuccès=False, valeurExporté='missing=Tests.méthodeManquant')


if __name__ == '__main__':
    unittest.main()
