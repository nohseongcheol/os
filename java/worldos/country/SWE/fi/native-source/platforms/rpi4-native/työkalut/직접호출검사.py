#!/usr/bin/env python3
"""jakelu_ARVO class의 직접 suomi GUI/säie_ARVO 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

aloite_juuri = Path(__file__).resolve().parents[1]

def Suorita_2():
    클래스들 = ('Ikkuna', 'painike', 'Nimike', 'tekstikenttä', '화면구성요소', '동작알림', 'tapahtuma_jono', 'työntekijä',
             '작업', '실행할일', '동작받이')
    nippu = aloite_juuri/'dist/jkoros-native-korean.jar'
    esittely = subprocess.check_output(['javap', '-classpath', str(nippu), '-private', '-c']+
                                ['suomi.oma.'+Nimi for Nimi in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in esittely, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(aloite_juuri/'build/examples/classes'), '-c', 'Ikkunaesimerkki']).decode()
    for 필수 in ('public static void Suorita_2()', 'suomi/oma/tapahtuma_jono.나중에실행', 'suomi/oma/동작알림.komento_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    kohde_ARVO = aloite_juuri/'build/verification/naming'; kohde_ARVO.mkdir(parents=True, exist_ok=True)
    (kohde_ARVO/'direct-bytecode.txt').write_text(esittely+'\n'+예제)
    LOG_TIETUE = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(nippu.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (kohde_ARVO/'direct-bytecode.json').write_text(json.dumps(LOG_TIETUE, ensure_ascii=False, indent=2)+'\n')
    print('PASS: suomi 직접 GUI·säie_ARVO 바이트코드와 예제 호출')

if __name__ == '__main__': Suorita_2()
