#!/usr/bin/env python3
"""nativo 커널의 shell, 프로세스 E_S, Unicode GUI 터미널을 real_dados raspi4b에서 testes."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Executar_comando import ação_raiz, comando


def iniciar():
    saída = ação_raiz / 'build/verification/shell'; saída.mkdir(parents=True, exist_ok=True)
    validação_relatar = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((ação_raiz / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcrição = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Processo = subprocess.Popen(comando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Processo.stdout,selectors.EVENT_READ)
        def receber_email(favorito, execução_TEMPOLIMITE=45):
            dados=bytearray(); encerrar_DESLOC=time.monotonic()+execução_TEMPOLIMITE
            while favorito not in dados:
                if time.monotonic()>encerrar_DESLOC or Processo.poll() is not None: raise AssertionError('UART timeout/exit: '+dados.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    fragmento_VALOR=누름값.fileobj.read(4096)
                    if fragmento_VALOR: dados.extend(fragmento_VALOR); transcrição.extend(fragmento_VALOR)
                if b'PANIC:' in dados or b'FAIL ' in dados: raise AssertionError(dados)
            return dados.decode('utf-8','replace').replace('\r\n','\n')
        def enviar(dados, favorito=b'jkoros-native> '):
            Processo.stdin.write(dados); Processo.stdin.flush(); return receber_email(favorito)
        def shell(linha_de_entrada, *예상결과):
            resultado=enviar(linha_de_entrada.encode()+b'\n')
            for VALOR in 예상결과: assert VALOR in resultado, (linha_de_entrada,VALOR,resultado)
            return resultado
        def ficheiro(Nome):
            texto=shell('hex '+Nome,'HEX BEGIN','HEX END'); busca_RC=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',texto,re.S)
            dados=bytes.fromhex(''.join(busca_RC.group(2).split())); assert len(dados)==int(busca_RC.group(1)); return dados
        try:
            receber_email(b'jkoros-native> ')
            shell('mkdir 작업; cd 작업; pwd','/작업')
            shell('mkdir 하위; echo "한글 dados 😀" > saudação_ae353e94.txt')
            assert ficheiro('saudação_ae353e94.txt')=='한글 dados 😀\n'.encode()
            shell('cp saudação_ae353e94.txt copiar_VALOR.txt; mv copiar_VALOR.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 dados 😀')
            shell('cd 하위; cat ../saudação_ae353e94.txt; cat /작업/saudação_ae353e94.txt; pwd','한글 dados 😀','/작업/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp saudação_ae353e94.txt saudação_ae353e94.txt; echo $?','1\n'); assert ficheiro('saudação_ae353e94.txt')=='한글 dados 😀\n'.encode()
            shell('export saudação_ae353e94=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ficheiro('saudação_ae353e94.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ficheiro('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > instrução_VALOR; echo two >> instrução_VALOR; echo three >> instrução_VALOR')
            shell('cat < instrução_VALOR | grep t | tee 추림 | wc -l','2\n'); assert ficheiro('추림')==b'two\nthree\n'
            shell('head -n 1 instrução_VALOR > câmera_frontal_VALOR; tail -n 1 instrução_VALOR > BACK_VALOR'); assert ficheiro('앞')==b'one\n'; assert ficheiro('뒤')==b'three\n'
            shell('grep absent instrução_VALOR; echo $?','1\n')
            shell('echo untouched > proteger_VALOR')
            shell('echo destroyed > proteger_VALOR |','명령이 빠졌습니다'); assert ficheiro('proteger_VALOR')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> proteger_VALOR','번호를 지정한 ficheiro descritor_entrada E_S mudar_MODO'); assert ficheiro('proteger_VALOR')==b'untouched\n'
            shell('rm 빈파일 리터럴 instrução_VALOR 추림 câmera_frontal_VALOR BACK_VALOR proteger_VALOR')
            validação_relatar['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > app_f5044b9b.txt"); assert ficheiro('app_f5044b9b.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < app_f5044b9b.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 'erro -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/app_f5044b9b.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ficheiro('/작업/자바.txt')
            shell('cd 작업; echo "echo script > execução_RC" > comando.sh; echo "false || echo recovered >> execução_RC" >> comando.sh; sh comando.sh')
            assert ficheiro('execução_RC')==b'script\nrecovered\n'
            shell('rm execução_RC; echo "exit 7" > sair_app.sh; sh sair_app.sh; echo $?','7\n')
            shell('rm sair_app.sh comando.sh app_f5044b9b.txt 자바.txt saudação_ae353e94.txt; cd /; rmdir 작업')
            validação_relatar['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            resultado=enviar(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert resultado.count('history-proof')>=2, resultado
            enviar(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            resultado=enviar(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in resultado, resultado
            resultado=enviar(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in resultado,resultado
            resultado=enviar('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in resultado,resultado
            긴글='한글'*50
            resultado=enviar(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in resultado
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "한글 terminal ABC xyz 012 😀"','한글 terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as cliente:
                cliente.settimeout(10); cliente.connect(str(모의제어접속))
                with cliente.makefile('rwb') as fluxo_VALOR:
                    json.loads(fluxo_VALOR.readline())
                    def 호출(Nome,argumento_MATRIZ=None):
                        rede_email={'execute':Nome}
                        if argumento_MATRIZ: rede_email['arguments']=argumento_MATRIZ
                        fluxo_VALOR.write((json.dumps(rede_email)+'\n').encode()); fluxo_VALOR.flush()
                        while True:
                            resposta=json.loads(fluxo_VALOR.readline())
                            if 'error' in resposta: raise AssertionError(resposta)
                            if 'return' in resposta: return resposta['return']
                    호출('qmp_capabilities')
                    foto=saída/'terminal.ppm'; 호출('screendump',{'filename':str(foto),'format':'ppm'})
                    호출('screendump',{'filename':str(saída/'terminal.png'),'format':'png'})
                    dados=foto.read_bytes().split(b'\n',3)[3]
                    def pixel(coordenada_X,Y_coordenada): return tuple(dados[(Y_coordenada*640+coordenada_X)*3:(Y_coordenada*640+coordenada_X)*3+3])
                    assert pixel(12,48)==(32,80,144),pixel(12,48)
                    assert len(set(pixel(coordenada_X,Y_coordenada) for Y_coordenada in range(100,116) for coordenada_X in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(foto),'format':'ppm'})
                    복원자료=foto.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    enviar(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(saída/'terminal-scroll.png'),'format':'png'})
                    resultado=enviar(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in resultado,resultado
                    shell('rm visible.txt')
                    호출('quit')
            Processo.wait(timeout=5)
            validação_relatar['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validação_relatar['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Processo.poll() is None:
                Processo.terminate()
                try: Processo.wait(timeout=5)
                except subprocess.TimeoutExpired: Processo.kill(); Processo.wait()
            준비살피미.close(); Processo.stdin.close(); Processo.stdout.close()
            (saída/'serial.log').write_bytes(transcrição)
            (saída/'report.json').write_text(json.dumps(validação_relatar,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': iniciar()
