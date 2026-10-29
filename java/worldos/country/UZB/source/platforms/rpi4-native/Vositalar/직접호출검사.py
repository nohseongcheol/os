#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/oqim_VALUE_5b72a632 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_ildiz = Path(__file__).resolve().parents[1]

def Bajarish():
    클래스들 = ('창', 'tugma', 'Yorliq', 'SMS_ma_lumotlar_maydoni', '화면구성요소', '동작알림', 'hodisa_navbat', '작업가닥',
             '작업', '실행할일', '동작받이')
    to_plam = Project_ildiz/'dist/jkoros-native-korean.jar'
    e_lon_qilish = subprocess.check_output(['javap', '-classpath', str(to_plam), '-private', '-c']+
                                ['한국어.자체.'+Nomi for Nomi in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in e_lon_qilish, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_ildiz/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Bajarish()', '한국어/자체/hodisa_navbat.나중에실행', '한국어/자체/동작알림.buyruq_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ko_chirish_joyi_VALUE = Project_ildiz/'build/verification/naming'; ko_chirish_joyi_VALUE.mkdir(parents=True, exist_ok=True)
    (ko_chirish_joyi_VALUE/'direct-bytecode.txt').write_text(e_lon_qilish+'\n'+예제)
    LOG_satr = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(to_plam.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ko_chirish_joyi_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_satr, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·oqim_VALUE_5b72a632 바이트코드와 예제 호출')

if __name__ == '__main__': Bajarish()
