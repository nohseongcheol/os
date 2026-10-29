#!/usr/bin/env python3
"""racineDépôt 전체의 interne 원문을 목록화한다. valeurExtérieur/générer 코드는 valeurComptageEnCours 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

racineProjet = Path(__file__).resolve().parents[1]
racineDépôt = racineProjet.parents[1]

def lancer():
    valeurExclure = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    enregistrementJournal = []
    for valeurRépertoire, listeEnfants, entréesListeFichier in os.walk(str(racineDépôt)):
        listeEnfants[:] = sorted(nom for nom in listeEnfants if nom not in valeurExclure)
        for nom in sorted(entréesListeFichier):
            chemin = Path(valeurRépertoire)/nom
            if chemin.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            Données = chemin.read_bytes()
            valeurEntréeÉlément = {'path': str(chemin.relative_to(racineDépôt)), 'sha256': hashlib.sha256(Données).hexdigest(),
                  'ascii_filename': all(ord(valeurCaractère)<128 for valeurCaractère in chemin.stem)}
            if chemin.suffix == '.py':
                déclarationsRestant = []
                try:
                    for valeurNœud in ast.walk(ast.parse(Données.decode('utf-8-sig'))):
                        motLexical = ''
                        if isinstance(valeurNœud, (ast.FunctionDef, ast.ClassDef)): motLexical = valeurNœud.name
                        elif isinstance(valeurNœud, ast.arg): motLexical = valeurNœud.arg
                        elif isinstance(valeurNœud, ast.Name) and isinstance(valeurNœud.ctx, ast.Store): motLexical = valeurNœud.id
                        if motLexical and all(ord(valeurCaractère)<128 for valeurCaractère in motLexical) and motLexical != '_' and not motLexical.startswith('__'):
                            déclarationsRestant.append({'name': motLexical, 'line': valeurNœud.lineno})
                    valeurEntréeÉlément['ascii_python_declarations'] = déclarationsRestant
                except (SyntaxError, UnicodeError) as erreur:
                    valeurEntréeÉlément['parse_error'] = str(erreur)
            enregistrementJournal.append(valeurEntréeÉlément)
    résultat = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(valeurExclure), 'files': enregistrementJournal,
          'file_count': len(enregistrementJournal), 'ascii_filename_count': sum(valeurEntréeÉlément['ascii_filename'] for valeurEntréeÉlément in enregistrementJournal),
          'python_files_with_ascii_declarations': sum(bool(valeurEntréeÉlément.get('ascii_python_declarations')) for valeurEntréeÉlément in enregistrementJournal),
          'all_repository_identifiers_korean': False,
          'note': '표준 connecter 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    valeurDestination = racineProjet/'build/verification/naming'; valeurDestination.mkdir(parents=True, exist_ok=True)
    (valeurDestination/'source-review.json').write_text(json.dumps(résultat, ensure_ascii=False, indent=2)+'\n')
    print('source', résultat['file_count'], '개; ASCII texteNomFichier', résultat['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fichier', résultat['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': lancer()
