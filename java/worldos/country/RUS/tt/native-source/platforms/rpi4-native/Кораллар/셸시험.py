#!/usr/bin/env python3
"""자체 커널의 тышча, 프로세스 К_Ч, Unicode GUI 터미널을 фактик_мәгълүмат raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from үтәргә_команда import экранга_җибәрү_тамыр, команда


def эшләтү():
    출력결과 = экранга_җибәрү_тамыр / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    раслау_отчет = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Процесс = subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процесс.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            мәгълүмат=bytearray(); тәмамлау_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in мәгълүмат:
                if time.monotonic()>тәмамлау_OFFSET or Процесс.poll() is not None: raise AssertionError('UART timeout/exit: '+мәгълүмат.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: мәгълүмат.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in мәгълүмат or b'FAIL ' in мәгълүмат: raise AssertionError(мәгълүмат)
            return мәгълүмат.decode('utf-8','replace').replace('\r\n','\n')
        def җибәрү(мәгълүмат, 확인표시=b'jkoros-native> '):
            Процесс.stdin.write(мәгълүмат); Процесс.stdin.flush(); return 수신하기(확인표시)
        def тышча(юл, *예상결과):
            үлчәм=җибәрү(юл.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in үлчәм, (юл,VALUE,үлчәм)
            return үлчәм
        def Birem(исем):
            Mäten=тышча('hex '+исем,'HEX BEGIN','HEX END'); Эзләү_үлчәм=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Mäten,re.S)
            мәгълүмат=bytes.fromhex(''.join(Эзләү_үлчәм.group(2).split())); assert len(мәгълүмат)==int(Эзләү_үлчәм.group(1)); return мәгълүмат
        try:
            수신하기(b'jkoros-native> ')
            тышча('mkdir 작업; cd 작업; pwd','/작업')
            тышча('mkdir 하위; echo "한글 мәгълүмат 😀" > 인사.txt')
            assert Birem('인사.txt')=='한글 мәгълүмат 😀\n'.encode()
            тышча('cp 인사.txt экземпляр_VALUE.txt; mv экземпляр_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 мәгълүмат 😀')
            тышча('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 мәгълүмат 😀','/작업/하위')
            тышча('cd ..; rmdir 하위; echo $?','1\n')
            тышча('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            тышча('cp 인사.txt 인사.txt; echo $?','1\n'); assert Birem('인사.txt')=='한글 мәгълүмат 😀\n'.encode()
            тышча('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Birem('인사.txt')
            тышча("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Birem('리터럴')=='$인사\n누리\n'.encode()
            тышча('echo one > аңлатма_VALUE; echo two >> аңлатма_VALUE; echo three >> аңлатма_VALUE')
            тышча('cat < аңлатма_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Birem('추림')==b'two\nthree\n'
            тышча('head -n 1 аңлатма_VALUE > 앞; tail -n 1 аңлатма_VALUE > Артка_VALUE'); assert Birem('앞')==b'one\n'; assert Birem('뒤')==b'three\n'
            тышча('grep absent аңлатма_VALUE; echo $?','1\n')
            тышча('echo untouched > саклау_VALUE')
            тышча('echo destroyed > саклау_VALUE |','명령이 빠졌습니다'); assert Birem('саклау_VALUE')==b'untouched\n'
            тышча('echo "oops','따옴표가 닫히지 않았습니다')
            тышча('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            тышча('echo bad 2> саклау_VALUE','번호를 지정한 Birem 서술자 К_Ч SWITCH_MODE'); assert Birem('саклау_VALUE')==b'untouched\n'
            тышча('rm 빈파일 리터럴 аңлатма_VALUE 추림 앞 Артка_VALUE саклау_VALUE')
            раслау_отчет['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            тышча("python -c 'print(123)' | wc -c",'4\n')
            тышча("python -c 'print(456)' > кушымта_f5044b9b.txt"); assert Birem('кушымта_f5044b9b.txt')==b'456\n'
            тышча("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            тышча("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < кушымта_f5044b9b.txt", "b'456\\n'", "b''")
            тышча("python -c 'print(\"x\"*17000)' | wc -c", 'Хата -28')
            тышча('echo recovered | wc -c','10\n')
            тышча("python -c 'import jkoros; print(jkoros.read("+'"/작업/кушымта_f5044b9b.txt"'+"))'",'456','exit 0')
            тышча('cd /; javac Hello.java','Compiled:','exit 0')
            тышча('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Birem('/작업/자바.txt')
            тышча('cd 작업; echo "echo script > 실행결과" > команда.sh; echo "false || echo recovered >> 실행결과" >> команда.sh; sh команда.sh')
            assert Birem('실행결과')==b'script\nrecovered\n'
            тышча('rm 실행결과; echo "exit 7" > Чыгу_кушымта.sh; sh Чыгу_кушымта.sh; echo $?','7\n')
            тышча('rm Чыгу_кушымта.sh команда.sh кушымта_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            раслау_отчет['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            тышча('echo history-proof','history-proof')
            үлчәм=җибәрү(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert үлчәм.count('history-proof')>=2, үлчәм
            җибәрү(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            үлчәм=җибәрү(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in үлчәм, үлчәм
            үлчәм=җибәрү(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in үлчәм,үлчәм
            үлчәм=җибәрү('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in үлчәм,үлчәм
            긴글='한글'*50
            үлчәм=җибәрү(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in үлчәм
            тышча('terminal','TERMINAL READY')
            тышча('clear')
            тышча('echo "한글 Терминал ABC xyz 012 😀"','한글 Терминал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10); клиент.connect(str(모의제어접속))
                with клиент.makefile('rwb') as агым_VALUE:
                    json.loads(агым_VALUE.readline())
                    def 호출(исем,аргумент_МАССИВ=None):
                        Челтәр_хәбәр={'execute':исем}
                        if аргумент_МАССИВ: Челтәр_хәбәр['arguments']=аргумент_МАССИВ
                        агым_VALUE.write((json.dumps(Челтәр_хәбәр)+'\n').encode()); агым_VALUE.flush()
                        while True:
                            җавап_бирү=json.loads(агым_VALUE.readline())
                            if 'error' in җавап_бирү: raise AssertionError(җавап_бирү)
                            if 'return' in җавап_бирү: return җавап_бирү['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    мәгълүмат=IMAGE.read_bytes().split(b'\n',3)[3]
                    def нокта(X_координатасы,세로좌표): return tuple(мәгълүмат[(세로좌표*640+X_координатасы)*3:(세로좌표*640+X_координатасы)*3+3])
                    assert нокта(12,48)==(32,80,144),нокта(12,48)
                    assert len(set(нокта(X_координатасы,세로좌표) for 세로좌표 in range(100,116) for X_координатасы in range(24,56)))>1,'Hangul glyphs missing'
                    тышча('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    тышча("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    тышча('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): тышча('echo scroll-'+str(순번),'scroll-'+str(순번))
                    җибәрү(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    үлчәм=җибәрү(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in үлчәм,үлчәм
                    тышча('rm visible.txt')
                    호출('quit')
            Процесс.wait(timeout=5)
            раслау_отчет['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            раслау_отчет['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Процесс.poll() is None:
                Процесс.terminate()
                try: Процесс.wait(timeout=5)
                except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait()
            준비살피미.close(); Процесс.stdin.close(); Процесс.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(раслау_отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': эшләтү()
