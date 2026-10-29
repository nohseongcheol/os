#!/usr/bin/env python3
"""deklarazio 고유번호와 UTF-8 byte_balio 위치로 자체 C 이름을 옮기는 일회성 이행 Tresnak.

외부 구조체의 멤버, kate_balio, C 표준 FUNTZIOA_balio, 이식 규약은 보존한다.
입력은 aldatu_balio 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_erro = Path(__file__).resolve().parents[1]

def exekutatu_komando():
    Analizatu_balio = json.loads((Project_erro/'build/한국어화/시언어분석.json').read_text())
    if Analizatu_balio['errorea']: raise SystemExit('Analizatu_balio 오류를 먼저 해결해야 합니다.')
    izen_taula = json.loads((Project_erro/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_erro/'명명/규격이름.json').read_text()))
    deklarazio_taula = Analizatu_balio['deklarazio']
    바꿀선언 = {ESKLUSIBOAK_balio:izen_taula[sarrera_balio['Izena']] for ESKLUSIBOAK_balio,sarrera_balio in deklarazio_taula.items()
                if sarrera_balio['Izena'] in izen_taula and sarrera_balio['Izena'] not in SD}
    konexio_taula = {sarrera_balio['Izena']:izen_taula[sarrera_balio['Izena']] for sarrera_balio in deklarazio_taula.values()
              if sarrera_balio.get('Konektatu')==4 and sarrera_balio['종류'] in (8,9)
              and sarrera_balio['Izena'] in izen_taula and sarrera_balio['Izena'] not in SD}
    # sortu AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Konektatu 이름만 유지한다.
    머리 = ['/* Euskara iturburu_zuhaitz 이름과 기존 gailu Konektatu kasu_balio. 자동 sortu: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(konexio_taula.items())]
    머리 += ['#endif','']
    (Project_erro/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Aldaketak_Zerrenda = defaultdict(dict)
    for Fitxategia,Geruzak_balio,Izena,ESKLUSIBOAK_balio in Analizatu_balio['Erreferentzia_materiala']:
        if ESKLUSIBOAK_balio in 바꿀선언:
            Aldaketak_Zerrenda[Fitxategia][Geruzak_balio] = (Izena,바꿀선언[ESKLUSIBOAK_balio])
    LOG_marka = ['Fitxategia\t원래바이트위치\t이전이름\t한국어이름']
    ez_ikusi_egin_balio = []
    for Fitxategia,aldatu_balio in Aldaketak_Zerrenda.items():
        Bide_izena = Path(Fitxategia); 원본 = Bide_izena.read_bytes(); datuak = 원본
        for Geruzak_balio,(옛이름,새이름) in sorted(aldatu_balio.items(),reverse=True):
            끝 = Geruzak_balio+len(옛이름.encode())
            if 원본[Geruzak_balio:끝] != 옛이름.encode():
                ez_ikusi_egin_balio.append((str(Bide_izena.relative_to(Project_erro)),Geruzak_balio,옛이름));continue
            datuak = datuak[:Geruzak_balio]+새이름.encode()+datuak[끝:]
            LOG_marka.append('{}\t{}\t{}\t{}'.format(Bide_izena.relative_to(Project_erro),Geruzak_balio,옛이름,새이름))
        Bide_izena.write_bytes(datuak)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_balio = {sarrera_balio['Izena']:izen_taula[sarrera_balio['Izena']] for sarrera_balio in deklarazio_taula.values()
              if sarrera_balio['종류']==501 and sarrera_balio['Izena'] in izen_taula and sarrera_balio['Izena'] not in SD}
    for Bide_izena in sorted({Path(sarrera_balio['Fitxategia']) for sarrera_balio in deklarazio_taula.values()}):
        lerro_Zerrenda = Bide_izena.read_text().splitlines(True); 이어짐 = False
        for INDIZE,Marra in enumerate(lerro_Zerrenda):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Marra))
            이어짐 = 전처리 and Marra.rstrip().endswith('\\')
            if 전처리:
                BEGIRATU_taula = izen_taula if re.match(r'\s*#\s*define\b',Marra) or 이어짐 else makro_balio
                lerro_Zerrenda[INDIZE] = 낱말.sub(lambda 맞음: BEGIRATU_taula.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Marra)
        Bide_izena.write_text(''.join(lerro_Zerrenda))
    # 각 자체 ITZULI_iturburu 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Bide_izena in sorted({Path(sarrera_balio['Fitxategia']) for sarrera_balio in deklarazio_taula.values()}):
        if Bide_izena.suffix not in ('.c','.cpp'):continue
        pareko_balio = '../' * len(Bide_izena.relative_to(Project_erro).parts[:-1]) + '명명/기계연결이름.h'
        Bide_izena.write_text('#include "'+pareko_balio+'"\n'+Bide_izena.read_text())
    (Project_erro/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_marka)+'\n')
    (Project_erro/'build/한국어화/전처리참조.json').write_text(json.dumps(ez_ikusi_egin_balio,ensure_ascii=False,indent=2)+'\n')
    print('aldatu_balio',len(LOG_marka)-1,'전처리 재검토',len(ez_ikusi_egin_balio),'gailu Konektatu',len(konexio_taula))

if __name__=='__main__': exekutatu_komando()
