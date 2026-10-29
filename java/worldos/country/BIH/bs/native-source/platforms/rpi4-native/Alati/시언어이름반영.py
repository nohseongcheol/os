#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 bajt_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Alati.

iz_eksternog_izvora_VALUE 구조체의 멤버, string_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 promijeniti_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

projicirati_koijen = Path(__file__).resolve().parents[1]

def Izvrši_komanda():
    분석 = json.loads((projicirati_koijen/'build/한국어화/시언어분석.json').read_text())
    if 분석['GRESKA']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    naziv_tabela = json.loads((projicirati_koijen/'명명/시언어이름.json').read_text())
    SD = set(json.loads((projicirati_koijen/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_VALUE:naziv_tabela[unos_VALUE['Naziv']] for UNIQUE_VALUE,unos_VALUE in 선언표.items()
                if unos_VALUE['Naziv'] in naziv_tabela and unos_VALUE['Naziv'] not in SD}
    veza_tabela = {unos_VALUE['Naziv']:naziv_tabela[unos_VALUE['Naziv']] for unos_VALUE in 선언표.values()
              if unos_VALUE.get('Spoji_se')==4 and unos_VALUE['종류'] in (8,9)
              and unos_VALUE['Naziv'] in naziv_tabela and unos_VALUE['Naziv'] not in SD}
    # generirati AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Spoji_se 이름만 유지한다.
    머리 = ['/* 한국어 izvor_stablo 이름과 기존 mašina Spoji_se slučaj_VALUE. 자동 generirati: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(veza_tabela.items())]
    머리 += ['#endif','']
    (projicirati_koijen/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Promjene_spisak = defaultdict(dict)
    for Fajl,Pomak_VALUE,Naziv,UNIQUE_VALUE in 분석['Reference']:
        if UNIQUE_VALUE in 바꿀선언:
            Promjene_spisak[Fajl][Pomak_VALUE] = (Naziv,바꿀선언[UNIQUE_VALUE])
    LOG_red = ['Fajl\t원래바이트위치\t이전이름\t한국어이름']
    ignorirati_VALUE = []
    for Fajl,promijeniti_VALUE in Promjene_spisak.items():
        Putanja = Path(Fajl); 원본 = Putanja.read_bytes(); podaci = 원본
        for Pomak_VALUE,(옛이름,새이름) in sorted(promijeniti_VALUE.items(),reverse=True):
            끝 = Pomak_VALUE+len(옛이름.encode())
            if 원본[Pomak_VALUE:끝] != 옛이름.encode():
                ignorirati_VALUE.append((str(Putanja.relative_to(projicirati_koijen)),Pomak_VALUE,옛이름));continue
            podaci = podaci[:Pomak_VALUE]+새이름.encode()+podaci[끝:]
            LOG_red.append('{}\t{}\t{}\t{}'.format(Putanja.relative_to(projicirati_koijen),Pomak_VALUE,옛이름,새이름))
        Putanja.write_bytes(podaci)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makronaredba_VALUE = {unos_VALUE['Naziv']:naziv_tabela[unos_VALUE['Naziv']] for unos_VALUE in 선언표.values()
              if unos_VALUE['종류']==501 and unos_VALUE['Naziv'] in naziv_tabela and unos_VALUE['Naziv'] not in SD}
    for Putanja in sorted({Path(unos_VALUE['Fajl']) for unos_VALUE in 선언표.values()}):
        redak_spisak = Putanja.read_text().splitlines(True); 이어짐 = False
        for INDEX,Linija in enumerate(redak_spisak):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Linija))
            이어짐 = 전처리 and Linija.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabela = naziv_tabela if re.match(r'\s*#\s*define\b',Linija) or 이어짐 else makronaredba_VALUE
                redak_spisak[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabela.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Linija)
        Putanja.write_text(''.join(redak_spisak))
    # 각 자체 Prevedi_izvor 단위에만 연결표를 넣는다. iz_eksternog_izvora_VALUE 배포본에는 전파하지 않는다.
    for Putanja in sorted({Path(unos_VALUE['Fajl']) for unos_VALUE in 선언표.values()}):
        if Putanja.suffix not in ('.c','.cpp'):continue
        peer_VALUE = '../' * len(Putanja.relative_to(projicirati_koijen).parts[:-1]) + '명명/기계연결이름.h'
        Putanja.write_text('#include "'+peer_VALUE+'"\n'+Putanja.read_text())
    (projicirati_koijen/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_red)+'\n')
    (projicirati_koijen/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorirati_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('promijeniti_VALUE',len(LOG_red)-1,'전처리 재검토',len(ignorirati_VALUE),'mašina Spoji_se',len(veza_tabela))

if __name__=='__main__': Izvrši_komanda()
