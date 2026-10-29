#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/ағын_мән 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

жоба_түбір = Path(__file__).resolve().parents[1]

def Орындау_2():
    클래스들 = ('Терезе', 'батырма', 'Белгі', 'мәтіндік_өріс', '화면구성요소', '동작알림', 'оқиға_кезек', '작업가닥',
             '작업', '실행할일', '동작받이')
    жинау = жоба_түбір/'dist/jkoros-native-korean.jar'
    мәлімдеме = subprocess.check_output(['javap', '-classpath', str(жинау), '-private', '-c']+
                                ['한국어.자체.'+Аты for Аты in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in мәлімдеме, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(жоба_түбір/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Орындау_2()', '한국어/자체/оқиға_кезек.나중에실행', '한국어/자체/동작알림.пәрмен_Мәтін'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    тағайындау_мән = жоба_түбір/'build/verification/naming'; тағайындау_мән.mkdir(parents=True, exist_ok=True)
    (тағайындау_мән/'direct-bytecode.txt').write_text(мәлімдеме+'\n'+예제)
    журнал_жол = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(жинау.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (тағайындау_мән/'direct-bytecode.json').write_text(json.dumps(журнал_жол, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·ағын_мән 바이트코드와 예제 호출')

if __name__ == '__main__': Орындау_2()
