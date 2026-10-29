#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from executar_comando import Project_raíz,Orde

def Executar_2():
    destino_VALOR_cargo=Project_raíz/'build/verification/windows';destino_VALOR_cargo.mkdir(parents=True,exist_ok=True)
    validación_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest()};LOG_fila=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        datos_cargo=subprocess.Popen(Orde()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(datos_cargo.stdout,selectors.EVENT_READ)
        def agarradoira_evento(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                SEGUNDO_VALOR=누름값.fileobj.read(65536)
                if SEGUNDO_VALOR:LOG_fila.extend(SEGUNDO_VALOR)
            assert b'PANIC:' not in LOG_fila and b'HALTED' not in LOG_fila,LOG_fila[-2048:]
        def 기다리기(확인표시,ao_corrente_cargo,초단위=50):
            finalizar_DESPRAZAMENTO=time.monotonic()+초단위
            while 확인표시 not in LOG_fila[ao_corrente_cargo:]:
                if time.monotonic()>finalizar_DESPRAZAMENTO or datos_cargo.poll() is not None:raise AssertionError(LOG_fila[ao_corrente_cargo:].decode('utf-8','replace'))
                agarradoira_evento()
            return bytes(LOG_fila[ao_corrente_cargo:])
        def enviar(SEGUNDO_VALOR,확인표시=b'jkoros-native> '):
            ao_corrente_cargo=len(LOG_fila);datos_cargo.stdin.write(SEGUNDO_VALOR);datos_cargo.stdin.flush();return 기다리기(확인표시,ao_corrente_cargo)
        def shell(cadea_datos):return enviar((cadea_datos+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def atallo_VALOR(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def clic_botón(X_coordenada,Y_coordenada):return bytes([30,1,1,X_coordenada&255,X_coordenada>>8,Y_coordenada&255,Y_coordenada>>8,30,1,0,X_coordenada&255,X_coordenada>>8,Y_coordenada&255,Y_coordenada>>8])
        def comando_MODO():
            datos_cargo.stdin.write(b'\x1b');datos_cargo.stdin.flush();finalizar_DESPRAZAMENTO=time.monotonic()+.2
            while time.monotonic()<finalizar_DESPRAZAMENTO:agarradoira_evento(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');agarradoira_evento(.3)
            shell('mkdir first; cd first; export NAME=one')
            enviar('vi 첫째.py\n'.encode(),b'NORMAL')
            enviar('i값 = 21\nprint(VALOR * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            finalizar_DESPRAZAMENTO=time.monotonic()+3
            while time.monotonic()<finalizar_DESPRAZAMENTO:agarradoira_evento(.1)
            enviar(atallo_VALOR(1),b'TERMINAL FOCUS 2');agarradoira_evento(.2)
            assert b'/\r\n' in shell('pwd')
            shell('export NAME=two')
            enviar('vi 둘째.txt\n'.encode(),b'NORMAL')
            enviar('i두 번째 Xanela\n'.encode(),b'INSERT')
            enviar(clic_botón(180,12),b'TERMINAL FOCUS 1');agarradoira_evento(.2)
            comando_MODO();enviar(b':wq\r')
            assert b'one:/first' in shell('echo "$NAME:$PWD"')
            assert 'VALOR = 21\r\nprint(VALOR * 2)'.encode() in shell('cat 첫째.py')
            RESULTANTE=shell('python 첫째.py');assert b'42\r\n' in RESULTANTE,RESULTANTE
            # Close the first shell with its actual title-bar X; second editor resumes.
            enviar(clic_botón(560,63),b'TERMINAL FOCUS 2');agarradoira_evento(.2)
            comando_MODO();enviar(b':wq\r')
            assert b'two:/' in shell('echo "$NAME:$PWD"')
            assert '두 번째 Xanela'.encode() in shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            enviar('vi 둘째.txt\n'.encode(),b'NORMAL');enviar(b'xu',b'NORMAL')
            enviar(b'iX',b'INSERT');comando_MODO();enviar(b':q\r',b'Unsaved')
            enviar(b':q!\r');assert '두 번째 Xanela'.encode() in shell('cat 둘째.txt')
            enviar(atallo_VALOR(1),b'TERMINAL FOCUS 1');agarradoira_evento(.2)
            enviar(atallo_VALOR(1),b'TERMINAL FOCUS 3');agarradoira_evento(.2)
            enviar(atallo_VALOR(1),b'TERMINAL FOCUS 4');agarradoira_evento(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            datos_cargo.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));datos_cargo.stdin.flush()
            shell('echo DRAGGED_OK')
            enviar('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            enviar('i저장하지 않은 datos'.encode(),b'INSERT')
            enviar(clic_botón(578,97),b'TERMINAL FOCUS 3');agarradoira_evento(.2)
            assert '버릴문서.txt'.encode() not in shell('ls')
            enviar(atallo_VALOR(1),b'TERMINAL FOCUS 4');agarradoira_evento(.2)
            shell('echo REUSED_WINDOW_OK')
            Completadas_cantidade=LOG_fila.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Completadas_cantidade)
            # UART completion precedes the next QEMU display refresh.
            finalizar_DESPRAZAMENTO=time.monotonic()+.3
            while time.monotonic()<finalizar_DESPRAZAMENTO:agarradoira_evento(.05)
            with socket.socket(socket.AF_UNIX) as código_de_carácter:
                código_de_carácter.settimeout(10);código_de_carácter.connect(str(모의제어접속))
                with código_de_carácter.makefile('rwb') as Ficheiro_introdución:
                    json.loads(Ficheiro_introdución.readline())
                    for solicitude_VALOR in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destino_VALOR_cargo/'four-terminals.png'),'format':'png'}}):
                        Ficheiro_introdución.write((json.dumps(solicitude_VALOR)+'\n').encode());Ficheiro_introdución.flush()
                        while True:
                            반환값=json.loads(Ficheiro_introdución.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(destino_VALOR_cargo/'four-terminals.png')).convert('RGB')
            for par_de_coordenadas,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(par_de_coordenadas)==색상,(par_de_coordenadas,화소들.getpixel(par_de_coordenadas))
            shell('echo FOUR_WINDOWS_OK')
            validación_informe.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if datos_cargo.poll() is None:datos_cargo.terminate()
            try:datos_cargo.wait(timeout=5)
            except subprocess.TimeoutExpired:datos_cargo.kill();datos_cargo.wait()
            선택기.close();datos_cargo.stdin.close();datos_cargo.stdout.close();(destino_VALOR_cargo/'serial.log').write_bytes(LOG_fila);(destino_VALOR_cargo/'report.json').write_text(json.dumps(validación_informe,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Executar_2()
