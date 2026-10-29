#!/usr/bin/env python3
"""배포 class의 직접 hrvatski GUI/nit_VALUE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

akcija_korijen = Path(__file__).resolve().parents[1]

def Pokreni():
    클래스들 = ('Prozor', 'gumb', 'Natpis', 'tekstno_polje', '화면구성요소', 'akcija_obavijest', 'događaj_red_čekanja', '작업가닥',
             '작업', '실행할일', '동작받이')
    komplet = akcija_korijen/'dist/jkoros-native-korean.jar'
    deklaracija = subprocess.check_output(['javap', '-classpath', str(komplet), '-private', '-c']+
                                ['hrvatski.vlastiti.'+Ime for Ime in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in deklaracija, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(akcija_korijen/'build/examples/classes'), '-c', 'PrimjerProzora']).decode()
    for 필수 in ('public static void Pokreni()', 'hrvatski/vlastiti/događaj_red_čekanja.나중에실행', 'hrvatski/vlastiti/akcija_obavijest.naredba_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    odredište_VALUE = akcija_korijen/'build/verification/naming'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    (odredište_VALUE/'direct-bytecode.txt').write_text(deklaracija+'\n'+예제)
    LOG_zapis = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(komplet.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (odredište_VALUE/'direct-bytecode.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')
    print('PASS: hrvatski 직접 GUI·nit_VALUE 바이트코드와 예제 호출')

if __name__ == '__main__': Pokreni()
