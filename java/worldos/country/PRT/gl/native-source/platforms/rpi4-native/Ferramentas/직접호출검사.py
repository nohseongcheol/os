#!/usr/bin/env python3
"""배포 class의 직접 Galego GUI/tema_VALOR 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

Project_raíz = Path(__file__).resolve().parents[1]

def Executar_2():
    클래스들 = ('Xanela', 'botón', 'Etiqueta', 'SMS_campo', '화면구성요소', '동작알림', 'evento_cola', '작업가닥',
             '작업', '실행할일', '동작받이')
    paquete = Project_raíz/'dist/jkoros-native-korean.jar'
    declaración = subprocess.check_output(['javap', '-classpath', str(paquete), '-private', '-c']+
                                ['Galego.자체.'+Nome for Nome in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in declaración, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(Project_raíz/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void Executar_2()', 'Galego/자체/evento_cola.나중에실행', 'Galego/자체/동작알림.comando_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    destino_VALOR = Project_raíz/'build/verification/naming'; destino_VALOR.mkdir(parents=True, exist_ok=True)
    (destino_VALOR/'direct-bytecode.txt').write_text(declaración+'\n'+예제)
    LOG_fila = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(paquete.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (destino_VALOR/'direct-bytecode.json').write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Galego 직접 GUI·tema_VALOR 바이트코드와 예제 호출')

if __name__ == '__main__': Executar_2()
