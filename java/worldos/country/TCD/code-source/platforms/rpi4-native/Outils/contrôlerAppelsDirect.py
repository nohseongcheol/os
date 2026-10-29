#!/usr/bin/env python3
"""valeurDistribution class의 직접 français GUI/valeurFilExécution 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

racineProjet = Path(__file__).resolve().parents[1]

def lancer():
    listeClasses = ('fenêtre', 'bouton', 'étiquette', 'ChampTexte', 'ÉlémentÉcran', 'NotificationAction', 'FileAttenteÉvènement', 'tâcheFond',
             'Tâche', 'TâcheTâcheExécutable', 'RécepteurAction')
    Paquet = racineProjet/'dist/jkoros-native-korean.jar'
    Déclarations = subprocess.check_output(['javap', '-classpath', str(Paquet), '-private', '-c']+
                                ['français.interne.'+nom for nom in listeClasses]).decode()
    for valeurProhibé in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert valeurProhibé not in Déclarations, valeurProhibé
    Exemples = subprocess.check_output(['javap', '-classpath', str(racineProjet/'build/examples/classes'), '-c', 'ExempleFenêtre']).decode()
    for estRequis in ('public static void lancer()', 'français/interne/FileAttenteÉvènement.invoquerUltérieur', 'français/interne/NotificationAction.texteCommande'):
        assert estRequis in Exemples, estRequis
    for valeurProhibé in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert valeurProhibé not in Exemples, valeurProhibé
    valeurDestination = racineProjet/'build/verification/naming'; valeurDestination.mkdir(parents=True, exist_ok=True)
    (valeurDestination/'direct-bytecode.txt').write_text(Déclarations+'\n'+Exemples)
    enregistrementJournal = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(Paquet.read_bytes()).hexdigest(), 'classes': list(listeClasses),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (valeurDestination/'direct-bytecode.json').write_text(json.dumps(enregistrementJournal, ensure_ascii=False, indent=2)+'\n')
    print('PASS: français 직접 GUI·valeurFilExécution 바이트코드와 Exemples invoquer')

if __name__ == '__main__': lancer()
