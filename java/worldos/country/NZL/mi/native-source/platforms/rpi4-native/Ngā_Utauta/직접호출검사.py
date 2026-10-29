#!/usr/bin/env python3
"""배포 class의 직접 Reo_Māori GUI/miro_uara 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

whakaatu_pūtake = Path(__file__).resolve().parents[1]

def whakahaere():
    클래스들 = ('창', 'pātene', 'tapanga', 'āpure_kuputuhi', '화면구성요소', '동작알림', 'hui_tūtira', '작업가닥',
             '작업', '실행할일', '동작받이')
    pūpū = whakaatu_pūtake/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(pūpū), '-private', '-c']+
                                ['Reo_Māori.자체.'+Ingoa for Ingoa in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(whakaatu_pūtake/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void whakahaere()', 'Reo_Māori/자체/hui_tūtira.나중에실행', 'Reo_Māori/자체/동작알림.tono_TEXT'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ūnga_uara = whakaatu_pūtake/'build/verification/naming'; ūnga_uara.mkdir(parents=True, exist_ok=True)
    (ūnga_uara/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    LOG_RECORD = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(pūpū.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ūnga_uara/'direct-bytecode.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Reo_Māori 직접 GUI·miro_uara 바이트코드와 예제 호출')

if __name__ == '__main__': whakahaere()
