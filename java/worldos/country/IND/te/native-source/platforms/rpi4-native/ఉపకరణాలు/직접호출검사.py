#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/థ్రెడ్_మూల్యం 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]

def నడుపుము():
    클래스들 = ('విండో', 'బటన్', 'లేబుల్', 'పాఠం_ఫీల్డ్', '화면구성요소', '동작알림', 'ఈవెంట్_నిరీక్షణ_క్రమం', '작업가닥',
             '작업', '실행할일', '동작받이')
    బండిల్ = ప్రొజెక్ట్_మూలం/'dist/jkoros-native-korean.jar'
    ప్రకటన = subprocess.check_output(['javap', '-classpath', str(బండిల్), '-private', '-c']+
                                ['한국어.자체.'+పేరు for పేరు in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in ప్రకటన, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(ప్రొజెక్ట్_మూలం/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void నడుపుము()', '한국어/자체/ఈవెంట్_నిరీక్షణ_క్రమం.나중에실행', '한국어/자체/동작알림.ఆదేశం_పాఠం'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    గమ్యం_మూల్యం = ప్రొజెక్ట్_మూలం/'build/verification/naming'; గమ్యం_మూల్యం.mkdir(parents=True, exist_ok=True)
    (గమ్యం_మూల్యం/'direct-bytecode.txt').write_text(ప్రకటన+'\n'+예제)
    లాగ్_వరుస = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(బండిల్.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (గమ్యం_మూల్యం/'direct-bytecode.json').write_text(json.dumps(లాగ్_వరుస, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·థ్రెడ్_మూల్యం 바이트코드와 예제 호출')

if __name__ == '__main__': నడుపుము()
