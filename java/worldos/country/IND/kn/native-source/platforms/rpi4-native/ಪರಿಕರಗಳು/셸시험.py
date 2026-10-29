#!/usr/bin/env python3
"""자체 커널의 ಶೆಲ್, 프로세스 ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್, Unicode GUI 터미널을 ನಿಜವಾದ_ಡೇಟಾ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ, ಆಜ್ಞೆ


def ಚಲಾಯಿಸು_2():
    출력결과 = ಬಿಂಬಿಸು_ಮೂಲ / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ದೃಢೀಕರಣ_ವರದಿ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        ಪ್ರಕ್ರಿಯೆ = subprocess.Popen(ಆಜ್ಞೆ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(ಪ್ರಕ್ರಿಯೆ.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ಡೇಟಾ=bytearray(); ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+시간제한
            while 확인표시 not in ಡೇಟಾ:
                if time.monotonic()>ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್ or ಪ್ರಕ್ರಿಯೆ.poll() is not None: raise AssertionError('UART timeout/exit: '+ಡೇಟಾ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ಡೇಟಾ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ಡೇಟಾ or b'FAIL ' in ಡೇಟಾ: raise AssertionError(ಡೇಟಾ)
            return ಡೇಟಾ.decode('utf-8','replace').replace('\r\n','\n')
        def ಕಳುಹಿಸಿ(ಡೇಟಾ, 확인표시=b'jkoros-native> '):
            ಪ್ರಕ್ರಿಯೆ.stdin.write(ಡೇಟಾ); ಪ್ರಕ್ರಿಯೆ.stdin.flush(); return 수신하기(확인표시)
        def ಶೆಲ್(ಸಾಲು, *예상결과):
            ಮಾಪನ=ಕಳುಹಿಸಿ(ಸಾಲು.encode()+b'\n')
            for ಮೌಲ್ಯ in 예상결과: assert ಮೌಲ್ಯ in ಮಾಪನ, (ಸಾಲು,ಮೌಲ್ಯ,ಮಾಪನ)
            return ಮಾಪನ
        def ಕಡತ(ಹೆಸರು):
            ಪಠ್ಯ=ಶೆಲ್('hex '+ಹೆಸರು,'HEX BEGIN','HEX END'); ಶೋಧ_ಮಾಪನ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ಪಠ್ಯ,re.S)
            ಡೇಟಾ=bytes.fromhex(''.join(ಶೋಧ_ಮಾಪನ.group(2).split())); assert len(ಡೇಟಾ)==int(ಶೋಧ_ಮಾಪನ.group(1)); return ಡೇಟಾ
        try:
            수신하기(b'jkoros-native> ')
            ಶೆಲ್('mkdir 작업; cd 작업; pwd','/작업')
            ಶೆಲ್('mkdir 하위; echo "한글 ಡೇಟಾ 😀" > 인사.txt')
            assert ಕಡತ('인사.txt')=='한글 ಡೇಟಾ 😀\n'.encode()
            ಶೆಲ್('cp 인사.txt ನಕಲಿಸು_ಮೌಲ್ಯ.txt; mv ನಕಲಿಸು_ಮೌಲ್ಯ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ಡೇಟಾ 😀')
            ಶೆಲ್('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ಡೇಟಾ 😀','/작업/하위')
            ಶೆಲ್('cd ..; rmdir 하위; echo $?','1\n')
            ಶೆಲ್('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ಶೆಲ್('cp 인사.txt 인사.txt; echo $?','1\n'); assert ಕಡತ('인사.txt')=='한글 ಡೇಟಾ 😀\n'.encode()
            ಶೆಲ್('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ಕಡತ('인사.txt')
            ಶೆಲ್("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ಕಡತ('리터럴')=='$인사\n누리\n'.encode()
            ಶೆಲ್('echo one > ಹೇಳಿಕೆ_ಮೌಲ್ಯ; echo two >> ಹೇಳಿಕೆ_ಮೌಲ್ಯ; echo three >> ಹೇಳಿಕೆ_ಮೌಲ್ಯ')
            ಶೆಲ್('cat < ಹೇಳಿಕೆ_ಮೌಲ್ಯ | grep t | tee 추림 | wc -l','2\n'); assert ಕಡತ('추림')==b'two\nthree\n'
            ಶೆಲ್('head -n 1 ಹೇಳಿಕೆ_ಮೌಲ್ಯ > ಮುಂದೆ_ಮೌಲ್ಯ; tail -n 1 ಹೇಳಿಕೆ_ಮೌಲ್ಯ > ಹಿಂದೆ_ಮೌಲ್ಯ'); assert ಕಡತ('앞')==b'one\n'; assert ಕಡತ('뒤')==b'three\n'
            ಶೆಲ್('grep absent ಹೇಳಿಕೆ_ಮೌಲ್ಯ; echo $?','1\n')
            ಶೆಲ್('echo untouched > ರಕ್ಷಿಸಿ_ಮೌಲ್ಯ')
            ಶೆಲ್('echo destroyed > ರಕ್ಷಿಸಿ_ಮೌಲ್ಯ |','명령이 빠졌습니다'); assert ಕಡತ('ರಕ್ಷಿಸಿ_ಮೌಲ್ಯ')==b'untouched\n'
            ಶೆಲ್('echo "oops','따옴표가 닫히지 않았습니다')
            ಶೆಲ್('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ಶೆಲ್('echo bad 2> ರಕ್ಷಿಸಿ_ಮೌಲ್ಯ','번호를 지정한 ಕಡತ 서술자 ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್ ಸ್ವಿಚ್_ಮಾಡಿ_ಮೋಡ್'); assert ಕಡತ('ರಕ್ಷಿಸಿ_ಮೌಲ್ಯ')==b'untouched\n'
            ಶೆಲ್('rm 빈파일 리터럴 ಹೇಳಿಕೆ_ಮೌಲ್ಯ 추림 ಮುಂದೆ_ಮೌಲ್ಯ ಹಿಂದೆ_ಮೌಲ್ಯ ರಕ್ಷಿಸಿ_ಮೌಲ್ಯ')
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ಶೆಲ್("python -c 'print(123)' | wc -c",'4\n')
            ಶೆಲ್("python -c 'print(456)' > ಅಪ್ಲಿ_f5044b9b.txt"); assert ಕಡತ('ಅಪ್ಲಿ_f5044b9b.txt')==b'456\n'
            ಶೆಲ್("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ಶೆಲ್("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ಅಪ್ಲಿ_f5044b9b.txt", "b'456\\n'", "b''")
            ಶೆಲ್("python -c 'print(\"x\"*17000)' | wc -c", 'ದೋಷ -28')
            ಶೆಲ್('echo recovered | wc -c','10\n')
            ಶೆಲ್("python -c 'import jkoros; print(jkoros.read("+'"/작업/ಅಪ್ಲಿ_f5044b9b.txt"'+"))'",'456','exit 0')
            ಶೆಲ್('cd /; javac Hello.java','Compiled:','exit 0')
            ಶೆಲ್('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ಕಡತ('/작업/자바.txt')
            ಶೆಲ್('cd 작업; echo "echo script > 실행결과" > ಆಜ್ಞೆ.sh; echo "false || echo recovered >> 실행결과" >> ಆಜ್ಞೆ.sh; sh ಆಜ್ಞೆ.sh')
            assert ಕಡತ('실행결과')==b'script\nrecovered\n'
            ಶೆಲ್('rm 실행결과; echo "exit 7" > ನಿರ್ಗಮನ_ಅಪ್ಲಿ.sh; sh ನಿರ್ಗಮನ_ಅಪ್ಲಿ.sh; echo $?','7\n')
            ಶೆಲ್('rm ನಿರ್ಗಮನ_ಅಪ್ಲಿ.sh ಆಜ್ಞೆ.sh ಅಪ್ಲಿ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ಶೆಲ್('echo history-proof','history-proof')
            ಮಾಪನ=ಕಳುಹಿಸಿ(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ಮಾಪನ.count('history-proof')>=2, ಮಾಪನ
            ಕಳುಹಿಸಿ(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ಮಾಪನ=ಕಳುಹಿಸಿ(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ಮಾಪನ, ಮಾಪನ
            ಮಾಪನ=ಕಳುಹಿಸಿ(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ಮಾಪನ,ಮಾಪನ
            ಮಾಪನ=ಕಳುಹಿಸಿ('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ಮಾಪನ,ಮಾಪನ
            긴글='한글'*50
            ಮಾಪನ=ಕಳುಹಿಸಿ(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ಮಾಪನ
            ಶೆಲ್('terminal','TERMINAL READY')
            ಶೆಲ್('clear')
            ಶೆಲ್('echo "한글 ಟರ್ಮಿನಲ್ ABC xyz 012 😀"','한글 ಟರ್ಮಿನಲ್ ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ಕ್ಲೈಂಟ್:
                ಕ್ಲೈಂಟ್.settimeout(10); ಕ್ಲೈಂಟ್.connect(str(모의제어접속))
                with ಕ್ಲೈಂಟ್.makefile('rwb') as ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ:
                    json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline())
                    def 호출(ಹೆಸರು,ವಾದ_ಅರೇ=None):
                        ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್={'execute':ಹೆಸರು}
                        if ವಾದ_ಅರೇ: ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್['arguments']=ವಾದ_ಅರೇ
                        ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.write((json.dumps(ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್)+'\n').encode()); ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.flush()
                        while True:
                            ಪ್ರತ್ಯುತ್ತರ=json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline())
                            if 'error' in ಪ್ರತ್ಯುತ್ತರ: raise AssertionError(ಪ್ರತ್ಯುತ್ತರ)
                            if 'return' in ಪ್ರತ್ಯುತ್ತರ: return ಪ್ರತ್ಯುತ್ತರ['return']
                    호출('qmp_capabilities')
                    ಇಮೇಜ್=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ಇಮೇಜ್),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ಡೇಟಾ=ಇಮೇಜ್.read_bytes().split(b'\n',3)[3]
                    def ಪೆಲ್(x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ): return tuple(ಡೇಟಾ[(Y_ಬಟನ್_ಸಮನ್ವಯ*640+x_ಸಮಭಾಜಕ)*3:(Y_ಬಟನ್_ಸಮನ್ವಯ*640+x_ಸಮಭಾಜಕ)*3+3])
                    assert ಪೆಲ್(12,48)==(32,80,144),ಪೆಲ್(12,48)
                    assert len(set(ಪೆಲ್(x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ) for Y_ಬಟನ್_ಸಮನ್ವಯ in range(100,116) for x_ಸಮಭಾಜಕ in range(24,56)))>1,'Hangul glyphs missing'
                    ಶೆಲ್('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ಶೆಲ್("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ಇಮೇಜ್),'format':'ppm'})
                    복원자료=ಇಮೇಜ್.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ಶೆಲ್('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ಶೆಲ್('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ಕಳುಹಿಸಿ(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ಮಾಪನ=ಕಳುಹಿಸಿ(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ಮಾಪನ,ಮಾಪನ
                    ಶೆಲ್('rm visible.txt')
                    호출('quit')
            ಪ್ರಕ್ರಿಯೆ.wait(timeout=5)
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ದೃಢೀಕರಣ_ವರದಿ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if ಪ್ರಕ್ರಿಯೆ.poll() is None:
                ಪ್ರಕ್ರಿಯೆ.terminate()
                try: ಪ್ರಕ್ರಿಯೆ.wait(timeout=5)
                except subprocess.TimeoutExpired: ಪ್ರಕ್ರಿಯೆ.kill(); ಪ್ರಕ್ರಿಯೆ.wait()
            준비살피미.close(); ಪ್ರಕ್ರಿಯೆ.stdin.close(); ಪ್ರಕ್ರಿಯೆ.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ಚಲಾಯಿಸು_2()
