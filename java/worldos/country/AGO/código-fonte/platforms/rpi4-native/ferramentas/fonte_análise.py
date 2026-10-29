#!/usr/bin/env python3
"""repositório_raiz 전체의 nativo 원문을 목록화한다. externo_VALOR/gerar 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

ação_raiz = Path(__file__).resolve().parents[1]
repositório_raiz = ação_raiz.parents[1]

def iniciar():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_linha = []
    for Diretório_VALOR, 하위들, 파일들 in os.walk(str(repositório_raiz)):
        하위들[:] = sorted(Nome for Nome in 하위들 if Nome not in 제외)
        for Nome in sorted(파일들):
            caminho = Path(Diretório_VALOR)/Nome
            if caminho.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            dados = caminho.read_bytes()
            entrada_VALOR_962f286b = {'path': str(caminho.relative_to(repositório_raiz)), 'sha256': hashlib.sha256(dados).hexdigest(),
                  'ascii_filename': all(ord(caractere_VALOR)<128 for caractere_VALOR in caminho.stem)}
            if caminho.suffix == '.py':
                남은선언 = []
                try:
                    for nó_VALOR in ast.walk(ast.parse(dados.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nó_VALOR, (ast.FunctionDef, ast.ClassDef)): 낱말 = nó_VALOR.name
                        elif isinstance(nó_VALOR, ast.arg): 낱말 = nó_VALOR.arg
                        elif isinstance(nó_VALOR, ast.Name) and isinstance(nó_VALOR.ctx, ast.Store): 낱말 = nó_VALOR.id
                        if 낱말 and all(ord(caractere_VALOR)<128 for caractere_VALOR in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nó_VALOR.lineno})
                    entrada_VALOR_962f286b['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as erro:
                    entrada_VALOR_962f286b['parse_error'] = str(erro)
            LOG_linha.append(entrada_VALOR_962f286b)
    resultado = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_linha,
          'file_count': len(LOG_linha), 'ascii_filename_count': sum(entrada_VALOR_962f286b['ascii_filename'] for entrada_VALOR_962f286b in LOG_linha),
          'python_files_with_ascii_declarations': sum(bool(entrada_VALOR_962f286b.get('ascii_python_declarations')) for entrada_VALOR_962f286b in LOG_linha),
          'all_repository_identifiers_korean': False,
          'note': '표준 Ligar 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    destino_VALOR = ação_raiz/'build/verification/naming'; destino_VALOR.mkdir(parents=True, exist_ok=True)
    (destino_VALOR/'source-review.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2)+'\n')
    print('códigoFonte', resultado['file_count'], '개; ASCII nome_de_arquivo_SMS', resultado['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ficheiro', resultado['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': iniciar()
