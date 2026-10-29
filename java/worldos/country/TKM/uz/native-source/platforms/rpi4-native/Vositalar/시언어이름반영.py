#!/usr/bin/env python3
"""e_lon_qilish 고유번호와 UTF-8 bayt_VALUE 위치로 자체 C 이름을 옮기는 일회성 이행 Vositalar.

외부 구조체의 멤버, satr_VALUE, C 표준 FUNCTION_VALUE, 이식 규약은 보존한다.
입력은 o_zgartirmoq_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Project_ildiz = Path(__file__).resolve().parents[1]

def bajarmoq_buyruq():
    분석 = json.loads((Project_ildiz/'build/한국어화/시언어분석.json').read_text())
    if 분석['Xato']: raise SystemExit('분석 오류를 먼저 해결해야 합니다.')
    nom_jadval = json.loads((Project_ildiz/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Project_ildiz/'명명/규격이름.json').read_text()))
    e_lon_qilish_jadval = 분석['e_lon_qilish']
    바꿀선언 = {UNIQUE_VALUE:nom_jadval[kiritish_VALUE['Nomi']] for UNIQUE_VALUE,kiritish_VALUE in e_lon_qilish_jadval.items()
                if kiritish_VALUE['Nomi'] in nom_jadval and kiritish_VALUE['Nomi'] not in SD}
    aloqa_jadval = {kiritish_VALUE['Nomi']:nom_jadval[kiritish_VALUE['Nomi']] for kiritish_VALUE in e_lon_qilish_jadval.values()
              if kiritish_VALUE.get('Ulanish')==4 and kiritish_VALUE['종류'] in (8,9)
              and kiritish_VALUE['Nomi'] in nom_jadval and kiritish_VALUE['Nomi'] not in SD}
    # generatsiiyalash AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Ulanish 이름만 유지한다.
    머리 = ['/* 한국어 manba_daraxt 이름과 기존 기계 Ulanish murojaat_VALUE. 자동 generatsiiyalash: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(aloqa_jadval.items())]
    머리 += ['#endif','']
    (Project_ildiz/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Tahrirlar_Ro_yxat = defaultdict(dict)
    for Fayl,OFFSET_VALUE,Nomi,UNIQUE_VALUE in 분석['Ma_lumotnomalar']:
        if UNIQUE_VALUE in 바꿀선언:
            Tahrirlar_Ro_yxat[Fayl][OFFSET_VALUE] = (Nomi,바꿀선언[UNIQUE_VALUE])
    LOG_satr = ['Fayl\t원래바이트위치\t이전이름\t한국어이름']
    o_tkazib_yubormoq_VALUE = []
    for Fayl,o_zgartirmoq_VALUE in Tahrirlar_Ro_yxat.items():
        yo_l = Path(Fayl); 원본 = yo_l.read_bytes(); ma_lumotlar = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(o_zgartirmoq_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                o_tkazib_yubormoq_VALUE.append((str(yo_l.relative_to(Project_ildiz)),OFFSET_VALUE,옛이름));continue
            ma_lumotlar = ma_lumotlar[:OFFSET_VALUE]+새이름.encode()+ma_lumotlar[끝:]
            LOG_satr.append('{}\t{}\t{}\t{}'.format(yo_l.relative_to(Project_ildiz),OFFSET_VALUE,옛이름,새이름))
        yo_l.write_bytes(ma_lumotlar)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {kiritish_VALUE['Nomi']:nom_jadval[kiritish_VALUE['Nomi']] for kiritish_VALUE in e_lon_qilish_jadval.values()
              if kiritish_VALUE['종류']==501 and kiritish_VALUE['Nomi'] in nom_jadval and kiritish_VALUE['Nomi'] not in SD}
    for yo_l in sorted({Path(kiritish_VALUE['Fayl']) for kiritish_VALUE in e_lon_qilish_jadval.values()}):
        satr_Ro_yxat = yo_l.read_text().splitlines(True); 이어짐 = False
        for INDEX,satr in enumerate(satr_Ro_yxat):
            전처리 = 이어짐 or bool(re.match(r'\s*#',satr))
            이어짐 = 전처리 and satr.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_jadval = nom_jadval if re.match(r'\s*#\s*define\b',satr) or 이어짐 else makro_VALUE
                satr_Ro_yxat[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_jadval.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],satr)
        yo_l.write_text(''.join(satr_Ro_yxat))
    # 각 자체 Tarjima_manba 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for yo_l in sorted({Path(kiritish_VALUE['Fayl']) for kiritish_VALUE in e_lon_qilish_jadval.values()}):
        if yo_l.suffix not in ('.c','.cpp'):continue
        bir_rangli_VALUE = '../' * len(yo_l.relative_to(Project_ildiz).parts[:-1]) + '명명/기계연결이름.h'
        yo_l.write_text('#include "'+bir_rangli_VALUE+'"\n'+yo_l.read_text())
    (Project_ildiz/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_satr)+'\n')
    (Project_ildiz/'build/한국어화/전처리참조.json').write_text(json.dumps(o_tkazib_yubormoq_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('o_zgartirmoq_VALUE',len(LOG_satr)-1,'전처리 재검토',len(o_tkazib_yubormoq_VALUE),'기계 Ulanish',len(aloqa_jadval))

if __name__=='__main__': bajarmoq_buyruq()
