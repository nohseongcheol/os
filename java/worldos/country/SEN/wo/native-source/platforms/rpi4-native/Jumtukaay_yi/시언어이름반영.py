#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 okte_xëyma 위치로 자체 C 이름을 옮기는 일회성 이행 Jumtukaay_yi.

외부 구조체의 멤버, araf_yu_bennoo_xëyma, C 표준 liëey_xëyma, 이식 규약은 보존한다.
입력은 soppi_xëyma_16f64fe4 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def def_ndigel():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['njumte']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    tur_àlluwa = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_xëyma:tur_àlluwa[dugal_xabaar_xëyma['tur_253d1510']] for UNIQUE_xëyma,dugal_xabaar_xëyma in 선언표.items()
                if dugal_xabaar_xëyma['tur_253d1510'] in tur_àlluwa and dugal_xabaar_xëyma['tur_253d1510'] not in SD}
    jokkalóo_àlluwa = {dugal_xabaar_xëyma['tur_253d1510']:tur_àlluwa[dugal_xabaar_xëyma['tur_253d1510']] for dugal_xabaar_xëyma in 선언표.values()
              if dugal_xabaar_xëyma.get('JOKKOO')==4 and dugal_xabaar_xëyma['종류'] in (8,9)
              and dugal_xabaar_xëyma['tur_253d1510'] in tur_àlluwa and dugal_xabaar_xëyma['tur_253d1510'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 JOKKOO 이름만 유지한다.
    머리 = ['/* 한국어 Cosaan_tëralinuy_pàcc 이름과 기존 masin JOKKOO ay_xëyma. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(jokkalóo_àlluwa.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Coppite_yi_lim = defaultdict(dict)
    for bara_denc,Randal_xëyma,tur_253d1510,UNIQUE_xëyma in 분석['Royukaay']:
        if UNIQUE_xëyma in 바꿀선언:
            Coppite_yi_lim[bara_denc][Randal_xëyma] = (tur_253d1510,바꿀선언[UNIQUE_xëyma])
    làq_Dënk = ['bara_denc\t원래바이트위치\t이전이름\t한국어이름']
    bañ_xëyma = []
    for bara_denc,soppi_xëyma_16f64fe4 in Coppite_yi_lim.items():
        Yoonu_jëmale = Path(bara_denc); 원본 = Yoonu_jëmale.read_bytes(); mbir = 원본
        for Randal_xëyma,(옛이름,새이름) in sorted(soppi_xëyma_16f64fe4.items(),reverse=True):
            끝 = Randal_xëyma+len(옛이름.encode())
            if 원본[Randal_xëyma:끝] != 옛이름.encode():
                bañ_xëyma.append((str(Yoonu_jëmale.relative_to(기준)),Randal_xëyma,옛이름));continue
            mbir = mbir[:Randal_xëyma]+새이름.encode()+mbir[끝:]
            làq_Dënk.append('{}\t{}\t{}\t{}'.format(Yoonu_jëmale.relative_to(기준),Randal_xëyma,옛이름,새이름))
        Yoonu_jëmale.write_bytes(mbir)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    gaawtal_xëyma = {dugal_xabaar_xëyma['tur_253d1510']:tur_àlluwa[dugal_xabaar_xëyma['tur_253d1510']] for dugal_xabaar_xëyma in 선언표.values()
              if dugal_xabaar_xëyma['종류']==501 and dugal_xabaar_xëyma['tur_253d1510'] in tur_àlluwa and dugal_xabaar_xëyma['tur_253d1510'] not in SD}
    for Yoonu_jëmale in sorted({Path(dugal_xabaar_xëyma['bara_denc']) for dugal_xabaar_xëyma in 선언표.values()}):
        buum_lim = Yoonu_jëmale.read_text().splitlines(True); 이어짐 = False
        for àlluwa_tur,buum in enumerate(buum_lim):
            전처리 = 이어짐 or bool(re.match(r'\s*#',buum))
            이어짐 = 전처리 and buum.rstrip().endswith('\\')
            if 전처리:
                표 = tur_àlluwa if re.match(r'\s*#\s*define\b',buum) or 이어짐 else gaawtal_xëyma
                buum_lim[àlluwa_tur] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],buum)
        Yoonu_jëmale.write_text(''.join(buum_lim))
    # 각 자체 Tekki_Cosaan 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Yoonu_jëmale in sorted({Path(dugal_xabaar_xëyma['bara_denc']) for dugal_xabaar_xëyma in 선언표.values()}):
        if Yoonu_jëmale.suffix not in ('.c','.cpp'):continue
        Nàttangoo_xëyma = '../' * len(Yoonu_jëmale.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        Yoonu_jëmale.write_text('#include "'+Nàttangoo_xëyma+'"\n'+Yoonu_jëmale.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(làq_Dënk)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(bañ_xëyma,ensure_ascii=False,indent=2)+'\n')
    print('soppi_xëyma_16f64fe4',len(làq_Dënk)-1,'전처리 재검토',len(bañ_xëyma),'masin JOKKOO',len(jokkalóo_àlluwa))

if __name__=='__main__': def_ndigel()
