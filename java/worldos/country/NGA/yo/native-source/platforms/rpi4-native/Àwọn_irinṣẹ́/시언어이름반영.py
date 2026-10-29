#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 báìtì_iye 위치로 자체 C 이름을 옮기는 일회성 이행 Àwọn_irinṣẹ́.

외부 구조체의 멤버, fọ́nrán_iye, C 표준 ÀKÀNṢEFỌMÚLÀ_iye, 이식 규약은 보존한다.
입력은 ṣàyípadà_iye 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def ṣiṣẹ́_àṣẹ():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['àṣìṣe']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    orúkọ_atọ́ka = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {Ọ̀TỌ̀_iye:orúkọ_atọ́ka[ìgbéwọlé_iye['Orúkọ']] for Ọ̀TỌ̀_iye,ìgbéwọlé_iye in 선언표.items()
                if ìgbéwọlé_iye['Orúkọ'] in orúkọ_atọ́ka and ìgbéwọlé_iye['Orúkọ'] not in SD}
    Ìsomọ́_atọ́ka = {ìgbéwọlé_iye['Orúkọ']:orúkọ_atọ́ka[ìgbéwọlé_iye['Orúkọ']] for ìgbéwọlé_iye in 선언표.values()
              if ìgbéwọlé_iye.get('Darapọ̀')==4 and ìgbéwọlé_iye['종류'] in (8,9)
              and ìgbéwọlé_iye['Orúkọ'] in orúkọ_atọ́ka and ìgbéwọlé_iye['Orúkọ'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Darapọ̀ 이름만 유지한다.
    머리 = ['/* 한국어 orísun_ètò_afigijúwe 이름과 기존 maṣíìnì Darapọ̀ iṣẹ́_iye. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(Ìsomọ́_atọ́ka.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Àwọn_àyípadà_Àtòkọ = defaultdict(dict)
    for Fáìlì,Ìtayọ_iye,Orúkọ,Ọ̀TỌ̀_iye in 분석['Ìtọ́ka']:
        if Ọ̀TỌ̀_iye in 바꿀선언:
            Àwọn_àyípadà_Àtòkọ[Fáìlì][Ìtayọ_iye] = (Orúkọ,바꿀선언[Ọ̀TỌ̀_iye])
    àkọsílẹ̀_ìṣe_ìlà_ìbú = ['Fáìlì\t원래바이트위치\t이전이름\t한국어이름']
    paátì_iye = []
    for Fáìlì,ṣàyípadà_iye in Àwọn_àyípadà_Àtòkọ.items():
        ọ̀nà = Path(Fáìlì); 원본 = ọ̀nà.read_bytes(); détà = 원본
        for Ìtayọ_iye,(옛이름,새이름) in sorted(ṣàyípadà_iye.items(),reverse=True):
            끝 = Ìtayọ_iye+len(옛이름.encode())
            if 원본[Ìtayọ_iye:끝] != 옛이름.encode():
                paátì_iye.append((str(ọ̀nà.relative_to(기준)),Ìtayọ_iye,옛이름));continue
            détà = détà[:Ìtayọ_iye]+새이름.encode()+détà[끝:]
            àkọsílẹ̀_ìṣe_ìlà_ìbú.append('{}\t{}\t{}\t{}'.format(ọ̀nà.relative_to(기준),Ìtayọ_iye,옛이름,새이름))
        ọ̀nà.write_bytes(détà)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    àtòpọ̀_bọ́tìnnì_ẹ̀bùrú_iye = {ìgbéwọlé_iye['Orúkọ']:orúkọ_atọ́ka[ìgbéwọlé_iye['Orúkọ']] for ìgbéwọlé_iye in 선언표.values()
              if ìgbéwọlé_iye['종류']==501 and ìgbéwọlé_iye['Orúkọ'] in orúkọ_atọ́ka and ìgbéwọlé_iye['Orúkọ'] not in SD}
    for ọ̀nà in sorted({Path(ìgbéwọlé_iye['Fáìlì']) for ìgbéwọlé_iye in 선언표.values()}):
        ìlà_Àtòkọ = ọ̀nà.read_text().splitlines(True); 이어짐 = False
        for wá_atọ̀ka_àkóónú,ìlà in enumerate(ìlà_Àtòkọ):
            전처리 = 이어짐 or bool(re.match(r'\s*#',ìlà))
            이어짐 = 전처리 and ìlà.rstrip().endswith('\\')
            if 전처리:
                표 = orúkọ_atọ́ka if re.match(r'\s*#\s*define\b',ìlà) or 이어짐 else àtòpọ̀_bọ́tìnnì_ẹ̀bùrú_iye
                ìlà_Àtòkọ[wá_atọ̀ka_àkóónú] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],ìlà)
        ọ̀nà.write_text(''.join(ìlà_Àtòkọ))
    # 각 자체 Aṣàtúmọ̀_èdè_orísun 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for ọ̀nà in sorted({Path(ìgbéwọlé_iye['Fáìlì']) for ìgbéwọlé_iye in 선언표.values()}):
        if ọ̀nà.suffix not in ('.c','.cpp'):continue
        ọ̀gbà_iye = '../' * len(ọ̀nà.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        ọ̀nà.write_text('#include "'+ọ̀gbà_iye+'"\n'+ọ̀nà.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(àkọsílẹ̀_ìṣe_ìlà_ìbú)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(paátì_iye,ensure_ascii=False,indent=2)+'\n')
    print('ṣàyípadà_iye',len(àkọsílẹ̀_ìṣe_ìlà_ìbú)-1,'전처리 재검토',len(paátì_iye),'maṣíìnì Darapọ̀',len(Ìsomọ́_atọ́ka))

if __name__=='__main__': ṣiṣẹ́_àṣẹ()
