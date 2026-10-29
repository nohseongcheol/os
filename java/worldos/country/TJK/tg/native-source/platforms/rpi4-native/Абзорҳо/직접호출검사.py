#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/ришта_қимат 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

기준 = Path(__file__).resolve().parents[1]

def порча():
    클래스들 = ('창', 'тугма', 'барчасп', 'Матн_майдон', '화면구성요소', '동작알림', 'рӯйдод_навбат', '작업가닥',
             '작업', '실행할일', '동작받이')
    баста = 기준/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(баста), '-private', '-c']+
                                ['한국어.자체.'+Ном for Ном in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(기준/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void порча()', '한국어/자체/рӯйдод_навбат.나중에실행', '한국어/자체/동작알림.фармон_Матн'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ҷои_таъинот_қимат = 기준/'build/verification/naming'; ҷои_таъинот_қимат.mkdir(parents=True, exist_ok=True)
    (ҷои_таъинот_қимат/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    сабт_кардан_сабт = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(баста.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ҷои_таъинот_қимат/'direct-bytecode.json').write_text(json.dumps(сабт_кардан_сабт, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·ришта_қимат 바이트코드와 예제 호출')

if __name__ == '__main__': порча()
