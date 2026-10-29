#!/usr/bin/env python3
"""declaración 고유번호와 UTF-8 byte_VALOR 위치로 자체 C 이름을 옮기는 일회성 이행 Ferramentas.

externo_VALOR 구조체의 멤버, cadea_VALOR, C 표준 FUNCIÓN_VALOR, 이식 규약은 보존한다.
입력은 modificar_VALOR 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_raíz = Path(__file__).resolve().parents[1]

def executar_comando():
    Análise_VALOR = json.loads((Project_raíz/'build/한국어화/시언어분석.json').read_text())
    if Análise_VALOR['ERRO']: raise SystemExit('Análise_VALOR 오류를 먼저 해결해야 합니다.')
    nome_táboa = json.loads((Project_raíz/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_raíz/'명명/규격이름.json').read_text()))
    declaración_táboa = Análise_VALOR['declaración']
    바꿀선언 = {ÚNICO_VALOR:nome_táboa[introdución_VALOR['Nome']] for ÚNICO_VALOR,introdución_VALOR in declaración_táboa.items()
                if introdución_VALOR['Nome'] in nome_táboa and introdución_VALOR['Nome'] not in SD}
    conexión_táboa = {introdución_VALOR['Nome']:nome_táboa[introdución_VALOR['Nome']] for introdución_VALOR in declaración_táboa.values()
              if introdución_VALOR.get('Conectar')==4 and introdución_VALOR['종류'] in (8,9)
              and introdución_VALOR['Nome'] in nome_táboa and introdución_VALOR['Nome'] not in SD}
    # xerar AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Conectar 이름만 유지한다.
    머리 = ['/* Galego fonte_árbore 이름과 기존 máquina Conectar caso_VALOR. 자동 xerar: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(conexión_táboa.items())]
    머리 += ['#endif','']
    (Project_raíz/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Modificacións_Lista = defaultdict(dict)
    for Ficheiro,DESPRAZAMENTO_VALOR,Nome,ÚNICO_VALOR in Análise_VALOR['Material_de_referencia']:
        if ÚNICO_VALOR in 바꿀선언:
            Modificacións_Lista[Ficheiro][DESPRAZAMENTO_VALOR] = (Nome,바꿀선언[ÚNICO_VALOR])
    LOG_fila = ['Ficheiro\t원래바이트위치\t이전이름\t한국어이름']
    ignorar_VALOR = []
    for Ficheiro,modificar_VALOR in Modificacións_Lista.items():
        CAMIÑO = Path(Ficheiro); 원본 = CAMIÑO.read_bytes(); datos = 원본
        for DESPRAZAMENTO_VALOR,(옛이름,새이름) in sorted(modificar_VALOR.items(),reverse=True):
            끝 = DESPRAZAMENTO_VALOR+len(옛이름.encode())
            if 원본[DESPRAZAMENTO_VALOR:끝] != 옛이름.encode():
                ignorar_VALOR.append((str(CAMIÑO.relative_to(Project_raíz)),DESPRAZAMENTO_VALOR,옛이름));continue
            datos = datos[:DESPRAZAMENTO_VALOR]+새이름.encode()+datos[끝:]
            LOG_fila.append('{}\t{}\t{}\t{}'.format(CAMIÑO.relative_to(Project_raíz),DESPRAZAMENTO_VALOR,옛이름,새이름))
        CAMIÑO.write_bytes(datos)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macro_VALOR = {introdución_VALOR['Nome']:nome_táboa[introdución_VALOR['Nome']] for introdución_VALOR in declaración_táboa.values()
              if introdución_VALOR['종류']==501 and introdución_VALOR['Nome'] in nome_táboa and introdución_VALOR['Nome'] not in SD}
    for CAMIÑO in sorted({Path(introdución_VALOR['Ficheiro']) for introdución_VALOR in declaración_táboa.values()}):
        liña_Lista = CAMIÑO.read_text().splitlines(True); 이어짐 = False
        for ÍNDICE,Liña in enumerate(liña_Lista):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Liña))
            이어짐 = 전처리 and Liña.rstrip().endswith('\\')
            if 전처리:
                Busca_táboa = nome_táboa if re.match(r'\s*#\s*define\b',Liña) or 이어짐 else macro_VALOR
                liña_Lista[ÍNDICE] = 낱말.sub(lambda 맞음: Busca_táboa.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Liña)
        CAMIÑO.write_text(''.join(liña_Lista))
    # 각 자체 TRADUCIR_fonte 단위에만 연결표를 넣는다. externo_VALOR 배포본에는 전파하지 않는다.
    for CAMIÑO in sorted({Path(introdución_VALOR['Ficheiro']) for introdución_VALOR in declaración_táboa.values()}):
        if CAMIÑO.suffix not in ('.c','.cpp'):continue
        punto_VALOR = '../' * len(CAMIÑO.relative_to(Project_raíz).parts[:-1]) + '명명/기계연결이름.h'
        CAMIÑO.write_text('#include "'+punto_VALOR+'"\n'+CAMIÑO.read_text())
    (Project_raíz/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_fila)+'\n')
    (Project_raíz/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorar_VALOR,ensure_ascii=False,indent=2)+'\n')
    print('modificar_VALOR',len(LOG_fila)-1,'전처리 재검토',len(ignorar_VALOR),'máquina Conectar',len(conexión_táboa))

if __name__=='__main__': executar_comando()
