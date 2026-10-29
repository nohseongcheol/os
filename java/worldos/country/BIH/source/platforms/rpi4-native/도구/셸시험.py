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
from 실행 import 기준, команда


def 시작():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    провјера_извјештај = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        процес = subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(процес.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            подаци=bytearray(); 끝위치=time.monotonic()+시간제한
            while 확인표시 not in подаци:
                if time.monotonic()>끝위치 or процес.poll() is not None: raise AssertionError('UART timeout/exit: '+подаци.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: подаци.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in подаци or b'FAIL ' in подаци: raise AssertionError(подаци)
            return подаци.decode('utf-8','replace').replace('\r\n','\n')
        def послати(подаци, 확인표시=b'jkoros-native> '):
            процес.stdin.write(подаци); процес.stdin.flush(); return 수신하기(확인표시)
        def љуска(редак, *예상결과):
            결과=послати(редак.encode()+b'\n')
            for вриједност in 예상결과: assert вриједност in 결과, (редак,вриједност,결과)
            return 결과
        def фајл(назив):
            текст=љуска('hex '+назив,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',текст,re.S)
            подаци=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(подаци)==int(찾은결과.group(1)); return подаци
        try:
            수신하기(b'jkoros-native> ')
            љуска('mkdir 작업; cd 작업; pwd','/작업')
            љуска('mkdir 하위; echo "한글 подаци 😀" > 인사.txt')
            assert фајл('인사.txt')=='한글 подаци 😀\n'.encode()
            љуска('cp 인사.txt инстанца_вриједност.txt; mv инстанца_вриједност.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 подаци 😀')
            љуска('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 подаци 😀','/작업/하위')
            љуска('cd ..; rmdir 하위; echo $?','1\n')
            љуска('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            љуска('cp 인사.txt 인사.txt; echo $?','1\n'); assert фајл('인사.txt')=='한글 подаци 😀\n'.encode()
            љуска('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in фајл('인사.txt')
            љуска("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert фајл('리터럴')=='$인사\n누리\n'.encode()
            љуска('echo one > изјава_вриједност; echo two >> изјава_вриједност; echo three >> изјава_вриједност')
            љуска('cat < изјава_вриједност | grep t | tee 추림 | wc -l','2\n'); assert фајл('추림')==b'two\nthree\n'
            љуска('head -n 1 изјава_вриједност > 앞; tail -n 1 изјава_вриједност > Назад_вриједност'); assert фајл('앞')==b'one\n'; assert фајл('뒤')==b'three\n'
            љуска('grep absent изјава_вриједност; echo $?','1\n')
            љуска('echo untouched > заштитити_вриједност')
            љуска('echo destroyed > заштитити_вриједност |','명령이 빠졌습니다'); assert фајл('заштитити_вриједност')==b'untouched\n'
            љуска('echo "oops','따옴표가 닫히지 않았습니다')
            љуска('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            љуска('echo bad 2> заштитити_вриједност','번호를 지정한 фајл 서술자 У_И промијенити_мод'); assert фајл('заштитити_вриједност')==b'untouched\n'
            љуска('rm 빈파일 리터럴 изјава_вриједност 추림 앞 Назад_вриједност заштитити_вриједност')
            провјера_извјештај['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            љуска("python -c 'print(123)' | wc -c",'4\n')
            љуска("python -c 'print(456)' > програм_f5044b9b.txt"); assert фајл('програм_f5044b9b.txt')==b'456\n'
            љуска("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            љуска("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < програм_f5044b9b.txt", "b'456\\n'", "b''")
            љуска("python -c 'print(\"x\"*17000)' | wc -c", 'грешка -28')
            љуска('echo recovered | wc -c','10\n')
            љуска("python -c 'import jkoros; print(jkoros.read("+'"/작업/програм_f5044b9b.txt"'+"))'",'456','exit 0')
            љуска('cd /; javac Hello.java','Compiled:','exit 0')
            љуска('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in фајл('/작업/자바.txt')
            љуска('cd 작업; echo "echo script > 실행결과" > команда.sh; echo "false || echo recovered >> 실행결과" >> команда.sh; sh команда.sh')
            assert фајл('실행결과')==b'script\nrecovered\n'
            љуска('rm 실행결과; echo "exit 7" > изаћи_програм.sh; sh изаћи_програм.sh; echo $?','7\n')
            љуска('rm изаћи_програм.sh команда.sh програм_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            провјера_извјештај['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            љуска('echo history-proof','history-proof')
            결과=послати(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            послати(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=послати(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=послати(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=послати('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=послати(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            љуска('terminal','TERMINAL READY')
            љуска('clear')
            љуска('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клијент:
                клијент.settimeout(10); клијент.connect(str(모의제어접속))
                with клијент.makefile('rwb') as ток_вриједност:
                    json.loads(ток_вриједност.readline())
                    def 호출(назив,аргумент_низ=None):
                        Мрежа_порука={'execute':назив}
                        if аргумент_низ: Мрежа_порука['arguments']=аргумент_низ
                        ток_вриједност.write((json.dumps(Мрежа_порука)+'\n').encode()); ток_вриједност.flush()
                        while True:
                            응답=json.loads(ток_вриједност.readline())
                            if 'error' in 응답: raise AssertionError(응답)
                            if 'return' in 응답: return 응답['return']
                    호출('qmp_capabilities')
                    слика=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(слика),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    подаци=слика.read_bytes().split(b'\n',3)[3]
                    def Пел(가로좌표,세로좌표): return tuple(подаци[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert Пел(12,48)==(32,80,144),Пел(12,48)
                    assert len(set(Пел(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    љуска('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    љуска("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(слика),'format':'ppm'})
                    복원자료=слика.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    љуска('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): љуска('echo scroll-'+str(순번),'scroll-'+str(순번))
                    послати(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=послати(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    љуска('rm visible.txt')
                    호출('quit')
            процес.wait(timeout=5)
            провјера_извјештај['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            провјера_извјештај['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if процес.poll() is None:
                процес.terminate()
                try: процес.wait(timeout=5)
                except subprocess.TimeoutExpired: процес.kill(); процес.wait()
            준비살피미.close(); процес.stdin.close(); процес.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(провјера_извјештај,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': 시작()
