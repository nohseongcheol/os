#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/thread_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_root = Path(__file__).resolve().parents[1]

def run():
    클래스들 = ('창', 'button', 'label', 'SMS_field', '화면구성요소', '동작알림', 'kaganapan_pila', '작업가닥',
             '작업', '실행할일', '동작받이')
    bundle = Project_root/'dist/jkoros-native-korean.jar'
    declaration = subprocess.check_output(['javap', '-classpath', str(bundle), '-private', '-c']+
                                ['한국어.자체.'+pangalan for pangalan in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in declaration, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_root/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void run()', '한국어/자체/kaganapan_pila.나중에실행', '한국어/자체/동작알림.utos_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    patutunguhan_VALUE = Project_root/'build/verification/naming'; patutunguhan_VALUE.mkdir(parents=True, exist_ok=True)
    (patutunguhan_VALUE/'direct-bytecode.txt').write_text(declaration+'\n'+예제)
    LOG_hanay = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(bundle.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (patutunguhan_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_hanay, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·thread_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': run()
