#!/usr/bin/env python3
"""자체 커널의 ljuska, 프로세스 U_I, Unicode GUI 터미널을 stvaran_podaci raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Izvrši_komanda import projicirati_koijen, Naredba


def Pokreni():
    출력결과 = projicirati_koijen / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    provjera_izvještaj = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((projicirati_koijen / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        proces = subprocess.Popen(Naredba()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(proces.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            podaci=bytearray(); završiti_Pomak=time.monotonic()+시간제한
            while 확인표시 not in podaci:
                if time.monotonic()>završiti_Pomak or proces.poll() is not None: raise AssertionError('UART timeout/exit: '+podaci.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: podaci.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in podaci or b'FAIL ' in podaci: raise AssertionError(podaci)
            return podaci.decode('utf-8','replace').replace('\r\n','\n')
        def poslati(podaci, 확인표시=b'jkoros-native> '):
            proces.stdin.write(podaci); proces.stdin.flush(); return 수신하기(확인표시)
        def ljuska(Linija, *예상결과):
            mjera=poslati(Linija.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in mjera, (Linija,VALUE,mjera)
            return mjera
        def Fajl(Naziv):
            Tekst=ljuska('hex '+Naziv,'HEX BEGIN','HEX END'); Traži_mjera=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Tekst,re.S)
            podaci=bytes.fromhex(''.join(Traži_mjera.group(2).split())); assert len(podaci)==int(Traži_mjera.group(1)); return podaci
        try:
            수신하기(b'jkoros-native> ')
            ljuska('mkdir 작업; cd 작업; pwd','/작업')
            ljuska('mkdir 하위; echo "한글 podaci 😀" > 인사.txt')
            assert Fajl('인사.txt')=='한글 podaci 😀\n'.encode()
            ljuska('cp 인사.txt instanca_VALUE.txt; mv instanca_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 podaci 😀')
            ljuska('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 podaci 😀','/작업/하위')
            ljuska('cd ..; rmdir 하위; echo $?','1\n')
            ljuska('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ljuska('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fajl('인사.txt')=='한글 podaci 😀\n'.encode()
            ljuska('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fajl('인사.txt')
            ljuska("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fajl('리터럴')=='$인사\n누리\n'.encode()
            ljuska('echo one > izjava_VALUE; echo two >> izjava_VALUE; echo three >> izjava_VALUE')
            ljuska('cat < izjava_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Fajl('추림')==b'two\nthree\n'
            ljuska('head -n 1 izjava_VALUE > 앞; tail -n 1 izjava_VALUE > ZAD_VALUE'); assert Fajl('앞')==b'one\n'; assert Fajl('뒤')==b'three\n'
            ljuska('grep absent izjava_VALUE; echo $?','1\n')
            ljuska('echo untouched > zaštititi_VALUE')
            ljuska('echo destroyed > zaštititi_VALUE |','명령이 빠졌습니다'); assert Fajl('zaštititi_VALUE')==b'untouched\n'
            ljuska('echo "oops','따옴표가 닫히지 않았습니다')
            ljuska('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ljuska('echo bad 2> zaštititi_VALUE','번호를 지정한 Fajl 서술자 U_I SWITCH_mod'); assert Fajl('zaštititi_VALUE')==b'untouched\n'
            ljuska('rm 빈파일 리터럴 izjava_VALUE 추림 앞 ZAD_VALUE zaštititi_VALUE')
            provjera_izvještaj['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ljuska("python -c 'print(123)' | wc -c",'4\n')
            ljuska("python -c 'print(456)' > program_f5044b9b.txt"); assert Fajl('program_f5044b9b.txt')==b'456\n'
            ljuska("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ljuska("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            ljuska("python -c 'print(\"x\"*17000)' | wc -c", 'GRESKA -28')
            ljuska('echo recovered | wc -c','10\n')
            ljuska("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            ljuska('cd /; javac Hello.java','Compiled:','exit 0')
            ljuska('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fajl('/작업/자바.txt')
            ljuska('cd 작업; echo "echo script > 실행결과" > Naredba.sh; echo "false || echo recovered >> 실행결과" >> Naredba.sh; sh Naredba.sh')
            assert Fajl('실행결과')==b'script\nrecovered\n'
            ljuska('rm 실행결과; echo "exit 7" > izaći_program.sh; sh izaći_program.sh; echo $?','7\n')
            ljuska('rm izaći_program.sh Naredba.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            provjera_izvještaj['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ljuska('echo history-proof','history-proof')
            mjera=poslati(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert mjera.count('history-proof')>=2, mjera
            poslati(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            mjera=poslati(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in mjera, mjera
            mjera=poslati(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in mjera,mjera
            mjera=poslati('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in mjera,mjera
            긴글='한글'*50
            mjera=poslati(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in mjera
            ljuska('terminal','TERMINAL READY')
            ljuska('clear')
            ljuska('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klijent:
                klijent.settimeout(10); klijent.connect(str(모의제어접속))
                with klijent.makefile('rwb') as tok_VALUE:
                    json.loads(tok_VALUE.readline())
                    def 호출(Naziv,argument_niz=None):
                        Mreža_poruka={'execute':Naziv}
                        if argument_niz: Mreža_poruka['arguments']=argument_niz
                        tok_VALUE.write((json.dumps(Mreža_poruka)+'\n').encode()); tok_VALUE.flush()
                        while True:
                            odgovoriti=json.loads(tok_VALUE.readline())
                            if 'error' in odgovoriti: raise AssertionError(odgovoriti)
                            if 'return' in odgovoriti: return odgovoriti['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    podaci=IMAGE.read_bytes().split(b'\n',3)[3]
                    def pel(koordinata_x,Y_koordinata): return tuple(podaci[(Y_koordinata*640+koordinata_x)*3:(Y_koordinata*640+koordinata_x)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(koordinata_x,Y_koordinata) for Y_koordinata in range(100,116) for koordinata_x in range(24,56)))>1,'Hangul glyphs missing'
                    ljuska('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ljuska("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ljuska('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ljuska('echo scroll-'+str(순번),'scroll-'+str(순번))
                    poslati(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    mjera=poslati(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in mjera,mjera
                    ljuska('rm visible.txt')
                    호출('quit')
            proces.wait(timeout=5)
            provjera_izvještaj['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            provjera_izvještaj['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if proces.poll() is None:
                proces.terminate()
                try: proces.wait(timeout=5)
                except subprocess.TimeoutExpired: proces.kill(); proces.wait()
            준비살피미.close(); proces.stdin.close(); proces.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(provjera_izvještaj,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Pokreni()
