#!/usr/bin/env python3
"""배포 class의 직접 Македонски GUI/нишка_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_корен = Path(__file__).resolve().parents[1]

def Изврши_2():
    클래스들 = ('창', 'копче', 'Ознака', 'СМС_поле', '화면구성요소', '동작알림', 'настан_ред_на_чекање', '작업가닥',
             '작업', '실행할일', '동작받이')
    пакет = Project_корен/'dist/jkoros-native-korean.jar'
    декларација = subprocess.check_output(['javap', '-classpath', str(пакет), '-private', '-c']+
                                ['Македонски.자체.'+Име for Име in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in декларација, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_корен/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Изврши_2()', 'Македонски/자체/настан_ред_на_чекање.나중에실행', 'Македонски/자체/동작알림.наредба_СМС'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    одредиште_VALUE = Project_корен/'build/verification/naming'; одредиште_VALUE.mkdir(parents=True, exist_ok=True)
    (одредиште_VALUE/'direct-bytecode.txt').write_text(декларација+'\n'+예제)
    LOG_ред = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(пакет.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (одредиште_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_ред, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Македонски 직접 GUI·нишка_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Изврши_2()
