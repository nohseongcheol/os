#!/usr/bin/env python3
"""savs 커널의 čaula, 프로세스 ievadizvade, Unicode GUI 터미널을 faktisks_dati raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Izpildīt_komanda import Project_sakne, Komanda


def Palaist():
    ražojums = Project_sakne / 'build/verification/shell'; ražojums.mkdir(parents=True, exist_ok=True)
    validācija_ziņot = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_sakne / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkripcija = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Process = subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Process.stdout,selectors.EVENT_READ)
        def saņemt_ziņa(marķieris, 시간제한=45):
            dati=bytearray(); beigt_zvanu_Nobīde=time.monotonic()+시간제한
            while marķieris not in dati:
                if time.monotonic()>beigt_zvanu_Nobīde or Process.poll() is not None: raise AssertionError('UART timeout/exit: '+dati.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: dati.extend(조각); transkripcija.extend(조각)
                if b'PANIC:' in dati or b'FAIL ' in dati: raise AssertionError(dati)
            return dati.decode('utf-8','replace').replace('\r\n','\n')
        def sūtīt(dati, marķieris=b'jkoros-native> '):
            Process.stdin.write(dati); Process.stdin.flush(); return saņemt_ziņa(marķieris)
        def čaula(Līniju, *예상결과):
            mērs=sūtīt(Līniju.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in mērs, (Līniju,VALUE,mērs)
            return mērs
        def Fails(Nosaukums):
            Teksts=čaula('hex '+Nosaukums,'HEX BEGIN','HEX END'); Meklēt_mērs=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Teksts,re.S)
            dati=bytes.fromhex(''.join(Meklēt_mērs.group(2).split())); assert len(dati)==int(Meklēt_mērs.group(1)); return dati
        try:
            saņemt_ziņa(b'jkoros-native> ')
            čaula('mkdir 작업; cd 작업; pwd','/작업')
            čaula('mkdir 하위; echo "한글 dati 😀" > 인사.txt')
            assert Fails('인사.txt')=='한글 dati 😀\n'.encode()
            čaula('cp 인사.txt kopēt_VALUE.txt; mv kopēt_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 dati 😀')
            čaula('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 dati 😀','/작업/하위')
            čaula('cd ..; rmdir 하위; echo $?','1\n')
            čaula('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            čaula('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fails('인사.txt')=='한글 dati 😀\n'.encode()
            čaula('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fails('인사.txt')
            čaula("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fails('리터럴')=='$인사\n누리\n'.encode()
            čaula('echo one > pārskats_VALUE; echo two >> pārskats_VALUE; echo three >> pārskats_VALUE')
            čaula('cat < pārskats_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Fails('추림')==b'two\nthree\n'
            čaula('head -n 1 pārskats_VALUE > priekšējā_VALUE; tail -n 1 pārskats_VALUE > ATPAKAĻ_VALUE'); assert Fails('앞')==b'one\n'; assert Fails('뒤')==b'three\n'
            čaula('grep absent pārskats_VALUE; echo $?','1\n')
            čaula('echo untouched > aizsargāt_VALUE')
            čaula('echo destroyed > aizsargāt_VALUE |','명령이 빠졌습니다'); assert Fails('aizsargāt_VALUE')==b'untouched\n'
            čaula('echo "oops','따옴표가 닫히지 않았습니다')
            čaula('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            čaula('echo bad 2> aizsargāt_VALUE','번호를 지정한 Fails 서술자 ievadizvade SWITCH_MODE'); assert Fails('aizsargāt_VALUE')==b'untouched\n'
            čaula('rm 빈파일 리터럴 pārskats_VALUE 추림 priekšējā_VALUE ATPAKAĻ_VALUE aizsargāt_VALUE')
            validācija_ziņot['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            čaula("python -c 'print(123)' | wc -c",'4\n')
            čaula("python -c 'print(456)' > programma_f5044b9b.txt"); assert Fails('programma_f5044b9b.txt')==b'456\n'
            čaula("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            čaula("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < programma_f5044b9b.txt", "b'456\\n'", "b''")
            čaula("python -c 'print(\"x\"*17000)' | wc -c", 'Kļūda -28')
            čaula('echo recovered | wc -c','10\n')
            čaula("python -c 'import jkoros; print(jkoros.read("+'"/작업/programma_f5044b9b.txt"'+"))'",'456','exit 0')
            čaula('cd /; javac Hello.java','Compiled:','exit 0')
            čaula('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fails('/작업/자바.txt')
            čaula('cd 작업; echo "echo script > 실행결과" > Komanda.sh; echo "false || echo recovered >> 실행결과" >> Komanda.sh; sh Komanda.sh')
            assert Fails('실행결과')==b'script\nrecovered\n'
            čaula('rm 실행결과; echo "exit 7" > Iziet_programma.sh; sh Iziet_programma.sh; echo $?','7\n')
            čaula('rm Iziet_programma.sh Komanda.sh programma_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validācija_ziņot['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            čaula('echo history-proof','history-proof')
            mērs=sūtīt(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert mērs.count('history-proof')>=2, mērs
            sūtīt(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            mērs=sūtīt(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in mērs, mērs
            mērs=sūtīt(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in mērs,mērs
            mērs=sūtīt('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in mērs,mērs
            긴글='한글'*50
            mērs=sūtīt(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in mērs
            čaula('terminal','TERMINAL READY')
            čaula('clear')
            čaula('echo "한글 Terminālis ABC xyz 012 😀"','한글 Terminālis ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klients:
                klients.settimeout(10); klients.connect(str(모의제어접속))
                with klients.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Nosaukums,arg_ARRAY=None):
                        tīkls_ziņa={'execute':Nosaukums}
                        if arg_ARRAY: tīkls_ziņa['arguments']=arg_ARRAY
                        Stream_VALUE.write((json.dumps(tīkls_ziņa)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            atbilde=json.loads(Stream_VALUE.readline())
                            if 'error' in atbilde: raise AssertionError(atbilde)
                            if 'return' in atbilde: return atbilde['return']
                    호출('qmp_capabilities')
                    IMAGE=ražojums/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(ražojums/'terminal.png'),'format':'png'})
                    dati=IMAGE.read_bytes().split(b'\n',3)[3]
                    def attēla_elements(x_koordināta,세로좌표): return tuple(dati[(세로좌표*640+x_koordināta)*3:(세로좌표*640+x_koordināta)*3+3])
                    assert attēla_elements(12,48)==(32,80,144),attēla_elements(12,48)
                    assert len(set(attēla_elements(x_koordināta,세로좌표) for 세로좌표 in range(100,116) for x_koordināta in range(24,56)))>1,'Hangul glyphs missing'
                    čaula('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    čaula("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    čaula('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): čaula('echo scroll-'+str(순번),'scroll-'+str(순번))
                    sūtīt(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(ražojums/'terminal-scroll.png'),'format':'png'})
                    mērs=sūtīt(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in mērs,mērs
                    čaula('rm visible.txt')
                    호출('quit')
            Process.wait(timeout=5)
            validācija_ziņot['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validācija_ziņot['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Process.poll() is None:
                Process.terminate()
                try: Process.wait(timeout=5)
                except subprocess.TimeoutExpired: Process.kill(); Process.wait()
            준비살피미.close(); Process.stdin.close(); Process.stdout.close()
            (ražojums/'serial.log').write_bytes(transkripcija)
            (ražojums/'report.json').write_text(json.dumps(validācija_ziņot,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Palaist()
