#!/usr/bin/env python3
"""erklæring 고유번호와 UTF-8 byte_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Verktøy.

ekstern_VALUE 구조체의 멤버, streng_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 endre_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

spegle_rot = Path(__file__).resolve().parents[1]

def Utfør_kommando():
    분석 = json.loads((spegle_rot/'build/한국어화/시언어분석.json').read_text())
    if 분석['FEIL']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    namn_tabell = json.loads((spegle_rot/'명명/시언어이름.json').read_text())
    SD = set(json.loads((spegle_rot/'명명/규격이름.json').read_text()))
    erklæring_tabell = 분석['erklæring']
    바꿀선언 = {UNIQUE_VALUE:namn_tabell[oppføring_VALUE['Namn']] for UNIQUE_VALUE,oppføring_VALUE in erklæring_tabell.items()
                if oppføring_VALUE['Namn'] in namn_tabell and oppføring_VALUE['Namn'] not in SD}
    kontakt_tabell = {oppføring_VALUE['Namn']:namn_tabell[oppføring_VALUE['Namn']] for oppføring_VALUE in erklæring_tabell.values()
              if oppføring_VALUE.get('Kopla_til')==4 and oppføring_VALUE['종류'] in (8,9)
              and oppføring_VALUE['Namn'] in namn_tabell and oppføring_VALUE['Namn'] not in SD}
    # generere AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Kopla_til 이름만 유지한다.
    머리 = ['/* 한국어 kjelde_tre 이름과 기존 maskin Kopla_til sak_VALUE. 자동 generere: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(kontakt_tabell.items())]
    머리 += ['#endif','']
    (spegle_rot/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Endringar_Liste = defaultdict(dict)
    for Fil,OFFSET_VALUE,Namn,UNIQUE_VALUE in 분석['Oppslagsverk']:
        if UNIQUE_VALUE in 바꿀선언:
            Endringar_Liste[Fil][OFFSET_VALUE] = (Namn,바꿀선언[UNIQUE_VALUE])
    LOG_rad = ['Fil\t원래바이트위치\t이전이름\t한국어이름']
    ignorere_VALUE = []
    for Fil,endre_VALUE in Endringar_Liste.items():
        STIGE = Path(Fil); 원본 = STIGE.read_bytes(); data = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(endre_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                ignorere_VALUE.append((str(STIGE.relative_to(spegle_rot)),OFFSET_VALUE,옛이름));continue
            data = data[:OFFSET_VALUE]+새이름.encode()+data[끝:]
            LOG_rad.append('{}\t{}\t{}\t{}'.format(STIGE.relative_to(spegle_rot),OFFSET_VALUE,옛이름,새이름))
        STIGE.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {oppføring_VALUE['Namn']:namn_tabell[oppføring_VALUE['Namn']] for oppføring_VALUE in erklæring_tabell.values()
              if oppføring_VALUE['종류']==501 and oppføring_VALUE['Namn'] in namn_tabell and oppføring_VALUE['Namn'] not in SD}
    for STIGE in sorted({Path(oppføring_VALUE['Fil']) for oppføring_VALUE in erklæring_tabell.values()}):
        line_Liste = STIGE.read_text().splitlines(True); 이어짐 = False
        for INDEX,linje in enumerate(line_Liste):
            전처리 = 이어짐 or bool(re.match(r'\s*#',linje))
            이어짐 = 전처리 and linje.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabell = namn_tabell if re.match(r'\s*#\s*define\b',linje) or 이어짐 else makro_VALUE
                line_Liste[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabell.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],linje)
        STIGE.write_text(''.join(line_Liste))
    # 각 자체 TRANSLATE_kjelde 단위에만 연결표를 넣는다. ekstern_VALUE 배포본에는 전파하지 않는다.
    for STIGE in sorted({Path(oppføring_VALUE['Fil']) for oppføring_VALUE in erklæring_tabell.values()}):
        if STIGE.suffix not in ('.c','.cpp'):continue
        node_VALUE_6a3b6fa7 = '../' * len(STIGE.relative_to(spegle_rot).parts[:-1]) + '명명/기계연결이름.h'
        STIGE.write_text('#include "'+node_VALUE_6a3b6fa7+'"\n'+STIGE.read_text())
    (spegle_rot/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_rad)+'\n')
    (spegle_rot/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorere_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('endre_VALUE',len(LOG_rad)-1,'전처리 재검토',len(ignorere_VALUE),'maskin Kopla_til',len(kontakt_tabell))

if __name__=='__main__': Utfør_kommando()
