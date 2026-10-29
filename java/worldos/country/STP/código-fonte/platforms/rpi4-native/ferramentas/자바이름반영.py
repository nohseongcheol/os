#!/usr/bin/env python3
"""nativo Java local_Scope 이름을 바꾼다. cadeia_VALOR·주석·externo_VALOR 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

ação_raiz = Path(__file__).resolve().parents[1]
mapeamento_VALOR = json.loads((ação_raiz / '명명/자바이름.json').read_text())
parte_expressão = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_linha = []
for Diretório_VALOR in ('códigoFonte', 'espaço_do_utilizador/자바', '한국어자바'):
    for caminho in sorted((ação_raiz / Diretório_VALOR).rglob('*.java')):
        códigoFonte = caminho.read_text()
        토막들 = list(parte_expressão.finditer(códigoFonte))
        사용이름 = {parte_entrada.group() for parte_entrada in 토막들 if re.search('[가-힣]', parte_entrada.group())}
        mapeamento_de_arquivo = {}
        for Anterior_item, 이후 in mapeamento_VALOR.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'local_Scope' + 새이름
            mapeamento_de_arquivo[Anterior_item] = 새이름
        수정 = []
        Anterior_parte = ''
        for parte_entrada in 토막들:
            낱말 = parte_entrada.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in mapeamento_de_arquivo and Anterior_parte != '.':
                수정.append((parte_entrada.start(), parte_entrada.end(), mapeamento_de_arquivo[낱말]))
                LOG_linha.append((str(caminho.relative_to(ação_raiz)), 낱말, mapeamento_de_arquivo[낱말]))
            Anterior_parte = 낱말
        for iniciar, 끝, 새이름 in reversed(수정): códigoFonte = códigoFonte[:iniciar] + 새이름 + códigoFonte[끝:]
        if 수정: caminho.write_text(códigoFonte)
(ação_raiz / '명명/자바이름대응.tsv').write_text('ficheiro\t이전\t이후\n' + ''.join('\t'.join(entrada_VALOR_962f286b)+'\n' for entrada_VALOR_962f286b in sorted(set(LOG_linha))))
print('Java Nome Referência alterar_VALOR:', len(LOG_linha))
