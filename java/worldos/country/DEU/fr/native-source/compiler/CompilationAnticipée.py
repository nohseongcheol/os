#!/usr/bin/env python3
"""élémentListePrécédentÉlément Python 경로를 Java 미리 번역기에 연결한다. traduireSource 구현은 OutilJava/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from Compilateur import ErreurCompilation

racineProjet = Path(__file__).resolve().parent

class CompilateurCodeMachine:
    def __init__(valeurSoi, classesEntrée, cibleExécution='kernel', nombreÉlémentsMotTas=262144):
        valeurSoi.listeChemin = [Données.chemin for Données in classesEntrée]
        valeurSoi.cibleExécution = cibleExécution
        valeurSoi.nombreÉlémentsMotTas = nombreÉlémentsMotTas

    def générer(valeurSoi, pointEntréeÉlément, entréesListeExporter, notationCaractèreUniversel=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as Tâche:
            cheminRésultat = Path(Tâche)/'generated.c'
            commande = ['sh', str(racineProjet/'tempsDeAnticipé.sh'), '--entry', pointEntréeÉlément,
                    '--profile', valeurSoi.cibleExécution, '--heap-words', str(valeurSoi.nombreÉlémentsMotTas), '-o', str(cheminRésultat)]
            if notationCaractèreUniversel: commande.append('--ucn')
            for valeurAffecter in entréesListeExporter: commande.extend(['--export', valeurAffecter])
            commande.extend(str(chemin) for chemin in valeurSoi.listeChemin)
            résultat = subprocess.run(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if résultat.returncode: raise ErreurCompilation(résultat.stderr.decode('utf-8', 'replace'))
            return cheminRésultat.read_text()

def lancer():
    raise SystemExit(subprocess.call(['sh', str(racineProjet/'tempsDeAnticipé.sh')] + sys.argv[1:]))

if __name__ == '__main__': lancer()
