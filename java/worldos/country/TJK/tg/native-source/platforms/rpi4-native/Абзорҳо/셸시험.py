#!/usr/bin/env python3
"""자체 커널의 восит, 프로세스 вуруд_хуруҷ, Unicode GUI 터미널을 воқеӣ_иттилоот raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from иҷро_кардан_фармон import 기준, фармон


def порча():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    санҷиши_эътибор_гузориш = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Раванд = subprocess.Popen(фармон()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Раванд.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            иттилоот=bytearray(); анҷом_додан_Интиқолшавӣ=time.monotonic()+시간제한
            while 확인표시 not in иттилоот:
                if time.monotonic()>анҷом_додан_Интиқолшавӣ or Раванд.poll() is not None: raise AssertionError('UART timeout/exit: '+иттилоот.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: иттилоот.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in иттилоот or b'FAIL ' in иттилоот: raise AssertionError(иттилоот)
            return иттилоот.decode('utf-8','replace').replace('\r\n','\n')
        def фиристодан(иттилоот, 확인표시=b'jkoros-native> '):
            Раванд.stdin.write(иттилоот); Раванд.stdin.flush(); return 수신하기(확인표시)
        def восит(хат, *예상결과):
            결과=фиристодан(хат.encode()+b'\n')
            for қимат in 예상결과: assert қимат in 결과, (хат,қимат,결과)
            return 결과
        def Файл(Ном):
            Матн=восит('hex '+Ном,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Матн,re.S)
            иттилоот=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(иттилоот)==int(찾은결과.group(1)); return иттилоот
        try:
            수신하기(b'jkoros-native> ')
            восит('mkdir 작업; cd 작업; pwd','/작업')
            восит('mkdir 하위; echo "한글 иттилоот 😀" > 인사.txt')
            assert Файл('인사.txt')=='한글 иттилоот 😀\n'.encode()
            восит('cp 인사.txt ҳолат_қимат.txt; mv ҳолат_қимат.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 иттилоот 😀')
            восит('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 иттилоот 😀','/작업/하위')
            восит('cd ..; rmdir 하위; echo $?','1\n')
            восит('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            восит('cp 인사.txt 인사.txt; echo $?','1\n'); assert Файл('인사.txt')=='한글 иттилоот 😀\n'.encode()
            восит('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Файл('인사.txt')
            восит("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Файл('리터럴')=='$인사\n누리\n'.encode()
            восит('echo one > баёния_қимат; echo two >> баёния_қимат; echo three >> баёния_қимат')
            восит('cat < баёния_қимат | grep t | tee 추림 | wc -l','2\n'); assert Файл('추림')==b'two\nthree\n'
            восит('head -n 1 баёния_қимат > 앞; tail -n 1 баёния_қимат > Бозгашт_қимат'); assert Файл('앞')==b'one\n'; assert Файл('뒤')==b'three\n'
            восит('grep absent баёния_қимат; echo $?','1\n')
            восит('echo untouched > муҳофизат_кардан_қимат')
            восит('echo destroyed > муҳофизат_кардан_қимат |','명령이 빠졌습니다'); assert Файл('муҳофизат_кардан_қимат')==b'untouched\n'
            восит('echo "oops','따옴표가 닫히지 않았습니다')
            восит('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            восит('echo bad 2> муҳофизат_кардан_қимат','번호를 지정한 Файл 서술자 вуруд_хуруҷ қатъу_васл_кардан_ҳолат'); assert Файл('муҳофизат_кардан_қимат')==b'untouched\n'
            восит('rm 빈파일 리터럴 баёния_қимат 추림 앞 Бозгашт_қимат муҳофизат_кардан_қимат')
            санҷиши_эътибор_гузориш['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            восит("python -c 'print(123)' | wc -c",'4\n')
            восит("python -c 'print(456)' > барнома_f5044b9b.txt"); assert Файл('барнома_f5044b9b.txt')==b'456\n'
            восит("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            восит("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < барнома_f5044b9b.txt", "b'456\\n'", "b''")
            восит("python -c 'print(\"x\"*17000)' | wc -c", 'Хато -28')
            восит('echo recovered | wc -c','10\n')
            восит("python -c 'import jkoros; print(jkoros.read("+'"/작업/барнома_f5044b9b.txt"'+"))'",'456','exit 0')
            восит('cd /; javac Hello.java','Compiled:','exit 0')
            восит('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Файл('/작업/자바.txt')
            восит('cd 작업; echo "echo script > 실행결과" > фармон.sh; echo "false || echo recovered >> 실행결과" >> фармон.sh; sh фармон.sh')
            assert Файл('실행결과')==b'script\nrecovered\n'
            восит('rm 실행결과; echo "exit 7" > Баромад_барнома.sh; sh Баромад_барнома.sh; echo $?','7\n')
            восит('rm Баромад_барнома.sh фармон.sh барнома_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            санҷиши_эътибор_гузориш['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            восит('echo history-proof','history-proof')
            결과=фиристодан(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            фиристодан(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=фиристодан(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=фиристодан(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=фиристодан('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=фиристодан(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            восит('terminal','TERMINAL READY')
            восит('clear')
            восит('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as муштарӣ:
                муштарӣ.settimeout(10); муштарӣ.connect(str(모의제어접속))
                with муштарӣ.makefile('rwb') as ҷараён_қимат:
                    json.loads(ҷараён_қимат.readline())
                    def 호출(Ном,аргумент_қатор=None):
                        Шабака_паём={'execute':Ном}
                        if аргумент_қатор: Шабака_паём['arguments']=аргумент_қатор
                        ҷараён_қимат.write((json.dumps(Шабака_паём)+'\n').encode()); ҷараён_қимат.flush()
                        while True:
                            ҷавоб_додан=json.loads(ҷараён_қимат.readline())
                            if 'error' in ҷавоб_додан: raise AssertionError(ҷавоб_додан)
                            if 'return' in ҷавоб_додан: return ҷавоб_додан['return']
                    호출('qmp_capabilities')
                    расм=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(расм),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    иттилоот=расм.read_bytes().split(b'\n',3)[3]
                    def пиксел(координатаи_х,세로좌표): return tuple(иттилоот[(세로좌표*640+координатаи_х)*3:(세로좌표*640+координатаи_х)*3+3])
                    assert пиксел(12,48)==(32,80,144),пиксел(12,48)
                    assert len(set(пиксел(координатаи_х,세로좌표) for 세로좌표 in range(100,116) for координатаи_х in range(24,56)))>1,'Hangul glyphs missing'
                    восит('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    восит("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(расм),'format':'ppm'})
                    복원자료=расм.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    восит('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): восит('echo scroll-'+str(순번),'scroll-'+str(순번))
                    фиристодан(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=фиристодан(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    восит('rm visible.txt')
                    호출('quit')
            Раванд.wait(timeout=5)
            санҷиши_эътибор_гузориш['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            санҷиши_эътибор_гузориш['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Раванд.poll() is None:
                Раванд.terminate()
                try: Раванд.wait(timeout=5)
                except subprocess.TimeoutExpired: Раванд.kill(); Раванд.wait()
            준비살피미.close(); Раванд.stdin.close(); Раванд.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(санҷиши_эътибор_гузориш,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': порча()
