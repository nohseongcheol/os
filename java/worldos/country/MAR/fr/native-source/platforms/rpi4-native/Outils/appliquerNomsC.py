#!/usr/bin/env python3
"""Déclarations 고유번호와 UTF-8 valeurOctet 위치로 interne C 이름을 옮기는 일회성 이행 Outils.

valeurExtérieur 구조체의 멤버, Chaîne, C 표준 Fonction, Portage 규약은 보존한다.
입력은 changerValeur valeurAvant 소스에 대한 examinerNomsC.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

racineProjet = Path(__file__).resolve().parents[1]

def exécuterCommande():
    examinerValeur = json.loads((racineProjet/'build/한국어화/시언어분석.json').read_text())
    if examinerValeur['erreur']: raise SystemExit('examinerValeur 오류를 먼저 해결해야 합니다.')
    tableNom = json.loads((racineProjet/'nommage/nomsC.json').read_text())
    définitionStandard = set(json.loads((racineProjet/'nommage/nomsStandard.json').read_text()))
    tableDéclaration = examinerValeur['Déclarations']
    remplacerVersDéclaration = {valeurUnique:tableNom[valeurEntréeÉlément['nom']] for valeurUnique,valeurEntréeÉlément in tableDéclaration.items()
                if valeurEntréeÉlément['nom'] in tableNom and valeurEntréeÉlément['nom'] not in définitionStandard}
    tableConnexion = {valeurEntréeÉlément['nom']:tableNom[valeurEntréeÉlément['nom']] for valeurEntréeÉlément in tableDéclaration.values()
              if valeurEntréeÉlément.get('connecter')==4 and valeurEntréeÉlément['valeurGenre'] in (8,9)
              and valeurEntréeÉlément['nom'] in tableNom and valeurEntréeÉlément['nom'] not in définitionStandard}
    # générer AOT C·어셈블리·공개 SDK가 공유하는 바이너리 connecter 이름만 유지한다.
    valeurTête = ['/* français arbreSource 이름과 기존 machine connecter valeurContrat. 자동 générer: nommage/nomsC.json */',
           '#ifndef entêteNomsLierMachineNatif', '#define entêteNomsLierMachineNatif']
    valeurTête += ['#define '+nomNouveau+' '+nomAncien for nomAncien,nomNouveau in sorted(tableConnexion.items())]
    valeurTête += ['#endif','']
    (racineProjet/'nommage/nomsLierMachine.h').write_text('\n'.join(valeurTête))
    listeChangements = defaultdict(dict)
    for Fichier,valeurDécalage,nom,valeurUnique in examinerValeur['référence']:
        if valeurUnique in remplacerVersDéclaration:
            listeChangements[Fichier][valeurDécalage] = (nom,remplacerVersDéclaration[valeurUnique])
    enregistrementJournal = ['Fichier\t원래바이트위치\t이전이름\t한국어이름']
    ignorerValeur = []
    for Fichier,changerValeur in listeChangements.items():
        chemin = Path(Fichier); original = chemin.read_bytes(); Données = original
        for valeurDécalage,(nomAncien,nomNouveau) in sorted(changerValeur.items(),reverse=True):
            terminaison = valeurDécalage+len(nomAncien.encode())
            if original[valeurDécalage:terminaison] != nomAncien.encode():
                ignorerValeur.append((str(chemin.relative_to(racineProjet)),valeurDécalage,nomAncien));continue
            Données = Données[:valeurDécalage]+nomNouveau.encode()+Données[terminaison:]
            enregistrementJournal.append('{}\t{}\t{}\t{}'.format(chemin.relative_to(racineProjet),valeurDécalage,nomAncien,nomNouveau))
        chemin.write_bytes(Données)
    # sourcePrétraiter 매개변수는 AST의 선언으로 나타나지 않는다. sourcePrétraiter 줄만 보완한다.
    motLexical = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    valeurMacro = {valeurEntréeÉlément['nom']:tableNom[valeurEntréeÉlément['nom']] for valeurEntréeÉlément in tableDéclaration.values()
              if valeurEntréeÉlément['valeurGenre']==501 and valeurEntréeÉlément['nom'] in tableNom and valeurEntréeÉlément['nom'] not in définitionStandard}
    for chemin in sorted({Path(valeurEntréeÉlément['Fichier']) for valeurEntréeÉlément in tableDéclaration.values()}):
        listeLigne = chemin.read_text().splitlines(True); estContinuation = False
        for numéro,ligne in enumerate(listeLigne):
            sourcePrétraiter = estContinuation or bool(re.match(r'\s*#',ligne))
            estContinuation = sourcePrétraiter and ligne.rstrip().endswith('\\')
            if sourcePrétraiter:
                Table = tableNom if re.match(r'\s*#\s*define\b',ligne) or estContinuation else valeurMacro
                listeLigne[numéro] = motLexical.sub(lambda estCorrespondant: Table.get(estCorrespondant[0],estCorrespondant[0]) if estCorrespondant[0] not in définitionStandard else estCorrespondant[0],ligne)
        chemin.write_text(''.join(listeLigne))
    # 각 interne traduireSource 단위에만 연결표를 넣는다. valeurExtérieur 배포본에는 전파하지 않는다.
    for chemin in sorted({Path(valeurEntréeÉlément['Fichier']) for valeurEntréeÉlément in tableDéclaration.values()}):
        if chemin.suffix not in ('.c','.cpp'):continue
        valeurPairRéseau = '../' * len(chemin.relative_to(racineProjet).parts[:-1]) + 'nommage/nomsLierMachine.h'
        chemin.write_text('#include "'+valeurPairRéseau+'"\n'+chemin.read_text())
    (racineProjet/'nommage/associationNomC.tsv').write_text('\n'.join(enregistrementJournal)+'\n')
    (racineProjet/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorerValeur,ensure_ascii=False,indent=2)+'\n')
    print('changerValeur',len(enregistrementJournal)-1,'sourcePrétraiter 재검토',len(ignorerValeur),'machine connecter',len(tableConnexion))

if __name__=='__main__': exécuterCommande()
