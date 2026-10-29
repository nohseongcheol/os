#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 byte_atuutilik 위치로 자체 C 이름을 옮기는 일회성 이행 도구.

외부 구조체의 멤버, qimiaq_atuutilik, C 표준 sugiakkannirut_atuutilik, 이식 규약은 보존한다.
입력은 asijjirli_atuutilik 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def 실행():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['tammarniq']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    atiq_kipu = json.loads((기준/'명명/시언어이름.json').read_text())
    규격 = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {고유:atiq_kipu[Iliniku_atuutilik['atiq']] for 고유,Iliniku_atuutilik in 선언표.items()
                if Iliniku_atuutilik['atiq'] in atiq_kipu and Iliniku_atuutilik['atiq'] not in 규격}
    kasuqsimaniq_kipu = {Iliniku_atuutilik['atiq']:atiq_kipu[Iliniku_atuutilik['atiq']] for Iliniku_atuutilik in 선언표.values()
              if Iliniku_atuutilik.get('kasurli')==4 and Iliniku_atuutilik['종류'] in (8,9)
              and Iliniku_atuutilik['atiq'] in atiq_kipu and Iliniku_atuutilik['atiq'] not in 규격}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 kasurli 이름만 유지한다.
    머리 = ['/* 한국어 pivviujuq_attavigiit 이름과 기존 기계 kasurli pijatsaq_atuutilik. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(kasuqsimaniq_kipu.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    변경들 = defaultdict(dict)
    for ini,변위,atiq,고유 in 분석['참조']:
        if 고유 in 바꿀선언:
            변경들[ini][변위] = (atiq,바꿀선언[고유])
    papattivik_sanimukutaak = ['ini\t원래바이트위치\t이전이름\t한국어이름']
    ikpiginagu_atuutilik = []
    for ini,asijjirli_atuutilik in 변경들.items():
        aqqut = Path(ini); 원본 = aqqut.read_bytes(); titiqqat = 원본
        for 변위,(옛이름,새이름) in sorted(asijjirli_atuutilik.items(),reverse=True):
            끝 = 변위+len(옛이름.encode())
            if 원본[변위:끝] != 옛이름.encode():
                ikpiginagu_atuutilik.append((str(aqqut.relative_to(기준)),변위,옛이름));continue
            titiqqat = titiqqat[:변위]+새이름.encode()+titiqqat[끝:]
            papattivik_sanimukutaak.append('{}\t{}\t{}\t{}'.format(aqqut.relative_to(기준),변위,옛이름,새이름))
        aqqut.write_bytes(titiqqat)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    aulattijjutialaaq_atuutilik = {Iliniku_atuutilik['atiq']:atiq_kipu[Iliniku_atuutilik['atiq']] for Iliniku_atuutilik in 선언표.values()
              if Iliniku_atuutilik['종류']==501 and Iliniku_atuutilik['atiq'] in atiq_kipu and Iliniku_atuutilik['atiq'] not in 규격}
    for aqqut in sorted({Path(Iliniku_atuutilik['ini']) for Iliniku_atuutilik in 선언표.values()}):
        titikutaak_Titiqpalliagaq = aqqut.read_text().splitlines(True); 이어짐 = False
        for nalunaiqsimavik,titikutaak in enumerate(titikutaak_Titiqpalliagaq):
            전처리 = 이어짐 or bool(re.match(r'\s*#',titikutaak))
            이어짐 = 전처리 and titikutaak.rstrip().endswith('\\')
            if 전처리:
                표 = atiq_kipu if re.match(r'\s*#\s*define\b',titikutaak) or 이어짐 else aulattijjutialaaq_atuutilik
                titikutaak_Titiqpalliagaq[nalunaiqsimavik] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in 규격 else 맞음[0],titikutaak)
        aqqut.write_text(''.join(titikutaak_Titiqpalliagaq))
    # 각 자체 번역 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for aqqut in sorted({Path(Iliniku_atuutilik['ini']) for Iliniku_atuutilik in 선언표.values()}):
        if aqqut.suffix not in ('.c','.cpp'):continue
        ilagijaujuq_atuutilik = '../' * len(aqqut.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        aqqut.write_text('#include "'+ilagijaujuq_atuutilik+'"\n'+aqqut.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(papattivik_sanimukutaak)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(ikpiginagu_atuutilik,ensure_ascii=False,indent=2)+'\n')
    print('asijjirli_atuutilik',len(papattivik_sanimukutaak)-1,'전처리 재검토',len(ikpiginagu_atuutilik),'기계 kasurli',len(kasuqsimaniq_kipu))

if __name__=='__main__': 실행()
