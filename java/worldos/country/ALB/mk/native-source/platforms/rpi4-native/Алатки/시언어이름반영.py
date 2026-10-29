#!/usr/bin/env python3
"""декларација 고유번호와 UTF-8 бајт_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Алатки.

외부 구조체의 멤버, низа_VALUE_6ca8363c, C 표준 ФУНКЦИЈА_VALUE, 이식 규약은 보존한다.
입력은 измени_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_корен = Path(__file__).resolve().parents[1]

def Изврши_наредба():
    분석 = json.loads((Project_корен/'build/한국어화/시언어분석.json').read_text())
    if 분석['ГРЕШКА']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    име_табела = json.loads((Project_корен/'명명/시언어이름.json').read_text())
    СД = set(json.loads((Project_корен/'명명/규격이름.json').read_text()))
    декларација_табела = 분석['декларација']
    바꿀선언 = {UNIQUE_VALUE:име_табела[внес_VALUE['Име']] for UNIQUE_VALUE,внес_VALUE in декларација_табела.items()
                if внес_VALUE['Име'] in име_табела and внес_VALUE['Име'] not in СД}
    врска_табела = {внес_VALUE['Име']:име_табела[внес_VALUE['Име']] for внес_VALUE in декларација_табела.values()
              if внес_VALUE.get('Врзи_се')==4 and внес_VALUE['종류'] in (8,9)
              and внес_VALUE['Име'] in име_табела and внес_VALUE['Име'] not in СД}
    # генерира AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Врзи_се 이름만 유지한다.
    머리 = ['/* Македонски извор_дрво 이름과 기존 машина Врзи_се задача_VALUE_102996da. 자동 генерира: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(врска_табела.items())]
    머리 += ['#endif','']
    (Project_корен/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Измени_Список = defaultdict(dict)
    for Датотека,OFFSET_VALUE,Име,UNIQUE_VALUE in 분석['Референци']:
        if UNIQUE_VALUE in 바꿀선언:
            Измени_Список[Датотека][OFFSET_VALUE] = (Име,바꿀선언[UNIQUE_VALUE])
    LOG_ред = ['Датотека\t원래바이트위치\t이전이름\t한국어이름']
    игнорира_VALUE = []
    for Датотека,измени_VALUE in Измени_Список.items():
        ПАТЕКА = Path(Датотека); 원본 = ПАТЕКА.read_bytes(); податоци = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(измени_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                игнорира_VALUE.append((str(ПАТЕКА.relative_to(Project_корен)),OFFSET_VALUE,옛이름));continue
            податоци = податоци[:OFFSET_VALUE]+새이름.encode()+податоци[끝:]
            LOG_ред.append('{}\t{}\t{}\t{}'.format(ПАТЕКА.relative_to(Project_корен),OFFSET_VALUE,옛이름,새이름))
        ПАТЕКА.write_bytes(податоци)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    макро_VALUE = {внес_VALUE['Име']:име_табела[внес_VALUE['Име']] for внес_VALUE in декларација_табела.values()
              if внес_VALUE['종류']==501 and внес_VALUE['Име'] in име_табела and внес_VALUE['Име'] not in СД}
    for ПАТЕКА in sorted({Path(внес_VALUE['Датотека']) for внес_VALUE in декларација_табела.values()}):
        ред_Список = ПАТЕКА.read_text().splitlines(True); 이어짐 = False
        for INDEX,ред in enumerate(ред_Список):
            전처리 = 이어짐 or bool(re.match(r'\s*#',ред))
            이어짐 = 전처리 and ред.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_табела = име_табела if re.match(r'\s*#\s*define\b',ред) or 이어짐 else макро_VALUE
                ред_Список[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_табела.get(맞음[0],맞음[0]) if 맞음[0] not in СД else 맞음[0],ред)
        ПАТЕКА.write_text(''.join(ред_Список))
    # 각 자체 Превод_извор 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for ПАТЕКА in sorted({Path(внес_VALUE['Датотека']) for внес_VALUE in декларација_табела.values()}):
        if ПАТЕКА.suffix not in ('.c','.cpp'):continue
        рамноправен_уред_VALUE = '../' * len(ПАТЕКА.relative_to(Project_корен).parts[:-1]) + '명명/기계연결이름.h'
        ПАТЕКА.write_text('#include "'+рамноправен_уред_VALUE+'"\n'+ПАТЕКА.read_text())
    (Project_корен/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_ред)+'\n')
    (Project_корен/'build/한국어화/전처리참조.json').write_text(json.dumps(игнорира_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('измени_VALUE',len(LOG_ред)-1,'전처리 재검토',len(игнорира_VALUE),'машина Врзи_се',len(врска_табела))

if __name__=='__main__': Изврши_наредба()
