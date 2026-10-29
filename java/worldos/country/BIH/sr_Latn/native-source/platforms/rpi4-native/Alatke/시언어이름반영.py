#!/usr/bin/env python3
"""deklaracija 고유번호와 UTF-8 bajt_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Alatke.

spoljni_VALUE 구조체의 멤버, niska_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 promeniti_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

radnja_koren = Path(__file__).resolve().parents[1]

def Izvrši_komanda():
    Analiza_VALUE = json.loads((radnja_koren/'build/한국어화/시언어분석.json').read_text())
    if Analiza_VALUE['greška']: raise SystemExit('Analiza_VALUE 오류를 먼저 해결해야 합니다.')
    ime_tabela = json.loads((radnja_koren/'명명/시언어이름.json').read_text())
    SD = set(json.loads((radnja_koren/'명명/규격이름.json').read_text()))
    deklaracija_tabela = Analiza_VALUE['deklaracija']
    바꿀선언 = {UNIQUE_VALUE:ime_tabela[stavka_VALUE['ime']] for UNIQUE_VALUE,stavka_VALUE in deklaracija_tabela.items()
                if stavka_VALUE['ime'] in ime_tabela and stavka_VALUE['ime'] not in SD}
    veza_tabela = {stavka_VALUE['ime']:ime_tabela[stavka_VALUE['ime']] for stavka_VALUE in deklaracija_tabela.values()
              if stavka_VALUE.get('veze')==4 and stavka_VALUE['종류'] in (8,9)
              and stavka_VALUE['ime'] in ime_tabela and stavka_VALUE['ime'] not in SD}
    # generisati AOT C·어셈블리·공개 SDK가 공유하는 바이너리 veze 이름만 유지한다.
    머리 = ['/* 한국어 izvor_stablo 이름과 기존 računar veze ugovor_VALUE. 자동 generisati: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(veza_tabela.items())]
    머리 += ['#endif','']
    (radnja_koren/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Promene_Lista = defaultdict(dict)
    for Datoteka,Pomak_VALUE,ime,UNIQUE_VALUE in Analiza_VALUE['referenca']:
        if UNIQUE_VALUE in 바꿀선언:
            Promene_Lista[Datoteka][Pomak_VALUE] = (ime,바꿀선언[UNIQUE_VALUE])
    LOG_snimi = ['Datoteka\t원래바이트위치\t이전이름\t한국어이름']
    zanemariti_VALUE = []
    for Datoteka,promeniti_VALUE in Promene_Lista.items():
        putanja = Path(Datoteka); 원본 = putanja.read_bytes(); podaci = 원본
        for Pomak_VALUE,(옛이름,새이름) in sorted(promeniti_VALUE.items(),reverse=True):
            끝 = Pomak_VALUE+len(옛이름.encode())
            if 원본[Pomak_VALUE:끝] != 옛이름.encode():
                zanemariti_VALUE.append((str(putanja.relative_to(radnja_koren)),Pomak_VALUE,옛이름));continue
            podaci = podaci[:Pomak_VALUE]+새이름.encode()+podaci[끝:]
            LOG_snimi.append('{}\t{}\t{}\t{}'.format(putanja.relative_to(radnja_koren),Pomak_VALUE,옛이름,새이름))
        putanja.write_bytes(podaci)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {stavka_VALUE['ime']:ime_tabela[stavka_VALUE['ime']] for stavka_VALUE in deklaracija_tabela.values()
              if stavka_VALUE['종류']==501 and stavka_VALUE['ime'] in ime_tabela and stavka_VALUE['ime'] not in SD}
    for putanja in sorted({Path(stavka_VALUE['Datoteka']) for stavka_VALUE in deklaracija_tabela.values()}):
        red_Lista = putanja.read_text().splitlines(True); 이어짐 = False
        for INDEX,red in enumerate(red_Lista):
            전처리 = 이어짐 or bool(re.match(r'\s*#',red))
            이어짐 = 전처리 and red.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabela = ime_tabela if re.match(r'\s*#\s*define\b',red) or 이어짐 else makro_VALUE
                red_Lista[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabela.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],red)
        putanja.write_text(''.join(red_Lista))
    # 각 자체 prevesti_izvor 단위에만 연결표를 넣는다. spoljni_VALUE 배포본에는 전파하지 않는다.
    for putanja in sorted({Path(stavka_VALUE['Datoteka']) for stavka_VALUE in deklaracija_tabela.values()}):
        if putanja.suffix not in ('.c','.cpp'):continue
        ravnopravni_uređaj_VALUE = '../' * len(putanja.relative_to(radnja_koren).parts[:-1]) + '명명/기계연결이름.h'
        putanja.write_text('#include "'+ravnopravni_uređaj_VALUE+'"\n'+putanja.read_text())
    (radnja_koren/'명명/C_ime_mapiranje.tsv').write_text('\n'.join(LOG_snimi)+'\n')
    (radnja_koren/'build/한국어화/전처리참조.json').write_text(json.dumps(zanemariti_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('promeniti_VALUE',len(LOG_snimi)-1,'전처리 재검토',len(zanemariti_VALUE),'računar veze',len(veza_tabela))

if __name__=='__main__': Izvrši_komanda()
