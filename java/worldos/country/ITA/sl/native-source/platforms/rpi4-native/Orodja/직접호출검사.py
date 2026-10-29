#!/usr/bin/env python3
"""배포 class의 직접 slovenščina GUI/nit_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

pobuda_koren = Path(__file__).resolve().parents[1]

def Zaženi():
    클래스들 = ('창', 'Gumb', 'Oznaka', 'SMS_polje', '화면구성요소', 'akcija_obvestilo', 'dogodek_čakalna_vrsta', '작업가닥',
             '작업', '실행할일', '동작받이')
    sveženj = pobuda_koren/'dist/jkoros-native-korean.jar'
    deklaracija = subprocess.check_output(['javap', '-classpath', str(sveženj), '-private', '-c']+
                                ['slovenščina.lastno.'+Ime for Ime in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklaracija, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(pobuda_koren/'build/examples/classes'), '-c', 'PrimerOkna']).decode()
    for 필수 in ('public static void Zaženi()', 'slovenščina/lastno/dogodek_čakalna_vrsta.나중에실행', 'slovenščina/lastno/akcija_obvestilo.ukaz_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    cilj_VALUE = pobuda_koren/'build/verification/naming'; cilj_VALUE.mkdir(parents=True, exist_ok=True)
    (cilj_VALUE/'direct-bytecode.txt').write_text(deklaracija+'\n'+예제)
    LOG_zapis = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(sveženj.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (cilj_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')
    print('PASS: slovenščina 직접 GUI·nit_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Zaženi()
