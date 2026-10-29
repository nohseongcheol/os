#!/usr/bin/env python3
"""자체 커널의 shell, 프로세스 E_S, Unicode GUI 터미널을 real_datos raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from executar_comando import Project_raíz, Orde


def Executar_2():
    출력결과 = Project_raíz / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    validación_informe = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_raíz / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proceso = subprocess.Popen(Orde()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proceso.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            datos=bytearray(); finalizar_DESPRAZAMENTO=time.monotonic()+시간제한
            while 확인표시 not in datos:
                if time.monotonic()>finalizar_DESPRAZAMENTO or Proceso.poll() is not None: raise AssertionError('UART timeout/exit: '+datos.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: datos.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in datos or b'FAIL ' in datos: raise AssertionError(datos)
            return datos.decode('utf-8','replace').replace('\r\n','\n')
        def enviar(datos, 확인표시=b'jkoros-native> '):
            Proceso.stdin.write(datos); Proceso.stdin.flush(); return 수신하기(확인표시)
        def shell(Liña, *예상결과):
            RESULTANTE=enviar(Liña.encode()+b'\n')
            for VALOR in 예상결과: assert VALOR in RESULTANTE, (Liña,VALOR,RESULTANTE)
            return RESULTANTE
        def Ficheiro(Nome):
            Texto=shell('hex '+Nome,'HEX BEGIN','HEX END'); ACHAR_medida=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Texto,re.S)
            datos=bytes.fromhex(''.join(ACHAR_medida.group(2).split())); assert len(datos)==int(ACHAR_medida.group(1)); return datos
        try:
            수신하기(b'jkoros-native> ')
            shell('mkdir 작업; cd 작업; pwd','/작업')
            shell('mkdir 하위; echo "한글 datos 😀" > 인사.txt')
            assert Ficheiro('인사.txt')=='한글 datos 😀\n'.encode()
            shell('cp 인사.txt copiar_VALOR.txt; mv copiar_VALOR.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 datos 😀')
            shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 datos 😀','/작업/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert Ficheiro('인사.txt')=='한글 datos 😀\n'.encode()
            shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Ficheiro('인사.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Ficheiro('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > instrución_VALOR; echo two >> instrución_VALOR; echo three >> instrución_VALOR')
            shell('cat < instrución_VALOR | grep t | tee 추림 | wc -l','2\n'); assert Ficheiro('추림')==b'two\nthree\n'
            shell('head -n 1 instrución_VALOR > frontal_VALOR; tail -n 1 instrución_VALOR > ATRÁS_VALOR'); assert Ficheiro('앞')==b'one\n'; assert Ficheiro('뒤')==b'three\n'
            shell('grep absent instrución_VALOR; echo $?','1\n')
            shell('echo untouched > protexer_VALOR')
            shell('echo destroyed > protexer_VALOR |','명령이 빠졌습니다'); assert Ficheiro('protexer_VALOR')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> protexer_VALOR','번호를 지정한 Ficheiro 서술자 E_S mudar_MODO'); assert Ficheiro('protexer_VALOR')==b'untouched\n'
            shell('rm 빈파일 리터럴 instrución_VALOR 추림 frontal_VALOR ATRÁS_VALOR protexer_VALOR')
            validación_informe['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > apl_f5044b9b.txt"); assert Ficheiro('apl_f5044b9b.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < apl_f5044b9b.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 'ERRO -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/apl_f5044b9b.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Ficheiro('/작업/자바.txt')
            shell('cd 작업; echo "echo script > 실행결과" > Orde.sh; echo "false || echo recovered >> 실행결과" >> Orde.sh; sh Orde.sh')
            assert Ficheiro('실행결과')==b'script\nrecovered\n'
            shell('rm 실행결과; echo "exit 7" > saír_apl.sh; sh saír_apl.sh; echo $?','7\n')
            shell('rm saír_apl.sh Orde.sh apl_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validación_informe['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            RESULTANTE=enviar(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert RESULTANTE.count('history-proof')>=2, RESULTANTE
            enviar(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            RESULTANTE=enviar(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in RESULTANTE, RESULTANTE
            RESULTANTE=enviar(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in RESULTANTE,RESULTANTE
            RESULTANTE=enviar('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in RESULTANTE,RESULTANTE
            긴글='한글'*50
            RESULTANTE=enviar(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in RESULTANTE
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as cliente:
                cliente.settimeout(10); cliente.connect(str(모의제어접속))
                with cliente.makefile('rwb') as fluxo_VALOR:
                    json.loads(fluxo_VALOR.readline())
                    def 호출(Nome,argumento_MATRIZ=None):
                        Rede_correo={'execute':Nome}
                        if argumento_MATRIZ: Rede_correo['arguments']=argumento_MATRIZ
                        fluxo_VALOR.write((json.dumps(Rede_correo)+'\n').encode()); fluxo_VALOR.flush()
                        while True:
                            resposta=json.loads(fluxo_VALOR.readline())
                            if 'error' in resposta: raise AssertionError(resposta)
                            if 'return' in resposta: return resposta['return']
                    호출('qmp_capabilities')
                    IMAXE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAXE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    datos=IMAXE.read_bytes().split(b'\n',3)[3]
                    def píxel(X_coordenada,Y_coordenada): return tuple(datos[(Y_coordenada*640+X_coordenada)*3:(Y_coordenada*640+X_coordenada)*3+3])
                    assert píxel(12,48)==(32,80,144),píxel(12,48)
                    assert len(set(píxel(X_coordenada,Y_coordenada) for Y_coordenada in range(100,116) for X_coordenada in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAXE),'format':'ppm'})
                    복원자료=IMAXE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    enviar(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    RESULTANTE=enviar(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in RESULTANTE,RESULTANTE
                    shell('rm visible.txt')
                    호출('quit')
            Proceso.wait(timeout=5)
            validación_informe['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validación_informe['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proceso.poll() is None:
                Proceso.terminate()
                try: Proceso.wait(timeout=5)
                except subprocess.TimeoutExpired: Proceso.kill(); Proceso.wait()
            준비살피미.close(); Proceso.stdin.close(); Proceso.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(validación_informe,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Executar_2()
