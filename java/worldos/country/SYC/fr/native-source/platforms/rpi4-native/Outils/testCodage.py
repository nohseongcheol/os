#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from exécuterCommande import racineProjet

def lancer():
    donnéesRésultat=racineProjet/'build/verification/coding';donnéesRésultat.mkdir(parents=True,exist_ok=True)
    rapportValidation={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(racineProjet/'Outils/sDKExporter.py')])
        with tarfile.open(str(racineProjet/'dist/jkoros-native-aarch64-sdk.tar.gz')) as lotComprimé:lotComprimé.extractall(str(donnéesRésultat))
        trousseDéveloppement=donnéesRésultat/'jkoros-native-sdk'
        listeSymboles=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(trousseDéveloppement/'lib/libposix-kor-user.a')]).decode()
        for nom in ('créerExtrémité','associerAdresse','envoyerDonnéesDatagramme','recevoirDonnéesDatagramme','ouvrirFichier','lireDonnéesFichier','écrireDonnéesFichier'):
            assert ' T '+nom+'\n' in listeSymboles, nom
        (donnéesRésultat/'korean-function-symbols.txt').write_text(listeSymboles)
        rapportValidation['checks'].append('real-korean-c-function-symbols')
        def exécuterCommande(nom,chemin,tableauArgument,attendu):
            positionDonnées=subprocess.run(['python3',str(racineProjet/'Outils/exécuterFichier.py'),str(chemin)]+tableauArgument,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (donnéesRésultat/(nom+'.log')).write_bytes(positionDonnées.stdout);assert positionDonnées.returncode==0,positionDonnées.stdout.decode('utf-8','replace')
            assert attendu.encode() in positionDonnées.stdout,positionDonnées.stdout;rapportValidation['checks'].append(nom)
        for valeurSuffixe in ('c','cpp'):
            fichierCodeExécutable=donnéesRésultat/('Salutation-'+valeurSuffixe+'.elf')
            subprocess.check_call(['python3',str(trousseDéveloppement/'compile.py'),str(trousseDéveloppement/'examples'/('Salutation.'+valeurSuffixe)),'-o',str(fichierCodeExécutable)])
            exécuterCommande('korean-'+valeurSuffixe,fichierCodeExécutable,[],'posix-kor invoquer')
        fichierCodeExécutable=donnéesRésultat/'valeurFlux.elf'
        subprocess.check_call(['python3',str(trousseDéveloppement/'compile.py'),str(trousseDéveloppement/'examples/valeurFlux.c'),'-o',str(fichierCodeExécutable)])
        exécuterCommande('c-stream-queues',fichierCodeExécutable,[],'C posix-kor 연결형 Communication PASS')
        exécuterCommande('korean-python',racineProjet/'Exemples/CodageHangul/Salutation.py',['--include',str(racineProjet/'Exemples/CodageHangul/français.py')],'안녕하세요 누리')
        exécuterCommande('guest-korean-javac',racineProjet/'Exemples/CodageHangul/Salutation.java',[],'안녕하세요 · valeurTotal=42')
        rapportValidation['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(donnéesRésultat/'report.json').write_text(json.dumps(rapportValidation,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':lancer()
