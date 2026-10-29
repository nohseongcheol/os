#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Executar_comando import ação_raiz,comando

def iniciar():
    destino_VALOR_cargo=ação_raiz/'build/verification/windows';destino_VALOR_cargo.mkdir(parents=True,exist_ok=True)
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
            shell('mkdir first; cd first; export NAME=one')
            enviar('vi 첫째.py\n'.encode(),b'NORMAL')
            enviar('i값 = 21\nprint(VALOR * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            encerrar_DESLOC=time.monotonic()+3
            while time.monotonic()<encerrar_DESLOC:alça_Evento(.1)
            enviar(atalho_VALOR(1),b'TERMINAL FOCUS 2');alça_Evento(.2)
            assert b'/\r\n' in shell('pwd')
            shell('export NAME=two')
            enviar('vi 둘째.txt\n'.encode(),b'NORMAL')
            enviar('i두 번째 Janela\n'.encode(),b'INSERT')
            enviar(clicar_botão(180,12),b'TERMINAL FOCUS 1');alça_Evento(.2)
            comando_MODO();enviar(b':wq\r')
            assert b'one:/first' in shell('echo "$NAME:$PWD"')
            assert 'VALOR = 21\r\nprint(VALOR * 2)'.encode() in shell('cat 첫째.py')
            resultado=shell('python 첫째.py');assert b'42\r\n' in resultado,resultado
            # Close the first shell with its actual title-bar X; second editor resumes.
            enviar(clicar_botão(560,63),b'TERMINAL FOCUS 2');alça_Evento(.2)
            comando_MODO();enviar(b':wq\r')
            assert b'two:/' in shell('echo "$NAME:$PWD"')
            assert '두 번째 Janela'.encode() in shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            enviar('vi 둘째.txt\n'.encode(),b'NORMAL');enviar(b'xu',b'NORMAL')
            enviar(b'iX',b'INSERT');comando_MODO();enviar(b':q\r',b'Unsaved')
            enviar(b':q!\r');assert '두 번째 Janela'.encode() in shell('cat 둘째.txt')
            enviar(atalho_VALOR(1),b'TERMINAL FOCUS 1');alça_Evento(.2)
            enviar(atalho_VALOR(1),b'TERMINAL FOCUS 3');alça_Evento(.2)
            enviar(atalho_VALOR(1),b'TERMINAL FOCUS 4');alça_Evento(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            dados_cargo.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));dados_cargo.stdin.flush()
            shell('echo DRAGGED_OK')
            enviar('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            enviar('i저장하지 않은 dados'.encode(),b'INSERT')
            enviar(clicar_botão(578,97),b'TERMINAL FOCUS 3');alça_Evento(.2)
            assert '버릴문서.txt'.encode() not in shell('ls')
            enviar(atalho_VALOR(1),b'TERMINAL FOCUS 4');alça_Evento(.2)
            shell('echo REUSED_WINDOW_OK')
            concluído_valor=LOG_linha.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',concluído_valor)
            # UART completion precedes the next QEMU display refresh.
            encerrar_DESLOC=time.monotonic()+.3
            while time.monotonic()<encerrar_DESLOC:alça_Evento(.05)
            with socket.socket(socket.AF_UNIX) as ponto_de_código:
                ponto_de_código.settimeout(10);ponto_de_código.connect(str(모의제어접속))
                with ponto_de_código.makefile('rwb') as Arquivo_entrada:
                    json.loads(Arquivo_entrada.readline())
                    for solicitação_VALOR in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destino_VALOR_cargo/'four-terminals.png'),'format':'png'}}):
                        Arquivo_entrada.write((json.dumps(solicitação_VALOR)+'\n').encode());Arquivo_entrada.flush()
                        while True:
                            반환값=json.loads(Arquivo_entrada.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(destino_VALOR_cargo/'four-terminals.png')).convert('RGB')
            for par_de_coordenadas,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(par_de_coordenadas)==색상,(par_de_coordenadas,화소들.getpixel(par_de_coordenadas))
            shell('echo FOUR_WINDOWS_OK')
            validação_relatar.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if dados_cargo.poll() is None:dados_cargo.terminate()
            try:dados_cargo.wait(timeout=5)
            except subprocess.TimeoutExpired:dados_cargo.kill();dados_cargo.wait()
            seletor_a916db4e.close();dados_cargo.stdin.close();dados_cargo.stdout.close();(destino_VALOR_cargo/'serial.log').write_bytes(LOG_linha);(destino_VALOR_cargo/'report.json').write_text(json.dumps(validação_relatar,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':iniciar()
