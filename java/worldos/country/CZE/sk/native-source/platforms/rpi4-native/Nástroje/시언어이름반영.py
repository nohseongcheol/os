#!/usr/bin/env python3
"""deklarácia 고유번호와 UTF-8 Byte_VALUE 위치로 vlastné C 이름을 옮기는 일회성 이행 Nástroje.

externý_VALUE 구조체의 멤버, reťazec_VALUE, C 표준 funkcia_VALUE, 이식 규약은 보존한다.
입력은 zmeniť_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

akcia_koreň = Path(__file__).resolve().parents[1]

def Vykonať_príkaz():
    Analýza_VALUE = json.loads((akcia_koreň/'build/한국어화/시언어분석.json').read_text())
    if Analýza_VALUE['chyba']: raise SystemExit('Analýza_VALUE 오류를 먼저 해결해야 합니다.')
    názov_tabuľka = json.loads((akcia_koreň/'명명/시언어이름.json').read_text())
    SD = set(json.loads((akcia_koreň/'명명/규격이름.json').read_text()))
    deklarácia_tabuľka = Analýza_VALUE['deklarácia']
    바꿀선언 = {UNIQUE_VALUE:názov_tabuľka[položka_VALUE['Názov']] for UNIQUE_VALUE,položka_VALUE in deklarácia_tabuľka.items()
                if položka_VALUE['Názov'] in názov_tabuľka and položka_VALUE['Názov'] not in SD}
    kontakt_tabuľka = {položka_VALUE['Názov']:názov_tabuľka[položka_VALUE['Názov']] for položka_VALUE in deklarácia_tabuľka.values()
              if položka_VALUE.get('Pripojiť')==4 and položka_VALUE['종류'] in (8,9)
              and položka_VALUE['Názov'] in názov_tabuľka and položka_VALUE['Názov'] not in SD}
    # generovať AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Pripojiť 이름만 유지한다.
    머리 = ['/* Slovenský zdroj_strom 이름과 기존 počítač_5eb260fa Pripojiť prípad_VALUE. 자동 generovať: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(kontakt_tabuľka.items())]
    머리 += ['#endif','']
    (akcia_koreň/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Zmeny_Zoznam = defaultdict(dict)
    for Súbor,Posun_VALUE,Názov,UNIQUE_VALUE in Analýza_VALUE['zdroj']:
        if UNIQUE_VALUE in 바꿀선언:
            Zmeny_Zoznam[Súbor][Posun_VALUE] = (Názov,바꿀선언[UNIQUE_VALUE])
    LOG_RECORD = ['Súbor\t원래바이트위치\t이전이름\t한국어이름']
    ignorovať_VALUE = []
    for Súbor,zmeniť_VALUE in Zmeny_Zoznam.items():
        Cesta = Path(Súbor); 원본 = Cesta.read_bytes(); údaje = 원본
        for Posun_VALUE,(옛이름,새이름) in sorted(zmeniť_VALUE.items(),reverse=True):
            끝 = Posun_VALUE+len(옛이름.encode())
            if 원본[Posun_VALUE:끝] != 옛이름.encode():
                ignorovať_VALUE.append((str(Cesta.relative_to(akcia_koreň)),Posun_VALUE,옛이름));continue
            údaje = údaje[:Posun_VALUE]+새이름.encode()+údaje[끝:]
            LOG_RECORD.append('{}\t{}\t{}\t{}'.format(Cesta.relative_to(akcia_koreň),Posun_VALUE,옛이름,새이름))
        Cesta.write_bytes(údaje)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {položka_VALUE['Názov']:názov_tabuľka[položka_VALUE['Názov']] for položka_VALUE in deklarácia_tabuľka.values()
              if položka_VALUE['종류']==501 and položka_VALUE['Názov'] in názov_tabuľka and položka_VALUE['Názov'] not in SD}
    for Cesta in sorted({Path(položka_VALUE['Súbor']) for položka_VALUE in deklarácia_tabuľka.values()}):
        linka_Zoznam = Cesta.read_text().splitlines(True); 이어짐 = False
        for INDEX,riadok in enumerate(linka_Zoznam):
            전처리 = 이어짐 or bool(re.match(r'\s*#',riadok))
            이어짐 = 전처리 and riadok.rstrip().endswith('\\')
            if 전처리:
                vyhľadávacia_tabuľka = názov_tabuľka if re.match(r'\s*#\s*define\b',riadok) or 이어짐 else makro_VALUE
                linka_Zoznam[INDEX] = 낱말.sub(lambda 맞음: vyhľadávacia_tabuľka.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],riadok)
        Cesta.write_text(''.join(linka_Zoznam))
    # 각 vlastné Preložiť_zdroj 단위에만 연결표를 넣는다. externý_VALUE 배포본에는 전파하지 않는다.
    for Cesta in sorted({Path(položka_VALUE['Súbor']) for položka_VALUE in deklarácia_tabuľka.values()}):
        if Cesta.suffix not in ('.c','.cpp'):continue
        partnerský_uzol_VALUE = '../' * len(Cesta.relative_to(akcia_koreň).parts[:-1]) + '명명/기계연결이름.h'
        Cesta.write_text('#include "'+partnerský_uzol_VALUE+'"\n'+Cesta.read_text())
    (akcia_koreň/'명명/C_názov_mapovanie.tsv').write_text('\n'.join(LOG_RECORD)+'\n')
    (akcia_koreň/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorovať_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('zmeniť_VALUE',len(LOG_RECORD)-1,'전처리 재검토',len(ignorovať_VALUE),'počítač_5eb260fa Pripojiť',len(kontakt_tabuľka))

if __name__=='__main__': Vykonať_príkaz()
