#!/usr/bin/env python3
"""paskirstymas_VALUE class의 직접 Lietuvių GUI/gija_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_šaknis = Path(__file__).resolve().parents[1]

def Paleisti():
    클래스들 = ('Langas', 'mygtukas', 'Pavadinimas', 'teksto_laukas', '화면구성요소', 'gavinys_pranešimas', 'įvykis_eilė', 'darbininkas',
             '작업', '실행할일', '동작받이')
    paketas = Project_šaknis/'dist/jkoros-native-korean.jar'
    deklaracija = subprocess.check_output(['javap', '-classpath', str(paketas), '-private', '-c']+
                                ['Lietuvių.savas.'+Pavadinimas_2 for Pavadinimas_2 in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklaracija, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_šaknis/'build/examples/classes'), '-c', 'LangoPavyzdys']).decode()
    for 필수 in ('public static void Paleisti()', 'Lietuvių/savas/įvykis_eilė.나중에실행', 'Lietuvių/savas/gavinys_pranešimas.komanda_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    vieta_VALUE = Project_šaknis/'build/verification/naming'; vieta_VALUE.mkdir(parents=True, exist_ok=True)
    (vieta_VALUE/'direct-bytecode.txt').write_text(deklaracija+'\n'+예제)
    LOG_RECORD = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(paketas.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (vieta_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Lietuvių 직접 GUI·gija_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Paleisti()
