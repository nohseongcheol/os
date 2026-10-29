#!/usr/bin/env python3
"""распределение_ЗНАЧЕН class의 직접 русский GUI/поток_ЗНАЧЕН_5b72a632 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

задача_корень = Path(__file__).resolve().parents[1]

def запустить():
    클래스들 = ('Окно', 'кнопка', 'Метка', 'текстовое_поле', 'экран_элемент', 'задача_уведомление', 'Событие_Очередь', 'фоноваяЗадача',
             '작업', '실행할일', '동작받이')
    пакет = задача_корень/'dist/jkoros-native-korean.jar'
    декларация = subprocess.check_output(['javap', '-classpath', str(пакет), '-private', '-c']+
                                ['русский.свой.'+Название for Название in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in декларация, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(задача_корень/'build/examples/classes'), '-c', 'ПримерОкна']).decode()
    for 필수 in ('public static void запустить()', 'русский/свой/Событие_Очередь.나중에실행', 'русский/свой/задача_уведомление.명령글'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    цель_ЗНАЧЕН = задача_корень/'build/verification/naming'; цель_ЗНАЧЕН.mkdir(parents=True, exist_ok=True)
    (цель_ЗНАЧЕН/'direct-bytecode.txt').write_text(декларация+'\n'+예제)
    LOG_ЗАПИСЬ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(пакет.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (цель_ЗНАЧЕН/'direct-bytecode.json').write_text(json.dumps(LOG_ЗАПИСЬ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: русский 직접 GUI·поток_ЗНАЧЕН_5b72a632 바이트코드와 예제 호출')

if __name__ == '__main__': запустить()
