#!/usr/bin/env python3
"""erklæring 고유번호와 UTF-8 byte_VERDI 위치로 eget C 이름을 옮기는 일회성 이행 Verktøy.

ekstern_VERDI 구조체의 멤버, streng_VERDI, C 표준 FUNKSJON_VERDI, 이식 규약은 보존한다.
입력은 endre_VERDI 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

speile_rot = Path(__file__).resolve().parents[1]

def Utfør_kommando():
    Analyser_VERDI = json.loads((speile_rot/'build/한국어화/시언어분석.json').read_text())
    if Analyser_VERDI['feil']: raise SystemExit('Analyser_VERDI 오류를 먼저 해결해야 합니다.')
    navn_tabell = json.loads((speile_rot/'명명/시언어이름.json').read_text())
    SD = set(json.loads((speile_rot/'명명/규격이름.json').read_text()))
    erklæring_tabell = Analyser_VERDI['erklæring']
    바꿀선언 = {UNIK_VERDI:navn_tabell[oppføring_VERDI['Navn']] for UNIK_VERDI,oppføring_VERDI in erklæring_tabell.items()
                if oppføring_VERDI['Navn'] in navn_tabell and oppføring_VERDI['Navn'] not in SD}
    kontakt_tabell = {oppføring_VERDI['Navn']:navn_tabell[oppføring_VERDI['Navn']] for oppføring_VERDI in erklæring_tabell.values()
              if oppføring_VERDI.get('Koble_til')==4 and oppføring_VERDI['종류'] in (8,9)
              and oppføring_VERDI['Navn'] in navn_tabell and oppføring_VERDI['Navn'] not in SD}
    # generere AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Koble_til 이름만 유지한다.
    머리 = ['/* norsk kilde_tre 이름과 기존 maskin Koble_til kontraktverdi. 자동 generere: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(kontakt_tabell.items())]
    머리 += ['#endif','']
    (speile_rot/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Endringer_Liste = defaultdict(dict)
    for Fil,FORSKYVNING_VERDI,Navn,UNIK_VERDI in Analyser_VERDI['referere']:
        if UNIK_VERDI in 바꿀선언:
            Endringer_Liste[Fil][FORSKYVNING_VERDI] = (Navn,바꿀선언[UNIK_VERDI])
    LOG_POST = ['Fil\t원래바이트위치\t이전이름\t한국어이름']
    avvis_VERDI = []
    for Fil,endre_VERDI in Endringer_Liste.items():
        Sti = Path(Fil); 원본 = Sti.read_bytes(); data = 원본
        for FORSKYVNING_VERDI,(옛이름,새이름) in sorted(endre_VERDI.items(),reverse=True):
            끝 = FORSKYVNING_VERDI+len(옛이름.encode())
            if 원본[FORSKYVNING_VERDI:끝] != 옛이름.encode():
                avvis_VERDI.append((str(Sti.relative_to(speile_rot)),FORSKYVNING_VERDI,옛이름));continue
            data = data[:FORSKYVNING_VERDI]+새이름.encode()+data[끝:]
            LOG_POST.append('{}\t{}\t{}\t{}'.format(Sti.relative_to(speile_rot),FORSKYVNING_VERDI,옛이름,새이름))
        Sti.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VERDI = {oppføring_VERDI['Navn']:navn_tabell[oppføring_VERDI['Navn']] for oppføring_VERDI in erklæring_tabell.values()
              if oppføring_VERDI['종류']==501 and oppføring_VERDI['Navn'] in navn_tabell and oppføring_VERDI['Navn'] not in SD}
    for Sti in sorted({Path(oppføring_VERDI['Fil']) for oppføring_VERDI in erklæring_tabell.values()}):
        linje_Liste = Sti.read_text().splitlines(True); 이어짐 = False
        for INDEKS,Linje in enumerate(linje_Liste):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Linje))
            이어짐 = 전처리 and Linje.rstrip().endswith('\\')
            if 전처리:
                oppslagstabell = navn_tabell if re.match(r'\s*#\s*define\b',Linje) or 이어짐 else makro_VERDI
                linje_Liste[INDEKS] = 낱말.sub(lambda 맞음: oppslagstabell.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Linje)
        Sti.write_text(''.join(linje_Liste))
    # 각 eget OVERSETT_kilde 단위에만 연결표를 넣는다. ekstern_VERDI 배포본에는 전파하지 않는다.
    for Sti in sorted({Path(oppføring_VERDI['Fil']) for oppføring_VERDI in erklæring_tabell.values()}):
        if Sti.suffix not in ('.c','.cpp'):continue
        node_VERDI_6a3b6fa7 = '../' * len(Sti.relative_to(speile_rot).parts[:-1]) + '명명/기계연결이름.h'
        Sti.write_text('#include "'+node_VERDI_6a3b6fa7+'"\n'+Sti.read_text())
    (speile_rot/'명명/C_navn_tildeling.tsv').write_text('\n'.join(LOG_POST)+'\n')
    (speile_rot/'build/한국어화/전처리참조.json').write_text(json.dumps(avvis_VERDI,ensure_ascii=False,indent=2)+'\n')
    print('endre_VERDI',len(LOG_POST)-1,'전처리 재검토',len(avvis_VERDI),'maskin Koble_til',len(kontakt_tabell))

if __name__=='__main__': Utfør_kommando()
