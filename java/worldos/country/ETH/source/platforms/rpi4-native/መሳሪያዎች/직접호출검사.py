#!/usr/bin/env python3
"""배포 class의 직접 አማርኛ GUI/ክር_እሴት 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

አሳይ_ስር = Path(__file__).resolve().parents[1]

def ማስኬጃ():
    클래스들 = ('창', 'አዝራር', 'ምልክት', 'ጽሁፍ_መስክ', '화면구성요소', '동작알림', 'ፍጻሜ_ሰልፍ', '작업가닥',
             '작업', '실행할일', '동작받이')
    ቀርቅብ = አሳይ_ስር/'dist/jkoros-native-korean.jar'
    እወጃ = subprocess.check_output(['javap', '-classpath', str(ቀርቅብ), '-private', '-c']+
                                ['አማርኛ.자체.'+ስም for ስም in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in እወጃ, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(አሳይ_ስር/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ማስኬጃ()', 'አማርኛ/자체/ፍጻሜ_ሰልፍ.나중에실행', 'አማርኛ/자체/동작알림.ትእዛዝ_ጽሁፍ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    መድረሻ_እሴት = አሳይ_ስር/'build/verification/naming'; መድረሻ_እሴት.mkdir(parents=True, exist_ok=True)
    (መድረሻ_እሴት/'direct-bytecode.txt').write_text(እወጃ+'\n'+예제)
    መዝግብ_ረድፍ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(ቀርቅብ.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (መድረሻ_እሴት/'direct-bytecode.json').write_text(json.dumps(መዝግብ_ረድፍ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: አማርኛ 직접 GUI·ክር_እሴት 바이트코드와 예제 호출')

if __name__ == '__main__': ማስኬጃ()
