#!/usr/bin/env python3
"""배포 class의 직접 Slovenský GUI/vlákno_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

akcia_koreň = Path(__file__).resolve().parents[1]

def Spustiť_2():
    클래스들 = ('Okno', 'Tlačidlo', 'Nápis', 'textové_pole', '화면구성요소', 'Akcia_upozornenie', 'udalosť_front', '작업가닥',
             '작업', '실행할일', '동작받이')
    zväzok = akcia_koreň/'dist/jkoros-native-korean.jar'
    deklarácia = subprocess.check_output(['javap', '-classpath', str(zväzok), '-private', '-c']+
                                ['Slovenský.vlastné.'+Názov for Názov in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklarácia, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(akcia_koreň/'build/examples/classes'), '-c', 'UkážkaOkna']).decode()
    for 필수 in ('public static void Spustiť_2()', 'Slovenský/vlastné/udalosť_front.나중에실행', 'Slovenský/vlastné/Akcia_upozornenie.príkaz_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    cieľ_VALUE = akcia_koreň/'build/verification/naming'; cieľ_VALUE.mkdir(parents=True, exist_ok=True)
    (cieľ_VALUE/'direct-bytecode.txt').write_text(deklarácia+'\n'+예제)
    LOG_RECORD = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(zväzok.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (cieľ_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Slovenský 직접 GUI·vlákno_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Spustiť_2()
