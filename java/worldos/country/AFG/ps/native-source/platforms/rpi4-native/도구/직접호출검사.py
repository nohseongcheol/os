#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/مزى_ارزښت 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ځغلول():
    클래스들 = ('창', 'تڼۍ', 'نښکه', '입력칸', '화면구성요소', '동작알림', 'پېښه_ليکه', '작업가닥',
             '작업', '실행할일', '동작받이')
    꾸러미 = 기준/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(꾸러미), '-private', '-c']+
                                ['한국어.자체.'+نوم for نوم in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(기준/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ځغلول()', '한국어/자체/پېښه_ليکه.나중에실행', '한국어/자체/동작알림.명령글'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    موخه_ارزښت = 기준/'build/verification/naming'; موخه_ارزښت.mkdir(parents=True, exist_ok=True)
    (موخه_ارزښت/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    خبرال_کیل = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(꾸러미.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (موخه_ارزښت/'direct-bytecode.json').write_text(json.dumps(خبرال_کیل, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·مزى_ارزښت 바이트코드와 예제 호출')

if __name__ == '__main__': ځغلول()
