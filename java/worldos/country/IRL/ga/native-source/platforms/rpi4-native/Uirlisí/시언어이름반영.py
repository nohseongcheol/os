#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 beart_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Uirlisí.

외부 구조체의 멤버, teaghrán_VALUE, C 표준 feidhm_VALUE, 이식 규약은 보존한다.
입력은 athraigh_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

teilgean_fréamh = Path(__file__).resolve().parents[1]

def Rith_ordú():
    분석 = json.loads((teilgean_fréamh/'build/한국어화/시언어분석.json').read_text())
    if 분석['ERREÁID']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    ainm_tábla = json.loads((teilgean_fréamh/'명명/시언어이름.json').read_text())
    SD = set(json.loads((teilgean_fréamh/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_VALUE:ainm_tábla[iontráil_VALUE['Ainm']] for UNIQUE_VALUE,iontráil_VALUE in 선언표.items()
                if iontráil_VALUE['Ainm'] in ainm_tábla and iontráil_VALUE['Ainm'] not in SD}
    nasc_tábla = {iontráil_VALUE['Ainm']:ainm_tábla[iontráil_VALUE['Ainm']] for iontráil_VALUE in 선언표.values()
              if iontráil_VALUE.get('Nasc')==4 and iontráil_VALUE['종류'] in (8,9)
              and iontráil_VALUE['Ainm'] in ainm_tábla and iontráil_VALUE['Ainm'] not in SD}
    # giniúint AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Nasc 이름만 유지한다.
    머리 = ['/* Gaeilge foinse_crann 이름과 기존 meaisín Nasc cás_VALUE. 자동 giniúint: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(nasc_tábla.items())]
    머리 += ['#endif','']
    (teilgean_fréamh/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Athruithe_Liosta = defaultdict(dict)
    for Comhad,OFFSET_VALUE,Ainm,UNIQUE_VALUE in 분석['Leabhair_thagartha']:
        if UNIQUE_VALUE in 바꿀선언:
            Athruithe_Liosta[Comhad][OFFSET_VALUE] = (Ainm,바꿀선언[UNIQUE_VALUE])
    LOG_ró = ['Comhad\t원래바이트위치\t이전이름\t한국어이름']
    déan_neamhaird_de_VALUE = []
    for Comhad,athraigh_VALUE in Athruithe_Liosta.items():
        CONAIR = Path(Comhad); 원본 = CONAIR.read_bytes(); sonraí = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(athraigh_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                déan_neamhaird_de_VALUE.append((str(CONAIR.relative_to(teilgean_fréamh)),OFFSET_VALUE,옛이름));continue
            sonraí = sonraí[:OFFSET_VALUE]+새이름.encode()+sonraí[끝:]
            LOG_ró.append('{}\t{}\t{}\t{}'.format(CONAIR.relative_to(teilgean_fréamh),OFFSET_VALUE,옛이름,새이름))
        CONAIR.write_bytes(sonraí)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macra_VALUE = {iontráil_VALUE['Ainm']:ainm_tábla[iontráil_VALUE['Ainm']] for iontráil_VALUE in 선언표.values()
              if iontráil_VALUE['종류']==501 and iontráil_VALUE['Ainm'] in ainm_tábla and iontráil_VALUE['Ainm'] not in SD}
    for CONAIR in sorted({Path(iontráil_VALUE['Comhad']) for iontráil_VALUE in 선언표.values()}):
        líne_Liosta = CONAIR.read_text().splitlines(True); 이어짐 = False
        for INDEX,Líne in enumerate(líne_Liosta):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Líne))
            이어짐 = 전처리 and Líne.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tábla = ainm_tábla if re.match(r'\s*#\s*define\b',Líne) or 이어짐 else macra_VALUE
                líne_Liosta[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tábla.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Líne)
        CONAIR.write_text(''.join(líne_Liosta))
    # 각 자체 Aistrigh_foinse 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for CONAIR in sorted({Path(iontráil_VALUE['Comhad']) for iontráil_VALUE in 선언표.values()}):
        if CONAIR.suffix not in ('.c','.cpp'):continue
        piara_VALUE = '../' * len(CONAIR.relative_to(teilgean_fréamh).parts[:-1]) + '명명/기계연결이름.h'
        CONAIR.write_text('#include "'+piara_VALUE+'"\n'+CONAIR.read_text())
    (teilgean_fréamh/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_ró)+'\n')
    (teilgean_fréamh/'build/한국어화/전처리참조.json').write_text(json.dumps(déan_neamhaird_de_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('athraigh_VALUE',len(LOG_ró)-1,'전처리 재검토',len(déan_neamhaird_de_VALUE),'meaisín Nasc',len(nasc_tábla))

if __name__=='__main__': Rith_ordú()
