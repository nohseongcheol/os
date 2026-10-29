#!/usr/bin/env python3
"""declaració 고유번호와 UTF-8 byte_VALOR 위치로 propi C 이름을 옮기는 일회성 이행 Eines.

extern_VALOR 구조체의 멤버, cadena_VALOR, C 표준 FUNCIÓ_VALOR, 이식 규약은 보존한다.
입력은 canviar_VALOR 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_rel = Path(__file__).resolve().parents[1]

def Executa_ordre():
    Anàlisi_VALOR = json.loads((Project_rel/'build/한국어화/시언어분석.json').read_text())
    if Anàlisi_VALOR['s_ha_produït_un_error']: raise SystemExit('Anàlisi_VALOR 오류를 먼저 해결해야 합니다.')
    nom_taula = json.loads((Project_rel/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_rel/'명명/규격이름.json').read_text()))
    declaració_taula = Anàlisi_VALOR['declaració']
    바꿀선언 = {ÚNICS_VALOR:nom_taula[introducció_VALOR['Nom']] for ÚNICS_VALOR,introducció_VALOR in declaració_taula.items()
                if introducció_VALOR['Nom'] in nom_taula and introducció_VALOR['Nom'] not in SD}
    connexió_taula = {introducció_VALOR['Nom']:nom_taula[introducció_VALOR['Nom']] for introducció_VALOR in declaració_taula.values()
              if introducció_VALOR.get('Connecta')==4 and introducció_VALOR['종류'] in (8,9)
              and introducció_VALOR['Nom'] in nom_taula and introducció_VALOR['Nom'] not in SD}
    # generar AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Connecta 이름만 유지한다.
    머리 = ['/* Català font_arbre 이름과 기존 màquina Connecta cas_VALOR. 자동 generar: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(connexió_taula.items())]
    머리 += ['#endif','']
    (Project_rel/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Canvis_Llista = defaultdict(dict)
    for Fitxer,DESPLAÇAMENT_VALOR,Nom,ÚNICS_VALOR in Anàlisi_VALOR['Referència']:
        if ÚNICS_VALOR in 바꿀선언:
            Canvis_Llista[Fitxer][DESPLAÇAMENT_VALOR] = (Nom,바꿀선언[ÚNICS_VALOR])
    LOG_fila = ['Fitxer\t원래바이트위치\t이전이름\t한국어이름']
    ignorar_VALOR = []
    for Fitxer,canviar_VALOR in Canvis_Llista.items():
        Camí = Path(Fitxer); 원본 = Camí.read_bytes(); dades = 원본
        for DESPLAÇAMENT_VALOR,(옛이름,새이름) in sorted(canviar_VALOR.items(),reverse=True):
            끝 = DESPLAÇAMENT_VALOR+len(옛이름.encode())
            if 원본[DESPLAÇAMENT_VALOR:끝] != 옛이름.encode():
                ignorar_VALOR.append((str(Camí.relative_to(Project_rel)),DESPLAÇAMENT_VALOR,옛이름));continue
            dades = dades[:DESPLAÇAMENT_VALOR]+새이름.encode()+dades[끝:]
            LOG_fila.append('{}\t{}\t{}\t{}'.format(Camí.relative_to(Project_rel),DESPLAÇAMENT_VALOR,옛이름,새이름))
        Camí.write_bytes(dades)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macro_VALOR = {introducció_VALOR['Nom']:nom_taula[introducció_VALOR['Nom']] for introducció_VALOR in declaració_taula.values()
              if introducció_VALOR['종류']==501 and introducció_VALOR['Nom'] in nom_taula and introducció_VALOR['Nom'] not in SD}
    for Camí in sorted({Path(introducció_VALOR['Fitxer']) for introducció_VALOR in declaració_taula.values()}):
        línia_Llista = Camí.read_text().splitlines(True); 이어짐 = False
        for INDEX,línia in enumerate(línia_Llista):
            전처리 = 이어짐 or bool(re.match(r'\s*#',línia))
            이어짐 = 전처리 and línia.rstrip().endswith('\\')
            if 전처리:
                Cerca_taula = nom_taula if re.match(r'\s*#\s*define\b',línia) or 이어짐 else macro_VALOR
                línia_Llista[INDEX] = 낱말.sub(lambda 맞음: Cerca_taula.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],línia)
        Camí.write_text(''.join(línia_Llista))
    # 각 propi TRADUEIX_font 단위에만 연결표를 넣는다. extern_VALOR 배포본에는 전파하지 않는다.
    for Camí in sorted({Path(introducció_VALOR['Fitxer']) for introducció_VALOR in declaració_taula.values()}):
        if Camí.suffix not in ('.c','.cpp'):continue
        homòleg_VALOR = '../' * len(Camí.relative_to(Project_rel).parts[:-1]) + '명명/기계연결이름.h'
        Camí.write_text('#include "'+homòleg_VALOR+'"\n'+Camí.read_text())
    (Project_rel/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_fila)+'\n')
    (Project_rel/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorar_VALOR,ensure_ascii=False,indent=2)+'\n')
    print('canviar_VALOR',len(LOG_fila)-1,'전처리 재검토',len(ignorar_VALOR),'màquina Connecta',len(connexió_taula))

if __name__=='__main__': Executa_ordre()
