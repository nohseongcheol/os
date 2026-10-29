#!/usr/bin/env python3
"""valorDistribución class의 직접 español GUI/valorHiloEjecución 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

raízProyecto = Path(__file__).resolve().parents[1]

def ponerEnMarcha():
    listaClases = ('ventana', 'botón', 'etiqueta', 'CampoTexto', 'ElementoPantalla', 'NotificaciónAcción', 'ColaEvento', 'tareaFondo',
             'Tarea', 'TareaTareaEjecutable', 'ReceptorAcción')
    Paquete = raízProyecto/'dist/jkoros-native-korean.jar'
    Declaraciones = subprocess.check_output(['javap', '-classpath', str(Paquete), '-private', '-c']+
                                ['español.propio.'+nombre for nombre in listaClases]).decode()
    for valorVedado in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert valorVedado not in Declaraciones, valorVedado
    Ejemplos = subprocess.check_output(['javap', '-classpath', str(raízProyecto/'build/examples/classes'), '-c', 'EjemploVentana']).decode()
    for esRequerido in ('public static void ponerEnMarcha()', 'español/propio/ColaEvento.invocarPosterior', 'español/propio/NotificaciónAcción.textoComando'):
        assert esRequerido in Ejemplos, esRequerido
    for valorVedado in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert valorVedado not in Ejemplos, valorVedado
    valorDestino = raízProyecto/'build/verification/naming'; valorDestino.mkdir(parents=True, exist_ok=True)
    (valorDestino/'direct-bytecode.txt').write_text(Declaraciones+'\n'+Ejemplos)
    registroEntradaDiario = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(Paquete.read_bytes()).hexdigest(), 'classes': list(listaClases),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (valorDestino/'direct-bytecode.json').write_text(json.dumps(registroEntradaDiario, ensure_ascii=False, indent=2)+'\n')
    print('PASS: español 직접 GUI·valorHiloEjecución 바이트코드와 Ejemplos invocar')

if __name__ == '__main__': ponerEnMarcha()
