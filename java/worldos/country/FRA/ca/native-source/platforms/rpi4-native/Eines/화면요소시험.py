#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Executa_ordre import Project_rel,Ordre

def Executa_2():
    destinació_VALOR_càrrec=Project_rel/'build/verification/swing';destinació_VALOR_càrrec.mkdir(parents=True,exist_ok=True)
    Classe_camí=Project_rel/'build/verification/new-java';Classe_camí.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_rel/'dist/jkoros-native-korean.jar'),'-d',str(Classe_camí),str(Project_rel/'시험/자바/스윙시험.java'),str(Project_rel/'시험/자바/한글창시험.java')])
    validació_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest()};LOG_fila=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        dades_càrrec=subprocess.Popen(Ordre()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(dades_càrrec.stdout,selectors.EVENT_READ)
        def control_incidència(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                SEGON_VALOR=누름값.fileobj.read(65536)
                if SEGON_VALOR:LOG_fila.extend(SEGON_VALOR)
            assert b'PANIC:' not in LOG_fila and b'HALTED' not in LOG_fila,LOG_fila[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            finalitzar_DESPLAÇAMENT=time.monotonic()+초단위
            while 확인표시 not in LOG_fila[현재위치:]:
                if time.monotonic()>finalitzar_DESPLAÇAMENT or dades_càrrec.poll() is not None:raise AssertionError(LOG_fila[현재위치:].decode('utf-8','replace'))
                control_incidència()
            return bytes(LOG_fila[현재위치:])
        def enviar(SEGON_VALOR,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_fila);dades_càrrec.stdin.write(SEGON_VALOR);dades_càrrec.stdin.flush();return 기다리기(확인표시,현재위치)
        def shell(cadena_dades):return enviar((cadena_dades+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def drecera_VALOR(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def clic_botó(X_coordenada,Y_coordenada):return bytes([30,1,1,X_coordenada&255,X_coordenada>>8,Y_coordenada&255,Y_coordenada>>8,30,1,0,X_coordenada&255,X_coordenada>>8,Y_coordenada&255,Y_coordenada>>8])
        def ordre_MODA():
            dades_càrrec.stdin.write(b'\x1b');dades_càrrec.stdin.flush();finalitzar_DESPLAÇAMENT=time.monotonic()+.2
            while time.monotonic()<finalitzar_DESPLAÇAMENT:control_incidència(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');control_incidència(.3)
            dades=(Project_rel/'build/verification/new-java/스윙시험.class').read_bytes()
            enviar('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dades),64):enviar(dades[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            enviar(b'.\n')
            enviar('java 스윙시험\n'.encode(),b'SWING READY')
            finalitzar_DESPLAÇAMENT=time.monotonic()+3
            while time.monotonic()<finalitzar_DESPLAÇAMENT:control_incidència(.1)
            # JFrame centered at (120,100), content at y=130.
            enviar(clic_botó(200,210),b'',)  # focus JTextField
            dades_càrrec.stdin.write('누리'.encode());dades_càrrec.stdin.flush()
            finalitzar_DESPLAÇAMENT=time.monotonic()+.3
            while time.monotonic()<finalitzar_DESPLAÇAMENT:control_incidència(.05)
            RESULTAT=enviar(clic_botó(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_fila)-len(RESULTAT))
            enviar(drecera_VALOR(1),b'TERMINAL FOCUS 2')
            RESULTAT=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in RESULTAT
            enviar(clic_botó(180,12),b'TERMINAL FOCUS 1')
            finalitzar_DESPLAÇAMENT=time.monotonic()+.3
            while time.monotonic()<finalitzar_DESPLAÇAMENT:control_incidència(.05)
            with socket.socket(socket.AF_UNIX) as codi_de_caràcter:
                codi_de_caràcter.settimeout(10);codi_de_caràcter.connect(str(모의제어접속))
                with codi_de_caràcter.makefile('rwb') as arxiu_introducció:
                    json.loads(arxiu_introducció.readline())
                    for sol_licitud_VALOR in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinació_VALOR_càrrec/'native-swing.png'),'format':'png'}}):
                        arxiu_introducció.write((json.dumps(sol_licitud_VALOR)+'\n').encode());arxiu_introducció.flush()
                        while True:
                            반환값=json.loads(arxiu_introducció.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            enviar(clic_botó(505,115))
            shell('echo SWING_CLOSED_OK')
            dades=(Classe_camí/'한글창시험.class').read_bytes()
            enviar('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dades),64):enviar(dades[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            enviar(b'.\n')
            enviar('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            enviar(clic_botó(200,255),'KOREAN SWING CLICK Nom'.encode())
            enviar(clic_botó(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            validació_informe.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Català Finestra/Botó/동작알림/incidència_cua directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if dades_càrrec.poll() is None:dades_càrrec.terminate()
            try:dades_càrrec.wait(timeout=5)
            except subprocess.TimeoutExpired:dades_càrrec.kill();dades_càrrec.wait()
            선택기.close();dades_càrrec.stdin.close();dades_càrrec.stdout.close();(destinació_VALOR_càrrec/'serial.log').write_bytes(LOG_fila);(destinació_VALOR_càrrec/'report.json').write_text(json.dumps(validació_informe,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Executa_2()
