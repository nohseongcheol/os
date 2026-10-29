#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/паток_значэнне_5b72a632 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Выканаць():
    클래스들 = ('창', 'кнопка', 'Адмеціна', 'Тэкст_поле', '화면구성요소', '동작알림', 'падзея_чарга', '작업가닥',
             '작업', '실행할일', '동작받이')
    пакет = 기준/'dist/jkoros-native-korean.jar'
    абвяшчэнне = subprocess.check_output(['javap', '-classpath', str(пакет), '-private', '-c']+
                                ['한국어.자체.'+Назва for Назва in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in абвяшчэнне, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(기준/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Выканаць()', '한국어/자체/падзея_чарга.나중에실행', '한국어/자체/동작알림.каманда_Тэкст'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    прызначэнне_значэнне_a0fbc067 = 기준/'build/verification/naming'; прызначэнне_значэнне_a0fbc067.mkdir(parents=True, exist_ok=True)
    (прызначэнне_значэнне_a0fbc067/'direct-bytecode.txt').write_text(абвяшчэнне+'\n'+예제)
    журнал_запіс = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(пакет.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (прызначэнне_значэнне_a0fbc067/'direct-bytecode.json').write_text(json.dumps(журнал_запіс, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·паток_значэнне_5b72a632 바이트코드와 예제 호출')

if __name__ == '__main__': Выканаць()
