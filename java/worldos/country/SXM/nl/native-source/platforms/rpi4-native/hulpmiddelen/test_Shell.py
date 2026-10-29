#!/usr/bin/env python3
"""Eigen 커널의 Shell, 프로세스 I_O, Unicode GUI 터미널을 werkelijk_gegevens raspi4b에서 tests."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Uitvoeren_opdracht import Taken_wortel, opdracht


def starten():
    uitvoer = Taken_wortel / 'build/verification/shell'; uitvoer.mkdir(parents=True, exist_ok=True)
    validatie_Rapport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Taken_wortel / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcriptie = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proces = subprocess.Popen(opdracht()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
        def ontvangen_e_mail(markering, uitvoerbewerking_TIMEOUT=45):
            gegevens=bytearray(); beëindigen_VERSCHUIVING=time.monotonic()+uitvoerbewerking_TIMEOUT
            while markering not in gegevens:
                if time.monotonic()>beëindigen_VERSCHUIVING or Proces.poll() is not None: raise AssertionError('UART timeout/exit: '+gegevens.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: gegevens.extend(조각); transcriptie.extend(조각)
                if b'PANIC:' in gegevens or b'FAIL ' in gegevens: raise AssertionError(gegevens)
            return gegevens.decode('utf-8','replace').replace('\r\n','\n')
        def e_mailen(gegevens, markering=b'jkoros-native> '):
            Proces.stdin.write(gegevens); Proces.stdin.flush(); return ontvangen_e_mail(markering)
        def Shell(invoerregel, *예상결과):
            resultaat=e_mailen(invoerregel.encode()+b'\n')
            for WAARDE in 예상결과: assert WAARDE in resultaat, (invoerregel,WAARDE,resultaat)
            return resultaat
        def bestand(Naam):
            tekst=Shell('hex '+Naam,'HEX BEGIN','HEX END'); Search_HR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',tekst,re.S)
            gegevens=bytes.fromhex(''.join(Search_HR.group(2).split())); assert len(gegevens)==int(Search_HR.group(1)); return gegevens
        try:
            ontvangen_e_mail(b'jkoros-native> ')
            Shell('mkdir 작업; cd 작업; pwd','/작업')
            Shell('mkdir 하위; echo "한글 gegevens 😀" > 인사.txt')
            assert bestand('인사.txt')=='한글 gegevens 😀\n'.encode()
            Shell('cp 인사.txt kopiëren_WAARDE.txt; mv kopiëren_WAARDE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 gegevens 😀')
            Shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 gegevens 😀','/작업/하위')
            Shell('cd ..; rmdir 하위; echo $?','1\n')
            Shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            Shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert bestand('인사.txt')=='한글 gegevens 😀\n'.encode()
            Shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in bestand('인사.txt')
            Shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert bestand('리터럴')=='$인사\n누리\n'.encode()
            Shell('echo one > overzicht_WAARDE; echo two >> overzicht_WAARDE; echo three >> overzicht_WAARDE')
            Shell('cat < overzicht_WAARDE | grep t | tee 추림 | wc -l','2\n'); assert bestand('추림')==b'two\nthree\n'
            Shell('head -n 1 overzicht_WAARDE > voorkant_WAARDE; tail -n 1 overzicht_WAARDE > BACK_WAARDE'); assert bestand('앞')==b'one\n'; assert bestand('뒤')==b'three\n'
            Shell('grep absent overzicht_WAARDE; echo $?','1\n')
            Shell('echo untouched > beschermen_WAARDE')
            Shell('echo destroyed > beschermen_WAARDE |','명령이 빠졌습니다'); assert bestand('beschermen_WAARDE')==b'untouched\n'
            Shell('echo "oops','따옴표가 닫히지 않았습니다')
            Shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            Shell('echo bad 2> beschermen_WAARDE','번호를 지정한 bestand 서술자 I_O switch_MODUS'); assert bestand('beschermen_WAARDE')==b'untouched\n'
            Shell('rm 빈파일 리터럴 overzicht_WAARDE 추림 voorkant_WAARDE BACK_WAARDE beschermen_WAARDE')
            validatie_Rapport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            Shell("python -c 'print(123)' | wc -c",'4\n')
            Shell("python -c 'print(456)' > app_f5044b9b.txt"); assert bestand('app_f5044b9b.txt')==b'456\n'
            Shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            Shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < app_f5044b9b.txt", "b'456\\n'", "b''")
            Shell("python -c 'print(\"x\"*17000)' | wc -c", 'fout -28')
            Shell('echo recovered | wc -c','10\n')
            Shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/app_f5044b9b.txt"'+"))'",'456','exit 0')
            Shell('cd /; javac Hello.java','Compiled:','exit 0')
            Shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in bestand('/작업/자바.txt')
            Shell('cd 작업; echo "echo script > uitvoerbewerking_HR" > opdracht.sh; echo "false || echo recovered >> uitvoerbewerking_HR" >> opdracht.sh; sh opdracht.sh')
            assert bestand('uitvoerbewerking_HR')==b'script\nrecovered\n'
            Shell('rm uitvoerbewerking_HR; echo "exit 7" > Einde_app.sh; sh Einde_app.sh; echo $?','7\n')
            Shell('rm Einde_app.sh opdracht.sh app_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validatie_Rapport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            Shell('echo history-proof','history-proof')
            resultaat=e_mailen(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert resultaat.count('history-proof')>=2, resultaat
            e_mailen(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            resultaat=e_mailen(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in resultaat, resultaat
            resultaat=e_mailen(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in resultaat,resultaat
            resultaat=e_mailen('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in resultaat,resultaat
            긴글='한글'*50
            resultaat=e_mailen(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in resultaat
            Shell('terminal','TERMINAL READY')
            Shell('clear')
            Shell('echo "한글 terminal ABC xyz 012 😀"','한글 terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10); client.connect(str(모의제어접속))
                with client.makefile('rwb') as Stream_WAARDE:
                    json.loads(Stream_WAARDE.readline())
                    def 호출(Naam,argument_MATRIX=None):
                        net_e_mail={'execute':Naam}
                        if argument_MATRIX: net_e_mail['arguments']=argument_MATRIX
                        Stream_WAARDE.write((json.dumps(net_e_mail)+'\n').encode()); Stream_WAARDE.flush()
                        while True:
                            reactie=json.loads(Stream_WAARDE.readline())
                            if 'error' in reactie: raise AssertionError(reactie)
                            if 'return' in reactie: return reactie['return']
                    호출('qmp_capabilities')
                    kopie=uitvoer/'terminal.ppm'; 호출('screendump',{'filename':str(kopie),'format':'ppm'})
                    호출('screendump',{'filename':str(uitvoer/'terminal.png'),'format':'png'})
                    gegevens=kopie.read_bytes().split(b'\n',3)[3]
                    def pixel(x_coördinaat,Y_coördinaat): return tuple(gegevens[(Y_coördinaat*640+x_coördinaat)*3:(Y_coördinaat*640+x_coördinaat)*3+3])
                    assert pixel(12,48)==(32,80,144),pixel(12,48)
                    assert len(set(pixel(x_coördinaat,Y_coördinaat) for Y_coördinaat in range(100,116) for x_coördinaat in range(24,56)))>1,'Hangul glyphs missing'
                    Shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    Shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(kopie),'format':'ppm'})
                    복원자료=kopie.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    Shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): Shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    e_mailen(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(uitvoer/'terminal-scroll.png'),'format':'png'})
                    resultaat=e_mailen(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in resultaat,resultaat
                    Shell('rm visible.txt')
                    호출('quit')
            Proces.wait(timeout=5)
            validatie_Rapport['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validatie_Rapport['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            준비살피미.close(); Proces.stdin.close(); Proces.stdout.close()
            (uitvoer/'serial.log').write_bytes(transcriptie)
            (uitvoer/'report.json').write_text(json.dumps(validatie_Rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': starten()
