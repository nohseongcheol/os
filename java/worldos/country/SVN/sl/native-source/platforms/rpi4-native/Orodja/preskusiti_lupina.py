#!/usr/bin/env python3
"""lastno 커널의 lupina, 프로세스 V_I, Unicode GUI 터미널을 dejanski_podatki raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Izvedi_ukaz import pobuda_koren, Ukaz


def Zaženi():
    출력결과 = pobuda_koren / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    preverjanje_veljavnosti_prijavi = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((pobuda_koren / 'build/kernel8.img').read_bytes()).hexdigest()}
    prepis = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Opravilo = subprocess.Popen(Ukaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Opravilo.stdout,selectors.EVENT_READ)
        def sprejeti_sprejemati_prejeti_prejemati_e_pošta(oznaka, 시간제한=45):
            podatki=bytearray(); končati_klic_odmik=time.monotonic()+시간제한
            while oznaka not in podatki:
                if time.monotonic()>končati_klic_odmik or Opravilo.poll() is not None: raise AssertionError('UART timeout/exit: '+podatki.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: podatki.extend(조각); prepis.extend(조각)
                if b'PANIC:' in podatki or b'FAIL ' in podatki: raise AssertionError(podatki)
            return podatki.decode('utf-8','replace').replace('\r\n','\n')
        def poslati(podatki, oznaka=b'jkoros-native> '):
            Opravilo.stdin.write(podatki); Opravilo.stdin.flush(); return sprejeti_sprejemati_prejeti_prejemati_e_pošta(oznaka)
        def lupina(Črtni, *예상결과):
            REZULTAT=poslati(Črtni.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in REZULTAT, (Črtni,VALUE,REZULTAT)
            return REZULTAT
        def Datoteka(Ime):
            Besedilo=lupina('hex '+Ime,'HEX BEGIN','HEX END'); Išči_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Besedilo,re.S)
            podatki=bytes.fromhex(''.join(Išči_KR.group(2).split())); assert len(podatki)==int(Išči_KR.group(1)); return podatki
        try:
            sprejeti_sprejemati_prejeti_prejemati_e_pošta(b'jkoros-native> ')
            lupina('mkdir 작업; cd 작업; pwd','/작업')
            lupina('mkdir 하위; echo "한글 podatki 😀" > 인사.txt')
            assert Datoteka('인사.txt')=='한글 podatki 😀\n'.encode()
            lupina('cp 인사.txt kopirati_VALUE.txt; mv kopirati_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 podatki 😀')
            lupina('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 podatki 😀','/작업/하위')
            lupina('cd ..; rmdir 하위; echo $?','1\n')
            lupina('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            lupina('cp 인사.txt 인사.txt; echo $?','1\n'); assert Datoteka('인사.txt')=='한글 podatki 😀\n'.encode()
            lupina('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Datoteka('인사.txt')
            lupina("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Datoteka('리터럴')=='$인사\n누리\n'.encode()
            lupina('echo one > izjava_VALUE; echo two >> izjava_VALUE; echo three >> izjava_VALUE')
            lupina('cat < izjava_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Datoteka('추림')==b'two\nthree\n'
            lupina('head -n 1 izjava_VALUE > sprednja_VALUE; tail -n 1 izjava_VALUE > ZAJ_VALUE'); assert Datoteka('앞')==b'one\n'; assert Datoteka('뒤')==b'three\n'
            lupina('grep absent izjava_VALUE; echo $?','1\n')
            lupina('echo untouched > zaščititi_VALUE')
            lupina('echo destroyed > zaščititi_VALUE |','명령이 빠졌습니다'); assert Datoteka('zaščititi_VALUE')==b'untouched\n'
            lupina('echo "oops','따옴표가 닫히지 않았습니다')
            lupina('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            lupina('echo bad 2> zaščititi_VALUE','번호를 지정한 Datoteka 서술자 V_I SWITCH_MODE'); assert Datoteka('zaščititi_VALUE')==b'untouched\n'
            lupina('rm 빈파일 리터럴 izjava_VALUE 추림 sprednja_VALUE ZAJ_VALUE zaščititi_VALUE')
            preverjanje_veljavnosti_prijavi['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            lupina("python -c 'print(123)' | wc -c",'4\n')
            lupina("python -c 'print(456)' > aplikacija_f5044b9b.txt"); assert Datoteka('aplikacija_f5044b9b.txt')==b'456\n'
            lupina("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            lupina("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < aplikacija_f5044b9b.txt", "b'456\\n'", "b''")
            lupina("python -c 'print(\"x\"*17000)' | wc -c", 'NAPAKA -28')
            lupina('echo recovered | wc -c','10\n')
            lupina("python -c 'import jkoros; print(jkoros.read("+'"/작업/aplikacija_f5044b9b.txt"'+"))'",'456','exit 0')
            lupina('cd /; javac Hello.java','Compiled:','exit 0')
            lupina('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Datoteka('/작업/자바.txt')
            lupina('cd 작업; echo "echo script > 실행결과" > Ukaz.sh; echo "false || echo recovered >> 실행결과" >> Ukaz.sh; sh Ukaz.sh')
            assert Datoteka('실행결과')==b'script\nrecovered\n'
            lupina('rm 실행결과; echo "exit 7" > Izhod_aplikacija.sh; sh Izhod_aplikacija.sh; echo $?','7\n')
            lupina('rm Izhod_aplikacija.sh Ukaz.sh aplikacija_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            preverjanje_veljavnosti_prijavi['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            lupina('echo history-proof','history-proof')
            REZULTAT=poslati(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert REZULTAT.count('history-proof')>=2, REZULTAT
            poslati(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            REZULTAT=poslati(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in REZULTAT, REZULTAT
            REZULTAT=poslati(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in REZULTAT,REZULTAT
            REZULTAT=poslati('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in REZULTAT,REZULTAT
            긴글='한글'*50
            REZULTAT=poslati(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in REZULTAT
            lupina('terminal','TERMINAL READY')
            lupina('clear')
            lupina('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as odjemalec:
                odjemalec.settimeout(10); odjemalec.connect(str(모의제어접속))
                with odjemalec.makefile('rwb') as tok_VALUE:
                    json.loads(tok_VALUE.readline())
                    def 호출(Ime,argument_ARRAY=None):
                        mreža_e_pošta={'execute':Ime}
                        if argument_ARRAY: mreža_e_pošta['arguments']=argument_ARRAY
                        tok_VALUE.write((json.dumps(mreža_e_pošta)+'\n').encode()); tok_VALUE.flush()
                        while True:
                            odgovor=json.loads(tok_VALUE.readline())
                            if 'error' in odgovor: raise AssertionError(odgovor)
                            if 'return' in odgovor: return odgovor['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    podatki=IMAGE.read_bytes().split(b'\n',3)[3]
                    def slikovna_pika(koordinata_x,세로좌표): return tuple(podatki[(세로좌표*640+koordinata_x)*3:(세로좌표*640+koordinata_x)*3+3])
                    assert slikovna_pika(12,48)==(32,80,144),slikovna_pika(12,48)
                    assert len(set(slikovna_pika(koordinata_x,세로좌표) for 세로좌표 in range(100,116) for koordinata_x in range(24,56)))>1,'Hangul glyphs missing'
                    lupina('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    lupina("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    lupina('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): lupina('echo scroll-'+str(순번),'scroll-'+str(순번))
                    poslati(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    REZULTAT=poslati(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in REZULTAT,REZULTAT
                    lupina('rm visible.txt')
                    호출('quit')
            Opravilo.wait(timeout=5)
            preverjanje_veljavnosti_prijavi['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            preverjanje_veljavnosti_prijavi['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Opravilo.poll() is None:
                Opravilo.terminate()
                try: Opravilo.wait(timeout=5)
                except subprocess.TimeoutExpired: Opravilo.kill(); Opravilo.wait()
            준비살피미.close(); Opravilo.stdin.close(); Opravilo.stdout.close()
            (출력결과/'serial.log').write_bytes(prepis)
            (출력결과/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Zaženi()
