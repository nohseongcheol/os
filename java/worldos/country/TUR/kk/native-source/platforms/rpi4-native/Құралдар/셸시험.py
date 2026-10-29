#!/usr/bin/env python3
"""자체 커널의 қоршам, 프로세스 енгізу_шығару, Unicode GUI 터미널을 нақты_деректер raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from орындау_пәрмен import жоба_түбір, Команда


def Орындау_2():
    출력결과 = жоба_түбір / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    тексерім_есеп = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((жоба_түбір / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Үрдіс = subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Үрдіс.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            деректер=bytearray(); тоқтату_жылжыту=time.monotonic()+시간제한
            while 확인표시 not in деректер:
                if time.monotonic()>тоқтату_жылжыту or Үрдіс.poll() is not None: raise AssertionError('UART timeout/exit: '+деректер.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: деректер.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in деректер or b'FAIL ' in деректер: raise AssertionError(деректер)
            return деректер.decode('utf-8','replace').replace('\r\n','\n')
        def жіберу(деректер, 확인표시=b'jkoros-native> '):
            Үрдіс.stdin.write(деректер); Үрдіс.stdin.flush(); return 수신하기(확인표시)
        def қоршам(Жол, *예상결과):
            НӘТИЖЕ=жіберу(Жол.encode()+b'\n')
            for мән in 예상결과: assert мән in НӘТИЖЕ, (Жол,мән,НӘТИЖЕ)
            return НӘТИЖЕ
        def Файл(Аты):
            Мәтін=қоршам('hex '+Аты,'HEX BEGIN','HEX END'); Іздеу_өлшем=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Мәтін,re.S)
            деректер=bytes.fromhex(''.join(Іздеу_өлшем.group(2).split())); assert len(деректер)==int(Іздеу_өлшем.group(1)); return деректер
        try:
            수신하기(b'jkoros-native> ')
            қоршам('mkdir 작업; cd 작업; pwd','/작업')
            қоршам('mkdir 하위; echo "한글 деректер 😀" > 인사.txt')
            assert Файл('인사.txt')=='한글 деректер 😀\n'.encode()
            қоршам('cp 인사.txt дана_мән.txt; mv дана_мән.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 деректер 😀')
            қоршам('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 деректер 😀','/작업/하위')
            қоршам('cd ..; rmdir 하위; echo $?','1\n')
            қоршам('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            қоршам('cp 인사.txt 인사.txt; echo $?','1\n'); assert Файл('인사.txt')=='한글 деректер 😀\n'.encode()
            қоршам('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Файл('인사.txt')
            қоршам("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Файл('리터럴')=='$인사\n누리\n'.encode()
            қоршам('echo one > нұсқау_мән; echo two >> нұсқау_мән; echo three >> нұсқау_мән')
            қоршам('cat < нұсқау_мән | grep t | tee 추림 | wc -l','2\n'); assert Файл('추림')==b'two\nthree\n'
            қоршам('head -n 1 нұсқау_мән > алдыңғы_камера_мән; tail -n 1 нұсқау_мән > АРТҚА_мән'); assert Файл('앞')==b'one\n'; assert Файл('뒤')==b'three\n'
            қоршам('grep absent нұсқау_мән; echo $?','1\n')
            қоршам('echo untouched > қорғау_мән')
            қоршам('echo destroyed > қорғау_мән |','명령이 빠졌습니다'); assert Файл('қорғау_мән')==b'untouched\n'
            қоршам('echo "oops','따옴표가 닫히지 않았습니다')
            қоршам('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            қоршам('echo bad 2> қорғау_мән','번호를 지정한 Файл 서술자 енгізу_шығару ауысу_режим'); assert Файл('қорғау_мән')==b'untouched\n'
            қоршам('rm 빈파일 리터럴 нұсқау_мән 추림 алдыңғы_камера_мән АРТҚА_мән қорғау_мән')
            тексерім_есеп['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            қоршам("python -c 'print(123)' | wc -c",'4\n')
            қоршам("python -c 'print(456)' > бағдарлама_f5044b9b.txt"); assert Файл('бағдарлама_f5044b9b.txt')==b'456\n'
            қоршам("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            қоршам("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < бағдарлама_f5044b9b.txt", "b'456\\n'", "b''")
            қоршам("python -c 'print(\"x\"*17000)' | wc -c", 'Қате -28')
            қоршам('echo recovered | wc -c','10\n')
            қоршам("python -c 'import jkoros; print(jkoros.read("+'"/작업/бағдарлама_f5044b9b.txt"'+"))'",'456','exit 0')
            қоршам('cd /; javac Hello.java','Compiled:','exit 0')
            қоршам('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Файл('/작업/자바.txt')
            қоршам('cd 작업; echo "echo script > 실행결과" > Команда.sh; echo "false || echo recovered >> 실행결과" >> Команда.sh; sh Команда.sh')
            assert Файл('실행결과')==b'script\nrecovered\n'
            қоршам('rm 실행결과; echo "exit 7" > Шығу_бағдарлама.sh; sh Шығу_бағдарлама.sh; echo $?','7\n')
            қоршам('rm Шығу_бағдарлама.sh Команда.sh бағдарлама_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            тексерім_есеп['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            қоршам('echo history-proof','history-proof')
            НӘТИЖЕ=жіберу(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert НӘТИЖЕ.count('history-proof')>=2, НӘТИЖЕ
            жіберу(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            НӘТИЖЕ=жіберу(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in НӘТИЖЕ, НӘТИЖЕ
            НӘТИЖЕ=жіберу(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in НӘТИЖЕ,НӘТИЖЕ
            НӘТИЖЕ=жіберу('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in НӘТИЖЕ,НӘТИЖЕ
            긴글='한글'*50
            НӘТИЖЕ=жіберу(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in НӘТИЖЕ
            қоршам('terminal','TERMINAL READY')
            қоршам('clear')
            қоршам('echo "한글 Терминал ABC xyz 012 😀"','한글 Терминал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10); клиент.connect(str(모의제어접속))
                with клиент.makefile('rwb') as ағым_мән:
                    json.loads(ағым_мән.readline())
                    def 호출(Аты,аргумент_массив=None):
                        желі_хабар={'execute':Аты}
                        if аргумент_массив: желі_хабар['arguments']=аргумент_массив
                        ағым_мән.write((json.dumps(желі_хабар)+'\n').encode()); ағым_мән.flush()
                        while True:
                            жауап=json.loads(ағым_мән.readline())
                            if 'error' in жауап: raise AssertionError(жауап)
                            if 'return' in жауап: return жауап['return']
                    호출('qmp_capabilities')
                    сурет=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(сурет),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    деректер=сурет.read_bytes().split(b'\n',3)[3]
                    def нүкте(x_координатасы,Y_түймешігі_координата): return tuple(деректер[(Y_түймешігі_координата*640+x_координатасы)*3:(Y_түймешігі_координата*640+x_координатасы)*3+3])
                    assert нүкте(12,48)==(32,80,144),нүкте(12,48)
                    assert len(set(нүкте(x_координатасы,Y_түймешігі_координата) for Y_түймешігі_координата in range(100,116) for x_координатасы in range(24,56)))>1,'Hangul glyphs missing'
                    қоршам('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    қоршам("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(сурет),'format':'ppm'})
                    복원자료=сурет.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    қоршам('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): қоршам('echo scroll-'+str(순번),'scroll-'+str(순번))
                    жіберу(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    НӘТИЖЕ=жіберу(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in НӘТИЖЕ,НӘТИЖЕ
                    қоршам('rm visible.txt')
                    호출('quit')
            Үрдіс.wait(timeout=5)
            тексерім_есеп['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            тексерім_есеп['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Үрдіс.poll() is None:
                Үрдіс.terminate()
                try: Үрдіс.wait(timeout=5)
                except subprocess.TimeoutExpired: Үрдіс.kill(); Үрдіс.wait()
            준비살피미.close(); Үрдіс.stdin.close(); Үрдіс.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(тексерім_есеп,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Орындау_2()
