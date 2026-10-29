#!/usr/bin/env python3
"""자체 커널의 обвивка, 프로세스 В_И, Unicode GUI 터미널을 действителен_данни raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from изпълнявам_команда import проект_корен, Команда


def Стартиране():
    출력결과 = проект_корен / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    проверка_отчет = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((проект_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    препис = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Процес = subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процес.stdout,selectors.EVENT_READ)
        def получавам_имейл(маркер, 시간제한=45):
            данни=bytearray(); прекратяване_на_повикването_Изместване=time.monotonic()+시간제한
            while маркер not in данни:
                if time.monotonic()>прекратяване_на_повикването_Изместване or Процес.poll() is not None: raise AssertionError('UART timeout/exit: '+данни.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: данни.extend(조각); препис.extend(조각)
                if b'PANIC:' in данни or b'FAIL ' in данни: raise AssertionError(данни)
            return данни.decode('utf-8','replace').replace('\r\n','\n')
        def изпращам(данни, маркер=b'jkoros-native> '):
            Процес.stdin.write(данни); Процес.stdin.flush(); return получавам_имейл(маркер)
        def обвивка(ред, *예상결과):
            РЕЗУЛТАТ=изпращам(ред.encode()+b'\n')
            for стойност in 예상결과: assert стойност in РЕЗУЛТАТ, (ред,стойност,РЕЗУЛТАТ)
            return РЕЗУЛТАТ
        def Файл(Име):
            Текст=обвивка('hex '+Име,'HEX BEGIN','HEX END'); търся_мярка=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Текст,re.S)
            данни=bytes.fromhex(''.join(търся_мярка.group(2).split())); assert len(данни)==int(търся_мярка.group(1)); return данни
        try:
            получавам_имейл(b'jkoros-native> ')
            обвивка('mkdir 작업; cd 작업; pwd','/작업')
            обвивка('mkdir 하위; echo "한글 данни 😀" > 인사.txt')
            assert Файл('인사.txt')=='한글 данни 😀\n'.encode()
            обвивка('cp 인사.txt копирам_стойност.txt; mv копирам_стойност.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 данни 😀')
            обвивка('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 данни 😀','/작업/하위')
            обвивка('cd ..; rmdir 하위; echo $?','1\n')
            обвивка('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            обвивка('cp 인사.txt 인사.txt; echo $?','1\n'); assert Файл('인사.txt')=='한글 данни 😀\n'.encode()
            обвивка('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Файл('인사.txt')
            обвивка("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Файл('리터럴')=='$인사\n누리\n'.encode()
            обвивка('echo one > команда_стойност; echo two >> команда_стойност; echo three >> команда_стойност')
            обвивка('cat < команда_стойност | grep t | tee 추림 | wc -l','2\n'); assert Файл('추림')==b'two\nthree\n'
            обвивка('head -n 1 команда_стойност > предна_стойност; tail -n 1 команда_стойност > НАЗАД_стойност'); assert Файл('앞')==b'one\n'; assert Файл('뒤')==b'three\n'
            обвивка('grep absent команда_стойност; echo $?','1\n')
            обвивка('echo untouched > защитавам_стойност')
            обвивка('echo destroyed > защитавам_стойност |','명령이 빠졌습니다'); assert Файл('защитавам_стойност')==b'untouched\n'
            обвивка('echo "oops','따옴표가 닫히지 않았습니다')
            обвивка('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            обвивка('echo bad 2> защитавам_стойност','번호를 지정한 Файл 서술자 В_И комутатор_режим'); assert Файл('защитавам_стойност')==b'untouched\n'
            обвивка('rm 빈파일 리터럴 команда_стойност 추림 предна_стойност НАЗАД_стойност защитавам_стойност')
            проверка_отчет['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            обвивка("python -c 'print(123)' | wc -c",'4\n')
            обвивка("python -c 'print(456)' > програма_f5044b9b.txt"); assert Файл('програма_f5044b9b.txt')==b'456\n'
            обвивка("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            обвивка("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < програма_f5044b9b.txt", "b'456\\n'", "b''")
            обвивка("python -c 'print(\"x\"*17000)' | wc -c", 'ГРЕШКА -28')
            обвивка('echo recovered | wc -c','10\n')
            обвивка("python -c 'import jkoros; print(jkoros.read("+'"/작업/програма_f5044b9b.txt"'+"))'",'456','exit 0')
            обвивка('cd /; javac Hello.java','Compiled:','exit 0')
            обвивка('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Файл('/작업/자바.txt')
            обвивка('cd 작업; echo "echo script > 실행결과" > Команда.sh; echo "false || echo recovered >> 실행결과" >> Команда.sh; sh Команда.sh')
            assert Файл('실행결과')==b'script\nrecovered\n'
            обвивка('rm 실행결과; echo "exit 7" > Изход_програма.sh; sh Изход_програма.sh; echo $?','7\n')
            обвивка('rm Изход_програма.sh Команда.sh програма_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            проверка_отчет['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            обвивка('echo history-proof','history-proof')
            РЕЗУЛТАТ=изпращам(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert РЕЗУЛТАТ.count('history-proof')>=2, РЕЗУЛТАТ
            изпращам(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            РЕЗУЛТАТ=изпращам(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in РЕЗУЛТАТ, РЕЗУЛТАТ
            РЕЗУЛТАТ=изпращам(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in РЕЗУЛТАТ,РЕЗУЛТАТ
            РЕЗУЛТАТ=изпращам('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in РЕЗУЛТАТ,РЕЗУЛТАТ
            긴글='한글'*50
            РЕЗУЛТАТ=изпращам(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in РЕЗУЛТАТ
            обвивка('terminal','TERMINAL READY')
            обвивка('clear')
            обвивка('echo "한글 Терминал ABC xyz 012 😀"','한글 Терминал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10); клиент.connect(str(모의제어접속))
                with клиент.makefile('rwb') as поток_стойност:
                    json.loads(поток_стойност.readline())
                    def 호출(Име,аргумент_масив=None):
                        мрежа_имейл={'execute':Име}
                        if аргумент_масив: мрежа_имейл['arguments']=аргумент_масив
                        поток_стойност.write((json.dumps(мрежа_имейл)+'\n').encode()); поток_стойност.flush()
                        while True:
                            отговор=json.loads(поток_стойност.readline())
                            if 'error' in отговор: raise AssertionError(отговор)
                            if 'return' in отговор: return отговор['return']
                    호출('qmp_capabilities')
                    снимка=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(снимка),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    данни=снимка.read_bytes().split(b'\n',3)[3]
                    def пиксел(x_координата,세로좌표): return tuple(данни[(세로좌표*640+x_координата)*3:(세로좌표*640+x_координата)*3+3])
                    assert пиксел(12,48)==(32,80,144),пиксел(12,48)
                    assert len(set(пиксел(x_координата,세로좌표) for 세로좌표 in range(100,116) for x_координата in range(24,56)))>1,'Hangul glyphs missing'
                    обвивка('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    обвивка("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(снимка),'format':'ppm'})
                    복원자료=снимка.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    обвивка('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): обвивка('echo scroll-'+str(순번),'scroll-'+str(순번))
                    изпращам(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    РЕЗУЛТАТ=изпращам(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in РЕЗУЛТАТ,РЕЗУЛТАТ
                    обвивка('rm visible.txt')
                    호출('quit')
            Процес.wait(timeout=5)
            проверка_отчет['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            проверка_отчет['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Процес.poll() is None:
                Процес.terminate()
                try: Процес.wait(timeout=5)
                except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
            준비살피미.close(); Процес.stdin.close(); Процес.stdout.close()
            (출력결과/'serial.log').write_bytes(препис)
            (출력결과/'report.json').write_text(json.dumps(проверка_отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Стартиране()
