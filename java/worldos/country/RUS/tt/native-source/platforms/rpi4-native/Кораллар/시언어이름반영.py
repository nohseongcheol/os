#!/usr/bin/env python3
"""선언 고유번호와 UTF-8 байт_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Кораллар.

외부 구조체의 멤버, юл_VALUE_6ca8363c, C 표준 ФУНКЦИЯ_VALUE, 이식 규약은 보존한다.
입력은 үзгәртү_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]

def үтәргә_команда():
    분석 = json.loads((экранга_җибәрү_тамыр/'build/한국어화/시언어분석.json').read_text())
    if 분석['Хата']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    исем_таблица = json.loads((экранга_җибәрү_тамыр/'명명/시언어이름.json').read_text())
    SD = set(json.loads((экранга_җибәрү_тамыр/'명명/규격이름.json').read_text()))
    선언표 = 분석['선언']
    바꿀선언 = {UNIQUE_VALUE:исем_таблица[кертү_VALUE['исем']] for UNIQUE_VALUE,кертү_VALUE in 선언표.items()
                if кертү_VALUE['исем'] in исем_таблица and кертү_VALUE['исем'] not in SD}
    тоташу_таблица = {кертү_VALUE['исем']:исем_таблица[кертү_VALUE['исем']] for кертү_VALUE in 선언표.values()
              if кертү_VALUE.get('ялгау')==4 and кертү_VALUE['종류'] in (8,9)
              and кертү_VALUE['исем'] in исем_таблица and кертү_VALUE['исем'] not in SD}
    # булдыру AOT C·어셈블리·공개 SDK가 공유하는 바이너리 ялгау 이름만 유지한다.
    머리 = ['/* Татарча чыганак_агач 이름과 기존 машина ялгау бирем_VALUE_102996da. 자동 булдыру: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(тоташу_таблица.items())]
    머리 += ['#endif','']
    (экранга_җибәрү_тамыр/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Үзгәрешләр_Исемлек = defaultdict(dict)
    for Birem,OFFSET_VALUE,исем,UNIQUE_VALUE in 분석['Белешмәлекләр']:
        if UNIQUE_VALUE in 바꿀선언:
            Үзгәрешләр_Исемлек[Birem][OFFSET_VALUE] = (исем,바꿀선언[UNIQUE_VALUE])
    LOG_юл = ['Birem\t원래바이트위치\t이전이름\t한국어이름']
    игътибар_итмәү_VALUE = []
    for Birem,үзгәртү_VALUE in Үзгәрешләр_Исемлек.items():
        Yul = Path(Birem); 원본 = Yul.read_bytes(); мәгълүмат = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(үзгәртү_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                игътибар_итмәү_VALUE.append((str(Yul.relative_to(экранга_җибәрү_тамыр)),OFFSET_VALUE,옛이름));continue
            мәгълүмат = мәгълүмат[:OFFSET_VALUE]+새이름.encode()+мәгълүмат[끝:]
            LOG_юл.append('{}\t{}\t{}\t{}'.format(Yul.relative_to(экранга_җибәрү_тамыр),OFFSET_VALUE,옛이름,새이름))
        Yul.write_bytes(мәгълүмат)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    макрос_VALUE = {кертү_VALUE['исем']:исем_таблица[кертү_VALUE['исем']] for кертү_VALUE in 선언표.values()
              if кертү_VALUE['종류']==501 and кертү_VALUE['исем'] in исем_таблица and кертү_VALUE['исем'] not in SD}
    for Yul in sorted({Path(кертү_VALUE['Birem']) for кертү_VALUE in 선언표.values()}):
        юл_Исемлек = Yul.read_text().splitlines(True); 이어짐 = False
        for INDEX,юл in enumerate(юл_Исемлек):
            전처리 = 이어짐 or bool(re.match(r'\s*#',юл))
            이어짐 = 전처리 and юл.rstrip().endswith('\\')
            if 전처리:
                Эзләү_таблица = исем_таблица if re.match(r'\s*#\s*define\b',юл) or 이어짐 else макрос_VALUE
                юл_Исемлек[INDEX] = 낱말.sub(lambda 맞음: Эзләү_таблица.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],юл)
        Yul.write_text(''.join(юл_Исемлек))
    # 각 자체 TRANSLATE_чыганак 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Yul in sorted({Path(кертү_VALUE['Birem']) for кертү_VALUE in 선언표.values()}):
        if Yul.suffix not in ('.c','.cpp'):continue
        тиңдәш_VALUE = '../' * len(Yul.relative_to(экранга_җибәрү_тамыр).parts[:-1]) + '명명/기계연결이름.h'
        Yul.write_text('#include "'+тиңдәш_VALUE+'"\n'+Yul.read_text())
    (экранга_җибәрү_тамыр/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_юл)+'\n')
    (экранга_җибәрү_тамыр/'build/한국어화/전처리참조.json').write_text(json.dumps(игътибар_итмәү_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('үзгәртү_VALUE',len(LOG_юл)-1,'전처리 재검토',len(игътибар_итмәү_VALUE),'машина ялгау',len(тоташу_таблица))

if __name__=='__main__': үтәргә_команда()
