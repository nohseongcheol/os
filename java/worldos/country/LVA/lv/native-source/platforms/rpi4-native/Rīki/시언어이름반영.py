#!/usr/bin/env python3
"""deklarācija 고유번호와 UTF-8 byte_VALUE 위치로 savs C 이름을 옮기는 일회성 이행 Rīki.

ārējs_VALUE 구조체의 멤버, virkne_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 mainīt_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_sakne = Path(__file__).resolve().parents[1]

def Izpildīt_komanda():
    analīze_VALUE = json.loads((Project_sakne/'build/한국어화/시언어분석.json').read_text())
    if analīze_VALUE['Kļūda']: raise SystemExit('analīze_VALUE 오류를 먼저 해결해야 합니다.')
    nosaukums_tabula = json.loads((Project_sakne/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_sakne/'명명/규격이름.json').read_text()))
    deklarācija_tabula = analīze_VALUE['deklarācija']
    바꿀선언 = {UNIQUE_VALUE:nosaukums_tabula[ievade_VALUE['Nosaukums']] for UNIQUE_VALUE,ievade_VALUE in deklarācija_tabula.items()
                if ievade_VALUE['Nosaukums'] in nosaukums_tabula and ievade_VALUE['Nosaukums'] not in SD}
    paziņa_tabula = {ievade_VALUE['Nosaukums']:nosaukums_tabula[ievade_VALUE['Nosaukums']] for ievade_VALUE in deklarācija_tabula.values()
              if ievade_VALUE.get('Savienoties')==4 and ievade_VALUE['종류'] in (8,9)
              and ievade_VALUE['Nosaukums'] in nosaukums_tabula and ievade_VALUE['Nosaukums'] not in SD}
    # ģenerēt AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Savienoties 이름만 유지한다.
    머리 = ['/* Latviešu avots_koks 이름과 기존 mašīna Savienoties līguma_vērtība. 자동 ģenerēt: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(paziņa_tabula.items())]
    머리 += ['#endif','']
    (Project_sakne/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Izmaiņas_Saraksts = defaultdict(dict)
    for Fails,Nobīde_VALUE,Nosaukums,UNIQUE_VALUE in analīze_VALUE['Uzziņas']:
        if UNIQUE_VALUE in 바꿀선언:
            Izmaiņas_Saraksts[Fails][Nobīde_VALUE] = (Nosaukums,바꿀선언[UNIQUE_VALUE])
    LOG_RECORD = ['Fails\t원래바이트위치\t이전이름\t한국어이름']
    ignorēt_VALUE = []
    for Fails,mainīt_VALUE in Izmaiņas_Saraksts.items():
        CEĻŠ = Path(Fails); 원본 = CEĻŠ.read_bytes(); dati = 원본
        for Nobīde_VALUE,(옛이름,새이름) in sorted(mainīt_VALUE.items(),reverse=True):
            끝 = Nobīde_VALUE+len(옛이름.encode())
            if 원본[Nobīde_VALUE:끝] != 옛이름.encode():
                ignorēt_VALUE.append((str(CEĻŠ.relative_to(Project_sakne)),Nobīde_VALUE,옛이름));continue
            dati = dati[:Nobīde_VALUE]+새이름.encode()+dati[끝:]
            LOG_RECORD.append('{}\t{}\t{}\t{}'.format(CEĻŠ.relative_to(Project_sakne),Nobīde_VALUE,옛이름,새이름))
        CEĻŠ.write_bytes(dati)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {ievade_VALUE['Nosaukums']:nosaukums_tabula[ievade_VALUE['Nosaukums']] for ievade_VALUE in deklarācija_tabula.values()
              if ievade_VALUE['종류']==501 and ievade_VALUE['Nosaukums'] in nosaukums_tabula and ievade_VALUE['Nosaukums'] not in SD}
    for CEĻŠ in sorted({Path(ievade_VALUE['Fails']) for ievade_VALUE in deklarācija_tabula.values()}):
        līnija_Saraksts = CEĻŠ.read_text().splitlines(True); 이어짐 = False
        for INDEX,Līniju in enumerate(līnija_Saraksts):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Līniju))
            이어짐 = 전처리 and Līniju.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabula = nosaukums_tabula if re.match(r'\s*#\s*define\b',Līniju) or 이어짐 else makro_VALUE
                līnija_Saraksts[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabula.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Līniju)
        CEĻŠ.write_text(''.join(līnija_Saraksts))
    # 각 savs translēt_avots 단위에만 연결표를 넣는다. ārējs_VALUE 배포본에는 전파하지 않는다.
    for CEĻŠ in sorted({Path(ievade_VALUE['Fails']) for ievade_VALUE in deklarācija_tabula.values()}):
        if CEĻŠ.suffix not in ('.c','.cpp'):continue
        vienranga_VALUE = '../' * len(CEĻŠ.relative_to(Project_sakne).parts[:-1]) + '명명/기계연결이름.h'
        CEĻŠ.write_text('#include "'+vienranga_VALUE+'"\n'+CEĻŠ.read_text())
    (Project_sakne/'명명/C_nosaukums_kartēšana.tsv').write_text('\n'.join(LOG_RECORD)+'\n')
    (Project_sakne/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorēt_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('mainīt_VALUE',len(LOG_RECORD)-1,'전처리 재검토',len(ignorēt_VALUE),'mašīna Savienoties',len(paziņa_tabula))

if __name__=='__main__': Izpildīt_komanda()
