#!/usr/bin/env python3
"""자체 커널의 обвивка, 프로세스 В_И, Unicode GUI 터미널을 реален_податоци raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Изврши_наредба import Project_корен, Команда


def Изврши_2():
    출력결과 = Project_корен / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    проверка_извештај = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Процес = subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процес.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            податоци=bytearray(); крај_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in податоци:
                if time.monotonic()>крај_OFFSET or Процес.poll() is not None: raise AssertionError('UART timeout/exit: '+податоци.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: податоци.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in податоци or b'FAIL ' in податоци: raise AssertionError(податоци)
            return податоци.decode('utf-8','replace').replace('\r\n','\n')
        def испрати(податоци, 확인표시=b'jkoros-native> '):
            Процес.stdin.write(податоци); Процес.stdin.flush(); return 수신하기(확인표시)
        def обвивка(ред, *예상결과):
            мерка=испрати(ред.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in мерка, (ред,VALUE,мерка)
            return мерка
        def Датотека(Име):
            Текст=обвивка('hex '+Име,'HEX BEGIN','HEX END'); SEARCH_мерка=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Текст,re.S)
            податоци=bytes.fromhex(''.join(SEARCH_мерка.group(2).split())); assert len(податоци)==int(SEARCH_мерка.group(1)); return податоци
        try:
            수신하기(b'jkoros-native> ')
            обвивка('mkdir 작업; cd 작업; pwd','/작업')
            обвивка('mkdir 하위; echo "한글 податоци 😀" > 인사.txt')
            assert Датотека('인사.txt')=='한글 податоци 😀\n'.encode()
            обвивка('cp 인사.txt копирај_VALUE.txt; mv копирај_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 податоци 😀')
            обвивка('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 податоци 😀','/작업/하위')
            обвивка('cd ..; rmdir 하위; echo $?','1\n')
            обвивка('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            обвивка('cp 인사.txt 인사.txt; echo $?','1\n'); assert Датотека('인사.txt')=='한글 податоци 😀\n'.encode()
            обвивка('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Датотека('인사.txt')
            обвивка("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Датотека('리터럴')=='$인사\n누리\n'.encode()
            обвивка('echo one > изјава_VALUE; echo two >> изјава_VALUE; echo three >> изјава_VALUE')
            обвивка('cat < изјава_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Датотека('추림')==b'two\nthree\n'
            обвивка('head -n 1 изјава_VALUE > предна_VALUE; tail -n 1 изјава_VALUE > Назад_VALUE'); assert Датотека('앞')==b'one\n'; assert Датотека('뒤')==b'three\n'
            обвивка('grep absent изјава_VALUE; echo $?','1\n')
            обвивка('echo untouched > заштита_VALUE')
            обвивка('echo destroyed > заштита_VALUE |','명령이 빠졌습니다'); assert Датотека('заштита_VALUE')==b'untouched\n'
            обвивка('echo "oops','따옴표가 닫히지 않았습니다')
            обвивка('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            обвивка('echo bad 2> заштита_VALUE','번호를 지정한 Датотека 서술자 В_И SWITCH_MODE'); assert Датотека('заштита_VALUE')==b'untouched\n'
            обвивка('rm 빈파일 리터럴 изјава_VALUE 추림 предна_VALUE Назад_VALUE заштита_VALUE')
            проверка_извештај['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            обвивка("python -c 'print(123)' | wc -c",'4\n')
            обвивка("python -c 'print(456)' > програма_f5044b9b.txt"); assert Датотека('програма_f5044b9b.txt')==b'456\n'
            обвивка("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            обвивка("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < програма_f5044b9b.txt", "b'456\\n'", "b''")
            обвивка("python -c 'print(\"x\"*17000)' | wc -c", 'ГРЕШКА -28')
            обвивка('echo recovered | wc -c','10\n')
            обвивка("python -c 'import jkoros; print(jkoros.read("+'"/작업/програма_f5044b9b.txt"'+"))'",'456','exit 0')
            обвивка('cd /; javac Hello.java','Compiled:','exit 0')
            обвивка('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Датотека('/작업/자바.txt')
            обвивка('cd 작업; echo "echo script > 실행결과" > Команда.sh; echo "false || echo recovered >> 실행결과" >> Команда.sh; sh Команда.sh')
            assert Датотека('실행결과')==b'script\nrecovered\n'
            обвивка('rm 실행결과; echo "exit 7" > Излез_програма.sh; sh Излез_програма.sh; echo $?','7\n')
            обвивка('rm Излез_програма.sh Команда.sh програма_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            проверка_извештај['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            обвивка('echo history-proof','history-proof')
            мерка=испрати(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert мерка.count('history-proof')>=2, мерка
            испрати(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            мерка=испрати(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in мерка, мерка
            мерка=испрати(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in мерка,мерка
            мерка=испрати('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in мерка,мерка
            긴글='한글'*50
            мерка=испрати(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in мерка
            обвивка('terminal','TERMINAL READY')
            обвивка('clear')
            обвивка('echo "한글 Терминал ABC xyz 012 😀"','한글 Терминал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10); клиент.connect(str(모의제어접속))
                with клиент.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Име,аргумент_низа=None):
                        Мрежа_порака={'execute':Име}
                        if аргумент_низа: Мрежа_порака['arguments']=аргумент_низа
                        Stream_VALUE.write((json.dumps(Мрежа_порака)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            одговори=json.loads(Stream_VALUE.readline())
                            if 'error' in одговори: raise AssertionError(одговори)
                            if 'return' in одговори: return одговори['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    податоци=IMAGE.read_bytes().split(b'\n',3)[3]
                    def пиксел(координата_х,세로좌표): return tuple(податоци[(세로좌표*640+координата_х)*3:(세로좌표*640+координата_х)*3+3])
                    assert пиксел(12,48)==(32,80,144),пиксел(12,48)
                    assert len(set(пиксел(координата_х,세로좌표) for 세로좌표 in range(100,116) for координата_х in range(24,56)))>1,'Hangul glyphs missing'
                    обвивка('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    обвивка("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    обвивка('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): обвивка('echo scroll-'+str(순번),'scroll-'+str(순번))
                    испрати(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    мерка=испрати(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in мерка,мерка
                    обвивка('rm visible.txt')
                    호출('quit')
            Процес.wait(timeout=5)
            проверка_извештај['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            проверка_извештај['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Процес.poll() is None:
                Процес.terminate()
                try: Процес.wait(timeout=5)
                except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
            준비살피미.close(); Процес.stdin.close(); Процес.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(проверка_извештај,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Изврши_2()
