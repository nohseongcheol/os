#!/usr/bin/env python3
"""bevallás 고유번호와 UTF-8 bájt_ÉRTÉK 위치로 saját C 이름을 옮기는 일회성 이행 Eszközök.

külső_ÉRTÉK 구조체의 멤버, sztring_ÉRTÉK, C 표준 FÜGGVÉNY_ÉRTÉK, 이식 규약은 보존한다.
입력은 módosítás_ÉRTÉK 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

teendő_gyök = Path(__file__).resolve().parents[1]

def végrehajt_parancs():
    Elemzés_ÉRTÉK = json.loads((teendő_gyök/'build/한국어화/시언어분석.json').read_text())
    if Elemzés_ÉRTÉK['HIBA']: raise SystemExit('Elemzés_ÉRTÉK 오류를 먼저 해결해야 합니다.')
    név_tábla = json.loads((teendő_gyök/'명명/시언어이름.json').read_text())
    SD = set(json.loads((teendő_gyök/'명명/규격이름.json').read_text()))
    bevallás_tábla = Elemzés_ÉRTÉK['bevallás']
    바꿀선언 = {EGYEDI_ÉRTÉK:név_tábla[bejegyzés_ÉRTÉK['Név']] for EGYEDI_ÉRTÉK,bejegyzés_ÉRTÉK in bevallás_tábla.items()
                if bejegyzés_ÉRTÉK['Név'] in név_tábla and bejegyzés_ÉRTÉK['Név'] not in SD}
    ismerős_tábla = {bejegyzés_ÉRTÉK['Név']:név_tábla[bejegyzés_ÉRTÉK['Név']] for bejegyzés_ÉRTÉK in bevallás_tábla.values()
              if bejegyzés_ÉRTÉK.get('Kapcsolódás')==4 and bejegyzés_ÉRTÉK['Altípus_ÉRTÉK'] in (8,9)
              and bejegyzés_ÉRTÉK['Név'] in név_tábla and bejegyzés_ÉRTÉK['Név'] not in SD}
    # generálás AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Kapcsolódás 이름만 유지한다.
    머리 = ['/* magyar forrás_fa 이름과 기존 gép Kapcsolódás szerződés_értéke. 자동 generálás: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(ismerős_tábla.items())]
    머리 += ['#endif','']
    (teendő_gyök/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Módosítások_Lista = defaultdict(dict)
    for Fájl,Ofszet_ÉRTÉK,Név,EGYEDI_ÉRTÉK in Elemzés_ÉRTÉK['hivatkozik']:
        if EGYEDI_ÉRTÉK in 바꿀선언:
            Módosítások_Lista[Fájl][Ofszet_ÉRTÉK] = (Név,바꿀선언[EGYEDI_ÉRTÉK])
    LOG_REKORD = ['Fájl\t원래바이트위치\t이전이름\t한국어이름']
    mellőz_ÉRTÉK = []
    for Fájl,módosítás_ÉRTÉK in Módosítások_Lista.items():
        ÚTVONAL = Path(Fájl); 원본 = ÚTVONAL.read_bytes(); adat = 원본
        for Ofszet_ÉRTÉK,(옛이름,새이름) in sorted(módosítás_ÉRTÉK.items(),reverse=True):
            끝 = Ofszet_ÉRTÉK+len(옛이름.encode())
            if 원본[Ofszet_ÉRTÉK:끝] != 옛이름.encode():
                mellőz_ÉRTÉK.append((str(ÚTVONAL.relative_to(teendő_gyök)),Ofszet_ÉRTÉK,옛이름));continue
            adat = adat[:Ofszet_ÉRTÉK]+새이름.encode()+adat[끝:]
            LOG_REKORD.append('{}\t{}\t{}\t{}'.format(ÚTVONAL.relative_to(teendő_gyök),Ofszet_ÉRTÉK,옛이름,새이름))
        ÚTVONAL.write_bytes(adat)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makró_ÉRTÉK = {bejegyzés_ÉRTÉK['Név']:név_tábla[bejegyzés_ÉRTÉK['Név']] for bejegyzés_ÉRTÉK in bevallás_tábla.values()
              if bejegyzés_ÉRTÉK['Altípus_ÉRTÉK']==501 and bejegyzés_ÉRTÉK['Név'] in név_tábla and bejegyzés_ÉRTÉK['Név'] not in SD}
    for ÚTVONAL in sorted({Path(bejegyzés_ÉRTÉK['Fájl']) for bejegyzés_ÉRTÉK in bevallás_tábla.values()}):
        sor_Lista = ÚTVONAL.read_text().splitlines(True); 이어짐 = False
        for INDEX,Vonal in enumerate(sor_Lista):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Vonal))
            이어짐 = 전처리 and Vonal.rstrip().endswith('\\')
            if 전처리:
                keresőtáblázat = név_tábla if re.match(r'\s*#\s*define\b',Vonal) or 이어짐 else makró_ÉRTÉK
                sor_Lista[INDEX] = 낱말.sub(lambda 맞음: keresőtáblázat.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Vonal)
        ÚTVONAL.write_text(''.join(sor_Lista))
    # 각 saját FORDÍTÁS_forrás 단위에만 연결표를 넣는다. külső_ÉRTÉK 배포본에는 전파하지 않는다.
    for ÚTVONAL in sorted({Path(bejegyzés_ÉRTÉK['Fájl']) for bejegyzés_ÉRTÉK in bevallás_tábla.values()}):
        if ÚTVONAL.suffix not in ('.c','.cpp'):continue
        társ_ÉRTÉK = '../' * len(ÚTVONAL.relative_to(teendő_gyök).parts[:-1]) + '명명/기계연결이름.h'
        ÚTVONAL.write_text('#include "'+társ_ÉRTÉK+'"\n'+ÚTVONAL.read_text())
    (teendő_gyök/'명명/C_név_leképezés.tsv').write_text('\n'.join(LOG_REKORD)+'\n')
    (teendő_gyök/'build/한국어화/전처리참조.json').write_text(json.dumps(mellőz_ÉRTÉK,ensure_ascii=False,indent=2)+'\n')
    print('módosítás_ÉRTÉK',len(LOG_REKORD)-1,'전처리 재검토',len(mellőz_ÉRTÉK),'gép Kapcsolódás',len(ismerős_tábla))

if __name__=='__main__': végrehajt_parancs()
