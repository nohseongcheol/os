#!/usr/bin/env python3
"""deklaration 고유번호와 UTF-8 byte_värde 위치로 eget C 이름을 옮기는 일회성 이행 verktyg.

extern_värde 구조체의 멤버, sträng_värde, C 표준 FUNKTION_värde, 이식 규약은 보존한다.
입력은 ändra_värde 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

åtgärd_rot = Path(__file__).resolve().parents[1]

def köra_kommando():
    Analysera_värde = json.loads((åtgärd_rot/'build/한국어화/시언어분석.json').read_text())
    if Analysera_värde['fel']: raise SystemExit('Analysera_värde 오류를 먼저 해결해야 합니다.')
    namn_tabell = json.loads((åtgärd_rot/'명명/시언어이름.json').read_text())
    SD = set(json.loads((åtgärd_rot/'명명/규격이름.json').read_text()))
    deklaration_tabell = Analysera_värde['deklaration']
    바꿀선언 = {UNIK_värde:namn_tabell[post_värde['Namn']] for UNIK_värde,post_värde in deklaration_tabell.items()
                if post_värde['Namn'] in namn_tabell and post_värde['Namn'] not in SD}
    kontakt_tabell = {post_värde['Namn']:namn_tabell[post_värde['Namn']] for post_värde in deklaration_tabell.values()
              if post_värde.get('Anslut')==4 and post_värde['variant_värde'] in (8,9)
              and post_värde['Namn'] in namn_tabell and post_värde['Namn'] not in SD}
    # generera AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Anslut 이름만 유지한다.
    머리 = ['/* Svenska källa_träd 이름과 기존 dator Anslut kontraktsvärde. 자동 generera: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(kontakt_tabell.items())]
    머리 += ['#endif','']
    (åtgärd_rot/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Ändringar_ange = defaultdict(dict)
    for filnamn,FÖRSKJUTNING_värde,Namn,UNIK_värde in Analysera_värde['referens']:
        if UNIK_värde in 바꿀선언:
            Ändringar_ange[filnamn][FÖRSKJUTNING_värde] = (Namn,바꿀선언[UNIK_värde])
    LOG_POST = ['filnamn\t원래바이트위치\t이전이름\t한국어이름']
    ignorera_värde = []
    for filnamn,ändra_värde in Ändringar_ange.items():
        sökväg_2 = Path(filnamn); 원본 = sökväg_2.read_bytes(); data = 원본
        for FÖRSKJUTNING_värde,(옛이름,새이름) in sorted(ändra_värde.items(),reverse=True):
            끝 = FÖRSKJUTNING_värde+len(옛이름.encode())
            if 원본[FÖRSKJUTNING_värde:끝] != 옛이름.encode():
                ignorera_värde.append((str(sökväg_2.relative_to(åtgärd_rot)),FÖRSKJUTNING_värde,옛이름));continue
            data = data[:FÖRSKJUTNING_värde]+새이름.encode()+data[끝:]
            LOG_POST.append('{}\t{}\t{}\t{}'.format(sökväg_2.relative_to(åtgärd_rot),FÖRSKJUTNING_värde,옛이름,새이름))
        sökväg_2.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_värde = {post_värde['Namn']:namn_tabell[post_värde['Namn']] for post_värde in deklaration_tabell.values()
              if post_värde['variant_värde']==501 and post_värde['Namn'] in namn_tabell and post_värde['Namn'] not in SD}
    for sökväg_2 in sorted({Path(post_värde['filnamn']) for post_värde in deklaration_tabell.values()}):
        rad_ange = sökväg_2.read_text().splitlines(True); 이어짐 = False
        for INDEX,inmatningsrad in enumerate(rad_ange):
            전처리 = 이어짐 or bool(re.match(r'\s*#',inmatningsrad))
            이어짐 = 전처리 and inmatningsrad.rstrip().endswith('\\')
            if 전처리:
                LETAUPP_tabell = namn_tabell if re.match(r'\s*#\s*define\b',inmatningsrad) or 이어짐 else makro_värde
                rad_ange[INDEX] = 낱말.sub(lambda 맞음: LETAUPP_tabell.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],inmatningsrad)
        sökväg_2.write_text(''.join(rad_ange))
    # 각 eget ÖVERSÄTT_källa 단위에만 연결표를 넣는다. extern_värde 배포본에는 전파하지 않는다.
    for sökväg_2 in sorted({Path(post_värde['filnamn']) for post_värde in deklaration_tabell.values()}):
        if sökväg_2.suffix not in ('.c','.cpp'):continue
        peer_värde = '../' * len(sökväg_2.relative_to(åtgärd_rot).parts[:-1]) + '명명/기계연결이름.h'
        sökväg_2.write_text('#include "'+peer_värde+'"\n'+sökväg_2.read_text())
    (åtgärd_rot/'명명/C_namn_mappning.tsv').write_text('\n'.join(LOG_POST)+'\n')
    (åtgärd_rot/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorera_värde,ensure_ascii=False,indent=2)+'\n')
    print('ändra_värde',len(LOG_POST)-1,'전처리 재검토',len(ignorera_värde),'dator Anslut',len(kontakt_tabell))

if __name__=='__main__': köra_kommando()
