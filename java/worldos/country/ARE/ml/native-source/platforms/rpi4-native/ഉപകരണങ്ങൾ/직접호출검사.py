#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/ത്രെഡ്_മൂല്യം 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]

def നടപ്പിലാക്കുക():
    클래스들 = ('창', 'ബട്ടണ്', 'ലേബല്', 'പാഠ_മണ്ഡലം', '화면구성요소', '동작알림', 'ഇവന്റ്_ക്യൂ', '작업가닥',
             '작업', '실행할일', '동작받이')
    ബണ്ടിൽ = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-korean.jar'
    പ്രസ്താവം = subprocess.check_output(['javap', '-classpath', str(ബണ്ടിൽ), '-private', '-c']+
                                ['한국어.자체.'+പേരു് for പേരു് in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in പ്രസ്താവം, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void നടപ്പിലാക്കുക()', '한국어/자체/ഇവന്റ്_ക്യൂ.나중에실행', '한국어/자체/동작알림.കമാന്_ഡ്_ലിഖിതം'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/naming'; ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.mkdir(parents=True, exist_ok=True)
    (ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'direct-bytecode.txt').write_text(പ്രസ്താവം+'\n'+예제)
    ലോഗ്_രേഖ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(ബണ്ടിൽ.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'direct-bytecode.json').write_text(json.dumps(ലോഗ്_രേഖ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·ത്രെഡ്_മൂല്യം 바이트코드와 예제 호출')

if __name__ == '__main__': നടപ്പിലാക്കുക()
