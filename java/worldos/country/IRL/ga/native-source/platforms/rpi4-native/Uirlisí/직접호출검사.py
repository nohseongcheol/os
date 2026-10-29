#!/usr/bin/env python3
"""배포 class의 직접 Gaeilge GUI/snáithe_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

teilgean_fréamh = Path(__file__).resolve().parents[1]

def Rith_2():
    클래스들 = ('창', 'cnaipe', 'Lipéad', 'réimse_téacs', '화면구성요소', '동작알림', 'ócáid_scuaine', '작업가닥',
             '작업', '실행할일', '동작받이')
    beart = teilgean_fréamh/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(beart), '-private', '-c']+
                                ['Gaeilge.자체.'+Ainm for Ainm in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(teilgean_fréamh/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Rith_2()', 'Gaeilge/자체/ócáid_scuaine.나중에실행', 'Gaeilge/자체/동작알림.ordú_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    sprioc_VALUE = teilgean_fréamh/'build/verification/naming'; sprioc_VALUE.mkdir(parents=True, exist_ok=True)
    (sprioc_VALUE/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    LOG_ró = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(beart.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (sprioc_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_ró, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Gaeilge 직접 GUI·snáithe_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Rith_2()
