#!/usr/bin/env python3
"""interne Java portéeLocal 이름을 바꾼다. Chaîne·주석·valeurExtérieur 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

racineProjet = Path(__file__).resolve().parents[1]
valeurAssociation = json.loads((racineProjet / 'nommage/nomsJava.json').read_text())
expressionFragmentBloc = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
enregistrementJournal = []
for valeurRépertoire in ('source', 'Utilisateur/Java', 'JavaFrançais'):
    for chemin in sorted((racineProjet / valeurRépertoire).rglob('*.java')):
        source = chemin.read_text()
        listeFragmentsListe = list(expressionFragmentBloc.finditer(source))
        nomUtilisé = {entréeÉlémentFragmentBloc.group() for entréeÉlémentFragmentBloc in listeFragmentsListe if re.search('[opérandePremier-힣]', entréeÉlémentFragmentBloc.group())}
        associationFichier = {}
        for élémentListePrécédentÉlément, valeurAprès in valeurAssociation.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            nomNouveau = valeurAprès
            while nomNouveau in nomUtilisé: nomNouveau = 'portéeLocal' + nomNouveau
            associationFichier[élémentListePrécédentÉlément] = nomNouveau
        modifierValeur = []
        fragmentBlocPrécédentÉlément = ''
        for entréeÉlémentFragmentBloc in listeFragmentsListe:
            motLexical = entréeÉlémentFragmentBloc.group()
            if motLexical.startswith(('//', '/*', '"', "'")): continue
            if motLexical in associationFichier and fragmentBlocPrécédentÉlément != '.':
                modifierValeur.append((entréeÉlémentFragmentBloc.start(), entréeÉlémentFragmentBloc.end(), associationFichier[motLexical]))
                enregistrementJournal.append((str(chemin.relative_to(racineProjet)), motLexical, associationFichier[motLexical]))
            fragmentBlocPrécédentÉlément = motLexical
        for lancer, terminaison, nomNouveau in reversed(modifierValeur): source = source[:lancer] + nomNouveau + source[terminaison:]
        if modifierValeur: chemin.write_text(source)
(racineProjet / 'nommage/associationNomJava.tsv').write_text('Fichier\t이전\t이후\n' + ''.join('\t'.join(valeurEntréeÉlément)+'\n' for valeurEntréeÉlément in sorted(set(enregistrementJournal))))
print('Java nom référence changerValeur:', len(enregistrementJournal))
