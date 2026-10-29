#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 bayiti_agaciro 위치로 자체 C 이름을 옮기는 일회성 이행 Ibikoresho.

외부 구조체의 멤버, igicenteruro_agaciro, C 표준 FUNCTION_agaciro, 이식 규약은 보존한다.
입력은 guhindura_agaciro_16f64fe4 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def gukora_ibwiriza():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['IKOSA']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    izina_imbonerahamwe = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {RUKUMBI_agaciro:izina_imbonerahamwe[icyinjizwa_agaciro['Izina']] for RUKUMBI_agaciro,icyinjizwa_agaciro in 선언표.items()
                if icyinjizwa_agaciro['Izina'] in izina_imbonerahamwe and icyinjizwa_agaciro['Izina'] not in SD}
    kwihuza_imbonerahamwe = {icyinjizwa_agaciro['Izina']:izina_imbonerahamwe[icyinjizwa_agaciro['Izina']] for icyinjizwa_agaciro in 선언표.values()
              if icyinjizwa_agaciro.get('Guhuza')==4 and icyinjizwa_agaciro['종류'] in (8,9)
              and icyinjizwa_agaciro['Izina'] in izina_imbonerahamwe and icyinjizwa_agaciro['Izina'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Guhuza 이름만 유지한다.
    머리 = ['/* Ikinyarwanda inkomoko_igiti 이름과 기존 imashini Guhuza ikibazo_agaciro. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(kwihuza_imbonerahamwe.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Ibyahinduwe_Urutonde = defaultdict(dict)
    for Idosiye,Ofuseti_agaciro,Izina,RUKUMBI_agaciro in 분석['Indanga']:
        if RUKUMBI_agaciro in 바꿀선언:
            Ibyahinduwe_Urutonde[Idosiye][Ofuseti_agaciro] = (Izina,바꿀선언[RUKUMBI_agaciro])
    kubika_umurongo = ['Idosiye\t원래바이트위치\t이전이름\t한국어이름']
    kwirengagiza_agaciro = []
    for Idosiye,guhindura_agaciro_16f64fe4 in Ibyahinduwe_Urutonde.items():
        Inzira = Path(Idosiye); 원본 = Inzira.read_bytes(); amakurushingiro = 원본
        for Ofuseti_agaciro,(옛이름,새이름) in sorted(guhindura_agaciro_16f64fe4.items(),reverse=True):
            끝 = Ofuseti_agaciro+len(옛이름.encode())
            if 원본[Ofuseti_agaciro:끝] != 옛이름.encode():
                kwirengagiza_agaciro.append((str(Inzira.relative_to(기준)),Ofuseti_agaciro,옛이름));continue
            amakurushingiro = amakurushingiro[:Ofuseti_agaciro]+새이름.encode()+amakurushingiro[끝:]
            kubika_umurongo.append('{}\t{}\t{}\t{}'.format(Inzira.relative_to(기준),Ofuseti_agaciro,옛이름,새이름))
        Inzira.write_bytes(amakurushingiro)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makoro_agaciro = {icyinjizwa_agaciro['Izina']:izina_imbonerahamwe[icyinjizwa_agaciro['Izina']] for icyinjizwa_agaciro in 선언표.values()
              if icyinjizwa_agaciro['종류']==501 and icyinjizwa_agaciro['Izina'] in izina_imbonerahamwe and icyinjizwa_agaciro['Izina'] not in SD}
    for Inzira in sorted({Path(icyinjizwa_agaciro['Idosiye']) for icyinjizwa_agaciro in 선언표.values()}):
        umurongo_Urutonde = Inzira.read_text().splitlines(True); 이어짐 = False
        for umugerekashakiro,umurongo in enumerate(umurongo_Urutonde):
            전처리 = 이어짐 or bool(re.match(r'\s*#',umurongo))
            이어짐 = 전처리 and umurongo.rstrip().endswith('\\')
            if 전처리:
                표 = izina_imbonerahamwe if re.match(r'\s*#\s*define\b',umurongo) or 이어짐 else makoro_agaciro
                umurongo_Urutonde[umugerekashakiro] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],umurongo)
        Inzira.write_text(''.join(umurongo_Urutonde))
    # 각 자체 Gusemura_inkomoko 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Inzira in sorted({Path(icyinjizwa_agaciro['Idosiye']) for icyinjizwa_agaciro in 선언표.values()}):
        if Inzira.suffix not in ('.c','.cpp'):continue
        Mugenzi_agaciro = '../' * len(Inzira.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        Inzira.write_text('#include "'+Mugenzi_agaciro+'"\n'+Inzira.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(kubika_umurongo)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(kwirengagiza_agaciro,ensure_ascii=False,indent=2)+'\n')
    print('guhindura_agaciro_16f64fe4',len(kubika_umurongo)-1,'전처리 재검토',len(kwirengagiza_agaciro),'imashini Guhuza',len(kwihuza_imbonerahamwe))

if __name__=='__main__': gukora_ibwiriza()
