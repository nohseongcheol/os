#!/usr/bin/env python3
"""자체 커널의 абалонка, 프로세스 увод_вывад, Unicode GUI 터미널을 фактычны_дадзеныя raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from выканаць_каманда import 기준, Загад


def Выканаць():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    праверка_справаздача = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Працэс = subprocess.Popen(Загад()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Працэс.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            дадзеныя=bytearray(); скончыць_Зрух=time.monotonic()+시간제한
            while 확인표시 not in дадзеныя:
                if time.monotonic()>скончыць_Зрух or Працэс.poll() is not None: raise AssertionError('UART timeout/exit: '+дадзеныя.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: дадзеныя.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in дадзеныя or b'FAIL ' in дадзеныя: raise AssertionError(дадзеныя)
            return дадзеныя.decode('utf-8','replace').replace('\r\n','\n')
        def адправіць(дадзеныя, 확인표시=b'jkoros-native> '):
            Працэс.stdin.write(дадзеныя); Працэс.stdin.flush(); return 수신하기(확인표시)
        def абалонка(лінія, *예상결과):
            결과=адправіць(лінія.encode()+b'\n')
            for значэнне in 예상결과: assert значэнне in 결과, (лінія,значэнне,결과)
            return 결과
        def Файл(Назва):
            Тэкст=абалонка('hex '+Назва,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Тэкст,re.S)
            дадзеныя=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(дадзеныя)==int(찾은결과.group(1)); return дадзеныя
        try:
            수신하기(b'jkoros-native> ')
            абалонка('mkdir 작업; cd 작업; pwd','/작업')
            абалонка('mkdir 하위; echo "한글 дадзеныя 😀" > 인사.txt')
            assert Файл('인사.txt')=='한글 дадзеныя 😀\n'.encode()
            абалонка('cp 인사.txt капіяваць_значэнне.txt; mv капіяваць_значэнне.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 дадзеныя 😀')
            абалонка('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 дадзеныя 😀','/작업/하위')
            абалонка('cd ..; rmdir 하위; echo $?','1\n')
            абалонка('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            абалонка('cp 인사.txt 인사.txt; echo $?','1\n'); assert Файл('인사.txt')=='한글 дадзеныя 😀\n'.encode()
            абалонка('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Файл('인사.txt')
            абалонка("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Файл('리터럴')=='$인사\n누리\n'.encode()
            абалонка('echo one > аператар_значэнне; echo two >> аператар_значэнне; echo three >> аператар_значэнне')
            абалонка('cat < аператар_значэнне | grep t | tee 추림 | wc -l','2\n'); assert Файл('추림')==b'two\nthree\n'
            абалонка('head -n 1 аператар_значэнне > пярэдняя_камера_значэнне; tail -n 1 аператар_значэнне > Назад_значэнне'); assert Файл('앞')==b'one\n'; assert Файл('뒤')==b'three\n'
            абалонка('grep absent аператар_значэнне; echo $?','1\n')
            абалонка('echo untouched > ахоўваць_значэнне')
            абалонка('echo destroyed > ахоўваць_значэнне |','명령이 빠졌습니다'); assert Файл('ахоўваць_значэнне')==b'untouched\n'
            абалонка('echo "oops','따옴표가 닫히지 않았습니다')
            абалонка('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            абалонка('echo bad 2> ахоўваць_значэнне','번호를 지정한 Файл 서술자 увод_вывад пераход_рэжым'); assert Файл('ахоўваць_значэнне')==b'untouched\n'
            абалонка('rm 빈파일 리터럴 аператар_значэнне 추림 пярэдняя_камера_значэнне Назад_значэнне ахоўваць_значэнне')
            праверка_справаздача['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            абалонка("python -c 'print(123)' | wc -c",'4\n')
            абалонка("python -c 'print(456)' > праграма_f5044b9b.txt"); assert Файл('праграма_f5044b9b.txt')==b'456\n'
            абалонка("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            абалонка("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < праграма_f5044b9b.txt", "b'456\\n'", "b''")
            абалонка("python -c 'print(\"x\"*17000)' | wc -c", 'ПАМЫЛКА -28')
            абалонка('echo recovered | wc -c','10\n')
            абалонка("python -c 'import jkoros; print(jkoros.read("+'"/작업/праграма_f5044b9b.txt"'+"))'",'456','exit 0')
            абалонка('cd /; javac Hello.java','Compiled:','exit 0')
            абалонка('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Файл('/작업/자바.txt')
            абалонка('cd 작업; echo "echo script > 실행결과" > Загад.sh; echo "false || echo recovered >> 실행결과" >> Загад.sh; sh Загад.sh')
            assert Файл('실행결과')==b'script\nrecovered\n'
            абалонка('rm 실행결과; echo "exit 7" > Выхад_праграма.sh; sh Выхад_праграма.sh; echo $?','7\n')
            абалонка('rm Выхад_праграма.sh Загад.sh праграма_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            праверка_справаздача['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            абалонка('echo history-proof','history-proof')
            결과=адправіць(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            адправіць(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=адправіць(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=адправіць(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=адправіць('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=адправіць(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            абалонка('terminal','TERMINAL READY')
            абалонка('clear')
            абалонка('echo "한글 Тэрмінал ABC xyz 012 😀"','한글 Тэрмінал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as кліент:
                кліент.settimeout(10); кліент.connect(str(모의제어접속))
                with кліент.makefile('rwb') as паток_значэнне:
                    json.loads(паток_значэнне.readline())
                    def 호출(Назва,аргумент_масіў=None):
                        Сетка_ліст={'execute':Назва}
                        if аргумент_масіў: Сетка_ліст['arguments']=аргумент_масіў
                        паток_значэнне.write((json.dumps(Сетка_ліст)+'\n').encode()); паток_значэнне.flush()
                        while True:
                            адказаць=json.loads(паток_значэнне.readline())
                            if 'error' in адказаць: raise AssertionError(адказаць)
                            if 'return' in адказаць: return адказаць['return']
                    호출('qmp_capabilities')
                    выява=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(выява),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    дадзеныя=выява.read_bytes().split(b'\n',3)[3]
                    def пэл(каардыната_x,세로좌표): return tuple(дадзеныя[(세로좌표*640+каардыната_x)*3:(세로좌표*640+каардыната_x)*3+3])
                    assert пэл(12,48)==(32,80,144),пэл(12,48)
                    assert len(set(пэл(каардыната_x,세로좌표) for 세로좌표 in range(100,116) for каардыната_x in range(24,56)))>1,'Hangul glyphs missing'
                    абалонка('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    абалонка("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(выява),'format':'ppm'})
                    복원자료=выява.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    абалонка('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): абалонка('echo scroll-'+str(순번),'scroll-'+str(순번))
                    адправіць(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=адправіць(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    абалонка('rm visible.txt')
                    호출('quit')
            Працэс.wait(timeout=5)
            праверка_справаздача['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            праверка_справаздача['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Працэс.poll() is None:
                Працэс.terminate()
                try: Працэс.wait(timeout=5)
                except subprocess.TimeoutExpired: Працэс.kill(); Працэс.wait()
            준비살피미.close(); Працэс.stdin.close(); Працэс.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(праверка_справаздача,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Выканаць()
