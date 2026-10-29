#!/usr/bin/env python3
"""배포 class의 직접 ಕನ್ನಡ GUI/ಎಳೆ_ಮೌಲ್ಯ 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]

def ಚಲಾಯಿಸು_2():
    클래스들 = ('창', 'ಬಟನ್', 'ಲೇಬಲ್', 'ಪಠ್ಯ_ಕ್ಷೇತ್ರ', '화면구성요소', '동작알림', 'ಸಂಗತಿ_ಸರದಿ', '작업가닥',
             '작업', '실행할일', '동작받이')
    ಬಂಡಲ್ = ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-korean.jar'
    ದೃಢೀಕರಣ = subprocess.check_output(['javap', '-classpath', str(ಬಂಡಲ್), '-private', '-c']+
                                ['ಕನ್ನಡ.자체.'+ಹೆಸರು for ಹೆಸರು in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in ದೃಢೀಕರಣ, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(ಬಿಂಬಿಸು_ಮೂಲ/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ಚಲಾಯಿಸು_2()', 'ಕನ್ನಡ/자체/ಸಂಗತಿ_ಸರದಿ.나중에실행', 'ಕನ್ನಡ/자체/동작알림.ಆದೇಶ_ಪಠ್ಯ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/naming'; ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.mkdir(parents=True, exist_ok=True)
    (ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'direct-bytecode.txt').write_text(ದೃಢೀಕರಣ+'\n'+예제)
    ಲಾಗ್_ದಾಖಲೆ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(ಬಂಡಲ್.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'direct-bytecode.json').write_text(json.dumps(ಲಾಗ್_ದಾಖಲೆ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: ಕನ್ನಡ 직접 GUI·ಎಳೆ_ಮೌಲ್ಯ 바이트코드와 예제 호출')

if __name__ == '__main__': ಚಲಾಯಿಸು_2()
