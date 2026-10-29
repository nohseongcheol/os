#!/usr/bin/env python3
"""자체 커널의 ଖୋଳ, 프로세스 ଇନପୁଟ୍_ଆଉଟପୁଟ୍, Unicode GUI 터미널을 ପ୍ରକୃତ_ଡାଟା raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, ନିର୍ଦ୍ଦେଶ


def ଚଳାନ୍ତୁ():
    출력결과 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ବୈଧକରଣ_ରିପୋର୍ଟ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        ପ୍ରକ୍ରିୟା = subprocess.Popen(ନିର୍ଦ୍ଦେଶ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(ପ୍ରକ୍ରିୟା.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ଡାଟା=bytearray(); ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+시간제한
            while 확인표시 not in ଡାଟା:
                if time.monotonic()>ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍ or ପ୍ରକ୍ରିୟା.poll() is not None: raise AssertionError('UART timeout/exit: '+ଡାଟା.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ଡାଟା.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ଡାଟା or b'FAIL ' in ଡାଟା: raise AssertionError(ଡାଟା)
            return ଡାଟା.decode('utf-8','replace').replace('\r\n','\n')
        def ପଠାନ୍ତୁ(ଡାଟା, 확인표시=b'jkoros-native> '):
            ପ୍ରକ୍ରିୟା.stdin.write(ଡାଟା); ପ୍ରକ୍ରିୟା.stdin.flush(); return 수신하기(확인표시)
        def ଖୋଳ(ରେଖା, *예상결과):
            ମାପ=ପଠାନ୍ତୁ(ରେଖା.encode()+b'\n')
            for ମୂଲ୍ୟ in 예상결과: assert ମୂଲ୍ୟ in ମାପ, (ରେଖା,ମୂଲ୍ୟ,ମାପ)
            return ମାପ
        def ଫାଇଲ(ନାମ):
            ପାଠ୍ଯ=ଖୋଳ('hex '+ନାମ,'HEX BEGIN','HEX END'); ସନ୍ଧାନ_ମାପ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ପାଠ୍ଯ,re.S)
            ଡାଟା=bytes.fromhex(''.join(ସନ୍ଧାନ_ମାପ.group(2).split())); assert len(ଡାଟା)==int(ସନ୍ଧାନ_ମାପ.group(1)); return ଡାଟା
        try:
            수신하기(b'jkoros-native> ')
            ଖୋଳ('mkdir 작업; cd 작업; pwd','/작업')
            ଖୋଳ('mkdir 하위; echo "한글 ଡାଟା 😀" > 인사.txt')
            assert ଫାଇଲ('인사.txt')=='한글 ଡାଟା 😀\n'.encode()
            ଖୋଳ('cp 인사.txt କପି_ମୂଲ୍ୟ.txt; mv କପି_ମୂଲ୍ୟ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ଡାଟା 😀')
            ଖୋଳ('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ଡାଟା 😀','/작업/하위')
            ଖୋଳ('cd ..; rmdir 하위; echo $?','1\n')
            ଖୋଳ('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ଖୋଳ('cp 인사.txt 인사.txt; echo $?','1\n'); assert ଫାଇଲ('인사.txt')=='한글 ଡାଟା 😀\n'.encode()
            ଖୋଳ('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ଫାଇଲ('인사.txt')
            ଖୋଳ("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ଫାଇଲ('리터럴')=='$인사\n누리\n'.encode()
            ଖୋଳ('echo one > ବିବୃତି_ମୂଲ୍ୟ; echo two >> ବିବୃତି_ମୂଲ୍ୟ; echo three >> ବିବୃତି_ମୂଲ୍ୟ')
            ଖୋଳ('cat < ବିବୃତି_ମୂଲ୍ୟ | grep t | tee 추림 | wc -l','2\n'); assert ଫାଇଲ('추림')==b'two\nthree\n'
            ଖୋଳ('head -n 1 ବିବୃତି_ମୂଲ୍ୟ > 앞; tail -n 1 ବିବୃତି_ମୂଲ୍ୟ > ପଛ_ମୂଲ୍ୟ'); assert ଫାଇଲ('앞')==b'one\n'; assert ଫାଇଲ('뒤')==b'three\n'
            ଖୋଳ('grep absent ବିବୃତି_ମୂଲ୍ୟ; echo $?','1\n')
            ଖୋଳ('echo untouched > ପ୍ରତିରୋଧ_ମୂଲ୍ୟ')
            ଖୋଳ('echo destroyed > ପ୍ରତିରୋଧ_ମୂଲ୍ୟ |','명령이 빠졌습니다'); assert ଫାଇଲ('ପ୍ରତିରୋଧ_ମୂଲ୍ୟ')==b'untouched\n'
            ଖୋଳ('echo "oops','따옴표가 닫히지 않았습니다')
            ଖୋଳ('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ଖୋଳ('echo bad 2> ପ୍ରତିରୋଧ_ମୂଲ୍ୟ','번호를 지정한 ଫାଇଲ 서술자 ଇନପୁଟ୍_ଆଉଟପୁଟ୍ ସୁଇଚ୍_ମୋଡ୍'); assert ଫାଇଲ('ପ୍ରତିରୋଧ_ମୂଲ୍ୟ')==b'untouched\n'
            ଖୋଳ('rm 빈파일 리터럴 ବିବୃତି_ମୂଲ୍ୟ 추림 앞 ପଛ_ମୂଲ୍ୟ ପ୍ରତିରୋଧ_ମୂଲ୍ୟ')
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ଖୋଳ("python -c 'print(123)' | wc -c",'4\n')
            ଖୋଳ("python -c 'print(456)' > ଅନୁପ୍ରୟୋଗ_f5044b9b.txt"); assert ଫାଇଲ('ଅନୁପ୍ରୟୋଗ_f5044b9b.txt')==b'456\n'
            ଖୋଳ("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ଖୋଳ("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ଅନୁପ୍ରୟୋଗ_f5044b9b.txt", "b'456\\n'", "b''")
            ଖୋଳ("python -c 'print(\"x\"*17000)' | wc -c", 'ତ୍ରୁଟି -28')
            ଖୋଳ('echo recovered | wc -c','10\n')
            ଖୋଳ("python -c 'import jkoros; print(jkoros.read("+'"/작업/ଅନୁପ୍ରୟୋଗ_f5044b9b.txt"'+"))'",'456','exit 0')
            ଖୋଳ('cd /; javac Hello.java','Compiled:','exit 0')
            ଖୋଳ('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ଫାଇଲ('/작업/자바.txt')
            ଖୋଳ('cd 작업; echo "echo script > 실행결과" > ନିର୍ଦ୍ଦେଶ.sh; echo "false || echo recovered >> 실행결과" >> ନିର୍ଦ୍ଦେଶ.sh; sh ନିର୍ଦ୍ଦେଶ.sh')
            assert ଫାଇଲ('실행결과')==b'script\nrecovered\n'
            ଖୋଳ('rm 실행결과; echo "exit 7" > ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ.sh; sh ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ.sh; echo $?','7\n')
            ଖୋଳ('rm ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ.sh ନିର୍ଦ୍ଦେଶ.sh ଅନୁପ୍ରୟୋଗ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ଖୋଳ('echo history-proof','history-proof')
            ମାପ=ପଠାନ୍ତୁ(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ମାପ.count('history-proof')>=2, ମାପ
            ପଠାନ୍ତୁ(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ମାପ=ପଠାନ୍ତୁ(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ମାପ, ମାପ
            ମାପ=ପଠାନ୍ତୁ(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ମାପ,ମାପ
            ମାପ=ପଠାନ୍ତୁ('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ମାପ,ମାପ
            긴글='한글'*50
            ମାପ=ପଠାନ୍ତୁ(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ମାପ
            ଖୋଳ('terminal','TERMINAL READY')
            ଖୋଳ('clear')
            ଖୋଳ('echo "한글 ଟର୍ମିନାଲ ABC xyz 012 😀"','한글 ଟର୍ମିନାଲ ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as କ୍ଲାଏଣ୍ଟ:
                କ୍ଲାଏଣ୍ଟ.settimeout(10); କ୍ଲାଏଣ୍ଟ.connect(str(모의제어접속))
                with କ୍ଲାଏଣ୍ଟ.makefile('rwb') as ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ:
                    json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline())
                    def 호출(ନାମ,ଯୁକ୍ତି_ଆରେ=None):
                        ନେଟ୍_ୱାର୍କ୍_ବାର୍ତ୍ତା={'execute':ନାମ}
                        if ଯୁକ୍ତି_ଆରେ: ନେଟ୍_ୱାର୍କ୍_ବାର୍ତ୍ତା['arguments']=ଯୁକ୍ତି_ଆରେ
                        ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.write((json.dumps(ନେଟ୍_ୱାର୍କ୍_ବାର୍ତ୍ତା)+'\n').encode()); ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.flush()
                        while True:
                            ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ=json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline())
                            if 'error' in ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ: raise AssertionError(ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ)
                            if 'return' in ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ: return ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ['return']
                    호출('qmp_capabilities')
                    ଚିତ୍ର=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ଚିତ୍ର),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ଡାଟା=ଚିତ୍ର.read_bytes().split(b'\n',3)[3]
                    def ପିକ୍ସେଲ୍(x_ସଂଯୋଜନ,세로좌표): return tuple(ଡାଟା[(세로좌표*640+x_ସଂଯୋଜନ)*3:(세로좌표*640+x_ସଂଯୋଜନ)*3+3])
                    assert ପିକ୍ସେଲ୍(12,48)==(32,80,144),ପିକ୍ସେଲ୍(12,48)
                    assert len(set(ପିକ୍ସେଲ୍(x_ସଂଯୋଜନ,세로좌표) for 세로좌표 in range(100,116) for x_ସଂଯୋଜନ in range(24,56)))>1,'Hangul glyphs missing'
                    ଖୋଳ('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ଖୋଳ("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ଚିତ୍ର),'format':'ppm'})
                    복원자료=ଚିତ୍ର.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ଖୋଳ('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ଖୋଳ('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ପଠାନ୍ତୁ(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ମାପ=ପଠାନ୍ତୁ(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ମାପ,ମାପ
                    ଖୋଳ('rm visible.txt')
                    호출('quit')
            ପ୍ରକ୍ରିୟା.wait(timeout=5)
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ବୈଧକରଣ_ରିପୋର୍ଟ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if ପ୍ରକ୍ରିୟା.poll() is None:
                ପ୍ରକ୍ରିୟା.terminate()
                try: ପ୍ରକ୍ରିୟା.wait(timeout=5)
                except subprocess.TimeoutExpired: ପ୍ରକ୍ରିୟା.kill(); ପ୍ରକ୍ରିୟା.wait()
            준비살피미.close(); ପ୍ରକ୍ରିୟା.stdin.close(); ପ୍ରକ୍ରିୟା.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ଚଳାନ୍ତୁ()
