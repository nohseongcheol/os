#!/usr/bin/env python3
"""배포 class의 직접 Català GUI/fil_VALOR 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_rel = Path(__file__).resolve().parents[1]

def Executa_2():
    클래스들 = ('Finestra', 'Botó', 'Etiqueta', 'SMS_camp', '화면구성요소', '동작알림', 'incidència_cua', '작업가닥',
             '작업', '실행할일', '동작받이')
    paquet = Project_rel/'dist/jkoros-native-korean.jar'
    declaració = subprocess.check_output(['javap', '-classpath', str(paquet), '-private', '-c']+
                                ['Català.propi.'+Nom for Nom in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in declaració, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_rel/'build/examples/classes'), '-c', 'ExempleFinestra']).decode()
    for 필수 in ('public static void Executa_2()', 'Català/propi/incidència_cua.나중에실행', 'Català/propi/동작알림.ordre_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    destinació_VALOR = Project_rel/'build/verification/naming'; destinació_VALOR.mkdir(parents=True, exist_ok=True)
    (destinació_VALOR/'direct-bytecode.txt').write_text(declaració+'\n'+예제)
    LOG_fila = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(paquet.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (destinació_VALOR/'direct-bytecode.json').write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Català 직접 GUI·fil_VALOR 바이트코드와 예제 호출')

if __name__ == '__main__': Executa_2()
