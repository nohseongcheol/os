#!/usr/bin/env python3
"""deklarata 고유번호와 UTF-8 bajt_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Mjete.

외부 구조체의 멤버, varg_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 ndryshoj_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_rrënjë = Path(__file__).resolve().parents[1]

def zbatoj_komandë():
    분석 = json.loads((Project_rrënjë/'build/한국어화/시언어분석.json').read_text())
    if 분석['GABIM']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    emër_tabelë = json.loads((Project_rrënjë/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_rrënjë/'명명/규격이름.json').read_text()))
    deklarata_tabelë = 분석['deklarata']
    바꿀선언 = {UNIQUE_VALUE:emër_tabelë[futje_VALUE['Emër']] for UNIQUE_VALUE,futje_VALUE in deklarata_tabelë.items()
                if futje_VALUE['Emër'] in emër_tabelë and futje_VALUE['Emër'] not in SD}
    lidhje_tabelë = {futje_VALUE['Emër']:emër_tabelë[futje_VALUE['Emër']] for futje_VALUE in deklarata_tabelë.values()
              if futje_VALUE.get('Lidhu')==4 and futje_VALUE['종류'] in (8,9)
              and futje_VALUE['Emër'] in emër_tabelë and futje_VALUE['Emër'] not in SD}
    # gjeneroj AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Lidhu 이름만 유지한다.
    머리 = ['/* 한국어 burim_degëzim 이름과 기존 makinë Lidhu punë_VALUE. 자동 gjeneroj: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(lidhje_tabelë.items())]
    머리 += ['#endif','']
    (Project_rrënjë/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Ndryshime_Listë = defaultdict(dict)
    for Kartelë,OFFSET_VALUE,Emër,UNIQUE_VALUE in 분석['Referencë']:
        if UNIQUE_VALUE in 바꿀선언:
            Ndryshime_Listë[Kartelë][OFFSET_VALUE] = (Emër,바꿀선언[UNIQUE_VALUE])
    LOG_RECORD = ['Kartelë\t원래바이트위치\t이전이름\t한국어이름']
    injoroj_VALUE = []
    for Kartelë,ndryshoj_VALUE in Ndryshime_Listë.items():
        POZICIONI = Path(Kartelë); 원본 = POZICIONI.read_bytes(); të_dhëna = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(ndryshoj_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                injoroj_VALUE.append((str(POZICIONI.relative_to(Project_rrënjë)),OFFSET_VALUE,옛이름));continue
            të_dhëna = të_dhëna[:OFFSET_VALUE]+새이름.encode()+të_dhëna[끝:]
            LOG_RECORD.append('{}\t{}\t{}\t{}'.format(POZICIONI.relative_to(Project_rrënjë),OFFSET_VALUE,옛이름,새이름))
        POZICIONI.write_bytes(të_dhëna)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {futje_VALUE['Emër']:emër_tabelë[futje_VALUE['Emër']] for futje_VALUE in deklarata_tabelë.values()
              if futje_VALUE['종류']==501 and futje_VALUE['Emër'] in emër_tabelë and futje_VALUE['Emër'] not in SD}
    for POZICIONI in sorted({Path(futje_VALUE['Kartelë']) for futje_VALUE in deklarata_tabelë.values()}):
        linjë_Listë = POZICIONI.read_text().splitlines(True); 이어짐 = False
        for INDEX,linjë in enumerate(linjë_Listë):
            전처리 = 이어짐 or bool(re.match(r'\s*#',linjë))
            이어짐 = 전처리 and linjë.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabelë = emër_tabelë if re.match(r'\s*#\s*define\b',linjë) or 이어짐 else makro_VALUE
                linjë_Listë[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabelë.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],linjë)
        POZICIONI.write_text(''.join(linjë_Listë))
    # 각 자체 Përkthe_burim 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for POZICIONI in sorted({Path(futje_VALUE['Kartelë']) for futje_VALUE in deklarata_tabelë.values()}):
        if POZICIONI.suffix not in ('.c','.cpp'):continue
        homolog_VALUE = '../' * len(POZICIONI.relative_to(Project_rrënjë).parts[:-1]) + '명명/기계연결이름.h'
        POZICIONI.write_text('#include "'+homolog_VALUE+'"\n'+POZICIONI.read_text())
    (Project_rrënjë/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_RECORD)+'\n')
    (Project_rrënjë/'build/한국어화/전처리참조.json').write_text(json.dumps(injoroj_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('ndryshoj_VALUE',len(LOG_RECORD)-1,'전처리 재검토',len(injoroj_VALUE),'makinë Lidhu',len(lidhje_tabelë))

if __name__=='__main__': zbatoj_komandë()
