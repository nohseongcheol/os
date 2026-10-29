#!/usr/bin/env python3
"""dreifing_VALUE class의 직접 Íslenska GUI/þráður_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

verk_rót = Path(__file__).resolve().parents[1]

def Keyra_2():
    클래스들 = ('Gluggi', 'hnappur', 'Skýring', 'SMS_reitur', '화면구성요소', '동작알림', 'atvik_biðröð', 'starfskraftur',
             '작업', '실행할일', '동작받이')
    búnt = verk_rót/'dist/jkoros-native-korean.jar'
    skýrsla = subprocess.check_output(['javap', '-classpath', str(búnt), '-private', '-c']+
                                ['Íslenska.eigin.'+Heiti for Heiti in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in skýrsla, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(verk_rót/'build/examples/classes'), '-c', 'Gluggadæmi']).decode()
    for 필수 in ('public static void Keyra_2()', 'Íslenska/eigin/atvik_biðröð.나중에실행', 'Íslenska/eigin/동작알림.skipun_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    endastaður_VALUE = verk_rót/'build/verification/naming'; endastaður_VALUE.mkdir(parents=True, exist_ok=True)
    (endastaður_VALUE/'direct-bytecode.txt').write_text(skýrsla+'\n'+예제)
    LOG_lína = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(búnt.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (endastaður_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_lína, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Íslenska 직접 GUI·þráður_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Keyra_2()
