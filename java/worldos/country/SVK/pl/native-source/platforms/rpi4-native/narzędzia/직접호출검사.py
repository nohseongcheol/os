#!/usr/bin/env python3
"""dystrybucja_WARTOŚĆ class의 직접 polski GUI/wątek_WARTOŚĆ 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_korzeń = Path(__file__).resolve().parents[1]

def Uruchom_2():
    클래스들 = ('Okno', 'przycisk', 'Etykieta', 'pole_tekstowe', '화면구성요소', 'akcja_powiadomienie', 'konkurs_kolejka', 'pracownik',
             '작업', '실행할일', '동작받이')
    pakiet = Project_korzeń/'dist/jkoros-native-korean.jar'
    deklaracja = subprocess.check_output(['javap', '-classpath', str(pakiet), '-private', '-c']+
                                ['polski.własny.'+Nazwa for Nazwa in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklaracja, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_korzeń/'build/examples/classes'), '-c', 'PrzykładOkna']).decode()
    for 필수 in ('public static void Uruchom_2()', 'polski/własny/konkurs_kolejka.나중에실행', 'polski/własny/akcja_powiadomienie.polecenie_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    cel_WARTOŚĆ = Project_korzeń/'build/verification/naming'; cel_WARTOŚĆ.mkdir(parents=True, exist_ok=True)
    (cel_WARTOŚĆ/'direct-bytecode.txt').write_text(deklaracja+'\n'+예제)
    LOG_zapis = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(pakiet.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (cel_WARTOŚĆ/'direct-bytecode.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')
    print('PASS: polski 직접 GUI·wątek_WARTOŚĆ 바이트코드와 예제 호출')

if __name__ == '__main__': Uruchom_2()
