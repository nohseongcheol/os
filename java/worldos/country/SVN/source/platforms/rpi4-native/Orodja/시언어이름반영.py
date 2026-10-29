#!/usr/bin/env python3
"""deklaracija 고유번호와 UTF-8 bajt_VALUE 위치로 lastno C 이름을 옮기는 일회성 이행 Orodja.

zunanji_VALUE 구조체의 멤버, niz_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 spremeniti_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

pobuda_koren = Path(__file__).resolve().parents[1]

def Izvedi_ukaz():
    analiza_VALUE = json.loads((pobuda_koren/'build/한국어화/시언어분석.json').read_text())
    if analiza_VALUE['NAPAKA']: raise SystemExit('analiza_VALUE 오류를 먼저 해결해야 합니다.')
    ime_tabela = json.loads((pobuda_koren/'명명/시언어이름.json').read_text())
    SD = set(json.loads((pobuda_koren/'명명/규격이름.json').read_text()))
    deklaracija_tabela = analiza_VALUE['deklaracija']
    바꿀선언 = {UNIQUE_VALUE:ime_tabela[vnos_VALUE['Ime']] for UNIQUE_VALUE,vnos_VALUE in deklaracija_tabela.items()
                if vnos_VALUE['Ime'] in ime_tabela and vnos_VALUE['Ime'] not in SD}
    povezava_tabela = {vnos_VALUE['Ime']:ime_tabela[vnos_VALUE['Ime']] for vnos_VALUE in deklaracija_tabela.values()
              if vnos_VALUE.get('Poveži')==4 and vnos_VALUE['종류'] in (8,9)
              and vnos_VALUE['Ime'] in ime_tabela and vnos_VALUE['Ime'] not in SD}
    # ustvariti AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Poveži 이름만 유지한다.
    머리 = ['/* slovenščina vir_drevo 이름과 기존 računalnik Poveži primer_VALUE. 자동 ustvariti: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(povezava_tabela.items())]
    머리 += ['#endif','']
    (pobuda_koren/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Spremembe_Seznam = defaultdict(dict)
    for Datoteka,odmik_VALUE,Ime,UNIQUE_VALUE in analiza_VALUE['Gradiva']:
        if UNIQUE_VALUE in 바꿀선언:
            Spremembe_Seznam[Datoteka][odmik_VALUE] = (Ime,바꿀선언[UNIQUE_VALUE])
    LOG_zapis = ['Datoteka\t원래바이트위치\t이전이름\t한국어이름']
    prezreti_VALUE = []
    for Datoteka,spremeniti_VALUE in Spremembe_Seznam.items():
        POT = Path(Datoteka); 원본 = POT.read_bytes(); podatki = 원본
        for odmik_VALUE,(옛이름,새이름) in sorted(spremeniti_VALUE.items(),reverse=True):
            끝 = odmik_VALUE+len(옛이름.encode())
            if 원본[odmik_VALUE:끝] != 옛이름.encode():
                prezreti_VALUE.append((str(POT.relative_to(pobuda_koren)),odmik_VALUE,옛이름));continue
            podatki = podatki[:odmik_VALUE]+새이름.encode()+podatki[끝:]
            LOG_zapis.append('{}\t{}\t{}\t{}'.format(POT.relative_to(pobuda_koren),odmik_VALUE,옛이름,새이름))
        POT.write_bytes(podatki)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {vnos_VALUE['Ime']:ime_tabela[vnos_VALUE['Ime']] for vnos_VALUE in deklaracija_tabela.values()
              if vnos_VALUE['종류']==501 and vnos_VALUE['Ime'] in ime_tabela and vnos_VALUE['Ime'] not in SD}
    for POT in sorted({Path(vnos_VALUE['Datoteka']) for vnos_VALUE in deklaracija_tabela.values()}):
        linija_Seznam = POT.read_text().splitlines(True); 이어짐 = False
        for INDEX,Črtni in enumerate(linija_Seznam):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Črtni))
            이어짐 = 전처리 and Črtni.rstrip().endswith('\\')
            if 전처리:
                iskalna_tabela = ime_tabela if re.match(r'\s*#\s*define\b',Črtni) or 이어짐 else makro_VALUE
                linija_Seznam[INDEX] = 낱말.sub(lambda 맞음: iskalna_tabela.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Črtni)
        POT.write_text(''.join(linija_Seznam))
    # 각 lastno prevesti_vir 단위에만 연결표를 넣는다. zunanji_VALUE 배포본에는 전파하지 않는다.
    for POT in sorted({Path(vnos_VALUE['Datoteka']) for vnos_VALUE in deklaracija_tabela.values()}):
        if POT.suffix not in ('.c','.cpp'):continue
        enakovreden_VALUE = '../' * len(POT.relative_to(pobuda_koren).parts[:-1]) + '명명/기계연결이름.h'
        POT.write_text('#include "'+enakovreden_VALUE+'"\n'+POT.read_text())
    (pobuda_koren/'명명/C_ime_preslikava.tsv').write_text('\n'.join(LOG_zapis)+'\n')
    (pobuda_koren/'build/한국어화/전처리참조.json').write_text(json.dumps(prezreti_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('spremeniti_VALUE',len(LOG_zapis)-1,'전처리 재검토',len(prezreti_VALUE),'računalnik Poveži',len(povezava_tabela))

if __name__=='__main__': Izvedi_ukaz()
