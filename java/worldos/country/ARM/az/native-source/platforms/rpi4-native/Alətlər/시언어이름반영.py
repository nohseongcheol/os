#!/usr/bin/env python3
"""bəyannamə 고유번호와 UTF-8 bayt_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Alətlər.

외부 구조체의 멤버, sətir_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 dəyişdirmək_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_kök = Path(__file__).resolve().parents[1]

def icra_etmək_əmr():
    분석 = json.loads((Project_kök/'build/한국어화/시언어분석.json').read_text())
    if 분석['XƏTA']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    ad_cədvəl = json.loads((Project_kök/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_kök/'명명/규격이름.json').read_text()))
    bəyannamə_cədvəl = 분석['bəyannamə']
    바꿀선언 = {UNIQUE_VALUE:ad_cədvəl[daxiletmə_VALUE['Ad']] for UNIQUE_VALUE,daxiletmə_VALUE in bəyannamə_cədvəl.items()
                if daxiletmə_VALUE['Ad'] in ad_cədvəl and daxiletmə_VALUE['Ad'] not in SD}
    qoşulma_cədvəl = {daxiletmə_VALUE['Ad']:ad_cədvəl[daxiletmə_VALUE['Ad']] for daxiletmə_VALUE in bəyannamə_cədvəl.values()
              if daxiletmə_VALUE.get('Bağlan')==4 and daxiletmə_VALUE['종류'] in (8,9)
              and daxiletmə_VALUE['Ad'] in ad_cədvəl and daxiletmə_VALUE['Ad'] not in SD}
    # yarat AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Bağlan 이름만 유지한다.
    머리 = ['/* 한국어 mənbə_ağac 이름과 기존 maşın Bağlan müqavilə_VALUE. 자동 yarat: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(qoşulma_cədvəl.items())]
    머리 += ['#endif','']
    (Project_kök/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Dəyişikliklər_Siyahı = defaultdict(dict)
    for FAYL,OFFSET_VALUE,Ad,UNIQUE_VALUE in 분석['İstinad']:
        if UNIQUE_VALUE in 바꿀선언:
            Dəyişikliklər_Siyahı[FAYL][OFFSET_VALUE] = (Ad,바꿀선언[UNIQUE_VALUE])
    LOG_yaz = ['FAYL\t원래바이트위치\t이전이름\t한국어이름']
    rədd_etmək_VALUE = []
    for FAYL,dəyişdirmək_VALUE in Dəyişikliklər_Siyahı.items():
        Cığır = Path(FAYL); 원본 = Cığır.read_bytes(); verilənlər = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(dəyişdirmək_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                rədd_etmək_VALUE.append((str(Cığır.relative_to(Project_kök)),OFFSET_VALUE,옛이름));continue
            verilənlər = verilənlər[:OFFSET_VALUE]+새이름.encode()+verilənlər[끝:]
            LOG_yaz.append('{}\t{}\t{}\t{}'.format(Cığır.relative_to(Project_kök),OFFSET_VALUE,옛이름,새이름))
        Cığır.write_bytes(verilənlər)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makros_VALUE = {daxiletmə_VALUE['Ad']:ad_cədvəl[daxiletmə_VALUE['Ad']] for daxiletmə_VALUE in bəyannamə_cədvəl.values()
              if daxiletmə_VALUE['종류']==501 and daxiletmə_VALUE['Ad'] in ad_cədvəl and daxiletmə_VALUE['Ad'] not in SD}
    for Cığır in sorted({Path(daxiletmə_VALUE['FAYL']) for daxiletmə_VALUE in bəyannamə_cədvəl.values()}):
        xətt_Siyahı = Cığır.read_text().splitlines(True); 이어짐 = False
        for INDEX,Giriş in enumerate(xətt_Siyahı):
            전처리 = 이어짐 or bool(re.match(r'\s*#',Giriş))
            이어짐 = 전처리 and Giriş.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_cədvəl = ad_cədvəl if re.match(r'\s*#\s*define\b',Giriş) or 이어짐 else makros_VALUE
                xətt_Siyahı[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_cədvəl.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],Giriş)
        Cığır.write_text(''.join(xətt_Siyahı))
    # 각 자체 TRANSLATE_mənbə 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for Cığır in sorted({Path(daxiletmə_VALUE['FAYL']) for daxiletmə_VALUE in bəyannamə_cədvəl.values()}):
        if Cığır.suffix not in ('.c','.cpp'):continue
        eynisəviyyəli_VALUE = '../' * len(Cığır.relative_to(Project_kök).parts[:-1]) + '명명/기계연결이름.h'
        Cığır.write_text('#include "'+eynisəviyyəli_VALUE+'"\n'+Cığır.read_text())
    (Project_kök/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_yaz)+'\n')
    (Project_kök/'build/한국어화/전처리참조.json').write_text(json.dumps(rədd_etmək_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('dəyişdirmək_VALUE',len(LOG_yaz)-1,'전처리 재검토',len(rədd_etmək_VALUE),'maşın Bağlan',len(qoşulma_cədvəl))

if __name__=='__main__': icra_etmək_əmr()
