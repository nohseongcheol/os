#!/usr/bin/env python3
"""tamko 고유번호와 UTF-8 baiti_thamani 위치로 자체 C 이름을 옮기는 일회성 이행 Zana.

외부 구조체의 멤버, tungo_thamani, C 표준 KITENDAKAZI_thamani, 이식 규약은 보존한다.
입력은 badilisha_thamani_16f64fe4 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def tekeleza_amri():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['kosa']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    jina_jedwali = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    tamko_jedwali = 분석['tamko']
    바꿀선언 = {KIPEKEE_thamani:jina_jedwali[ingizo_thamani['Jina']] for KIPEKEE_thamani,ingizo_thamani in tamko_jedwali.items()
                if ingizo_thamani['Jina'] in jina_jedwali and ingizo_thamani['Jina'] not in SD}
    muunganisho_jedwali = {ingizo_thamani['Jina']:jina_jedwali[ingizo_thamani['Jina']] for ingizo_thamani in tamko_jedwali.values()
              if ingizo_thamani.get('UNGANISHA')==4 and ingizo_thamani['종류'] in (8,9)
              and ingizo_thamani['Jina'] in jina_jedwali and ingizo_thamani['Jina'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 UNGANISHA 이름만 유지한다.
    머리 = ['/* 한국어 chanzo_mti 이름과 기존 mashine UNGANISHA Kazi_thamani. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(muunganisho_jedwali.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Mabadiliko_Orodha = defaultdict(dict)
    for faili,Chipua_thamani,Jina,KIPEKEE_thamani in 분석['Marejeleo']:
        if KIPEKEE_thamani in 바꿀선언:
            Mabadiliko_Orodha[faili][Chipua_thamani] = (Jina,바꿀선언[KIPEKEE_thamani])
    batli_REKODI = ['faili\t원래바이트위치\t이전이름\t한국어이름']
    puuza_thamani_3c26be06 = []
    for faili,badilisha_thamani_16f64fe4 in Mabadiliko_Orodha.items():
        njia = Path(faili); 원본 = njia.read_bytes(); data = 원본
        for Chipua_thamani,(옛이름,새이름) in sorted(badilisha_thamani_16f64fe4.items(),reverse=True):
            끝 = Chipua_thamani+len(옛이름.encode())
            if 원본[Chipua_thamani:끝] != 옛이름.encode():
                puuza_thamani_3c26be06.append((str(njia.relative_to(기준)),Chipua_thamani,옛이름));continue
            data = data[:Chipua_thamani]+새이름.encode()+data[끝:]
            batli_REKODI.append('{}\t{}\t{}\t{}'.format(njia.relative_to(기준),Chipua_thamani,옛이름,새이름))
        njia.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_thamani = {ingizo_thamani['Jina']:jina_jedwali[ingizo_thamani['Jina']] for ingizo_thamani in tamko_jedwali.values()
              if ingizo_thamani['종류']==501 and ingizo_thamani['Jina'] in jina_jedwali and ingizo_thamani['Jina'] not in SD}
    for njia in sorted({Path(ingizo_thamani['faili']) for ingizo_thamani in tamko_jedwali.values()}):
        laini_Orodha = njia.read_text().splitlines(True); 이어짐 = False
        for kielezo,laini in enumerate(laini_Orodha):
            전처리 = 이어짐 or bool(re.match(r'\s*#',laini))
            이어짐 = 전처리 and laini.rstrip().endswith('\\')
            if 전처리:
                표 = jina_jedwali if re.match(r'\s*#\s*define\b',laini) or 이어짐 else makro_thamani
                laini_Orodha[kielezo] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],laini)
        njia.write_text(''.join(laini_Orodha))
    # 각 자체 Tafsiri_chanzo 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for njia in sorted({Path(ingizo_thamani['faili']) for ingizo_thamani in tamko_jedwali.values()}):
        if njia.suffix not in ('.c','.cpp'):continue
        kompyuta_rika_thamani = '../' * len(njia.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        njia.write_text('#include "'+kompyuta_rika_thamani+'"\n'+njia.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(batli_REKODI)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(puuza_thamani_3c26be06,ensure_ascii=False,indent=2)+'\n')
    print('badilisha_thamani_16f64fe4',len(batli_REKODI)-1,'전처리 재검토',len(puuza_thamani_3c26be06),'mashine UNGANISHA',len(muunganisho_jedwali))

if __name__=='__main__': tekeleza_amri()
