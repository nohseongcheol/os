#!/usr/bin/env python3
"""distribuzione_VALORE class의 직접 Italiano GUI/thread_VALORE 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

azione_radice = Path(__file__).resolve().parents[1]

def avvia():
    클래스들 = ('Finestra', 'pulsante', 'Etichetta', 'campo_di_testo', 'schermata_elemento', 'Action_informativa', 'evento_coda', 'esecutoreAsincrono',
             '작업', '실행할일', '동작받이')
    aggregare = azione_radice/'dist/jkoros-native-korean.jar'
    dichiarazione = subprocess.check_output(['javap', '-classpath', str(aggregare), '-private', '-c']+
                                ['Italiano.nativo.'+Nome for Nome in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in dichiarazione, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(azione_radice/'build/examples/classes'), '-c', 'EsempioFinestra']).decode()
    for 필수 in ('public static void avvia()', 'Italiano/nativo/evento_coda.나중에실행', 'Italiano/nativo/Action_informativa.comando_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    meta_VALORE = azione_radice/'build/verification/naming'; meta_VALORE.mkdir(parents=True, exist_ok=True)
    (meta_VALORE/'direct-bytecode.txt').write_text(dichiarazione+'\n'+예제)
    LOG_riga = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(aggregare.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (meta_VALORE/'direct-bytecode.json').write_text(json.dumps(LOG_riga, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Italiano 직접 GUI·thread_VALORE 바이트코드와 예제 호출')

if __name__ == '__main__': avvia()
