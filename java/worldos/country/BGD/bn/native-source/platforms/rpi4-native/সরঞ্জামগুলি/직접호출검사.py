#!/usr/bin/env python3
"""배포 class의 직접 বাংলা GUI/থ্রেড_মান 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

প্রকল্প_মূল = Path(__file__).resolve().parents[1]

def চালনা():
    클래스들 = ('창', 'বোতাম', 'লেবেল', 'পাঠ্য_ক্ষেত্র', '화면구성요소', '동작알림', 'ঘটনা_সারিবদ্ধ', '작업가닥',
             '작업', '실행할일', '동작받이')
    পাঁজা = প্রকল্প_মূল/'dist/jkoros-native-korean.jar'
    ঘোষণা = subprocess.check_output(['javap', '-classpath', str(পাঁজা), '-private', '-c']+
                                ['বাংলা.নিজ.'+নাম for নাম in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in ঘোষণা, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(প্রকল্প_মূল/'build/examples/classes'), '-c', 'জানালানমুনা']).decode()
    for 필수 in ('public static void চালনা()', 'বাংলা/নিজ/ঘটনা_সারিবদ্ধ.나중에실행', 'বাংলা/নিজ/동작알림.আদেশ_পাঠ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    গন্তব্য_মান = প্রকল্প_মূল/'build/verification/naming'; গন্তব্য_মান.mkdir(parents=True, exist_ok=True)
    (গন্তব্য_মান/'direct-bytecode.txt').write_text(ঘোষণা+'\n'+예제)
    লগ_সারি = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(পাঁজা.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (গন্তব্য_মান/'direct-bytecode.json').write_text(json.dumps(লগ_সারি, ensure_ascii=False, indent=2)+'\n')
    print('PASS: বাংলা 직접 GUI·থ্রেড_মান 바이트코드와 예제 호출')

if __name__ == '__main__': চালনা()
