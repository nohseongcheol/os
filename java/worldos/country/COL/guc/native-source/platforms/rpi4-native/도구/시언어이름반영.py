#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 waai_ajutuu 위치로 자체 C 이름을 옮기는 일회성 이행 도구.

외부 구조체의 멤버, kaleena_ajutuu, C 표준 함수, 이식 규약은 보존한다.
입력은 변경 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def 실행():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['ajachitia']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    이름표 = json.loads((기준/'명명/시언어이름.json').read_text())
    규격 = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {고유:이름표[ekeroliaa_ajutuu['이름']] for 고유,ekeroliaa_ajutuu in 선언표.items()
                if ekeroliaa_ajutuu['이름'] in 이름표 and ekeroliaa_ajutuu['이름'] not in 규격}
    epe_ipajia_taapüla = {ekeroliaa_ajutuu['이름']:이름표[ekeroliaa_ajutuu['이름']] for ekeroliaa_ajutuu in 선언표.values()
              if ekeroliaa_ajutuu.get('a_ataa')==4 and ekeroliaa_ajutuu['종류'] in (8,9)
              and ekeroliaa_ajutuu['이름'] in 이름표 and ekeroliaa_ajutuu['이름'] not in 규격}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 a_ataa 이름만 유지한다.
    머리 = ['/* 한국어 eejeejetülein_wunu_ulia 이름과 기존 기계 a_ataa achikii_ajutuu. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(epe_ipajia_taapüla.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    변경들 = defaultdict(dict)
    for anaajaalaa,변위,이름,고유 in 분석['참조']:
        if 고유 in 바꿀선언:
            변경들[anaajaalaa][변위] = (이름,바꿀선언[고유])
    aa_innachikimaajatü_aparatsee = ['anaajaalaa\t원래바이트위치\t이전이름\t한국어이름']
    무시 = []
    for anaajaalaa,변경 in 변경들.items():
        wopu_a_ttaaleemüin = Path(anaajaalaa); 원본 = wopu_a_ttaaleemüin.read_bytes(); atijaaya = 원본
        for 변위,(옛이름,새이름) in sorted(변경.items(),reverse=True):
            끝 = 변위+len(옛이름.encode())
            if 원본[변위:끝] != 옛이름.encode():
                무시.append((str(wopu_a_ttaaleemüin.relative_to(기준)),변위,옛이름));continue
            atijaaya = atijaaya[:변위]+새이름.encode()+atijaaya[끝:]
            aa_innachikimaajatü_aparatsee.append('{}\t{}\t{}\t{}'.format(wopu_a_ttaaleemüin.relative_to(기준),변위,옛이름,새이름))
        wopu_a_ttaaleemüin.write_bytes(atijaaya)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    maaküra_ajutuu = {ekeroliaa_ajutuu['이름']:이름표[ekeroliaa_ajutuu['이름']] for ekeroliaa_ajutuu in 선언표.values()
              if ekeroliaa_ajutuu['종류']==501 and ekeroliaa_ajutuu['이름'] in 이름표 and ekeroliaa_ajutuu['이름'] not in 규격}
    for wopu_a_ttaaleemüin in sorted({Path(ekeroliaa_ajutuu['anaajaalaa']) for ekeroliaa_ajutuu in 선언표.values()}):
        줄들 = wopu_a_ttaaleemüin.read_text().splitlines(True); 이어짐 = False
        for ee_iyatialujuna,liinia in enumerate(줄들):
            전처리 = 이어짐 or bool(re.match(r'\s*#',liinia))
            이어짐 = 전처리 and liinia.rstrip().endswith('\\')
            if 전처리:
                표 = 이름표 if re.match(r'\s*#\s*define\b',liinia) or 이어짐 else maaküra_ajutuu
                줄들[ee_iyatialujuna] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in 규격 else 맞음[0],liinia)
        wopu_a_ttaaleemüin.write_text(''.join(줄들))
    # 각 자체 번역 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for wopu_a_ttaaleemüin in sorted({Path(ekeroliaa_ajutuu['anaajaalaa']) for ekeroliaa_ajutuu in 선언표.values()}):
        if wopu_a_ttaaleemüin.suffix not in ('.c','.cpp'):continue
        wanaawasü_ajutuu = '../' * len(wopu_a_ttaaleemüin.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        wopu_a_ttaaleemüin.write_text('#include "'+wanaawasü_ajutuu+'"\n'+wopu_a_ttaaleemüin.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(aa_innachikimaajatü_aparatsee)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(무시,ensure_ascii=False,indent=2)+'\n')
    print('변경',len(aa_innachikimaajatü_aparatsee)-1,'전처리 재검토',len(무시),'기계 a_ataa',len(epe_ipajia_taapüla))

if __name__=='__main__': 실행()
