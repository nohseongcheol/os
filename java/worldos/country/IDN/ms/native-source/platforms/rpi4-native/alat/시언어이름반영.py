#!/usr/bin/env python3
"""pengisytiharan_4f4f026b 고유번호와 UTF-8 bait_VALUE 위치로 Asli C 이름을 옮기는 일회성 이행 alat.

외부 구조체의 멤버, rentetan_VALUE, C 표준 fungsi_VALUE, 이식 규약은 보존한다.
입력은 ubah_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

projek_akar = Path(__file__).resolve().parents[1]

def laksanakan_perintah():
    Analisis_VALUE = json.loads((projek_akar/'build/한국어화/시언어분석.json').read_text())
    if Analisis_VALUE['RALAT']: raise SystemExit('Analisis_VALUE 오류를 먼저 해결해야 합니다.')
    nama_jadual = json.loads((projek_akar/'명명/시언어이름.json').read_text())
    SD = set(json.loads((projek_akar/'명명/규격이름.json').read_text()))
    pengisytiharan_jadual = Analisis_VALUE['pengisytiharan_4f4f026b']
    바꿀선언 = {UNIQUE_VALUE:nama_jadual[pemasukan_VALUE['Nama']] for UNIQUE_VALUE,pemasukan_VALUE in pengisytiharan_jadual.items()
                if pemasukan_VALUE['Nama'] in nama_jadual and pemasukan_VALUE['Nama'] not in SD}
    hubungan_jadual = {pemasukan_VALUE['Nama']:nama_jadual[pemasukan_VALUE['Nama']] for pemasukan_VALUE in pengisytiharan_jadual.values()
              if pemasukan_VALUE.get('Sambung')==4 and pemasukan_VALUE['종류'] in (8,9)
              and pemasukan_VALUE['Nama'] in nama_jadual and pemasukan_VALUE['Nama'] not in SD}
    # jana AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Sambung 이름만 유지한다.
    머리 = ['/* Melayu sumber_pepohon 이름과 기존 mesin Sambung kes_VALUE. 자동 jana: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    머리 += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(hubungan_jadual.items())]
    머리 += ['#endif','']
    (projek_akar/'명명/기계연결이름.h').write_text('\n'.join(머리))
    Perubahan_Senarai = defaultdict(dict)
    for Fail,Ofset_VALUE,Nama,UNIQUE_VALUE in Analisis_VALUE['Rujukan']:
        if UNIQUE_VALUE in 바꿀선언:
            Perubahan_Senarai[Fail][Ofset_VALUE] = (Nama,바꿀선언[UNIQUE_VALUE])
    LOG_baris = ['Fail\t원래바이트위치\t이전이름\t한국어이름']
    abai_VALUE = []
    for Fail,ubah_VALUE in Perubahan_Senarai.items():
        LALUAN = Path(Fail); 원본 = LALUAN.read_bytes(); data = 원본
        for Ofset_VALUE,(옛이름,새이름) in sorted(ubah_VALUE.items(),reverse=True):
            끝 = Ofset_VALUE+len(옛이름.encode())
            if 원본[Ofset_VALUE:끝] != 옛이름.encode():
                abai_VALUE.append((str(LALUAN.relative_to(projek_akar)),Ofset_VALUE,옛이름));continue
            data = data[:Ofset_VALUE]+새이름.encode()+data[끝:]
            LOG_baris.append('{}\t{}\t{}\t{}'.format(LALUAN.relative_to(projek_akar),Ofset_VALUE,옛이름,새이름))
        LALUAN.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {pemasukan_VALUE['Nama']:nama_jadual[pemasukan_VALUE['Nama']] for pemasukan_VALUE in pengisytiharan_jadual.values()
              if pemasukan_VALUE['종류']==501 and pemasukan_VALUE['Nama'] in nama_jadual and pemasukan_VALUE['Nama'] not in SD}
    for LALUAN in sorted({Path(pemasukan_VALUE['Fail']) for pemasukan_VALUE in pengisytiharan_jadual.values()}):
        baris_Senarai = LALUAN.read_text().splitlines(True); 이어짐 = False
        for INDEX,baris in enumerate(baris_Senarai):
            전처리 = 이어짐 or bool(re.match(r'\s*#',baris))
            이어짐 = 전처리 and baris.rstrip().endswith('\\')
            if 전처리:
                Carian_jadual = nama_jadual if re.match(r'\s*#\s*define\b',baris) or 이어짐 else makro_VALUE
                baris_Senarai[INDEX] = 낱말.sub(lambda 맞음: Carian_jadual.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],baris)
        LALUAN.write_text(''.join(baris_Senarai))
    # 각 Asli Terjemah_sumber 단위에만 연결표를 넣는다. 외부 배포본에는 전파하지 않는다.
    for LALUAN in sorted({Path(pemasukan_VALUE['Fail']) for pemasukan_VALUE in pengisytiharan_jadual.values()}):
        if LALUAN.suffix not in ('.c','.cpp'):continue
        rakan_VALUE = '../' * len(LALUAN.relative_to(projek_akar).parts[:-1]) + '명명/기계연결이름.h'
        LALUAN.write_text('#include "'+rakan_VALUE+'"\n'+LALUAN.read_text())
    (projek_akar/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_baris)+'\n')
    (projek_akar/'build/한국어화/전처리참조.json').write_text(json.dumps(abai_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('ubah_VALUE',len(LOG_baris)-1,'전처리 재검토',len(abai_VALUE),'mesin Sambung',len(hubungan_jadual))

if __name__=='__main__': laksanakan_perintah()
