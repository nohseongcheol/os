#!/usr/bin/env python3
"""deklaracija 고유번호와 UTF-8 bajt_VALUE 위치로 vlastiti C 이름을 옮기는 일회성 이행 Alati.

vanjski_VALUE 구조체의 멤버, niz_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 promijeniti_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

akcija_korijen = Path(__file__).resolve().parents[1]

def Izvrši_naredba():
    analiza_VALUE = json.loads((akcija_korijen/'build/한국어화/시언어분석.json').read_text())
    if analiza_VALUE['GREŠKA']: raise SystemExit('analiza_VALUE 오류를 먼저 해결해야 합니다.')
    naziv_tablica = json.loads((akcija_korijen/'명명/시언어이름.json').read_text())
    SD = set(json.loads((akcija_korijen/'명명/규격이름.json').read_text()))
    deklaracija_tablica = analiza_VALUE['deklaracija']
    바꿀선언 = {UNIQUE_VALUE:naziv_tablica[unos_VALUE['Ime']] for UNIQUE_VALUE,unos_VALUE in deklaracija_tablica.items()
                if unos_VALUE['Ime'] in naziv_tablica and unos_VALUE['Ime'] not in SD}
    veza_tablica = {unos_VALUE['Ime']:naziv_tablica[unos_VALUE['Ime']] for unos_VALUE in deklaracija_tablica.values()
              if unos_VALUE.get('Spoji_se')==4 and unos_VALUE['종류'] in (8,9)
              and unos_VALUE['Ime'] in naziv_tablica and unos_VALUE['Ime'] not in SD}
    # generirati AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Spoji_se 이름만 유지한다.
    머리 = ['/* hrvatski izvor_stablo 이름과 기존 stroj Spoji_se slučaj_VALUE. 자동 generirati: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(veza_tablica.items())]
    머리 += ['#endif','']
    (akcija_korijen/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Promjene_Popis = defaultdict(dict)
    for Datoteka,pomak_VALUE,Ime,UNIQUE_VALUE in analiza_VALUE['Reference']:
        if UNIQUE_VALUE in 바꿀선언:
            Promjene_Popis[Datoteka][pomak_VALUE] = (Ime,바꿀선언[UNIQUE_VALUE])
    LOG_zapis = ['Datoteka\t원래바이트위치\t이전이름\t한국어이름']
    odbaci_VALUE = []
    for Datoteka,promijeniti_VALUE in Promjene_Popis.items():
        PUTANJA = Path(Datoteka); 원본 = PUTANJA.read_bytes(); podaci = 원본
        for pomak_VALUE,(옛이름,새이름) in sorted(promijeniti_VALUE.items(),reverse=True):
            끝 = pomak_VALUE+len(옛이름.encode())
            if 원본[pomak_VALUE:끝] != 옛이름.encode():
                odbaci_VALUE.append((str(PUTANJA.relative_to(akcija_korijen)),pomak_VALUE,옛이름));continue
            podaci = podaci[:pomak_VALUE]+새이름.encode()+podaci[끝:]
            LOG_zapis.append('{}\t{}\t{}\t{}'.format(PUTANJA.relative_to(akcija_korijen),pomak_VALUE,옛이름,새이름))
        PUTANJA.write_bytes(podaci)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {unos_VALUE['Ime']:naziv_tablica[unos_VALUE['Ime']] for unos_VALUE in deklaracija_tablica.values()
              if unos_VALUE['종류']==501 and unos_VALUE['Ime'] in naziv_tablica and unos_VALUE['Ime'] not in SD}
    for PUTANJA in sorted({Path(unos_VALUE['Datoteka']) for unos_VALUE in deklaracija_tablica.values()}):
        red_Popis = PUTANJA.read_text().splitlines(True); 이어짐 = False
        for INDEX,red in enumerate(red_Popis):
            전처리 = 이어짐 or bool(re.match(r'\s*#',red))
            이어짐 = 전처리 and red.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tablica = naziv_tablica if re.match(r'\s*#\s*define\b',red) or 이어짐 else makro_VALUE
                red_Popis[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tablica.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],red)
        PUTANJA.write_text(''.join(red_Popis))
    # 각 vlastiti prevesti_izvor 단위에만 연결표를 넣는다. vanjski_VALUE 배포본에는 전파하지 않는다.
    for PUTANJA in sorted({Path(unos_VALUE['Datoteka']) for unos_VALUE in deklaracija_tablica.values()}):
        if PUTANJA.suffix not in ('.c','.cpp'):continue
        ravnopravan_član_VALUE = '../' * len(PUTANJA.relative_to(akcija_korijen).parts[:-1]) + '명명/기계연결이름.h'
        PUTANJA.write_text('#include "'+ravnopravan_član_VALUE+'"\n'+PUTANJA.read_text())
    (akcija_korijen/'명명/C_naziv_mapiranje.tsv').write_text('\n'.join(LOG_zapis)+'\n')
    (akcija_korijen/'build/한국어화/전처리참조.json').write_text(json.dumps(odbaci_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('promijeniti_VALUE',len(LOG_zapis)-1,'전처리 재검토',len(odbaci_VALUE),'stroj Spoji_se',len(veza_tablica))

if __name__=='__main__': Izvrši_naredba()
