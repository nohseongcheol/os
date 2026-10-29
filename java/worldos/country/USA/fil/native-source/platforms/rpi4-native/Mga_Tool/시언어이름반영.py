#!/usr/bin/env python3
"""declaration 고유번호와 UTF-8 byte_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Mga_Tool.

외부 구조체의 멤버, string_VALUE, C 표준 pormula_VALUE, 이식 규약은 보존한다.
입력은 baguhin_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_root = Path(__file__).resolve().parents[1]

def Mag_execute_utos():
    분석 = json.loads((Project_root/'build/한국어화/시언어분석.json').read_text())
    if 분석['error']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    pangalan_talahanayan = json.loads((Project_root/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_root/'명명/규격이름.json').read_text()))
    declaration_talahanayan = 분석['declaration']
    바꿀선언 = {UNIQUE_VALUE:pangalan_talahanayan[pagpasok_VALUE['pangalan']] for UNIQUE_VALUE,pagpasok_VALUE in declaration_talahanayan.items()
                if pagpasok_VALUE['pangalan'] in pangalan_talahanayan and pagpasok_VALUE['pangalan'] not in SD}
    koneksyon_talahanayan = {pagpasok_VALUE['pangalan']:pangalan_talahanayan[pagpasok_VALUE['pangalan']] for pagpasok_VALUE in declaration_talahanayan.values()
              if pagpasok_VALUE.get('CONNECT')==4 and pagpasok_VALUE['종류'] in (8,9)
              and pagpasok_VALUE['pangalan'] in pangalan_talahanayan and pagpasok_VALUE['pangalan'] not in SD}
    # mag_generate AOT C·어셈블리·공개 SDK가 공유하는 바이너리 CONNECT 이름만 유지한다.
    머리 = ['/* 한국어 pinagmulan_balangkas 이름과 기존 machine CONNECT kaso_VALUE. 자동 mag_generate: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(koneksyon_talahanayan.items())]
    머리 += ['#endif','']
    (Project_root/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Mga_Pagbabago_list = defaultdict(dict)
    for file,OFFSET_VALUE,pangalan,UNIQUE_VALUE in 분석['Sanggunian']:
        if UNIQUE_VALUE in 바꿀선언:
            Mga_Pagbabago_list[file][OFFSET_VALUE] = (pangalan,바꿀선언[UNIQUE_VALUE])
    LOG_hanay = ['file\t원래바이트위치\t이전이름\t한국어이름']
    balewalain_VALUE = []
    for file,baguhin_VALUE in Mga_Pagbabago_list.items():
        path = Path(file); 원본 = path.read_bytes(); data = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(baguhin_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                balewalain_VALUE.append((str(path.relative_to(Project_root)),OFFSET_VALUE,옛이름));continue
            data = data[:OFFSET_VALUE]+새이름.encode()+data[끝:]
            LOG_hanay.append('{}\t{}\t{}\t{}'.format(path.relative_to(Project_root),OFFSET_VALUE,옛이름,새이름))
        path.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {pagpasok_VALUE['pangalan']:pangalan_talahanayan[pagpasok_VALUE['pangalan']] for pagpasok_VALUE in declaration_talahanayan.values()
              if pagpasok_VALUE['종류']==501 and pagpasok_VALUE['pangalan'] in pangalan_talahanayan and pagpasok_VALUE['pangalan'] not in SD}
    for path in sorted({Path(pagpasok_VALUE['file']) for pagpasok_VALUE in declaration_talahanayan.values()}):
        linya_list = path.read_text().splitlines(True); 이어짐 = False
        for INDEX,linya in enumerate(linya_list):
            전처리 = 이어짐 or bool(re.match(r'\s*#',linya))
            이어짐 = 전처리 and linya.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_talahanayan = pangalan_talahanayan if re.match(r'\s*#\s*define\b',linya) or 이어짐 else makro_VALUE
                linya_list[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_talahanayan.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],linya)
        path.write_text(''.join(linya_list))
    # 각 자체 TRANSLATE_pinagmulan 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for path in sorted({Path(pagpasok_VALUE['file']) for pagpasok_VALUE in declaration_talahanayan.values()}):
        if path.suffix not in ('.c','.cpp'):continue
        peer_VALUE = '../' * len(path.relative_to(Project_root).parts[:-1]) + '명명/기계연결이름.h'
        path.write_text('#include "'+peer_VALUE+'"\n'+path.read_text())
    (Project_root/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_hanay)+'\n')
    (Project_root/'build/한국어화/전처리참조.json').write_text(json.dumps(balewalain_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('baguhin_VALUE',len(LOG_hanay)-1,'전처리 재검토',len(balewalain_VALUE),'machine CONNECT',len(koneksyon_talahanayan))

if __name__=='__main__': Mag_execute_utos()
