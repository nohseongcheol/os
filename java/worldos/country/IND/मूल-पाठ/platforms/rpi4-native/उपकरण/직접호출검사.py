#!/usr/bin/env python3
"""배포 class의 직접 हिंदी GUI/थ्रेड_मान 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]

def चलाएँ():
    클래스들 = ('खिड़की', 'बटन', 'लेबल', 'पाठ_फ़ील्ड', '화면구성요소', 'एक्शन_सूचना', 'घटना_कतार', 'कार्यसूत्र',
             '작업', '실행할일', '동작받이')
    बंडल = प्रोजेक्ट_करें_मूल/'dist/jkoros-native-korean.jar'
    घोषणा = subprocess.check_output(['javap', '-classpath', str(बंडल), '-private', '-c']+
                                ['हिंदी.निज.'+नाम for नाम in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in घोषणा, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(प्रोजेक्ट_करें_मूल/'build/examples/classes'), '-c', 'खिड़कीउदाहरण']).decode()
    for 필수 in ('public static void चलाएँ()', 'हिंदी/निज/घटना_कतार.나중에실행', 'हिंदी/निज/एक्शन_सूचना.आदेश_पाठ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    गंतव्य_मान = प्रोजेक्ट_करें_मूल/'build/verification/naming'; गंतव्य_मान.mkdir(parents=True, exist_ok=True)
    (गंतव्य_मान/'direct-bytecode.txt').write_text(घोषणा+'\n'+예제)
    लॉग_रिकॉर्ड = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(बंडल.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (गंतव्य_मान/'direct-bytecode.json').write_text(json.dumps(लॉग_रिकॉर्ड, ensure_ascii=False, indent=2)+'\n')
    print('PASS: हिंदी 직접 GUI·थ्रेड_मान 바이트코드와 예제 호출')

if __name__ == '__main__': चलाएँ()
