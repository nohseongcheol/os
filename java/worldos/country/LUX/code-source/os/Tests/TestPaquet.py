#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

position = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as valeurTemporaire:
    valeurRépertoire = Path(valeurTemporaire)
    valeurFrontière = valeurRépertoire / '시험장치.java'
    valeurFrontière.write_text('''
class Périphérique { static int valeurHorodatage; static int millisecondes() { return valeurHorodatage++; } static void céderBrièvement() {} }
class TerminalTexte { static void écrire(String valeur) {} static void écrireNuméro(int valeur) {} }
class PiloteRéseau {
    static int adresseBaseEntréeSortie = 1, nombreÉlémentsTransmettre, recevoirNombreÉléments;
    static int[] adressePériphérique = {0x52,0x54,0,0x12,0x34,0x56}, valeurRécent;
    static int recevoir(int[] Données) { return 0; }
    static int envoyer(int[] Données, int longueur) { valeurRécent = Données.clone(); return longueur; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(valeurRépertoire), str(valeurFrontière),
                    str(position / 'source/PileRéseau.java'), str(position / 'Tests/TestPaquet.java')], check=True)
    subprocess.run(['java', '-cp', str(valeurRépertoire), 'TestPaquet'], check=True, timeout=10)
