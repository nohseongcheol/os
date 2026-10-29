#!/usr/bin/env python3
"""erklæring 고유번호와 UTF-8 byte_VÆRDI 위치로 eget C 이름을 옮기는 일회성 이행 Værktøjer.

ekstern_VÆRDI 구조체의 멤버, streng_VÆRDI, C 표준 FUNKTION_VÆRDI, 이식 규약은 보존한다.
입력은 ændre_VÆRDI 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

To_do_rod = Path(__file__).resolve().parents[1]

def Udfør_kommando():
    Analyse_VÆRDI = json.loads((To_do_rod/'build/한국어화/시언어분석.json').read_text())
    if Analyse_VÆRDI['fejl']: raise SystemExit('Analyse_VÆRDI 오류를 먼저 해결해야 합니다.')
    navn_tabel = json.loads((To_do_rod/'명명/시언어이름.json').read_text())
    SD = set(json.loads((To_do_rod/'명명/규격이름.json').read_text()))
    erklæring_tabel = Analyse_VÆRDI['erklæring']
    바꿀선언 = {ENTYDIGE_VÆRDI:navn_tabel[post_VÆRDI_962f286b['Navn']] for ENTYDIGE_VÆRDI,post_VÆRDI_962f286b in erklæring_tabel.items()
                if post_VÆRDI_962f286b['Navn'] in navn_tabel and post_VÆRDI_962f286b['Navn'] not in SD}
    forbindelse_tabel = {post_VÆRDI_962f286b['Navn']:navn_tabel[post_VÆRDI_962f286b['Navn']] for post_VÆRDI_962f286b in erklæring_tabel.values()
              if post_VÆRDI_962f286b.get('Tilslut')==4 and post_VÆRDI_962f286b['종류'] in (8,9)
              and post_VÆRDI_962f286b['Navn'] in navn_tabel and post_VÆRDI_962f286b['Navn'] not in SD}
    # generere AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Tilslut 이름만 유지한다.
    머리 = ['/* Dansk kilde_træ 이름과 기존 maskine Tilslut kontraktværdi. 자동 generere: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(forbindelse_tabel.items())]
    머리 += ['#endif','']
    (To_do_rod/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Ændringer_Liste = defaultdict(dict)
    for Fil,FORSKYDNING_VÆRDI,Navn,ENTYDIGE_VÆRDI in Analyse_VÆRDI['referere']:
        if ENTYDIGE_VÆRDI in 바꿀선언:
            Ændringer_Liste[Fil][FORSKYDNING_VÆRDI] = (Navn,바꿀선언[ENTYDIGE_VÆRDI])
    LOG_post = ['Fil\t원래바이트위치\t이전이름\t한국어이름']
    ignorer_VÆRDI = []
    for Fil,ændre_VÆRDI in Ændringer_Liste.items():
        Sti = Path(Fil); 원본 = Sti.read_bytes(); data = 원본
        for FORSKYDNING_VÆRDI,(옛이름,새이름) in sorted(ændre_VÆRDI.items(),reverse=True):
            끝 = FORSKYDNING_VÆRDI+len(옛이름.encode())
            if 원본[FORSKYDNING_VÆRDI:끝] != 옛이름.encode():
                ignorer_VÆRDI.append((str(Sti.relative_to(To_do_rod)),FORSKYDNING_VÆRDI,옛이름));continue
            data = data[:FORSKYDNING_VÆRDI]+새이름.encode()+data[끝:]
            LOG_post.append('{}\t{}\t{}\t{}'.format(Sti.relative_to(To_do_rod),FORSKYDNING_VÆRDI,옛이름,새이름))
        Sti.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VÆRDI = {post_VÆRDI_962f286b['Navn']:navn_tabel[post_VÆRDI_962f286b['Navn']] for post_VÆRDI_962f286b in erklæring_tabel.values()
              if post_VÆRDI_962f286b['종류']==501 and post_VÆRDI_962f286b['Navn'] in navn_tabel and post_VÆRDI_962f286b['Navn'] not in SD}
    for Sti in sorted({Path(post_VÆRDI_962f286b['Fil']) for post_VÆRDI_962f286b in erklæring_tabel.values()}):
        linje_Liste = Sti.read_text().splitlines(True); 이어짐 = False
        for INDEKS,Linje in enumerate(linje_Liste):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Linje))
            이어짐 = 전처리 and Linje.rstrip().endswith('\\')
            if 전처리:
                Opslag_tabel = navn_tabel if re.match(r'\s*#\s*define\b',Linje) or 이어짐 else makro_VÆRDI
                linje_Liste[INDEKS] = 낱말.sub(lambda 맞음: Opslag_tabel.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Linje)
        Sti.write_text(''.join(linje_Liste))
    # 각 eget OVERSÆT_kilde 단위에만 연결표를 넣는다. ekstern_VÆRDI 배포본에는 전파하지 않는다.
    for Sti in sorted({Path(post_VÆRDI_962f286b['Fil']) for post_VÆRDI_962f286b in erklæring_tabel.values()}):
        if Sti.suffix not in ('.c','.cpp'):continue
        peer_VÆRDI = '../' * len(Sti.relative_to(To_do_rod).parts[:-1]) + '명명/기계연결이름.h'
        Sti.write_text('#include "'+peer_VÆRDI+'"\n'+Sti.read_text())
    (To_do_rod/'명명/C_navn_tilknytning.tsv').write_text('\n'.join(LOG_post)+'\n')
    (To_do_rod/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorer_VÆRDI,ensure_ascii=False,indent=2)+'\n')
    print('ændre_VÆRDI',len(LOG_post)-1,'전처리 재검토',len(ignorer_VÆRDI),'maskine Tilslut',len(forbindelse_tabel))

if __name__=='__main__': Udfør_kommando()
