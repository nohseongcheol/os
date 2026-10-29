#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 ibhayithi_inani 위치로 자체 C 이름을 옮기는 일회성 이행 Amathuluzi.

외부 구조체의 멤버, uchunge_inani, C 표준 umsebenzi_inani, 이식 규약은 보존한다.
입력은 guqula_inani 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def yenza_umyalo():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['Iphutha']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    igama_ithebula = json.loads((기준/'명명/시언어이름.json').read_text())
    I_SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {OKUHLUKILE_inani:igama_ithebula[okufakwayo_inani['Igama']] for OKUHLUKILE_inani,okufakwayo_inani in 선언표.items()
                if okufakwayo_inani['Igama'] in igama_ithebula and okufakwayo_inani['Igama'] not in I_SD}
    uxhumano_ithebula = {okufakwayo_inani['Igama']:igama_ithebula[okufakwayo_inani['Igama']] for okufakwayo_inani in 선언표.values()
              if okufakwayo_inani.get('Xhumanisa')==4 and okufakwayo_inani['종류'] in (8,9)
              and okufakwayo_inani['Igama'] in igama_ithebula and okufakwayo_inani['Igama'] not in I_SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Xhumanisa 이름만 유지한다.
    머리 = ['/* Isi_Zulu umthombo_isihlahla 이름과 기존 umshini Xhumanisa udaba_inani. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(uxhumano_ithebula.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Izinguquko_Uhlu = defaultdict(dict)
    for Ihele,I_ofisethi_inani,Igama,OKUHLUKILE_inani in 분석['Ireferensi']:
        if OKUHLUKILE_inani in 바꿀선언:
            Izinguquko_Uhlu[Ihele][I_ofisethi_inani] = (Igama,바꿀선언[OKUHLUKILE_inani])
    loga_umugqa = ['Ihele\t원래바이트위치\t이전이름\t한국어이름']
    shaya_indiva_inani = []
    for Ihele,guqula_inani in Izinguquko_Uhlu.items():
        Indlela_2 = Path(Ihele); 원본 = Indlela_2.read_bytes(); imininingwane = 원본
        for I_ofisethi_inani,(옛이름,새이름) in sorted(guqula_inani.items(),reverse=True):
            끝 = I_ofisethi_inani+len(옛이름.encode())
            if 원본[I_ofisethi_inani:끝] != 옛이름.encode():
                shaya_indiva_inani.append((str(Indlela_2.relative_to(기준)),I_ofisethi_inani,옛이름));continue
            imininingwane = imininingwane[:I_ofisethi_inani]+새이름.encode()+imininingwane[끝:]
            loga_umugqa.append('{}\t{}\t{}\t{}'.format(Indlela_2.relative_to(기준),I_ofisethi_inani,옛이름,새이름))
        Indlela_2.write_bytes(imininingwane)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    imakhro_inani = {okufakwayo_inani['Igama']:igama_ithebula[okufakwayo_inani['Igama']] for okufakwayo_inani in 선언표.values()
              if okufakwayo_inani['종류']==501 and okufakwayo_inani['Igama'] in igama_ithebula and okufakwayo_inani['Igama'] not in I_SD}
    for Indlela_2 in sorted({Path(okufakwayo_inani['Ihele']) for okufakwayo_inani in 선언표.values()}):
        umugqa_Uhlu = Indlela_2.read_text().splitlines(True); 이어짐 = False
        for thola_inkomba,umugqa in enumerate(umugqa_Uhlu):
            전처리 = 이어짐 or bool(re.match(r'\s*#',umugqa))
            이어짐 = 전처리 and umugqa.rstrip().endswith('\\')
            if 전처리:
                표 = igama_ithebula if re.match(r'\s*#\s*define\b',umugqa) or 이어짐 else imakhro_inani
                umugqa_Uhlu[thola_inkomba] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in I_SD else 맞음[0],umugqa)
        Indlela_2.write_text(''.join(umugqa_Uhlu))
    # 각 자체 Ukuhumusha_umthombo 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Indlela_2 in sorted({Path(okufakwayo_inani['Ihele']) for okufakwayo_inani in 선언표.values()}):
        if Indlela_2.suffix not in ('.c','.cpp'):continue
        untanga_inani = '../' * len(Indlela_2.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        Indlela_2.write_text('#include "'+untanga_inani+'"\n'+Indlela_2.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(loga_umugqa)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(shaya_indiva_inani,ensure_ascii=False,indent=2)+'\n')
    print('guqula_inani',len(loga_umugqa)-1,'전처리 재검토',len(shaya_indiva_inani),'umshini Xhumanisa',len(uxhumano_ithebula))

if __name__=='__main__': yenza_umyalo()
