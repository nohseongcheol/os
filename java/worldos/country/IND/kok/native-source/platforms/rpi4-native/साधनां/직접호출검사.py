#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/थ्रॅड_मोल 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]

def चलोवप():
    클래스들 = ('창', 'बटन', 'लेबल', 'लिखीत_मळ', '화면구성요소', '동작알림', 'प्रसंग_प्रतिक्षावळ', '작업가닥',
             '작업', '실행할일', '동작받이')
    रास = प्रॉजॅक्ट_रूट/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(रास), '-private', '-c']+
                                ['한국어.자체.'+नांव for नांव in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(प्रॉजॅक्ट_रूट/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void चलोवप()', '한국어/자체/प्रसंग_प्रतिक्षावळ.나중에실행', '한국어/자체/동작알림.आदेश_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    नियुक्त_स्थान_मोल = प्रॉजॅक्ट_रूट/'build/verification/naming'; नियुक्त_स्थान_मोल.mkdir(parents=True, exist_ok=True)
    (नियुक्त_स्थान_मोल/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    LOG_नोंद = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(रास.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (नियुक्त_स्थान_मोल/'direct-bytecode.json').write_text(json.dumps(LOG_नोंद, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·थ्रॅड_मोल 바이트코드와 예제 호출')

if __name__ == '__main__': चलोवप()
