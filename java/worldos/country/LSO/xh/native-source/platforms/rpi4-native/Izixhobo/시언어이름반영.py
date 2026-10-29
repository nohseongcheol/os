#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 ibhayithi_ixabiso 위치로 자체 C 이름을 옮기는 일회성 이행 Izixhobo.

외부 구조체의 멤버, uluhlu_lweekharektha_ixabiso, C 표준 INKQUBO_ixabiso, 이식 규약은 보존한다.
입력은 tshintsha_ixabiso 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]

def ukwenza_umyalelo():
    분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
    if 분석['Impazamo']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    igama_itheyibhile = json.loads((기준/'명명/시언어이름.json').read_text())
    I_SD = set(json.loads((기준/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {EYODWA_ixabiso:igama_itheyibhile[ufako_nkcukacha_ixabiso['Igama']] for EYODWA_ixabiso,ufako_nkcukacha_ixabiso in 선언표.items()
                if ufako_nkcukacha_ixabiso['Igama'] in igama_itheyibhile and ufako_nkcukacha_ixabiso['Igama'] not in I_SD}
    uqhagamshelo_itheyibhile = {ufako_nkcukacha_ixabiso['Igama']:igama_itheyibhile[ufako_nkcukacha_ixabiso['Igama']] for ufako_nkcukacha_ixabiso in 선언표.values()
              if ufako_nkcukacha_ixabiso.get('Nxulumanisa')==4 and ufako_nkcukacha_ixabiso['종류'] in (8,9)
              and ufako_nkcukacha_ixabiso['Igama'] in igama_itheyibhile and ufako_nkcukacha_ixabiso['Igama'] not in I_SD}
    # 생성 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Nxulumanisa 이름만 유지한다.
    머리 = ['/* isiXhosa umthombo_umthi 이름과 기존 umatshini Nxulumanisa isiganeko_ixabiso. 자동 생성: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(uqhagamshelo_itheyibhile.items())]
    머리 += ['#endif','']
    (기준/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Iinguquko_uludwe = defaultdict(dict)
    for iFayili,Ukulinganisa_ixabiso,Igama,EYODWA_ixabiso in 분석['Isalathiso']:
        if EYODWA_ixabiso in 바꿀선언:
            Iinguquko_uludwe[iFayili][Ukulinganisa_ixabiso] = (Igama,바꿀선언[EYODWA_ixabiso])
    ilog_umqolo = ['iFayili\t원래바이트위치\t이전이름\t한국어이름']
    ngahoyi_ixabiso = []
    for iFayili,tshintsha_ixabiso in Iinguquko_uludwe.items():
        INDLELA = Path(iFayili); 원본 = INDLELA.read_bytes(); iingcombolo = 원본
        for Ukulinganisa_ixabiso,(옛이름,새이름) in sorted(tshintsha_ixabiso.items(),reverse=True):
            끝 = Ukulinganisa_ixabiso+len(옛이름.encode())
            if 원본[Ukulinganisa_ixabiso:끝] != 옛이름.encode():
                ngahoyi_ixabiso.append((str(INDLELA.relative_to(기준)),Ukulinganisa_ixabiso,옛이름));continue
            iingcombolo = iingcombolo[:Ukulinganisa_ixabiso]+새이름.encode()+iingcombolo[끝:]
            ilog_umqolo.append('{}\t{}\t{}\t{}'.format(INDLELA.relative_to(기준),Ukulinganisa_ixabiso,옛이름,새이름))
        INDLELA.write_bytes(iingcombolo)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    imakhro_ixabiso = {ufako_nkcukacha_ixabiso['Igama']:igama_itheyibhile[ufako_nkcukacha_ixabiso['Igama']] for ufako_nkcukacha_ixabiso in 선언표.values()
              if ufako_nkcukacha_ixabiso['종류']==501 and ufako_nkcukacha_ixabiso['Igama'] in igama_itheyibhile and ufako_nkcukacha_ixabiso['Igama'] not in I_SD}
    for INDLELA in sorted({Path(ufako_nkcukacha_ixabiso['iFayili']) for ufako_nkcukacha_ixabiso in 선언표.values()}):
        umgca_uludwe = INDLELA.read_text().splitlines(True); 이어짐 = False
        for indeksa,umgca in enumerate(umgca_uludwe):
            전처리 = 이어짐 or bool(re.match(r'\s*#',umgca))
            이어짐 = 전처리 and umgca.rstrip().endswith('\\')
            if 전처리:
                표 = igama_itheyibhile if re.match(r'\s*#\s*define\b',umgca) or 이어짐 else imakhro_ixabiso
                umgca_uludwe[indeksa] = 낱말.sub(lambda 맞음: 표.get(맞음[0],맞음[0]) if 맞음[0] not in I_SD else 맞음[0],umgca)
        INDLELA.write_text(''.join(umgca_uludwe))
    # 각 자체 Ukuguqulela_umthombo 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for INDLELA in sorted({Path(ufako_nkcukacha_ixabiso['iFayili']) for ufako_nkcukacha_ixabiso in 선언표.values()}):
        if INDLELA.suffix not in ('.c','.cpp'):continue
        untanga_ixabiso = '../' * len(INDLELA.relative_to(기준).parts[:-1]) + '명명/기계연결이름.h'
        INDLELA.write_text('#include "'+untanga_ixabiso+'"\n'+INDLELA.read_text())
    (기준/'명명/시언어이름대응.tsv').write_text('\n'.join(ilog_umqolo)+'\n')
    (기준/'build/한국어화/전처리참조.json').write_text(json.dumps(ngahoyi_ixabiso,ensure_ascii=False,indent=2)+'\n')
    print('tshintsha_ixabiso',len(ilog_umqolo)-1,'전처리 재검토',len(ngahoyi_ixabiso),'umatshini Nxulumanisa',len(uqhagamshelo_itheyibhile))

if __name__=='__main__': ukwenza_umyalelo()
