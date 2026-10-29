#!/usr/bin/env python3
"""자체 커널의 ሽፋን, 프로세스 입출력, Unicode GUI 터미널을 ትኽክለኛ_ሓበሬታ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ተግብር_ትእዛዝ import 기준, ትእዛዝ


def ኣኺድ():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ምርግጋፅ_ጸብጻብ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        መስርሕ = subprocess.Popen(ትእዛዝ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(መስርሕ.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ሓበሬታ=bytearray(); ኣቑም_ሽፋን=time.monotonic()+시간제한
            while 확인표시 not in ሓበሬታ:
                if time.monotonic()>ኣቑም_ሽፋን or መስርሕ.poll() is not None: raise AssertionError('UART timeout/exit: '+ሓበሬታ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ሓበሬታ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ሓበሬታ or b'FAIL ' in ሓበሬታ: raise AssertionError(ሓበሬታ)
            return ሓበሬታ.decode('utf-8','replace').replace('\r\n','\n')
        def ለኣኽ(ሓበሬታ, 확인표시=b'jkoros-native> '):
            መስርሕ.stdin.write(ሓበሬታ); መስርሕ.stdin.flush(); return 수신하기(확인표시)
        def ሽፋን(መስመር, *예상결과):
            결과=ለኣኽ(መስመር.encode()+b'\n')
            for ዋጋ in 예상결과: assert ዋጋ in 결과, (መስመር,ዋጋ,결과)
            return 결과
        def ፋይል(ሽም):
            ጽሑፍ=ሽፋን('hex '+ሽም,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ጽሑፍ,re.S)
            ሓበሬታ=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(ሓበሬታ)==int(찾은결과.group(1)); return ሓበሬታ
        try:
            수신하기(b'jkoros-native> ')
            ሽፋን('mkdir 작업; cd 작업; pwd','/작업')
            ሽፋን('mkdir 하위; echo "한글 ሓበሬታ 😀" > 인사.txt')
            assert ፋይል('인사.txt')=='한글 ሓበሬታ 😀\n'.encode()
            ሽፋን('cp 인사.txt ቅዳሕ_ዋጋ.txt; mv ቅዳሕ_ዋጋ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ሓበሬታ 😀')
            ሽፋን('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ሓበሬታ 😀','/작업/하위')
            ሽፋን('cd ..; rmdir 하위; echo $?','1\n')
            ሽፋን('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ሽፋን('cp 인사.txt 인사.txt; echo $?','1\n'); assert ፋይል('인사.txt')=='한글 ሓበሬታ 😀\n'.encode()
            ሽፋን('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ፋይል('인사.txt')
            ሽፋን("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ፋይል('리터럴')=='$인사\n누리\n'.encode()
            ሽፋን('echo one > መግለጺ_ዋጋ_22f14643; echo two >> መግለጺ_ዋጋ_22f14643; echo three >> መግለጺ_ዋጋ_22f14643')
            ሽፋን('cat < መግለጺ_ዋጋ_22f14643 | grep t | tee 추림 | wc -l','2\n'); assert ፋይል('추림')==b'two\nthree\n'
            ሽፋን('head -n 1 መግለጺ_ዋጋ_22f14643 > 앞; tail -n 1 መግለጺ_ዋጋ_22f14643 > ድሕሪት_ዋጋ'); assert ፋይል('앞')==b'one\n'; assert ፋይል('뒤')==b'three\n'
            ሽፋን('grep absent መግለጺ_ዋጋ_22f14643; echo $?','1\n')
            ሽፋን('echo untouched > ሓልው_ዋጋ')
            ሽፋን('echo destroyed > ሓልው_ዋጋ |','명령이 빠졌습니다'); assert ፋይል('ሓልው_ዋጋ')==b'untouched\n'
            ሽፋን('echo "oops','따옴표가 닫히지 않았습니다')
            ሽፋን('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ሽፋን('echo bad 2> ሓልው_ዋጋ','번호를 지정한 ፋይል 서술자 입출력 ቀይር_ኹነት'); assert ፋይል('ሓልው_ዋጋ')==b'untouched\n'
            ሽፋን('rm 빈파일 리터럴 መግለጺ_ዋጋ_22f14643 추림 앞 ድሕሪት_ዋጋ ሓልው_ዋጋ')
            ምርግጋፅ_ጸብጻብ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ሽፋን("python -c 'print(123)' | wc -c",'4\n')
            ሽፋን("python -c 'print(456)' > መተግበሪ_f5044b9b.txt"); assert ፋይል('መተግበሪ_f5044b9b.txt')==b'456\n'
            ሽፋን("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ሽፋን("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < መተግበሪ_f5044b9b.txt", "b'456\\n'", "b''")
            ሽፋን("python -c 'print(\"x\"*17000)' | wc -c", 'ጌጋ -28')
            ሽፋን('echo recovered | wc -c','10\n')
            ሽፋን("python -c 'import jkoros; print(jkoros.read("+'"/작업/መተግበሪ_f5044b9b.txt"'+"))'",'456','exit 0')
            ሽፋን('cd /; javac Hello.java','Compiled:','exit 0')
            ሽፋን('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ፋይል('/작업/자바.txt')
            ሽፋን('cd 작업; echo "echo script > 실행결과" > ትእዛዝ.sh; echo "false || echo recovered >> 실행결과" >> ትእዛዝ.sh; sh ትእዛዝ.sh')
            assert ፋይል('실행결과')==b'script\nrecovered\n'
            ሽፋን('rm 실행결과; echo "exit 7" > ውጻእ_መተግበሪ.sh; sh ውጻእ_መተግበሪ.sh; echo $?','7\n')
            ሽፋን('rm ውጻእ_መተግበሪ.sh ትእዛዝ.sh መተግበሪ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ምርግጋፅ_ጸብጻብ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ሽፋን('echo history-proof','history-proof')
            결과=ለኣኽ(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            ለኣኽ(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=ለኣኽ(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=ለኣኽ(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=ለኣኽ('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=ለኣኽ(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            ሽፋን('terminal','TERMINAL READY')
            ሽፋን('clear')
            ሽፋን('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ዓሚል:
                ዓሚል.settimeout(10); ዓሚል.connect(str(모의제어접속))
                with ዓሚል.makefile('rwb') as ወሓዚ_ዋጋ:
                    json.loads(ወሓዚ_ዋጋ.readline())
                    def 호출(ሽም,ሓባሪ_ቁጽሪ_ተርታ=None):
                        ማሕበራዊ_ኔትወርክ_መልእኽቲ={'execute':ሽም}
                        if ሓባሪ_ቁጽሪ_ተርታ: ማሕበራዊ_ኔትወርክ_መልእኽቲ['arguments']=ሓባሪ_ቁጽሪ_ተርታ
                        ወሓዚ_ዋጋ.write((json.dumps(ማሕበራዊ_ኔትወርክ_መልእኽቲ)+'\n').encode()); ወሓዚ_ዋጋ.flush()
                        while True:
                            መልስ=json.loads(ወሓዚ_ዋጋ.readline())
                            if 'error' in መልስ: raise AssertionError(መልስ)
                            if 'return' in መልስ: return መልስ['return']
                    호출('qmp_capabilities')
                    ምስሊ=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ምስሊ),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ሓበሬታ=ምስሊ.read_bytes().split(b'\n',3)[3]
                    def ንጣብ(가로좌표,세로좌표): return tuple(ሓበሬታ[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert ንጣብ(12,48)==(32,80,144),ንጣብ(12,48)
                    assert len(set(ንጣብ(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    ሽፋን('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ሽፋን("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ምስሊ),'format':'ppm'})
                    복원자료=ምስሊ.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ሽፋን('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ሽፋን('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ለኣኽ(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=ለኣኽ(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    ሽፋን('rm visible.txt')
                    호출('quit')
            መስርሕ.wait(timeout=5)
            ምርግጋፅ_ጸብጻብ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ምርግጋፅ_ጸብጻብ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if መስርሕ.poll() is None:
                መስርሕ.terminate()
                try: መስርሕ.wait(timeout=5)
                except subprocess.TimeoutExpired: መስርሕ.kill(); መስርሕ.wait()
            준비살피미.close(); መስርሕ.stdin.close(); መስርሕ.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ምርግጋፅ_ጸብጻብ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ኣኺድ()
