#!/usr/bin/env python3
"""свой 커널의 оболочка, 프로세스 входные_данные_выход, Unicode GUI 터미널을 фактический_данные raspi4b에서 испытания."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 실행 import задача_корень, команда


def запустить():
    выход = задача_корень / 'build/verification/shell'; выход.mkdir(parents=True, exist_ok=True)
    проверка_Отчет = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((задача_корень / 'build/kernel8.img').read_bytes()).hexdigest()}
    расшифровка = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Процесс = subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        готовность_монитор=selectors.DefaultSelector(); готовность_монитор.register(Процесс.stdout,selectors.EVENT_READ)
        def получить_письмо(метка, выполнение_ТАЙМАУТ=45):
            данные=bytearray(); элемент_СМЕЩ=time.monotonic()+выполнение_ТАЙМАУТ
            while метка not in данные:
                if time.monotonic()>элемент_СМЕЩ or Процесс.poll() is not None: raise AssertionError('UART timeout/exit: '+данные.decode('utf-8','replace'))
                for 누름값,_ in готовность_монитор.select(.1):
                    блок_ЗНАЧЕН_652d4b53=누름값.fileobj.read(4096)
                    if блок_ЗНАЧЕН_652d4b53: данные.extend(блок_ЗНАЧЕН_652d4b53); расшифровка.extend(блок_ЗНАЧЕН_652d4b53)
                if b'PANIC:' in данные or b'FAIL ' in данные: raise AssertionError(данные)
            return данные.decode('utf-8','replace').replace('\r\n','\n')
        def написать(данные, метка=b'jkoros-native> '):
            Процесс.stdin.write(данные); Процесс.stdin.flush(); return получить_письмо(метка)
        def оболочка(строка_ввода, *예상결과):
            результат=написать(строка_ввода.encode()+b'\n')
            for ЗНАЧЕН in 예상결과: assert ЗНАЧЕН in результат, (строка_ввода,ЗНАЧЕН,результат)
            return результат
        def файл(Название):
            текст=оболочка('hex '+Название,'HEX BEGIN','HEX END'); ПОИСК_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',текст,re.S)
            данные=bytes.fromhex(''.join(ПОИСК_KR.group(2).split())); assert len(данные)==int(ПОИСК_KR.group(1)); return данные
        try:
            получить_письмо(b'jkoros-native> ')
            оболочка('mkdir 작업; cd 작업; pwd','/작업')
            оболочка('mkdir 하위; echo "한글 данные 😀" > приветствие_ae353e94.txt')
            assert файл('приветствие_ae353e94.txt')=='한글 данные 😀\n'.encode()
            оболочка('cp приветствие_ae353e94.txt экземпляр_ЗНАЧЕН.txt; mv экземпляр_ЗНАЧЕН.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 данные 😀')
            оболочка('cd 하위; cat ../приветствие_ae353e94.txt; cat /작업/приветствие_ae353e94.txt; pwd','한글 данные 😀','/작업/하위')
            оболочка('cd ..; rmdir 하위; echo $?','1\n')
            оболочка('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            оболочка('cp приветствие_ae353e94.txt приветствие_ae353e94.txt; echo $?','1\n'); assert файл('приветствие_ae353e94.txt')=='한글 данные 😀\n'.encode()
            оболочка('export приветствие_ae353e94=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in файл('приветствие_ae353e94.txt')
            оболочка("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert файл('리터럴')=='$인사\n누리\n'.encode()
            оболочка('echo one > выписка_ЗНАЧЕН; echo two >> выписка_ЗНАЧЕН; echo three >> выписка_ЗНАЧЕН')
            оболочка('cat < выписка_ЗНАЧЕН | grep t | tee 추림 | wc -l','2\n'); assert файл('추림')==b'two\nthree\n'
            оболочка('head -n 1 выписка_ЗНАЧЕН > лицевая_камера_ЗНАЧЕН; tail -n 1 выписка_ЗНАЧЕН > BACK_ЗНАЧЕН'); assert файл('앞')==b'one\n'; assert файл('뒤')==b'three\n'
            оболочка('grep absent выписка_ЗНАЧЕН; echo $?','1\n')
            оболочка('echo untouched > защитить_ЗНАЧЕН')
            оболочка('echo destroyed > защитить_ЗНАЧЕН |','명령이 빠졌습니다'); assert файл('защитить_ЗНАЧЕН')==b'untouched\n'
            оболочка('echo "oops','따옴표가 닫히지 않았습니다')
            оболочка('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            оболочка('echo bad 2> защитить_ЗНАЧЕН','번호를 지정한 файл дескриптор_ввод входные_данные_выход перейти_МОДА'); assert файл('защитить_ЗНАЧЕН')==b'untouched\n'
            оболочка('rm 빈파일 리터럴 выписка_ЗНАЧЕН 추림 лицевая_камера_ЗНАЧЕН BACK_ЗНАЧЕН защитить_ЗНАЧЕН')
            проверка_Отчет['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            оболочка("python -c 'print(123)' | wc -c",'4\n')
            оболочка("python -c 'print(456)' > программа_f5044b9b.txt"); assert файл('программа_f5044b9b.txt')==b'456\n'
            оболочка("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            оболочка("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < программа_f5044b9b.txt", "b'456\\n'", "b''")
            оболочка("python -c 'print(\"x\"*17000)' | wc -c", 'ошибка -28')
            оболочка('echo recovered | wc -c','10\n')
            оболочка("python -c 'import jkoros; print(jkoros.read("+'"/작업/программа_f5044b9b.txt"'+"))'",'456','exit 0')
            оболочка('cd /; javac Hello.java','Compiled:','exit 0')
            оболочка('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in файл('/작업/자바.txt')
            оболочка('cd 작업; echo "echo script > выполнение_KR" > команда.sh; echo "false || echo recovered >> выполнение_KR" >> команда.sh; sh команда.sh')
            assert файл('выполнение_KR')==b'script\nrecovered\n'
            оболочка('rm выполнение_KR; echo "exit 7" > Выход_программа.sh; sh Выход_программа.sh; echo $?','7\n')
            оболочка('rm Выход_программа.sh команда.sh программа_f5044b9b.txt 자바.txt приветствие_ae353e94.txt; cd /; rmdir 작업')
            проверка_Отчет['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            оболочка('echo history-proof','history-proof')
            результат=написать(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert результат.count('history-proof')>=2, результат
            написать(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            результат=написать(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in результат, результат
            результат=написать(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in результат,результат
            результат=написать('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in результат,результат
            긴글='한글'*50
            результат=написать(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in результат
            оболочка('terminal','TERMINAL READY')
            оболочка('clear')
            оболочка('echo "한글 терминал ABC xyz 012 😀"','한글 терминал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10); клиент.connect(str(모의제어접속))
                with клиент.makefile('rwb') as поток_ЗНАЧЕН:
                    json.loads(поток_ЗНАЧЕН.readline())
                    def 호출(Название,аргумент_МАССИВ=None):
                        сеть_письмо={'execute':Название}
                        if аргумент_МАССИВ: сеть_письмо['arguments']=аргумент_МАССИВ
                        поток_ЗНАЧЕН.write((json.dumps(сеть_письмо)+'\n').encode()); поток_ЗНАЧЕН.flush()
                        while True:
                            ответ=json.loads(поток_ЗНАЧЕН.readline())
                            if 'error' in ответ: raise AssertionError(ответ)
                            if 'return' in ответ: return ответ['return']
                    호출('qmp_capabilities')
                    фото=выход/'terminal.ppm'; 호출('screendump',{'filename':str(фото),'format':'ppm'})
                    호출('screendump',{'filename':str(выход/'terminal.png'),'format':'png'})
                    данные=фото.read_bytes().split(b'\n',3)[3]
                    def пиксель(координата_X,Y_координата): return tuple(данные[(Y_координата*640+координата_X)*3:(Y_координата*640+координата_X)*3+3])
                    assert пиксель(12,48)==(32,80,144),пиксель(12,48)
                    assert len(set(пиксель(координата_X,Y_координата) for Y_координата in range(100,116) for координата_X in range(24,56)))>1,'Hangul glyphs missing'
                    оболочка('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    оболочка("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(фото),'format':'ppm'})
                    복원자료=фото.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    оболочка('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): оболочка('echo scroll-'+str(순번),'scroll-'+str(순번))
                    написать(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(выход/'terminal-scroll.png'),'format':'png'})
                    результат=написать(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in результат,результат
                    оболочка('rm visible.txt')
                    호출('quit')
            Процесс.wait(timeout=5)
            проверка_Отчет['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            проверка_Отчет['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Процесс.poll() is None:
                Процесс.terminate()
                try: Процесс.wait(timeout=5)
                except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait()
            готовность_монитор.close(); Процесс.stdin.close(); Процесс.stdout.close()
            (выход/'serial.log').write_bytes(расшифровка)
            (выход/'report.json').write_text(json.dumps(проверка_Отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': запустить()
