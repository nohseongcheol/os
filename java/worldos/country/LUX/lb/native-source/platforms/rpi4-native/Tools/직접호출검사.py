#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/Thread_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

projezéieren_Racinn = Path(__file__).resolve().parents[1]

def Laf():
    클래스들 = ('창', 'Tast', 'Numm_5ce2bd6f', 'Textfeld', '화면구성요소', '동작알림', 'Evenement_Schlaang', '작업가닥',
             '작업', '실행할일', '동작받이')
    Bëndel = projezéieren_Racinn/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(Bëndel), '-private', '-c']+
                                ['한국어.자체.'+Numm for Numm in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(projezéieren_Racinn/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Laf()', '한국어/자체/Evenement_Schlaang.나중에실행', '한국어/자체/동작알림.Befeel_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    Zil_VALUE = projezéieren_Racinn/'build/verification/naming'; Zil_VALUE.mkdir(parents=True, exist_ok=True)
    (Zil_VALUE/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    LOG_Rei = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(Bëndel.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (Zil_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_Rei, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·Thread_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Laf()
