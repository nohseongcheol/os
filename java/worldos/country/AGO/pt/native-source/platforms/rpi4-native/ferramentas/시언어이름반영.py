#!/usr/bin/env python3
"""declaração 고유번호와 UTF-8 byte_VALOR 위치로 nativo C 이름을 옮기는 일회성 이행 ferramentas.

externo_VALOR 구조체의 멤버, cadeia_VALOR, C 표준 FUNÇÃO_VALOR, 이식 규약은 보존한다.
입력은 alterar_VALOR 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ação_raiz = Path(__file__).resolve().parents[1]

def Executar_comando():
    Analisar_VALOR = json.loads((ação_raiz/'build/한국어화/시언어분석.json').read_text())
    if Analisar_VALOR['erro']: raise SystemExit('Analisar_VALOR 오류를 먼저 해결해야 합니다.')
    nome_tabela = json.loads((ação_raiz/'명명/시언어이름.json').read_text())
    SD = set(json.loads((ação_raiz/'명명/규격이름.json').read_text()))
    declaração_tabela = Analisar_VALOR['declaração']
    바꿀선언 = {ÚNICO_VALOR:nome_tabela[entrada_VALOR_962f286b['Nome']] for ÚNICO_VALOR,entrada_VALOR_962f286b in declaração_tabela.items()
                if entrada_VALOR_962f286b['Nome'] in nome_tabela and entrada_VALOR_962f286b['Nome'] not in SD}
    conexão_tabela = {entrada_VALOR_962f286b['Nome']:nome_tabela[entrada_VALOR_962f286b['Nome']] for entrada_VALOR_962f286b in declaração_tabela.values()
              if entrada_VALOR_962f286b.get('Ligar')==4 and entrada_VALOR_962f286b['Tipo_VALOR'] in (8,9)
              and entrada_VALOR_962f286b['Nome'] in nome_tabela and entrada_VALOR_962f286b['Nome'] not in SD}
    # gerar AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Ligar 이름만 유지한다.
    HEAD_VALOR = ['/* Português fonte_árvore 이름과 기존 computador Ligar valor_do_contrato. 자동 gerar: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    HEAD_VALOR += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(conexão_tabela.items())]
    HEAD_VALOR += ['#endif','']
    (ação_raiz/'명명/기계연결이름.h').write_text('\n'.join(HEAD_VALOR))
    Alterações_Lista = defaultdict(dict)
    for ficheiro,DESLOC_VALOR,Nome,ÚNICO_VALOR in Analisar_VALOR['Referência']:
        if ÚNICO_VALOR in 바꿀선언:
            Alterações_Lista[ficheiro][DESLOC_VALOR] = (Nome,바꿀선언[ÚNICO_VALOR])
    LOG_linha = ['ficheiro\t원래바이트위치\t이전이름\t한국어이름']
    ignorar_VALOR = []
    for ficheiro,alterar_VALOR in Alterações_Lista.items():
        caminho = Path(ficheiro); 원본 = caminho.read_bytes(); dados = 원본
        for DESLOC_VALOR,(옛이름,새이름) in sorted(alterar_VALOR.items(),reverse=True):
            끝 = DESLOC_VALOR+len(옛이름.encode())
            if 원본[DESLOC_VALOR:끝] != 옛이름.encode():
                ignorar_VALOR.append((str(caminho.relative_to(ação_raiz)),DESLOC_VALOR,옛이름));continue
            dados = dados[:DESLOC_VALOR]+새이름.encode()+dados[끝:]
            LOG_linha.append('{}\t{}\t{}\t{}'.format(caminho.relative_to(ação_raiz),DESLOC_VALOR,옛이름,새이름))
        caminho.write_bytes(dados)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macro_VALOR = {entrada_VALOR_962f286b['Nome']:nome_tabela[entrada_VALOR_962f286b['Nome']] for entrada_VALOR_962f286b in declaração_tabela.values()
              if entrada_VALOR_962f286b['Tipo_VALOR']==501 and entrada_VALOR_962f286b['Nome'] in nome_tabela and entrada_VALOR_962f286b['Nome'] not in SD}
    for caminho in sorted({Path(entrada_VALOR_962f286b['ficheiro']) for entrada_VALOR_962f286b in declaração_tabela.values()}):
        linha_Lista = caminho.read_text().splitlines(True); 이어짐 = False
        for ÍNDICE,linha_de_entrada in enumerate(linha_Lista):
            전처리 = 이어짐 or bool(re.match(r'\s*#',linha_de_entrada))
            이어짐 = 전처리 and linha_de_entrada.rstrip().endswith('\\')
            if 전처리:
                tabela_de_pesquisa = nome_tabela if re.match(r'\s*#\s*define\b',linha_de_entrada) or 이어짐 else macro_VALOR
                linha_Lista[ÍNDICE] = 낱말.sub(lambda 맞음: tabela_de_pesquisa.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],linha_de_entrada)
        caminho.write_text(''.join(linha_Lista))
    # 각 nativo mover_fonte 단위에만 연결표를 넣는다. externo_VALOR 배포본에는 전파하지 않는다.
    for caminho in sorted({Path(entrada_VALOR_962f286b['ficheiro']) for entrada_VALOR_962f286b in declaração_tabela.values()}):
        if caminho.suffix not in ('.c','.cpp'):continue
        par_VALOR = '../' * len(caminho.relative_to(ação_raiz).parts[:-1]) + '명명/기계연결이름.h'
        caminho.write_text('#include "'+par_VALOR+'"\n'+caminho.read_text())
    (ação_raiz/'명명/C_nome_mapeamento.tsv').write_text('\n'.join(LOG_linha)+'\n')
    (ação_raiz/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorar_VALOR,ensure_ascii=False,indent=2)+'\n')
    print('alterar_VALOR',len(LOG_linha)-1,'전처리 재검토',len(ignorar_VALOR),'computador Ligar',len(conexão_tabela))

if __name__=='__main__': Executar_comando()
