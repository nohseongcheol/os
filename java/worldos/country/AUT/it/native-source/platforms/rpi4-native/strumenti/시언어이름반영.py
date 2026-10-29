#!/usr/bin/env python3
"""dichiarazione 고유번호와 UTF-8 byte_VALORE 위치로 nativo C 이름을 옮기는 일회성 이행 strumenti.

esterno_VALORE 구조체의 멤버, stringa_VALORE, C 표준 FUNZIONE_VALORE, 이식 규약은 보존한다.
입력은 cambiare_VALORE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

azione_radice = Path(__file__).resolve().parents[1]

def Esegui_comando():
    Analizza_VALORE = json.loads((azione_radice/'build/한국어화/시언어분석.json').read_text())
    if Analizza_VALORE['errore']: raise SystemExit('Analizza_VALORE 오류를 먼저 해결해야 합니다.')
    nome_tabella = json.loads((azione_radice/'명명/시언어이름.json').read_text())
    SD = set(json.loads((azione_radice/'명명/규격이름.json').read_text()))
    dichiarazione_tabella = Analizza_VALORE['dichiarazione']
    바꿀선언 = {UNICI_VALORE:nome_tabella[voce_VALORE['Nome']] for UNICI_VALORE,voce_VALORE in dichiarazione_tabella.items()
                if voce_VALORE['Nome'] in nome_tabella and voce_VALORE['Nome'] not in SD}
    connessione_tabella = {voce_VALORE['Nome']:nome_tabella[voce_VALORE['Nome']] for voce_VALORE in dichiarazione_tabella.values()
              if voce_VALORE.get('Connetti')==4 and voce_VALORE['Kind_VALORE'] in (8,9)
              and voce_VALORE['Nome'] in nome_tabella and voce_VALORE['Nome'] not in SD}
    # generare AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Connetti 이름만 유지한다.
    intestazione_VALORE = ['/* Italiano fonte_albero 이름과 기존 computer Connetti valore_di_contratto. 자동 generare: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    intestazione_VALORE += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(connessione_tabella.items())]
    intestazione_VALORE += ['#endif','']
    (azione_radice/'명명/기계연결이름.h').write_text('\n'.join(intestazione_VALORE))
    Modifiche_elenco = defaultdict(dict)
    for file,SCARTO_VALORE,Nome,UNICI_VALORE in Analizza_VALORE['fonti']:
        if UNICI_VALORE in 바꿀선언:
            Modifiche_elenco[file][SCARTO_VALORE] = (Nome,바꿀선언[UNICI_VALORE])
    LOG_riga = ['file\t원래바이트위치\t이전이름\t한국어이름']
    rifiuta_VALORE = []
    for file,cambiare_VALORE in Modifiche_elenco.items():
        percorso = Path(file); 원본 = percorso.read_bytes(); dati = 원본
        for SCARTO_VALORE,(옛이름,새이름) in sorted(cambiare_VALORE.items(),reverse=True):
            끝 = SCARTO_VALORE+len(옛이름.encode())
            if 원본[SCARTO_VALORE:끝] != 옛이름.encode():
                rifiuta_VALORE.append((str(percorso.relative_to(azione_radice)),SCARTO_VALORE,옛이름));continue
            dati = dati[:SCARTO_VALORE]+새이름.encode()+dati[끝:]
            LOG_riga.append('{}\t{}\t{}\t{}'.format(percorso.relative_to(azione_radice),SCARTO_VALORE,옛이름,새이름))
        percorso.write_bytes(dati)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macro_VALORE = {voce_VALORE['Nome']:nome_tabella[voce_VALORE['Nome']] for voce_VALORE in dichiarazione_tabella.values()
              if voce_VALORE['Kind_VALORE']==501 and voce_VALORE['Nome'] in nome_tabella and voce_VALORE['Nome'] not in SD}
    for percorso in sorted({Path(voce_VALORE['file']) for voce_VALORE in dichiarazione_tabella.values()}):
        riga_elenco = percorso.read_text().splitlines(True); 이어짐 = False
        for INDICE,riga_di_ingresso in enumerate(riga_elenco):
            전처리 = 이어짐 or bool(re.match(r'\s*#',riga_di_ingresso))
            이어짐 = 전처리 and riga_di_ingresso.rstrip().endswith('\\')
            if 전처리:
                tabella_di_ricerca = nome_tabella if re.match(r'\s*#\s*define\b',riga_di_ingresso) or 이어짐 else macro_VALORE
                riga_elenco[INDICE] = 낱말.sub(lambda 맞음: tabella_di_ricerca.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],riga_di_ingresso)
        percorso.write_text(''.join(riga_elenco))
    # 각 nativo TRADUCI_fonte 단위에만 연결표를 넣는다. esterno_VALORE 배포본에는 전파하지 않는다.
    for percorso in sorted({Path(voce_VALORE['file']) for voce_VALORE in dichiarazione_tabella.values()}):
        if percorso.suffix not in ('.c','.cpp'):continue
        peer_VALORE = '../' * len(percorso.relative_to(azione_radice).parts[:-1]) + '명명/기계연결이름.h'
        percorso.write_text('#include "'+peer_VALORE+'"\n'+percorso.read_text())
    (azione_radice/'명명/C_nome_mapping.tsv').write_text('\n'.join(LOG_riga)+'\n')
    (azione_radice/'build/한국어화/전처리참조.json').write_text(json.dumps(rifiuta_VALORE,ensure_ascii=False,indent=2)+'\n')
    print('cambiare_VALORE',len(LOG_riga)-1,'전처리 재검토',len(rifiuta_VALORE),'computer Connetti',len(connessione_tabella))

if __name__=='__main__': Esegui_comando()
