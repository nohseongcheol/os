#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 ባይት_ዋጋ 위치로 자체 C 이름을 옮기는 일회성 이행 መሳርሒታት.

외부 구조체의 멤버, ሕብረ_ቁምፊ_ዋጋ, C 표준 ተግባር_ዋጋ, 이식 규약은 보존한다.
입력은 ለውጥ_ዋጋ 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def ተግብር_ትእዛዝ():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['ጌጋ']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    ሽም_ሰሌዳ = json.loads((기준/'명명/시언어이름.json').read_text())
    규격 = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {고유:ሽም_ሰሌዳ[ምእታው_ዋጋ['ሽም']] for 고유,ምእታው_ዋጋ in 선언표.items()
                if ምእታው_ዋጋ['ሽም'] in ሽም_ሰሌዳ and ምእታው_ዋጋ['ሽም'] not in 규격}
    ርክብ_ሰሌዳ = {ምእታው_ዋጋ['ሽም']:ሽም_ሰሌዳ[ምእታው_ዋጋ['ሽም']] for ምእታው_ዋጋ in 선언표.values()
              if ምእታው_ዋጋ.get('ኣላግብ')==4 and ምእታው_ዋጋ['종류'] in (8,9)
              and ምእታው_ዋጋ['ሽም'] in ሽም_ሰሌዳ and ምእታው_ዋጋ['ሽም'] not in 규격}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 ኣላግብ 이름만 유지한다.
    머리 = ['/* ትግርኛ ምንጪ_ገረብ 이름과 기존 ማሽን ኣላግብ ዕዮ_ዋጋ_102996da. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(ርክብ_ሰሌዳ.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    ለውጥታት_ዝርዝር = defaultdict(dict)
    for ፋይል,ሽፋን_ዋጋ,ሽም,고유 in 분석['መወከሲ']:
        if 고유 in 바꿀선언:
            ለውጥታት_ዝርዝር[ፋይል][ሽፋን_ዋጋ] = (ሽም,바꿀선언[고유])
    ምዝጉብ_ሪጋ = ['ፋይል\t원래바이트위치\t이전이름\t한국어이름']
    ሸለል_በል_ዋጋ = []
    for ፋይል,ለውጥ_ዋጋ in ለውጥታት_ዝርዝር.items():
        መገዲ = Path(ፋይል); 원본 = መገዲ.read_bytes(); ሓበሬታ = 원본
        for ሽፋን_ዋጋ,(옛이름,새이름) in sorted(ለውጥ_ዋጋ.items(),reverse=True):
            끝 = ሽፋን_ዋጋ+len(옛이름.encode())
            if 원본[ሽፋን_ዋጋ:끝] != 옛이름.encode():
                ሸለል_በል_ዋጋ.append((str(መገዲ.relative_to(기준)),ሽፋን_ዋጋ,옛이름));continue
            ሓበሬታ = ሓበሬታ[:ሽፋን_ዋጋ]+새이름.encode()+ሓበሬታ[끝:]
            ምዝጉብ_ሪጋ.append('{}\t{}\t{}\t{}'.format(መገዲ.relative_to(기준),ሽፋን_ዋጋ,옛이름,새이름))
        መገዲ.write_bytes(ሓበሬታ)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    ማክሮ_ዋጋ = {ምእታው_ዋጋ['ሽም']:ሽም_ሰሌዳ[ምእታው_ዋጋ['ሽም']] for ምእታው_ዋጋ in 선언표.values()
              if ምእታው_ዋጋ['종류']==501 and ምእታው_ዋጋ['ሽም'] in ሽም_ሰሌዳ and ምእታው_ዋጋ['ሽም'] not in 규격}
    for መገዲ in sorted({Path(ምእታው_ዋጋ['ፋይል']) for ምእታው_ዋጋ in 선언표.values()}):
        መስመር_ዝርዝር = መገዲ.read_text().splitlines(True); 이어짐 = False
        for መሐበሪ,መስመር in enumerate(መስመር_ዝርዝር):
            전처리 = 이어짐 or bool(re.match(r'\s*#',መስመር))
            이어짐 = 전처리 and መስመር.rstrip().endswith('\\')
            if 전처리:
                표 = ሽም_ሰሌዳ if re.match(r'\s*#\s*define\b',መስመር) or 이어짐 else ማክሮ_ዋጋ
                መስመር_ዝርዝር[መሐበሪ] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in 규격 else 맞음[0],መስመር)
        መገዲ.write_text(''.join(መስመር_ዝርዝር))
    # 각 자체 ተርጉም_ምንጪ 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for መገዲ in sorted({Path(ምእታው_ዋጋ['ፋይል']) for ምእታው_ዋጋ in 선언표.values()}):
        if መገዲ.suffix not in ('.c','.cpp'):continue
        መዘና_ዋጋ = '../' * len(መገዲ.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        መገዲ.write_text('#include "'+መዘና_ዋጋ+'"\n'+መገዲ.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(ምዝጉብ_ሪጋ)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(ሸለል_በል_ዋጋ,ensure_ascii=False,indent=2)+'\n')
    print('ለውጥ_ዋጋ',len(ምዝጉብ_ሪጋ)-1,'전처리 재검토',len(ሸለል_በል_ዋጋ),'ማሽን ኣላግብ',len(ርክብ_ሰሌዳ))

if __name__=='__main__': ተግብር_ትእዛዝ()
