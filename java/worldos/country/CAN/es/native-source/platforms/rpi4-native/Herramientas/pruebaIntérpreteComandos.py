#!/usr/bin/env python3
"""propio 커널의 intérpreteComandos, 프로세스 salidaEntrada, Unicode GUI 터미널을 datosEfectivo raspi4b에서 Pruebas."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ejecutarComando import raízProyecto, comando


def ponerEnMarcha():
    salida = raízProyecto / 'build/verification/shell'; salida.mkdir(parents=True, exist_ok=True)
    informeValidación = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((raízProyecto / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcripción = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as rutaTrabajoEnCurso:
        conexiónControlDoblePrueba = Path(rutaTrabajoEnCurso) / 'qmp.sock'
        proceso = subprocess.Popen(comando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(conexiónControlDoblePrueba)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        monitorEstadoDisponibilidad=selectors.DefaultSelector(); monitorEstadoDisponibilidad.register(proceso.stdout,selectors.EVENT_READ)
        def recibirMensaje(marcador, tiempoEsperaEjecución=45):
            Datos=bytearray(); desfaseFin=time.monotonic()+tiempoEsperaEjecución
            while marcador not in Datos:
                if time.monotonic()>desfaseFin or proceso.poll() is not None: raise AssertionError('UART timeout/exit: '+Datos.decode('utf-8','replace'))
                for valorPulsado,_ in monitorEstadoDisponibilidad.select(.1):
                    valorFragmento=valorPulsado.fileobj.read(4096)
                    if valorFragmento: Datos.extend(valorFragmento); transcripción.extend(valorFragmento)
                if b'PANIC:' in Datos or b'FAIL ' in Datos: raise AssertionError(Datos)
            return Datos.decode('utf-8','replace').replace('\r\n','\n')
        def enviar(Datos, marcador=b'jkoros-native> '):
            proceso.stdin.write(Datos); proceso.stdin.flush(); return recibirMensaje(marcador)
        def intérpreteComandos(línea, *esperado):
            resultado=enviar(línea.encode()+b'\n')
            for valor in esperado: assert valor in resultado, (línea,valor,resultado)
            return resultado
        def Archivo(nombre):
            texto=intérpreteComandos('hex '+nombre,'HEX BEGIN','HEX END'); buscarCoincidenciaResultado=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',texto,re.S)
            Datos=bytes.fromhex(''.join(buscarCoincidenciaResultado.group(2).split())); assert len(Datos)==int(buscarCoincidenciaResultado.group(1)); return Datos
        try:
            recibirMensaje(b'jkoros-native> ')
            intérpreteComandos('mkdir Tarea; cd Tarea; pwd','/Tarea')
            intérpreteComandos('mkdir 하위; echo "한글 Datos 😀" > Saludo.txt')
            assert Archivo('Saludo.txt')=='한글 Datos 😀\n'.encode()
            intérpreteComandos('cp Saludo.txt copiarValor.txt; mv copiarValor.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 Datos 😀')
            intérpreteComandos('cd 하위; cat ../Saludo.txt; cat /Tarea/Saludo.txt; pwd','한글 Datos 😀','/Tarea/하위')
            intérpreteComandos('cd ..; rmdir 하위; echo $?','1\n')
            intérpreteComandos('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            intérpreteComandos('cp Saludo.txt Saludo.txt; echo $?','1\n'); assert Archivo('Saludo.txt')=='한글 Datos 😀\n'.encode()
            intérpreteComandos('export Saludo=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/Tarea','GOOD')
            assert b'BAD\n' not in Archivo('Saludo.txt')
            intérpreteComandos("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Archivo('리터럴')=='$인사\n누리\n'.encode()
            intérpreteComandos('echo one > valorInstrucción; echo two >> valorInstrucción; echo three >> valorInstrucción')
            intérpreteComandos('cat < valorInstrucción | grep t | tee 추림 | wc -l','2\n'); assert Archivo('추림')==b'two\nthree\n'
            intérpreteComandos('head -n 1 valorInstrucción > valorLadoDelantero; tail -n 1 valorInstrucción > valorLadoPosterior'); assert Archivo('앞')==b'one\n'; assert Archivo('뒤')==b'three\n'
            intérpreteComandos('grep absent valorInstrucción; echo $?','1\n')
            intérpreteComandos('echo untouched > protegerValor')
            intérpreteComandos('echo destroyed > protegerValor |','명령이 빠졌습니다'); assert Archivo('protegerValor')==b'untouched\n'
            intérpreteComandos('echo "oops','따옴표가 닫히지 않았습니다')
            intérpreteComandos('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            intérpreteComandos('echo bad 2> protegerValor','번호를 지정한 Archivo entradaElementoDescriptor salidaEntrada modoConmutar'); assert Archivo('protegerValor')==b'untouched\n'
            intérpreteComandos('rm 빈파일 리터럴 valorInstrucción 추림 valorLadoDelantero valorLadoPosterior protegerValor')
            informeValidación['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            intérpreteComandos("python -c 'print(123)' | wc -c",'4\n')
            intérpreteComandos("python -c 'print(456)' > Programa.txt"); assert Archivo('Programa.txt')==b'456\n'
            intérpreteComandos("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            intérpreteComandos("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < Programa.txt", "b'456\\n'", "b''")
            intérpreteComandos("python -c 'print(\"x\"*17000)' | wc -c", 'error -28')
            intérpreteComandos('echo recovered | wc -c','10\n')
            intérpreteComandos("python -c 'import jkoros; print(jkoros.read("+'"/Tarea/Programa.txt"'+"))'",'456','exit 0')
            intérpreteComandos('cd /; javac Hello.java','Compiled:','exit 0')
            intérpreteComandos('java Hello > /Tarea/Java.txt'); assert '안녕하세요'.encode() in Archivo('/Tarea/Java.txt')
            intérpreteComandos('cd Tarea; echo "echo script > resultadoEjecución" > comando.sh; echo "false || echo recovered >> resultadoEjecución" >> comando.sh; sh comando.sh')
            assert Archivo('resultadoEjecución')==b'script\nrecovered\n'
            intérpreteComandos('rm resultadoEjecución; echo "exit 7" > programaSalir.sh; sh programaSalir.sh; echo $?','7\n')
            intérpreteComandos('rm programaSalir.sh comando.sh Programa.txt Java.txt Saludo.txt; cd /; rmdir Tarea')
            informeValidación['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            intérpreteComandos('echo history-proof','history-proof')
            resultado=enviar(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert resultado.count('history-proof')>=2, resultado
            enviar(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            resultado=enviar(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in resultado, resultado
            resultado=enviar(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in resultado,resultado
            resultado=enviar('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in resultado,resultado
            textoLargo='한글'*50
            resultado=enviar(('echo '+textoLargo+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+textoLargo+'\r\njkoros-native> ').encode()); assert '\n'+textoLargo+'\n' in resultado
            intérpreteComandos('terminal','TERMINAL READY')
            intérpreteComandos('clear')
            intérpreteComandos('echo "한글 terminal ABC xyz 012 😀"','한글 terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as cliente:
                cliente.settimeout(10); cliente.connect(str(conexiónControlDoblePrueba))
                with cliente.makefile('rwb') as valorFlujo:
                    json.loads(valorFlujo.readline())
                    def invocar(nombre,arregloArgumento=None):
                        mensajeRed={'execute':nombre}
                        if arregloArgumento: mensajeRed['arguments']=arregloArgumento
                        valorFlujo.write((json.dumps(mensajeRed)+'\n').encode()); valorFlujo.flush()
                        while True:
                            respuesta=json.loads(valorFlujo.readline())
                            if 'error' in respuesta: raise AssertionError(respuesta)
                            if 'return' in respuesta: return respuesta['return']
                    invocar('qmp_capabilities')
                    imagen=salida/'terminal.ppm'; invocar('screendump',{'filename':str(imagen),'format':'ppm'})
                    invocar('screendump',{'filename':str(salida/'terminal.png'),'format':'png'})
                    Datos=imagen.read_bytes().split(b'\n',3)[3]
                    def píxel(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical): return tuple(Datos[(coordenadaCoordenadaVertical*640+coordenadaCoordenadaHorizontal)*3:(coordenadaCoordenadaVertical*640+coordenadaCoordenadaHorizontal)*3+3])
                    assert píxel(12,48)==(32,80,144),píxel(12,48)
                    assert len(set(píxel(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical) for coordenadaCoordenadaVertical in range(100,116) for coordenadaCoordenadaHorizontal in range(24,56)))>1,'Hangul glyphs missing'
                    intérpreteComandos('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    intérpreteComandos("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    invocar('screendump',{'filename':str(imagen),'format':'ppm'})
                    datosRestaurado=imagen.read_bytes().split(b'\n',3)[3]
                    assert tuple(datosRestaurado[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    intérpreteComandos('echo test > visible.txt; cat visible.txt','test')
                    for índiceOrdinal in range(27): intérpreteComandos('echo scroll-'+str(índiceOrdinal),'scroll-'+str(índiceOrdinal))
                    enviar(b'\x1b[5~\x1b[6~\n')
                    invocar('screendump',{'filename':str(salida/'terminal-scroll.png'),'format':'png'})
                    resultado=enviar(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in resultado,resultado
                    intérpreteComandos('rm visible.txt')
                    invocar('quit')
            proceso.wait(timeout=5)
            informeValidación['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            informeValidación['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if proceso.poll() is None:
                proceso.terminate()
                try: proceso.wait(timeout=5)
                except subprocess.TimeoutExpired: proceso.kill(); proceso.wait()
            monitorEstadoDisponibilidad.close(); proceso.stdin.close(); proceso.stdout.close()
            (salida/'serial.log').write_bytes(transcripción)
            (salida/'report.json').write_text(json.dumps(informeValidación,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ponerEnMarcha()
