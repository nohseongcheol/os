#!/usr/bin/env python3
"""deklarace_4f4f026b 고유번호와 UTF-8 bajt_HODNOTA 위치로 vlastní C 이름을 옮기는 일회성 이행 nástroje.

externí_HODNOTA 구조체의 멤버, řetězec_HODNOTA, C 표준 funkce_HODNOTA, 이식 규약은 보존한다.
입력은 změnit_HODNOTA 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

akce_kořen = Path(__file__).resolve().parents[1]

def Provést_příkaz():
    Analýza_HODNOTA = json.loads((akce_kořen/'build/한국어화/시언어분석.json').read_text())
    if Analýza_HODNOTA['chyba']: raise SystemExit('Analýza_HODNOTA 오류를 먼저 해결해야 합니다.')
    název_tabulka = json.loads((akce_kořen/'명명/시언어이름.json').read_text())
    SD = set(json.loads((akce_kořen/'명명/규격이름.json').read_text()))
    deklarace_tabulka = Analýza_HODNOTA['deklarace_4f4f026b']
    바꿀선언 = {UNIQUE_HODNOTA:název_tabulka[položka_HODNOTA['Název']] for UNIQUE_HODNOTA,položka_HODNOTA in deklarace_tabulka.items()
                if položka_HODNOTA['Název'] in název_tabulka and položka_HODNOTA['Název'] not in SD}
    kontakt_tabulka = {položka_HODNOTA['Název']:název_tabulka[položka_HODNOTA['Název']] for položka_HODNOTA in deklarace_tabulka.values()
              if položka_HODNOTA.get('Připojit')==4 and položka_HODNOTA['Druh_HODNOTA'] in (8,9)
              and položka_HODNOTA['Název'] in název_tabulka and položka_HODNOTA['Název'] not in SD}
    # generovat AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Připojit 이름만 유지한다.
    머리 = ['/* čeština zdroj_strom 이름과 기존 počítač Připojit hodnota_smlouvy. 자동 generovat: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(kontakt_tabulka.items())]
    머리 += ['#endif','']
    (akce_kořen/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Změny_Seznam = defaultdict(dict)
    for název_souboru,POSUN_HODNOTA,Název,UNIQUE_HODNOTA in Analýza_HODNOTA['odkaz']:
        if UNIQUE_HODNOTA in 바꿀선언:
            Změny_Seznam[název_souboru][POSUN_HODNOTA] = (Název,바꿀선언[UNIQUE_HODNOTA])
    LOGZ_ZÁZNAM = ['název_souboru\t원래바이트위치\t이전이름\t한국어이름']
    ignorovat_HODNOTA = []
    for název_souboru,změnit_HODNOTA in Změny_Seznam.items():
        cesta_2 = Path(název_souboru); 원본 = cesta_2.read_bytes(); data = 원본
        for POSUN_HODNOTA,(옛이름,새이름) in sorted(změnit_HODNOTA.items(),reverse=True):
            끝 = POSUN_HODNOTA+len(옛이름.encode())
            if 원본[POSUN_HODNOTA:끝] != 옛이름.encode():
                ignorovat_HODNOTA.append((str(cesta_2.relative_to(akce_kořen)),POSUN_HODNOTA,옛이름));continue
            data = data[:POSUN_HODNOTA]+새이름.encode()+data[끝:]
            LOGZ_ZÁZNAM.append('{}\t{}\t{}\t{}'.format(cesta_2.relative_to(akce_kořen),POSUN_HODNOTA,옛이름,새이름))
        cesta_2.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_HODNOTA = {položka_HODNOTA['Název']:název_tabulka[položka_HODNOTA['Název']] for položka_HODNOTA in deklarace_tabulka.values()
              if položka_HODNOTA['Druh_HODNOTA']==501 and položka_HODNOTA['Název'] in název_tabulka and položka_HODNOTA['Název'] not in SD}
    for cesta_2 in sorted({Path(položka_HODNOTA['název_souboru']) for položka_HODNOTA in deklarace_tabulka.values()}):
        čára_Seznam = cesta_2.read_text().splitlines(True); 이어짐 = False
        for INDEX,vstupní_řádek in enumerate(čára_Seznam):
            전처리 = 이어짐 or bool(re.match(r'\s*#',vstupní_řádek))
            이어짐 = 전처리 and vstupní_řádek.rstrip().endswith('\\')
            if 전처리:
                VYHLEDAT_tabulka = název_tabulka if re.match(r'\s*#\s*define\b',vstupní_řádek) or 이어짐 else makro_HODNOTA
                čára_Seznam[INDEX] = 낱말.sub(lambda 맞음: VYHLEDAT_tabulka.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],vstupní_řádek)
        cesta_2.write_text(''.join(čára_Seznam))
    # 각 vlastní převést_zdroj 단위에만 연결표를 넣는다. externí_HODNOTA 배포본에는 전파하지 않는다.
    for cesta_2 in sorted({Path(položka_HODNOTA['název_souboru']) for položka_HODNOTA in deklarace_tabulka.values()}):
        if cesta_2.suffix not in ('.c','.cpp'):continue
        partner_HODNOTA = '../' * len(cesta_2.relative_to(akce_kořen).parts[:-1]) + '명명/기계연결이름.h'
        cesta_2.write_text('#include "'+partner_HODNOTA+'"\n'+cesta_2.read_text())
    (akce_kořen/'명명/시언어이름대응.tsv').write_text('\n'.join(LOGZ_ZÁZNAM)+'\n')
    (akce_kořen/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorovat_HODNOTA,ensure_ascii=False,indent=2)+'\n')
    print('změnit_HODNOTA',len(LOGZ_ZÁZNAM)-1,'전처리 재검토',len(ignorovat_HODNOTA),'počítač Připojit',len(kontakt_tabulka))

if __name__=='__main__': Provést_příkaz()
