#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 baịtị_valuu 위치로 자체 C 이름을 옮기는 일회성 이행 Ngwaọrụ.

외부 구조체의 멤버, ùsòròokwū_valuu, C 표준 ọrụ_valuu, 이식 규약은 보존한다.
입력은 gbanwèe_valuu 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def mee_nnyemiwu():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['mmejọ']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    akara_ahà_tebùl = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {PỤRỤICHE_valuu:akara_ahà_tebùl[ndebà_valuu['Aha']] for PỤRỤICHE_valuu,ndebà_valuu in 선언표.items()
                if ndebà_valuu['Aha'] in akara_ahà_tebùl and ndebà_valuu['Aha'] not in SD}
    njikọ_tebùl = {ndebà_valuu['Aha']:akara_ahà_tebùl[ndebà_valuu['Aha']] for ndebà_valuu in 선언표.values()
              if ndebà_valuu.get('Banye')==4 and ndebà_valuu['종류'] in (8,9)
              and ndebà_valuu['Aha'] in akara_ahà_tebùl and ndebà_valuu['Aha'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Banye 이름만 유지한다.
    머리 = ['/* 한국어 ebensìbịa_èsèrèsè_osisi 이름과 기존 ngwa_komputa Banye ngō_valuu. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(njikọ_tebùl.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Mgbanwe_gasi_ndepụta = defaultdict(dict)
    for Faịlụ,Nnokwata_valuu,Aha,PỤRỤICHE_valuu in 분석['Nrụtụ_aka']:
        if PỤRỤICHE_valuu in 바꿀선언:
            Mgbanwe_gasi_ndepụta[Faịlụ][Nnokwata_valuu] = (Aha,바꿀선언[PỤRỤICHE_valuu])
    ndekọ_NDEKỌ = ['Faịlụ\t원래바이트위치\t이전이름\t한국어이름']
    leghara_anya_valuu = []
    for Faịlụ,gbanwèe_valuu in Mgbanwe_gasi_ndepụta.items():
        ụzọ_ozi = Path(Faịlụ); 원본 = ụzọ_ozi.read_bytes(); datà = 원본
        for Nnokwata_valuu,(옛이름,새이름) in sorted(gbanwèe_valuu.items(),reverse=True):
            끝 = Nnokwata_valuu+len(옛이름.encode())
            if 원본[Nnokwata_valuu:끝] != 옛이름.encode():
                leghara_anya_valuu.append((str(ụzọ_ozi.relative_to(기준)),Nnokwata_valuu,옛이름));continue
            datà = datà[:Nnokwata_valuu]+새이름.encode()+datà[끝:]
            ndekọ_NDEKỌ.append('{}\t{}\t{}\t{}'.format(ụzọ_ozi.relative_to(기준),Nnokwata_valuu,옛이름,새이름))
        ụzọ_ozi.write_bytes(datà)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    nkèokpookpo_valuu = {ndebà_valuu['Aha']:akara_ahà_tebùl[ndebà_valuu['Aha']] for ndebà_valuu in 선언표.values()
              if ndebà_valuu['종류']==501 and ndebà_valuu['Aha'] in akara_ahà_tebùl and ndebà_valuu['Aha'] not in SD}
    for ụzọ_ozi in sorted({Path(ndebà_valuu['Faịlụ']) for ndebà_valuu in 선언표.values()}):
        ahịrī_ndepụta = ụzọ_ozi.read_text().splitlines(True); 이어짐 = False
        for indèks,ahịrī in enumerate(ahịrī_ndepụta):
            전처리 = 이어짐 or bool(re.match(r'\s*#',ahịrī))
            이어짐 = 전처리 and ahịrī.rstrip().endswith('\\')
            if 전처리:
                표 = akara_ahà_tebùl if re.match(r'\s*#\s*define\b',ahịrī) or 이어짐 else nkèokpookpo_valuu
                ahịrī_ndepụta[indèks] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],ahịrī)
        ụzọ_ozi.write_text(''.join(ahịrī_ndepụta))
    # 각 자체 Tụgharia_ebensìbịa 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for ụzọ_ozi in sorted({Path(ndebà_valuu['Faịlụ']) for ndebà_valuu in 선언표.values()}):
        if ụzọ_ozi.suffix not in ('.c','.cpp'):continue
        ibè_valuu = '../' * len(ụzọ_ozi.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        ụzọ_ozi.write_text('#include "'+ibè_valuu+'"\n'+ụzọ_ozi.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(ndekọ_NDEKỌ)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(leghara_anya_valuu,ensure_ascii=False,indent=2)+'\n')
    print('gbanwèe_valuu',len(ndekọ_NDEKỌ)-1,'전처리 재검토',len(leghara_anya_valuu),'ngwa_komputa Banye',len(njikọ_tebùl))

if __name__=='__main__': mee_nnyemiwu()
