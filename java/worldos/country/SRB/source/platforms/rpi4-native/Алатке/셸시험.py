#!/usr/bin/env python3
"""자체 커널의 љуска, 프로세스 У_И, Unicode GUI 터미널을 стваран_подаци raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Изврши_команда import пројектовати_корен, Наредба


def Покрени():
    출력결과 = пројектовати_корен / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    провјера_извештај = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((пројектовати_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    транскрипт = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Процес = subprocess.Popen(Наредба()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процес.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            подаци=bytearray(); завршити_Помак=time.monotonic()+시간제한
            while 확인표시 not in подаци:
                if time.monotonic()>завршити_Помак or Процес.poll() is not None: raise AssertionError('UART timeout/exit: '+подаци.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: подаци.extend(조각); транскрипт.extend(조각)
                if b'PANIC:' in подаци or b'FAIL ' in подаци: raise AssertionError(подаци)
            return подаци.decode('utf-8','replace').replace('\r\n','\n')
        def послати(подаци, 확인표시=b'jkoros-native> '):
            Процес.stdin.write(подаци); Процес.stdin.flush(); return 수신하기(확인표시)
        def љуска(Ред, *예상결과):
            ИСХОД=послати(Ред.encode()+b'\n')
            for вриједност in 예상결과: assert вриједност in ИСХОД, (Ред,вриједност,ИСХОД)
            return ИСХОД
        def Датотека(Назив):
            Текст=љуска('hex '+Назив,'HEX BEGIN','HEX END'); тражити_мера=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Текст,re.S)
            подаци=bytes.fromhex(''.join(тражити_мера.group(2).split())); assert len(подаци)==int(тражити_мера.group(1)); return подаци
        try:
            수신하기(b'jkoros-native> ')
            љуска('mkdir 작업; cd 작업; pwd','/작업')
            љуска('mkdir 하위; echo "한글 подаци 😀" > 인사.txt')
            assert Датотека('인사.txt')=='한글 подаци 😀\n'.encode()
            љуска('cp 인사.txt инстанца_вриједност.txt; mv инстанца_вриједност.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 подаци 😀')
            љуска('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 подаци 😀','/작업/하위')
            љуска('cd ..; rmdir 하위; echo $?','1\n')
            љуска('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            љуска('cp 인사.txt 인사.txt; echo $?','1\n'); assert Датотека('인사.txt')=='한글 подаци 😀\n'.encode()
            љуска('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Датотека('인사.txt')
            љуска("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Датотека('리터럴')=='$인사\n누리\n'.encode()
            љуска('echo one > изјава_вриједност; echo two >> изјава_вриједност; echo three >> изјава_вриједност')
            љуска('cat < изјава_вриједност | grep t | tee 추림 | wc -l','2\n'); assert Датотека('추림')==b'two\nthree\n'
            љуска('head -n 1 изјава_вриједност > 앞; tail -n 1 изјава_вриједност > НАЗАД_вриједност'); assert Датотека('앞')==b'one\n'; assert Датотека('뒤')==b'three\n'
            љуска('grep absent изјава_вриједност; echo $?','1\n')
            љуска('echo untouched > заштитити_вриједност')
            љуска('echo destroyed > заштитити_вриједност |','명령이 빠졌습니다'); assert Датотека('заштитити_вриједност')==b'untouched\n'
            љуска('echo "oops','따옴표가 닫히지 않았습니다')
            љуска('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            љуска('echo bad 2> заштитити_вриједност','번호를 지정한 Датотека 서술자 У_И пребацити_мод'); assert Датотека('заштитити_вриједност')==b'untouched\n'
            љуска('rm 빈파일 리터럴 изјава_вриједност 추림 앞 НАЗАД_вриједност заштитити_вриједност')
            провјера_извештај['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            љуска("python -c 'print(123)' | wc -c",'4\n')
            љуска("python -c 'print(456)' > програм_f5044b9b.txt"); assert Датотека('програм_f5044b9b.txt')==b'456\n'
            љуска("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            љуска("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < програм_f5044b9b.txt", "b'456\\n'", "b''")
            љуска("python -c 'print(\"x\"*17000)' | wc -c", 'ГРЕШКА -28')
            љуска('echo recovered | wc -c','10\n')
            љуска("python -c 'import jkoros; print(jkoros.read("+'"/작업/програм_f5044b9b.txt"'+"))'",'456','exit 0')
            љуска('cd /; javac Hello.java','Compiled:','exit 0')
            љуска('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Датотека('/작업/자바.txt')
            љуска('cd 작업; echo "echo script > 실행결과" > Наредба.sh; echo "false || echo recovered >> 실행결과" >> Наредба.sh; sh Наредба.sh')
            assert Датотека('실행결과')==b'script\nrecovered\n'
            љуска('rm 실행결과; echo "exit 7" > Излаз_програм.sh; sh Излаз_програм.sh; echo $?','7\n')
            љуска('rm Излаз_програм.sh Наредба.sh програм_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            провјера_извештај['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            љуска('echo history-proof','history-proof')
            ИСХОД=послати(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ИСХОД.count('history-proof')>=2, ИСХОД
            послати(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ИСХОД=послати(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ИСХОД, ИСХОД
            ИСХОД=послати(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ИСХОД,ИСХОД
            ИСХОД=послати('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ИСХОД,ИСХОД
            긴글='한글'*50
            ИСХОД=послати(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ИСХОД
            љуска('terminal','TERMINAL READY')
            љуска('clear')
            љуска('echo "한글 Терминал ABC xyz 012 😀"','한글 Терминал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клијент:
                клијент.settimeout(10); клијент.connect(str(모의제어접속))
                with клијент.makefile('rwb') as ток_вриједност:
                    json.loads(ток_вриједност.readline())
                    def 호출(Назив,аргумент_низ=None):
                        Мрежа_порука={'execute':Назив}
                        if аргумент_низ: Мрежа_порука['arguments']=аргумент_низ
                        ток_вриједност.write((json.dumps(Мрежа_порука)+'\n').encode()); ток_вриједност.flush()
                        while True:
                            одговор=json.loads(ток_вриједност.readline())
                            if 'error' in одговор: raise AssertionError(одговор)
                            if 'return' in одговор: return одговор['return']
                    호출('qmp_capabilities')
                    слика=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(слика),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    подаци=слика.read_bytes().split(b'\n',3)[3]
                    def пиксел(x_координата,дугме_Y_координата): return tuple(подаци[(дугме_Y_координата*640+x_координата)*3:(дугме_Y_координата*640+x_координата)*3+3])
                    assert пиксел(12,48)==(32,80,144),пиксел(12,48)
                    assert len(set(пиксел(x_координата,дугме_Y_координата) for дугме_Y_координата in range(100,116) for x_координата in range(24,56)))>1,'Hangul glyphs missing'
                    љуска('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    љуска("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(слика),'format':'ppm'})
                    복원자료=слика.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    љуска('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): љуска('echo scroll-'+str(순번),'scroll-'+str(순번))
                    послати(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ИСХОД=послати(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ИСХОД,ИСХОД
                    љуска('rm visible.txt')
                    호출('quit')
            Процес.wait(timeout=5)
            провјера_извештај['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            провјера_извештај['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Процес.poll() is None:
                Процес.terminate()
                try: Процес.wait(timeout=5)
                except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
            준비살피미.close(); Процес.stdin.close(); Процес.stdout.close()
            (출력결과/'serial.log').write_bytes(транскрипт)
            (출력결과/'report.json').write_text(json.dumps(провјера_извештај,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Покрени()
