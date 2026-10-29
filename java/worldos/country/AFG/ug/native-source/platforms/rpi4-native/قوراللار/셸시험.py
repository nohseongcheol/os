#!/usr/bin/env python3
"""자체 커널의 قاپ, 프로세스 입출력, Unicode GUI 터미널을 ھەقىقىي_مەلۇمات raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز, بۇيرۇق


def ئىجرا_قىل_2():
    출력결과 = كۆرسىتىش_يىلتىز / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    دەلىللەش_خەۋەر = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        جەريان = subprocess.Popen(بۇيرۇق()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(جەريان.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            مەلۇمات=bytearray(); تاماملىماق_ئاغما=time.monotonic()+시간제한
            while 확인표시 not in مەلۇمات:
                if time.monotonic()>تاماملىماق_ئاغما or جەريان.poll() is not None: raise AssertionError('UART timeout/exit: '+مەلۇمات.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: مەلۇمات.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in مەلۇمات or b'FAIL ' in مەلۇمات: raise AssertionError(مەلۇمات)
            return مەلۇمات.decode('utf-8','replace').replace('\r\n','\n')
        def ئەۋەتمەك(مەلۇمات, 확인표시=b'jkoros-native> '):
            جەريان.stdin.write(مەلۇمات); جەريان.stdin.flush(); return 수신하기(확인표시)
        def قاپ(قۇر, *예상결과):
            ئۆلچەم=ئەۋەتمەك(قۇر.encode()+b'\n')
            for قىممىتى in 예상결과: assert قىممىتى in ئۆلچەم, (قۇر,قىممىتى,ئۆلچەم)
            return ئۆلچەم
        def ھۆججەت(ئاتى):
            تېكىست=قاپ('hex '+ئاتى,'HEX BEGIN','HEX END'); ئىزدەش_ئۆلچەم=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',تېكىست,re.S)
            مەلۇمات=bytes.fromhex(''.join(ئىزدەش_ئۆلچەم.group(2).split())); assert len(مەلۇمات)==int(ئىزدەش_ئۆلچەم.group(1)); return مەلۇمات
        try:
            수신하기(b'jkoros-native> ')
            قاپ('mkdir 작업; cd 작업; pwd','/작업')
            قاپ('mkdir 하위; echo "한글 مەلۇمات 😀" > 인사.txt')
            assert ھۆججەت('인사.txt')=='한글 مەلۇمات 😀\n'.encode()
            قاپ('cp 인사.txt مىسال_قىممىتى.txt; mv مىسال_قىممىتى.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 مەلۇمات 😀')
            قاپ('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 مەلۇمات 😀','/작업/하위')
            قاپ('cd ..; rmdir 하위; echo $?','1\n')
            قاپ('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            قاپ('cp 인사.txt 인사.txt; echo $?','1\n'); assert ھۆججەت('인사.txt')=='한글 مەلۇمات 😀\n'.encode()
            قاپ('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ھۆججەت('인사.txt')
            قاپ("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ھۆججەت('리터럴')=='$인사\n누리\n'.encode()
            قاپ('echo one > جۈملە_قىممىتى; echo two >> جۈملە_قىممىتى; echo three >> جۈملە_قىممىتى')
            قاپ('cat < جۈملە_قىممىتى | grep t | tee 추림 | wc -l','2\n'); assert ھۆججەت('추림')==b'two\nthree\n'
            قاپ('head -n 1 جۈملە_قىممىتى > 앞; tail -n 1 جۈملە_قىممىتى > ئارقىغا_قىممىتى'); assert ھۆججەت('앞')==b'one\n'; assert ھۆججەت('뒤')==b'three\n'
            قاپ('grep absent جۈملە_قىممىتى; echo $?','1\n')
            قاپ('echo untouched > قوغدىماق_قىممىتى')
            قاپ('echo destroyed > قوغدىماق_قىممىتى |','명령이 빠졌습니다'); assert ھۆججەت('قوغدىماق_قىممىتى')==b'untouched\n'
            قاپ('echo "oops','따옴표가 닫히지 않았습니다')
            قاپ('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            قاپ('echo bad 2> قوغدىماق_قىممىتى','번호를 지정한 ھۆججەت 서술자 입출력 ئۆزگەرتمەك_ھالەت'); assert ھۆججەت('قوغدىماق_قىممىتى')==b'untouched\n'
            قاپ('rm 빈파일 리터럴 جۈملە_قىممىتى 추림 앞 ئارقىغا_قىممىتى قوغدىماق_قىممىتى')
            دەلىللەش_خەۋەر['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            قاپ("python -c 'print(123)' | wc -c",'4\n')
            قاپ("python -c 'print(456)' > ئەپ_f5044b9b.txt"); assert ھۆججەت('ئەپ_f5044b9b.txt')==b'456\n'
            قاپ("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            قاپ("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ئەپ_f5044b9b.txt", "b'456\\n'", "b''")
            قاپ("python -c 'print(\"x\"*17000)' | wc -c", 'خاتالىق -28')
            قاپ('echo recovered | wc -c','10\n')
            قاپ("python -c 'import jkoros; print(jkoros.read("+'"/작업/ئەپ_f5044b9b.txt"'+"))'",'456','exit 0')
            قاپ('cd /; javac Hello.java','Compiled:','exit 0')
            قاپ('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ھۆججەت('/작업/자바.txt')
            قاپ('cd 작업; echo "echo script > 실행결과" > بۇيرۇق.sh; echo "false || echo recovered >> 실행결과" >> بۇيرۇق.sh; sh بۇيرۇق.sh')
            assert ھۆججەت('실행결과')==b'script\nrecovered\n'
            قاپ('rm 실행결과; echo "exit 7" > چىقىش_ئەپ.sh; sh چىقىش_ئەپ.sh; echo $?','7\n')
            قاپ('rm چىقىش_ئەپ.sh بۇيرۇق.sh ئەپ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            دەلىللەش_خەۋەر['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            قاپ('echo history-proof','history-proof')
            ئۆلچەم=ئەۋەتمەك(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ئۆلچەم.count('history-proof')>=2, ئۆلچەم
            ئەۋەتمەك(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ئۆلچەم=ئەۋەتمەك(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ئۆلچەم, ئۆلچەم
            ئۆلچەم=ئەۋەتمەك(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ئۆلچەم,ئۆلچەم
            ئۆلچەم=ئەۋەتمەك('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ئۆلچەم,ئۆلچەم
            긴글='한글'*50
            ئۆلچەم=ئەۋەتمەك(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ئۆلچەم
            قاپ('terminal','TERMINAL READY')
            قاپ('clear')
            قاپ('echo "한글 تېرمىنال ABC xyz 012 😀"','한글 تېرمىنال ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ئابۇنىتېر:
                ئابۇنىتېر.settimeout(10); ئابۇنىتېر.connect(str(모의제어접속))
                with ئابۇنىتېر.makefile('rwb') as ئېقىم_قىممىتى:
                    json.loads(ئېقىم_قىممىتى.readline())
                    def 호출(ئاتى,دەلىل_رەت=None):
                        تور_ئۇچۇر={'execute':ئاتى}
                        if دەلىل_رەت: تور_ئۇچۇر['arguments']=دەلىل_رەت
                        ئېقىم_قىممىتى.write((json.dumps(تور_ئۇچۇر)+'\n').encode()); ئېقىم_قىممىتى.flush()
                        while True:
                            جاۋابلاش=json.loads(ئېقىم_قىممىتى.readline())
                            if 'error' in جاۋابلاش: raise AssertionError(جاۋابلاش)
                            if 'return' in جاۋابلاش: return جاۋابلاش['return']
                    호출('qmp_capabilities')
                    رەسىم=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(رەسىم),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    مەلۇمات=رەسىم.read_bytes().split(b'\n',3)[3]
                    def پىكسېل(x_كوردىنات,세로좌표): return tuple(مەلۇمات[(세로좌표*640+x_كوردىنات)*3:(세로좌표*640+x_كوردىنات)*3+3])
                    assert پىكسېل(12,48)==(32,80,144),پىكسېل(12,48)
                    assert len(set(پىكسېل(x_كوردىنات,세로좌표) for 세로좌표 in range(100,116) for x_كوردىنات in range(24,56)))>1,'Hangul glyphs missing'
                    قاپ('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    قاپ("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(رەسىم),'format':'ppm'})
                    복원자료=رەسىم.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    قاپ('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): قاپ('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ئەۋەتمەك(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ئۆلچەم=ئەۋەتمەك(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ئۆلچەم,ئۆلچەم
                    قاپ('rm visible.txt')
                    호출('quit')
            جەريان.wait(timeout=5)
            دەلىللەش_خەۋەر['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            دەلىللەش_خەۋەر['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if جەريان.poll() is None:
                جەريان.terminate()
                try: جەريان.wait(timeout=5)
                except subprocess.TimeoutExpired: جەريان.kill(); جەريان.wait()
            준비살피미.close(); جەريان.stdin.close(); جەريان.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(دەلىللەش_خەۋەر,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ئىجرا_قىل_2()
