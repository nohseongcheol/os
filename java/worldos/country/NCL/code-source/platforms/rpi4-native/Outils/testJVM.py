#!/usr/bin/env python3
"""OpenJDK와 interne ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from exécuterCommande import racineProjet


def lancer():
    sortie = racineProjet / 'build/verification/jvm'
    cheminClasse = sortie / 'classes'; cheminClasse.mkdir(parents=True, exist_ok=True)
    lotJava = racineProjet / 'dist/jkoros-native-korean.jar'
    ListeSources = sorted((racineProjet / 'Tests/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(lotJava), '-d', str(cheminClasse)] + [str(donnéesChaîne) for donnéesChaîne in ListeSources])
    testListe = [('testObjets', ['valeurArrièrePlan', 'valeurBranche', 'peutCalculer']), ('testExceptions', []), ('TestCollection', []),
             ('testFilsExécution', ['valeurCompteur', 'ActionTâche', 'valeurFilExécution']), ('testHangul', []), ('testMiseEnRéseau', []), ('testMiseEnRéseauCoréen', []), ('testExceptionsCoréen', []), ('sourceHangul', []), ('testFrontières', []), ('valider.testLot', []), ('TestCompatibilitéEntréeÉlément', [])]
    rapportValidation = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((racineProjet / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(lotJava.read_bytes()).hexdigest(), 'tests': []}
    try:
        for nom, inclusions in testListe:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as cheminTemporaire:
                attendu = subprocess.check_output(['java', '-Xverify:all', '-cp', str(cheminClasse) + ':' + str(lotJava), nom], cwd=cheminTemporaire, timeout=15).decode('utf-8')
            argumentsCommande = ['python3', str(racineProjet / 'Outils/exécuterFichier.py'), str(cheminClasse / (nom.replace('.', '/') + '.class'))]
            if '.' in nom: argumentsCommande += ['--class-name', nom]
            for inclure in inclusions: argumentsCommande += ['--include', str(cheminClasse / (inclure + '.class'))]
            if nom == 'sourceHangul': argumentsCommande[2] = str(racineProjet / 'Tests/Java/sourceHangul.java')
            montantAchevé = subprocess.run(argumentsCommande, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            résultatEffectif = montantAchevé.stdout.decode('utf-8').replace('\r\n', '\n')
            (sortie / (nom + '.log')).write_text(résultatEffectif, encoding='utf-8')
            estÉgal = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", résultatEffectif, re.S)
            assert montantAchevé.returncode == 0 and estÉgal, (nom, résultatEffectif)
            résultat = next(donnéesChaîne for donnéesChaîne in estÉgal.groups() if donnéesChaîne is not None) + '\n'
            assert résultat == attendu, (nom, attendu, résultat)
            rapportValidation['tests'].append({'name': nom, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', nom, flush=True)
        # interne JVM에 직접 연결한 français valeurFilExécution/진입점은 OpenJDK용 래퍼가 아니다.
        montantAchevé = subprocess.run(['python3', str(racineProjet/'Outils/exécuterFichier.py'), str(cheminClasse/'testFilsExécutionCoréen.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        résultat = montantAchevé.stdout.decode('utf-8').replace('\r\n', '\n')
        (sortie/'testFilsExécutionCoréen.log').write_text(résultat)
        assert montantAchevé.returncode == 0 and 'français 직접 valeurFilExécution valeurPassage\n' in résultat and '\nexit 0\n' in résultat, résultat
        rapportValidation['direct_korean_thread_and_entry'] = True
        print('PASS: français 직접 valeurFilExécution·exécuterTâche·lancer pointEntréeÉlément', flush=True)
        valide = (cheminClasse / 'testObjets.class').read_bytes()
        testCas = [('판거부', valide[:6] + b'\x00\x35' + valide[8:], 'supported class versions'),
                 ('잘린클래스', valide[:24], 'truncated class file')]
        rapportValidation['rejection_tests'] = []
        for nom, donnéesChargeUtile, texteNotification in testCas:
            testDonnées = sortie / (nom + '.class'); testDonnées.write_bytes(donnéesChargeUtile)
            montantAchevé = subprocess.run(['python3', str(racineProjet / 'Outils/exécuterFichier.py'), str(testDonnées)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            texte = montantAchevé.stdout.decode('utf-8').replace('\r\n', '\n')
            (sortie / (nom + '.log')).write_text(texte, encoding='utf-8')
            assert montantAchevé.returncode == 1 and texteNotification in texte and 'exit 1\n' in texte, (nom, texte)
            rapportValidation['rejection_tests'].append({'name': nom, 'passed': True})
            print('PASS (rejected):', nom, flush=True)
        rapportValidation['passed'] = True
    finally:
        (sortie / 'report.json').write_text(json.dumps(rapportValidation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    lancer()
