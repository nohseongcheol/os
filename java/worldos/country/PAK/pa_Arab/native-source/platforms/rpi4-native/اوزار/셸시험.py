#!/usr/bin/env python3
"""자체 커널의 شیل, 프로세스 입출력, Unicode GUI 터미널을 اصلی_کوائف raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from نفاذ_کرو_حکم import 기준, حکم


def چلاؤ():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    جواز_دہی_رپورٹ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        عمل = subprocess.Popen(حکم()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(عمل.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            کوائف=bytearray(); ختم_کرو_آف_سیٹ=time.monotonic()+시간제한
            while 확인표시 not in کوائف:
                if time.monotonic()>ختم_کرو_آف_سیٹ or عمل.poll() is not None: raise AssertionError('UART timeout/exit: '+کوائف.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: کوائف.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in کوائف or b'FAIL ' in کوائف: raise AssertionError(کوائف)
            return کوائف.decode('utf-8','replace').replace('\r\n','\n')
        def بھیجو(کوائف, 확인표시=b'jkoros-native> '):
            عمل.stdin.write(کوائف); عمل.stdin.flush(); return 수신하기(확인표시)
        def شیل(لائن, *예상결과):
            결과=بھیجو(لائن.encode()+b'\n')
            for قدر in 예상결과: assert قدر in 결과, (لائن,قدر,결과)
            return 결과
        def فائل(ناں):
            متن=شیل('hex '+ناں,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',متن,re.S)
            کوائف=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(کوائف)==int(찾은결과.group(1)); return کوائف
        try:
            수신하기(b'jkoros-native> ')
            شیل('mkdir 작업; cd 작업; pwd','/작업')
            شیل('mkdir 하위; echo "한글 کوائف 😀" > 인사.txt')
            assert فائل('인사.txt')=='한글 کوائف 😀\n'.encode()
            شیل('cp 인사.txt نقل_قدر.txt; mv نقل_قدر.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 کوائف 😀')
            شیل('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 کوائف 😀','/작업/하위')
            شیل('cd ..; rmdir 하위; echo $?','1\n')
            شیل('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            شیل('cp 인사.txt 인사.txt; echo $?','1\n'); assert فائل('인사.txt')=='한글 کوائف 😀\n'.encode()
            شیل('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in فائل('인사.txt')
            شیل("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert فائل('리터럴')=='$인사\n누리\n'.encode()
            شیل('echo one > بیان_قدر; echo two >> بیان_قدر; echo three >> بیان_قدر')
            شیل('cat < بیان_قدر | grep t | tee 추림 | wc -l','2\n'); assert فائل('추림')==b'two\nthree\n'
            شیل('head -n 1 بیان_قدر > 앞; tail -n 1 بیان_قدر > پیچھے_قدر'); assert فائل('앞')==b'one\n'; assert فائل('뒤')==b'three\n'
            شیل('grep absent بیان_قدر; echo $?','1\n')
            شیل('echo untouched > حفاظت_کرو_قدر')
            شیل('echo destroyed > حفاظت_کرو_قدر |','명령이 빠졌습니다'); assert فائل('حفاظت_کرو_قدر')==b'untouched\n'
            شیل('echo "oops','따옴표가 닫히지 않았습니다')
            شیل('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            شیل('echo bad 2> حفاظت_کرو_قدر','번호를 지정한 فائل 서술자 입출력 سوئچ_کرو_موڈ'); assert فائل('حفاظت_کرو_قدر')==b'untouched\n'
            شیل('rm 빈파일 리터럴 بیان_قدر 추림 앞 پیچھے_قدر حفاظت_کرو_قدر')
            جواز_دہی_رپورٹ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            شیل("python -c 'print(123)' | wc -c",'4\n')
            شیل("python -c 'print(456)' > ایپ_f5044b9b.txt"); assert فائل('ایپ_f5044b9b.txt')==b'456\n'
            شیل("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            شیل("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ایپ_f5044b9b.txt", "b'456\\n'", "b''")
            شیل("python -c 'print(\"x\"*17000)' | wc -c", 'نقص -28')
            شیل('echo recovered | wc -c','10\n')
            شیل("python -c 'import jkoros; print(jkoros.read("+'"/작업/ایپ_f5044b9b.txt"'+"))'",'456','exit 0')
            شیل('cd /; javac Hello.java','Compiled:','exit 0')
            شیل('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in فائل('/작업/자바.txt')
            شیل('cd 작업; echo "echo script > 실행결과" > حکم.sh; echo "false || echo recovered >> 실행결과" >> حکم.sh; sh حکم.sh')
            assert فائل('실행결과')==b'script\nrecovered\n'
            شیل('rm 실행결과; echo "exit 7" > خارج_کرو_ایپ.sh; sh خارج_کرو_ایپ.sh; echo $?','7\n')
            شیل('rm خارج_کرو_ایپ.sh حکم.sh ایپ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            جواز_دہی_رپورٹ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            شیل('echo history-proof','history-proof')
            결과=بھیجو(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            بھیجو(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=بھیجو(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=بھیجو(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=بھیجو('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=بھیجو(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            شیل('terminal','TERMINAL READY')
            شیل('clear')
            شیل('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as گاہک:
                گاہک.settimeout(10); گاہک.connect(str(모의제어접속))
                with گاہک.makefile('rwb') as سٹریم_قدر:
                    json.loads(سٹریم_قدر.readline())
                    def 호출(ناں,دلیل_ایرے=None):
                        نیٹ_ورک_پیغام={'execute':ناں}
                        if دلیل_ایرے: نیٹ_ورک_پیغام['arguments']=دلیل_ایرے
                        سٹریم_قدر.write((json.dumps(نیٹ_ورک_پیغام)+'\n').encode()); سٹریم_قدر.flush()
                        while True:
                            جواب_دیوؤ=json.loads(سٹریم_قدر.readline())
                            if 'error' in جواب_دیوؤ: raise AssertionError(جواب_دیوؤ)
                            if 'return' in جواب_دیوؤ: return جواب_دیوؤ['return']
                    호출('qmp_capabilities')
                    نقش=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(نقش),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    کوائف=نقش.read_bytes().split(b'\n',3)[3]
                    def دانہ(x_محدد,세로좌표): return tuple(کوائف[(세로좌표*640+x_محدد)*3:(세로좌표*640+x_محدد)*3+3])
                    assert دانہ(12,48)==(32,80,144),دانہ(12,48)
                    assert len(set(دانہ(x_محدد,세로좌표) for 세로좌표 in range(100,116) for x_محدد in range(24,56)))>1,'Hangul glyphs missing'
                    شیل('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    شیل("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(نقش),'format':'ppm'})
                    복원자료=نقش.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    شیل('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): شیل('echo scroll-'+str(순번),'scroll-'+str(순번))
                    بھیجو(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=بھیجو(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    شیل('rm visible.txt')
                    호출('quit')
            عمل.wait(timeout=5)
            جواز_دہی_رپورٹ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            جواز_دہی_رپورٹ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if عمل.poll() is None:
                عمل.terminate()
                try: عمل.wait(timeout=5)
                except subprocess.TimeoutExpired: عمل.kill(); عمل.wait()
            준비살피미.close(); عمل.stdin.close(); عمل.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(جواز_دہی_رپورٹ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': چلاؤ()
