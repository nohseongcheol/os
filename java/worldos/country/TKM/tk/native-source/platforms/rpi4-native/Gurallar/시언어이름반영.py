#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 baýt_baha 위치로 자체 C 이름을 옮기는 일회성 이행 Gurallar.

외부 구조체의 멤버, setir_baha_6ca8363c, C 표준 FUNCTION_baha, 이식 규약은 보존한다.
입력은 üýtget_baha 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def ýerine_ýetir_buýruk():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['Hata']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    at_tablisa = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_baha:at_tablisa[girizmeklik_baha['Ad']] for UNIQUE_baha,girizmeklik_baha in 선언표.items()
                if girizmeklik_baha['Ad'] in at_tablisa and girizmeklik_baha['Ad'] not in SD}
    birikme_tablisa = {girizmeklik_baha['Ad']:at_tablisa[girizmeklik_baha['Ad']] for girizmeklik_baha in 선언표.values()
              if girizmeklik_baha.get('Birikme')==4 and girizmeklik_baha['종류'] in (8,9)
              and girizmeklik_baha['Ad'] in at_tablisa and girizmeklik_baha['Ad'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Birikme 이름만 유지한다.
    머리 = ['/* 한국어 gor_agaç 이름과 기존 kompýuter Birikme ýumuş_baha_102996da. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(birikme_tablisa.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Üýtgeşiklikler_Sanaw = defaultdict(dict)
    for Faýl,Süýşüriş_baha,Ad,UNIQUE_baha in 분석['Salgylanma']:
        if UNIQUE_baha in 바꿀선언:
            Üýtgeşiklikler_Sanaw[Faýl][Süýşüriş_baha] = (Ad,바꿀선언[UNIQUE_baha])
    hasaba_alyş_setir = ['Faýl\t원래바이트위치\t이전이름\t한국어이름']
    ähmiýet_berme_baha = []
    for Faýl,üýtget_baha in Üýtgeşiklikler_Sanaw.items():
        Ýol = Path(Faýl); 원본 = Ýol.read_bytes(); maglumat = 원본
        for Süýşüriş_baha,(옛이름,새이름) in sorted(üýtget_baha.items(),reverse=True):
            끝 = Süýşüriş_baha+len(옛이름.encode())
            if 원본[Süýşüriş_baha:끝] != 옛이름.encode():
                ähmiýet_berme_baha.append((str(Ýol.relative_to(기준)),Süýşüriş_baha,옛이름));continue
            maglumat = maglumat[:Süýşüriş_baha]+새이름.encode()+maglumat[끝:]
            hasaba_alyş_setir.append('{}\t{}\t{}\t{}'.format(Ýol.relative_to(기준),Süýşüriş_baha,옛이름,새이름))
        Ýol.write_bytes(maglumat)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makros_baha = {girizmeklik_baha['Ad']:at_tablisa[girizmeklik_baha['Ad']] for girizmeklik_baha in 선언표.values()
              if girizmeklik_baha['종류']==501 and girizmeklik_baha['Ad'] in at_tablisa and girizmeklik_baha['Ad'] not in SD}
    for Ýol in sorted({Path(girizmeklik_baha['Faýl']) for girizmeklik_baha in 선언표.values()}):
        setir_Sanaw = Ýol.read_text().splitlines(True); 이어짐 = False
        for indeks,setir in enumerate(setir_Sanaw):
            전처리 = 이어짐 or bool(re.match(r'\s*#',setir))
            이어짐 = 전처리 and setir.rstrip().endswith('\\')
            if 전처리:
                표 = at_tablisa if re.match(r'\s*#\s*define\b',setir) or 이어짐 else makros_baha
                setir_Sanaw[indeks] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],setir)
        Ýol.write_text(''.join(setir_Sanaw))
    # 각 자체 Terjime_gor 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Ýol in sorted({Path(girizmeklik_baha['Faýl']) for girizmeklik_baha in 선언표.values()}):
        if Ýol.suffix not in ('.c','.cpp'):continue
        deň_derejeli_düwün_baha = '../' * len(Ýol.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        Ýol.write_text('#include "'+deň_derejeli_düwün_baha+'"\n'+Ýol.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(hasaba_alyş_setir)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(ähmiýet_berme_baha,ensure_ascii=False,indent=2)+'\n')
    print('üýtget_baha',len(hasaba_alyş_setir)-1,'전처리 재검토',len(ähmiýet_berme_baha),'kompýuter Birikme',len(birikme_tablisa))

if __name__=='__main__': ýerine_ýetir_buýruk()
