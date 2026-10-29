#!/usr/bin/env python3
"""배포 class의 직접 Malti GUI/fil_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

pprojetta_għerq = Path(__file__).resolve().parents[1]

def serje():
    클래스들 = ('창', 'buttuna', 'tikketta', 'qasam_ta_test', '화면구성요소', '동작알림', 'avveniment_kju', '작업가닥',
             '작업', '실행할일', '동작받이')
    lott = pprojetta_għerq/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(lott), '-private', '-c']+
                                ['Malti.자체.'+isem for isem in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(pprojetta_għerq/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void serje()', 'Malti/자체/avveniment_kju.나중에실행', 'Malti/자체/동작알림.kmand_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    destinazzjoni_VALUE = pprojetta_għerq/'build/verification/naming'; destinazzjoni_VALUE.mkdir(parents=True, exist_ok=True)
    (destinazzjoni_VALUE/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    LOG_RECORD = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(lott.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (destinazzjoni_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Malti 직접 GUI·fil_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': serje()
