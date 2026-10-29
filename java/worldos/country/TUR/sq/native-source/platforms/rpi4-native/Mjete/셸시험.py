#!/usr/bin/env python3
"""자체 커널의 pasues, 프로세스 I_O, Unicode GUI 터미널을 aktual_të_dhëna raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from zbatoj_komandë import Project_rrënjë, Komanda


def Ekzekuto():
    출력결과 = Project_rrënjë / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    miratim_raport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_rrënjë / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proçes = subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proçes.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            të_dhëna=bytearray(); mbaroj_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in të_dhëna:
                if time.monotonic()>mbaroj_OFFSET or Proçes.poll() is not None: raise AssertionError('UART timeout/exit: '+të_dhëna.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: të_dhëna.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in të_dhëna or b'FAIL ' in të_dhëna: raise AssertionError(të_dhëna)
            return të_dhëna.decode('utf-8','replace').replace('\r\n','\n')
        def dërgoj(të_dhëna, 확인표시=b'jkoros-native> '):
            Proçes.stdin.write(të_dhëna); Proçes.stdin.flush(); return 수신하기(확인표시)
        def pasues(linjë, *예상결과):
            llogaritje=dërgoj(linjë.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in llogaritje, (linjë,VALUE,llogaritje)
            return llogaritje
        def Kartelë(Emër):
            Teksti=pasues('hex '+Emër,'HEX BEGIN','HEX END'); Kërkim_llogaritje=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Teksti,re.S)
            të_dhëna=bytes.fromhex(''.join(Kërkim_llogaritje.group(2).split())); assert len(të_dhëna)==int(Kërkim_llogaritje.group(1)); return të_dhëna
        try:
            수신하기(b'jkoros-native> ')
            pasues('mkdir 작업; cd 작업; pwd','/작업')
            pasues('mkdir 하위; echo "한글 të_dhëna 😀" > 인사.txt')
            assert Kartelë('인사.txt')=='한글 të_dhëna 😀\n'.encode()
            pasues('cp 인사.txt kopjoj_VALUE.txt; mv kopjoj_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 të_dhëna 😀')
            pasues('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 të_dhëna 😀','/작업/하위')
            pasues('cd ..; rmdir 하위; echo $?','1\n')
            pasues('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            pasues('cp 인사.txt 인사.txt; echo $?','1\n'); assert Kartelë('인사.txt')=='한글 të_dhëna 😀\n'.encode()
            pasues('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Kartelë('인사.txt')
            pasues("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Kartelë('리터럴')=='$인사\n누리\n'.encode()
            pasues('echo one > deklarim_VALUE; echo two >> deklarim_VALUE; echo three >> deklarim_VALUE')
            pasues('cat < deklarim_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Kartelë('추림')==b'two\nthree\n'
            pasues('head -n 1 deklarim_VALUE > e_përparme_VALUE; tail -n 1 deklarim_VALUE > PAS_VALUE'); assert Kartelë('앞')==b'one\n'; assert Kartelë('뒤')==b'three\n'
            pasues('grep absent deklarim_VALUE; echo $?','1\n')
            pasues('echo untouched > mbroj_VALUE')
            pasues('echo destroyed > mbroj_VALUE |','명령이 빠졌습니다'); assert Kartelë('mbroj_VALUE')==b'untouched\n'
            pasues('echo "oops','따옴표가 닫히지 않았습니다')
            pasues('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            pasues('echo bad 2> mbroj_VALUE','번호를 지정한 Kartelë 서술자 I_O SWITCH_MODE'); assert Kartelë('mbroj_VALUE')==b'untouched\n'
            pasues('rm 빈파일 리터럴 deklarim_VALUE 추림 e_përparme_VALUE PAS_VALUE mbroj_VALUE')
            miratim_raport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            pasues("python -c 'print(123)' | wc -c",'4\n')
            pasues("python -c 'print(456)' > program_f5044b9b.txt"); assert Kartelë('program_f5044b9b.txt')==b'456\n'
            pasues("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            pasues("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            pasues("python -c 'print(\"x\"*17000)' | wc -c", 'GABIM -28')
            pasues('echo recovered | wc -c','10\n')
            pasues("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            pasues('cd /; javac Hello.java','Compiled:','exit 0')
            pasues('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Kartelë('/작업/자바.txt')
            pasues('cd 작업; echo "echo script > 실행결과" > Komanda.sh; echo "false || echo recovered >> 실행결과" >> Komanda.sh; sh Komanda.sh')
            assert Kartelë('실행결과')==b'script\nrecovered\n'
            pasues('rm 실행결과; echo "exit 7" > dal_program.sh; sh dal_program.sh; echo $?','7\n')
            pasues('rm dal_program.sh Komanda.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            miratim_raport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            pasues('echo history-proof','history-proof')
            llogaritje=dërgoj(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert llogaritje.count('history-proof')>=2, llogaritje
            dërgoj(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            llogaritje=dërgoj(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in llogaritje, llogaritje
            llogaritje=dërgoj(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in llogaritje,llogaritje
            llogaritje=dërgoj('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in llogaritje,llogaritje
            긴글='한글'*50
            llogaritje=dërgoj(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in llogaritje
            pasues('terminal','TERMINAL READY')
            pasues('clear')
            pasues('echo "한글 Terminali ABC xyz 012 😀"','한글 Terminali ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10); klient.connect(str(모의제어접속))
                with klient.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Emër,argument_ARRAY=None):
                        rrjet_email={'execute':Emër}
                        if argument_ARRAY: rrjet_email['arguments']=argument_ARRAY
                        Stream_VALUE.write((json.dumps(rrjet_email)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            replikë=json.loads(Stream_VALUE.readline())
                            if 'error' in replikë: raise AssertionError(replikë)
                            if 'return' in replikë: return replikë['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    të_dhëna=IMAGE.read_bytes().split(b'\n',3)[3]
                    def pikëz(koordinata_x,Y_koordinatë): return tuple(të_dhëna[(Y_koordinatë*640+koordinata_x)*3:(Y_koordinatë*640+koordinata_x)*3+3])
                    assert pikëz(12,48)==(32,80,144),pikëz(12,48)
                    assert len(set(pikëz(koordinata_x,Y_koordinatë) for Y_koordinatë in range(100,116) for koordinata_x in range(24,56)))>1,'Hangul glyphs missing'
                    pasues('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    pasues("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    pasues('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): pasues('echo scroll-'+str(순번),'scroll-'+str(순번))
                    dërgoj(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    llogaritje=dërgoj(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in llogaritje,llogaritje
                    pasues('rm visible.txt')
                    호출('quit')
            Proçes.wait(timeout=5)
            miratim_raport['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            miratim_raport['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proçes.poll() is None:
                Proçes.terminate()
                try: Proçes.wait(timeout=5)
                except subprocess.TimeoutExpired: Proçes.kill(); Proçes.wait()
            준비살피미.close(); Proçes.stdin.close(); Proçes.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(miratim_raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Ekzekuto()
