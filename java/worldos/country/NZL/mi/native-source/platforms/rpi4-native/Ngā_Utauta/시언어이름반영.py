#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 paita_uara 위치로 자체 C 이름을 옮기는 일회성 이행 Ngā_Utauta.

외부 구조체의 멤버, aho_uara, C 표준 TAUMAHI_uara, 이식 규약은 보존한다.
입력은 huri_uara 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

whakaatu_pūtake = Path(__file__).resolve().parents[1]

def kawe_tono():
    분석 = json.loads((whakaatu_pūtake/'build/한국어화/시언어분석.json').read_text())
    if 분석['Pōhēhē']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    ingoa_ripanga = json.loads((whakaatu_pūtake/'명명/시언어이름.json').read_text())
    SD = set(json.loads((whakaatu_pūtake/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_uara:ingoa_ripanga[tāurunga_uara['Ingoa']] for UNIQUE_uara,tāurunga_uara in 선언표.items()
                if tāurunga_uara['Ingoa'] in ingoa_ripanga and tāurunga_uara['Ingoa'] not in SD}
    hononga_ripanga = {tāurunga_uara['Ingoa']:ingoa_ripanga[tāurunga_uara['Ingoa']] for tāurunga_uara in 선언표.values()
              if tāurunga_uara.get('TŪHONO')==4 and tāurunga_uara['종류'] in (8,9)
              and tāurunga_uara['Ingoa'] in ingoa_ripanga and tāurunga_uara['Ingoa'] not in SD}
    # waihanga AOT C·어셈블리·공개 SDK가 공유하는 바이너리 TŪHONO 이름만 유지한다.
    머리 = ['/* Reo_Māori pūtake_rākau 이름과 기존 mīhini TŪHONO kēhi_uara. 자동 waihanga: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(hononga_ripanga.items())]
    머리 += ['#endif','']
    (whakaatu_pūtake/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Ngā_Huringa_Rārangi = defaultdict(dict)
    for Kōnae,OFFSET_uara,Ingoa,UNIQUE_uara in 분석['Pūranga_kōrero']:
        if UNIQUE_uara in 바꿀선언:
            Ngā_Huringa_Rārangi[Kōnae][OFFSET_uara] = (Ingoa,바꿀선언[UNIQUE_uara])
    LOG_RECORD = ['Kōnae\t원래바이트위치\t이전이름\t한국어이름']
    waiho_uara = []
    for Kōnae,huri_uara in Ngā_Huringa_Rārangi.items():
        ara = Path(Kōnae); 원본 = ara.read_bytes(); raraunga = 원본
        for OFFSET_uara,(옛이름,새이름) in sorted(huri_uara.items(),reverse=True):
            끝 = OFFSET_uara+len(옛이름.encode())
            if 원본[OFFSET_uara:끝] != 옛이름.encode():
                waiho_uara.append((str(ara.relative_to(whakaatu_pūtake)),OFFSET_uara,옛이름));continue
            raraunga = raraunga[:OFFSET_uara]+새이름.encode()+raraunga[끝:]
            LOG_RECORD.append('{}\t{}\t{}\t{}'.format(ara.relative_to(whakaatu_pūtake),OFFSET_uara,옛이름,새이름))
        ara.write_bytes(raraunga)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    tonotono_uara = {tāurunga_uara['Ingoa']:ingoa_ripanga[tāurunga_uara['Ingoa']] for tāurunga_uara in 선언표.values()
              if tāurunga_uara['종류']==501 and tāurunga_uara['Ingoa'] in ingoa_ripanga and tāurunga_uara['Ingoa'] not in SD}
    for ara in sorted({Path(tāurunga_uara['Kōnae']) for tāurunga_uara in 선언표.values()}):
        hononga_Rārangi = ara.read_text().splitlines(True); 이어짐 = False
        for INDEX,hononga in enumerate(hononga_Rārangi):
            전처리 = 이어짐 or bool(re.match(r'\s*#',hononga))
            이어짐 = 전처리 and hononga.rstrip().endswith('\\')
            if 전처리:
                Rapu_ripanga = ingoa_ripanga if re.match(r'\s*#\s*define\b',hononga) or 이어짐 else tonotono_uara
                hononga_Rārangi[INDEX] = 낱말.sub(lambda 맞음: Rapu_ripanga.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],hononga)
        ara.write_text(''.join(hononga_Rārangi))
    # 각 자체 TRANSLATE_pūtake 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for ara in sorted({Path(tāurunga_uara['Kōnae']) for tāurunga_uara in 선언표.values()}):
        if ara.suffix not in ('.c','.cpp'):continue
        hoa_uara = '../' * len(ara.relative_to(whakaatu_pūtake).parts[:-1]) + '명명/기계연결이름.h'
        ara.write_text('#include "'+hoa_uara+'"\n'+ara.read_text())
    (whakaatu_pūtake/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_RECORD)+'\n')
    (whakaatu_pūtake/'build/한국어화/전처리참조.json').write_text(json.dumps(waiho_uara,ensure_ascii=False,indent=2)+'\n')
    print('huri_uara',len(LOG_RECORD)-1,'전처리 재검토',len(waiho_uara),'mīhini TŪHONO',len(hononga_ripanga))

if __name__=='__main__': kawe_tono()
