#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 baidht_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 innealan.

외부 구조체의 멤버, sreang_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 atharraich_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

tilg_freumh = Path(__file__).resolve().parents[1]

def gnìomhaich_àithne():
    분석 = json.loads((tilg_freumh/'build/한국어화/시언어분석.json').read_text())
    if 분석['Mearachd']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    ainm_clàr = json.loads((tilg_freumh/'명명/시언어이름.json').read_text())
    SD = set(json.loads((tilg_freumh/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_VALUE:ainm_clàr[cur_a_steach_VALUE['Ainm']] for UNIQUE_VALUE,cur_a_steach_VALUE in 선언표.items()
                if cur_a_steach_VALUE['Ainm'] in ainm_clàr and cur_a_steach_VALUE['Ainm'] not in SD}
    ceangal_clàr = {cur_a_steach_VALUE['Ainm']:ainm_clàr[cur_a_steach_VALUE['Ainm']] for cur_a_steach_VALUE in 선언표.values()
              if cur_a_steach_VALUE.get('CONNECT')==4 and cur_a_steach_VALUE['종류'] in (8,9)
              and cur_a_steach_VALUE['Ainm'] in ainm_clàr and cur_a_steach_VALUE['Ainm'] not in SD}
    # gin AOT C·어셈블리·공개 SDK가 공유하는 바이너리 CONNECT 이름만 유지한다.
    머리 = ['/* 한국어 tùs_craobh 이름과 기존 inneal CONNECT cùis_VALUE. 자동 gin: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(ceangal_clàr.items())]
    머리 += ['#endif','']
    (tilg_freumh/'명명/기계연결이름.h').write_text('\n'.join(머리))
    atharraichean_Liosta = defaultdict(dict)
    for faidhle,OFFSET_VALUE,Ainm,UNIQUE_VALUE in 분석['fiosrachadh']:
        if UNIQUE_VALUE in 바꿀선언:
            atharraichean_Liosta[faidhle][OFFSET_VALUE] = (Ainm,바꿀선언[UNIQUE_VALUE])
    LOG_ràgh = ['faidhle\t원래바이트위치\t이전이름\t한국어이름']
    leig_seachad_VALUE = []
    for faidhle,atharraich_VALUE in atharraichean_Liosta.items():
        Slighe = Path(faidhle); 원본 = Slighe.read_bytes(); dàta = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(atharraich_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                leig_seachad_VALUE.append((str(Slighe.relative_to(tilg_freumh)),OFFSET_VALUE,옛이름));continue
            dàta = dàta[:OFFSET_VALUE]+새이름.encode()+dàta[끝:]
            LOG_ràgh.append('{}\t{}\t{}\t{}'.format(Slighe.relative_to(tilg_freumh),OFFSET_VALUE,옛이름,새이름))
        Slighe.write_bytes(dàta)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macro_VALUE = {cur_a_steach_VALUE['Ainm']:ainm_clàr[cur_a_steach_VALUE['Ainm']] for cur_a_steach_VALUE in 선언표.values()
              if cur_a_steach_VALUE['종류']==501 and cur_a_steach_VALUE['Ainm'] in ainm_clàr and cur_a_steach_VALUE['Ainm'] not in SD}
    for Slighe in sorted({Path(cur_a_steach_VALUE['faidhle']) for cur_a_steach_VALUE in 선언표.values()}):
        loidhne_Liosta = Slighe.read_text().splitlines(True); 이어짐 = False
        for INDEX,loidhne in enumerate(loidhne_Liosta):
            전처리 = 이어짐 or bool(re.match(r'\s*#',loidhne))
            이어짐 = 전처리 and loidhne.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_clàr = ainm_clàr if re.match(r'\s*#\s*define\b',loidhne) or 이어짐 else macro_VALUE
                loidhne_Liosta[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_clàr.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],loidhne)
        Slighe.write_text(''.join(loidhne_Liosta))
    # 각 자체 TRANSLATE_tùs 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Slighe in sorted({Path(cur_a_steach_VALUE['faidhle']) for cur_a_steach_VALUE in 선언표.values()}):
        if Slighe.suffix not in ('.c','.cpp'):continue
        seise_VALUE = '../' * len(Slighe.relative_to(tilg_freumh).parts[:-1]) + '명명/기계연결이름.h'
        Slighe.write_text('#include "'+seise_VALUE+'"\n'+Slighe.read_text())
    (tilg_freumh/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_ràgh)+'\n')
    (tilg_freumh/'build/한국어화/전처리참조.json').write_text(json.dumps(leig_seachad_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('atharraich_VALUE',len(LOG_ràgh)-1,'전처리 재검토',len(leig_seachad_VALUE),'inneal CONNECT',len(ceangal_clàr))

if __name__=='__main__': gnìomhaich_àithne()
