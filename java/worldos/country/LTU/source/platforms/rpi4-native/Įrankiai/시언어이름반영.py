#!/usr/bin/env python3
"""deklaracija 고유번호와 UTF-8 baitas_VALUE 위치로 savas C 이름을 옮기는 일회성 이행 Įrankiai.

išorinis_VALUE 구조체의 멤버, eilutė_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 keisti_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_šaknis = Path(__file__).resolve().parents[1]

def Vykdyti_komanda():
    Analizė_VALUE = json.loads((Project_šaknis/'build/한국어화/시언어분석.json').read_text())
    if Analizė_VALUE['KLAIDA']: raise SystemExit('Analizė_VALUE 오류를 먼저 해결해야 합니다.')
    pavadinimas_lentelė = json.loads((Project_šaknis/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_šaknis/'명명/규격이름.json').read_text()))
    deklaracija_lentelė = Analizė_VALUE['deklaracija']
    바꿀선언 = {UNIQUE_VALUE:pavadinimas_lentelė[įrašas_VALUE['Pavadinimas_2']] for UNIQUE_VALUE,įrašas_VALUE in deklaracija_lentelė.items()
                if įrašas_VALUE['Pavadinimas_2'] in pavadinimas_lentelė and įrašas_VALUE['Pavadinimas_2'] not in SD}
    ryšys_lentelė = {įrašas_VALUE['Pavadinimas_2']:pavadinimas_lentelė[įrašas_VALUE['Pavadinimas_2']] for įrašas_VALUE in deklaracija_lentelė.values()
              if įrašas_VALUE.get('Prisijungti')==4 and įrašas_VALUE['종류'] in (8,9)
              and įrašas_VALUE['Pavadinimas_2'] in pavadinimas_lentelė and įrašas_VALUE['Pavadinimas_2'] not in SD}
    # generuoti AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Prisijungti 이름만 유지한다.
    머리 = ['/* Lietuvių šaltinis_medis 이름과 기존 mašina Prisijungti sutarties_vertė. 자동 generuoti: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(ryšys_lentelė.items())]
    머리 += ['#endif','']
    (Project_šaknis/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Keitimai_Sąrašas = defaultdict(dict)
    for Failas,OFFSET_VALUE,Pavadinimas_2,UNIQUE_VALUE in Analizė_VALUE['nuoroda']:
        if UNIQUE_VALUE in 바꿀선언:
            Keitimai_Sąrašas[Failas][OFFSET_VALUE] = (Pavadinimas_2,바꿀선언[UNIQUE_VALUE])
    LOG_RECORD = ['Failas\t원래바이트위치\t이전이름\t한국어이름']
    nepaisyti_VALUE = []
    for Failas,keisti_VALUE in Keitimai_Sąrašas.items():
        KELIAS = Path(Failas); 원본 = KELIAS.read_bytes(); duomenys = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(keisti_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                nepaisyti_VALUE.append((str(KELIAS.relative_to(Project_šaknis)),OFFSET_VALUE,옛이름));continue
            duomenys = duomenys[:OFFSET_VALUE]+새이름.encode()+duomenys[끝:]
            LOG_RECORD.append('{}\t{}\t{}\t{}'.format(KELIAS.relative_to(Project_šaknis),OFFSET_VALUE,옛이름,새이름))
        KELIAS.write_bytes(duomenys)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makrokomanda_VALUE = {įrašas_VALUE['Pavadinimas_2']:pavadinimas_lentelė[įrašas_VALUE['Pavadinimas_2']] for įrašas_VALUE in deklaracija_lentelė.values()
              if įrašas_VALUE['종류']==501 and įrašas_VALUE['Pavadinimas_2'] in pavadinimas_lentelė and įrašas_VALUE['Pavadinimas_2'] not in SD}
    for KELIAS in sorted({Path(įrašas_VALUE['Failas']) for įrašas_VALUE in deklaracija_lentelė.values()}):
        eilutė_Sąrašas = KELIAS.read_text().splitlines(True); 이어짐 = False
        for INDEX,Eilutė in enumerate(eilutė_Sąrašas):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Eilutė))
            이어짐 = 전처리 and Eilutė.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_lentelė = pavadinimas_lentelė if re.match(r'\s*#\s*define\b',Eilutė) or 이어짐 else makrokomanda_VALUE
                eilutė_Sąrašas[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_lentelė.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Eilutė)
        KELIAS.write_text(''.join(eilutė_Sąrašas))
    # 각 savas Versti_šaltinis 단위에만 연결표를 넣는다. išorinis_VALUE 배포본에는 전파하지 않는다.
    for KELIAS in sorted({Path(įrašas_VALUE['Failas']) for įrašas_VALUE in deklaracija_lentelė.values()}):
        if KELIAS.suffix not in ('.c','.cpp'):continue
        lygiavertis_mazgas_VALUE = '../' * len(KELIAS.relative_to(Project_šaknis).parts[:-1]) + '명명/기계연결이름.h'
        KELIAS.write_text('#include "'+lygiavertis_mazgas_VALUE+'"\n'+KELIAS.read_text())
    (Project_šaknis/'명명/C_pavadinimas_susiejimas.tsv').write_text('\n'.join(LOG_RECORD)+'\n')
    (Project_šaknis/'build/한국어화/전처리참조.json').write_text(json.dumps(nepaisyti_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('keisti_VALUE',len(LOG_RECORD)-1,'전처리 재검토',len(nepaisyti_VALUE),'mašina Prisijungti',len(ryšys_lentelė))

if __name__=='__main__': Vykdyti_komanda()
