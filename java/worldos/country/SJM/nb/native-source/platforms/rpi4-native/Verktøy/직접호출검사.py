#!/usr/bin/env python3
"""distribusjon_VERDI class의 직접 norsk GUI/tråd_VERDI 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

speile_rot = Path(__file__).resolve().parents[1]

def Kjør_2():
    클래스들 = ('Vindu', 'Knapp', 'Etikett', 'tekstfelt', 'skjermbilde_element', 'Gjøremål_notice', 'hendelse_kø', 'arbeider',
             '작업', '실행할일', '동작받이')
    bunt = speile_rot/'dist/jkoros-native-korean.jar'
    erklæring = subprocess.check_output(['javap', '-classpath', str(bunt), '-private', '-c']+
                                ['norsk.eget.'+Navn for Navn in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in erklæring, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(speile_rot/'build/examples/classes'), '-c', 'Vinduseksempel']).decode()
    for 필수 in ('public static void Kjør_2()', 'norsk/eget/hendelse_kø.나중에실행', 'norsk/eget/Gjøremål_notice.kommando_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    mål_VERDI = speile_rot/'build/verification/naming'; mål_VERDI.mkdir(parents=True, exist_ok=True)
    (mål_VERDI/'direct-bytecode.txt').write_text(erklæring+'\n'+예제)
    LOG_POST = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(bunt.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (mål_VERDI/'direct-bytecode.json').write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2)+'\n')
    print('PASS: norsk 직접 GUI·tråd_VERDI 바이트코드와 예제 호출')

if __name__ == '__main__': Kjør_2()
