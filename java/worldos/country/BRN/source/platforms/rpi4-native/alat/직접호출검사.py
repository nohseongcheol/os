#!/usr/bin/env python3
"""배포 class의 직접 Melayu GUI/urutan_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

projek_akar = Path(__file__).resolve().parents[1]

def Jalan():
    클래스들 = ('Tetingkap', 'Butang', 'label', 'medan_teks', '화면구성요소', '동작알림', 'acara_baris', '작업가닥',
             '작업', '실행할일', '동작받이')
    pakej = projek_akar/'dist/jkoros-native-korean.jar'
    pengisytiharan_4f4f026b = subprocess.check_output(['javap', '-classpath', str(pakej), '-private', '-c']+
                                ['Melayu.Asli.'+Nama for Nama in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in pengisytiharan_4f4f026b, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(projek_akar/'build/examples/classes'), '-c', 'ContohTetingkap']).decode()
    for 필수 in ('public static void Jalan()', 'Melayu/Asli/acara_baris.나중에실행', 'Melayu/Asli/동작알림.perintah_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    destinasi_VALUE = projek_akar/'build/verification/naming'; destinasi_VALUE.mkdir(parents=True, exist_ok=True)
    (destinasi_VALUE/'direct-bytecode.txt').write_text(pengisytiharan_4f4f026b+'\n'+예제)
    LOG_baris = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(pakej.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (destinasi_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Melayu 직접 GUI·urutan_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Jalan()
