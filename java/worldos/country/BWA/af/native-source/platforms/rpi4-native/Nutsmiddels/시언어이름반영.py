#!/usr/bin/env python3
"""verklaring 고유번호와 UTF-8 greep_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Nutsmiddels.

외부 구조체의 멤버, string_VALUE, C 표준 funksie_VALUE, 이식 규약은 보존한다.
입력은 verander_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_wortel = Path(__file__).resolve().parents[1]

def uitvoer_bevel():
    분석 = json.loads((Project_wortel/'build/한국어화/시언어분석.json').read_text())
    if 분석['Fout']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    naam_tabel = json.loads((Project_wortel/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_wortel/'명명/규격이름.json').read_text()))
    verklaring_tabel = 분석['verklaring']
    바꿀선언 = {UNIQUE_VALUE:naam_tabel[inskrywing_VALUE['Naam']] for UNIQUE_VALUE,inskrywing_VALUE in verklaring_tabel.items()
                if inskrywing_VALUE['Naam'] in naam_tabel and inskrywing_VALUE['Naam'] not in SD}
    verbinding_tabel = {inskrywing_VALUE['Naam']:naam_tabel[inskrywing_VALUE['Naam']] for inskrywing_VALUE in verklaring_tabel.values()
              if inskrywing_VALUE.get('Koppel')==4 and inskrywing_VALUE['종류'] in (8,9)
              and inskrywing_VALUE['Naam'] in naam_tabel and inskrywing_VALUE['Naam'] not in SD}
    # genereer AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Koppel 이름만 유지한다.
    머리 = ['/* 한국어 bron_boom 이름과 기존 masjien Koppel saak_VALUE. 자동 genereer: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(verbinding_tabel.items())]
    머리 += ['#endif','']
    (Project_wortel/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Veranderings_Lys = defaultdict(dict)
    for Lêer,OFFSET_VALUE,Naam,UNIQUE_VALUE in 분석['Naslaan']:
        if UNIQUE_VALUE in 바꿀선언:
            Veranderings_Lys[Lêer][OFFSET_VALUE] = (Naam,바꿀선언[UNIQUE_VALUE])
    LOG_ry = ['Lêer\t원래바이트위치\t이전이름\t한국어이름']
    ignoreer_VALUE = []
    for Lêer,verander_VALUE in Veranderings_Lys.items():
        Pad = Path(Lêer); 원본 = Pad.read_bytes(); data = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(verander_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                ignoreer_VALUE.append((str(Pad.relative_to(Project_wortel)),OFFSET_VALUE,옛이름));continue
            data = data[:OFFSET_VALUE]+새이름.encode()+data[끝:]
            LOG_ry.append('{}\t{}\t{}\t{}'.format(Pad.relative_to(Project_wortel),OFFSET_VALUE,옛이름,새이름))
        Pad.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {inskrywing_VALUE['Naam']:naam_tabel[inskrywing_VALUE['Naam']] for inskrywing_VALUE in verklaring_tabel.values()
              if inskrywing_VALUE['종류']==501 and inskrywing_VALUE['Naam'] in naam_tabel and inskrywing_VALUE['Naam'] not in SD}
    for Pad in sorted({Path(inskrywing_VALUE['Lêer']) for inskrywing_VALUE in verklaring_tabel.values()}):
        lyn_Lys = Pad.read_text().splitlines(True); 이어짐 = False
        for INDEX,lyn in enumerate(lyn_Lys):
            전처리 = 이어짐 or bool(re.match(r'\s*#',lyn))
            이어짐 = 전처리 and lyn.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabel = naam_tabel if re.match(r'\s*#\s*define\b',lyn) or 이어짐 else makro_VALUE
                lyn_Lys[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabel.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],lyn)
        Pad.write_text(''.join(lyn_Lys))
    # 각 자체 Vertaal_bron 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Pad in sorted({Path(inskrywing_VALUE['Lêer']) for inskrywing_VALUE in verklaring_tabel.values()}):
        if Pad.suffix not in ('.c','.cpp'):continue
        portuur_VALUE = '../' * len(Pad.relative_to(Project_wortel).parts[:-1]) + '명명/기계연결이름.h'
        Pad.write_text('#include "'+portuur_VALUE+'"\n'+Pad.read_text())
    (Project_wortel/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_ry)+'\n')
    (Project_wortel/'build/한국어화/전처리참조.json').write_text(json.dumps(ignoreer_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('verander_VALUE',len(LOG_ry)-1,'전처리 재검토',len(ignoreer_VALUE),'masjien Koppel',len(verbinding_tabel))

if __name__=='__main__': uitvoer_bevel()
