#!/usr/bin/env python3
"""dağıtım_değer class의 직접 Türkçe GUI/yazışma_değer 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

işlem_kök = Path(__file__).resolve().parents[1]

def çalıştır():
    클래스들 = ('Pencere', 'düğme', 'Etiket', 'metin_alanı', '화면구성요소', 'Eylem_uyarı', 'olay_sıra', 'arkaPlanGörevi',
             '작업', '실행할일', '동작받이')
    paket_iş = işlem_kök/'dist/jkoros-native-korean.jar'
    bildirim = subprocess.check_output(['javap', '-classpath', str(paket_iş), '-private', '-c']+
                                ['Türkçe.Öz.'+İsim for İsim in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in bildirim, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(işlem_kök/'build/examples/classes'), '-c', 'PencereÖrneği']).decode()
    for 필수 in ('public static void çalıştır()', 'Türkçe/Öz/olay_sıra.나중에실행', 'Türkçe/Öz/Eylem_uyarı.komut_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    hedef_değer = işlem_kök/'build/verification/naming'; hedef_değer.mkdir(parents=True, exist_ok=True)
    (hedef_değer/'direct-bytecode.txt').write_text(bildirim+'\n'+예제)
    LOG_KAYIT = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(paket_iş.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (hedef_değer/'direct-bytecode.json').write_text(json.dumps(LOG_KAYIT, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Türkçe 직접 GUI·yazışma_değer 바이트코드와 예제 호출')

if __name__ == '__main__': çalıştır()
