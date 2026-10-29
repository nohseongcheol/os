#!/usr/bin/env python3
"""nommage rogner·exception·경로를 검사한다. --시언어는 libclang Déclarations 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

racineProjet = Path(__file__).resolve().parents[1]
racineDépôt = racineProjet.parents[1]

def lancer():
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('--langueC', action='store_true')
    arguments = Analyseur.parse_args()
    échecs = []
    valeurContrat = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    nombreÉlémentsFichier = 0
    tableParamètre = {}
    fonctionArgumentsVariables = set()
    nœudsAST = {}
    compilateursPartagé = [racineDépôt/'compiler/Compilateur.py', racineDépôt/'compiler/CompilationAnticipée.py']
    for chemin in list((racineProjet/'Outils').glob('*.py')) + list((racineProjet/'Exemples').rglob('*.py')) + compilateursPartagé:
        if chemin.name.endswith(('이름반영.py', '이름분석.py')): continue
        nombreÉlémentsFichier += 1
        nœudAST = ast.parse(chemin.read_text()); nœudsAST[chemin] = nœudAST
        for valeurEntréeÉlément in ast.walk(nœudAST):
            if isinstance(valeurEntréeÉlément, ast.FunctionDef):
                tableParamètre.setdefault(valeurEntréeÉlément.name, set()).update(argumentParamètre.arg for argumentParamètre in valeurEntréeÉlément.args.args + valeurEntréeÉlément.args.kwonlyargs)
                if valeurEntréeÉlément.args.kwarg: fonctionArgumentsVariables.add(valeurEntréeÉlément.name)
            if isinstance(valeurEntréeÉlément, ast.ClassDef):
                for Fonction in valeurEntréeÉlément.body:
                    if isinstance(Fonction, ast.FunctionDef) and Fonction.name == '__init__':
                        tableParamètre.setdefault(valeurEntréeÉlément.name, set()).update(argumentParamètre.arg for argumentParamètre in Fonction.args.args + Fonction.args.kwonlyargs)
            nom = ''
            if isinstance(valeurEntréeÉlément, (ast.FunctionDef, ast.ClassDef)): nom = valeurEntréeÉlément.name
            elif isinstance(valeurEntréeÉlément, ast.Name) and isinstance(valeurEntréeÉlément.ctx, ast.Store): nom = valeurEntréeÉlément.id
            elif isinstance(valeurEntréeÉlément, ast.arg): nom = valeurEntréeÉlément.arg
            if nom and nom not in valeurContrat and all(ord(valeurCaractère)<128 for valeurCaractère in nom):
                échecs.append('{}:{}: {}'.format(chemin.relative_to(racineDépôt), valeurEntréeÉlément.lineno, nom))
    for chemin, nœudAST in nœudsAST.items():
        for invoquer in ast.walk(nœudAST):
            if not isinstance(invoquer, ast.Call): continue
            nom = invoquer.func.id if isinstance(invoquer.func, ast.Name) else invoquer.func.attr if isinstance(invoquer.func, ast.Attribute) else ''
            if nom not in tableParamètre or nom in fonctionArgumentsVariables or not any(ord(valeurCaractère)>127 for valeurCaractère in nom): continue
            for argumentParamètre in invoquer.keywords:
                if argumentParamètre.arg and argumentParamètre.arg not in tableParamètre[nom]:
                    échecs.append('{}:{}: {}의 매개변수 {}'.format(chemin.relative_to(racineDépôt), invoquer.lineno, nom, argumentParamètre.arg))
    for ligne in (racineProjet/'nommage/associationNomFichier.tsv').read_text().splitlines()[1:]:
        élémentListePrécédentÉlément, élémentListeActuel, entréeÉlémentValeurProcessus = ligne.split('\t')
        if not (racineProjet/élémentListeActuel).is_file(): échecs.append('valeurDéplacer Fichier méthodeManquant: '+élémentListeActuel)
        if entréeÉlémentValeurProcessus == '호환진입점유지' and not (racineProjet/élémentListePrécédentÉlément).is_file(): échecs.append('호환 pointEntréeÉlément méthodeManquant: '+élémentListePrécédentÉlément)
    Exemples = (racineProjet.parents[1]/'example/java/ExempleRéseau.java').read_text()
    for appelsInterdit in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if appelsInterdit in Exemples: échecs.append('네트워크 예제에 남은 표준 직접 invoquer: '+appelsInterdit)
    # 사용자가 읽는 Java 예제는 motsRéservé/리터럴을 제외한 식별자도 construireTous 한국어다.
    motsRéservé = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for chemin in sorted((racineProjet.parents[1]/'example/java').glob('*.java')):
        source = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', chemin.read_text())
        for nom in re.findall(r'\b[^\W\d]\w*\b', source, re.UNICODE):
            if nom not in motsRéservé and all(ord(valeurCaractère)<128 for valeurCaractère in nom):
                échecs.append('{}: 예제의 영어 valeurIdentificateur {}'.format(chemin.name, nom))
    for nom in ('fenêtre', 'bouton', 'étiquette', 'ChampTexte', 'ÉlémentÉcran', 'FileAttenteÉvènement', 'tâcheFond', 'TâcheTâcheExécutable', 'RécepteurAction', 'NotificationAction', 'Tâche'):
        source = (racineProjet/'JavaFrançais/français/interne'/(nom+'.java')).read_text()
        source = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', source)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', source):
            échecs.append(nom+': français 직접 구현에 표준 valeurObjet 래퍼가 남았습니다.')
    exempleC = (racineProjet.parents[1]/'example/c/ExempleRéseau.c').read_text()
    for nom in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if nom in exempleC: échecs.append('C Communication 예제에 남은 표준 nom: '+nom)
    exemplePython = (racineProjet.parents[1]/'example/python/ExempleRéseau.py').read_text()
    if 'OSError' in exemplePython or '.args' in exemplePython: échecs.append('Python Communication 예제에 남은 표준 exception 직접 valeurUtiliser')
    valeurTête = (racineProjet.parents[1]/'posix-kor/arm64-native/Entêtes/ABIRéseau.h').read_text()
    for nom in ('FamilleInternet', 'PriseRéseauDatagramme', 'ProtocoleDatagramme', 'AdressePriseRéseau', 'AdressePriseRéseauInternet', 'créerExtrémité', 'envoyerDonnéesDatagramme'):
        if re.search(r'^#define\s+'+nom+r'\b', valeurTête, re.M): échecs.append('C 직접 réalisation 대신 valeurMacro valeurUtiliser: '+nom)
    nombreÉlémentsFichierJava = 0
    for valeurRacine in ('source', 'Utilisateur/Java', 'JavaFrançais'):
        for chemin in (racineProjet/valeurRacine).rglob('*.java'):
            nombreÉlémentsFichierJava += 1
            source = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', chemin.read_text())
            for estCorrespondant in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', source):
                échecs.append('{}: 한국어화되지 않은 Déclarations {}'.format(chemin.relative_to(racineProjet), estCorrespondant[1]))
            if valeurRacine == 'JavaFrançais' and re.search(r'\bthrows\s+[A-Za-z]', source):
                échecs.append('{}: 공개 exception Déclarations'.format(chemin.relative_to(racineProjet)))
    nombreFichiersJavaX86 = 0
    nomsJavaStandard = {'String', 'length', 'charAt'}
    for chemin in sorted((racineDépôt/'os/source').glob('*.java')):
        nombreFichiersJavaX86 += 1
        source = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', chemin.read_text())
        for nom in re.findall(r'\b[^\W\d]\w*\b', source, re.UNICODE):
            if nom not in motsRéservé | nomsJavaStandard and all(ord(valeurCaractère)<128 for valeurCaractère in nom):
                échecs.append('{}: interne 영어 valeurIdentificateur {}'.format(chemin.relative_to(racineDépôt), nom))
    enregistrementJournal = {'passed': False, 'python_files': nombreÉlémentsFichier, 'java_files': nombreÉlémentsFichierJava,
          'x86_java_files': nombreFichiersJavaX86, 'host_compiler_python_files': len(compilateursPartagé), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if arguments.langueC:
        subprocess.check_call(['python3', str(racineProjet/'Outils/examinerNomsC.py')])
        examinerValeur = json.loads((racineProjet/'build/한국어화/시언어분석.json').read_text())
        échecs.extend(str(erreur) for erreur in examinerValeur['erreur'])
        aBIExporter = set(json.loads((racineProjet/'nommage/nomsStandard.json').read_text()))
        for valeurEntréeÉlément in examinerValeur['Déclarations'].values():
            nom = valeurEntréeÉlément['nom']; chemin = Path(valeurEntréeÉlément['Fichier'])
            source = chemin.read_bytes()
            # français 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if source[valeurEntréeÉlément['valeurDécalage']:valeurEntréeÉlément['valeurDécalage']+len(nom)] == nom.encode() and nom not in aBIExporter:
                échecs.append('{}:{}: {}'.format(chemin.relative_to(racineProjet), valeurEntréeÉlément['ligne'], nom))
        enregistrementJournal['c_semantic_checked'] = True
        enregistrementJournal['c_source_sha256'] = {str(Path(Fichier).relative_to(racineProjet)):fichierHachage for Fichier,fichierHachage in examinerValeur['원문해시'].items()}
    enregistrementJournal['passed'] = not échecs; enregistrementJournal['failures'] = échecs
    valeurDestination = racineProjet/'build/verification/naming'; valeurDestination.mkdir(parents=True, exist_ok=True)
    (valeurDestination/'report.json').write_text(json.dumps(enregistrementJournal, ensure_ascii=False, indent=2)+'\n')
    if échecs: raise SystemExit('\n'.join(échecs))
    print('PASS: français Déclarations·Fichier chemin·호환 pointEntréeÉlément·Communication Exemples')

if __name__ == '__main__': lancer()
