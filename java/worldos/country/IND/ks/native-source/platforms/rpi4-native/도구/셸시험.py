#!/usr/bin/env python3
"""자체 커널의 셸, 프로세스 입출력, Unicode GUI 터미널을 실제 raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 실행 import 기준, 명령


def 시작():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    검증기록 = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        실행과정 = subprocess.Popen(명령()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(실행과정.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            자료=bytearray(); 끝위치=time.monotonic()+시간제한
            while 확인표시 not in 자료:
                if time.monotonic()>끝위치 or 실행과정.poll() is not None: raise AssertionError('UART timeout/exit: '+자료.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: 자료.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in 자료 or b'FAIL ' in 자료: raise AssertionError(자료)
            return 자료.decode('utf-8','replace').replace('\r\n','\n')
        def 보내기(자료, 확인표시=b'jkoros-native> '):
            실행과정.stdin.write(자료); 실행과정.stdin.flush(); return 수신하기(확인표시)
        def 셸(줄, *예상결과):
            결과=보내기(줄.encode()+b'\n')
            for 값 in 예상결과: assert 값 in 결과, (줄,값,결과)
            return 결과
        def फ़ाइल(이름):
            글=셸('hex '+이름,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',글,re.S)
            자료=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(자료)==int(찾은결과.group(1)); return 자료
        try:
            수신하기(b'jkoros-native> ')
            셸('mkdir 작업; cd 작업; pwd','/작업')
            셸('mkdir 하위; echo "한글 자료 😀" > 인사.txt')
            assert फ़ाइल('인사.txt')=='한글 자료 😀\n'.encode()
            셸('cp 인사.txt 복사.txt; mv 복사.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 자료 😀')
            셸('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 자료 😀','/작업/하위')
            셸('cd ..; rmdir 하위; echo $?','1\n')
            셸('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            셸('cp 인사.txt 인사.txt; echo $?','1\n'); assert फ़ाइल('인사.txt')=='한글 자료 😀\n'.encode()
            셸('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in फ़ाइल('인사.txt')
            셸("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert फ़ाइल('리터럴')=='$인사\n누리\n'.encode()
            셸('echo one > 문장; echo two >> 문장; echo three >> 문장')
            셸('cat < 문장 | grep t | tee 추림 | wc -l','2\n'); assert फ़ाइल('추림')==b'two\nthree\n'
            셸('head -n 1 문장 > 앞; tail -n 1 문장 > 뒤'); assert फ़ाइल('앞')==b'one\n'; assert फ़ाइल('뒤')==b'three\n'
            셸('grep absent 문장; echo $?','1\n')
            셸('echo untouched > 보호')
            셸('echo destroyed > 보호 |','명령이 빠졌습니다'); assert फ़ाइल('보호')==b'untouched\n'
            셸('echo "oops','따옴표가 닫히지 않았습니다')
            셸('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            셸('echo bad 2> 보호','번호를 지정한 फ़ाइल 서술자 입출력 전환'); assert फ़ाइल('보호')==b'untouched\n'
            셸('rm 빈파일 리터럴 문장 추림 앞 뒤 보호')
            검증기록['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            셸("python -c 'print(123)' | wc -c",'4\n')
            셸("python -c 'print(456)' > 프로그램.txt"); assert फ़ाइल('프로그램.txt')==b'456\n'
            셸("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            셸("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < 프로그램.txt", "b'456\\n'", "b''")
            셸("python -c 'print(\"x\"*17000)' | wc -c", '오류 -28')
            셸('echo recovered | wc -c','10\n')
            셸("python -c 'import jkoros; print(jkoros.read("+'"/작업/프로그램.txt"'+"))'",'456','exit 0')
            셸('cd /; javac Hello.java','Compiled:','exit 0')
            셸('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in फ़ाइल('/작업/자바.txt')
            셸('cd 작업; echo "echo script > 실행결과" > 명령.sh; echo "false || echo recovered >> 실행결과" >> 명령.sh; sh 명령.sh')
            assert फ़ाइल('실행결과')==b'script\nrecovered\n'
            셸('rm 실행결과; echo "exit 7" > 종료.sh; sh 종료.sh; echo $?','7\n')
            셸('rm 종료.sh 명령.sh 프로그램.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            검증기록['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            셸('echo history-proof','history-proof')
            결과=보내기(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            보내기(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=보내기(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=보내기(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=보내기('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=보내기(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            셸('terminal','TERMINAL READY')
            셸('clear')
            셸('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as 접속자:
                접속자.settimeout(10); 접속자.connect(str(모의제어접속))
                with 접속자.makefile('rwb') as 흐름:
                    json.loads(흐름.readline())
                    def 호출(이름,인수배열=None):
                        통신문={'execute':이름}
                        if 인수배열: 통신문['arguments']=인수배열
                        흐름.write((json.dumps(통신문)+'\n').encode()); 흐름.flush()
                        while True:
                            응답=json.loads(흐름.readline())
                            if 'error' in 응답: raise AssertionError(응답)
                            if 'return' in 응답: return 응답['return']
                    호출('qmp_capabilities')
                    실행영상=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(실행영상),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    자료=실행영상.read_bytes().split(b'\n',3)[3]
                    def 화소(가로좌표,세로좌표): return tuple(자료[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert 화소(12,48)==(32,80,144),화소(12,48)
                    assert len(set(화소(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    셸('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    셸("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(실행영상),'format':'ppm'})
                    복원자료=실행영상.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    셸('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): 셸('echo scroll-'+str(순번),'scroll-'+str(순번))
                    보내기(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=보내기(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    셸('rm visible.txt')
                    호출('quit')
            실행과정.wait(timeout=5)
            검증기록['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            검증기록['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if 실행과정.poll() is None:
                실행과정.terminate()
                try: 실행과정.wait(timeout=5)
                except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait()
            준비살피미.close(); 실행과정.stdin.close(); 실행과정.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': 시작()
