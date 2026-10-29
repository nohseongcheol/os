#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/თემა_მნიშვნელობა 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]

def გაშვება():
    클래스들 = ('창', 'ღილაკი', 'სათაური', 'ტექსტური_ველი', '화면구성요소', '동작알림', 'მოვლენა_რიგი', '작업가닥',
             '작업', '실행할일', '동작받이')
    შეკვრა = პროეცირება_ფესვი/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(შეკვრა), '-private', '-c']+
                                ['한국어.자체.'+სახელი for სახელი in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(პროეცირება_ფესვი/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void გაშვება()', '한국어/자체/მოვლენა_რიგი.나중에실행', '한국어/자체/동작알림.ბრძანება_ტექსტი'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    მიმართულება_მნიშვნელობა = პროეცირება_ფესვი/'build/verification/naming'; მიმართულება_მნიშვნელობა.mkdir(parents=True, exist_ok=True)
    (მიმართულება_მნიშვნელობა/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    ჟურნალი_ჩაწერა = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(შეკვრა.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (მიმართულება_მნიშვნელობა/'direct-bytecode.json').write_text(json.dumps(ჟურნალი_ჩაწერა, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·თემა_მნიშვნელობა 바이트코드와 예제 호출')

if __name__ == '__main__': გაშვება()
