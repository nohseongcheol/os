#!/usr/bin/env python3
"""declarație 고유번호와 UTF-8 byte_VALUE 위치로 propriu C 이름을 옮기는 일회성 이행 Instrumente.

extern_VALUE 구조체의 멤버, șir_VALUE, C 표준 funcție_VALUE, 이식 규약은 보존한다.
입력은 schimba_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_rădăcină = Path(__file__).resolve().parents[1]

def executa_comandă():
    Analiză_VALUE = json.loads((Project_rădăcină/'build/한국어화/시언어분석.json').read_text())
    if Analiză_VALUE['eroare']: raise SystemExit('Analiză_VALUE 오류를 먼저 해결해야 합니다.')
    nume_tabel = json.loads((Project_rădăcină/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_rădăcină/'명명/규격이름.json').read_text()))
    declarație_tabel = Analiză_VALUE['declarație']
    바꿀선언 = {UNIQUE_VALUE:nume_tabel[intrare_VALUE['Nume']] for UNIQUE_VALUE,intrare_VALUE in declarație_tabel.items()
                if intrare_VALUE['Nume'] in nume_tabel and intrare_VALUE['Nume'] not in SD}
    conexiune_tabel = {intrare_VALUE['Nume']:nume_tabel[intrare_VALUE['Nume']] for intrare_VALUE in declarație_tabel.values()
              if intrare_VALUE.get('Conectează')==4 and intrare_VALUE['종류'] in (8,9)
              and intrare_VALUE['Nume'] in nume_tabel and intrare_VALUE['Nume'] not in SD}
    # genera AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Conectează 이름만 유지한다.
    머리 = ['/* Română sursă_arborescență 이름과 기존 mașină Conectează caz_VALUE. 자동 genera: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(conexiune_tabel.items())]
    머리 += ['#endif','']
    (Project_rădăcină/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Modificări_Listă = defaultdict(dict)
    for Fișier,OFFSET_VALUE,Nume,UNIQUE_VALUE in Analiză_VALUE['referință']:
        if UNIQUE_VALUE in 바꿀선언:
            Modificări_Listă[Fișier][OFFSET_VALUE] = (Nume,바꿀선언[UNIQUE_VALUE])
    LOG_RECORD = ['Fișier\t원래바이트위치\t이전이름\t한국어이름']
    ignora_VALUE = []
    for Fișier,schimba_VALUE in Modificări_Listă.items():
        Cale = Path(Fișier); 원본 = Cale.read_bytes(); date = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(schimba_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                ignora_VALUE.append((str(Cale.relative_to(Project_rădăcină)),OFFSET_VALUE,옛이름));continue
            date = date[:OFFSET_VALUE]+새이름.encode()+date[끝:]
            LOG_RECORD.append('{}\t{}\t{}\t{}'.format(Cale.relative_to(Project_rădăcină),OFFSET_VALUE,옛이름,새이름))
        Cale.write_bytes(date)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macrocomandă_VALUE = {intrare_VALUE['Nume']:nume_tabel[intrare_VALUE['Nume']] for intrare_VALUE in declarație_tabel.values()
              if intrare_VALUE['종류']==501 and intrare_VALUE['Nume'] in nume_tabel and intrare_VALUE['Nume'] not in SD}
    for Cale in sorted({Path(intrare_VALUE['Fișier']) for intrare_VALUE in declarație_tabel.values()}):
        linie_Listă = Cale.read_text().splitlines(True); 이어짐 = False
        for INDEX,Linie in enumerate(linie_Listă):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Linie))
            이어짐 = 전처리 and Linie.rstrip().endswith('\\')
            if 전처리:
                tabel_de_căutare = nume_tabel if re.match(r'\s*#\s*define\b',Linie) or 이어짐 else macrocomandă_VALUE
                linie_Listă[INDEX] = 낱말.sub(lambda 맞음: tabel_de_căutare.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Linie)
        Cale.write_text(''.join(linie_Listă))
    # 각 propriu TRANSLATE_sursă 단위에만 연결표를 넣는다. extern_VALUE 배포본에는 전파하지 않는다.
    for Cale in sorted({Path(intrare_VALUE['Fișier']) for intrare_VALUE in declarație_tabel.values()}):
        if Cale.suffix not in ('.c','.cpp'):continue
        pereche_VALUE = '../' * len(Cale.relative_to(Project_rădăcină).parts[:-1]) + '명명/기계연결이름.h'
        Cale.write_text('#include "'+pereche_VALUE+'"\n'+Cale.read_text())
    (Project_rădăcină/'명명/C_nume_mapare.tsv').write_text('\n'.join(LOG_RECORD)+'\n')
    (Project_rădăcină/'build/한국어화/전처리참조.json').write_text(json.dumps(ignora_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('schimba_VALUE',len(LOG_RECORD)-1,'전처리 재검토',len(ignora_VALUE),'mașină Conectează',len(conexiune_tabel))

if __name__=='__main__': executa_comandă()
