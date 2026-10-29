#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 byte_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Għodod.

외부 구조체의 멤버, string_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 bidel_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

pprojetta_għerq = Path(__file__).resolve().parents[1]

def eżegwixxa_kmand():
    분석 = json.loads((pprojetta_għerq/'build/한국어화/시언어분석.json').read_text())
    if 분석['żball']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    isem_tabella = json.loads((pprojetta_għerq/'명명/시언어이름.json').read_text())
    SD = set(json.loads((pprojetta_għerq/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_VALUE:isem_tabella[entrata_VALUE['isem']] for UNIQUE_VALUE,entrata_VALUE in 선언표.items()
                if entrata_VALUE['isem'] in isem_tabella and entrata_VALUE['isem'] not in SD}
    konnessjoni_tabella = {entrata_VALUE['isem']:isem_tabella[entrata_VALUE['isem']] for entrata_VALUE in 선언표.values()
              if entrata_VALUE.get('AQBAD')==4 and entrata_VALUE['종류'] in (8,9)
              and entrata_VALUE['isem'] in isem_tabella and entrata_VALUE['isem'] not in SD}
    # iġġenera AOT C·어셈블리·공개 SDK가 공유하는 바이너리 AQBAD 이름만 유지한다.
    머리 = ['/* Malti sors_siġra 이름과 기존 kompjuter AQBAD każ_VALUE. 자동 iġġenera: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(konnessjoni_tabella.items())]
    머리 += ['#endif','']
    (pprojetta_għerq/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Bidliet_Lista = defaultdict(dict)
    for fajl,OFFSET_VALUE,isem,UNIQUE_VALUE in 분석['Referenza']:
        if UNIQUE_VALUE in 바꿀선언:
            Bidliet_Lista[fajl][OFFSET_VALUE] = (isem,바꿀선언[UNIQUE_VALUE])
    LOG_RECORD = ['fajl\t원래바이트위치\t이전이름\t한국어이름']
    injora_VALUE = []
    for fajl,bidel_VALUE in Bidliet_Lista.items():
        mogħdija = Path(fajl); 원본 = mogħdija.read_bytes(); data = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(bidel_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                injora_VALUE.append((str(mogħdija.relative_to(pprojetta_għerq)),OFFSET_VALUE,옛이름));continue
            data = data[:OFFSET_VALUE]+새이름.encode()+data[끝:]
            LOG_RECORD.append('{}\t{}\t{}\t{}'.format(mogħdija.relative_to(pprojetta_għerq),OFFSET_VALUE,옛이름,새이름))
        mogħdija.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {entrata_VALUE['isem']:isem_tabella[entrata_VALUE['isem']] for entrata_VALUE in 선언표.values()
              if entrata_VALUE['종류']==501 and entrata_VALUE['isem'] in isem_tabella and entrata_VALUE['isem'] not in SD}
    for mogħdija in sorted({Path(entrata_VALUE['fajl']) for entrata_VALUE in 선언표.values()}):
        linja_Lista = mogħdija.read_text().splitlines(True); 이어짐 = False
        for INDEX,linja in enumerate(linja_Lista):
            전처리 = 이어짐 or bool(re.match(r'\s*#',linja))
            이어짐 = 전처리 and linja.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabella = isem_tabella if re.match(r'\s*#\s*define\b',linja) or 이어짐 else makro_VALUE
                linja_Lista[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabella.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],linja)
        mogħdija.write_text(''.join(linja_Lista))
    # 각 자체 Ittraduċi_sors 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for mogħdija in sorted({Path(entrata_VALUE['fajl']) for entrata_VALUE in 선언표.values()}):
        if mogħdija.suffix not in ('.c','.cpp'):continue
        peer_VALUE = '../' * len(mogħdija.relative_to(pprojetta_għerq).parts[:-1]) + '명명/기계연결이름.h'
        mogħdija.write_text('#include "'+peer_VALUE+'"\n'+mogħdija.read_text())
    (pprojetta_għerq/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_RECORD)+'\n')
    (pprojetta_għerq/'build/한국어화/전처리참조.json').write_text(json.dumps(injora_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('bidel_VALUE',len(LOG_RECORD)-1,'전처리 재검토',len(injora_VALUE),'kompjuter AQBAD',len(konnessjoni_tabella))

if __name__=='__main__': eżegwixxa_kmand()
