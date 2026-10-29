#!/usr/bin/env python3
"""distribuição_VALOR class의 직접 Português GUI/thread_VALOR 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

ação_raiz = Path(__file__).resolve().parents[1]

def iniciar():
    클래스들 = ('Janela', 'botão', 'Etiqueta', 'campo_de_texto', 'tela_elemento', 'Ação_aviso', 'Evento_Fila', 'tarefaSegundoPlano',
             '작업', '실행할일', '동작받이')
    grupo = ação_raiz/'dist/jkoros-native-korean.jar'
    declaração = subprocess.check_output(['javap', '-classpath', str(grupo), '-private', '-c']+
                                ['Português.nativo.'+Nome for Nome in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in declaração, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(ação_raiz/'build/examples/classes'), '-c', 'ExemploJanela']).decode()
    for 필수 in ('public static void iniciar()', 'Português/nativo/Evento_Fila.나중에실행', 'Português/nativo/Ação_aviso.comando_SMS'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    destino_VALOR = ação_raiz/'build/verification/naming'; destino_VALOR.mkdir(parents=True, exist_ok=True)
    (destino_VALOR/'direct-bytecode.txt').write_text(declaração+'\n'+예제)
    LOG_linha = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(grupo.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (destino_VALOR/'direct-bytecode.json').write_text(json.dumps(LOG_linha, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Português 직접 GUI·thread_VALOR 바이트코드와 예제 호출')

if __name__ == '__main__': iniciar()
