#!/usr/bin/env python3
"""eget 커널의 Shell, 프로세스 indata_utleverans, Unicode GUI 터미널을 verklig_data raspi4b에서 tester."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from köra_kommando import åtgärd_rot, kommando


def Kör():
    utleverans = åtgärd_rot / 'build/verification/shell'; utleverans.mkdir(parents=True, exist_ok=True)
    validering_Rapport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((åtgärd_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    avskrift = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Process = subprocess.Popen(kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Process.stdout,selectors.EVENT_READ)
        def få_dokument(markör_8b722c5f, körning_TIMEOUT=45):
            data=bytearray(); avsluta_FÖRSKJUTNING=time.monotonic()+körning_TIMEOUT
            while markör_8b722c5f not in data:
                if time.monotonic()>avsluta_FÖRSKJUTNING or Process.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); avskrift.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def skicka(data, markör_8b722c5f=b'jkoros-native> '):
            Process.stdin.write(data); Process.stdin.flush(); return få_dokument(markör_8b722c5f)
        def Shell(inmatningsrad, *예상결과):
            RESULTAT=skicka(inmatningsrad.encode()+b'\n')
            for värde in 예상결과: assert värde in RESULTAT, (inmatningsrad,värde,RESULTAT)
            return RESULTAT
        def filnamn(Namn):
            text=Shell('hex '+Namn,'HEX BEGIN','HEX END'); SÖK_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',text,re.S)
            data=bytes.fromhex(''.join(SÖK_KR.group(2).split())); assert len(data)==int(SÖK_KR.group(1)); return data
        try:
            få_dokument(b'jkoros-native> ')
            Shell('mkdir 작업; cd 작업; pwd','/작업')
            Shell('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert filnamn('인사.txt')=='한글 data 😀\n'.encode()
            Shell('cp 인사.txt kopia_värde.txt; mv kopia_värde.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            Shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            Shell('cd ..; rmdir 하위; echo $?','1\n')
            Shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            Shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert filnamn('인사.txt')=='한글 data 😀\n'.encode()
            Shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in filnamn('인사.txt')
            Shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert filnamn('리터럴')=='$인사\n누리\n'.encode()
            Shell('echo one > utdrag_värde; echo two >> utdrag_värde; echo three >> utdrag_värde')
            Shell('cat < utdrag_värde | grep t | tee 추림 | wc -l','2\n'); assert filnamn('추림')==b'two\nthree\n'
            Shell('head -n 1 utdrag_värde > framåtvänd_värde; tail -n 1 utdrag_värde > BACK_värde'); assert filnamn('앞')==b'one\n'; assert filnamn('뒤')==b'three\n'
            Shell('grep absent utdrag_värde; echo $?','1\n')
            Shell('echo untouched > skydda_värde')
            Shell('echo destroyed > skydda_värde |','명령이 빠졌습니다'); assert filnamn('skydda_värde')==b'untouched\n'
            Shell('echo "oops','따옴표가 닫히지 않았습니다')
            Shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            Shell('echo bad 2> skydda_värde','번호를 지정한 filnamn 서술자 indata_utleverans byta_läge'); assert filnamn('skydda_värde')==b'untouched\n'
            Shell('rm 빈파일 리터럴 utdrag_värde 추림 framåtvänd_värde BACK_värde skydda_värde')
            validering_Rapport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            Shell("python -c 'print(123)' | wc -c",'4\n')
            Shell("python -c 'print(456)' > app_f5044b9b.txt"); assert filnamn('app_f5044b9b.txt')==b'456\n'
            Shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            Shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < app_f5044b9b.txt", "b'456\\n'", "b''")
            Shell("python -c 'print(\"x\"*17000)' | wc -c", 'fel -28')
            Shell('echo recovered | wc -c','10\n')
            Shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/app_f5044b9b.txt"'+"))'",'456','exit 0')
            Shell('cd /; javac Hello.java','Compiled:','exit 0')
            Shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in filnamn('/작업/자바.txt')
            Shell('cd 작업; echo "echo script > körning_KR" > kommando.sh; echo "false || echo recovered >> körning_KR" >> kommando.sh; sh kommando.sh')
            assert filnamn('körning_KR')==b'script\nrecovered\n'
            Shell('rm körning_KR; echo "exit 7" > Utgång_app.sh; sh Utgång_app.sh; echo $?','7\n')
            Shell('rm Utgång_app.sh kommando.sh app_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validering_Rapport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            Shell('echo history-proof','history-proof')
            RESULTAT=skicka(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert RESULTAT.count('history-proof')>=2, RESULTAT
            skicka(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            RESULTAT=skicka(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in RESULTAT, RESULTAT
            RESULTAT=skicka(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in RESULTAT,RESULTAT
            RESULTAT=skicka('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in RESULTAT,RESULTAT
            긴글='한글'*50
            RESULTAT=skicka(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in RESULTAT
            Shell('terminal','TERMINAL READY')
            Shell('clear')
            Shell('echo "한글 kommandotolk ABC xyz 012 😀"','한글 kommandotolk ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10); klient.connect(str(모의제어접속))
                with klient.makefile('rwb') as flöde_värde:
                    json.loads(flöde_värde.readline())
                    def 호출(Namn,argument_MATRIS=None):
                        nätverk_dokument={'execute':Namn}
                        if argument_MATRIS: nätverk_dokument['arguments']=argument_MATRIS
                        flöde_värde.write((json.dumps(nätverk_dokument)+'\n').encode()); flöde_värde.flush()
                        while True:
                            svara=json.loads(flöde_värde.readline())
                            if 'error' in svara: raise AssertionError(svara)
                            if 'return' in svara: return svara['return']
                    호출('qmp_capabilities')
                    BILD=utleverans/'terminal.ppm'; 호출('screendump',{'filename':str(BILD),'format':'ppm'})
                    호출('screendump',{'filename':str(utleverans/'terminal.png'),'format':'png'})
                    data=BILD.read_bytes().split(b'\n',3)[3]
                    def bildpunkt(x_koordinat,Y_koordinat): return tuple(data[(Y_koordinat*640+x_koordinat)*3:(Y_koordinat*640+x_koordinat)*3+3])
                    assert bildpunkt(12,48)==(32,80,144),bildpunkt(12,48)
                    assert len(set(bildpunkt(x_koordinat,Y_koordinat) for Y_koordinat in range(100,116) for x_koordinat in range(24,56)))>1,'Hangul glyphs missing'
                    Shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    Shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(BILD),'format':'ppm'})
                    복원자료=BILD.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    Shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): Shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    skicka(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(utleverans/'terminal-scroll.png'),'format':'png'})
                    RESULTAT=skicka(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in RESULTAT,RESULTAT
                    Shell('rm visible.txt')
                    호출('quit')
            Process.wait(timeout=5)
            validering_Rapport['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validering_Rapport['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Process.poll() is None:
                Process.terminate()
                try: Process.wait(timeout=5)
                except subprocess.TimeoutExpired: Process.kill(); Process.wait()
            준비살피미.close(); Process.stdin.close(); Process.stdout.close()
            (utleverans/'serial.log').write_bytes(avskrift)
            (utleverans/'report.json').write_text(json.dumps(validering_Rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Kör()
