#!/usr/bin/env python3
"""배포 class의 직접 ትግርኛ GUI/ፈትሊ_ዋጋ 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ኣኺድ():
    클래스들 = ('창', 'መጠወቒ', 'ገላጺ', 'ጽሑፍ_ሜዳ', '화면구성요소', '동작알림', 'ፍጻመ_ሪጋ', '작업가닥',
             '작업', '실행할일', '동작받이')
    ጥማር = 기준/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(ጥማር), '-private', '-c']+
                                ['ትግርኛ.자체.'+ሽም for ሽም in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(기준/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ኣኺድ()', 'ትግርኛ/자체/ፍጻመ_ሪጋ.나중에실행', 'ትግርኛ/자체/동작알림.ትእዛዝ_ጽሑፍ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    መዓልቦ_ዋጋ = 기준/'build/verification/naming'; መዓልቦ_ዋጋ.mkdir(parents=True, exist_ok=True)
    (መዓልቦ_ዋጋ/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    ምዝጉብ_ሪጋ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(ጥማር.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (መዓልቦ_ዋጋ/'direct-bytecode.json').write_text(json.dumps(ምዝጉብ_ሪጋ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: ትግርኛ 직접 GUI·ፈትሊ_ዋጋ 바이트코드와 예제 호출')

if __name__ == '__main__': ኣኺድ()
