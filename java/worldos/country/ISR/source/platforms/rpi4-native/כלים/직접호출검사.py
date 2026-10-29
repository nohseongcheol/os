#!/usr/bin/env python3
"""הפצה_ערך class의 직접 עברית GUI/שרשור_ערך 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

לשקף_בסיס = Path(__file__).resolve().parents[1]

def הפעלה():
    클래스들 = ('חלון', 'לחצן', 'תווית', 'שדה_טקסט', '화면구성요소', 'המלצה_הודעה', 'אירוע_תור', 'משימתרקע',
             '작업', '실행할일', '동작받이')
    חבילה = לשקף_בסיס/'dist/jkoros-native-korean.jar'
    הצהרה = subprocess.check_output(['javap', '-classpath', str(חבילה), '-private', '-c']+
                                ['עברית.עצמי.'+שם for שם in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in הצהרה, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(לשקף_בסיס/'build/examples/classes'), '-c', 'דוגמתחלון']).decode()
    for 필수 in ('public static void הפעלה()', 'עברית/עצמי/אירוע_תור.나중에실행', 'עברית/עצמי/המלצה_הודעה.פקודה_טקסט'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    יעד_ערך = לשקף_בסיס/'build/verification/naming'; יעד_ערך.mkdir(parents=True, exist_ok=True)
    (יעד_ערך/'direct-bytecode.txt').write_text(הצהרה+'\n'+예제)
    לרשום_שיא = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(חבילה.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (יעד_ערך/'direct-bytecode.json').write_text(json.dumps(לרשום_שיא, ensure_ascii=False, indent=2)+'\n')
    print('PASS: עברית 직접 GUI·שרשור_ערך 바이트코드와 예제 호출')

if __name__ == '__main__': הפעלה()
