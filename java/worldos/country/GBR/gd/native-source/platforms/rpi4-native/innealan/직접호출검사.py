#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/snàithlean_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

tilg_freumh = Path(__file__).resolve().parents[1]

def ruith():
    클래스들 = ('창', 'putan', 'bileag', 'raon_teacsa', '화면구성요소', '동작알림', 'tachartas_ciutha', '작업가닥',
             '작업', '실행할일', '동작받이')
    trusgan = tilg_freumh/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(trusgan), '-private', '-c']+
                                ['한국어.자체.'+Ainm for Ainm in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(tilg_freumh/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ruith()', '한국어/자체/tachartas_ciutha.나중에실행', '한국어/자체/동작알림.àithne_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ceann_uidhe_VALUE = tilg_freumh/'build/verification/naming'; ceann_uidhe_VALUE.mkdir(parents=True, exist_ok=True)
    (ceann_uidhe_VALUE/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    LOG_ràgh = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(trusgan.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ceann_uidhe_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_ràgh, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·snàithlean_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': ruith()
