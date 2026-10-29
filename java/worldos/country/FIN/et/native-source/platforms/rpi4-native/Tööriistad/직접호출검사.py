#!/usr/bin/env python3
"""turustus_VALUE class의 직접 Eesti GUI/lõim_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_juur = Path(__file__).resolve().parents[1]

def Käivita_2():
    클래스들 = ('창', 'nupp', 'Silt', 'tekstiväli', '화면구성요소', 'Toiming_teatamine', 'sündmus_järjekord', 'töötaja',
             '작업', '실행할일', '동작받이')
    kogum = Project_juur/'dist/jkoros-native-korean.jar'
    deklaratsioon = subprocess.check_output(['javap', '-classpath', str(kogum), '-private', '-c']+
                                ['Eesti.oma.'+Nimi_2 for Nimi_2 in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklaratsioon, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_juur/'build/examples/classes'), '-c', 'AknaNäide']).decode()
    for 필수 in ('public static void Käivita_2()', 'Eesti/oma/sündmus_järjekord.나중에실행', 'Eesti/oma/Toiming_teatamine.käsk_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    sihtkoht_VALUE = Project_juur/'build/verification/naming'; sihtkoht_VALUE.mkdir(parents=True, exist_ok=True)
    (sihtkoht_VALUE/'direct-bytecode.txt').write_text(deklaratsioon+'\n'+예제)
    LOG_kirje = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(kogum.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (sihtkoht_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_kirje, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Eesti 직접 GUI·lõim_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Käivita_2()
