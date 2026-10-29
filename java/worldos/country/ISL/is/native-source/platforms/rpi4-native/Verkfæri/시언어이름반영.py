#!/usr/bin/env python3
"""skýrsla 고유번호와 UTF-8 bæti_VALUE 위치로 eigin C 이름을 옮기는 일회성 이행 Verkfæri.

외부 구조체의 멤버, strengur_VALUE, C 표준 fall_VALUE, 이식 규약은 보존한다.
입력은 breyta_VALUE_16f64fe4 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

verk_rót = Path(__file__).resolve().parents[1]

def keyra_skipun():
    분석 = json.loads((verk_rót/'build/한국어화/시언어분석.json').read_text())
    if 분석['Villa']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    heiti_tafla = json.loads((verk_rót/'명명/시언어이름.json').read_text())
    SD = set(json.loads((verk_rót/'명명/규격이름.json').read_text()))
    skýrsla_tafla = 분석['skýrsla']
    바꿀선언 = {UNIQUE_VALUE:heiti_tafla[færsla_VALUE['Heiti']] for UNIQUE_VALUE,færsla_VALUE in skýrsla_tafla.items()
                if færsla_VALUE['Heiti'] in heiti_tafla and færsla_VALUE['Heiti'] not in SD}
    tenging_tafla = {færsla_VALUE['Heiti']:heiti_tafla[færsla_VALUE['Heiti']] for færsla_VALUE in skýrsla_tafla.values()
              if færsla_VALUE.get('Tengjast')==4 and færsla_VALUE['종류'] in (8,9)
              and færsla_VALUE['Heiti'] in heiti_tafla and færsla_VALUE['Heiti'] not in SD}
    # skapa AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Tengjast 이름만 유지한다.
    머리 = ['/* Íslenska uppruni_tré 이름과 기존 vél Tengjast samningsvirði. 자동 skapa: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(tenging_tafla.items())]
    머리 += ['#endif','']
    (verk_rót/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Breytingar_Listi = defaultdict(dict)
    for Skrá,OFFSET_VALUE,Heiti,UNIQUE_VALUE in 분석['tilvísun']:
        if UNIQUE_VALUE in 바꿀선언:
            Breytingar_Listi[Skrá][OFFSET_VALUE] = (Heiti,바꿀선언[UNIQUE_VALUE])
    LOG_lína = ['Skrá\t원래바이트위치\t이전이름\t한국어이름']
    hunsa_VALUE = []
    for Skrá,breyta_VALUE_16f64fe4 in Breytingar_Listi.items():
        SLÓÐ = Path(Skrá); 원본 = SLÓÐ.read_bytes(); gögn = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(breyta_VALUE_16f64fe4.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                hunsa_VALUE.append((str(SLÓÐ.relative_to(verk_rót)),OFFSET_VALUE,옛이름));continue
            gögn = gögn[:OFFSET_VALUE]+새이름.encode()+gögn[끝:]
            LOG_lína.append('{}\t{}\t{}\t{}'.format(SLÓÐ.relative_to(verk_rót),OFFSET_VALUE,옛이름,새이름))
        SLÓÐ.write_bytes(gögn)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    fjölvi_VALUE = {færsla_VALUE['Heiti']:heiti_tafla[færsla_VALUE['Heiti']] for færsla_VALUE in skýrsla_tafla.values()
              if færsla_VALUE['종류']==501 and færsla_VALUE['Heiti'] in heiti_tafla and færsla_VALUE['Heiti'] not in SD}
    for SLÓÐ in sorted({Path(færsla_VALUE['Skrá']) for færsla_VALUE in skýrsla_tafla.values()}):
        lína_Listi = SLÓÐ.read_text().splitlines(True); 이어짐 = False
        for INDEX,Lína in enumerate(lína_Listi):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Lína))
            이어짐 = 전처리 and Lína.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tafla = heiti_tafla if re.match(r'\s*#\s*define\b',Lína) or 이어짐 else fjölvi_VALUE
                lína_Listi[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tafla.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Lína)
        SLÓÐ.write_text(''.join(lína_Listi))
    # 각 eigin Þýða_uppruni 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for SLÓÐ in sorted({Path(færsla_VALUE['Skrá']) for færsla_VALUE in skýrsla_tafla.values()}):
        if SLÓÐ.suffix not in ('.c','.cpp'):continue
        jafningi_VALUE = '../' * len(SLÓÐ.relative_to(verk_rót).parts[:-1]) + '명명/기계연결이름.h'
        SLÓÐ.write_text('#include "'+jafningi_VALUE+'"\n'+SLÓÐ.read_text())
    (verk_rót/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_lína)+'\n')
    (verk_rót/'build/한국어화/전처리참조.json').write_text(json.dumps(hunsa_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('breyta_VALUE_16f64fe4',len(LOG_lína)-1,'전처리 재검토',len(hunsa_VALUE),'vél Tengjast',len(tenging_tafla))

if __name__=='__main__': keyra_skipun()
