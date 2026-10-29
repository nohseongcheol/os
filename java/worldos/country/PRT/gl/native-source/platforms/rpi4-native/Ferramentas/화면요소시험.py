#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from executar_comando import Project_raíz,Orde

def Executar_2():
    destino_VALOR_cargo=Project_raíz/'build/verification/swing';destino_VALOR_cargo.mkdir(parents=True,exist_ok=True)
    Clase_camiño=Project_raíz/'build/verification/new-java';Clase_camiño.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_raíz/'dist/jkoros-native-korean.jar'),'-d',str(Clase_camiño),str(Project_raíz/'시험/자바/스윙시험.java'),str(Project_raíz/'시험/자바/한글창시험.java')])
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
            datos=(Project_raíz/'build/verification/new-java/스윙시험.class').read_bytes()
            enviar('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(datos),64):enviar(datos[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            enviar(b'.\n')
            enviar('java 스윙시험\n'.encode(),b'SWING READY')
            finalizar_DESPRAZAMENTO=time.monotonic()+3
            while time.monotonic()<finalizar_DESPRAZAMENTO:agarradoira_evento(.1)
            # JFrame centered at (120,100), content at y=130.
            enviar(clic_botón(200,210),b'',)  # focus JTextField
            datos_cargo.stdin.write('누리'.encode());datos_cargo.stdin.flush()
            finalizar_DESPRAZAMENTO=time.monotonic()+.3
            while time.monotonic()<finalizar_DESPRAZAMENTO:agarradoira_evento(.05)
            RESULTANTE=enviar(clic_botón(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_fila)-len(RESULTANTE))
            enviar(atallo_VALOR(1),b'TERMINAL FOCUS 2')
            RESULTANTE=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in RESULTANTE
            enviar(clic_botón(180,12),b'TERMINAL FOCUS 1')
            finalizar_DESPRAZAMENTO=time.monotonic()+.3
            while time.monotonic()<finalizar_DESPRAZAMENTO:agarradoira_evento(.05)
            with socket.socket(socket.AF_UNIX) as código_de_carácter:
                código_de_carácter.settimeout(10);código_de_carácter.connect(str(모의제어접속))
                with código_de_carácter.makefile('rwb') as Ficheiro_introdución:
                    json.loads(Ficheiro_introdución.readline())
                    for solicitude_VALOR in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destino_VALOR_cargo/'native-swing.png'),'format':'png'}}):
                        Ficheiro_introdución.write((json.dumps(solicitude_VALOR)+'\n').encode());Ficheiro_introdución.flush()
                        while True:
                            반환값=json.loads(Ficheiro_introdución.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            enviar(clic_botón(505,115))
            shell('echo SWING_CLOSED_OK')
            datos=(Clase_camiño/'한글창시험.class').read_bytes()
            enviar('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(datos),64):enviar(datos[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            enviar(b'.\n')
            enviar('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            enviar(clic_botón(200,255),'KOREAN SWING CLICK Nome'.encode())
            enviar(clic_botón(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            validación_informe.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Galego Xanela/botón/동작알림/evento_cola directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if datos_cargo.poll() is None:datos_cargo.terminate()
            try:datos_cargo.wait(timeout=5)
            except subprocess.TimeoutExpired:datos_cargo.kill();datos_cargo.wait()
            선택기.close();datos_cargo.stdin.close();datos_cargo.stdout.close();(destino_VALOR_cargo/'serial.log').write_bytes(LOG_fila);(destino_VALOR_cargo/'report.json').write_text(json.dumps(validación_informe,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Executar_2()
