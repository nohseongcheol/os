#!/usr/bin/env python3
"""vlastiti 커널의 ljuska, 프로세스 U_I, Unicode GUI 터미널을 stvaran_podaci raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Izvrši_naredba import akcija_korijen, Naredba


def Pokreni():
    출력결과 = akcija_korijen / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    provjera_izvješće = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((akcija_korijen / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkript = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proces = subprocess.Popen(Naredba()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
        def primiti_poruka(marker, 시간제한=45):
            podaci=bytearray(); završiti_razgovor_pomak=time.monotonic()+시간제한
            while marker not in podaci:
                if time.monotonic()>završiti_razgovor_pomak or Proces.poll() is not None: raise AssertionError('UART timeout/exit: '+podaci.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    fragment_VALUE=누름값.fileobj.read(4096)
                    if fragment_VALUE: podaci.extend(fragment_VALUE); transkript.extend(fragment_VALUE)
                if b'PANIC:' in podaci or b'FAIL ' in podaci: raise AssertionError(podaci)
            return podaci.decode('utf-8','replace').replace('\r\n','\n')
        def slati(podaci, marker=b'jkoros-native> '):
            Proces.stdin.write(podaci); Proces.stdin.flush(); return primiti_poruka(marker)
        def ljuska(red, *예상결과):
            REZULTAT=slati(red.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in REZULTAT, (red,VALUE,REZULTAT)
            return REZULTAT
        def Datoteka(Ime):
            Tekst=ljuska('hex '+Ime,'HEX BEGIN','HEX END'); Traži_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Tekst,re.S)
            podaci=bytes.fromhex(''.join(Traži_KR.group(2).split())); assert len(podaci)==int(Traži_KR.group(1)); return podaci
        try:
            primiti_poruka(b'jkoros-native> ')
            ljuska('mkdir 작업; cd 작업; pwd','/작업')
            ljuska('mkdir 하위; echo "한글 podaci 😀" > 인사.txt')
            assert Datoteka('인사.txt')=='한글 podaci 😀\n'.encode()
            ljuska('cp 인사.txt instanca_VALUE.txt; mv instanca_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 podaci 😀')
            ljuska('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 podaci 😀','/작업/하위')
            ljuska('cd ..; rmdir 하위; echo $?','1\n')
            ljuska('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ljuska('cp 인사.txt 인사.txt; echo $?','1\n'); assert Datoteka('인사.txt')=='한글 podaci 😀\n'.encode()
            ljuska('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Datoteka('인사.txt')
            ljuska("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Datoteka('리터럴')=='$인사\n누리\n'.encode()
            ljuska('echo one > izjava_VALUE; echo two >> izjava_VALUE; echo three >> izjava_VALUE')
            ljuska('cat < izjava_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Datoteka('추림')==b'two\nthree\n'
            ljuska('head -n 1 izjava_VALUE > prednja_VALUE; tail -n 1 izjava_VALUE > TRAG_VALUE'); assert Datoteka('앞')==b'one\n'; assert Datoteka('뒤')==b'three\n'
            ljuska('grep absent izjava_VALUE; echo $?','1\n')
            ljuska('echo untouched > zaštititi_VALUE')
            ljuska('echo destroyed > zaštititi_VALUE |','명령이 빠졌습니다'); assert Datoteka('zaštititi_VALUE')==b'untouched\n'
            ljuska('echo "oops','따옴표가 닫히지 않았습니다')
            ljuska('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ljuska('echo bad 2> zaštititi_VALUE','번호를 지정한 Datoteka 서술자 U_I SWITCH_MODE'); assert Datoteka('zaštititi_VALUE')==b'untouched\n'
            ljuska('rm 빈파일 리터럴 izjava_VALUE 추림 prednja_VALUE TRAG_VALUE zaštititi_VALUE')
            provjera_izvješće['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ljuska("python -c 'print(123)' | wc -c",'4\n')
            ljuska("python -c 'print(456)' > program_f5044b9b.txt"); assert Datoteka('program_f5044b9b.txt')==b'456\n'
            ljuska("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ljuska("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < program_f5044b9b.txt", "b'456\\n'", "b''")
            ljuska("python -c 'print(\"x\"*17000)' | wc -c", 'GREŠKA -28')
            ljuska('echo recovered | wc -c','10\n')
            ljuska("python -c 'import jkoros; print(jkoros.read("+'"/작업/program_f5044b9b.txt"'+"))'",'456','exit 0')
            ljuska('cd /; javac Hello.java','Compiled:','exit 0')
            ljuska('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Datoteka('/작업/자바.txt')
            ljuska('cd 작업; echo "echo script > 실행결과" > Naredba.sh; echo "false || echo recovered >> 실행결과" >> Naredba.sh; sh Naredba.sh')
            assert Datoteka('실행결과')==b'script\nrecovered\n'
            ljuska('rm 실행결과; echo "exit 7" > Izlaz_program.sh; sh Izlaz_program.sh; echo $?','7\n')
            ljuska('rm Izlaz_program.sh Naredba.sh program_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            provjera_izvješće['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ljuska('echo history-proof','history-proof')
            REZULTAT=slati(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert REZULTAT.count('history-proof')>=2, REZULTAT
            slati(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            REZULTAT=slati(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in REZULTAT, REZULTAT
            REZULTAT=slati(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in REZULTAT,REZULTAT
            REZULTAT=slati('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in REZULTAT,REZULTAT
            긴글='한글'*50
            REZULTAT=slati(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in REZULTAT
            ljuska('terminal','TERMINAL READY')
            ljuska('clear')
            ljuska('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klijent:
                klijent.settimeout(10); klijent.connect(str(모의제어접속))
                with klijent.makefile('rwb') as tok_VALUE:
                    json.loads(tok_VALUE.readline())
                    def 호출(Ime,argument_ARRAY=None):
                        mreža_poruka={'execute':Ime}
                        if argument_ARRAY: mreža_poruka['arguments']=argument_ARRAY
                        tok_VALUE.write((json.dumps(mreža_poruka)+'\n').encode()); tok_VALUE.flush()
                        while True:
                            odgovor=json.loads(tok_VALUE.readline())
                            if 'error' in odgovor: raise AssertionError(odgovor)
                            if 'return' in odgovor: return odgovor['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    podaci=IMAGE.read_bytes().split(b'\n',3)[3]
                    def slikovni_element(koordinata_x,세로좌표): return tuple(podaci[(세로좌표*640+koordinata_x)*3:(세로좌표*640+koordinata_x)*3+3])
                    assert slikovni_element(12,48)==(32,80,144),slikovni_element(12,48)
                    assert len(set(slikovni_element(koordinata_x,세로좌표) for 세로좌표 in range(100,116) for koordinata_x in range(24,56)))>1,'Hangul glyphs missing'
                    ljuska('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ljuska("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ljuska('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ljuska('echo scroll-'+str(순번),'scroll-'+str(순번))
                    slati(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    REZULTAT=slati(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in REZULTAT,REZULTAT
                    ljuska('rm visible.txt')
                    호출('quit')
            Proces.wait(timeout=5)
            provjera_izvješće['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            provjera_izvješće['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            준비살피미.close(); Proces.stdin.close(); Proces.stdout.close()
            (출력결과/'serial.log').write_bytes(transkript)
            (출력결과/'report.json').write_text(json.dumps(provjera_izvješće,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Pokreni()
