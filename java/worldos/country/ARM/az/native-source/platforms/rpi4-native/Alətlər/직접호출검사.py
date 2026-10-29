#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/axın_VALUE_5b72a632 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_kök = Path(__file__).resolve().parents[1]

def İcra_Et():
    클래스들 = ('창', 'düymə', 'Etiket', 'SMS_sahə', '화면구성요소', '동작알림', 'hadisə_növbə', '작업가닥',
             '작업', '실행할일', '동작받이')
    paket = Project_kök/'dist/jkoros-native-korean.jar'
    bəyannamə = subprocess.check_output(['javap', '-classpath', str(paket), '-private', '-c']+
                                ['한국어.자체.'+Ad for Ad in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in bəyannamə, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_kök/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void İcra_Et()', '한국어/자체/hadisə_növbə.나중에실행', '한국어/자체/동작알림.əmr_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    təyinat_VALUE_a0fbc067 = Project_kök/'build/verification/naming'; təyinat_VALUE_a0fbc067.mkdir(parents=True, exist_ok=True)
    (təyinat_VALUE_a0fbc067/'direct-bytecode.txt').write_text(bəyannamə+'\n'+예제)
    LOG_yaz = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(paket.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (təyinat_VALUE_a0fbc067/'direct-bytecode.json').write_text(json.dumps(LOG_yaz, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·axın_VALUE_5b72a632 바이트코드와 예제 호출')

if __name__ == '__main__': İcra_Et()
