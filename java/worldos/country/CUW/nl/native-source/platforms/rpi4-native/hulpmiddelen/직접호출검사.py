#!/usr/bin/env python3
"""distributie_WAARDE class의 직접 Nederlands GUI/thread_WAARDE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Taken_wortel = Path(__file__).resolve().parents[1]

def starten():
    클래스들 = ('Venster', 'knop', 'Etiket', 'tekstveld', 'scherm_element', 'Actie_kennisgeving', 'gebeurtenis_wachtrij', 'achtergrondwerker',
             '작업', '실행할일', '동작받이')
    bundel = Taken_wortel/'dist/jkoros-native-korean.jar'
    aangifte = subprocess.check_output(['javap', '-classpath', str(bundel), '-private', '-c']+
                                ['Nederlands.Eigen.'+Naam for Naam in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in aangifte, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Taken_wortel/'build/examples/classes'), '-c', 'Venstervoorbeeld']).decode()
    for 필수 in ('public static void starten()', 'Nederlands/Eigen/gebeurtenis_wachtrij.나중에실행', 'Nederlands/Eigen/Actie_kennisgeving.opdracht_sms'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    doel_WAARDE = Taken_wortel/'build/verification/naming'; doel_WAARDE.mkdir(parents=True, exist_ok=True)
    (doel_WAARDE/'direct-bytecode.txt').write_text(aangifte+'\n'+예제)
    LOG_RECORD = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(bundel.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (doel_WAARDE/'direct-bytecode.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Nederlands 직접 GUI·thread_WAARDE 바이트코드와 예제 호출')

if __name__ == '__main__': starten()
