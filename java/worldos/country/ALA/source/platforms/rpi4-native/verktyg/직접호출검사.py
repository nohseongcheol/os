#!/usr/bin/env python3
"""fördelning_värde class의 직접 Svenska GUI/tråd_värde 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

åtgärd_rot = Path(__file__).resolve().parents[1]

def Kör():
    클래스들 = ('Fönster', 'knapp', 'Etikett', 'textfält', 'skärmbild_element', '동작알림', 'händelse_kö', 'arbete',
             '작업', '실행할일', '동작받이')
    bunt = åtgärd_rot/'dist/jkoros-native-korean.jar'
    deklaration = subprocess.check_output(['javap', '-classpath', str(bunt), '-private', '-c']+
                                ['Svenska.eget.'+Namn for Namn in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklaration, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(åtgärd_rot/'build/examples/classes'), '-c', 'Fönsterexempel']).decode()
    for 필수 in ('public static void Kör()', 'Svenska/eget/händelse_kö.나중에실행', 'Svenska/eget/동작알림.kommando_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    mål_värde = åtgärd_rot/'build/verification/naming'; mål_värde.mkdir(parents=True, exist_ok=True)
    (mål_värde/'direct-bytecode.txt').write_text(deklaration+'\n'+예제)
    LOG_POST = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(bunt.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (mål_värde/'direct-bytecode.json').write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Svenska 직접 GUI·tråd_värde 바이트코드와 예제 호출')

if __name__ == '__main__': Kör()
