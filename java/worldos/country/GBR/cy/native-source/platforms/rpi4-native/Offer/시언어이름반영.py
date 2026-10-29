#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 beit_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Offer.

외부 구조체의 멤버, testun_VALUE, C 표준 SWYDDOGAETH_VALUE, 이식 규약은 보존한다.
입력은 newid_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

prosiect_gwraidd = Path(__file__).resolve().parents[1]

def Gweithredu_gorchymyn():
    Dadansoddi_VALUE = json.loads((prosiect_gwraidd/'build/한국어화/시언어분석.json').read_text())
    if Dadansoddi_VALUE['Gwall']: raise SystemExit('Dadansoddi_VALUE 오류를 먼저 해결해야 합니다.')
    enw_tabl = json.loads((prosiect_gwraidd/'명명/시언어이름.json').read_text())
    SD = set(json.loads((prosiect_gwraidd/'명명/규격이름.json').read_text()))
    선언표 = Dadansoddi_VALUE['선언']
    바꿀선언 = {UNIQUE_VALUE:enw_tabl[cofnod_VALUE['Enw']] for UNIQUE_VALUE,cofnod_VALUE in 선언표.items()
                if cofnod_VALUE['Enw'] in enw_tabl and cofnod_VALUE['Enw'] not in SD}
    cyswllt_tabl = {cofnod_VALUE['Enw']:enw_tabl[cofnod_VALUE['Enw']] for cofnod_VALUE in 선언표.values()
              if cofnod_VALUE.get('Cysylltu')==4 and cofnod_VALUE['종류'] in (8,9)
              and cofnod_VALUE['Enw'] in enw_tabl and cofnod_VALUE['Enw'] not in SD}
    # cynhyrchu AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Cysylltu 이름만 유지한다.
    머리 = ['/* Cymraeg ffynhonnell_coeden 이름과 기존 peiriant Cysylltu tasg_VALUE. 자동 cynhyrchu: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(cyswllt_tabl.items())]
    머리 += ['#endif','']
    (prosiect_gwraidd/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Newidiadau_Rhestr = defaultdict(dict)
    for Ffeil,OFFSET_VALUE,Enw,UNIQUE_VALUE in Dadansoddi_VALUE['cyfeiriad']:
        if UNIQUE_VALUE in 바꿀선언:
            Newidiadau_Rhestr[Ffeil][OFFSET_VALUE] = (Enw,바꿀선언[UNIQUE_VALUE])
    LOG_rhes = ['Ffeil\t원래바이트위치\t이전이름\t한국어이름']
    anwybyddu_VALUE = []
    for Ffeil,newid_VALUE in Newidiadau_Rhestr.items():
        LLWYBR = Path(Ffeil); 원본 = LLWYBR.read_bytes(); data = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(newid_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                anwybyddu_VALUE.append((str(LLWYBR.relative_to(prosiect_gwraidd)),OFFSET_VALUE,옛이름));continue
            data = data[:OFFSET_VALUE]+새이름.encode()+data[끝:]
            LOG_rhes.append('{}\t{}\t{}\t{}'.format(LLWYBR.relative_to(prosiect_gwraidd),OFFSET_VALUE,옛이름,새이름))
        LLWYBR.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macro_VALUE = {cofnod_VALUE['Enw']:enw_tabl[cofnod_VALUE['Enw']] for cofnod_VALUE in 선언표.values()
              if cofnod_VALUE['종류']==501 and cofnod_VALUE['Enw'] in enw_tabl and cofnod_VALUE['Enw'] not in SD}
    for LLWYBR in sorted({Path(cofnod_VALUE['Ffeil']) for cofnod_VALUE in 선언표.values()}):
        llinell_Rhestr = LLWYBR.read_text().splitlines(True); 이어짐 = False
        for INDEX,llinell in enumerate(llinell_Rhestr):
            전처리 = 이어짐 or bool(re.match(r'\s*#',llinell))
            이어짐 = 전처리 and llinell.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabl = enw_tabl if re.match(r'\s*#\s*define\b',llinell) or 이어짐 else macro_VALUE
                llinell_Rhestr[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabl.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],llinell)
        LLWYBR.write_text(''.join(llinell_Rhestr))
    # 각 자체 Cyfieithu_ffynhonnell 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for LLWYBR in sorted({Path(cofnod_VALUE['Ffeil']) for cofnod_VALUE in 선언표.values()}):
        if LLWYBR.suffix not in ('.c','.cpp'):continue
        cymar_VALUE = '../' * len(LLWYBR.relative_to(prosiect_gwraidd).parts[:-1]) + '명명/기계연결이름.h'
        LLWYBR.write_text('#include "'+cymar_VALUE+'"\n'+LLWYBR.read_text())
    (prosiect_gwraidd/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_rhes)+'\n')
    (prosiect_gwraidd/'build/한국어화/전처리참조.json').write_text(json.dumps(anwybyddu_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('newid_VALUE',len(LOG_rhes)-1,'전처리 재검토',len(anwybyddu_VALUE),'peiriant Cysylltu',len(cyswllt_tabl))

if __name__=='__main__': Gweithredu_gorchymyn()
