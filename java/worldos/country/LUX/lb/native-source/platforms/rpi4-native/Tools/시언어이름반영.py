#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 Byte_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Tools.

외부 구조체의 멤버, Zeechefolleg_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 änneren_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

projezéieren_Racinn = Path(__file__).resolve().parents[1]

def ausféieren_Befeel():
    분석 = json.loads((projezéieren_Racinn/'build/한국어화/시언어분석.json').read_text())
    if 분석['Feeler']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    Numm_Tabell = json.loads((projezéieren_Racinn/'명명/시언어이름.json').read_text())
    SD = set(json.loads((projezéieren_Racinn/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_VALUE:Numm_Tabell[Agab_VALUE['Numm']] for UNIQUE_VALUE,Agab_VALUE in 선언표.items()
                if Agab_VALUE['Numm'] in Numm_Tabell and Agab_VALUE['Numm'] not in SD}
    Verbindung_Tabell = {Agab_VALUE['Numm']:Numm_Tabell[Agab_VALUE['Numm']] for Agab_VALUE in 선언표.values()
              if Agab_VALUE.get('Verbannen')==4 and Agab_VALUE['종류'] in (8,9)
              and Agab_VALUE['Numm'] in Numm_Tabell and Agab_VALUE['Numm'] not in SD}
    # generéieren AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Verbannen 이름만 유지한다.
    머리 = ['/* 한국어 Quell_Bamstruktur 이름과 기존 Computer Verbannen Job_VALUE. 자동 generéieren: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(Verbindung_Tabell.items())]
    머리 += ['#endif','']
    (projezéieren_Racinn/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Ännerungen_Lëscht = defaultdict(dict)
    for Fichier,OFFSET_VALUE,Numm,UNIQUE_VALUE in 분석['Referenzen']:
        if UNIQUE_VALUE in 바꿀선언:
            Ännerungen_Lëscht[Fichier][OFFSET_VALUE] = (Numm,바꿀선언[UNIQUE_VALUE])
    LOG_Rei = ['Fichier\t원래바이트위치\t이전이름\t한국어이름']
    ignoréieren_VALUE = []
    for Fichier,änneren_VALUE in Ännerungen_Lëscht.items():
        Wee = Path(Fichier); 원본 = Wee.read_bytes(); Daten = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(änneren_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                ignoréieren_VALUE.append((str(Wee.relative_to(projezéieren_Racinn)),OFFSET_VALUE,옛이름));continue
            Daten = Daten[:OFFSET_VALUE]+새이름.encode()+Daten[끝:]
            LOG_Rei.append('{}\t{}\t{}\t{}'.format(Wee.relative_to(projezéieren_Racinn),OFFSET_VALUE,옛이름,새이름))
        Wee.write_bytes(Daten)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    Makro_VALUE = {Agab_VALUE['Numm']:Numm_Tabell[Agab_VALUE['Numm']] for Agab_VALUE in 선언표.values()
              if Agab_VALUE['종류']==501 and Agab_VALUE['Numm'] in Numm_Tabell and Agab_VALUE['Numm'] not in SD}
    for Wee in sorted({Path(Agab_VALUE['Fichier']) for Agab_VALUE in 선언표.values()}):
        Zeil_Lëscht = Wee.read_text().splitlines(True); 이어짐 = False
        for INDEX,Zeil in enumerate(Zeil_Lëscht):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Zeil))
            이어짐 = 전처리 and Zeil.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_Tabell = Numm_Tabell if re.match(r'\s*#\s*define\b',Zeil) or 이어짐 else Makro_VALUE
                Zeil_Lëscht[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_Tabell.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Zeil)
        Wee.write_text(''.join(Zeil_Lëscht))
    # 각 자체 TRANSLATE_Quell 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Wee in sorted({Path(Agab_VALUE['Fichier']) for Agab_VALUE in 선언표.values()}):
        if Wee.suffix not in ('.c','.cpp'):continue
        Peer_VALUE = '../' * len(Wee.relative_to(projezéieren_Racinn).parts[:-1]) + '명명/기계연결이름.h'
        Wee.write_text('#include "'+Peer_VALUE+'"\n'+Wee.read_text())
    (projezéieren_Racinn/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_Rei)+'\n')
    (projezéieren_Racinn/'build/한국어화/전처리참조.json').write_text(json.dumps(ignoréieren_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('änneren_VALUE',len(LOG_Rei)-1,'전처리 재검토',len(ignoréieren_VALUE),'Computer Verbannen',len(Verbindung_Tabell))

if __name__=='__main__': ausféieren_Befeel()
