#!/usr/bin/env python3
"""aangifte 고유번호와 UTF-8 byte_WAARDE 위치로 Eigen C 이름을 옮기는 일회성 이행 hulpmiddelen.

extern_WAARDE 구조체의 멤버, tekenreeks_WAARDE, C 표준 FUNCTIE_WAARDE, 이식 규약은 보존한다.
입력은 wijzigen_WAARDE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Taken_wortel = Path(__file__).resolve().parents[1]

def Uitvoeren_opdracht():
    Analyseren_WAARDE = json.loads((Taken_wortel/'build/한국어화/시언어분석.json').read_text())
    if Analyseren_WAARDE['fout']: raise SystemExit('Analyseren_WAARDE 오류를 먼저 해결해야 합니다.')
    naam_tabel = json.loads((Taken_wortel/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Taken_wortel/'명명/규격이름.json').read_text()))
    aangifte_tabel = Analyseren_WAARDE['aangifte']
    바꿀선언 = {UNIEK_WAARDE:naam_tabel[invoer_WAARDE_962f286b['Naam']] for UNIEK_WAARDE,invoer_WAARDE_962f286b in aangifte_tabel.items()
                if invoer_WAARDE_962f286b['Naam'] in naam_tabel and invoer_WAARDE_962f286b['Naam'] not in SD}
    verbinding_tabel = {invoer_WAARDE_962f286b['Naam']:naam_tabel[invoer_WAARDE_962f286b['Naam']] for invoer_WAARDE_962f286b in aangifte_tabel.values()
              if invoer_WAARDE_962f286b.get('Verbinden')==4 and invoer_WAARDE_962f286b['soort_WAARDE'] in (8,9)
              and invoer_WAARDE_962f286b['Naam'] in naam_tabel and invoer_WAARDE_962f286b['Naam'] not in SD}
    # genereren AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Verbinden 이름만 유지한다.
    kop_WAARDE = ['/* Nederlands bron_structuur 이름과 기존 machine Verbinden contractwaarde. 자동 genereren: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    kop_WAARDE += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(verbinding_tabel.items())]
    kop_WAARDE += ['#endif','']
    (Taken_wortel/'명명/기계연결이름.h').write_text('\n'.join(kop_WAARDE))
    Wijzigingen_Lijst = defaultdict(dict)
    for bestand,VERSCHUIVING_WAARDE,Naam,UNIEK_WAARDE in Analyseren_WAARDE['verwijzen']:
        if UNIEK_WAARDE in 바꿀선언:
            Wijzigingen_Lijst[bestand][VERSCHUIVING_WAARDE] = (Naam,바꿀선언[UNIEK_WAARDE])
    LOG_RECORD = ['bestand\t원래바이트위치\t이전이름\t한국어이름']
    negeren_WAARDE = []
    for bestand,wijzigen_WAARDE in Wijzigingen_Lijst.items():
        pad = Path(bestand); 원본 = pad.read_bytes(); gegevens = 원본
        for VERSCHUIVING_WAARDE,(옛이름,새이름) in sorted(wijzigen_WAARDE.items(),reverse=True):
            끝 = VERSCHUIVING_WAARDE+len(옛이름.encode())
            if 원본[VERSCHUIVING_WAARDE:끝] != 옛이름.encode():
                negeren_WAARDE.append((str(pad.relative_to(Taken_wortel)),VERSCHUIVING_WAARDE,옛이름));continue
            gegevens = gegevens[:VERSCHUIVING_WAARDE]+새이름.encode()+gegevens[끝:]
            LOG_RECORD.append('{}\t{}\t{}\t{}'.format(pad.relative_to(Taken_wortel),VERSCHUIVING_WAARDE,옛이름,새이름))
        pad.write_bytes(gegevens)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macro_WAARDE = {invoer_WAARDE_962f286b['Naam']:naam_tabel[invoer_WAARDE_962f286b['Naam']] for invoer_WAARDE_962f286b in aangifte_tabel.values()
              if invoer_WAARDE_962f286b['soort_WAARDE']==501 and invoer_WAARDE_962f286b['Naam'] in naam_tabel and invoer_WAARDE_962f286b['Naam'] not in SD}
    for pad in sorted({Path(invoer_WAARDE_962f286b['bestand']) for invoer_WAARDE_962f286b in aangifte_tabel.values()}):
        lijn_Lijst = pad.read_text().splitlines(True); 이어짐 = False
        for INDEX,invoerregel in enumerate(lijn_Lijst):
            전처리 = 이어짐 or bool(re.match(r'\s*#',invoerregel))
            이어짐 = 전처리 and invoerregel.rstrip().endswith('\\')
            if 전처리:
                opzoektabel = naam_tabel if re.match(r'\s*#\s*define\b',invoerregel) or 이어짐 else macro_WAARDE
                lijn_Lijst[INDEX] = 낱말.sub(lambda 맞음: opzoektabel.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],invoerregel)
        pad.write_text(''.join(lijn_Lijst))
    # 각 Eigen VERTALEN_bron 단위에만 연결표를 넣는다. extern_WAARDE 배포본에는 전파하지 않는다.
    for pad in sorted({Path(invoer_WAARDE_962f286b['bestand']) for invoer_WAARDE_962f286b in aangifte_tabel.values()}):
        if pad.suffix not in ('.c','.cpp'):continue
        peer_WAARDE = '../' * len(pad.relative_to(Taken_wortel).parts[:-1]) + '명명/기계연결이름.h'
        pad.write_text('#include "'+peer_WAARDE+'"\n'+pad.read_text())
    (Taken_wortel/'명명/C_naam_toewijzing.tsv').write_text('\n'.join(LOG_RECORD)+'\n')
    (Taken_wortel/'build/한국어화/전처리참조.json').write_text(json.dumps(negeren_WAARDE,ensure_ascii=False,indent=2)+'\n')
    print('wijzigen_WAARDE',len(LOG_RECORD)-1,'전처리 재검토',len(negeren_WAARDE),'machine Verbinden',len(verbinding_tabel))

if __name__=='__main__': Uitvoeren_opdracht()
