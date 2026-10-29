#!/usr/bin/env python3
"""자체 커널의 ሼል, 프로세스 ግቤት_ውጤት, Unicode GUI 터미널을 ትክክለኛ_ውሂብ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ፈጽም_ትእዛዝ import አሳይ_ስር, ትእዛዝ


def ማስኬጃ():
    출력결과 = አሳይ_ስር / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ማረጋገጥ_ዘገባ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((አሳይ_ስር / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        ሂደቶች = subprocess.Popen(ትእዛዝ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(ሂደቶች.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ውሂብ=bytearray(); ጨርስ_ዝንፍ=time.monotonic()+시간제한
            while 확인표시 not in ውሂብ:
                if time.monotonic()>ጨርስ_ዝንፍ or ሂደቶች.poll() is not None: raise AssertionError('UART timeout/exit: '+ውሂብ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ውሂብ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ውሂብ or b'FAIL ' in ውሂብ: raise AssertionError(ውሂብ)
            return ውሂብ.decode('utf-8','replace').replace('\r\n','\n')
        def ላክ(ውሂብ, 확인표시=b'jkoros-native> '):
            ሂደቶች.stdin.write(ውሂብ); ሂደቶች.stdin.flush(); return 수신하기(확인표시)
        def ሼል(መስመር, *예상결과):
            ልኬት=ላክ(መስመር.encode()+b'\n')
            for እሴት in 예상결과: assert እሴት in ልኬት, (መስመር,እሴት,ልኬት)
            return ልኬት
        def ፋይል(ስም):
            ጽሁፍ=ሼል('hex '+ስም,'HEX BEGIN','HEX END'); ፈልግ_ልኬት=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ጽሁፍ,re.S)
            ውሂብ=bytes.fromhex(''.join(ፈልግ_ልኬት.group(2).split())); assert len(ውሂብ)==int(ፈልግ_ልኬት.group(1)); return ውሂብ
        try:
            수신하기(b'jkoros-native> ')
            ሼል('mkdir 작업; cd 작업; pwd','/작업')
            ሼል('mkdir 하위; echo "한글 ውሂብ 😀" > 인사.txt')
            assert ፋይል('인사.txt')=='한글 ውሂብ 😀\n'.encode()
            ሼል('cp 인사.txt ቅዳ_እሴት.txt; mv ቅዳ_እሴት.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ውሂብ 😀')
            ሼል('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ውሂብ 😀','/작업/하위')
            ሼል('cd ..; rmdir 하위; echo $?','1\n')
            ሼል('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ሼል('cp 인사.txt 인사.txt; echo $?','1\n'); assert ፋይል('인사.txt')=='한글 ውሂብ 😀\n'.encode()
            ሼል('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ፋይል('인사.txt')
            ሼል("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ፋይል('리터럴')=='$인사\n누리\n'.encode()
            ሼል('echo one > መግለጫ_እሴት; echo two >> መግለጫ_እሴት; echo three >> መግለጫ_እሴት')
            ሼል('cat < መግለጫ_እሴት | grep t | tee 추림 | wc -l','2\n'); assert ፋይል('추림')==b'two\nthree\n'
            ሼል('head -n 1 መግለጫ_እሴት > ፊት_እሴት; tail -n 1 መግለጫ_እሴት > ተመለስ_እሴት'); assert ፋይል('앞')==b'one\n'; assert ፋይል('뒤')==b'three\n'
            ሼል('grep absent መግለጫ_እሴት; echo $?','1\n')
            ሼል('echo untouched > ጠብቅ_እሴት')
            ሼል('echo destroyed > ጠብቅ_እሴት |','명령이 빠졌습니다'); assert ፋይል('ጠብቅ_እሴት')==b'untouched\n'
            ሼል('echo "oops','따옴표가 닫히지 않았습니다')
            ሼል('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ሼል('echo bad 2> ጠብቅ_እሴት','번호를 지정한 ፋይል 서술자 ግቤት_ውጤት ቀይር_ሁነታ'); assert ፋይል('ጠብቅ_እሴት')==b'untouched\n'
            ሼል('rm 빈파일 리터럴 መግለጫ_እሴት 추림 ፊት_እሴት ተመለስ_እሴት ጠብቅ_እሴት')
            ማረጋገጥ_ዘገባ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ሼል("python -c 'print(123)' | wc -c",'4\n')
            ሼል("python -c 'print(456)' > ፕሮግራም_f5044b9b.txt"); assert ፋይል('ፕሮግራም_f5044b9b.txt')==b'456\n'
            ሼል("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ሼል("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ፕሮግራም_f5044b9b.txt", "b'456\\n'", "b''")
            ሼል("python -c 'print(\"x\"*17000)' | wc -c", 'ስህተት -28')
            ሼል('echo recovered | wc -c','10\n')
            ሼል("python -c 'import jkoros; print(jkoros.read("+'"/작업/ፕሮግራም_f5044b9b.txt"'+"))'",'456','exit 0')
            ሼል('cd /; javac Hello.java','Compiled:','exit 0')
            ሼል('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ፋይል('/작업/자바.txt')
            ሼል('cd 작업; echo "echo script > 실행결과" > ትእዛዝ.sh; echo "false || echo recovered >> 실행결과" >> ትእዛዝ.sh; sh ትእዛዝ.sh')
            assert ፋይል('실행결과')==b'script\nrecovered\n'
            ሼል('rm 실행결과; echo "exit 7" > ውጣ_ፕሮግራም.sh; sh ውጣ_ፕሮግራም.sh; echo $?','7\n')
            ሼል('rm ውጣ_ፕሮግራም.sh ትእዛዝ.sh ፕሮግራም_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ማረጋገጥ_ዘገባ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ሼል('echo history-proof','history-proof')
            ልኬት=ላክ(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ልኬት.count('history-proof')>=2, ልኬት
            ላክ(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ልኬት=ላክ(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ልኬት, ልኬት
            ልኬት=ላክ(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ልኬት,ልኬት
            ልኬት=ላክ('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ልኬት,ልኬት
            긴글='한글'*50
            ልኬት=ላክ(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ልኬት
            ሼል('terminal','TERMINAL READY')
            ሼል('clear')
            ሼል('echo "한글 ተርሚናል ABC xyz 012 😀"','한글 ተርሚናል ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ተገልጋይ:
                ተገልጋይ.settimeout(10); ተገልጋይ.connect(str(모의제어접속))
                with ተገልጋይ.makefile('rwb') as ልቀቅ_እሴት:
                    json.loads(ልቀቅ_እሴት.readline())
                    def 호출(ስም,ነጋሪ_እሴት_ድርድር=None):
                        መረብ_ኢሜይል={'execute':ስም}
                        if ነጋሪ_እሴት_ድርድር: መረብ_ኢሜይል['arguments']=ነጋሪ_እሴት_ድርድር
                        ልቀቅ_እሴት.write((json.dumps(መረብ_ኢሜይል)+'\n').encode()); ልቀቅ_እሴት.flush()
                        while True:
                            መልስ=json.loads(ልቀቅ_እሴት.readline())
                            if 'error' in መልስ: raise AssertionError(መልስ)
                            if 'return' in መልስ: return መልስ['return']
                    호출('qmp_capabilities')
                    ምስል=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ምስል),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ውሂብ=ምስል.read_bytes().split(b'\n',3)[3]
                    def ፒክስል(ኤክስ_አስተባባሪ,세로좌표): return tuple(ውሂብ[(세로좌표*640+ኤክስ_አስተባባሪ)*3:(세로좌표*640+ኤክስ_አስተባባሪ)*3+3])
                    assert ፒክስል(12,48)==(32,80,144),ፒክስል(12,48)
                    assert len(set(ፒክስል(ኤክስ_አስተባባሪ,세로좌표) for 세로좌표 in range(100,116) for ኤክስ_አስተባባሪ in range(24,56)))>1,'Hangul glyphs missing'
                    ሼል('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ሼል("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ምስል),'format':'ppm'})
                    복원자료=ምስል.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ሼል('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ሼል('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ላክ(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ልኬት=ላክ(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ልኬት,ልኬት
                    ሼል('rm visible.txt')
                    호출('quit')
            ሂደቶች.wait(timeout=5)
            ማረጋገጥ_ዘገባ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ማረጋገጥ_ዘገባ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if ሂደቶች.poll() is None:
                ሂደቶች.terminate()
                try: ሂደቶች.wait(timeout=5)
                except subprocess.TimeoutExpired: ሂደቶች.kill(); ሂደቶች.wait()
            준비살피미.close(); ሂደቶች.stdin.close(); ሂደቶች.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ማስኬጃ()
