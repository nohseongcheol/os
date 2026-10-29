#!/usr/bin/env python3
"""deklaratsioon 고유번호와 UTF-8 bait_VALUE 위치로 oma C 이름을 옮기는 일회성 이행 Tööriistad.

väline_VALUE 구조체의 멤버, string_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 muutma_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_juur = Path(__file__).resolve().parents[1]

def Täida_käsk():
    Analüüs_VALUE = json.loads((Project_juur/'build/한국어화/시언어분석.json').read_text())
    if Analüüs_VALUE['VIGA']: raise SystemExit('Analüüs_VALUE 오류를 먼저 해결해야 합니다.')
    nimetus_tabel = json.loads((Project_juur/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_juur/'명명/규격이름.json').read_text()))
    deklaratsioon_tabel = Analüüs_VALUE['deklaratsioon']
    바꿀선언 = {UNIQUE_VALUE:nimetus_tabel[kirje_VALUE['Nimi_2']] for UNIQUE_VALUE,kirje_VALUE in deklaratsioon_tabel.items()
                if kirje_VALUE['Nimi_2'] in nimetus_tabel and kirje_VALUE['Nimi_2'] not in SD}
    ühendus_tabel = {kirje_VALUE['Nimi_2']:nimetus_tabel[kirje_VALUE['Nimi_2']] for kirje_VALUE in deklaratsioon_tabel.values()
              if kirje_VALUE.get('Ühendu')==4 and kirje_VALUE['종류'] in (8,9)
              and kirje_VALUE['Nimi_2'] in nimetus_tabel and kirje_VALUE['Nimi_2'] not in SD}
    # genereerima AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Ühendu 이름만 유지한다.
    머리 = ['/* Eesti lähe_puu 이름과 기존 arvuti Ühendu lepingu_väärtus. 자동 genereerima: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(ühendus_tabel.items())]
    머리 += ['#endif','']
    (Project_juur/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Muudatused_Loend = defaultdict(dict)
    for Fail,nihe_VALUE,Nimi_2,UNIQUE_VALUE in Analüüs_VALUE['viide']:
        if UNIQUE_VALUE in 바꿀선언:
            Muudatused_Loend[Fail][nihe_VALUE] = (Nimi_2,바꿀선언[UNIQUE_VALUE])
    LOG_kirje = ['Fail\t원래바이트위치\t이전이름\t한국어이름']
    eirama_VALUE = []
    for Fail,muutma_VALUE in Muudatused_Loend.items():
        RADA = Path(Fail); 원본 = RADA.read_bytes(); andmed = 원본
        for nihe_VALUE,(옛이름,새이름) in sorted(muutma_VALUE.items(),reverse=True):
            끝 = nihe_VALUE+len(옛이름.encode())
            if 원본[nihe_VALUE:끝] != 옛이름.encode():
                eirama_VALUE.append((str(RADA.relative_to(Project_juur)),nihe_VALUE,옛이름));continue
            andmed = andmed[:nihe_VALUE]+새이름.encode()+andmed[끝:]
            LOG_kirje.append('{}\t{}\t{}\t{}'.format(RADA.relative_to(Project_juur),nihe_VALUE,옛이름,새이름))
        RADA.write_bytes(andmed)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {kirje_VALUE['Nimi_2']:nimetus_tabel[kirje_VALUE['Nimi_2']] for kirje_VALUE in deklaratsioon_tabel.values()
              if kirje_VALUE['종류']==501 and kirje_VALUE['Nimi_2'] in nimetus_tabel and kirje_VALUE['Nimi_2'] not in SD}
    for RADA in sorted({Path(kirje_VALUE['Fail']) for kirje_VALUE in deklaratsioon_tabel.values()}):
        liin_Loend = RADA.read_text().splitlines(True); 이어짐 = False
        for INDEX,Joon in enumerate(liin_Loend):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Joon))
            이어짐 = 전처리 and Joon.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabel = nimetus_tabel if re.match(r'\s*#\s*define\b',Joon) or 이어짐 else makro_VALUE
                liin_Loend[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabel.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Joon)
        RADA.write_text(''.join(liin_Loend))
    # 각 oma Tõlgi_lähe 단위에만 연결표를 넣는다. väline_VALUE 배포본에는 전파하지 않는다.
    for RADA in sorted({Path(kirje_VALUE['Fail']) for kirje_VALUE in deklaratsioon_tabel.values()}):
        if RADA.suffix not in ('.c','.cpp'):continue
        partner_VALUE = '../' * len(RADA.relative_to(Project_juur).parts[:-1]) + '명명/기계연결이름.h'
        RADA.write_text('#include "'+partner_VALUE+'"\n'+RADA.read_text())
    (Project_juur/'명명/_15_nimetus_vastendamine.tsv').write_text('\n'.join(LOG_kirje)+'\n')
    (Project_juur/'build/한국어화/전처리참조.json').write_text(json.dumps(eirama_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('muutma_VALUE',len(LOG_kirje)-1,'전처리 재검토',len(eirama_VALUE),'arvuti Ühendu',len(ühendus_tabel))

if __name__=='__main__': Täida_käsk()
