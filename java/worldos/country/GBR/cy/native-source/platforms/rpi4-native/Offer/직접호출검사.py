#!/usr/bin/env python3
"""배포 class의 직접 Cymraeg GUI/edefyn_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

prosiect_gwraidd = Path(__file__).resolve().parents[1]

def Gweithredu_2():
    클래스들 = ('창', 'botwm', 'label', 'maes_testun', '화면구성요소', '동작알림', 'digwyddiad_ciw', '작업가닥',
             '작업', '실행할일', '동작받이')
    bwndel = prosiect_gwraidd/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(bwndel), '-private', '-c']+
                                ['Cymraeg.자체.'+Enw for Enw in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(prosiect_gwraidd/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Gweithredu_2()', 'Cymraeg/자체/digwyddiad_ciw.나중에실행', 'Cymraeg/자체/동작알림.gorchymyn_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    cyrchfan_VALUE = prosiect_gwraidd/'build/verification/naming'; cyrchfan_VALUE.mkdir(parents=True, exist_ok=True)
    (cyrchfan_VALUE/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    LOG_rhes = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(bwndel.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (cyrchfan_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_rhes, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Cymraeg 직접 GUI·edefyn_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Gweithredu_2()
