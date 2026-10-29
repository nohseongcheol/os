#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Executar_comando import ação_raiz,comando

def iniciar():
    destino_VALOR_cargo=ação_raiz/'build/verification/swing';destino_VALOR_cargo.mkdir(parents=True,exist_ok=True)
    aula_caminho=ação_raiz/'build/verification/new-java';aula_caminho.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ação_raiz/'dist/jkoros-native-korean.jar'),'-d',str(aula_caminho),str(ação_raiz/'testes/자바/Swing_teste.java'),str(ação_raiz/'testes/자바/한글창시험.java')])
    validação_relatar={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest()};LOG_linha=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        dados_cargo=subprocess.Popen(comando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        seletor_a916db4e=selectors.DefaultSelector();seletor_a916db4e.register(dados_cargo.stdout,selectors.EVENT_READ)
        def alça_Evento(초단위=.1):
            for 누름값,_ in seletor_a916db4e.select(초단위):
                SEGUNDO_VALOR=누름값.fileobj.read(65536)
                if SEGUNDO_VALOR:LOG_linha.extend(SEGUNDO_VALOR)
            assert b'PANIC:' not in LOG_linha and b'HALTED' not in LOG_linha,LOG_linha[-2048:]
        def 기다리기(favorito,em_dia_cargo,초단위=50):
            encerrar_DESLOC=time.monotonic()+초단위
            while favorito not in LOG_linha[em_dia_cargo:]:
                if time.monotonic()>encerrar_DESLOC or dados_cargo.poll() is not None:raise AssertionError(LOG_linha[em_dia_cargo:].decode('utf-8','replace'))
                alça_Evento()
            return bytes(LOG_linha[em_dia_cargo:])
        def enviar(SEGUNDO_VALOR,favorito=b'jkoros-native> '):
            em_dia_cargo=len(LOG_linha);dados_cargo.stdin.write(SEGUNDO_VALOR);dados_cargo.stdin.flush();return 기다리기(favorito,em_dia_cargo)
        def shell(cadeia_dados):return enviar((cadeia_dados+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def atalho_VALOR(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def clicar_botão(coordenada_X,Y_coordenada):return bytes([30,1,1,coordenada_X&255,coordenada_X>>8,Y_coordenada&255,Y_coordenada>>8,30,1,0,coordenada_X&255,coordenada_X>>8,Y_coordenada&255,Y_coordenada>>8])
        def comando_MODO():
            dados_cargo.stdin.write(b'\x1b');dados_cargo.stdin.flush();encerrar_DESLOC=time.monotonic()+.2
            while time.monotonic()<encerrar_DESLOC:alça_Evento(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');alça_Evento(.3)
            dados=(ação_raiz/'build/verification/new-java/Swing_teste.class').read_bytes()
            enviar('load Swing_teste.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dados),64):enviar(dados[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            enviar(b'.\n')
            enviar('java Swing_teste\n'.encode(),b'SWING READY')
            encerrar_DESLOC=time.monotonic()+3
            while time.monotonic()<encerrar_DESLOC:alça_Evento(.1)
            # JFrame centered at (120,100), content at y=130.
            enviar(clicar_botão(200,210),b'',)  # focus JTextField
            dados_cargo.stdin.write('누리'.encode());dados_cargo.stdin.flush()
            encerrar_DESLOC=time.monotonic()+.3
            while time.monotonic()<encerrar_DESLOC:alça_Evento(.05)
            resultado=enviar(clicar_botão(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_linha)-len(resultado))
            enviar(atalho_VALOR(1),b'TERMINAL FOCUS 2')
            resultado=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in resultado
            enviar(clicar_botão(180,12),b'TERMINAL FOCUS 1')
            encerrar_DESLOC=time.monotonic()+.3
            while time.monotonic()<encerrar_DESLOC:alça_Evento(.05)
            with socket.socket(socket.AF_UNIX) as ponto_de_código:
                ponto_de_código.settimeout(10);ponto_de_código.connect(str(모의제어접속))
                with ponto_de_código.makefile('rwb') as Arquivo_entrada:
                    json.loads(Arquivo_entrada.readline())
                    for solicitação_VALOR in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destino_VALOR_cargo/'native-swing.png'),'format':'png'}}):
                        Arquivo_entrada.write((json.dumps(solicitação_VALOR)+'\n').encode());Arquivo_entrada.flush()
                        while True:
                            반환값=json.loads(Arquivo_entrada.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            enviar(clicar_botão(505,115))
            shell('echo SWING_CLOSED_OK')
            dados=(aula_caminho/'한글창시험.class').read_bytes()
            enviar('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dados),64):enviar(dados[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            enviar(b'.\n')
            enviar('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            enviar(clicar_botão(200,255),'KOREAN SWING CLICK Nome'.encode())
            enviar(clicar_botão(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            validação_relatar.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Português Janela/botão/Ação_aviso/Evento_Fila directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if dados_cargo.poll() is None:dados_cargo.terminate()
            try:dados_cargo.wait(timeout=5)
            except subprocess.TimeoutExpired:dados_cargo.kill();dados_cargo.wait()
            seletor_a916db4e.close();dados_cargo.stdin.close();dados_cargo.stdout.close();(destino_VALOR_cargo/'serial.log').write_bytes(LOG_linha);(destino_VALOR_cargo/'report.json').write_text(json.dumps(validação_relatar,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':iniciar()
