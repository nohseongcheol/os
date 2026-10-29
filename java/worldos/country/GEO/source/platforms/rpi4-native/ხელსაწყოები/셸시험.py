#!/usr/bin/env python3
"""자체 커널의 გარემო, 프로세스 შეტანა_გამოტანა, Unicode GUI 터미널을 რეალური_მონაცემები raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from შესრულება_ბრძანება import პროეცირება_ფესვი, ბრძანება


def გაშვება():
    출력결과 = პროეცირება_ფესვი / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    გადამოწმება_ანგარიში = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        პროცესი = subprocess.Popen(ბრძანება()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(პროცესი.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            მონაცემები=bytearray(); დასასრული_ოფსეტი=time.monotonic()+시간제한
            while 확인표시 not in მონაცემები:
                if time.monotonic()>დასასრული_ოფსეტი or პროცესი.poll() is not None: raise AssertionError('UART timeout/exit: '+მონაცემები.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: მონაცემები.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in მონაცემები or b'FAIL ' in მონაცემები: raise AssertionError(მონაცემები)
            return მონაცემები.decode('utf-8','replace').replace('\r\n','\n')
        def გაგზავნა(მონაცემები, 확인표시=b'jkoros-native> '):
            პროცესი.stdin.write(მონაცემები); პროცესი.stdin.flush(); return 수신하기(확인표시)
        def გარემო(ხაზი, *예상결과):
            გაზომვა=გაგზავნა(ხაზი.encode()+b'\n')
            for მნიშვნელობა in 예상결과: assert მნიშვნელობა in გაზომვა, (ხაზი,მნიშვნელობა,გაზომვა)
            return გაზომვა
        def ფაილი(სახელი):
            ტექსტი=გარემო('hex '+სახელი,'HEX BEGIN','HEX END'); ძებნა_გაზომვა=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ტექსტი,re.S)
            მონაცემები=bytes.fromhex(''.join(ძებნა_გაზომვა.group(2).split())); assert len(მონაცემები)==int(ძებნა_გაზომვა.group(1)); return მონაცემები
        try:
            수신하기(b'jkoros-native> ')
            გარემო('mkdir 작업; cd 작업; pwd','/작업')
            გარემო('mkdir 하위; echo "한글 მონაცემები 😀" > 인사.txt')
            assert ფაილი('인사.txt')=='한글 მონაცემები 😀\n'.encode()
            გარემო('cp 인사.txt ასლი_მნიშვნელობა.txt; mv ასლი_მნიშვნელობა.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 მონაცემები 😀')
            გარემო('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 მონაცემები 😀','/작업/하위')
            გარემო('cd ..; rmdir 하위; echo $?','1\n')
            გარემო('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            გარემო('cp 인사.txt 인사.txt; echo $?','1\n'); assert ფაილი('인사.txt')=='한글 მონაცემები 😀\n'.encode()
            გარემო('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ფაილი('인사.txt')
            გარემო("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ფაილი('리터럴')=='$인사\n누리\n'.encode()
            გარემო('echo one > ბრძანება_მნიშვნელობა; echo two >> ბრძანება_მნიშვნელობა; echo three >> ბრძანება_მნიშვნელობა')
            გარემო('cat < ბრძანება_მნიშვნელობა | grep t | tee 추림 | wc -l','2\n'); assert ფაილი('추림')==b'two\nthree\n'
            გარემო('head -n 1 ბრძანება_მნიშვნელობა > 앞; tail -n 1 ბრძანება_მნიშვნელობა > უკან_მნიშვნელობა'); assert ფაილი('앞')==b'one\n'; assert ფაილი('뒤')==b'three\n'
            გარემო('grep absent ბრძანება_მნიშვნელობა; echo $?','1\n')
            გარემო('echo untouched > დაცვა_მნიშვნელობა')
            გარემო('echo destroyed > დაცვა_მნიშვნელობა |','명령이 빠졌습니다'); assert ფაილი('დაცვა_მნიშვნელობა')==b'untouched\n'
            გარემო('echo "oops','따옴표가 닫히지 않았습니다')
            გარემო('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            გარემო('echo bad 2> დაცვა_მნიშვნელობა','번호를 지정한 ფაილი 서술자 შეტანა_გამოტანა გადართვა_რეჟიმი'); assert ფაილი('დაცვა_მნიშვნელობა')==b'untouched\n'
            გარემო('rm 빈파일 리터럴 ბრძანება_მნიშვნელობა 추림 앞 უკან_მნიშვნელობა დაცვა_მნიშვნელობა')
            გადამოწმება_ანგარიში['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            გარემო("python -c 'print(123)' | wc -c",'4\n')
            გარემო("python -c 'print(456)' > აპი_f5044b9b.txt"); assert ფაილი('აპი_f5044b9b.txt')==b'456\n'
            გარემო("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            გარემო("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < აპი_f5044b9b.txt", "b'456\\n'", "b''")
            გარემო("python -c 'print(\"x\"*17000)' | wc -c", 'შეცდომა -28')
            გარემო('echo recovered | wc -c','10\n')
            გარემო("python -c 'import jkoros; print(jkoros.read("+'"/작업/აპი_f5044b9b.txt"'+"))'",'456','exit 0')
            გარემო('cd /; javac Hello.java','Compiled:','exit 0')
            გარემო('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ფაილი('/작업/자바.txt')
            გარემო('cd 작업; echo "echo script > 실행결과" > ბრძანება.sh; echo "false || echo recovered >> 실행결과" >> ბრძანება.sh; sh ბრძანება.sh')
            assert ფაილი('실행결과')==b'script\nrecovered\n'
            გარემო('rm 실행결과; echo "exit 7" > გასვლა_აპი.sh; sh გასვლა_აპი.sh; echo $?','7\n')
            გარემო('rm გასვლა_აპი.sh ბრძანება.sh აპი_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            გადამოწმება_ანგარიში['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            გარემო('echo history-proof','history-proof')
            გაზომვა=გაგზავნა(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert გაზომვა.count('history-proof')>=2, გაზომვა
            გაგზავნა(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            გაზომვა=გაგზავნა(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in გაზომვა, გაზომვა
            გაზომვა=გაგზავნა(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in გაზომვა,გაზომვა
            გაზომვა=გაგზავნა('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in გაზომვა,გაზომვა
            긴글='한글'*50
            გაზომვა=გაგზავნა(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in გაზომვა
            გარემო('terminal','TERMINAL READY')
            გარემო('clear')
            გარემო('echo "한글 ტერმინალი ABC xyz 012 😀"','한글 ტერმინალი ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as კლიენტი:
                კლიენტი.settimeout(10); კლიენტი.connect(str(모의제어접속))
                with კლიენტი.makefile('rwb') as ნაკადი_მნიშვნელობა:
                    json.loads(ნაკადი_მნიშვნელობა.readline())
                    def 호출(სახელი,არგუმენტი_მასივი=None):
                        ქსელი_წერილი={'execute':სახელი}
                        if არგუმენტი_მასივი: ქსელი_წერილი['arguments']=არგუმენტი_მასივი
                        ნაკადი_მნიშვნელობა.write((json.dumps(ქსელი_წერილი)+'\n').encode()); ნაკადი_მნიშვნელობა.flush()
                        while True:
                            პასუხი=json.loads(ნაკადი_მნიშვნელობა.readline())
                            if 'error' in პასუხი: raise AssertionError(პასუხი)
                            if 'return' in პასუხი: return პასუხი['return']
                    호출('qmp_capabilities')
                    ნახატი=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ნახატი),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    მონაცემები=ნახატი.read_bytes().split(b'\n',3)[3]
                    def პიქსელი(x_კოორდინატა,Y_ღილაკი_კოორდინატი): return tuple(მონაცემები[(Y_ღილაკი_კოორდინატი*640+x_კოორდინატა)*3:(Y_ღილაკი_კოორდინატი*640+x_კოორდინატა)*3+3])
                    assert პიქსელი(12,48)==(32,80,144),პიქსელი(12,48)
                    assert len(set(პიქსელი(x_კოორდინატა,Y_ღილაკი_კოორდინატი) for Y_ღილაკი_კოორდინატი in range(100,116) for x_კოორდინატა in range(24,56)))>1,'Hangul glyphs missing'
                    გარემო('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    გარემო("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ნახატი),'format':'ppm'})
                    복원자료=ნახატი.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    გარემო('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): გარემო('echo scroll-'+str(순번),'scroll-'+str(순번))
                    გაგზავნა(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    გაზომვა=გაგზავნა(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in გაზომვა,გაზომვა
                    გარემო('rm visible.txt')
                    호출('quit')
            პროცესი.wait(timeout=5)
            გადამოწმება_ანგარიში['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            გადამოწმება_ანგარიში['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if პროცესი.poll() is None:
                პროცესი.terminate()
                try: პროცესი.wait(timeout=5)
                except subprocess.TimeoutExpired: პროცესი.kill(); პროცესი.wait()
            준비살피미.close(); პროცესი.stdin.close(); პროცესი.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': გაშვება()
