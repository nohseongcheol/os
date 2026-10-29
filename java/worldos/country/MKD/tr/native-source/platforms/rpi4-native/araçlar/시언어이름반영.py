#!/usr/bin/env python3
"""bildirim 고유번호와 UTF-8 bayt_değer 위치로 Öz C 이름을 옮기는 일회성 이행 araçlar.

dış_değer 구조체의 멤버, dize_değer, C 표준 işlev_değer, 이식 규약은 보존한다.
입력은 değiştirmek_değer 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

işlem_kök = Path(__file__).resolve().parents[1]

def yürütmek_komut():
    Analiz_değer = json.loads((işlem_kök/'build/한국어화/시언어분석.json').read_text())
    if Analiz_değer['hata']: raise SystemExit('Analiz_değer 오류를 먼저 해결해야 합니다.')
    ad_tablo = json.loads((işlem_kök/'명명/시언어이름.json').read_text())
    SD = set(json.loads((işlem_kök/'명명/규격이름.json').read_text()))
    bildirim_tablo = Analiz_değer['bildirim']
    바꿀선언 = {BENZERSİZ_değer:ad_tablo[girdi_değer['İsim']] for BENZERSİZ_değer,girdi_değer in bildirim_tablo.items()
                if girdi_değer['İsim'] in ad_tablo and girdi_değer['İsim'] not in SD}
    cxn_tablo = {girdi_değer['İsim']:ad_tablo[girdi_değer['İsim']] for girdi_değer in bildirim_tablo.values()
              if girdi_değer.get('Bağlan')==4 and girdi_değer['Tip_değer'] in (8,9)
              and girdi_değer['İsim'] in ad_tablo and girdi_değer['İsim'] not in SD}
    # oluşturmak AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Bağlan 이름만 유지한다.
    머리 = ['/* Türkçe kaynak_ağaç 이름과 기존 makine Bağlan sözleşme_değeri. 자동 oluşturmak: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(cxn_tablo.items())]
    머리 += ['#endif','']
    (işlem_kök/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Değişiklikler_Liste = defaultdict(dict)
    for dosya,Ofset_değer,İsim,BENZERSİZ_değer in Analiz_değer['Başvuru']:
        if BENZERSİZ_değer in 바꿀선언:
            Değişiklikler_Liste[dosya][Ofset_değer] = (İsim,바꿀선언[BENZERSİZ_değer])
    LOG_KAYIT = ['dosya\t원래바이트위치\t이전이름\t한국어이름']
    yoksaymak_değer = []
    for dosya,değiştirmek_değer in Değişiklikler_Liste.items():
        yol = Path(dosya); 원본 = yol.read_bytes(); veri = 원본
        for Ofset_değer,(옛이름,새이름) in sorted(değiştirmek_değer.items(),reverse=True):
            끝 = Ofset_değer+len(옛이름.encode())
            if 원본[Ofset_değer:끝] != 옛이름.encode():
                yoksaymak_değer.append((str(yol.relative_to(işlem_kök)),Ofset_değer,옛이름));continue
            veri = veri[:Ofset_değer]+새이름.encode()+veri[끝:]
            LOG_KAYIT.append('{}\t{}\t{}\t{}'.format(yol.relative_to(işlem_kök),Ofset_değer,옛이름,새이름))
        yol.write_bytes(veri)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_değer = {girdi_değer['İsim']:ad_tablo[girdi_değer['İsim']] for girdi_değer in bildirim_tablo.values()
              if girdi_değer['Tip_değer']==501 and girdi_değer['İsim'] in ad_tablo and girdi_değer['İsim'] not in SD}
    for yol in sorted({Path(girdi_değer['dosya']) for girdi_değer in bildirim_tablo.values()}):
        hat_Liste = yol.read_text().splitlines(True); 이어짐 = False
        for Dizin,girdi_satırı in enumerate(hat_Liste):
            전처리 = 이어짐 or bool(re.match(r'\s*#',girdi_satırı))
            이어짐 = 전처리 and girdi_satırı.rstrip().endswith('\\')
            if 전처리:
                arama_tablosu = ad_tablo if re.match(r'\s*#\s*define\b',girdi_satırı) or 이어짐 else makro_değer
                hat_Liste[Dizin] = 낱말.sub(lambda 맞음: arama_tablosu.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],girdi_satırı)
        yol.write_text(''.join(hat_Liste))
    # 각 Öz çevir_kaynak 단위에만 연결표를 넣는다. dış_değer 배포본에는 전파하지 않는다.
    for yol in sorted({Path(girdi_değer['dosya']) for girdi_değer in bildirim_tablo.values()}):
        if yol.suffix not in ('.c','.cpp'):continue
        eş_değer = '../' * len(yol.relative_to(işlem_kök).parts[:-1]) + '명명/기계연결이름.h'
        yol.write_text('#include "'+eş_değer+'"\n'+yol.read_text())
    (işlem_kök/'명명/C_ad_eşleme.tsv').write_text('\n'.join(LOG_KAYIT)+'\n')
    (işlem_kök/'build/한국어화/전처리참조.json').write_text(json.dumps(yoksaymak_değer,ensure_ascii=False,indent=2)+'\n')
    print('değiştirmek_değer',len(LOG_KAYIT)-1,'전처리 재검토',len(yoksaymak_değer),'makine Bağlan',len(cxn_tablo))

if __name__=='__main__': yürütmek_komut()
