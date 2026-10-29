#!/usr/bin/env python3
"""bayyanarwa 고유번호와 UTF-8 bayit_Daraja 위치로 자체 C 이름을 옮기는 일회성 이행 Kaya.

외부 구조체의 멤버, Zare_Daraja, C 표준 AIKI_Daraja, 이식 규약은 보존한다.
입력은 Canza_Daraja 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def gudanar_Umarni():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['Kuskure']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    Suna_tebur = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    bayyanarwa_tebur = 분석['bayyanarwa']
    바꿀선언 = {MUSAMMAN_Daraja:Suna_tebur[Mashigar_bayanai_Daraja['Suna']] for MUSAMMAN_Daraja,Mashigar_bayanai_Daraja in bayyanarwa_tebur.items()
                if Mashigar_bayanai_Daraja['Suna'] in Suna_tebur and Mashigar_bayanai_Daraja['Suna'] not in SD}
    haɗi_tebur = {Mashigar_bayanai_Daraja['Suna']:Suna_tebur[Mashigar_bayanai_Daraja['Suna']] for Mashigar_bayanai_Daraja in bayyanarwa_tebur.values()
              if Mashigar_bayanai_Daraja.get('Haɗi')==4 and Mashigar_bayanai_Daraja['종류'] in (8,9)
              and Mashigar_bayanai_Daraja['Suna'] in Suna_tebur and Mashigar_bayanai_Daraja['Suna'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Haɗi 이름만 유지한다.
    머리 = ['/* 한국어 tushe_Li_irabin_tarin_bayanai 이름과 기존 na_ura_mai_kwakwalwa Haɗi Kes_Daraja. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(haɗi_tebur.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Canje_canje_Jeri = defaultdict(dict)
    for Fayil,Sassautawa_Daraja,Suna,MUSAMMAN_Daraja in 분석['Manazarta']:
        if MUSAMMAN_Daraja in 바꿀선언:
            Canje_canje_Jeri[Fayil][Sassautawa_Daraja] = (Suna,바꿀선언[MUSAMMAN_Daraja])
    logu_naɗa = ['Fayil\t원래바이트위치\t이전이름\t한국어이름']
    ƙyale_Daraja = []
    for Fayil,Canza_Daraja in Canje_canje_Jeri.items():
        Hanyar_shiga = Path(Fayil); 원본 = Hanyar_shiga.read_bytes(); Tarin_bayani = 원본
        for Sassautawa_Daraja,(옛이름,새이름) in sorted(Canza_Daraja.items(),reverse=True):
            끝 = Sassautawa_Daraja+len(옛이름.encode())
            if 원본[Sassautawa_Daraja:끝] != 옛이름.encode():
                ƙyale_Daraja.append((str(Hanyar_shiga.relative_to(기준)),Sassautawa_Daraja,옛이름));continue
            Tarin_bayani = Tarin_bayani[:Sassautawa_Daraja]+새이름.encode()+Tarin_bayani[끝:]
            logu_naɗa.append('{}\t{}\t{}\t{}'.format(Hanyar_shiga.relative_to(기준),Sassautawa_Daraja,옛이름,새이름))
        Hanyar_shiga.write_bytes(Tarin_bayani)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    Makullin_gargadi_Daraja = {Mashigar_bayanai_Daraja['Suna']:Suna_tebur[Mashigar_bayanai_Daraja['Suna']] for Mashigar_bayanai_Daraja in bayyanarwa_tebur.values()
              if Mashigar_bayanai_Daraja['종류']==501 and Mashigar_bayanai_Daraja['Suna'] in Suna_tebur and Mashigar_bayanai_Daraja['Suna'] not in SD}
    for Hanyar_shiga in sorted({Path(Mashigar_bayanai_Daraja['Fayil']) for Mashigar_bayanai_Daraja in bayyanarwa_tebur.values()}):
        Layi_Jeri = Hanyar_shiga.read_text().splitlines(True); 이어짐 = False
        for Indes,Layi in enumerate(Layi_Jeri):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Layi))
            이어짐 = 전처리 and Layi.rstrip().endswith('\\')
            if 전처리:
                표 = Suna_tebur if re.match(r'\s*#\s*define\b',Layi) or 이어짐 else Makullin_gargadi_Daraja
                Layi_Jeri[Indes] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Layi)
        Hanyar_shiga.write_text(''.join(Layi_Jeri))
    # 각 자체 Fasara_tushe 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Hanyar_shiga in sorted({Path(Mashigar_bayanai_Daraja['Fayil']) for Mashigar_bayanai_Daraja in bayyanarwa_tebur.values()}):
        if Hanyar_shiga.suffix not in ('.c','.cpp'):continue
        Fiya_Daraja = '../' * len(Hanyar_shiga.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        Hanyar_shiga.write_text('#include "'+Fiya_Daraja+'"\n'+Hanyar_shiga.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(logu_naɗa)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(ƙyale_Daraja,ensure_ascii=False,indent=2)+'\n')
    print('Canza_Daraja',len(logu_naɗa)-1,'전처리 재검토',len(ƙyale_Daraja),'na_ura_mai_kwakwalwa Haɗi',len(haɗi_tebur))

if __name__=='__main__': gudanar_Umarni()
