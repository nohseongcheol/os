#!/usr/bin/env python3
"""propi 커널의 shell, 프로세스 E_S, Unicode GUI 터미널을 real_dades raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Executa_ordre import Project_rel, Ordre


def Executa_2():
    출력결과 = Project_rel / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    validació_informe = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_rel / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Procés = subprocess.Popen(Ordre()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Procés.stdout,selectors.EVENT_READ)
        def rebre_correu(확인표시, 시간제한=45):
            dades=bytearray(); finalitzar_DESPLAÇAMENT=time.monotonic()+시간제한
            while 확인표시 not in dades:
                if time.monotonic()>finalitzar_DESPLAÇAMENT or Procés.poll() is not None: raise AssertionError('UART timeout/exit: '+dades.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: dades.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in dades or b'FAIL ' in dades: raise AssertionError(dades)
            return dades.decode('utf-8','replace').replace('\r\n','\n')
        def enviar(dades, 확인표시=b'jkoros-native> '):
            Procés.stdin.write(dades); Procés.stdin.flush(); return rebre_correu(확인표시)
        def shell(línia, *예상결과):
            RESULTAT=enviar(línia.encode()+b'\n')
            for VALOR in 예상결과: assert VALOR in RESULTAT, (línia,VALOR,RESULTAT)
            return RESULTAT
        def Fitxer(Nom):
            SMS=shell('hex '+Nom,'HEX BEGIN','HEX END'); Cerca_mesura=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            dades=bytes.fromhex(''.join(Cerca_mesura.group(2).split())); assert len(dades)==int(Cerca_mesura.group(1)); return dades
        try:
            rebre_correu(b'jkoros-native> ')
            shell('mkdir 작업; cd 작업; pwd','/작업')
            shell('mkdir 하위; echo "한글 dades 😀" > 인사.txt')
            assert Fitxer('인사.txt')=='한글 dades 😀\n'.encode()
            shell('cp 인사.txt copiar_VALOR.txt; mv copiar_VALOR.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 dades 😀')
            shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 dades 😀','/작업/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fitxer('인사.txt')=='한글 dades 😀\n'.encode()
            shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fitxer('인사.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fitxer('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > instrucció_VALOR; echo two >> instrucció_VALOR; echo three >> instrucció_VALOR')
            shell('cat < instrucció_VALOR | grep t | tee 추림 | wc -l','2\n'); assert Fitxer('추림')==b'two\nthree\n'
            shell('head -n 1 instrucció_VALOR > frontal_VALOR; tail -n 1 instrucció_VALOR > ENRERE_VALOR'); assert Fitxer('앞')==b'one\n'; assert Fitxer('뒤')==b'three\n'
            shell('grep absent instrucció_VALOR; echo $?','1\n')
            shell('echo untouched > protegir_VALOR')
            shell('echo destroyed > protegir_VALOR |','명령이 빠졌습니다'); assert Fitxer('protegir_VALOR')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> protegir_VALOR','번호를 지정한 Fitxer 서술자 E_S canvi_MODA'); assert Fitxer('protegir_VALOR')==b'untouched\n'
            shell('rm 빈파일 리터럴 instrucció_VALOR 추림 frontal_VALOR ENRERE_VALOR protegir_VALOR')
            validació_informe['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > programa_f5044b9b.txt"); assert Fitxer('programa_f5044b9b.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < programa_f5044b9b.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 's_ha_produït_un_error -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/programa_f5044b9b.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fitxer('/작업/자바.txt')
            shell('cd 작업; echo "echo script > 실행결과" > Ordre.sh; echo "false || echo recovered >> 실행결과" >> Ordre.sh; sh Ordre.sh')
            assert Fitxer('실행결과')==b'script\nrecovered\n'
            shell('rm 실행결과; echo "exit 7" > Surt_programa.sh; sh Surt_programa.sh; echo $?','7\n')
            shell('rm Surt_programa.sh Ordre.sh programa_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validació_informe['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            RESULTAT=enviar(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert RESULTAT.count('history-proof')>=2, RESULTAT
            enviar(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            RESULTAT=enviar(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in RESULTAT, RESULTAT
            RESULTAT=enviar(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in RESULTAT,RESULTAT
            RESULTAT=enviar('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in RESULTAT,RESULTAT
            긴글='한글'*50
            RESULTAT=enviar(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in RESULTAT
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10); client.connect(str(모의제어접속))
                with client.makefile('rwb') as flux_VALOR:
                    json.loads(flux_VALOR.readline())
                    def 호출(Nom,arg_MATRIU=None):
                        xarxa_correu={'execute':Nom}
                        if arg_MATRIU: xarxa_correu['arguments']=arg_MATRIU
                        flux_VALOR.write((json.dumps(xarxa_correu)+'\n').encode()); flux_VALOR.flush()
                        while True:
                            resposta=json.loads(flux_VALOR.readline())
                            if 'error' in resposta: raise AssertionError(resposta)
                            if 'return' in resposta: return resposta['return']
                    호출('qmp_capabilities')
                    IMATGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMATGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    dades=IMATGE.read_bytes().split(b'\n',3)[3]
                    def píxel(X_coordenada,Y_coordenada): return tuple(dades[(Y_coordenada*640+X_coordenada)*3:(Y_coordenada*640+X_coordenada)*3+3])
                    assert píxel(12,48)==(32,80,144),píxel(12,48)
                    assert len(set(píxel(X_coordenada,Y_coordenada) for Y_coordenada in range(100,116) for X_coordenada in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMATGE),'format':'ppm'})
                    복원자료=IMATGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    enviar(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    RESULTAT=enviar(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in RESULTAT,RESULTAT
                    shell('rm visible.txt')
                    호출('quit')
            Procés.wait(timeout=5)
            validació_informe['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validació_informe['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Procés.poll() is None:
                Procés.terminate()
                try: Procés.wait(timeout=5)
                except subprocess.TimeoutExpired: Procés.kill(); Procés.wait()
            준비살피미.close(); Procés.stdin.close(); Procés.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(validació_informe,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Executa_2()
