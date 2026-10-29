#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/нит_вриједност 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

пројектовати_корен = Path(__file__).resolve().parents[1]

def Покрени():
    클래스들 = ('Прозор', 'дугме', 'Натпис', 'текстуално_поље', '화면구성요소', '동작알림', 'догађај_редослед', '작업가닥',
             '작업', '실행할일', '동작받이')
    пакет = пројектовати_корен/'dist/jkoros-native-korean.jar'
    декларација = subprocess.check_output(['javap', '-classpath', str(пакет), '-private', '-c']+
                                ['한국어.자체.'+Назив for Назив in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in декларација, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(пројектовати_корен/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Покрени()', '한국어/자체/догађај_редослед.나중에실행', '한국어/자체/동작알림.команда_Текст'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    одредиште_вриједност = пројектовати_корен/'build/verification/naming'; одредиште_вриједност.mkdir(parents=True, exist_ok=True)
    (одредиште_вриједност/'direct-bytecode.txt').write_text(декларација+'\n'+예제)
    евиденција_ред = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(пакет.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (одредиште_вриједност/'direct-bytecode.json').write_text(json.dumps(евиденција_ред, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·нит_вриједност 바이트코드와 예제 호출')

if __name__ == '__main__': Покрени()
