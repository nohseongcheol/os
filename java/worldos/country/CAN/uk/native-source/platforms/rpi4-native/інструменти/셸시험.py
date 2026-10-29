#!/usr/bin/env python3
"""своє 커널의 оболонка, 프로세스 ввід_вивід, Unicode GUI 터미널을 фактично_дані raspi4b에서 випробування."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Виконати_команда import Дії_корінь, команда


def запустити():
    출력결과 = Дії_корінь / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    перевірка_звіт = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Дії_корінь / 'build/kernel8.img').read_bytes()).hexdigest()}
    транскрипт = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Процеси = subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процеси.stdout,selectors.EVENT_READ)
        def отримувати_повідомлення(маркер, 시간제한=45):
            дані=bytearray(); завершити_виклик_Зміщена_копія=time.monotonic()+시간제한
            while маркер not in дані:
                if time.monotonic()>завершити_виклик_Зміщена_копія or Процеси.poll() is not None: raise AssertionError('UART timeout/exit: '+дані.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: дані.extend(조각); транскрипт.extend(조각)
                if b'PANIC:' in дані or b'FAIL ' in дані: raise AssertionError(дані)
            return дані.decode('utf-8','replace').replace('\r\n','\n')
        def надсилати(дані, маркер=b'jkoros-native> '):
            Процеси.stdin.write(дані); Процеси.stdin.flush(); return отримувати_повідомлення(маркер)
        def оболонка(рядок_введення, *예상결과):
            результат=надсилати(рядок_введення.encode()+b'\n')
            for значення in 예상결과: assert значення in результат, (рядок_введення,значення,результат)
            return результат
        def файл(Назва):
            текст=оболонка('hex '+Назва,'HEX BEGIN','HEX END'); Пошук_КР=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',текст,re.S)
            дані=bytes.fromhex(''.join(Пошук_КР.group(2).split())); assert len(дані)==int(Пошук_КР.group(1)); return дані
        try:
            отримувати_повідомлення(b'jkoros-native> ')
            оболонка('mkdir 작업; cd 작업; pwd','/작업')
            оболонка('mkdir 하위; echo "한글 дані 😀" > 인사.txt')
            assert файл('인사.txt')=='한글 дані 😀\n'.encode()
            оболонка('cp 인사.txt екземпляр_значення.txt; mv екземпляр_значення.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 дані 😀')
            оболонка('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 дані 😀','/작업/하위')
            оболонка('cd ..; rmdir 하위; echo $?','1\n')
            оболонка('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            оболонка('cp 인사.txt 인사.txt; echo $?','1\n'); assert файл('인사.txt')=='한글 дані 😀\n'.encode()
            оболонка('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in файл('인사.txt')
            оболонка("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert файл('리터럴')=='$인사\n누리\n'.encode()
            оболонка('echo one > оператор_значення; echo two >> оператор_значення; echo three >> оператор_значення')
            оболонка('cat < оператор_значення | grep t | tee 추림 | wc -l','2\n'); assert файл('추림')==b'two\nthree\n'
            оболонка('head -n 1 оператор_значення > фронтальна_камера_значення; tail -n 1 оператор_значення > НАЗАД_значення'); assert файл('앞')==b'one\n'; assert файл('뒤')==b'three\n'
            оболонка('grep absent оператор_значення; echo $?','1\n')
            оболонка('echo untouched > захищати_значення')
            оболонка('echo destroyed > захищати_значення |','명령이 빠졌습니다'); assert файл('захищати_значення')==b'untouched\n'
            оболонка('echo "oops','따옴표가 닫히지 않았습니다')
            оболонка('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            оболонка('echo bad 2> захищати_значення','번호를 지정한 файл 서술자 ввід_вивід перехід_режим'); assert файл('захищати_значення')==b'untouched\n'
            оболонка('rm 빈파일 리터럴 оператор_значення 추림 фронтальна_камера_значення НАЗАД_значення захищати_значення')
            перевірка_звіт['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            оболонка("python -c 'print(123)' | wc -c",'4\n')
            оболонка("python -c 'print(456)' > програма_f5044b9b.txt"); assert файл('програма_f5044b9b.txt')==b'456\n'
            оболонка("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            оболонка("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < програма_f5044b9b.txt", "b'456\\n'", "b''")
            оболонка("python -c 'print(\"x\"*17000)' | wc -c", 'ПОМИЛКА -28')
            оболонка('echo recovered | wc -c','10\n')
            оболонка("python -c 'import jkoros; print(jkoros.read("+'"/작업/програма_f5044b9b.txt"'+"))'",'456','exit 0')
            оболонка('cd /; javac Hello.java','Compiled:','exit 0')
            оболонка('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in файл('/작업/자바.txt')
            оболонка('cd 작업; echo "echo script > 실행결과" > команда.sh; echo "false || echo recovered >> 실행결과" >> команда.sh; sh команда.sh')
            assert файл('실행결과')==b'script\nrecovered\n'
            оболонка('rm 실행결과; echo "exit 7" > Вийти_програма.sh; sh Вийти_програма.sh; echo $?','7\n')
            оболонка('rm Вийти_програма.sh команда.sh програма_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            перевірка_звіт['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            оболонка('echo history-proof','history-proof')
            результат=надсилати(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert результат.count('history-proof')>=2, результат
            надсилати(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            результат=надсилати(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in результат, результат
            результат=надсилати(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in результат,результат
            результат=надсилати('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in результат,результат
            긴글='한글'*50
            результат=надсилати(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in результат
            оболонка('terminal','TERMINAL READY')
            оболонка('clear')
            оболонка('echo "한글 термінал ABC xyz 012 😀"','한글 термінал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клієнт:
                клієнт.settimeout(10); клієнт.connect(str(모의제어접속))
                with клієнт.makefile('rwb') as потік_значення:
                    json.loads(потік_значення.readline())
                    def 호출(Назва,аргумент_масив=None):
                        мережа_повідомлення={'execute':Назва}
                        if аргумент_масив: мережа_повідомлення['arguments']=аргумент_масив
                        потік_значення.write((json.dumps(мережа_повідомлення)+'\n').encode()); потік_значення.flush()
                        while True:
                            відповідь=json.loads(потік_значення.readline())
                            if 'error' in відповідь: raise AssertionError(відповідь)
                            if 'return' in відповідь: return відповідь['return']
                    호출('qmp_capabilities')
                    фото=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(фото),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    дані=фото.read_bytes().split(b'\n',3)[3]
                    def елемент_зображення(координата_X,세로좌표): return tuple(дані[(세로좌표*640+координата_X)*3:(세로좌표*640+координата_X)*3+3])
                    assert елемент_зображення(12,48)==(32,80,144),елемент_зображення(12,48)
                    assert len(set(елемент_зображення(координата_X,세로좌표) for 세로좌표 in range(100,116) for координата_X in range(24,56)))>1,'Hangul glyphs missing'
                    оболонка('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    оболонка("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(фото),'format':'ppm'})
                    복원자료=фото.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    оболонка('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): оболонка('echo scroll-'+str(순번),'scroll-'+str(순번))
                    надсилати(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    результат=надсилати(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in результат,результат
                    оболонка('rm visible.txt')
                    호출('quit')
            Процеси.wait(timeout=5)
            перевірка_звіт['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            перевірка_звіт['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Процеси.poll() is None:
                Процеси.terminate()
                try: Процеси.wait(timeout=5)
                except subprocess.TimeoutExpired: Процеси.kill(); Процеси.wait()
            준비살피미.close(); Процеси.stdin.close(); Процеси.stdout.close()
            (출력결과/'serial.log').write_bytes(транскрипт)
            (출력결과/'report.json').write_text(json.dumps(перевірка_звіт,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': запустити()
