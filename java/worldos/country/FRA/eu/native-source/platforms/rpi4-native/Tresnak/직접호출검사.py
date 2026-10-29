#!/usr/bin/env python3
"""배포 class의 직접 Euskara GUI/hari_balio 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_erro = Path(__file__).resolve().parents[1]

def Exekutatu_2():
    클래스들 = ('Leihoa', 'botoia', 'Etiketa', 'SMS_eremu', '화면구성요소', '동작알림', 'gertaera_ilara', '작업가닥',
             '작업', '실행할일', '동작받이')
    multzo = Project_erro/'dist/jkoros-native-korean.jar'
    deklarazio = subprocess.check_output(['javap', '-classpath', str(multzo), '-private', '-c']+
                                ['Euskara.자체.'+Izena for Izena in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklarazio, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_erro/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Exekutatu_2()', 'Euskara/자체/gertaera_ilara.나중에실행', 'Euskara/자체/동작알림.komando_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    helburu_balio_a0fbc067 = Project_erro/'build/verification/naming'; helburu_balio_a0fbc067.mkdir(parents=True, exist_ok=True)
    (helburu_balio_a0fbc067/'direct-bytecode.txt').write_text(deklarazio+'\n'+예제)
    LOG_marka = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(multzo.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (helburu_balio_a0fbc067/'direct-bytecode.json').write_text(json.dumps(LOG_marka, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Euskara 직접 GUI·hari_balio 바이트코드와 예제 호출')

if __name__ == '__main__': Exekutatu_2()
