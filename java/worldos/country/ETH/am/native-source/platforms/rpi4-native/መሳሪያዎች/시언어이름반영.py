#!/usr/bin/env python3
"""እወጃ 고유번호와 UTF-8 ባይት_እሴት 위치로 자체 C 이름을 옮기는 일회성 이행 መሳሪያዎች.

외부 구조체의 멤버, ኅብረቁምፊ_እሴት, C 표준 ተግባር_እሴት, 이식 규약은 보존한다.
입력은 ለውጥ_እሴት 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

አሳይ_ስር = Path(__file__).resolve().parents[1]

def ፈጽም_ትእዛዝ():
    분석 = json.loads((አሳይ_ስር/'build/한국어화/시언어분석.json').read_text())
    if 분석['ስህተት']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    ስም_ሰንጠረዥ = json.loads((አሳይ_ስር/'명명/시언어이름.json').read_text())
    규격 = set(json.loads((አሳይ_ስር/'명명/규격이름.json').read_text()))
    እወጃ_ሰንጠረዥ = 분석['እወጃ']
    바꿀선언 = {고유:ስም_ሰንጠረዥ[ምዝግብ_እሴት['ስም']] for 고유,ምዝግብ_እሴት in እወጃ_ሰንጠረዥ.items()
                if ምዝግብ_እሴት['ስም'] in ስም_ሰንጠረዥ and ምዝግብ_እሴት['ስም'] not in 규격}
    ግንኙነት_ሰንጠረዥ = {ምዝግብ_እሴት['ስም']:ስም_ሰንጠረዥ[ምዝግብ_እሴት['ስም']] for ምዝግብ_እሴት in እወጃ_ሰንጠረዥ.values()
              if ምዝግብ_እሴት.get('መገናኛ')==4 and ምዝግብ_እሴት['종류'] in (8,9)
              and ምዝግብ_እሴት['ስም'] in ስም_ሰንጠረዥ and ምዝግብ_እሴት['ስም'] not in 규격}
    # አዘጋጅ AOT C·어셈블리·공개 SDK가 공유하는 바이너리 መገናኛ 이름만 유지한다.
    머리 = ['/* አማርኛ ምንጭ_ዛፍ 이름과 기존 ማሽን መገናኛ ስራ_እሴት_102996da. 자동 አዘጋጅ: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(ግንኙነት_ሰንጠረዥ.items())]
    머리 += ['#endif','']
    (አሳይ_ስር/'명명/기계연결이름.h').write_text('\n'.join(머리))
    ለውጦች_ዝርዝር = defaultdict(dict)
    for ፋይል,ዝንፍ_እሴት,ስም,고유 in 분석['ማጣቀሻ']:
        if 고유 in 바꿀선언:
            ለውጦች_ዝርዝር[ፋይል][ዝንፍ_እሴት] = (ስም,바꿀선언[고유])
    መዝግብ_ረድፍ = ['ፋይል\t원래바이트위치\t이전이름\t한국어이름']
    ተወው_እሴት = []
    for ፋይል,ለውጥ_እሴት in ለውጦች_ዝርዝር.items():
        መተላለፊያ = Path(ፋይል); 원본 = መተላለፊያ.read_bytes(); ውሂብ = 원본
        for ዝንፍ_እሴት,(옛이름,새이름) in sorted(ለውጥ_እሴት.items(),reverse=True):
            끝 = ዝንፍ_እሴት+len(옛이름.encode())
            if 원본[ዝንፍ_እሴት:끝] != 옛이름.encode():
                ተወው_እሴት.append((str(መተላለፊያ.relative_to(አሳይ_ስር)),ዝንፍ_እሴት,옛이름));continue
            ውሂብ = ውሂብ[:ዝንፍ_እሴት]+새이름.encode()+ውሂብ[끝:]
            መዝግብ_ረድፍ.append('{}\t{}\t{}\t{}'.format(መተላለፊያ.relative_to(አሳይ_ስር),ዝንፍ_እሴት,옛이름,새이름))
        መተላለፊያ.write_bytes(ውሂብ)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    ማክሮ_እሴት = {ምዝግብ_እሴት['ስም']:ስም_ሰንጠረዥ[ምዝግብ_እሴት['ስም']] for ምዝግብ_እሴት in እወጃ_ሰንጠረዥ.values()
              if ምዝግብ_እሴት['종류']==501 and ምዝግብ_እሴት['ስም'] in ስም_ሰንጠረዥ and ምዝግብ_እሴት['ስም'] not in 규격}
    for መተላለፊያ in sorted({Path(ምዝግብ_እሴት['ፋይል']) for ምዝግብ_እሴት in እወጃ_ሰንጠረዥ.values()}):
        መስመር_ዝርዝር = መተላለፊያ.read_text().splitlines(True); 이어짐 = False
        for መረጃ_ጠቆመ,መስመር in enumerate(መስመር_ዝርዝር):
            전처리 = 이어짐 or bool(re.match(r'\s*#',መስመር))
            이어짐 = 전처리 and መስመር.rstrip().endswith('\\')
            if 전처리:
                ፍለጋ_ሰንጠረዥ = ስም_ሰንጠረዥ if re.match(r'\s*#\s*define\b',መስመር) or 이어짐 else ማክሮ_እሴት
                መስመር_ዝርዝር[መረጃ_ጠቆመ] = 낱말.sub(lambda 맞음: ፍለጋ_ሰንጠረዥ.get(맞음[0],맞음[0]) if 맞음[0] not in 규격 else 맞음[0],መስመር)
        መተላለፊያ.write_text(''.join(መስመር_ዝርዝር))
    # 각 자체 ተርጉም_ምንጭ 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for መተላለፊያ in sorted({Path(ምዝግብ_እሴት['ፋይል']) for ምዝግብ_እሴት in እወጃ_ሰንጠረዥ.values()}):
        if መተላለፊያ.suffix not in ('.c','.cpp'):continue
        አቻ_እሴት = '../' * len(መተላለፊያ.relative_to(አሳይ_ስር).parts[:-1]) + '명명/기계연결이름.h'
        መተላለፊያ.write_text('#include "'+አቻ_እሴት+'"\n'+መተላለፊያ.read_text())
    (አሳይ_ስር/'명명/시언어이름대응.tsv').write_text('\n'.join(መዝግብ_ረድፍ)+'\n')
    (አሳይ_ስር/'build/한국어화/전처리참조.json').write_text(json.dumps(ተወው_እሴት,ensure_ascii=False,indent=2)+'\n')
    print('ለውጥ_እሴት',len(መዝግብ_ረድፍ)-1,'전처리 재검토',len(ተወው_እሴት),'ማሽን መገናኛ',len(ግንኙነት_ሰንጠረዥ))

if __name__=='__main__': ፈጽም_ትእዛዝ()
