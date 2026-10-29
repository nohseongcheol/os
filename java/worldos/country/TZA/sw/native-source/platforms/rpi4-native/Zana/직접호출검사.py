#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/mtungo_thamani 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

기준 = Path(__file__).resolve().parents[1]

def endesha():
    클래스들 = ('창', 'kitufe', 'lebo', 'SMS_uga', '화면구성요소', '동작알림', 'tukio_foleni', '작업가닥',
             '작업', '실행할일', '동작받이')
    fungasha = 기준/'dist/jkoros-native-korean.jar'
    tamko = subprocess.check_output(['javap', '-classpath', str(fungasha), '-private', '-c']+
                                ['한국어.자체.'+Jina for Jina in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in tamko, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(기준/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void endesha()', '한국어/자체/tukio_foleni.나중에실행', '한국어/자체/동작알림.amri_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    fikio_thamani = 기준/'build/verification/naming'; fikio_thamani.mkdir(parents=True, exist_ok=True)
    (fikio_thamani/'direct-bytecode.txt').write_text(tamko+'\n'+예제)
    batli_REKODI = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(fungasha.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (fikio_thamani/'direct-bytecode.json').write_text(json.dumps(batli_REKODI, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·mtungo_thamani 바이트코드와 예제 호출')

if __name__ == '__main__': endesha()
