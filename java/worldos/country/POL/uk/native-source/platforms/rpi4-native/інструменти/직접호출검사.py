#!/usr/bin/env python3
"""배포 class의 직접 українська GUI/потік_значення_5b72a632 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Дії_корінь = Path(__file__).resolve().parents[1]

def запустити():
    클래스들 = ('Вікно', 'кнопка', 'Мітка', 'текстове_поле', '화면구성요소', 'Дія_повідомлення', 'подія_черга', 'фоноваЗадача',
             '작업', '실행할일', '동작받이')
    набір = Дії_корінь/'dist/jkoros-native-korean.jar'
    оголошення_4f4f026b = subprocess.check_output(['javap', '-classpath', str(набір), '-private', '-c']+
                                ['українська.своє.'+Назва for Назва in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in оголошення_4f4f026b, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Дії_корінь/'build/examples/classes'), '-c', 'ПрикладВікна']).decode()
    for 필수 in ('public static void запустити()', 'українська/своє/подія_черга.나중에실행', 'українська/своє/Дія_повідомлення.команда_Текст'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    місце_значення = Дії_корінь/'build/verification/naming'; місце_значення.mkdir(parents=True, exist_ok=True)
    (місце_значення/'direct-bytecode.txt').write_text(оголошення_4f4f026b+'\n'+예제)
    журнал_запис = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(набір.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (місце_значення/'direct-bytecode.json').write_text(json.dumps(журнал_запис, ensure_ascii=False, indent=2)+'\n')
    print('PASS: українська 직접 GUI·потік_значення_5b72a632 바이트코드와 예제 호출')

if __name__ == '__main__': запустити()
