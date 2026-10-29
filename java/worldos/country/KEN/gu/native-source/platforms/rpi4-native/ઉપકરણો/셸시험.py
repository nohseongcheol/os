#!/usr/bin/env python3
"""자체 커널의 શેલ, 프로세스 ઇનપુટ_આઉટપુટ, Unicode GUI 터미널을 વાસ્તવિક_ડેટા raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ, આદેશ


def ચલાવો_2():
    출력결과 = પ્રોજેક્ટ_રૂટ / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    માન્યતા_અહેવાલ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        પ્રક્રિયા = subprocess.Popen(આદેશ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(પ્રક્રિયા.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ડેટા=bytearray(); અંત_કરો_ઑફસેટ=time.monotonic()+시간제한
            while 확인표시 not in ડેટા:
                if time.monotonic()>અંત_કરો_ઑફસેટ or પ્રક્રિયા.poll() is not None: raise AssertionError('UART timeout/exit: '+ડેટા.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ડેટા.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ડેટા or b'FAIL ' in ડેટા: raise AssertionError(ડેટા)
            return ડેટા.decode('utf-8','replace').replace('\r\n','\n')
        def મોકલો(ડેટા, 확인표시=b'jkoros-native> '):
            પ્રક્રિયા.stdin.write(ડેટા); પ્રક્રિયા.stdin.flush(); return 수신하기(확인표시)
        def શેલ(લાઇન, *예상결과):
            પરિમાણ=મોકલો(લાઇન.encode()+b'\n')
            for મૂલ્ય in 예상결과: assert મૂલ્ય in પરિમાણ, (લાઇન,મૂલ્ય,પરિમાણ)
            return પરિમાણ
        def ફાઈલ(નામ):
            લખાણ=શેલ('hex '+નામ,'HEX BEGIN','HEX END'); શોધ_પરિમાણ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',લખાણ,re.S)
            ડેટા=bytes.fromhex(''.join(શોધ_પરિમાણ.group(2).split())); assert len(ડેટા)==int(શોધ_પરિમાણ.group(1)); return ડેટા
        try:
            수신하기(b'jkoros-native> ')
            શેલ('mkdir 작업; cd 작업; pwd','/작업')
            શેલ('mkdir 하위; echo "한글 ડેટા 😀" > 인사.txt')
            assert ફાઈલ('인사.txt')=='한글 ડેટા 😀\n'.encode()
            શેલ('cp 인사.txt ઉદાહરણ_મૂલ્ય.txt; mv ઉદાહરણ_મૂલ્ય.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ડેટા 😀')
            શેલ('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ડેટા 😀','/작업/하위')
            શેલ('cd ..; rmdir 하위; echo $?','1\n')
            શેલ('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            શેલ('cp 인사.txt 인사.txt; echo $?','1\n'); assert ફાઈલ('인사.txt')=='한글 ડેટા 😀\n'.encode()
            શેલ('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ફાઈલ('인사.txt')
            શેલ("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ફાઈલ('리터럴')=='$인사\n누리\n'.encode()
            શેલ('echo one > વિધાન_મૂલ્ય; echo two >> વિધાન_મૂલ્ય; echo three >> વિધાન_મૂલ્ય')
            શેલ('cat < વિધાન_મૂલ્ય | grep t | tee 추림 | wc -l','2\n'); assert ફાઈલ('추림')==b'two\nthree\n'
            શેલ('head -n 1 વિધાન_મૂલ્ય > 앞; tail -n 1 વિધાન_મૂલ્ય > બેક_મૂલ્ય'); assert ફાઈલ('앞')==b'one\n'; assert ફાઈલ('뒤')==b'three\n'
            શેલ('grep absent વિધાન_મૂલ્ય; echo $?','1\n')
            શેલ('echo untouched > રક્ષણ_કરો_મૂલ્ય')
            શેલ('echo destroyed > રક્ષણ_કરો_મૂલ્ય |','명령이 빠졌습니다'); assert ફાઈલ('રક્ષણ_કરો_મૂલ્ય')==b'untouched\n'
            શેલ('echo "oops','따옴표가 닫히지 않았습니다')
            શેલ('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            શેલ('echo bad 2> રક્ષણ_કરો_મૂલ્ય','번호를 지정한 ફાઈલ 서술자 ઇનપુટ_આઉટપુટ સ્વિચ_મોડ'); assert ફાઈલ('રક્ષણ_કરો_મૂલ્ય')==b'untouched\n'
            શેલ('rm 빈파일 리터럴 વિધાન_મૂલ્ય 추림 앞 બેક_મૂલ્ય રક્ષણ_કરો_મૂલ્ય')
            માન્યતા_અહેવાલ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            શેલ("python -c 'print(123)' | wc -c",'4\n')
            શેલ("python -c 'print(456)' > એપ્લિકેશન_f5044b9b.txt"); assert ફાઈલ('એપ્લિકેશન_f5044b9b.txt')==b'456\n'
            શેલ("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            શેલ("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < એપ્લિકેશન_f5044b9b.txt", "b'456\\n'", "b''")
            શેલ("python -c 'print(\"x\"*17000)' | wc -c", 'ભૂલ -28')
            શેલ('echo recovered | wc -c','10\n')
            શેલ("python -c 'import jkoros; print(jkoros.read("+'"/작업/એપ્લિકેશન_f5044b9b.txt"'+"))'",'456','exit 0')
            શેલ('cd /; javac Hello.java','Compiled:','exit 0')
            શેલ('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ફાઈલ('/작업/자바.txt')
            શેલ('cd 작업; echo "echo script > 실행결과" > આદેશ.sh; echo "false || echo recovered >> 실행결과" >> આદેશ.sh; sh આદેશ.sh')
            assert ફાઈલ('실행결과')==b'script\nrecovered\n'
            શેલ('rm 실행결과; echo "exit 7" > પ્રસ્થાન_એપ્લિકેશન.sh; sh પ્રસ્થાન_એપ્લિકેશન.sh; echo $?','7\n')
            શેલ('rm પ્રસ્થાન_એપ્લિકેશન.sh આદેશ.sh એપ્લિકેશન_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            માન્યતા_અહેવાલ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            શેલ('echo history-proof','history-proof')
            પરિમાણ=મોકલો(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert પરિમાણ.count('history-proof')>=2, પરિમાણ
            મોકલો(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            પરિમાણ=મોકલો(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in પરિમાણ, પરિમાણ
            પરિમાણ=મોકલો(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in પરિમાણ,પરિમાણ
            પરિમાણ=મોકલો('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in પરિમાણ,પરિમાણ
            긴글='한글'*50
            પરિમાણ=મોકલો(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in પરિમાણ
            શેલ('terminal','TERMINAL READY')
            શેલ('clear')
            શેલ('echo "한글 ટર્મિનલ ABC xyz 012 😀"','한글 ટર્મિનલ ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ક્લાયંટ:
                ક્લાયંટ.settimeout(10); ક્લાયંટ.connect(str(모의제어접속))
                with ક્લાયંટ.makefile('rwb') as સ્ટ્રીમ_મૂલ્ય:
                    json.loads(સ્ટ્રીમ_મૂલ્ય.readline())
                    def 호출(નામ,દલીલ_અરે=None):
                        નેટવર્ક_સંદેશ={'execute':નામ}
                        if દલીલ_અરે: નેટવર્ક_સંદેશ['arguments']=દલીલ_અરે
                        સ્ટ્રીમ_મૂલ્ય.write((json.dumps(નેટવર્ક_સંદેશ)+'\n').encode()); સ્ટ્રીમ_મૂલ્ય.flush()
                        while True:
                            જવાબ=json.loads(સ્ટ્રીમ_મૂલ્ય.readline())
                            if 'error' in જવાબ: raise AssertionError(જવાબ)
                            if 'return' in જવાબ: return જવાબ['return']
                    호출('qmp_capabilities')
                    છબી=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(છબી),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ડેટા=છબી.read_bytes().split(b'\n',3)[3]
                    def પેલ(x_યામ,세로좌표): return tuple(ડેટા[(세로좌표*640+x_યામ)*3:(세로좌표*640+x_યામ)*3+3])
                    assert પેલ(12,48)==(32,80,144),પેલ(12,48)
                    assert len(set(પેલ(x_યામ,세로좌표) for 세로좌표 in range(100,116) for x_યામ in range(24,56)))>1,'Hangul glyphs missing'
                    શેલ('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    શેલ("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(છબી),'format':'ppm'})
                    복원자료=છબી.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    શેલ('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): શેલ('echo scroll-'+str(순번),'scroll-'+str(순번))
                    મોકલો(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    પરિમાણ=મોકલો(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in પરિમાણ,પરિમાણ
                    શેલ('rm visible.txt')
                    호출('quit')
            પ્રક્રિયા.wait(timeout=5)
            માન્યતા_અહેવાલ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            માન્યતા_અહેવાલ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if પ્રક્રિયા.poll() is None:
                પ્રક્રિયા.terminate()
                try: પ્રક્રિયા.wait(timeout=5)
                except subprocess.TimeoutExpired: પ્રક્રિયા.kill(); પ્રક્રિયા.wait()
            준비살피미.close(); પ્રક્રિયા.stdin.close(); પ્રક્રિયા.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ચલાવો_2()
