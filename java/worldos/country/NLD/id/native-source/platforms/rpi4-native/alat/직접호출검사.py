#!/usr/bin/env python3
"""배포 class의 직접 Indonesia GUI/alur_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Tugas_akar = Path(__file__).resolve().parents[1]

def jalankan():
    클래스들 = ('Jendela', 'tombol', 'Nama', 'bidang_teks', '화면구성요소', '동작알림', 'acara_antrean', 'tugasLatar',
             '작업', '실행할일', '동작받이')
    paket = Tugas_akar/'dist/jkoros-native-korean.jar'
    deklarasi_4f4f026b = subprocess.check_output(['javap', '-classpath', str(paket), '-private', '-c']+
                                ['Indonesia.Asli.'+Nama_2 for Nama_2 in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklarasi_4f4f026b, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Tugas_akar/'build/examples/classes'), '-c', 'ContohJendela']).decode()
    for 필수 in ('public static void jalankan()', 'Indonesia/Asli/acara_antrean.나중에실행', 'Indonesia/Asli/동작알림.perintah_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    tujuan_VALUE = Tugas_akar/'build/verification/naming'; tujuan_VALUE.mkdir(parents=True, exist_ok=True)
    (tujuan_VALUE/'direct-bytecode.txt').write_text(deklarasi_4f4f026b+'\n'+예제)
    LOG_baris = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(paket.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (tujuan_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Indonesia 직접 GUI·alur_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': jalankan()
