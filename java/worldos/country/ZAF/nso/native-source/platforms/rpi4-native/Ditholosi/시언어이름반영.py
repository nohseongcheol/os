#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 paete_boleng 위치로 자체 C 이름을 옮기는 일회성 이행 Ditholosi.

외부 구조체의 멤버, molokoloko_boleng, C 표준 TIRO_boleng, 이식 규약은 보존한다.
입력은 fetoša_boleng 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def phethagatša_taelo():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['Phošo']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    leina_tafola = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {SETEE_boleng:leina_tafola[go_tsenya_tshedimošo_boleng['Leina']] for SETEE_boleng,go_tsenya_tshedimošo_boleng in 선언표.items()
                if go_tsenya_tshedimošo_boleng['Leina'] in leina_tafola and go_tsenya_tshedimošo_boleng['Leina'] not in SD}
    kgokaganya_tafola = {go_tsenya_tshedimošo_boleng['Leina']:leina_tafola[go_tsenya_tshedimošo_boleng['Leina']] for go_tsenya_tshedimošo_boleng in 선언표.values()
              if go_tsenya_tshedimošo_boleng.get('Ikgokaganye')==4 and go_tsenya_tshedimošo_boleng['종류'] in (8,9)
              and go_tsenya_tshedimošo_boleng['Leina'] in leina_tafola and go_tsenya_tshedimošo_boleng['Leina'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Ikgokaganye 이름만 유지한다.
    머리 = ['/* 한국어 mohlodi_mohlare 이름과 기존 motšhene Ikgokaganye taba_boleng. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(kgokaganya_tafola.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Diphetogo_Lenaneo = defaultdict(dict)
    for Faele,E_Šetšego_boleng,Leina,SETEE_boleng in 분석['Dipadišo']:
        if SETEE_boleng in 바꿀선언:
            Diphetogo_Lenaneo[Faele][E_Šetšego_boleng] = (Leina,바꿀선언[SETEE_boleng])
    pego_rei = ['Faele\t원래바이트위치\t이전이름\t한국어이름']
    hlokomologa_boleng = []
    for Faele,fetoša_boleng in Diphetogo_Lenaneo.items():
        Tsejana = Path(Faele); 원본 = Tsejana.read_bytes(); data = 원본
        for E_Šetšego_boleng,(옛이름,새이름) in sorted(fetoša_boleng.items(),reverse=True):
            끝 = E_Šetšego_boleng+len(옛이름.encode())
            if 원본[E_Šetšego_boleng:끝] != 옛이름.encode():
                hlokomologa_boleng.append((str(Tsejana.relative_to(기준)),E_Šetšego_boleng,옛이름));continue
            data = data[:E_Šetšego_boleng]+새이름.encode()+data[끝:]
            pego_rei.append('{}\t{}\t{}\t{}'.format(Tsejana.relative_to(기준),E_Šetšego_boleng,옛이름,새이름))
        Tsejana.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makhro_boleng = {go_tsenya_tshedimošo_boleng['Leina']:leina_tafola[go_tsenya_tshedimošo_boleng['Leina']] for go_tsenya_tshedimošo_boleng in 선언표.values()
              if go_tsenya_tshedimošo_boleng['종류']==501 and go_tsenya_tshedimošo_boleng['Leina'] in leina_tafola and go_tsenya_tshedimošo_boleng['Leina'] not in SD}
    for Tsejana in sorted({Path(go_tsenya_tshedimošo_boleng['Faele']) for go_tsenya_tshedimošo_boleng in 선언표.values()}):
        mothaladi_Lenaneo = Tsejana.read_text().splitlines(True); 이어짐 = False
        for lokela,mothaladi in enumerate(mothaladi_Lenaneo):
            전처리 = 이어짐 or bool(re.match(r'\s*#',mothaladi))
            이어짐 = 전처리 and mothaladi.rstrip().endswith('\\')
            if 전처리:
                표 = leina_tafola if re.match(r'\s*#\s*define\b',mothaladi) or 이어짐 else makhro_boleng
                mothaladi_Lenaneo[lokela] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],mothaladi)
        Tsejana.write_text(''.join(mothaladi_Lenaneo))
    # 각 자체 Fetolela_mohlodi 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Tsejana in sorted({Path(go_tsenya_tshedimošo_boleng['Faele']) for go_tsenya_tshedimošo_boleng in 선언표.values()}):
        if Tsejana.suffix not in ('.c','.cpp'):continue
        sedirišwa_sa_legoro_le_tee_boleng = '../' * len(Tsejana.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        Tsejana.write_text('#include "'+sedirišwa_sa_legoro_le_tee_boleng+'"\n'+Tsejana.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(pego_rei)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(hlokomologa_boleng,ensure_ascii=False,indent=2)+'\n')
    print('fetoša_boleng',len(pego_rei)-1,'전처리 재검토',len(hlokomologa_boleng),'motšhene Ikgokaganye',len(kgokaganya_tafola))

if __name__=='__main__': phethagatša_taelo()
