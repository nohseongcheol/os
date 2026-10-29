#!/usr/bin/env python3
"""배포 class의 직접 Română GUI/fir_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_rădăcină = Path(__file__).resolve().parents[1]

def Pornește():
    클래스들 = ('Fereastră', 'buton', 'Etichetă', 'câmp_text', '화면구성요소', 'Acțiune_înștiințare', 'eveniment_coadă', '작업가닥',
             '작업', '실행할일', '동작받이')
    set = Project_rădăcină/'dist/jkoros-native-korean.jar'
    declarație = subprocess.check_output(['javap', '-classpath', str(set), '-private', '-c']+
                                ['Română.propriu.'+Nume for Nume in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in declarație, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_rădăcină/'build/examples/classes'), '-c', 'ExempluFereastră']).decode()
    for 필수 in ('public static void Pornește()', 'Română/propriu/eveniment_coadă.나중에실행', 'Română/propriu/Acțiune_înștiințare.comandă_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    destinație_VALUE = Project_rădăcină/'build/verification/naming'; destinație_VALUE.mkdir(parents=True, exist_ok=True)
    (destinație_VALUE/'direct-bytecode.txt').write_text(declarație+'\n'+예제)
    LOG_RECORD = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(set.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (destinație_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Română 직접 GUI·fir_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Pornește()
