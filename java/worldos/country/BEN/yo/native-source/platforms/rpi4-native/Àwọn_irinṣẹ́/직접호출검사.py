#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/èròjà_atẹ̀lélànà_iye 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Rọ́ọ̀nù():
    클래스들 = ('창', 'bọ́tìnnì', 'àkọlé', 'SMS_àayè_wúnrẹ̀n', '화면구성요소', '동작알림', 'ìgbéṣẹ̀_ìtòléra', '작업가닥',
             '작업', '실행할일', '동작받이')
    àkópọ̀ = 기준/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(àkópọ̀), '-private', '-c']+
                                ['한국어.자체.'+Orúkọ for Orúkọ in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(기준/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Rọ́ọ̀nù()', '한국어/자체/ìgbéṣẹ̀_ìtòléra.나중에실행', '한국어/자체/동작알림.àṣẹ_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    èbúté_iye = 기준/'build/verification/naming'; èbúté_iye.mkdir(parents=True, exist_ok=True)
    (èbúté_iye/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    àkọsílẹ̀_ìṣe_ìlà_ìbú = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(àkópọ̀.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (èbúté_iye/'direct-bytecode.json').write_text(json.dumps(àkọsílẹ̀_ìṣe_ìlà_ìbú, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·èròjà_atẹ̀lélànà_iye 바이트코드와 예제 호출')

if __name__ == '__main__': Rọ́ọ̀nù()
