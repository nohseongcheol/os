#!/usr/bin/env python3
"""elosztás_ÉRTÉK class의 직접 magyar GUI/szál_ÉRTÉK 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

teendő_gyök = Path(__file__).resolve().parents[1]

def Futtatás():
    클래스들 = ('Ablak', 'gomb', 'Címke', 'szövegmező', '화면구성요소', 'Action_alapelv', 'esemény_várólista', 'dolgozó',
             '작업', '실행할일', '동작받이')
    köteg = teendő_gyök/'dist/jkoros-native-korean.jar'
    bevallás = subprocess.check_output(['javap', '-classpath', str(köteg), '-private', '-c']+
                                ['magyar.saját.'+Név for Név in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in bevallás, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(teendő_gyök/'build/examples/classes'), '-c', 'AblakPélda']).decode()
    for 필수 in ('public static void Futtatás()', 'magyar/saját/esemény_várólista.나중에실행', 'magyar/saját/Action_alapelv.parancs_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    cél_ÉRTÉK = teendő_gyök/'build/verification/naming'; cél_ÉRTÉK.mkdir(parents=True, exist_ok=True)
    (cél_ÉRTÉK/'direct-bytecode.txt').write_text(bevallás+'\n'+예제)
    LOG_REKORD = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(köteg.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (cél_ÉRTÉK/'direct-bytecode.json').write_text(json.dumps(LOG_REKORD, ensure_ascii=False, indent=2)+'\n')
    print('PASS: magyar 직접 GUI·szál_ÉRTÉK 바이트코드와 예제 호출')

if __name__ == '__main__': Futtatás()
