#!/usr/bin/env python3
"""deklaracja 고유번호와 UTF-8 bajt_WARTOŚĆ 위치로 własny C 이름을 옮기는 일회성 이행 narzędzia.

zewnętrzny_WARTOŚĆ 구조체의 멤버, ciąg_WARTOŚĆ, C 표준 FUNKCJA_WARTOŚĆ, 이식 규약은 보존한다.
입력은 zmienić_WARTOŚĆ 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_korzeń = Path(__file__).resolve().parents[1]

def Wykonaj_polecenie():
    Analiza_WARTOŚĆ = json.loads((Project_korzeń/'build/한국어화/시언어분석.json').read_text())
    if Analiza_WARTOŚĆ['błąd']: raise SystemExit('Analiza_WARTOŚĆ 오류를 먼저 해결해야 합니다.')
    nazwa_tabela = json.loads((Project_korzeń/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_korzeń/'명명/규격이름.json').read_text()))
    deklaracja_tabela = Analiza_WARTOŚĆ['deklaracja']
    바꿀선언 = {UNIKATOWE_WARTOŚĆ:nazwa_tabela[wpis_WARTOŚĆ['Nazwa']] for UNIKATOWE_WARTOŚĆ,wpis_WARTOŚĆ in deklaracja_tabela.items()
                if wpis_WARTOŚĆ['Nazwa'] in nazwa_tabela and wpis_WARTOŚĆ['Nazwa'] not in SD}
    połączenie_tabela = {wpis_WARTOŚĆ['Nazwa']:nazwa_tabela[wpis_WARTOŚĆ['Nazwa']] for wpis_WARTOŚĆ in deklaracja_tabela.values()
              if wpis_WARTOŚĆ.get('Połącz')==4 and wpis_WARTOŚĆ['Rodzaj_WARTOŚĆ'] in (8,9)
              and wpis_WARTOŚĆ['Nazwa'] in nazwa_tabela and wpis_WARTOŚĆ['Nazwa'] not in SD}
    # generować AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Połącz 이름만 유지한다.
    머리 = ['/* polski źródło_drzewo 이름과 기존 maszyna Połącz wartość_kontraktu. 자동 generować: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(połączenie_tabela.items())]
    머리 += ['#endif','']
    (Project_korzeń/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Zmiany_Lista = defaultdict(dict)
    for nazwa_pliku,przesunąć_WARTOŚĆ_450fc799,Nazwa,UNIKATOWE_WARTOŚĆ in Analiza_WARTOŚĆ['odwołanie']:
        if UNIKATOWE_WARTOŚĆ in 바꿀선언:
            Zmiany_Lista[nazwa_pliku][przesunąć_WARTOŚĆ_450fc799] = (Nazwa,바꿀선언[UNIKATOWE_WARTOŚĆ])
    LOG_zapis = ['nazwa_pliku\t원래바이트위치\t이전이름\t한국어이름']
    ignorować_WARTOŚĆ = []
    for nazwa_pliku,zmienić_WARTOŚĆ in Zmiany_Lista.items():
        ścieżka_2 = Path(nazwa_pliku); 원본 = ścieżka_2.read_bytes(); dane = 원본
        for przesunąć_WARTOŚĆ_450fc799,(옛이름,새이름) in sorted(zmienić_WARTOŚĆ.items(),reverse=True):
            끝 = przesunąć_WARTOŚĆ_450fc799+len(옛이름.encode())
            if 원본[przesunąć_WARTOŚĆ_450fc799:끝] != 옛이름.encode():
                ignorować_WARTOŚĆ.append((str(ścieżka_2.relative_to(Project_korzeń)),przesunąć_WARTOŚĆ_450fc799,옛이름));continue
            dane = dane[:przesunąć_WARTOŚĆ_450fc799]+새이름.encode()+dane[끝:]
            LOG_zapis.append('{}\t{}\t{}\t{}'.format(ścieżka_2.relative_to(Project_korzeń),przesunąć_WARTOŚĆ_450fc799,옛이름,새이름))
        ścieżka_2.write_bytes(dane)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_WARTOŚĆ = {wpis_WARTOŚĆ['Nazwa']:nazwa_tabela[wpis_WARTOŚĆ['Nazwa']] for wpis_WARTOŚĆ in deklaracja_tabela.values()
              if wpis_WARTOŚĆ['Rodzaj_WARTOŚĆ']==501 and wpis_WARTOŚĆ['Nazwa'] in nazwa_tabela and wpis_WARTOŚĆ['Nazwa'] not in SD}
    for ścieżka_2 in sorted({Path(wpis_WARTOŚĆ['nazwa_pliku']) for wpis_WARTOŚĆ in deklaracja_tabela.values()}):
        linia_Lista = ścieżka_2.read_text().splitlines(True); 이어짐 = False
        for INDEKS,wiersz_wejścia in enumerate(linia_Lista):
            전처리 = 이어짐 or bool(re.match(r'\s*#',wiersz_wejścia))
            이어짐 = 전처리 and wiersz_wejścia.rstrip().endswith('\\')
            if 전처리:
                WYSZUKAJ_tabela = nazwa_tabela if re.match(r'\s*#\s*define\b',wiersz_wejścia) or 이어짐 else makro_WARTOŚĆ
                linia_Lista[INDEKS] = 낱말.sub(lambda 맞음: WYSZUKAJ_tabela.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],wiersz_wejścia)
        ścieżka_2.write_text(''.join(linia_Lista))
    # 각 własny TŁUMACZ_źródło 단위에만 연결표를 넣는다. zewnętrzny_WARTOŚĆ 배포본에는 전파하지 않는다.
    for ścieżka_2 in sorted({Path(wpis_WARTOŚĆ['nazwa_pliku']) for wpis_WARTOŚĆ in deklaracja_tabela.values()}):
        if ścieżka_2.suffix not in ('.c','.cpp'):continue
        węzeł_równorzędny_WARTOŚĆ = '../' * len(ścieżka_2.relative_to(Project_korzeń).parts[:-1]) + '명명/기계연결이름.h'
        ścieżka_2.write_text('#include "'+węzeł_równorzędny_WARTOŚĆ+'"\n'+ścieżka_2.read_text())
    (Project_korzeń/'명명/C_nazwa_mapowanie.tsv').write_text('\n'.join(LOG_zapis)+'\n')
    (Project_korzeń/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorować_WARTOŚĆ,ensure_ascii=False,indent=2)+'\n')
    print('zmienić_WARTOŚĆ',len(LOG_zapis)-1,'전처리 재검토',len(ignorować_WARTOŚĆ),'maszyna Połącz',len(połączenie_tabela))

if __name__=='__main__': Wykonaj_polecenie()
