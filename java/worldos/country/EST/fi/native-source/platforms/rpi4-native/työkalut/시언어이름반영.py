#!/usr/bin/env python3
"""esittely 고유번호와 UTF-8 tavu_ARVO 위치로 oma C 이름을 옮기는 일회성 이행 työkalut.

ulkoinen_ARVO 구조체의 멤버, merkkijono_ARVO, C 표준 funktio_ARVO, 이식 규약은 보존한다.
입력은 muuttaa_ARVO 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

aloite_juuri = Path(__file__).resolve().parents[1]

def Suorita_komento():
    Analysoi_ARVO = json.loads((aloite_juuri/'build/한국어화/시언어분석.json').read_text())
    if Analysoi_ARVO['VIRHE']: raise SystemExit('Analysoi_ARVO 오류를 먼저 해결해야 합니다.')
    nimi_taulukko = json.loads((aloite_juuri/'명명/시언어이름.json').read_text())
    SD = set(json.loads((aloite_juuri/'명명/규격이름.json').read_text()))
    esittely_taulukko = Analysoi_ARVO['esittely']
    바꿀선언 = {AINUTKERTAISET_ARVOT_ARVO:nimi_taulukko[merkintä_ARVO_962f286b['Nimi']] for AINUTKERTAISET_ARVOT_ARVO,merkintä_ARVO_962f286b in esittely_taulukko.items()
                if merkintä_ARVO_962f286b['Nimi'] in nimi_taulukko and merkintä_ARVO_962f286b['Nimi'] not in SD}
    yhteys_taulukko = {merkintä_ARVO_962f286b['Nimi']:nimi_taulukko[merkintä_ARVO_962f286b['Nimi']] for merkintä_ARVO_962f286b in esittely_taulukko.values()
              if merkintä_ARVO_962f286b.get('Yhdistä')==4 and merkintä_ARVO_962f286b['종류'] in (8,9)
              and merkintä_ARVO_962f286b['Nimi'] in nimi_taulukko and merkintä_ARVO_962f286b['Nimi'] not in SD}
    # generoida AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Yhdistä 이름만 유지한다.
    머리 = ['/* suomi lähde_puu 이름과 기존 kone Yhdistä sopimuksen_arvo. 자동 generoida: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(yhteys_taulukko.items())]
    머리 += ['#endif','']
    (aloite_juuri/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Muutokset_luettelo = defaultdict(dict)
    for tiedoston_nimi,SIIRTYMÄ_ARVO,Nimi,AINUTKERTAISET_ARVOT_ARVO in Analysoi_ARVO['viite']:
        if AINUTKERTAISET_ARVOT_ARVO in 바꿀선언:
            Muutokset_luettelo[tiedoston_nimi][SIIRTYMÄ_ARVO] = (Nimi,바꿀선언[AINUTKERTAISET_ARVOT_ARVO])
    LOG_TIETUE = ['tiedoston_nimi\t원래바이트위치\t이전이름\t한국어이름']
    ohita_ARVO = []
    for tiedoston_nimi,muuttaa_ARVO in Muutokset_luettelo.items():
        polku_2 = Path(tiedoston_nimi); 원본 = polku_2.read_bytes(); data = 원본
        for SIIRTYMÄ_ARVO,(옛이름,새이름) in sorted(muuttaa_ARVO.items(),reverse=True):
            끝 = SIIRTYMÄ_ARVO+len(옛이름.encode())
            if 원본[SIIRTYMÄ_ARVO:끝] != 옛이름.encode():
                ohita_ARVO.append((str(polku_2.relative_to(aloite_juuri)),SIIRTYMÄ_ARVO,옛이름));continue
            data = data[:SIIRTYMÄ_ARVO]+새이름.encode()+data[끝:]
            LOG_TIETUE.append('{}\t{}\t{}\t{}'.format(polku_2.relative_to(aloite_juuri),SIIRTYMÄ_ARVO,옛이름,새이름))
        polku_2.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_ARVO = {merkintä_ARVO_962f286b['Nimi']:nimi_taulukko[merkintä_ARVO_962f286b['Nimi']] for merkintä_ARVO_962f286b in esittely_taulukko.values()
              if merkintä_ARVO_962f286b['종류']==501 and merkintä_ARVO_962f286b['Nimi'] in nimi_taulukko and merkintä_ARVO_962f286b['Nimi'] not in SD}
    for polku_2 in sorted({Path(merkintä_ARVO_962f286b['tiedoston_nimi']) for merkintä_ARVO_962f286b in esittely_taulukko.values()}):
        rivi_luettelo = polku_2.read_text().splitlines(True); 이어짐 = False
        for INDEKSI,syöterivi in enumerate(rivi_luettelo):
            전처리 = 이어짐 or bool(re.match(r'\s*#',syöterivi))
            이어짐 = 전처리 and syöterivi.rstrip().endswith('\\')
            if 전처리:
                HAKU_taulukko = nimi_taulukko if re.match(r'\s*#\s*define\b',syöterivi) or 이어짐 else makro_ARVO
                rivi_luettelo[INDEKSI] = 낱말.sub(lambda 맞음: HAKU_taulukko.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],syöterivi)
        polku_2.write_text(''.join(rivi_luettelo))
    # 각 oma KÄÄNNÄ_lähde 단위에만 연결표를 넣는다. ulkoinen_ARVO 배포본에는 전파하지 않는다.
    for polku_2 in sorted({Path(merkintä_ARVO_962f286b['tiedoston_nimi']) for merkintä_ARVO_962f286b in esittely_taulukko.values()}):
        if polku_2.suffix not in ('.c','.cpp'):continue
        vertaissolmu_ARVO = '../' * len(polku_2.relative_to(aloite_juuri).parts[:-1]) + '명명/기계연결이름.h'
        polku_2.write_text('#include "'+vertaissolmu_ARVO+'"\n'+polku_2.read_text())
    (aloite_juuri/'명명/C_nimi_yhdistämismääritys.tsv').write_text('\n'.join(LOG_TIETUE)+'\n')
    (aloite_juuri/'build/한국어화/전처리참조.json').write_text(json.dumps(ohita_ARVO,ensure_ascii=False,indent=2)+'\n')
    print('muuttaa_ARVO',len(LOG_TIETUE)-1,'전처리 재검토',len(ohita_ARVO),'kone Yhdistä',len(yhteys_taulukko))

if __name__=='__main__': Suorita_komento()
