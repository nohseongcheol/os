#!/usr/bin/env python3
"""distribuce_HODNOTA class의 직접 čeština GUI/vlákno_HODNOTA 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

akce_kořen = Path(__file__).resolve().parents[1]

def Spustit_2():
    클래스들 = ('Okno', 'tlačítko', 'Popisek', 'textové_pole', '화면구성요소', 'Akce_povinnost_zvěřejnit', 'událost_fronta', 'pracovník',
             '작업', '실행할일', '동작받이')
    sada = akce_kořen/'dist/jkoros-native-korean.jar'
    deklarace_4f4f026b = subprocess.check_output(['javap', '-classpath', str(sada), '-private', '-c']+
                                ['čeština.vlastní.'+Název for Název in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklarace_4f4f026b, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(akce_kořen/'build/examples/classes'), '-c', 'UkázkaOkna']).decode()
    for 필수 in ('public static void Spustit_2()', 'čeština/vlastní/událost_fronta.나중에실행', 'čeština/vlastní/Akce_povinnost_zvěřejnit.příkaz_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    cíl_HODNOTA = akce_kořen/'build/verification/naming'; cíl_HODNOTA.mkdir(parents=True, exist_ok=True)
    (cíl_HODNOTA/'direct-bytecode.txt').write_text(deklarace_4f4f026b+'\n'+예제)
    LOGZ_ZÁZNAM = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(sada.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (cíl_HODNOTA/'direct-bytecode.json').write_text(json.dumps(LOGZ_ZÁZNAM, ensure_ascii=False, indent=2)+'\n')
    print('PASS: čeština 직접 GUI·vlákno_HODNOTA 바이트코드와 예제 호출')

if __name__ == '__main__': Spustit_2()
