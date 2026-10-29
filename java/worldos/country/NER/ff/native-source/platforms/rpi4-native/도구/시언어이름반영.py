#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 oktee_njaru 위치로 자체 C 이름을 옮기는 일회성 이행 도구.

외부 구조체의 멤버, ɓoggol_njaru, C 표준 juɓɓol_njaru, 이식 규약은 보존한다.
입력은 waklude_njaru 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def 실행():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['juumre']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    innde_taabal = json.loads((기준/'명명/시언어이름.json').read_text())
    규격 = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {고유:innde_taabal[naatnugol_njaru['innde']] for 고유,naatnugol_njaru in 선언표.items()
                if naatnugol_njaru['innde'] in innde_taabal and naatnugol_njaru['innde'] not in 규격}
    ceŋondiral_taabal = {naatnugol_njaru['innde']:innde_taabal[naatnugol_njaru['innde']] for naatnugol_njaru in 선언표.values()
              if naatnugol_njaru.get('seŋaade')==4 and naatnugol_njaru['종류'] in (8,9)
              and naatnugol_njaru['innde'] in innde_taabal and naatnugol_njaru['innde'] not in 규격}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 seŋaade 이름만 유지한다.
    머리 = ['/* 한국어 sewnde_lekki 이름과 기존 기계 seŋaade haaju_njaru. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(ceŋondiral_taabal.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    변경들 = defaultdict(dict)
    for fiilde,변위,innde,고유 in 분석['참조']:
        if 고유 in 바꿀선언:
            변경들[fiilde][변위] = (innde,바꿀선언[고유])
    suurnal_winndande = ['fiilde\t원래바이트위치\t이전이름\t한국어이름']
    faalkisaade_njaru = []
    for fiilde,waklude_njaru in 변경들.items():
        laawol = Path(fiilde); 원본 = laawol.read_bytes(); keɓe = 원본
        for 변위,(옛이름,새이름) in sorted(waklude_njaru.items(),reverse=True):
            끝 = 변위+len(옛이름.encode())
            if 원본[변위:끝] != 옛이름.encode():
                faalkisaade_njaru.append((str(laawol.relative_to(기준)),변위,옛이름));continue
            keɓe = keɓe[:변위]+새이름.encode()+keɓe[끝:]
            suurnal_winndande.append('{}\t{}\t{}\t{}'.format(laawol.relative_to(기준),변위,옛이름,새이름))
        laawol.write_bytes(keɓe)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    매크로 = {naatnugol_njaru['innde']:innde_taabal[naatnugol_njaru['innde']] for naatnugol_njaru in 선언표.values()
              if naatnugol_njaru['종류']==501 and naatnugol_njaru['innde'] in innde_taabal and naatnugol_njaru['innde'] not in 규격}
    for laawol in sorted({Path(naatnugol_njaru['fiilde']) for naatnugol_njaru in 선언표.values()}):
        diidol_Doggol = laawol.read_text().splitlines(True); 이어짐 = False
        for joopirdu,diidol in enumerate(diidol_Doggol):
            전처리 = 이어짐 or bool(re.match(r'\s*#',diidol))
            이어짐 = 전처리 and diidol.rstrip().endswith('\\')
            if 전처리:
                표 = innde_taabal if re.match(r'\s*#\s*define\b',diidol) or 이어짐 else 매크로
                diidol_Doggol[joopirdu] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in 규격 else 맞음[0],diidol)
        laawol.write_text(''.join(diidol_Doggol))
    # 각 자체 번역 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for laawol in sorted({Path(naatnugol_njaru['fiilde']) for naatnugol_njaru in 선언표.values()}):
        if laawol.suffix not in ('.c','.cpp'):continue
        giƴiraaɗo_njaru = '../' * len(laawol.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        laawol.write_text('#include "'+giƴiraaɗo_njaru+'"\n'+laawol.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(suurnal_winndande)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(faalkisaade_njaru,ensure_ascii=False,indent=2)+'\n')
    print('waklude_njaru',len(suurnal_winndande)-1,'전처리 재검토',len(faalkisaade_njaru),'기계 seŋaade',len(ceŋondiral_taabal))

if __name__=='__main__': 실행()
