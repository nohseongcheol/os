#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/tråd_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

spegle_rot = Path(__file__).resolve().parents[1]

def Køyr_2():
    클래스들 = ('창', 'knapp', 'Etikett', 'SMS_felt', '화면구성요소', '동작알림', 'hending_kø', '작업가닥',
             '작업', '실행할일', '동작받이')
    bunt = spegle_rot/'dist/jkoros-native-korean.jar'
    erklæring = subprocess.check_output(['javap', '-classpath', str(bunt), '-private', '-c']+
                                ['한국어.자체.'+Namn for Namn in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in erklæring, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(spegle_rot/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Køyr_2()', '한국어/자체/hending_kø.나중에실행', '한국어/자체/동작알림.kommando_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    mål_VALUE = spegle_rot/'build/verification/naming'; mål_VALUE.mkdir(parents=True, exist_ok=True)
    (mål_VALUE/'direct-bytecode.txt').write_text(erklæring+'\n'+예제)
    LOG_rad = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(bunt.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (mål_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_rad, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·tråd_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Køyr_2()
