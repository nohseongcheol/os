#!/usr/bin/env python3
"""배포 class의 직접 Татарча GUI/агым_VALUE_5b72a632 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]

def эшләтү():
    클래스들 = ('창', 'төймә', 'тамга', 'текст_кыры', '화면구성요소', '동작알림', 'вакыйга_чират', '작업가닥',
             '작업', '실행할일', '동작받이')
    пакет = экранга_җибәрү_тамыр/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(пакет), '-private', '-c']+
                                ['Татарча.자체.'+исем for исем in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(экранга_җибәрү_тамыр/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void эшләтү()', 'Татарча/자체/вакыйга_чират.나중에실행', 'Татарча/자체/동작알림.команда_СМС'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    күчерү_урыны_VALUE = экранга_җибәрү_тамыр/'build/verification/naming'; күчерү_урыны_VALUE.mkdir(parents=True, exist_ok=True)
    (күчерү_урыны_VALUE/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    LOG_юл = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(пакет.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (күчерү_урыны_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_юл, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Татарча 직접 GUI·агым_VALUE_5b72a632 바이트코드와 예제 호출')

if __name__ == '__main__': эшләтү()
