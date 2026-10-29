#!/usr/bin/env python3
"""자체 커널의 سیپۍ, 프로세스 ننوتنی_وتنی, Unicode GUI 터미널을 실제 raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 실행 import 기준, بولۍ


def ځغلول():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    باورکړن_راپور = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        بهير = subprocess.Popen(بولۍ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(بهير.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            اومتوک=bytearray(); 끝위치=time.monotonic()+시간제한
            while 확인표시 not in اومتوک:
                if time.monotonic()>끝위치 or بهير.poll() is not None: raise AssertionError('UART timeout/exit: '+اومتوک.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: اومتوک.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in اومتوک or b'FAIL ' in اومتوک: raise AssertionError(اومتوک)
            return اومتوک.decode('utf-8','replace').replace('\r\n','\n')
        def استول(اومتوک, 확인표시=b'jkoros-native> '):
            بهير.stdin.write(اومتوک); بهير.stdin.flush(); return 수신하기(확인표시)
        def سیپۍ(ليکه, *예상결과):
            결과=استول(ليکه.encode()+b'\n')
            for ارزښت in 예상결과: assert ارزښت in 결과, (ليکه,ارزښت,결과)
            return 결과
        def دوتنه(نوم):
            ليکنه=سیپۍ('hex '+نوم,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ليکنه,re.S)
            اومتوک=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(اومتوک)==int(찾은결과.group(1)); return اومتوک
        try:
            수신하기(b'jkoros-native> ')
            سیپۍ('mkdir 작업; cd 작업; pwd','/작업')
            سیپۍ('mkdir 하위; echo "한글 اومتوک 😀" > 인사.txt')
            assert دوتنه('인사.txt')=='한글 اومتوک 😀\n'.encode()
            سیپۍ('cp 인사.txt بېلګه_ارزښت_37b3d3b1.txt; mv بېلګه_ارزښت_37b3d3b1.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 اومتوک 😀')
            سیپۍ('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 اومتوک 😀','/작업/하위')
            سیپۍ('cd ..; rmdir 하위; echo $?','1\n')
            سیپۍ('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            سیپۍ('cp 인사.txt 인사.txt; echo $?','1\n'); assert دوتنه('인사.txt')=='한글 اومتوک 😀\n'.encode()
            سیپۍ('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in دوتنه('인사.txt')
            سیپۍ("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert دوتنه('리터럴')=='$인사\n누리\n'.encode()
            سیپۍ('echo one > وينا_ارزښت; echo two >> وينا_ارزښت; echo three >> وينا_ارزښت')
            سیپۍ('cat < وينا_ارزښت | grep t | tee 추림 | wc -l','2\n'); assert دوتنه('추림')==b'two\nthree\n'
            سیپۍ('head -n 1 وينا_ارزښت > 앞; tail -n 1 وينا_ارزښت > 뒤'); assert دوتنه('앞')==b'one\n'; assert دوتنه('뒤')==b'three\n'
            سیپۍ('grep absent وينا_ارزښت; echo $?','1\n')
            سیپۍ('echo untouched > خونديېل_ارزښت')
            سیپۍ('echo destroyed > خونديېل_ارزښت |','명령이 빠졌습니다'); assert دوتنه('خونديېل_ارزښت')==b'untouched\n'
            سیپۍ('echo "oops','따옴표가 닫히지 않았습니다')
            سیپۍ('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            سیپۍ('echo bad 2> خونديېل_ارزښت','번호를 지정한 دوتنه 서술자 ننوتنی_وتنی 전환'); assert دوتنه('خونديېل_ارزښت')==b'untouched\n'
            سیپۍ('rm 빈파일 리터럴 وينا_ارزښت 추림 앞 뒤 خونديېل_ارزښت')
            باورکړن_راپور['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            سیپۍ("python -c 'print(123)' | wc -c",'4\n')
            سیپۍ("python -c 'print(456)' > کاريال_f5044b9b.txt"); assert دوتنه('کاريال_f5044b9b.txt')==b'456\n'
            سیپۍ("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            سیپۍ("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < کاريال_f5044b9b.txt", "b'456\\n'", "b''")
            سیپۍ("python -c 'print(\"x\"*17000)' | wc -c", 'تېروتنه -28')
            سیپۍ('echo recovered | wc -c','10\n')
            سیپۍ("python -c 'import jkoros; print(jkoros.read("+'"/작업/کاريال_f5044b9b.txt"'+"))'",'456','exit 0')
            سیپۍ('cd /; javac Hello.java','Compiled:','exit 0')
            سیپۍ('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in دوتنه('/작업/자바.txt')
            سیپۍ('cd 작업; echo "echo script > 실행결과" > بولۍ.sh; echo "false || echo recovered >> 실행결과" >> بولۍ.sh; sh بولۍ.sh')
            assert دوتنه('실행결과')==b'script\nrecovered\n'
            سیپۍ('rm 실행결과; echo "exit 7" > وتون_کاريال.sh; sh وتون_کاريال.sh; echo $?','7\n')
            سیپۍ('rm وتون_کاريال.sh بولۍ.sh کاريال_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            باورکړن_راپور['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            سیپۍ('echo history-proof','history-proof')
            결과=استول(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            استول(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=استول(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=استول(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=استول('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=استول(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            سیپۍ('terminal','TERMINAL READY')
            سیپۍ('clear')
            سیپۍ('echo "한글 پايالی ABC xyz 012 😀"','한글 پايالی ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as پېرن:
                پېرن.settimeout(10); پېرن.connect(str(모의제어접속))
                with پېرن.makefile('rwb') as بهنګ_ارزښت:
                    json.loads(بهنګ_ارزښت.readline())
                    def 호출(نوم,ارزښتوړى_لړوند=None):
                        جال_استوزه={'execute':نوم}
                        if ارزښتوړى_لړوند: جال_استوزه['arguments']=ارزښتوړى_لړوند
                        بهنګ_ارزښت.write((json.dumps(جال_استوزه)+'\n').encode()); بهنګ_ارزښت.flush()
                        while True:
                            응답=json.loads(بهنګ_ارزښت.readline())
                            if 'error' in 응답: raise AssertionError(응답)
                            if 'return' in 응답: return 응답['return']
                    호출('qmp_capabilities')
                    انځور=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(انځور),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    اومتوک=انځور.read_bytes().split(b'\n',3)[3]
                    def پکسل(가로좌표,세로좌표): return tuple(اومتوک[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert پکسل(12,48)==(32,80,144),پکسل(12,48)
                    assert len(set(پکسل(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    سیپۍ('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    سیپۍ("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(انځور),'format':'ppm'})
                    복원자료=انځور.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    سیپۍ('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): سیپۍ('echo scroll-'+str(순번),'scroll-'+str(순번))
                    استول(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=استول(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    سیپۍ('rm visible.txt')
                    호출('quit')
            بهير.wait(timeout=5)
            باورکړن_راپور['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            باورکړن_راپور['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if بهير.poll() is None:
                بهير.terminate()
                try: بهير.wait(timeout=5)
                except subprocess.TimeoutExpired: بهير.kill(); بهير.wait()
            준비살피미.close(); بهير.stdin.close(); بهير.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(باورکړن_راپور,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ځغلول()
