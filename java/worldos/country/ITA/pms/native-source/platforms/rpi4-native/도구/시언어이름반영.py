#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 바이트 위치로 자체 C 이름을 옮기는 일회성 이행 도구.

외부 구조체의 멤버, 문자열, C 표준 함수, 이식 규약은 보존한다.
입력은 변경 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def 실행():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['Eror']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    이름표 = json.loads((기준/'명명/시언어이름.json').read_text())
    규격 = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {고유:이름표[항목['Nòm']] for 고유,항목 in 선언표.items()
                if 항목['Nòm'] in 이름표 and 항목['Nòm'] not in 규격}
    연결표 = {항목['Nòm']:이름표[항목['Nòm']] for 항목 in 선언표.values()
              if 항목.get('연결')==4 and 항목['종류'] in (8,9)
              and 항목['Nòm'] in 이름표 and 항목['Nòm'] not in 규격}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 연결 이름만 유지한다.
    머리 = ['/* 한국어 소스 이름과 기존 기계 연결 규약. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(연결표.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    변경들 = defaultdict(dict)
    for 파일,변위,Nòm,고유 in 분석['참조']:
        if 고유 in 바꿀선언:
            변경들[파일][변위] = (Nòm,바꿀선언[고유])
    기록 = ['파일\t원래바이트위치\t이전이름\t한국어이름']
    무시 = []
    for 파일,변경 in 변경들.items():
        경로 = Path(파일); 원본 = 경로.read_bytes(); 자료 = 원본
        for 변위,(옛이름,새이름) in sorted(변경.items(),reverse=True):
            끝 = 변위+len(옛이름.encode())
            if 원본[변위:끝] != 옛이름.encode():
                무시.append((str(경로.relative_to(기준)),변위,옛이름));continue
            자료 = 자료[:변위]+새이름.encode()+자료[끝:]
            기록.append('{}\t{}\t{}\t{}'.format(경로.relative_to(기준),변위,옛이름,새이름))
        경로.write_bytes(자료)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    매크로 = {항목['Nòm']:이름표[항목['Nòm']] for 항목 in 선언표.values()
              if 항목['종류']==501 and 항목['Nòm'] in 이름표 and 항목['Nòm'] not in 규격}
    for 경로 in sorted({Path(항목['파일']) for 항목 in 선언표.values()}):
        줄들 = 경로.read_text().splitlines(True); 이어짐 = False
        for 번호,줄 in enumerate(줄들):
            전처리 = 이어짐 or bool(re.match(r'\s*#',줄))
            이어짐 = 전처리 and 줄.rstrip().endswith('\\')
            if 전처리:
                표 = 이름표 if re.match(r'\s*#\s*define\b',줄) or 이어짐 else 매크로
                줄들[번호] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in 규격 else 맞음[0],줄)
        경로.write_text(''.join(줄들))
    # 각 자체 번역 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for 경로 in sorted({Path(항목['파일']) for 항목 in 선언표.values()}):
        if 경로.suffix not in ('.c','.cpp'):continue
        상대 = '../' * len(경로.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        경로.write_text('#include "'+상대+'"\n'+경로.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(기록)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(무시,ensure_ascii=False,indent=2)+'\n')
    print('변경',len(기록)-1,'전처리 재검토',len(무시),'기계 연결',len(연결표))

if __name__=='__main__': 실행()
