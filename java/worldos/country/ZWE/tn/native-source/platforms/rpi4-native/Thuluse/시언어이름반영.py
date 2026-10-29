#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 baete_Boleng 위치로 자체 C 이름을 옮기는 일회성 이행 Thuluse.

외부 구조체의 멤버, dikwalwa_Boleng, C 표준 TIRISO_Boleng, 이식 규약은 보존한다.
입력은 fetola_Boleng 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def diragatsa_Taelo():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['phoso']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    leina_lenaneothalo = json.loads((기준/'명명/시언어이름.json').read_text())
    SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {TLHOMOLOGA_Boleng:leina_lenaneothalo[tsenyo_Boleng['leina']] for TLHOMOLOGA_Boleng,tsenyo_Boleng in 선언표.items()
                if tsenyo_Boleng['leina'] in leina_lenaneothalo and tsenyo_Boleng['leina'] not in SD}
    Kgolagano_lenaneothalo = {tsenyo_Boleng['leina']:leina_lenaneothalo[tsenyo_Boleng['leina']] for tsenyo_Boleng in 선언표.values()
              if tsenyo_Boleng.get('Golaganya')==4 and tsenyo_Boleng['종류'] in (8,9)
              and tsenyo_Boleng['leina'] in leina_lenaneothalo and tsenyo_Boleng['leina'] not in SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Golaganya 이름만 유지한다.
    머리 = ['/* 한국어 Motswedi_sebopego_sa_tshedimosetso 이름과 기존 motšhine Golaganya konteraka_Boleng. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(Kgolagano_lenaneothalo.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Diphetogo_lenaane = defaultdict(dict)
    for faele,Baya_ka_Tekatekanyo_Boleng,leina,TLHOMOLOGA_Boleng in 분석['Tshupiso']:
        if TLHOMOLOGA_Boleng in 바꿀선언:
            Diphetogo_lenaane[faele][Baya_ka_Tekatekanyo_Boleng] = (leina,바꿀선언[TLHOMOLOGA_Boleng])
    rekota_mola = ['faele\t원래바이트위치\t이전이름\t한국어이름']
    ikgatholose_Boleng = []
    for faele,fetola_Boleng in Diphetogo_lenaane.items():
        tsela = Path(faele); 원본 = tsela.read_bytes(); tshedimosetso = 원본
        for Baya_ka_Tekatekanyo_Boleng,(옛이름,새이름) in sorted(fetola_Boleng.items(),reverse=True):
            끝 = Baya_ka_Tekatekanyo_Boleng+len(옛이름.encode())
            if 원본[Baya_ka_Tekatekanyo_Boleng:끝] != 옛이름.encode():
                ikgatholose_Boleng.append((str(tsela.relative_to(기준)),Baya_ka_Tekatekanyo_Boleng,옛이름));continue
            tshedimosetso = tshedimosetso[:Baya_ka_Tekatekanyo_Boleng]+새이름.encode()+tshedimosetso[끝:]
            rekota_mola.append('{}\t{}\t{}\t{}'.format(tsela.relative_to(기준),Baya_ka_Tekatekanyo_Boleng,옛이름,새이름))
        tsela.write_bytes(tshedimosetso)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makhero_Boleng = {tsenyo_Boleng['leina']:leina_lenaneothalo[tsenyo_Boleng['leina']] for tsenyo_Boleng in 선언표.values()
              if tsenyo_Boleng['종류']==501 and tsenyo_Boleng['leina'] in leina_lenaneothalo and tsenyo_Boleng['leina'] not in SD}
    for tsela in sorted({Path(tsenyo_Boleng['faele']) for tsenyo_Boleng in 선언표.values()}):
        Mola_lenaane = tsela.read_text().splitlines(True); 이어짐 = False
        for tshupane,Mola in enumerate(Mola_lenaane):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Mola))
            이어짐 = 전처리 and Mola.rstrip().endswith('\\')
            if 전처리:
                표 = leina_lenaneothalo if re.match(r'\s*#\s*define\b',Mola) or 이어짐 else makhero_Boleng
                Mola_lenaane[tshupane] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Mola)
        tsela.write_text(''.join(Mola_lenaane))
    # 각 자체 Ranola_Motswedi 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for tsela in sorted({Path(tsenyo_Boleng['faele']) for tsenyo_Boleng in 선언표.values()}):
        if tsela.suffix not in ('.c','.cpp'):continue
        semphato_Boleng = '../' * len(tsela.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        tsela.write_text('#include "'+semphato_Boleng+'"\n'+tsela.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(rekota_mola)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(ikgatholose_Boleng,ensure_ascii=False,indent=2)+'\n')
    print('fetola_Boleng',len(rekota_mola)-1,'전처리 재검토',len(ikgatholose_Boleng),'motšhine Golaganya',len(Kgolagano_lenaneothalo))

if __name__=='__main__': diragatsa_Taelo()
