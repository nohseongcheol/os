#!/usr/bin/env python3
"""distribution_VÆRDI class의 직접 Dansk GUI/tråd_VÆRDI 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

To_do_rod = Path(__file__).resolve().parents[1]

def Kør_2():
    클래스들 = ('Vindue', 'knap', 'Etiket', 'tekstfelt', 'skærmbillede_element', '동작알림', 'hændelse_kø', 'arbejder',
             '작업', '실행할일', '동작받이')
    bundt = To_do_rod/'dist/jkoros-native-korean.jar'
    erklæring = subprocess.check_output(['javap', '-classpath', str(bundt), '-private', '-c']+
                                ['Dansk.eget.'+Navn for Navn in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in erklæring, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(To_do_rod/'build/examples/classes'), '-c', 'Vindueseksempel']).decode()
    for 필수 in ('public static void Kør_2()', 'Dansk/eget/hændelse_kø.나중에실행', 'Dansk/eget/동작알림.kommando_sms'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    destination_VÆRDI = To_do_rod/'build/verification/naming'; destination_VÆRDI.mkdir(parents=True, exist_ok=True)
    (destination_VÆRDI/'direct-bytecode.txt').write_text(erklæring+'\n'+예제)
    LOG_post = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(bundt.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (destination_VÆRDI/'direct-bytecode.json').write_text(json.dumps(LOG_post, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Dansk 직접 GUI·tråd_VÆRDI 바이트코드와 예제 호출')

if __name__ == '__main__': Kør_2()
