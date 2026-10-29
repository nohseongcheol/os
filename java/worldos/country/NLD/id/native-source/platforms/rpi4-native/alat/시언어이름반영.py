#!/usr/bin/env python3
"""deklarasi_4f4f026b 고유번호와 UTF-8 byte_VALUE 위치로 Asli C 이름을 옮기는 일회성 이행 alat.

eksternal_VALUE 구조체의 멤버, string_VALUE, C 표준 fungsi_VALUE, 이식 규약은 보존한다.
입력은 ubah_VALUE 전 소스에 대한 시언어이름분석.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

Tugas_akar = Path(__file__).resolve().parents[1]

def Jalankan_perintah():
    Analisis_VALUE = json.loads((Tugas_akar/'build/한국어화/시언어분석.json').read_text())
    if Analisis_VALUE['galat']: raise SystemExit('Analisis_VALUE 오류를 먼저 해결해야 합니다.')
    nama_tabel = json.loads((Tugas_akar/'명명/시언어이름.json').read_text())
    SD = set(json.loads((Tugas_akar/'명명/규격이름.json').read_text()))
    deklarasi_tabel = Analisis_VALUE['deklarasi_4f4f026b']
    바꿀선언 = {UNIQUE_VALUE:nama_tabel[entri_VALUE['Nama_2']] for UNIQUE_VALUE,entri_VALUE in deklarasi_tabel.items()
                if entri_VALUE['Nama_2'] in nama_tabel and entri_VALUE['Nama_2'] not in SD}
    koneksi_tabel = {entri_VALUE['Nama_2']:nama_tabel[entri_VALUE['Nama_2']] for entri_VALUE in deklarasi_tabel.values()
              if entri_VALUE.get('Sambung')==4 and entri_VALUE['종류'] in (8,9)
              and entri_VALUE['Nama_2'] in nama_tabel and entri_VALUE['Nama_2'] not in SD}
    # buat AOT C·어셈블리·공개 SDK가 공유하는 바이너리 Sambung 이름만 유지한다.
    kepala_VALUE = ['/* Indonesia sumber_pohon 이름과 기존 mesin Sambung kasus_VALUE. 자동 buat: 명명/시언어이름.json */',
           '#ifndef 자체기계연결이름머리', '#define 자체기계연결이름머리']
    kepala_VALUE += ['#define '+새이름+' '+옛이름 for 옛이름,새이름 in sorted(koneksi_tabel.items())]
    kepala_VALUE += ['#endif','']
    (Tugas_akar/'명명/기계연결이름.h').write_text('\n'.join(kepala_VALUE))
    Perubahan_Daftar = defaultdict(dict)
    for berkas,OFFSET_VALUE,Nama_2,UNIQUE_VALUE in Analisis_VALUE['Referensi']:
        if UNIQUE_VALUE in 바꿀선언:
            Perubahan_Daftar[berkas][OFFSET_VALUE] = (Nama_2,바꿀선언[UNIQUE_VALUE])
    LOG_baris = ['berkas\t원래바이트위치\t이전이름\t한국어이름']
    abaikan_VALUE = []
    for berkas,ubah_VALUE in Perubahan_Daftar.items():
        jalur = Path(berkas); 원본 = jalur.read_bytes(); data = 원본
        for OFFSET_VALUE,(옛이름,새이름) in sorted(ubah_VALUE.items(),reverse=True):
            끝 = OFFSET_VALUE+len(옛이름.encode())
            if 원본[OFFSET_VALUE:끝] != 옛이름.encode():
                abaikan_VALUE.append((str(jalur.relative_to(Tugas_akar)),OFFSET_VALUE,옛이름));continue
            data = data[:OFFSET_VALUE]+새이름.encode()+data[끝:]
            LOG_baris.append('{}\t{}\t{}\t{}'.format(jalur.relative_to(Tugas_akar),OFFSET_VALUE,옛이름,새이름))
        jalur.write_bytes(data)
    # 전처리 매개변수는 AST의 선언으로 나타나지 않는다. 전처리 줄만 보완한다.
    낱말 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makro_VALUE = {entri_VALUE['Nama_2']:nama_tabel[entri_VALUE['Nama_2']] for entri_VALUE in deklarasi_tabel.values()
              if entri_VALUE['종류']==501 and entri_VALUE['Nama_2'] in nama_tabel and entri_VALUE['Nama_2'] not in SD}
    for jalur in sorted({Path(entri_VALUE['berkas']) for entri_VALUE in deklarasi_tabel.values()}):
        baris_Daftar = jalur.read_text().splitlines(True); 이어짐 = False
        for INDEX,baris_masukan in enumerate(baris_Daftar):
            전처리 = 이어짐 or bool(re.match(r'\s*#',baris_masukan))
            이어짐 = 전처리 and baris_masukan.rstrip().endswith('\\')
            if 전처리:
                LOOKUP_tabel = nama_tabel if re.match(r'\s*#\s*define\b',baris_masukan) or 이어짐 else makro_VALUE
                baris_Daftar[INDEX] = 낱말.sub(lambda 맞음: LOOKUP_tabel.get(맞음[0],맞음[0]) if 맞음[0] not in SD else 맞음[0],baris_masukan)
        jalur.write_text(''.join(baris_Daftar))
    # 각 Asli TRANSLATE_sumber 단위에만 연결표를 넣는다. eksternal_VALUE 배포본에는 전파하지 않는다.
    for jalur in sorted({Path(entri_VALUE['berkas']) for entri_VALUE in deklarasi_tabel.values()}):
        if jalur.suffix not in ('.c','.cpp'):continue
        serekan_VALUE = '../' * len(jalur.relative_to(Tugas_akar).parts[:-1]) + '명명/기계연결이름.h'
        jalur.write_text('#include "'+serekan_VALUE+'"\n'+jalur.read_text())
    (Tugas_akar/'명명/시언어이름대응.tsv').write_text('\n'.join(LOG_baris)+'\n')
    (Tugas_akar/'build/한국어화/전처리참조.json').write_text(json.dumps(abaikan_VALUE,ensure_ascii=False,indent=2)+'\n')
    print('ubah_VALUE',len(LOG_baris)-1,'전처리 재검토',len(abaikan_VALUE),'mesin Sambung',len(koneksi_tabel))

if __name__=='__main__': Jalankan_perintah()
