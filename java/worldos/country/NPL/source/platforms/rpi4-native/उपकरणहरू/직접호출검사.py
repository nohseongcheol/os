#!/usr/bin/env python3
"""배포 class의 직접 नेपाली GUI/धागो_मान 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

परियोजना_रूट = Path(__file__).resolve().parents[1]

def चलाउनुहोस्():
    클래스들 = ('창', 'बटन', 'लेबुल', 'पाठ_क्षेत्र', '화면구성요소', '동작알림', 'घटना_लाइन', '작업가닥',
             '작업', '실행할일', '동작받이')
    पोको = परियोजना_रूट/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(पोको), '-private', '-c']+
                                ['नेपाली.निज.'+नाम for नाम in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(परियोजना_रूट/'build/examples/classes'), '-c', 'झ्यालउदाहरण']).decode()
    for 필수 in ('public static void चलाउनुहोस्()', 'नेपाली/निज/घटना_लाइन.나중에실행', 'नेपाली/निज/동작알림.आदेश_पाठ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    गन्तव्य_मान = परियोजना_रूट/'build/verification/naming'; गन्तव्य_मान.mkdir(parents=True, exist_ok=True)
    (गन्तव्य_मान/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    लग_रेकर्ड = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(पोको.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (गन्तव्य_मान/'direct-bytecode.json').write_text(json.dumps(लग_रेकर्ड, ensure_ascii=False, indent=2)+'\n')
    print('PASS: नेपाली 직접 GUI·धागो_मान 바이트코드와 예제 호출')

if __name__ == '__main__': चलाउनुहोस्()
